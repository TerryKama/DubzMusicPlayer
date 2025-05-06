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

root = tk.Tk()
root.title("DubzMusicPlayer")

lyrics_label = tk.Label(root, text="Lyrics will appear here.", justify="left", width=50, height=10)
lyrics_label.pack()

open_button = tk.Button(root, text="Open Song", command=open_file)
open_button.pack()

stop_button = tk.Button(root, text="Stop Music", command=stop_music)
stop_button.pack()

root.mainloop()