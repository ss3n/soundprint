class ListenerCommon:
    TIMESTAMP = ('PLAYED_AT', float)
    TRACK_ID = ('TRACK_ID', str)
    LISTENED_TIME = ('LISTENED_MS', int)

    SCHEMA = [TIMESTAMP[0], TRACK_ID[0], LISTENED_TIME[0]]

    FILE_PATH_PREFIX = 'history/listening/'
