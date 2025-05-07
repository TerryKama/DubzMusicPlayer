import eyed3
import os
import requests
from urllib.parse import quote

GENIUS_API_KEY = 'u7Ij4hLJSPXAuEGWNmvYqLoBvZJ52z74wYViX55PLpiBW0IgJmMk67ytcXoI3I7bj3d7EehZrXed-t72S7sDww'
GENIUS_API_URL = 'https://api.genius.com'

def fetch_lyrics_from_genius(song_title, artist_name):
    song_title = quote(song_title)
    artist_name = quote(artist_name)
    search_url = f"{GENIUS_API_URL}/search?q{song_title} {artist_name}"
    headers = {'Authorisation': f'Bearer {GENIUS_API_KEY}'}

    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        if result['response']['hits']:
            song_info = result['response']['hits'][0]['result']
            song_url = song_info['url']
            return song_url
        else:
            return "Lyrics not found."
    else:
        return "Error fetching lyrics"
    
def get_lyrics(file_path):
    audio = eyed3.load(file_path)
    if audio.tag and audio.tag.lyrics:
        return audio.tag.lyrics[0].text
    return "No embedded lyrics found."