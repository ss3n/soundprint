from src.common.listener import ListenerCommon
from src.common.tracker import TrackerCommon
from src.common.albumer import AlbumerCommon
from src.common.artister import ArtisterCommon


class JoinerCommon:
    SCHEMA = [
        # Listening fields
        ListenerCommon.TIMESTAMP,
        ListenerCommon.LISTENED_TIME,

        # Track attributes
        TrackerCommon.TRACK_ID,
        TrackerCommon.NAME,
        TrackerCommon.DURATION_MS,
        TrackerCommon.POPULARITY,
        TrackerCommon.EXPLICIT,
        TrackerCommon.ACOUSTICNESS,
        TrackerCommon.DANCEABILITY,
        TrackerCommon.ENERGY,
        TrackerCommon.LIVENESS,
        TrackerCommon.LOUDNESS,
        TrackerCommon.INSTRUMENTALNESS,
        TrackerCommon.SPEECHINESS,
        TrackerCommon.VALENCE,
        TrackerCommon.KEY,
        TrackerCommon.MODE,
        TrackerCommon.TEMPO,
        TrackerCommon.TIME_SIGNATURE,

        # Album attributes
        AlbumerCommon.ALBUM_ID,
        AlbumerCommon.TYPE,
        AlbumerCommon.GENRE,
        AlbumerCommon.LABEL,
        AlbumerCommon.NAME,
        AlbumerCommon.POPULARITY,
        AlbumerCommon.RELEASE_DATE,
        AlbumerCommon.TOTAL_TRACKS,
        
        # Artist attributes
        ArtisterCommon.ARTIST_ID,
        ArtisterCommon.ARTIST_NAME,
        ArtisterCommon.ARTIST_GENRE,
        ArtisterCommon.ARTIST_POPULARITY
    ]

    FILE_PATH_PREFIX = 'history/data/'
