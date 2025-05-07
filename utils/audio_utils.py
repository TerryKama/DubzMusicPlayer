import pygame

pygame.mixer.init()

def play_song(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def stop_song():
    pygame.mixer.music.stop()