# Import flask and datetime module for showing date and time
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes and domains

@app.route('/new_playlist', methods=['POST'])
def on_new_playlist():
    '''Given a journal entry, generate a playlist and return a UUID used to access it'''
    return 'TESTUUID-1234'

# @app.route('/playlist/<uuid>')
# def on_playlist(uuid):
@app.route('/playlist')
def on_playlist():
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


@app.route('/feeling', methods=['POST'])
def handle_data():
    data = request.json  # Access the JSON data sent from React
    print(data)  # For demonstration, print the data. Process as needed.

    # Return a response to your frontend
    return jsonify({"message": "Data received successfully", "yourData": data}), 200

# Running app
if __name__ == '__main__':
    app.run(debug=True)