from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "XXXXX"
CLIENT_SECRET = "XXX"

sp = spotipy.Spotify(
    auth_manager= SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username="XXXX", 
    )
)
user_id = sp.current_user()["id"]

selected_date = input("Please insert date in YYYY-MM-DD format: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{selected_date}/")
#print(f"https://www.billboard.com/charts/hot-100/{selected_date}/")
website = response.text

bb_site = BeautifulSoup(website, "html.parser")

list_scrapped = bb_site.select(selector="li h3", id="title-of-a-story")
songs_list = [song.get_text(strip=True) for song in list_scrapped]

song_uris = []
year = selected_date.split("-")[0]
for song in songs_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#print(songs_list)


playlist = sp.user_playlist_create(user=user_id, name=f"{selected_date} Billboard 100", public=False)
# print(playlist)

#print(song_uris[0:99])

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris[0:99])
