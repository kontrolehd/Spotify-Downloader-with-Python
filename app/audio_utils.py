import ffmpeg
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
import requests
import os
import logging

logger = logging.getLogger(__name__)

def convert_to_mp3_and_tag(input_path, output_path, metadata):
    # Convert audio to mp3 using ffmpeg
    try:
        (
            ffmpeg
            .input(input_path)
            .output(output_path, format='mp3', audio_bitrate='192k')
            .overwrite_output()
            .run(quiet=True)
        )
        logger.info(f"Converted audio to mp3: {output_path}")
    except ffmpeg.Error as e:
        error_msg = e.stderr.decode() if e.stderr else str(e)
        logger.error(f"ffmpeg error: {error_msg}")
        raise RuntimeError(f"ffmpeg error: {error_msg}")

    # Add ID3 tags
    try:
        audio = EasyID3(output_path)
        audio['title'] = metadata.get('title', '')
        audio['artist'] = metadata.get('artist', '')
        audio['album'] = metadata.get('album', '')
        audio['date'] = metadata.get('year', '')
        audio.save()
        logger.info(f"Added ID3 tags to: {output_path}")
    except Exception as e:
        logger.error(f"Error adding ID3 tags: {e}")
        raise

    # Add cover art
    if metadata.get('cover_url'):
        try:
            img_data = requests.get(metadata['cover_url']).content
            audio = ID3(output_path)
            audio['APIC'] = APIC(
                encoding=3,
                mime='image/jpeg',
                type=3,  # Cover front
                desc='Cover',
                data=img_data
            )
            audio.save()
            logger.info(f"Added cover art to: {output_path}")
        except Exception as e:
            logger.warning(f"Failed to add cover art: {e}")
