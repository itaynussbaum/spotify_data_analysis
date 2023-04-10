import os
import discogs_client
import logging
from app import get_user_tracks, get_master_ids, get_discogs_info, get_credentials, Spotify
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

client_id = os.environ["SPOTIFY_CLIENT_ID"]
client_pass = os.environ["SPOTIFY_CLIENT_SECRET"]
spotify = Spotify(client_id, client_pass)
app2 = Flask(__name__)
CORS(app2)

@app2.route("/api/vinyl-recommendations", methods=["GET"])
def vinyl_recommendations():
    logging.info("vinyl_recommendations function called")
    tracks = get_user_tracks()
    logging.info(f"Tracks: {tracks}")
    master_ids = get_master_ids(tracks)
    logging.info(f"Master IDs: {master_ids}")
    results = get_discogs_info(master_ids)
    logging.info(f"Results: {results}")
    return jsonify(results)

if __name__ == "__main__":
    app2.run(debug=True)
