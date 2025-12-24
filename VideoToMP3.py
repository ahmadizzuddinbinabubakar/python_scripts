import os
from moviepy.editor import VideoFileClip

def convert_mp4s_to_mp3(input_video_dir, output_mp3_dir):
    """
    Converts all MP4 files from a source folder to MP3 files in a destination folder.

    Args:
        input_video_dir (str): The path to the folder containing your MP4 videos.
        output_mp3_dir (str): The path to the folder where the MP3 files will be saved.
    """
    
    # Check if the input directory exists
    if not os.path.isdir(input_video_dir):
        print(f"Error: Input video directory not found at {input_video_dir}")
        return

    # Create the output directory if it does not exist
    if not os.path.exists(output_mp3_dir):
        os.makedirs(output_mp3_dir)
        print(f"Created output directory at {output_mp3_dir}")

    print(f"Starting conversion for MP4 files in: {input_video_dir}\n")
    
    # Get a list of all files in the input directory
    for filename in os.listdir(input_video_dir):
        # Check if the file is an MP4
        if filename.lower().endswith('.mp4'):
            try:
                # Construct the full input and output file paths
                mp4_file_path = os.path.join(input_video_dir, filename)
                
                # Get the filename without the extension and add the new extension
                mp3_filename = os.path.splitext(filename)[0] + ".mp3"
                mp3_file_path = os.path.join(output_mp3_dir, mp3_filename)

                print(f"Converting '{filename}' to '{mp3_filename}'...")
                
                # Create a VideoFileClip and write the audio to an MP3 file
                video_clip = VideoFileClip(mp4_file_path)
                video_clip.audio.write_audiofile(mp3_file_path, codec='mp3')
                
                print(f"Successfully converted '{filename}'.")
                
                # Close the clips to free up resources
                video_clip.close()

            except Exception as e:
                print(f"Error converting '{filename}': {e}")
                
    print("\nConversion process complete!")

# --- Example Usage ---
# Replace 'path/to/your/videos' and 'path/to/your/mp3s' with the actual directories
input_folder = 'path/to/your/videos'
output_folder = 'path/to/your/mp3s'

convert_mp4s_to_mp3(input_folder, output_folder)
