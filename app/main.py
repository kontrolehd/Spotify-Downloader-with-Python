from flask import Flask, request, jsonify, send_from_directory
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from spotify_utils import get_spotify_metadata
from youtube_utils import search_and_download_audio
from audio_utils import convert_to_mp3_and_tag
import uuid
import time

from flask import Flask, request, jsonify, send_from_directory, render_template

app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

# Cleanup files older than 10 minutes
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/style.css')
def style_css():
    return app.send_static_file('style.css')

@app.route('/main.js')
def main_js():
    return app.send_static_file('main.js')

def cleanup_temp_files():
    now = time.time()
    for filename in os.listdir(TEMP_DIR):
        file_path = os.path.join(TEMP_DIR, filename)
        if os.path.isfile(file_path):
            if now - os.path.getmtime(file_path) > 600:
                try:
                    os.remove(file_path)
                    logger.info(f"Removed temp file: {file_path}")
                except Exception as e:
                    logger.error(f"Error removing file {file_path}: {e}")

@app.route('/download', methods=['POST'])
def download():
    cleanup_temp_files()
    data = request.get_json()
    spotify_url = data.get('spotify_url')
    logger.info(f"Received download request for URL: {spotify_url}")
    if not spotify_url:
        logger.warning("No Spotify URL provided in request")
        print("[ERROR] No Spotify URL provided in request")
        return jsonify({'error': 'No Spotify URL provided'}), 400

    try:
        # Get metadata from Spotify
        logger.info("Fetching metadata from Spotify")
        print("[INFO] Fetching metadata from Spotify")
        metadata = get_spotify_metadata(spotify_url)
        if not metadata:
            logger.error(f"Failed to retrieve metadata for URL: {spotify_url}")
            print(f"[ERROR] Failed to retrieve metadata for URL: {spotify_url}")
            return jsonify({'error': 'Could not retrieve metadata from Spotify'}), 400

        # Search and download audio from YouTube
        logger.info(f"Searching and downloading audio for: {metadata.get('artist')} - {metadata.get('title')}")
        print(f"[INFO] Searching and downloading audio for: {metadata.get('artist')} - {metadata.get('title')}")
        audio_path = search_and_download_audio(metadata)
        if not audio_path:
            logger.error(f"Failed to download audio from YouTube for: {metadata}")
            print(f"[ERROR] Failed to download audio from YouTube for: {metadata}")
            return jsonify({'error': 'Could not download audio from YouTube'}), 400

        # Convert to MP3 and tag
        mp3_filename = f"{uuid.uuid4()}.mp3"
        mp3_path = os.path.join(TEMP_DIR, mp3_filename)
        logger.info(f"Converting audio to mp3 and tagging: {mp3_path}")
        print(f"[INFO] Converting audio to mp3 and tagging: {mp3_path}")
        try:
            convert_to_mp3_and_tag(audio_path, mp3_path, metadata)
        except Exception as e:
            logger.error(f"Error converting and tagging audio: {e}")
            print(f"[ERROR] Error converting and tagging audio: {e}")
            return jsonify({'error': 'Failed to convert and tag audio'}), 500

        # Remove raw audio file
        if os.path.exists(audio_path):
            try:
                os.remove(audio_path)
                logger.info(f"Removed raw audio file: {audio_path}")
                print(f"[INFO] Removed raw audio file: {audio_path}")
            except Exception as e:
                logger.warning(f"Failed to remove raw audio file {audio_path}: {e}")
                print(f"[WARNING] Failed to remove raw audio file {audio_path}: {e}")

        download_url = f"/temp/{mp3_filename}"

        response = {
            'download_url': download_url,
            'title': metadata.get('title'),
            'artist': metadata.get('artist'),
            'cover_url': metadata.get('cover_url')
        }
        logger.info(f"Download ready: {response}")
        print(f"[INFO] Download ready: {response}")
        return jsonify(response)

    except Exception as e:
        logger.exception("Unexpected error during download process")
        print(f"[EXCEPTION] Unexpected error during download process: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/temp/<filename>')
def serve_temp_file(filename):
    return send_from_directory(TEMP_DIR, filename, as_attachment=True)

import argparse

def download_song_console(spotify_url):
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Reuse the same logic as in the Flask route
    from spotify_utils import get_spotify_metadata
    from youtube_utils import search_and_download_audio
    from audio_utils import convert_to_mp3_and_tag
    import uuid
    import os
    import time

    TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    def cleanup_temp_files():
        now = time.time()
        for filename in os.listdir(TEMP_DIR):
            file_path = os.path.join(TEMP_DIR, filename)
            if os.path.isfile(file_path):
                if now - os.path.getmtime(file_path) > 600:
                    try:
                        os.remove(file_path)
                        logger.info(f"Removed temp file: {file_path}")
                    except Exception as e:
                        logger.error(f"Error removing file {file_path}: {e}")

    cleanup_temp_files()
    logger.info(f"Received download request for URL: {spotify_url}")
    if not spotify_url:
        logger.warning("No Spotify URL provided in request")
        print("[ERROR] No Spotify URL provided in request")
        return

    try:
        logger.info("Fetching metadata from Spotify")
        print("[INFO] Fetching metadata from Spotify")
        metadata = get_spotify_metadata(spotify_url)
        if not metadata:
            logger.error(f"Failed to retrieve metadata for URL: {spotify_url}")
            print(f"[ERROR] Failed to retrieve metadata for URL: {spotify_url}")
            return

        logger.info(f"Searching and downloading audio for: {metadata.get('artist')} - {metadata.get('title')}")
        print(f"[INFO] Searching and downloading audio for: {metadata.get('artist')} - {metadata.get('title')}")
        audio_path = search_and_download_audio(metadata)
        if not audio_path:
            logger.error(f"Failed to download audio from YouTube for: {metadata}")
            print(f"[ERROR] Failed to download audio from YouTube for: {metadata}")
            return

        mp3_filename = f"{uuid.uuid4()}.mp3"
        mp3_path = os.path.join(TEMP_DIR, mp3_filename)
        logger.info(f"Converting audio to mp3 and tagging: {mp3_path}")
        print(f"[INFO] Converting audio to mp3 and tagging: {mp3_path}")
        try:
            convert_to_mp3_and_tag(audio_path, mp3_path, metadata)
        except Exception as e:
            logger.error(f"Error converting and tagging audio: {e}")
            print(f"[ERROR] Error converting and tagging audio: {e}")
            return

        if os.path.exists(audio_path):
            try:
                os.remove(audio_path)
                logger.info(f"Removed raw audio file: {audio_path}")
                print(f"[INFO] Removed raw audio file: {audio_path}")
            except Exception as e:
                logger.warning(f"Failed to remove raw audio file {audio_path}: {e}")
                print(f"[WARNING] Failed to remove raw audio file {audio_path}: {e}")

        print(f"[SUCCESS] Download complete: {mp3_path}")
        logger.info(f"Download complete: {mp3_path}")

    except Exception as e:
        logger.exception("Unexpected error during download process")
        print(f"[EXCEPTION] Unexpected error during download process: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Spotify Downloader')
    parser.add_argument('--console', type=str, help='Spotify URL to download via console')
    args = parser.parse_args()

    if args.console:
        download_song_console(args.console)
    else:
        app.run(debug=True)
