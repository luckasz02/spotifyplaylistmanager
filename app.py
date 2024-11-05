from flask import Flask, request, jsonify, render_template, redirect, session, url_for, make_response
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from datetime import timedelta
from werkzeug.middleware.proxy_fix import ProxyFix
import random

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()
print(app.secret_key)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30) # Session timeout after 30 minutes
app.permanent_session_lifetime = timedelta(minutes=30)
app.wsgi_app = ProxyFix(app.wsgi_app)

# Spotify credentials
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
REDIRECT_URI = 'http://localhost:8888/callback'
SCOPE = 'playlist-modify-public'
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    show_dialog=True,
    cache_path=None  # Disable local token caching
)

# Checking Login State
@app.route('/check_login', methods=['GET'])
def check_login():
    token_info = session.get('token_info', None)
    response = make_response(jsonify(bool(token_info)))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response

# Authentication route
@app.route('/login')
def login():
    print(f"Session before login: {session}")  # Debug: Confirm session is empty
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

# Callback route
@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('index'))

# Get Spotify client
def get_spotify_client():
    token_info = session.get('token_info', None)
    if not token_info:
        raise Exception("Authentication required")
    if sp_oauth.is_token_expired(token_info):
        session.clear()
        raise Exception("Authentication required")
    print(f"Current token info: {token_info}")  # Debug token info
    return spotipy.Spotify(auth=token_info['access_token'])

# Get user info
@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    try:
        sp = get_spotify_client()
        user_info = sp.current_user()  # Get user information
        return jsonify({
            "display_name": user_info.get("display_name"),
            "email": user_info.get("email")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get user playlists
@app.route('/get_user_playlists', methods=['GET'])
def get_user_playlists():
    sp = get_spotify_client()
    user = sp.current_user()
    print(f"Fetching playlists for user: {user['display_name']} ({user['id']})")  # Debug info
    playlists = sp.current_user_playlists(limit=50)
    return jsonify([{'name': playlist['name'], 'id': playlist['id']} for playlist in playlists['items']])

# Route to render index.html template
@app.route('/')
def index():
    return render_template('index.html')

# Route to search tracks
@app.route('/search_tracks', methods=['POST'])
def search_tracks():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri=REDIRECT_URI,
                                                   scope=SCOPE))
    track_name = request.json['track_name']
    results = sp.search(q=track_name, limit=10, type='track')
    tracks = [{'name': track['name'], 'id': track['id']} for track in results['tracks']['items']]
    return jsonify(tracks)

# Route to add tracks to playlist
@app.route('/add_to_playlist', methods=['POST'])
def add_to_playlist():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri=REDIRECT_URI,
                                                   scope=SCOPE))
    playlist_id = request.json['playlist_id']
    track_ids = request.json['track_ids']
    sp.user_playlist_add_tracks(user=sp.current_user()['id'], playlist_id=playlist_id, tracks=track_ids)
    return jsonify({'message': 'Tracks added successfully'})

# Fetch playlist tracks
def get_playlist_tracks(playlist_id):
    sp = get_spotify_client()
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return [track['track']['id'] for track in tracks if track['track']]

# Replace tracks in the playlist
def replace_playlist_tracks(playlist_id, tracks):
    sp = get_spotify_client()
    sp.playlist_replace_items(playlist_id, tracks[:100])
    if len(tracks) > 100:
        for i in range(100, len(tracks), 100):
            sp.playlist_add_items(playlist_id, tracks[i:i+100])

# Function to shuffle and update the playlist
@app.route('/shuffle_playlist', methods=['POST'])
def shuffle_playlist():
    try:
        playlist_id = request.json['playlist_id']  # Get playlist ID from the request
        tracks = get_playlist_tracks(playlist_id)
        random.shuffle(tracks)
        replace_playlist_tracks(playlist_id, tracks)
        return jsonify({"message": "Playlist shuffled successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to logout
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clear the session data
    global sp_oauth
    sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        show_dialog=True,
        cache_path=".cache"  # Specify cache path to delete it
    )
    
    # Check and delete the cached token file
    if os.path.exists(".cache"):
        os.remove(".cache")
    
    response = make_response(jsonify({"message": "Logged out successfully"}))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response

if __name__ == '__main__':
    app.run(debug=True, port=8888)
