from datetime import date
import os
import sys
import uuid
import json

from flask import Flask, request, jsonify
from text_to_playlist import TextToPlaylist
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
generator = TextToPlaylist(secrets_file='./secrets.yaml')
storage = {}

FAKE_HISTORIC = True

if FAKE_HISTORIC:
    with open('historic.json', 'r', encoding='utf-8') as f:
        storage = json.load(f)

@app.route('/new_playlist', methods=['POST'])
def on_new_playlist():
    '''Given a journal entry, generate a playlist and return a UUID used to access it'''
    prompt = request.json['prompt']
    generate_artwork = True if request.json['generate_artwork'] == True else False
    results = generator.text_to_song_list(prompt, generate_artwork=generate_artwork)
    id = str(uuid.uuid4())
    results['uuid'] = id
    results['date'] = date.today().isoformat()
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

@app.route('/dump_data')
def on_dump_data():
    # This whole concept about as inefficient as it could possibly be, but it'll do for a demo
    dump = {}
    for item in list(storage.values()):
        date = item['date']
        if date in dump:
            dump[date].append(item['sentiment'])
        else:
            dump[date] = [item['sentiment']]
    return dump


if __name__ == "__main__":
    app.run(debug=True, port=5001)