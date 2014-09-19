from flask import Flask
from flask import request
from flask import jsonify

import spotify

api = spotify.SearchAPI()
app = Flask('spotify-poems')

@app.route('/')
def index():
    return "spotify-poems"

@app.route('/api/spotifize')
def spotifize_poem():
    poem =  request.args.get('poem')
    playlist = spotify.Poem(poem).spotifize(api)
    return jsonify(poem = poem,
                   playlist = playlist)

if __name__ == "__main__":
    app.run(debug=True)