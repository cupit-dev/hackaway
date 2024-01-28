import os
import sys
import uuid

from flask import Flask, request, jsonify
from text_to_playlist import TextToPlaylist
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
generator = TextToPlaylist(secrets_file='./secrets.yaml')
storage = {}

# Enable to generate album covers with DALLE-3
# This costs about 5p a pop, so use sparingly
GENERATE_ARTWORK = True

@app.route('/new_playlist', methods=['POST'])
def on_new_playlist():
    '''Given a journal entry, generate a playlist and return a UUID used to access it'''
    prompt = request.json['prompt']
    results = generator.text_to_song_list(prompt, generate_artwork=GENERATE_ARTWORK)
    id = str(uuid.uuid4())
    results['uuid'] = id
    storage[id] = results
    return on_playlist(id)


@app.route('/playlist/<uuid>/upload', methods=['GET', 'POST'])
def on_upload_playlist(uuid):
    '''Upload playlist at given UUID to Spotify'''
    if uuid not in storage:
        return f'Playlist {uuid} not found', 400
    playlist = storage[uuid]
    remote_uuid = generator.upload_playlist(playlist)
    if playlist['artwork']:
        generator.upload_cover_art(remote_uuid, playlist['artwork'])
    storage[uuid]['uploaded'] = True
    storage[uuid]['remote_uuid'] = remote_uuid
    return 'Playlist added', 201


@app.route('/playlist/<uuid>')
def on_playlist(uuid):
    '''Return a playlist as a JSON object, containing a title, description, and list of songs (incl. title, artists, and track IDs)'''
    if uuid not in storage:
        return f'Playlist {uuid} not found', 400
    return storage[uuid]


if __name__ == "__main__":
    app.run(debug=True, port=5001)