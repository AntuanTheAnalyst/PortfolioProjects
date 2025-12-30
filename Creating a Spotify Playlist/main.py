import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import json

SPOTIPY_REDIRECT_URI = os.environ.get("SPOTIPY_REDIRECT_URI")
SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com/callback",
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
    )
)
user_id = sp.current_user()["id"]

year_info = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
# input_year = 2005-01-15
URL = f"https://www.billboard.com/charts/hot-100/{year_info}/"

HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/136.0.0.0 Safari/537.36"
}

response = requests.get(URL, headers=HEADER)
songs_web_page = response.text
soup = BeautifulSoup(songs_web_page, "html.parser")

song_names_tag = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_tag]
# print(song_names)

year = year_info.split("-")[0]

song_uris = []
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track", limit=1)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"'{song}' not found on Spotify. Skipping.")

print("Found URIs:", song_uris)

play_list = sp.user_playlist_create(user=user_id, name=f"{year_info} Billboard 100",
                                    public=False, collaborative=False, description=f"Some songs from {year}")
play_list_id = play_list['id']

sp.playlist_add_items(playlist_id=play_list_id, items=song_uris, position=None)

playlist_url = play_list["external_urls"]['spotify']
print(f"Your playlist: {playlist_url}")
