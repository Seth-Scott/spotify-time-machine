import requests
from bs4 import BeautifulSoup
import spotipy
import spotipy.util as util
import os

# billboard global variables
YEAR = input("What year do you want to time travel to? Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{YEAR}/"

# spotify global variables
USERNAME = os.getenv("USERNAME")
SCOPE = "playlist-modify-public"
TOKEN = util.prompt_for_user_token(username=USERNAME, scope=SCOPE)
sp = spotipy.Spotify(auth=TOKEN)


def scrape_billboard():
    """scrapes billboard for the given date"""
    response = requests.get(url=URL)
    website = response.text
    soup = BeautifulSoup(website, "html.parser")
    songs = soup.findAll(name="h3",
                         class_='c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 '
                                'lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 '
                                'u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 '
                                'u-max-width-230@tablet-only')
    song_list = [(song.getText().strip(), song.findNext("span").getText().replace("\n\t\n\t", "").replace("\n", "")) for
                 song in songs]
    return song_list


def create_playlist(year):
    """creates a playlist, generates a name"""
    created_playlist = sp.user_playlist_create(USERNAME, f"Billboard {YEAR}", public=True, collaborative=False,
                                               description=f'The Billboard top 100 for {YEAR}')
    return created_playlist["id"]


def add_tracks_to_playlist(playlist, songs):
    """adds the tracks from Billboard to the playlist"""
    uris = []
    for song in songs:
        results = sp.search(q=f'{song[0]},{song[1]}', type='track,artist', limit=1)

        try:
            uris.append(results["tracks"]["items"][0]["uri"].split(":")[2])
            print(f'{results["tracks"]["items"][0]["uri"].split(":")[2]}, success')
        except IndexError:
            print("song add failed")
            pass

    sp.user_playlist_add_tracks(user=USERNAME, playlist_id=playlist, tracks=uris)


new_playlist = create_playlist(YEAR)
scraped_songs = scrape_billboard()
add_tracks_to_playlist(new_playlist, scraped_songs)
