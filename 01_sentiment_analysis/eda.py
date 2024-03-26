import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

client_id = "3899576b5fcb4c458beba2cce99aa1b6"
client_secret = "4f57df7614df4f75b54364bf3c3018fd"
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id, client_secret))
