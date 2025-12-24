import pyttsx3

# initialize Text-to-speech engine
engine = pyttsx3.init()

# set speed
engine.setProperty('rate', 135)

# get details of all voices available & set voice
voices = engine.getProperty("voices")
# # print(voices[2].id)
# engine.setProperty('voice',voices[2].id)

# # convert this text to speech
# text = "おはようございます！ 調理場を見てもいいですか？"
# engine.say(text)

# # saving speech audio into a file
# engine.save_to_file(text, "python.mp3")
# # engine.runAndWait()

# # play the speech
# engine.runAndWait()


engine.setProperty('voice',voices[0].id)

# convert this text to speech
text = "kun readings"
# engine.say(text)
engine.save_to_file(text, "kun-readings.mp3")
engine.runAndWait()
