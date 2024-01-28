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

currentUUID = ''
@app.route('/new_playlist', methods=['POST'])
def on_new_playlist():
    '''Given a journal entry, generate a playlist and return a UUID used to access it'''
    prompt = request.json['prompt']
    results = generator.text_to_song_list(prompt)
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
    generator.upload_playlist(playlist)
    storage[uuid]['uploaded'] = True
    return 'Playlist added', 201


@app.route('/playlist/<uuid>')
def on_playlist(uuid):
    '''Return a playlist as a JSON object, containing a title, description, and list of songs (incl. title, artists, and track IDs)'''
    if uuid not in storage:
        return f'Playlist {uuid} not found', 400
    return storage[uuid]
    
    # return uuid 

@app.route('/cover_art/<uuid>')
def on_playlist_(uuid):
    '''Return a playlist image as a 512x512 base64 encoded jpeg. Generated on first request to save on API costs.'''
    return {
        'cover_art': 'ubsdfbgiafvnosnoaivmnasljdfnj;asfnasjkdfnaskldjfnlsadjf'
    }



if __name__ == "__main__":
    app.run(debug=True, port=5001)