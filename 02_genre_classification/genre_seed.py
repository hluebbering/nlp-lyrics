import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import warnings
warnings.simplefilter("ignore")

# import track_data
genres_v2 = pd.read_csv("../assets/data/genre_seeds.csv")

client_id = "bd1c5f1d16b94210bc1776e172cbd264"
client_secret = "b152588a487b4f6e9429bdd1bfd92fb3"
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id, client_secret))


def track_features(id, artist_id, note):
    meta = sp.track(id)
    audio_features = sp.audio_features(id)
    artist_info = sp.artist(artist_id)

    if audio_features[0] is None:
        return None

    name = meta['name']
    track_id = meta['id']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    artist_id = meta['album']['artists'][0]['id']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']

    artist_pop = artist_info["popularity"]
    artist_genres = artist_info["genres"]
    artist_followers = artist_info["followers"]['total']

    acousticness = audio_features[0]['acousticness']
    danceability = audio_features[0]['danceability']
    energy = audio_features[0]['energy']
    instrumentalness = audio_features[0]['instrumentalness']
    liveness = audio_features[0]['liveness']
    loudness = audio_features[0]['loudness']
    speechiness = audio_features[0]['speechiness']
    tempo = audio_features[0]['tempo']
    valence = audio_features[0]['valence']
    key = audio_features[0]['key']
    mode = audio_features[0]['mode']
    time_signature = audio_features[0]['time_signature']

    return [name, track_id, album, artist, artist_id, release_date, length, popularity,
            artist_pop, artist_genres, artist_followers, acousticness, danceability,
            energy, instrumentalness, liveness, loudness, speechiness,
            tempo, valence, key, mode, time_signature, note]


# sp.recommendation_genre_seeds() "trip-hop", "trance"
genre_seeds = ["acoustic", "chill", "dance", "edm", "emo", "grunge", "happy", "hip-hop", "indie",
               "piano", "pop", "punk", "rock", "romance", "sad", "techno", "r-n-b"]

all_genre_seed_tracks = []

for genre in genre_seeds:
    genre_rec = sp.recommendations(seed_genres=[genre])['tracks']

    for song in genre_rec:
        song_id = song['id']
        song_artist_id = song['artists'][0]['id']
        song_audio = track_features(
            id=song_id, artist_id=song_artist_id, note=genre)
        all_genre_seed_tracks.append(song_audio)


df = pd.DataFrame(all_genre_seed_tracks,
                  columns=['name', 'track_id', 'album', 'artist', 'artist_id', 'release_date', 'length', 'popularity',
                           'artist_pop', 'artist_genres', 'artist_followers', 'acousticness', 'danceability',
                           'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness',
                           'tempo', 'valence', 'key', 'mode', 'time_signature', 'genre'])


df_add = df.append(genres_v2, ignore_index=True)
df_add = df_add.drop_duplicates(subset=['track_id', 'genre'])
#df_add = df_add.drop(columns=['Unnamed: 0.1', 'Unnamed: 0'])

df_add.to_csv("../assets/data/genre_seeds.csv", index=None)
