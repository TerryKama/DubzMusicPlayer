import tkinter as tk
from tkinter import filedialog
from utils.audio_utils import play_song, stop_song
from utils.lyrics_fetcher import get_lyrics

def launch_ui():
    def open_file():
        file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if file_path:
            play_song(file_path)
            lyrics = get_lyrics(file_path)
            lyrics_label.config(text=lyrics)

    root = tk.Tk()
    root.title("Dubz Music Player")

    lyrics_label = tk.Label(root, text="Lyrics will appear here.", wraplength=400, justify="left")
    lyrics_label.pack(padx=10, pady=10)

    tk.Button(root, text="Open Song", command=open_file).pack(pady=5)
    tk.Button(root, text="Stop", command=stop_song).pack(pady=5)

    root.mainloop()