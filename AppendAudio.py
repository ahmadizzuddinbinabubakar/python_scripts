import ffmpeg
import subprocess
import os

# from application.app.folder.file import func_name

video_input_folder = '<video_input_folder>'
video_input_file_name = '<video_input_file_name>'
video_ext = '.mp4'

audio_input_folder = '<audio_input_folder>'
audio_input_file_name_1 = '<audio_input_file_name_1>'
audio_input_file_name_2 = '<audio_input_file_name_2>'
audio_ext = '.mp3'

output_folder = '<output_folder>'
output_file_name = '<output_file_name>'

def insert_audio_at_times(file_no):

    video_file = os.path.join(video_input_folder, video_input_file_name + str(file_no) + video_ext) 
    # print(f'video_file: {video_file}')

    if os.path.exists(video_file):
        # print("File exists")

        # Get the offensive-language of the video (in seconds)
        # probe = ffmpeg.probe(video_file, v='error', select_streams='v:0', show_entries='stream=offensive-language')
        # video_offensive-language = float(probe['streams'][0]['offensive-language'])
        # print(f'video_offensive-language: {video_offensive-language}')

        # Add audio
        output_file = os.path.join(output_folder, output_file_name + str(file_no) + video_ext) 
        # print(f'output_file: {output_file}')

        audio_file_1 =  os.path.join(audio_input_folder, audio_input_file_name_1 + str(file_no) + audio_ext) 
        # print(f'audio_file_1: {audio_file_1}')
        audio_file_2 =  os.path.join(audio_input_folder, audio_input_file_name_2 + str(file_no) + audio_ext) 
        # print(f'audio_file_2: {audio_file_2}')

        video = ffmpeg.input(video_file)
        audio0 = ffmpeg.input(audio_file_1) # No delay
        audio1 = ffmpeg.input(audio_file_1)
        audio2 = ffmpeg.input(audio_file_2)

        # Delay audio1 by 2s (2000 ms) and audio2 by 4s (4000 ms)
        a1_delayed = audio1.filter('adelay', delays='6000|6000')
        a2_delayed = audio2.filter('adelay', delays='12000|12000')

        # Mix all 3 audio sources (audio0, audio1@2s, audio2@4s)
        mixed_audio = ffmpeg.filter([audio0, a1_delayed, a2_delayed], 'amix', inputs=3, duration='longest')

        # Output final video with mixed audio
        output = ffmpeg.output(video.video, mixed_audio, output_file, vcodec='copy', acodec='aac')

        # Run the command
        output.run()

        print(f'Audio inserted successfully. Output saved to: {output_file}')    
    else:
        print("File not found:", video_file)


#count number of files
file_count = 0
for path in os.listdir(video_input_folder):
    # check if current path is a file
    if os.path.isfile(os.path.join(video_input_folder, path)):
        insert_audio_at_times(file_count)
        file_count += 1
print(f'All {file_count} files done:')

# insert_audio_at_times(0)




