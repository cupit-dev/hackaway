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

@app.route('/new_playlist', methods=['POST'])
def on_new_playlist():
    '''Given a journal entry, generate a playlist and return a UUID used to access it'''
    prompt = request.json['prompt']
    print('please work', prompt)
    results = generator.text_to_song_list(prompt)
    id = str(uuid.uuid4())
    storage[id] = results

    return on_playlist(id)
    # return {'uuid': id}
    

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
    
    
    # return {
    #     'title': 'My Playlist',
    #     'description': 'Example playlist blah blah blah',
    #     'tracks': [
    #         {
    #             'name': 'Tune 1',
    #             'artists': ['artist 1', 'artist 2'],  # ths is actually an object but artists[x]['name'] works
    #             'track_id': 'qwertyuiop'
    #         },
    #         {
    #             'title': 'Banger 2',
    #             'artists': ['artist 1', 'artist 2'],
    #             'track_id': 'qwertyuiop'
    #         }
    #     ]
    # }

@app.route('/cover_art/<uuid>')
def on_playlist_(uuid):
    '''Return a playlist image as a 512x512 base64 encoded jpeg. Generated on first request to save on API costs.'''
    return {
        'cover_art': 'ubsdfbgiafvnosnoaivmnasljdfnj;asfnasjkdfnaskldjfnlsadjf'
    }



if __name__ == "__main__":
    app.run(debug=True, port=5001)