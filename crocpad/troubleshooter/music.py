import pygame
import threading
from threading import Thread

freq = 44100    # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2    # 1 is mono, 2 is stereo
buffer = 1024   # number of samples
volume = 1      # float from 0 to 1

class StopMusic(Exception):
	pass
	
def play_music(music_file):
    clock = pygame.time.Clock()
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        clock.tick(30)

def st(music_file):
	pygame.mixer.init(freq, bitsize, channels, buffer)
	pygame.mixer.music.set_volume(volume)
	try:
	    play_music(music_file)
	except StopMusic:
	    pygame.mixer.music.fadeout(1000)
	    pygame.mixer.music.stop()
	    raise SystemExit

def play(midi):
  t = Thread(target=st, args=(midi,))
  t.start()
  return t
