import pygame
import eyed3
import tkinter as tk
from tkinter import filedialog

pygame.mixer.init()

def play_music(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def stop_music():
    pygame.mixer.music.stop()

def load_lyrics(file_path):
    audio_file = eyed3.load(file_path)
    lyrics = audio_file.tag.lyrics[0].text if audio_file.tag.lyrics else "No lyrics found"
    return lyrics

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*mp3")])
    if file_path:
        play_music(file_path)
        lyrics = load_lyrics(file_path)
        lyrics_label.config(text=lyrics)

