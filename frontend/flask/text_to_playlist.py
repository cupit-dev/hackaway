#! ./venv/bin/python3

from datetime import date
import yaml
import os.path
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
import re

from emotional_playlist_generator import EmotionalPlaylistGenerator

class TextToPlaylist():
    def __init__(self, sp=None, spotify_auth=None, openai_key=None, secrets_file=None, limit=100):

        if sp:
            self.sp = sp
        if spotify_auth:
            self.spotify_auth = spotify_auth
        if openai_key:
            self.openai_key = openai_key

        if not openai_key or not spotify_auth:
            if not os.path.isfile('./secrets.yaml' if not secrets_file else secrets_file):
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
            auth_manager = SpotifyOAuth(client_id=self.spotify_auth['client_id'], client_secret=self.spotify_auth['secret'], redirect_uri='http://localhost:5000', scope='user-top-read,playlist-modify-private,playlist-modify-public,user-read-private,user-read-email,ugc-image-upload')
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

    def text_to_song_list(self, journal_entry, generate_artwork=False):
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

        emotion_summary = self.generator.analyse_emotion(journal_entry)
        music_parameters = self.generator.get_music_parameters(emotion_summary)

        spotify_params = {}
        for line in music_parameters.split('\n'):
            match = re.match(r'^.*target_(\w+).*=(.*)$', line)
            if match:
                param, value = match.groups()
                spotify_params[f'target_{param}'] = float(value)

        reccs = self.sp.recommendations(seed_artists=[id for id, _ in top_five_artists], limit=self.limit, **spotify_params)
        title = self.generator.get_playlist_name(emotion_summary)

        artwork = None
        if generate_artwork:
            artwork = self.generator.get_playlist_cover(emotion_summary)

        return {
            'tracks': reccs['tracks'],
            'prompt': journal_entry,
            'summary': emotion_summary,
            'sentiment': spotify_params,
            'title': title,
            'artwork': artwork,
            'uploaded': False
        }
    
    
    def upload_playlist(self, playlist):
        title = f"{playlist['title']} ({date.today().strftime("%d/%m/%Y")})"
        user_id = self.sp.me()['id']
        remote = self.sp.user_playlist_create(user=user_id, name=title, public=False, description=playlist['summary'])
        self.sp.playlist_add_items(remote['id'], [track['id'] for track in playlist['tracks']])
        return remote['id']


    def upload_cover_art(self, uuid, artwork):
        self.sp.playlist_upload_cover_image(uuid, artwork)

