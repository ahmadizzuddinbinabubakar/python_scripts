import os
import subprocess
from moviepy.editor import VideoFileClip, concatenate_videoclips
from natsort import natsorted

# pip install moviepy
# pip install natsort
# change input folder, output folder, output file name at end of script
# python video_compilation.py

def combine_mp4_files(source_folder, output_folder, output_filename="combined_video.mp4"):
    """
    Combines all MP4 files from a source folder into a single video file,
    sorting them numerically by filename.

    Args:
        source_folder (str): The path to the folder containing the MP4 files.
        output_folder (str): The path where the combined video will be saved.
        output_filename (str): The name of the output video file.
    """
    # 1. Set source folder path
    print(f"Searching for MP4 files in: {source_folder}")

    # Create a list of all MP4 files in the source folder
    video_files = [os.path.join(source_folder, f) 
                   for f in os.listdir(source_folder) 
                   if f.lower().endswith('.mp4')]
    
    # Sort files naturally (numerically) to ensure correct ordering
    video_files = natsorted(video_files)
    
    if not video_files:
        print("No MP4 files found in the source folder.")
        return

    # 2. Set output folder path (create if it does not exist)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)
        print(f"Output folder '{output_folder}' created.")
    
    output_path = os.path.join(output_folder, output_filename)
    
    # 3. Combine the mp4 files in a loop
    video_clips = []
    for video_file in video_files:
        try:
            print(f"Adding {os.path.basename(video_file)}...")
            clip = VideoFileClip(video_file)
            video_clips.append(clip)
        except Exception as e:
            print(f"Could not read {video_file}. Error: {e}")
            
    if not video_clips:
        print("No video clips could be loaded for combining.")
        return

    print("Concatenating video clips...")
    final_clip = concatenate_videoclips(video_clips, method="compose")
    
    # 4. Output into output folder
    print(f"Writing combined video to: {output_path}")
    try:
        final_clip.write_videofile(output_path, codec="libx264")
        print("Video combination successful!")
    except Exception as e:
        print(f"An error occurred while writing the video file: {e}")
    finally:
        # Close all clips to free up resources
        for clip in video_clips:
            clip.close()

def combine_mp4_files_efficient(source_folder, output_folder, output_filename="combined_video.mp4", batch_size=100):
    """
    Combines all MP4 files in batches to conserve memory.
    """
    video_files = [os.path.join(source_folder, f) 
                   for f in os.listdir(source_folder) 
                   if f.lower().endswith('.mp4')]
    video_files = natsorted(video_files)
    
    if not video_files:
        print("No MP4 files found.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_path = os.path.join(output_folder, output_filename)
    
    final_clip = None
    
    for i in range(0, len(video_files), batch_size):
        batch_files = video_files[i:i + batch_size]
        clips_in_batch = []
        
        print(f"Processing batch {i//batch_size + 1}...")
        
        for video_file in batch_files:
            try:
                clip = VideoFileClip(video_file)
                clips_in_batch.append(clip)
            except Exception as e:
                print(f"Could not read {video_file}. Error: {e}")

        if clips_in_batch:
            batch_clip = concatenate_videoclips(clips_in_batch, method="compose")
            if final_clip is None:
                final_clip = batch_clip
            else:
                final_clip = concatenate_videoclips([final_clip, batch_clip], method="compose")
        
        for clip in clips_in_batch:
            clip.close()

    if final_clip:
        print(f"Writing combined video to: {output_path}")
        final_clip.write_videofile(output_path, codec="libx264")
        final_clip.close()
        print("Video combination successful!")
    else:
        print("No video clips could be loaded for combining.")

def combine_mp4_files_ffmpeg(source_folder, output_folder, output_filename="combined_video.mp4"):
    """
    Combines all MP4 files from a source folder into a single video file using ffmpeg.

    Args:
        source_folder (str): The path to the folder containing the MP4 files.
        output_folder (str): The path where the combined video will be saved.
        output_filename (str): The name of the output video file.
    """
    print(f"Searching for MP4 files in: {source_folder}")

    # Create a list of all MP4 files in the source folder
    video_files = [os.path.join(source_folder, f) 
                   for f in os.listdir(source_folder) 
                   if f.lower().endswith('.mp4')]
    
    # Sort files naturally (numerically) to ensure correct ordering
    video_files = natsorted(video_files)
    
    if not video_files:
        print("No MP4 files found in the source folder.")
        return

    # 2. Set output folder path (create if it does not exist)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)
        print(f"Output folder '{output_folder}' created.")
    
    output_path = os.path.join(output_folder, output_filename)
    
    # 3. Create a text file with the list of videos
    list_file_path = os.path.join(output_folder, "filelist.txt")
    with open(list_file_path, "w") as f:
        for video_file in video_files:
            f.write(f"file '{video_file}'\n")

    # 4. Use ffmpeg to concatenate the videos
    print("Concatenating video clips using ffmpeg...")
    try:
        command = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", list_file_path,
            "-c", "copy",
            output_path
        ]
        subprocess.run(command, check=True)
        print("Video combination successful!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running ffmpeg: {e}")
    except FileNotFoundError:
        print("ffmpeg not found. Please ensure ffmpeg is installed and in your system's PATH.")
    finally:
        # Clean up the temporary file list
        if os.path.exists(list_file_path):
            os.remove(list_file_path)        


if __name__ == "__main__":
    # --- Configuration ---
    # Replace these paths with your actual folder paths
    SOURCE_FOLDER = '<SOURCE_FOLDER>'
    OUTPUT_FOLDER = '<OUTPUT_FOLDER>'
    OUTPUT_FILENAME = "<OUTPUT_FILENAME>"
    
    # Run the function
    # combine_mp4_files_efficient(SOURCE_FOLDER, OUTPUT_FOLDER, OUTPUT_FILENAME)
    # combine_mp4_files(SOURCE_FOLDER, OUTPUT_FOLDER, OUTPUT_FILENAME)

    # Run the ffmpeg concatenation function
    combine_mp4_files_ffmpeg(SOURCE_FOLDER, OUTPUT_FOLDER, OUTPUT_FILENAME)
