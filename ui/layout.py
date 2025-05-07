import tkinter as tk
from tkinter import filedialog
from utils.audio_utils import play_song, stop_song, resume_song, pause_song, set_volume
from utils.lyrics_fetcher import get_lyrics, fetch_lyrics_from_genius
import eyed3
import pygame
import time

def launch_ui():
    def open_file():
        file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if file_path:
            play_song(file_path)
            update_progress_bar(file_path)

            lyrics = get_lyrics(file_path)

            if lyrics == "No embedded lyrics found.":
                audio = eyed3.load(file_path)
                song_title = audio.tag.title if audio.tag.title else "Unknown Title"
                artist_name = audio.tag.artist if audio.tag.artist else "Unknown Artist"
                lyrics = fetch_lyrics_from_genius(song_title, artist_name)
            lyrics_label.config(text=lyrics)

    def update_progress_bar(file_path):
        total_length = pygame.mixer.music.get_length()
        start_time = time.time()

        def update():
            elapsed_time = time.time() - start_time
            progress = elapsed_time / total_length * 100
            progress_var.set(progress)
            if pygame.mixer.music.get_busy():
                root.after(1000, update)
        update()

    def change_volume(val):
        volume = float(val) / 100
        set_volume(volume)

    root = tk.Tk()
    root.title("Dubz Music Player")

    lyrics_label = tk.Label(root, text="Lyrics will appear here.", wraplength=400, justify="left")
    lyrics_label.pack(padx=10, pady=10)

    progress_var = tk.DoubleVar()
    progress_bar = tk.Scale(root, variable=progress_var, from_=0, to=100, orient="horizontal", length=300, showvalue=False)
    progress_bar.pack(padx=10, pady=10)

    volume_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", label="Volume", command=change_volume)
    volume_slider.set(50)
    volume_slider.pack(padx=10, pady=10)

    tk.Button(root, text="Open Song", command=open_file).pack(pady=5)
    tk.Button(root, text="Pause", command=pause_song).pack(pady=5)
    tk.Button(root, text="Resume", command=resume_song).pack(pady=5)
    tk.Button(root, text="Stop", command=stop_song).pack(pady=5)

    root.mainloop()