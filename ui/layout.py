import tkinter as tk
from tkinter import filedialog, ttk
from utils.audio_utils import play_song, stop_song, pause_song, resume_song, set_volume
from utils.lyrics_fetcher import get_lyrics, fetch_lyrics_from_genius
import eyed3
import pygame
import time
import threading

def format_time(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def launch_ui():
    current_file_path = None
    start_time = None
    total_length = 0

    def open_file():
        nonlocal current_file_path, start_time, total_length

        file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if file_path:
            current_file_path = file_path
            play_song(file_path)
            start_time = time.time()

            # Get total duration of song
            total_length = pygame.mixer.Sound(file_path).get_length()
            total_time_label.config(text=format_time(total_length))

            update_progress()

            # Load lyrics
            lyrics = get_lyrics(file_path)
            if lyrics == "No embedded lyrics found.":
                audio = eyed3.load(file_path)
                song_title = audio.tag.title if audio.tag and audio.tag.title else "Unknown Title"
                artist_name = audio.tag.artist if audio.tag and audio.tag.artist else "Unknown Artist"
                lyrics = fetch_lyrics_from_genius(song_title, artist_name)

            lyrics_label.config(text=lyrics)

    def update_progress():
        if pygame.mixer.music.get_busy():
            elapsed = time.time() - start_time
            current_time_label.config(text=format_time(elapsed))
            progress_percent = (elapsed / total_length) * 100
            progress_bar['value'] = min(progress_percent, 100)
            root.after(1000, update_progress)
        else:
            progress_bar['value'] = 0
            current_time_label.config(text="00:00")

    def change_volume(val):
        volume = float(val) / 100
        set_volume(volume)

    root = tk.Tk()
    root.title("Dubz Music Player")
    root.geometry("500x500")

    # Lyrics display
    lyrics_label = tk.Label(root, text="Lyrics will appear here.", wraplength=450, justify="left")
    lyrics_label.pack(padx=10, pady=10)

    # Playback time labels and progress bar
    time_frame = tk.Frame(root)
    time_frame.pack(pady=5)

    current_time_label = tk.Label(time_frame, text="00:00")
    current_time_label.pack(side="left", padx=10)

    progress_bar = ttk.Progressbar(time_frame, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(side="left")

    total_time_label = tk.Label(time_frame, text="00:00")
    total_time_label.pack(side="left", padx=10)

    # Volume slider
    volume_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", label="Volume", command=change_volume)
    volume_slider.set(50)
    volume_slider.pack(pady=10)

    # Playback controls
    controls_frame = tk.Frame(root)
    controls_frame.pack(pady=10)

    tk.Button(controls_frame, text="Open Song", command=open_file).pack(side="left", padx=5)
    tk.Button(controls_frame, text="Pause", command=pause_song).pack(side="left", padx=5)
    tk.Button(controls_frame, text="Resume", command=resume_song).pack(side="left", padx=5)
    tk.Button(controls_frame, text="Stop", command=stop_song).pack(side="left", padx=5)

    root.mainloop()
