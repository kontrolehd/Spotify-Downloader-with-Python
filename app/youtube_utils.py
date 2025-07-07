import yt_dlp
import os
import tempfile
import logging

logger = logging.getLogger(__name__)

def search_and_download_audio(metadata):
    # Construct search query from metadata
    query = f"{metadata.get('artist')} - {metadata.get('title')}"
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, "downloaded_audio.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '192',
        }],
        'default_search': 'ytsearch1',
        'nocheckcertificate': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(query, download=True)
            filename = ydl.prepare_filename(info)
            # The postprocessor changes extension to m4a
            base, ext = os.path.splitext(filename)
            audio_file = base + ".m4a"
            if os.path.exists(audio_file):
                logger.info(f"Downloaded audio file: {audio_file}")
                return audio_file
            else:
                logger.info(f"Downloaded audio file: {filename}")
                return filename
        except Exception as e:
            logger.error(f"Error downloading audio for query '{query}': {e}")
            return None
