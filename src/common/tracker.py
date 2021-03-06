from src.common.listener import ListenerCommon


class TrackerCommon:
    TRACK_ID = ListenerCommon.TRACK_ID
    ALBUM_ID = ('ALBUM_ID', str)
    ARTIST_ID = ('ARTIST_ID', str)
    DURATION_MS = ('TRACK_DURATION_MS', int)
    NAME = ('TRACK_NAME', str)
    POPULARITY = ('TRACK_POPULARITY', int)
    EXPLICIT = ('TRACK_EXPLICIT', bool)

    ACOUSTICNESS = ('TRACK_ACOUSTICNESS', float)
    DANCEABILITY = ('TRACK_DANCEABILITY', float)
    ENERGY = ('TRACK_ENERGY', float)
    INSTRUMENTALNESS = ('TRACK_INSTRUMENTALNESS', float)
    KEY = ('TRACK_KEY', int)
    LIVENESS = ('TRACK_LIVENESS', float)
    LOUDNESS = ('TRACK_LOUDNESS', float)
    MODE = ('TRACK_MODE', int)
    SPEECHINESS = ('TRACK_SPEECHINESS', float)
    TEMPO = ('TRACK_TEMPO', float)
    TIME_SIGNATURE = ('TRACK_TIME_SIGNATURE', int)
    VALENCE = ('TRACK_VALENCE', float)

    SCHEMA = [TRACK_ID[0], NAME[0], DURATION_MS[0], ALBUM_ID[0], ARTIST_ID[0], POPULARITY[0], EXPLICIT[0],
              ACOUSTICNESS[0], DANCEABILITY[0], ENERGY[0], LIVENESS[0], LOUDNESS[0],
              INSTRUMENTALNESS[0], SPEECHINESS[0], VALENCE[0],
              KEY[0], MODE[0], TEMPO[0], TIME_SIGNATURE[0]]

    FILE_PATH_PREFIX = 'history/tracks/'
