from typing import List

GENRE_SEPARATOR = '|'


class ArtisterCommon:
    ARTIST_ID = 'ARTIST_ID'
    ARTIST_NAME = 'ARTIST_NAME'
    ARTIST_GENRES = 'ARTIST_GENRES'
    ARTIST_POPULARITY = 'ARTIST_POPULARITY'

    SCHEMA = [ARTIST_ID, ARTIST_NAME, ARTIST_GENRES, ARTIST_POPULARITY]

    FILE_PATH_PREFIX = 'history/artists/'

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
