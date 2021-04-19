from src.common.listener import ListenerCommon
from src.common.tracker import TrackerCommon
from src.common.albumer import AlbumerCommon
from src.common.artister import ArtisterCommon


class JoinerCommon:
    # Listening fields
    LISTEN_TIMESTAMP = ListenerCommon.TIMESTAMP
    LISTENED_TIME = ListenerCommon.LISTENED_TIME

    # Track attributes
    TRACK_ID = TrackerCommon.TRACK_ID
    TRACK_NAME = TrackerCommon.NAME
    TRACK_DURATION_MS = TrackerCommon.DURATION_MS
    TRACK_POPULARITY = TrackerCommon.POPULARITY
    TRACK_EXPLICIT = TrackerCommon.EXPLICIT
    TRACK_ACOUSTICNESS = TrackerCommon.ACOUSTICNESS
    TRACK_DANCEABILITY = TrackerCommon.DANCEABILITY
    TRACK_ENERGY = TrackerCommon.ENERGY
    TRACK_LIVENESS = TrackerCommon.LIVENESS
    TRACK_LOUDNESS = TrackerCommon.LOUDNESS
    TRACK_INSTRUMENTALNESS = TrackerCommon.INSTRUMENTALNESS
    TRACK_SPEECHINESS = TrackerCommon.SPEECHINESS
    TRACK_VALENCE = TrackerCommon.VALENCE
    TRACK_KEY = TrackerCommon.KEY
    TRACK_MODE = TrackerCommon.MODE
    TRACK_TEMPO = TrackerCommon.TEMPO
    TRACK_TIME_SIGNATURE = TrackerCommon.TIME_SIGNATURE

    # Albums attributes
    ALBUM_ID = AlbumerCommon.ALBUM_ID
    ALBUM_TYPE = AlbumerCommon.TYPE
    ALBUM_GENRE = AlbumerCommon.GENRE
    ALBUM_LABEL = AlbumerCommon.LABEL
    ALBUM_NAME = AlbumerCommon.NAME
    ALBUM_POPULARITY = AlbumerCommon.POPULARITY
    ALBUM_RELEASE_DATE = AlbumerCommon.RELEASE_DATE
    ALBUM_TOTAL_TRACKS = AlbumerCommon.TOTAL_TRACKS

    # Artists attributes
    ARTIST_ID = ArtisterCommon.ARTIST_ID
    ARTIST_NAME = ArtisterCommon.ARTIST_NAME
    ARTIST_GENRE = ArtisterCommon.ARTIST_GENRE
    ARTIST_POPULARITY = ArtisterCommon.ARTIST_POPULARITY

    SCHEMA = [
        # Listening fields
        LISTEN_TIMESTAMP[0],
        LISTENED_TIME[0],
        
        # Track attributes
        TRACK_ID[0],
        TRACK_NAME[0],
        TRACK_DURATION_MS[0],
        TRACK_POPULARITY[0],
        TRACK_EXPLICIT[0],
        TRACK_ACOUSTICNESS[0],
        TRACK_DANCEABILITY[0],
        TRACK_ENERGY[0],
        TRACK_LIVENESS[0],
        TRACK_LOUDNESS[0],
        TRACK_INSTRUMENTALNESS[0],
        TRACK_SPEECHINESS[0],
        TRACK_VALENCE[0],
        TRACK_KEY[0],
        TRACK_MODE[0],
        TRACK_TEMPO[0],
        TRACK_TIME_SIGNATURE[0],

        # Album attributes
        ALBUM_ID[0],
        ALBUM_TYPE[0],
        ALBUM_GENRE[0],
        ALBUM_LABEL[0],
        ALBUM_NAME[0],
        ALBUM_POPULARITY[0],
        ALBUM_RELEASE_DATE[0],
        ALBUM_TOTAL_TRACKS[0],
        
        # Artist attributes
        ARTIST_ID[0],
        ARTIST_NAME[0],
        ARTIST_GENRE[0],
        ARTIST_POPULARITY[0]
    ]

    FILE_PATH_PREFIX = 'history/data/'
