from typing import List
from src.common.listener import ListenerCommon

ARTIST_SEPARATOR = '|'


class TrackerCommon:
    TRACK_ID = ListenerCommon.TRACK_ID
    ALBUM_ID = 'ALBUM_ID'
    ARTIST_IDS = 'ARTIST_IDS'
    DURATION_MS = ListenerCommon.DURATION
    NAME = 'TRACK_NAME'
    POPULARITY = 'TRACK_POPULARITY'
    EXPLICIT = 'TRACK_EXPLICIT'

    ACOUSTICNESS = 'TRACK_ACOUSTICNESS'
    DANCEABILITY = 'TRACK_DANCEABILITY'
    ENERGY = 'TRACK_ENERGY'
    INSTRUMENTALNESS = 'TRACK_INSTRUMENTALNESS'
    KEY = 'TRACK_KEY'
    LIVENESS = 'TRACK_LIVENESS'
    LOUDNESS = 'TRACK_LOUDNESS'
    MODE = 'TRACK_MODE'
    SPEECHINESS = 'TRACK_SPEECHINESS'
    TEMPO = 'TRACK_TEMPO'
    TIME_SIGNATURE = 'TRACK_TIME_SIGNATURE'
    VALENCE = 'TRACK_VALENCE'

    SCHEMA = [TRACK_ID, NAME, DURATION_MS, ALBUM_ID, ARTIST_IDS, POPULARITY, EXPLICIT,
              ACOUSTICNESS, DANCEABILITY, ENERGY, LIVENESS, LOUDNESS, INSTRUMENTALNESS, SPEECHINESS, VALENCE,
              KEY, MODE, TEMPO, TIME_SIGNATURE]

    FILE_PATH_PREFIX = 'history/tracks/'

    @staticmethod
    def encode_artist_id_list(list_str: List[str]) -> str:
        """
        Encode a list of artist-id strings into a single string
        :param list_str: List of artist-id strings
        :return: Single string representing the list of artist-ids
        """
        return ARTIST_SEPARATOR.join(list_str)

    @staticmethod
    def decode_artist_id_list(str_list: str) -> List[str]:
        """
        Decode a string representing a list of artist-ids to get a list of artist-id strings
        :param str_list: Single string representing list of artist-ids
        :return: List of artist-id strings
        """
        return str_list.split(ARTIST_SEPARATOR)
