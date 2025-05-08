import tkinter as tk
from tkinter import filedialog, ttk
from utils.audio_utils import play_song, stop_song, pause_song, resume_song, set_volume
from utils.lyrics_fetcher import get_lyrics, fetch_lyrics_from_genius
import eyed3
import pygame
import time
import random
from PIL import Image, ImageTk
import os
from rapidfuzz import fuzz
from tkinterdnd2 import DND_FILES, TkinterDnD

def format_time(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def launch_ui():
    original_playlist = []
    shuffle_enabled = [False]
    repeat_enabled = [False]
    playlist = []
    current_index = [0]
    total_length = 0
    start_time = None

    def add_songs():
        files = filedialog.askopenfilenames(filetypes=[("MP3 Files", "*.mp3")])
        for file in files:
            playlist.append(file)
            original_playlist.append(file)
            playlist_box.insert(tk.END, os.path.basename(file))

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
        try:
            total_length = pygame.mixer.Sound(file_path).get_length()
        except:
            total_length = 0
        total_time_label.config(text=format_time(total_length))

        # Update "Now Playing"
        try:
            audio = eyed3.load(file_path)
            song_title = audio.tag.title if audio.tag and audio.tag.title else "Unknown Title"
            artist = audio.tag.artist if audio.tag and audio.tag.artist else "Unknown Artist"
        except:
            song_title, artist = "Unknown Title", "Unknown Artist"

        song_title_label.config(text=f"Title: {song_title}")
        artist_label.config(text=f"Artist: {artist}")
        duration_label.config(text=f"Duration: {format_time(total_length)}")

        update_progress()
        show_lyrics(file_path)
        show_album_art(file_path)

    def show_lyrics(file_path):
        lyrics = get_lyrics(file_path)
        if lyrics == "No embedded lyrics found.":
            try:
                audio = eyed3.load(file_path)
                song_title = audio.tag.title if audio.tag and audio.tag.title else "Unknown Title"
                artist_name = audio.tag.artist if audio.tag and audio.tag.artist else "Unknown Artist"
                lyrics = fetch_lyrics_from_genius(song_title, artist_name)
            except:
                lyrics = "Lyrics not found."
        lyrics_label.config(text=lyrics)

    def show_album_art(file_path):
        try:
            audio = eyed3.load(file_path)
            if audio.tag and audio.tag.images:
                image_data = audio.tag.images[0].image_data
                with open("temp_album.jpg", "wb") as img_file:
                    img_file.write(image_data)
                img = Image.open("temp_album.jpg")
                img = img.resize((150, 150))
                album_img = ImageTk.PhotoImage(img)
                album_art_label.config(image=album_img)
                album_art_label.image = album_img
            else:
                album_art_label.config(image="", text="No Album Art")
        except:
            album_art_label.config(image="", text="No Album Art")

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
            progress_percent = (elapsed / total_length) * 100 if total_length else 0
            progress_bar['value'] = min(progress_percent, 100)
            root.after(1000, update_progress)
        else:
            current_time_label.config(text="00:00")
            progress_bar['value'] = 0
            if repeat_enabled[0]:
                load_and_play(current_index[0])
            elif current_index[0] + 1 < len(playlist):
                next_song()

    def change_volume(val):
        volume = float(val) / 100
        set_volume(volume)

    def toggle_shuffle():
        shuffle_enabled[0] = not shuffle_enabled[0]
        if shuffle_enabled[0]:
            random.shuffle(playlist)
            shuffle_btn.config(text="Shuffle: ON")
        else:
            playlist.clear()
            playlist.extend(original_playlist)
            shuffle_btn.config(text="Shuffle: OFF")
        playlist_box.delete(0, tk.END)
        for file in playlist:
            playlist_box.insert(tk.END, os.path.basename(file))

    def toggle_repeat():
        repeat_enabled[0] = not repeat_enabled[0]
        repeat_btn.config(text="Repeat: ON" if repeat_enabled[0] else "Repeat: OFF")

    def save_playlist():
        file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text", "*.txt")])
        if file:
            with open(file, "w") as f:
                for song in original_playlist:
                    f.write(f"{song}\n")

    def load_playlist():
        file = filedialog.askopenfilename(filetypes=[("Text", "*.txt")])
        if file:
            playlist.clear()
            original_playlist.clear()
            playlist_box.delete(0, tk.END)
            with open(file, "r") as f:
                for line in f:
                    song = line.strip()
                    playlist.append(song)
                    original_playlist.append(song)
                    playlist_box.insert(tk.END, os.path.basename(song))

    def handle_key_press(event):
        key = event.keysym.lower()

        if key == "space":
            if pygame.mixer.music.get_busy():
                pause_song()
            else:
                resume_song()

        elif key == "right":
            next_song()

        elif key == "left":
            prev_song()

        elif key == "o" and (event.state & 0x4):  # Ctrl+O
            add_songs()

        elif key == "s" and (event.state & 0x4):  # Ctrl+S
            save_playlist()

    def handle_drop(event):
        files = root.tk.splitlist(event.data)
        for file in files:
            if file.lower().endswith(".mp3"):
                playlist.append(file)
                original_playlist.append(file)
                playlist_box.insert(tk.END, os.path.basename(file))

    # ---- Themes ----
    themes = {
        "dark": {
            "bg": "#202020",
            "fg": "white",
            "entry_bg": "#303030",
            "highlight": "#505050",
            "lyrics_fg": "lightgreen",
        },
        "light": {
            "bg": "#f0f0f0",
            "fg": "#000000",
            "entry_bg": "#ffffff",
            "highlight": "#cccccc",
            "lyrics_fg": "#006600",
        }
    }
    current_theme = ["dark"]

    def apply_theme(widget):
        theme = themes[current_theme[0]]
        for child in widget.winfo_children():
            try:
                if isinstance(child, tk.Label):
                    fg = theme["lyrics_fg"] if "lyrics" in str(child).lower() else theme["fg"]
                    child.configure(bg=theme["bg"], fg=fg)
                elif isinstance(child, tk.Entry):
                    child.configure(bg=theme["entry_bg"], fg=theme["fg"])
                elif isinstance(child, tk.Listbox):
                    child.configure(bg=theme["entry_bg"], fg=theme["fg"], selectbackground=theme["highlight"])
                elif isinstance(child, tk.Button):
                    child.configure(bg=theme["bg"], fg=theme["fg"])
                elif isinstance(child, tk.Scale):
                    child.configure(bg=theme["bg"], fg=theme["fg"])
                else:
                    child.configure(bg=theme["bg"])
            except:
                pass
            apply_theme(child)

    def toggle_theme():
        current_theme[0] = "light" if current_theme[0] == "dark" else "dark"
        apply_theme(root)

    # ---- UI ----
    root = TkinterDnD.Tk()
    root.title("Dubz Music Player")
    root.geometry("600x650")
    root.configure(bg="#202020")  # dark background

    now_playing_frame = tk.Frame(root, bg="#2a2a2a", pady=5)
    now_playing_frame.pack(fill="x")

    song_title_label = tk.Label(now_playing_frame, text="Title: -", bg="#2a2a2a", fg="white", font=("Helvetica", 10, "bold"))
    song_title_label.pack(side="left", padx=10)

    artist_label = tk.Label(now_playing_frame, text="Artist: -", bg="#2a2a2a", fg="white", font=("Helvetica", 10))
    artist_label.pack(side="left", padx=10)

    duration_label = tk.Label(now_playing_frame, text="Duration: 00:00", bg="#2a2a2a", fg="white", font=("Helvetica", 10))
    duration_label.pack(side="left", padx=10)

    # Search bar
    search_var = tk.StringVar()

    def filter_playlist(*args):
        query = search_var.get().lower()
        playlist_box.delete(0, tk.END)

        for file in playlist:
            filename = os.path.basename(file).lower()
            match_score = fuzz.partial_ratio(query, filename.lower())
            if match_score >= 70:
                playlist_box.insert(tk.END, os.path.basename(file))

    search_var.trace_add("write", filter_playlist)
    search_frame = tk.Frame(root)
    search_frame.pack(pady=5)

    search_entry = tk.Entry(search_frame, textvariable=search_var, width=45)
    search_entry.pack(side="left", padx=(0, 5))

    def clear_search():
        search_var.set("")
        search_entry.focus()

    tk.Button(search_frame, text="×", width=2, command=clear_search).pack(side="left")

    playlist_box = tk.Listbox(root, width=60, height=5)
    playlist_box.pack(pady=10)
    playlist_box.drop_target_register(DND_FILES)
    playlist_box.dnd_bind("<<Drop>>", handle_drop)

    album_art_label = tk.Label(root)
    album_art_label.pack(pady=5)

    lyrics_label = tk.Label(root, text="Lyrics will appear here.", wraplength=550, justify="left")
    lyrics_label.pack(padx=10, pady=10)

    time_frame = tk.Frame(root)
    time_frame.pack(pady=5)

    current_time_label = tk.Label(time_frame, text="00:00")
    current_time_label.pack(side="left", padx=10)

    progress_bar = ttk.Progressbar(time_frame, orient="horizontal", length=350, mode="determinate")
    progress_bar.pack(side="left")

    total_time_label = tk.Label(time_frame, text="00:00")
    total_time_label.pack(side="left", padx=10)

    volume_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", label="Volume", command=change_volume)
    volume_slider.set(50)
    volume_slider.pack(pady=10)

    controls = tk.Frame(root)
    controls.pack(pady=5)

    tk.Button(controls, text="Add Songs", command=add_songs).pack(side="left", padx=5)
    tk.Button(controls, text="Play", command=play_selected).pack(side="left", padx=5)
    tk.Button(controls, text="Next", command=next_song).pack(side="left", padx=5)
    tk.Button(controls, text="Prev", command=prev_song).pack(side="left", padx=5)

    shuffle_btn = tk.Button(controls, text="Shuffle: OFF", command=toggle_shuffle)
    shuffle_btn.pack(side="left", padx=5)

    repeat_btn = tk.Button(controls, text="Repeat: OFF", command=toggle_repeat)
    repeat_btn.pack(side="left", padx=5)

    tk.Button(controls, text="Save Playlist", command=save_playlist).pack(side="left", padx=5)
    tk.Button(controls, text="Load Playlist", command=load_playlist).pack(side="left", padx=5)

    tk.Button(root, text="Toggle Theme", command=toggle_theme).pack(pady=10)

    root.bind("<KeyPress>", handle_key_press)

    apply_theme(root)
    root.mainloop()
