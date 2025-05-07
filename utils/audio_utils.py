import pygame

pygame.mixer.init()

def play_song(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def stop_song():
    pygame.mixer.music.stop()

def pause_song():
    pygame.mixer.music.pause()

def resume_song():
    pygame.mixer.music.unpause()

def set_volume(volume):
    pygame.mixer.music.set_volume(volume)