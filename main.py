import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json


# Get top 100 song from billboard music chart

year = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

billboard_url = "https://www.billboard.com/charts/hot-100/"+year
response = requests.get(billboard_url)

soup = BeautifulSoup(response.text, "html.parser")
data = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
songs = [song.string for song in data]

# Spotify API

client_id = YOUR_CLIENT_ID
client_secret = YOUR_CLIENT_SECRET

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            scope="playlist-modify-private",
            redirect_uri="http://example.com",
            client_id=client_id,
            client_secret=client_secret,
            show_dialog=True,
            cache_path="token.txt"
        )
    )
user_id = sp.current_user()['id']
year = year.split('-')[0]

song_uri = []
for song in songs:
    result = sp.search(q=f"track:{song} year:{year}", type='track')
    try:
        uri = result['tracks']['items'][0]['uri']
        song_uri.append(uri)
    except IndexError:
        print(f"{song} doesnt exist in spotify. Skipped!")

playlist = sp.user_playlist_create(user=user_id, name=f"{year} Billboard 100 - Python Project", public=False)
print(playlist)
sp.playlist_add_items(playlist_id=playlist['id'], items=song_uri)
