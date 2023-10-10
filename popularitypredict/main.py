from decouple import Config
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import json
load_dotenv()

CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CLIENT_ID = os.getenv('CLIENT_ID')
REDIRECT_URI = os.getenv('REDIRECT_URI')

sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI)

access_token_info = sp_oauth.get_cached_token()
if access_token_info:
    access_token = access_token_info['access_token']
else:
    access_token = None

if access_token:
    sp = spotipy.Spotify(auth=access_token)
track_id='7x9aauaA9cu6tyfpHnqDLo'
# Create a large dataset by combining different playlists

playlist1 = sp.playlist_tracks(playlist_id="37i9dQZEVXbMDoHDwVN2tF", fields=None)
# print(playlist1)
audio_feature = sp.audio_features(tracks=[track_id])
# print(audio_feature)


print(len(playlist1['items']))

def create_table(playlist):
    data = []
    for track in playlist:
        info = track['track']
        artists = ""
        total_followers = 0
        for artist in info['artists']:
            artists += artist['name'] + ", "
            total_followers += sp.artist(artist['id'])['followers']['total']
        track_audio = []
        for feature in list(sp.audio_features(tracks=[info['id']])[0].values())[:11]:
            track_audio.append(feature)
        track_detail = [info['id'], info['name'], artists, total_followers,
                        info['popularity']]
        track_detail.extend(track_audio)
        data.append(track_detail)
    columns = ['ID', 'Song Name', 'Artists', 'Followers', 'Popularity']
    columns.extend(list(sp.audio_features(tracks=[track_id])[0].keys())[:11])

    df = pd.DataFrame(data=data, columns=columns)
    return df

data = create_table(playlist1['items'])
print(data.head())

