import os
import pandas as pd
import spotipy
from spotipy import SpotifyClientCredentials
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

client_credential_manager = SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credential_manager)

artists = [
'x'
]

def get_features(tracks_id):
    track = sp.track(tracks_id)
    audio_features =  sp.audio_features(tracks_id)

    # Check if audio_features is None
    if audio_features is None:
        return None

    # Get the features from the Track info
    track_id = track['id']
    track_name = track['name']
    length = track['duration_ms']
    track_popularity = track['popularity']
    release_date = track['album']['release_date']
    album_id = track['album']['id']
    album_name = track['album']['name']
    artist_name = track['album']['artists'][0]['name']

    # Get the features from the Audio Features object
    acousticness = audio_features[0]['acousticness']
    danceability = audio_features[0]['danceability']
    energy = audio_features[0]['energy']
    instrumentalness = audio_features[0]['instrumentalness']
    liveness = audio_features[0]['liveness']
    speechiness = audio_features[0]['speechiness']
    loudness = audio_features[0]['loudness']
    mode = audio_features[0]['mode']
    tempo = audio_features[0]['tempo']
    time_signature = audio_features[0]['time_signature']

    features = [track_id, track_name, release_date, length, track_popularity, album_id, album_name, artist_name,
                acousticness, danceability, energy, instrumentalness, liveness, speechiness, loudness, mode, tempo, time_signature]
    
    return features

def get_songs():
    tracks = []
    for i in artists:
        song = sp.search(q=i, type='track', limit=10)
        for j in range(10):
            tracks_id = song['tracks']['items'][j]['id']
            get_track = get_features(tracks_id)
            tracks.append(get_track)
    df = pd.DataFrame(tracks, columns=['track_id', 'track_name', 'release_date', 'length', 'track_popularity', 'album_id', 'album_name', 'artist_name',
                                       'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'loudness', 'mode', 'tempo', 'time_signature'])
    return df


df = get_songs()
df.to_csv(r'spotify_api_data.csv', index=False)