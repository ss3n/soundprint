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

    TYPED_SCHEMA = [
        # Listening fields
        LISTEN_TIMESTAMP,
        LISTENED_TIME,
        
        # Track attributes
        TRACK_ID,
        TRACK_NAME,
        TRACK_DURATION_MS,
        TRACK_POPULARITY,
        TRACK_EXPLICIT,
        TRACK_ACOUSTICNESS,
        TRACK_DANCEABILITY,
        TRACK_ENERGY,
        TRACK_LIVENESS,
        TRACK_LOUDNESS,
        TRACK_INSTRUMENTALNESS,
        TRACK_SPEECHINESS,
        TRACK_VALENCE,
        TRACK_KEY,
        TRACK_MODE,
        TRACK_TEMPO,
        TRACK_TIME_SIGNATURE,

        # Album attributes
        ALBUM_ID,
        ALBUM_TYPE,
        ALBUM_GENRE,
        ALBUM_LABEL,
        ALBUM_NAME,
        ALBUM_POPULARITY,
        ALBUM_RELEASE_DATE,
        ALBUM_TOTAL_TRACKS,
        
        # Artist attributes
        ARTIST_ID,
        ARTIST_NAME,
        ARTIST_GENRE,
        ARTIST_POPULARITY
    ]

    SCHEMA = list(map(lambda ts: ts[0], TYPED_SCHEMA))

    FILE_PATH_PREFIX = 'history/data/'
