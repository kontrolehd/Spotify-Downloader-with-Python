import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
import re

import config

client_credentials_manager = SpotifyClientCredentials(client_id=config.SPOTIFY_CLIENT_ID, client_secret=config.SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def parse_spotify_url(url):
    print(f"[DEBUG] Original URL: {url}")
    # Remove query parameters if present
    url = url.split('?')[0]
    print(f"[DEBUG] URL after stripping query params: {url}")
    # Extract type and id from Spotify URL
    pattern = r"open\.spotify\.com\/(?:intl-[a-z]{2}\/)?(track|album|playlist)\/([a-zA-Z0-9]+)"
    match = re.search(pattern, url)
    print(f"[DEBUG] Regex match: {match}")
    if match:
        print(f"[DEBUG] Extracted type: {match.group(1)}, id: {match.group(2)}")
        return match.group(1), match.group(2)
    return None, None

def get_spotify_metadata(spotify_url):
    content_type, content_id = parse_spotify_url(spotify_url)
    if not content_type or not content_id:
        return None

    if content_type == 'track':
        track = sp.track(content_id)
        metadata = {
            'title': track['name'],
            'artist': ', '.join([artist['name'] for artist in track['artists']]),
            'album': track['album']['name'],
            'year': track['album']['release_date'][:4],
            'cover_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
            'duration_ms': track['duration_ms']
        }
        return metadata
    elif content_type == 'album':
        album = sp.album(content_id)
        # For simplicity, return album metadata of first track
        tracks = album['tracks']['items']
        if not tracks:
            return None
        first_track = tracks[0]
        metadata = {
            'title': first_track['name'],
            'artist': ', '.join([artist['name'] for artist in album['artists']]),
            'album': album['name'],
            'year': album['release_date'][:4],
            'cover_url': album['images'][0]['url'] if album['images'] else None,
            'duration_ms': first_track['duration_ms']
        }
        return metadata
    elif content_type == 'playlist':
        playlist = sp.playlist(content_id)
        # For simplicity, return metadata of first track in playlist
        tracks = playlist['tracks']['items']
        if not tracks:
            return None
        first_track = tracks[0]['track']
        metadata = {
            'title': first_track['name'],
            'artist': ', '.join([artist['name'] for artist in first_track['artists']]),
            'album': first_track['album']['name'],
            'year': first_track['album']['release_date'][:4],
            'cover_url': first_track['album']['images'][0]['url'] if first_track['album']['images'] else None,
            'duration_ms': first_track['duration_ms']
        }
        return metadata
    else:
        return None
