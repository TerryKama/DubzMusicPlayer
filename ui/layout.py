import tkinter as tk
from tkinter import filedialog, ttk
from utils.audio_utils import play_song, stop_song, pause_song, resume_song, set_volume
from utils.lyrics_fetcher import get_lyrics, fetch_lyrics_from_genius
import eyed3
import pygame
import time
import random
from PIL import Image, ImageTk

def format_time(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def launch_ui():
    playlist = []
    current_index = [0]  # use list to make it mutable in nested functions
    total_length = 0
    start_time = None

    def add_songs():
        files = filedialog.askopenfilenames(filetypes=[("MP3 Files", "*.mp3")])
        for file in files:
            playlist.append(file)
            playlist_box.insert(tk.END, file.split("/")[-1] if "/" in file else file.split("\\")[-1])

    def play_selected():
        idx = playlist_box.curselection()
        if idx:
            current_index[0] = idx[0]
            load_and_play(current_index[0])

    def load_and_play(index):
        nonlocal start_time, total_length
        if index < 0 or index >= len(playlist):
            return
        file_path = playlist[index]
        play_song(file_path)
        start_time = time.time()
        total_length = pygame.mixer.Sound(file_path).get_length()
        total_time_label.config(text=format_time(total_length))
        update_progress()
        show_lyrics(file_path)

    def show_lyrics(file_path):
        lyrics = get_lyrics(file_path)
        if lyrics == "No embedded lyrics found.":
            audio = eyed3.load(file_path)
            song_title = audio.tag.title if audio.tag and audio.tag.title else "Unknown Title"
            artist_name = audio.tag.artist if audio.tag and audio.tag.artist else "Unknown Artist"
            lyrics = fetch_lyrics_from_genius(song_title, artist_name)
        lyrics_label.config(text=lyrics)

    def next_song():
        if current_index[0] + 1 < len(playlist):
            current_index[0] += 1
            load_and_play(current_index[0])

    def prev_song():
        if current_index[0] - 1 >= 0:
            current_index[0] -= 1
            load_and_play(current_index[0])

    def update_progress():
        if pygame.mixer.music.get_busy():
            elapsed = time.time() - start_time
            current_time_label.config(text=format_time(elapsed))
            progress_percent = (elapsed / total_length) * 100
            progress_bar['value'] = min(progress_percent, 100)
            root.after(1000, update_progress)
        else:
            current_time_label.config(text="00:00")
            progress_bar['value'] = 0
            if current_index[0] + 1 < len(playlist):
                next_song()

    def change_volume(val):
        volume = float(val) / 100
        set_volume(volume)

    root = tk.Tk()
    root.title("Dubz Music Player")
    root.geometry("600x600")

    # Playlist box
    playlist_box = tk.Listbox(root, width=60, height=5)
    playlist_box.pack(pady=10)

    # Lyrics display
    lyrics_label = tk.Label(root, text="Lyrics will appear here.", wraplength=550, justify="left")
    lyrics_label.pack(padx=10, pady=10)

    # Time and progress bar
    time_frame = tk.Frame(root)
    time_frame.pack(pady=5)

    current_time_label = tk.Label(time_frame, text="00:00")
    current_time_label.pack(side="left", padx=10)

    progress_bar = ttk.Progressbar(time_frame, orient="horizontal", length=350, mode="determinate")
    progress_bar.pack(side="left")

    total_time_label = tk.Label(time_frame, text="00:00")
    total_time_label.pack(side="left", padx=10)

    # Volume slider
    volume_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", label="Volume", command=change_volume)
    volume_slider.set(50)
    volume_slider.pack(pady=10)

    # Controls
    controls = tk.Frame(root)
    controls.pack(pady=5)

    tk.Button(controls, text="Add Songs", command=add_songs).pack(side="left", padx=5)
    tk.Button(controls, text="Play Selected", command=play_selected).pack(side="left", padx=5)
    tk.Button(controls, text="Previous", command=prev_song).pack(side="left", padx=5)
    tk.Button(controls, text="Next", command=next_song).pack(side="left", padx=5)
    tk.Button(controls, text="Pause", command=pause_song).pack(side="left", padx=5)
    tk.Button(controls, text="Resume", command=resume_song).pack(side="left", padx=5)
    tk.Button(controls, text="Stop", command=stop_song).pack(side="left", padx=5)

    root.mainloop()
