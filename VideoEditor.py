import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

input_folder = '<input_folder>'
input_file_folder = '<input_file_folder>'
output_folder = '<output_folder>'

index = 0
tmp = 0
file_count = 0

#count number of files
for path in os.listdir(input_folder+input_file_folder):
    # check if current path is a file
    if os.path.isfile(os.path.join(input_folder+input_file_folder, path)):
        file_count += 1
print('File count:', file_count)

#concatenate videos
i = 0
while i < file_count:
    try:
        # Read files
        tmp_file_name = i + 1
        vid1 = VideoFileClip(input_folder + input_file_folder + "\\" + str(tmp_file_name) + ".mp4")
        tmp_file_name += 1
        vid2 = VideoFileClip(input_folder + input_file_folder + "\\" + str(tmp_file_name) + ".mp4")
        tmp_file_name += 1
        vid3 = VideoFileClip(input_folder + input_file_folder + "\\" + str(tmp_file_name) + ".mp4")
        # print(vid1.filename + "," + vid2.filename + "," + vid3.filename)

        i += 3
        # print(i)

        # # Concat them
        final = concatenate_videoclips([vid1, vid2, vid3])

        # # Write output to the file
        final.write_videofile(output_folder + "<file_name>" + "_" + str(index) + ".mp4")
        print("output: " + output_folder + "<file_name>" + "_" + str(index) + ".mp4")
        index += 1        

    except:
        print("error")
