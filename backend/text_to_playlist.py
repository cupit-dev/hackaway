#! ./venv/bin/python3

import yaml
import os.path
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
import re

from emotional_playlist_generator import EmotionalPlaylistGenerator

class TextToPlaylist():
    def __init__(self, sp=None, spotify_auth=None, openai_key=None, limit=100):

        if sp:
            self.sp = sp
        if spotify_auth:
            self.spotify_auth = spotify_auth
        if openai_key:
            self.openai_key = openai_key

        if not openai_key or not spotify_auth:
            if not os.path.isfile('./secrets.yaml'):
                print('No secrets file - aborting')
                raise FileNotFoundError

            with open("./secrets.yaml", "r") as f:
                try:
                    data = yaml.safe_load(f)
                    if not spotify_auth:
                        self.spotify_auth = data['spotify']
                    if not openai_key:
                        self.openai_key = data['openai']['secret']
                except yaml.YAMLError as exc:
                    print(exc)
                    raise yaml.YAMLError
            
        if not sp:
            auth_manager = SpotifyOAuth(client_id=self.spotify_auth['client_id'], client_secret=self.spotify_auth['secret'], redirect_uri='http://localhost:5000', scope='user-top-read')
            self.sp = spotipy.Spotify(auth_manager=auth_manager)

        self.generator = EmotionalPlaylistGenerator(api_key=self.openai_key)
        self.limit = limit

# Spotify can base recommendations off up to 5 tracks/artists/genres at once, but the genres are fairly useless - there's only a small
# list of acceptable options and they don't correspond to the genres attached to artists, while tracks don't have a genre attached at all.
# Therefore, we do some trickery to get a list of the user's 5 top genres across their favourite 50 artists, then we use the top artist
# from within each genre to form the basis for the recommendation.
# Basic flow:
#   - get the user's top 50 artists over the last six months, and count the top 5 genres represented by those artists
#   - Get the top artist that hasn't already been picked, once per genre, up to a maximum of five artists
#   - use the recommendations feature to generate a short playlist with a valence based on their mood

    def text_to_song_list(self, journal_entry):
        artists = self.sp.current_user_top_artists(limit=50, time_range='medium_term')

        genre_count = Counter()
        genre_to_top_artists = {}

        for artist in artists['items']:
            genre_count.update(artist['genres'])
            for genre in artist['genres']:
                if genre in genre_to_top_artists:
                    genre_to_top_artists[genre].append((artist['id'], artist['name']))
                else:
                    genre_to_top_artists[genre] = [(artist['id'], artist['name'])]

        top_five_artists = []
        for genre, _ in genre_count.most_common(15):
            if len(top_five_artists) >= 5:
                break
            for artist in genre_to_top_artists[genre]:
                if artist not in top_five_artists:
                    top_five_artists.append(artist)
                    break

        # print(genre_count.most_common(10))
        # print(genre_to_top_artists)
        # print(top_five_artists)

        emotion_summary = self.generator.analyse_emotion(journal_entry)
        music_parameters = self.generator.get_music_parameters(emotion_summary)

        valence = float(re.search(r'^.*target_valence.*=(.*)', music_parameters, flags=re.MULTILINE).group(1))
        danceability = float(re.search(r'^.*target_danceability.*=(.*)', music_parameters, flags=re.MULTILINE).group(1))
        energy = float(re.search(r'^.*target_energy.*=(.*)', music_parameters, flags=re.MULTILINE).group(1))
        acousticness = float(re.search(r'^.*target_acousticness.*=(.*)', music_parameters, flags=re.MULTILINE).group(1))
        reccs = self.sp.recommendations(seed_artists=[id for id, _ in top_five_artists], limit=self.limit ,target_danceability=danceability, target_valence=valence, target_energy=energy, target_acousticness=acousticness)
        return reccs