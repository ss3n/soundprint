from src.common.tracker import TrackerCommon


class AlbumerCommon:
    ALBUM_ID = TrackerCommon.ALBUM_ID
    TYPE = ('ALBUM_TYPE', str)
    GENRE = ('ALBUM_GENRE', str)
    LABEL = ('ALBUM_LABEL', str)
    NAME = ('ALBUM_NAME', str)
    POPULARITY = ('ALBUM_POPULARITY', int)
    RELEASE_DATE = ('ALBUM_RELEASE_DATE', float)
    TOTAL_TRACKS = ('ALBUM_TRACK_COUNT', int)

    SCHEMA = [ALBUM_ID[0], NAME[0], TYPE[0], GENRE[0], RELEASE_DATE[0], LABEL[0], TOTAL_TRACKS[0], POPULARITY[0]]

    FILE_PATH_PREFIX = 'history/albums/'
