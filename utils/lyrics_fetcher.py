import eye3
import os

def get_lyrics(file_path):
    audio = eye3.load(file_path)
    if audio.tag and audio.tag.lyrics:
        return audio.tag.lyrics[0].text
    return "No embedded lyrics found."