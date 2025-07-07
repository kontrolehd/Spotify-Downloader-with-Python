# Spotify-Downloader-with-Python

A professional Spotify track downloader web application with optional console usage.

## Features

- Download Spotify tracks by providing a Spotify URL.
- Fetches metadata from Spotify API.
- Searches and downloads audio from YouTube.
- Converts audio to MP3 and tags with metadata and cover art.
- Web interface with modern, professional UI.
- Optional console mode for command-line usage.
- Robust error handling and detailed debug logging.

## Setup

1. Clone the repository.

2. Install dependencies:

```bash
pip install -r app/requirements.txt
```

3. Configure Spotify API credentials:

Edit `app/config.py` and replace the placeholders with your Spotify Client ID and Client Secret.

```python
SPOTIFY_CLIENT_ID = "your_spotify_client_id_here"
SPOTIFY_CLIENT_SECRET = "your_spotify_client_secret_here"
```

## Usage

### Web Interface

Run the Flask app:

```bash
python app/main.py
```

Open your browser and navigate to `http://127.0.0.1:5000/`.

Enter a Spotify track URL and download the MP3.

### Console Mode

Download a track directly from the command line:

```bash
python app/main.py --console "SPOTIFY_TRACK_URL"
```

Example:

```bash
python app/main.py --console "https://open.spotify.com/track/your_track_id"
```

The MP3 file will be saved in the `app/temp` directory.

## Notes

- The app uses the Spotify API and YouTube to fetch and download audio.
- Ensure you have `ffmpeg` installed and accessible in your system PATH.
- Temporary files older than 10 minutes are automatically cleaned up.

## License

MIT License
