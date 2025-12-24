#pip install gTTS
from gtts import gTTS

#pip install pygame
from pygame import mixer

tts = gTTS(text='お元気ですか', lang='ja')
tts.save("good.mp3")

# mixer.init()
# mixer.music.load('good.mp3')
# mixer.music.play()

#pip install python-vlc
# import vlc
# p = vlc.MediaPlayer("good.mp3")
# p.play()