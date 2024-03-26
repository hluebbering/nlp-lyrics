import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

client_id = "3899576b5fcb4c458beba2cce99aa1b6"
client_secret = "4f57df7614df4f75b54364bf3c3018fd"
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id, client_secret))


def playlist_follower_count(playlist_id: str):
    """
    Retrieves the follower count for a given playlist.

    Args:
        playlist_id (str): The ID of the playlist.

    Returns:
        int: The number of followers for the playlist.
    """
    playlist = sp.playlist(playlist_id)
    return playlist["followers"]["total"]


def get_top_playlists(username: str, lim: int):
    """
    Retrieves the top playlists for a given username.

    Args:
        username (str): The username for which to retrieve the playlists.
        lim (int): The maximum number of playlists to return.

    Returns:
        pd.DataFrame: A DataFrame containing the top playlists sorted by follower count.
    """
    all_playlists = sp.user_playlists(username)  # Get user playlists
    playlist_data = [
        {
            "thumbnail": item["images"][0]["url"],
            "name": item["name"],
            "id": item["id"],
            "description": item["description"],
            "tracks": item["tracks"]["total"],
            "followers": playlist_follower_count(item["id"]),
        }
        for item in all_playlists["items"]  # Iterate over each playlist item
    ]
    # Create DataFrame and sort by followers
    playlist_df = pd.DataFrame(playlist_data)

    return playlist_df.nlargest(lim, "followers")  # Return top playlists
