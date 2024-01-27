from flask import Flask

app = Flask(__name__)

@app.route('/new_playlist', methods=['POST'])
def on_new_playlist():
    '''Given a journal entry, generate a playlist and return a UUID used to access it'''
    return 'TESTUUID-1234'

@app.route('/playlist/<uuid>')
def on_playlist(uuid):
    '''Return a playlist as a JSON object, containing a title, description, and list of songs (incl. title, artists, and track IDs)'''
    return {
        'title': 'My Playlist',
        'description': 'Example playlist blah blah blah',
        'tracks': [
            {
                'title': 'Tune 1',
                'artists': ['artist 1', 'artist 2'],
                'track_id': 'qwertyuiop'
            },
            {
                'title': 'Banger 2',
                'artists': ['artist 1', 'artist 2'],
                'track_id': 'qwertyuiop'
            }
        ]
    }

@app.route('/cover_art/<uuid>')
def on_playlist_():
    '''Return a playlist image as a 512x512 base64 encoded jpeg. Generated on first request to save on API costs.'''
    return {
        'cover_art': 'ubsdfbgiafvnosnoaivmnasljdfnj;asfnasjkdfnaskldjfnlsadjf'
    }



if __name__ == "__main__":
    app.run(debug=True)