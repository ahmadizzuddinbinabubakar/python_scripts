import pandas as pd
import pyttsx3
import os

print("1. start")
# Declarations
input_folder = '<input_folder>'
input_file_name = '<input_file_name>'
input_file_ext = '.csv'
input_file_path = input_folder + input_file_name + input_file_ext
# 'F:\\programming\\python\\ExcelDataToAudio\\data\\nihongohack-data-hiragana.csv'

column1 = 'word'
column2 = 'reading'
column3 = 'meaning'
# column4 = 'kun readings'

output_folder = '<output_folder>'
output_file_name = input_file_name
output_file_ext = '.mp3'
# output_file_ext = '.wav'
# output_file_path = input_folder + input_file_name + input_file_ext
print("2. declarations ok")

# Create file folder
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
print("3. create folder ok folder existed")    

# Read CSV file from a folder
df = pd.read_csv(input_file_path)
# df = pd.read_csv(input_file_path, header=None, skiprows=1, usecols=["symbol"])
# df = pd.read_csv(input_file_path, usecols=['symbol'])
print("4. read csv ok")

# converting column data to list
c1 = df[column1].tolist()
# c2 = df[column2].tolist()
# c3 = df[column3].tolist()
# c4 = df[column4].tolist()
print("5. convert column to list ok")

# Display the DataFrame
# print(df)
# print(symbol)


# initialize Text-to-speech engine
engine = pyttsx3.init()
print("6. initialize tts ok")

# set speed
engine.setProperty('rate', 135)
engine.setProperty('volume', 1)

# get details of all voices available & set voice
voices = engine.getProperty("voices")
print("7. setup tts ok")

count = 0
for word in c1:
  output_file_path = output_folder + output_file_name +'-' + column1 + '-' + str(count) + output_file_ext
  engine.setProperty('voice',voices[2].id) #japanese
  engine.save_to_file(word, output_file_path)
  engine.runAndWait()
  print(output_file_path)
  print(word)
  count = count + 1
print("8. convert column1 ok")  