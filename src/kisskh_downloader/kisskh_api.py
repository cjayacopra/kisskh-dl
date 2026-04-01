import json
import logging
import os
import sys
from typing import Dict, List, Optional
from urllib.parse import urljoin

import requests
from dotenv import load_dotenv

from kisskh_downloader.models.drama import Drama
from kisskh_downloader.models.search import DramaInfo, Search
from kisskh_downloader.models.sub import Sub, SubItem

load_dotenv()

logger = logging.getLogger(__name__)


def _get_api_url() -> str:
    api_url = os.getenv("KISSKH_API_URL")
    if not api_url:
        raise ValueError(
            "KISSKH_API_URL environment variable not set. "
            "Please configure your API URL in .env file or set the environment variable."
        )
    if not api_url.endswith("/"):
        api_url += "/"
    return api_url


class KissKHApi:
    def __init__(self):
        self.base_url = _get_api_url()
        self.session = None

    def _drama_api_url(self, drama_id: int) -> str:
        return urljoin(self.base_url, f"info/{drama_id}")

    def _search_api_url(self, query: str) -> str:
        return urljoin(self.base_url, f"search?q={query}")

    def _subtitle_api_url(self, episode_id: int) -> str:
        return urljoin(self.base_url, f"resolve/{episode_id}")

    def _stream_api_url(self, episode_id: int) -> str:
        return urljoin(self.base_url, f"resolve/{episode_id}")

    def _get_session(self) -> requests.Session:
        if self.session is None:
            self.session = requests.Session()
        return self.session

    def _request(self, url: str) -> requests.models.Response:
        """Helper for all the request call

        :param url: url to do the get request on
        :return: reponse for a specific get request
        """
        logger.debug(f"Making GET {url}")
        session = self._get_session()
        response = session.get(url)
        response.raise_for_status()
        response_json = response.json()
        logger.debug(f"Response: {json.dumps(response_json, indent=4)}")
        return response

    def get_episode_ids(
        self, drama_id: int, start: int = 1, stop: int = sys.maxsize
    ) -> Dict[int, int]:
        """Get episode ids for a specific drama

        :param drama_id: drama id
        :param start: starting episode, defaults to 1
        :param stop: ending episode, defaults to sys.maxsize
        :return: returns episode id for starting episode till ending episode range
        """
        drama_api_url = self._drama_api_url(drama_id=drama_id)
        response = self._request(drama_api_url)
        drama = Drama.model_validate(response.json())
        return drama.get_episodes_ids(start=start, stop=stop)

    def get_subtitles(self, episode_id: int, *language_filter: str) -> List[SubItem]:
        subtitle_api_url = self._subtitle_api_url(episode_id=episode_id)
        response = self._request(subtitle_api_url)
        data = response.json()
        subtitles_data = data.get("subtitles", [])
        subtitles: Sub = Sub.model_validate(subtitles_data)

        lang_code_map = {
            "en": "english",
            "km": "khmer",
            "id": "indonesia",
            "ms": "malay",
            "ar": "arabic",
            "zh": "chinese",
            "th": "thai",
            "vi": "vietnamese",
            "tl": "tagalog",
            "my": "burmese",
            "lo": "lao",
            "hi": "hindi",
        }

        filter_lower = [lang.lower() for lang in language_filter]
        filter_mapped = [lang_code_map.get(f, f) for f in filter_lower]

        filtered_subtitles: List[SubItem] = []
        if "all" in language_filter:
            filtered_subtitles.extend(subtitle for subtitle in subtitles)
        elif language_filter:
            filtered_subtitles.extend(
                subtitle
                for subtitle in subtitles
                if subtitle.label.lower() in filter_mapped
                or subtitle.label.lower() in filter_lower
            )
        else:
            filtered_subtitles.extend(subtitle for subtitle in subtitles)
        return filtered_subtitles

    def search_dramas_by_query(self, query: str) -> Search:
        """Get all drama for a specific search query

        :param query: search string
        :return: dramas for that search query
        """
        search_api_url = self._search_api_url(query)
        response = self._request(search_api_url)
        return Search.model_validate(response.json())

    def get_stream_url(self, episode_id: int) -> str:
        stream_api_url = self._stream_api_url(episode_id)
        response = self._request(stream_api_url)
        return response.json()["stream"]["Video"]

    def get_drama_by_query(self, query: str) -> Optional[DramaInfo]:
        """Select specific drama from a search query

        :param query: search string
        :return: information for drama which is selected
        """
        dramas = self.search_dramas_by_query(query=query)
        if len(dramas) == 0:
            logger.warning(
                f"No drama with query {query} found! "
                "Make sure you spelled everything correct."
            )
            return None

        user_selection = 0
        while user_selection < 1 or user_selection > len(dramas) + 1:
            for index, drama in enumerate(dramas, start=1):
                logger.info(f"{index}. {drama.title}")

            user_selection = int(input("Select a drama from above: "))

        return dramas[user_selection - 1]
