import logging
import os
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse

import requests
import yt_dlp

from kisskh_downloader.helper.decrypt_subtitle import SubtitleDecrypter
from kisskh_downloader.models.sub import SubItem

logger = logging.getLogger(__name__)


class Downloader:
    def __init__(self, referer: str) -> None:
        self.referer = referer

    def download_video_from_stream_url(
        self, video_stream_url: str, filepath: str, quality: str
    ) -> None:
        """Download a video from stream url

        :param video_stream_url: stream url
        :param filepath: file path where to download
        :param quality: quality to select
        """
        ydl_opts = {
            "format": f"bestvideo[height<={quality[:-1]}]+bestaudio/best[height<={quality[:-1]}]/best",
            "concurrent_fragment_downloads": 15,
            "outtmpl": f"{filepath}.%(ext)s",
            "http_headers": {
                "Referer": self.referer,
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
                "Origin": "https://kisskh.co",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
            },
            "hls_headers": {
                "Referer": self.referer,
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
                "Origin": "https://kisskh.co",
            },
            "nocheckcertificate": True,
            "no_warnings": True,
            "quiet": False,
            "extractor_retries": 10,
            "fragment_retries": 10,
            "skip_unavailable_fragments": False,
            "verbose": logger.getEffectiveLevel() == logging.DEBUG,
            "retries": 10,
            "prefer_free_formats": True,
            "allow_unplayable_formats": False,
            "extractor_args": {
                "generic": {
                    "nocheckcertificate": True,
                },
            },
        }
        logger.debug(f"Calling download with following options: {ydl_opts}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(video_stream_url)

    def download_subtitles(
        self,
        subtitles: List[SubItem],
        filepath: str,
        decrypter: Optional[SubtitleDecrypter] = None,
    ) -> None:
        for subtitle in subtitles:
            logger.info(f"Downloading {subtitle.label} sub...")
            extension = os.path.splitext(urlparse(subtitle.file).path)[-1]
            if not extension:
                extension = ".vtt"
            label_clean = subtitle.label.lower().replace(" ", "_")
            response = requests.get(subtitle.file, timeout=60)
            output_path = Path(f"{filepath}.{label_clean}{extension}")
            output_path.write_bytes(response.content)
            if decrypter is not None:
                decrypted_subtitle = decrypter.decrypt_subtitles(output_path)
                decrypted_subtitle.save(output_path)
