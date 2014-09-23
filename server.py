from flask import Flask
from flask import request
from flask import jsonify
from flask import send_from_directory
import time
import os

import spotify

api = spotify.SearchAPI()
app = Flask('spotify-poems', static_folder='webapp')

@app.route('/api/spotifize')
def spotifize():
    time0 = time.time()
    query =  request.args.get('q')

    if not query: return jsonify()
    if len(query) == 0: return jsonify()

    poem = spotify.PoemSentence(query)
    playlist = poem.spotifize(api)
    coverage = poem.coverage()
    time1 = time.time()

    return jsonify(query = query,
                   coverage = coverage,
                   playlist = playlist,
                   execution_time =  time1 - time0)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route('/<path:filename>')  
def send_file(filename):  
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
