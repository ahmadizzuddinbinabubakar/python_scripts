import os
from pydub import AudioSegment

# pip install pydub
# pip install audioop-lts
# python IncreaseMP3Volume.py


def increase_volume(input_dir, output_dir, volume_percentage):
    """
    Increases the volume of all MP3 files in a folder and saves them to a new location.
    
    Args:
        input_dir (str): The path to the folder containing the MP3 files.
        output_dir (str): The path to the folder where the processed files will be saved.
        volume_percentage (float): The percentage to increase the volume by (e.g., 200 for 200%).
    """
    
    # A 200% increase is roughly a +6 dB gain, as doubling the amplitude
    # is approximately 6.02 dB (20 * log10(2)).
    db_increase = 6 * (volume_percentage / 100.0)

    # Ensure the output directory exists. If not, create it.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Process each file in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".mp3"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            try:
                # Load the mp3 file
                audio = AudioSegment.from_mp3(input_path)
                
                # Increase the volume
                louder_audio = audio + db_increase
                
                # Export the processed audio to the output directory
                louder_audio.export(output_path, format="mp3")
                print(f"Processed '{filename}' -> Saved to '{output_path}'")
                
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    # --- Set your folder paths and volume here ---
    input_folder = '<input_folder>'
    output_folder = '<output_folder>'
    volume_increase_percent = 200

    increase_volume(input_folder, output_folder, volume_increase_percent)
