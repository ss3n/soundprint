from src.common.tracker import TrackerCommon


class ArtisterCommon:
    ARTIST_ID = TrackerCommon.ARTIST_ID
    ARTIST_NAME = ('ARTIST_NAME', str)
    ARTIST_GENRE = ('ARTIST_GENRE', str)
    ARTIST_POPULARITY = ('ARTIST_POPULARITY', int)

    SCHEMA = [ARTIST_ID[0], ARTIST_NAME[0], ARTIST_GENRE[0], ARTIST_POPULARITY[0]]

    FILE_PATH_PREFIX = 'history/artists/'
