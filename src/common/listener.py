class ListenerCommon:
    TIMESTAMP = 'PLAYED_AT'
    TRACK_ID = 'TRACK_ID'
    LISTENED_TIME = 'LISTENED_MS'

    SCHEMA = [TIMESTAMP, TRACK_ID, LISTENED_TIME]

    FILE_PATH_PREFIX = 'history/listening/'
