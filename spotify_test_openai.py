#! ./venv/bin/python3

import yaml
import os.path
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
import re

from emotional_playlist_generator import EmotionalPlaylistGenerator

if not os.path.isfile('./secrets.yaml'):
    print('No secrets file - aborting')
    exit(1)

with open("./secrets.yaml", "r") as f:
    try:
        data = yaml.safe_load(f)
        spotify_auth = data['spotify']
        openai_key = data['openai']['secret']
    except yaml.YAMLError as exc:
        print(exc)
        exit(1)

generator = EmotionalPlaylistGenerator(api_key=openai_key)

# auth_manager = SpotifyClientCredentials(client_id=spotify_auth['client_id'], client_secret=spotify_auth['secret'])
print('Authenticating, please wait...')
auth_manager = SpotifyOAuth(client_id=spotify_auth['client_id'], client_secret=spotify_auth['secret'], redirect_uri='http://localhost:5000', scope='user-top-read')
sp = spotipy.Spotify(auth_manager=auth_manager)
print('Auth successful!')

# Spotify can base recommendations off up to 5 tracks/artists/genres at once, but the genres are fairly useless - there's only a small
# list of acceptable options and they don't correspond to the genres attached to artists, while tracks don't have a genre attached at all.
# Therefore, we do some trickery to get a list of the user's 5 top genres across their favourite 50 artists, then we use the top artist
# from within each genre to form the basis for the recommendation.
# Basic flow:
#   - get the user's top 50 artists over the last six months, and count the top 5 genres represented by those artists
#   - Get the top artist that hasn't already been picked, once per genre, up to a maximum of five artists
#   - use the recommendations feature to generate a short playlist with a valence based on their mood

artists = sp.current_user_top_artists(limit=50, time_range='medium_term')

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
        
journal_entry = input("Enter your jounal entry: ")

emotion_summary = generator.analyse_emotion(journal_entry)
print(emotion_summary)
music_parameters = generator.get_music_parameters(emotion_summary)
print(music_parameters)

valence = float(re.search(r'^.*target_valence.*=(.*)', music_parameters, flags=re.MULTILINE).group(1))
danceability = float(re.search(r'^.*target_danceability.*=(.*)', music_parameters, flags=re.MULTILINE).group(1))
energy = float(re.search(r'^.*target_energy.*=(.*)', music_parameters, flags=re.MULTILINE).group(1))
acousticness = float(re.search(r'^.*target_acousticness.*=(.*)', music_parameters, flags=re.MULTILINE).group(1))

print('Stats:')
print(f'To summarise: {emotion_summary}')
print(f'You\'re feeling {valence * 100}% happy, {danceability * 100}% danceable, {energy * 100}% energetic, and {acousticness * 100}% acoustic.')
print(f'Your top 10 genres are: {", ".join([g for g, _ in genre_count.most_common(10)])}')
print(f'Your top 5 artists, spread across your top 5ish genres, are: {", ".join([a for _, a in top_five_artists])}')

limit = input('How many tracks to recommend? (at most, 1-50): ')
limit = int(''.join(c for c in limit if c.isdigit()))
# limit = min(50, max(1, limit))

reccs = sp.recommendations(seed_artists=[id for id, _ in top_five_artists], limit=limit ,target_danceability=danceability, target_valence=valence, target_energy=energy, target_acousticness=acousticness)

print('We recommend:')
for track in reccs['tracks']:
    print(f'  - "{track["name"]}" by {[a["name"] for a in track["artists"]]}')