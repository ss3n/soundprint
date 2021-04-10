from typing import List
from src.common.tracker import TrackerCommon

GENRE_SEPARATOR = '|'


class AlbumerCommon:
    ALBUM_ID = TrackerCommon.ALBUM_ID
    TYPE = 'ALBUM_TYPE'
    GENRES = 'ALBUM_GENRES'
    LABEL = 'ALBUM_LABEL'
    NAME = 'ALBUM_NAME'
    POPULARITY = 'ALBUM_POPULARITY'
    RELEASE_DATE = 'ALBUM_RELEASE_DATE'
    TOTAL_TRACKS = 'ALBUM_TRACK_COUNT'

    SCHEMA = [ALBUM_ID, NAME, TYPE, GENRES, RELEASE_DATE, LABEL, TOTAL_TRACKS, POPULARITY]

    FILE_PATH_PREFIX = 'history/albums/'

    @staticmethod
    def encode_genres(list_str: List[str]) -> str:
        """
        Encode a list of genre-strings into a single string representing that list
        :param list_str: List of genres
        :return: Single string representing the list of genres
        """
        return GENRE_SEPARATOR.join(list_str)

    @staticmethod
    def decode_genres(str_list: str) -> List[str]:
        """
        Decode a single string representing a list of genres to a list of genre-strings
        :param str_list: Single string representing a list of genres
        :return: List of genre-strings
        """
        return str_list.split(GENRE_SEPARATOR)
