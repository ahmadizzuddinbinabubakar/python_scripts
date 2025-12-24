import os
import datetime
import shutil
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

#todo: pip install --upgrade google-api-python-client google-auth google-auth-oauthlib
#cd F:\programming\python\YoutubeScheduler    
#run: python youtube_upload.py

# YouTube API scope and client secrets
SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube"  # full access to manage playlists
         ] 
CLIENT_SECRETS_FILE = "client_secrets.json"
CREDENTIALS_FILE = "youtube_token.json"

def authenticate_youtube():
    creds = None
    
    # Check if token file exists and load credentials from it
    if os.path.exists(CREDENTIALS_FILE):
        creds = Credentials.from_authorized_user_file(CREDENTIALS_FILE, SCOPES)

    # If no valid credentials, refresh the token or prompt for new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())  # Try refreshing the token
            except Exception as e:
                print(f"Error refreshing token: {e}")
                creds = None
        if not creds or not creds.valid:
            # Token is expired or invalid, re-authenticate the user
            print("Authentication required. Please log in.")
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)  # This opens a web browser for authentication

        # Save the credentials for future use
        with open(CREDENTIALS_FILE, "w") as token:
            token.write(creds.to_json())

    # Return the authenticated YouTube API client
    return build("youtube", "v3", credentials=creds)

def select_videos(video_folder, count=10):
    videos = [f for f in os.listdir(video_folder) if f.lower().endswith(('.mp4', '.mov', '.avi'))]
    videos.sort()  # You can customize sorting logic
    return videos[:count]

def schedule_date(date_str):
    # Input format: "31-07-2025"
    try:
        dt = datetime.datetime.strptime(date_str, "%d-%m-%Y")
        # Schedule time is set to 12:00 UTC (you can change this if needed)
        dt = dt.replace(hour=12, minute=0, second=0)
        return dt.isoformat() + "Z"
    except ValueError:
        raise ValueError("Invalid date format. Use DD-MM-YYYY.")

def upload_video(youtube, file_path, title, playlist_id, scheduled_time):
    request_body = {
        "snippet": {
            "title": title,
            "description": "<description>",
            "tags": ["<tag1>", "<tag2>"],
            "categoryId": "27",  # Education
        },
        "status": {
            "privacyStatus": "private",  # will be scheduled to become public
            "publishAt": scheduled_time,
            "selfDeclaredMadeForKids": False,
        }
    }

    media_file = MediaFileUpload(file_path, chunksize=-1, resumable=True)

    video_response = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    ).execute()

    video_id = video_response["id"]

    # Add video to playlist
    youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    ).execute()

    return video_id

def move_to_archive(video_path, archive_folder):
    os.makedirs(archive_folder, exist_ok=True)
    shutil.move(video_path, os.path.join(archive_folder, os.path.basename(video_path)))

def main(video_folder, archive_folder, playlist_id, schedule_date_str):
    youtube = authenticate_youtube()

    videos_to_upload = select_videos(video_folder, count=10)
    if not videos_to_upload:
        print("No videos found to upload.")
        return

    publish_time = schedule_date(schedule_date_str)

    for video_file in videos_to_upload:
        full_path = os.path.join(video_folder, video_file)
        print(f"Uploading: {video_file}")
        try:
            upload_video(youtube, full_path, video_file, playlist_id, publish_time)
            move_to_archive(full_path, archive_folder)
            print(f"Uploaded and moved to archive: {video_file}")
        except Exception as e:
            print(f"Error uploading {video_file}: {e}")

if __name__ == "__main__":
    VIDEO_FOLDER = r"<VIDEO_FOLDER>"  # Change this to your input folder
    ARCHIVE_FOLDER = r"<ARCHIVE_FOLDER>" # Where to move after upload
    PLAYLIST_ID = "<PLAYLIST_ID>"  # Set this to your actual playlist ID
    SCHEDULE_DATE = "04-08-2027"  # DD-MM-YYYY format

    #REMINDER: 
    # 1. Change schedule_date
    # 2. Change playlist_id for different playlists
    # 2. CHANGE DETAILS IN upload_video FOR DIFFERENT PLAYLIST

    main(VIDEO_FOLDER, ARCHIVE_FOLDER, PLAYLIST_ID, SCHEDULE_DATE)
