from src.common.tracker import TrackerCommon


class ArtisterCommon:
    ARTIST_ID = TrackerCommon.ARTIST_ID
    ARTIST_NAME = 'ARTIST_NAME'
    ARTIST_GENRE = 'ARTIST_GENRE'
    ARTIST_POPULARITY = 'ARTIST_POPULARITY'

    SCHEMA = [ARTIST_ID, ARTIST_NAME, ARTIST_GENRE, ARTIST_POPULARITY]

    FILE_PATH_PREFIX = 'history/artists/'
