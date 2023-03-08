import spotipy
from spotipy.oauth2 import SpotifyOAuth

URI = 'https://127.0.0.1:8000/spotify/'


class Spotify:
    # init method or constructor
    def __init__(self, client_id: str, client_pass: str):
        self.__client_id = client_id
        self.__client_pass = client_pass
        auth = SpotifyOAuth(client_id=client_id,
                            client_secret=client_pass,
                            redirect_uri=URI,
                            scope=['user-top-read'])
        # set up the Spotipy client
        self.spotify = spotipy.Spotify(auth_manager=auth)

    def get_top_tracks(self):
        top_tracks = self.spotify.current_user_top_tracks(limit=5, offset=0, time_range='short_term')
        return top_tracks
