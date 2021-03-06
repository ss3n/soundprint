from typing import List
import tekore as tk
import pandas as pd

from src.common import soundprintutils
from src.common.tracker import TrackerCommon
from src.common.albumer import AlbumerCommon


def get_albums_data(spotify_client: tk.Spotify, album_ids: List[str]) -> pd.DataFrame:
    """
    Given a spotify-client and list of album-ids, compiles a dataframe with metadata for all the albums.
    The compiled metadata contains the following fields for each album:
    1. album-id
    2. album-name
    3. album-type - album/single/compilation
    4. genre - if album has multiple generes, there will a row for the album for each genre
    5. album-release-date
    6. label - Music label for releasing the album
    7. album-track-count - total number of tracks in album
    8. album-popularity - (0-100) number signifying album's popularity
    """
    # Query Spotify for albums metadata
    albums_metadata = spotify_client.albums(album_ids) if len(album_ids) > 0 else []

    album_dict_list = []
    for album in albums_metadata:
        album_dict = {}
        soundprintutils.update_dict_by_schema(album_dict, AlbumerCommon.ALBUM_ID, album.id)
        soundprintutils.update_dict_by_schema(album_dict, AlbumerCommon.TYPE, album.album_type)
        soundprintutils.update_dict_by_schema(album_dict, AlbumerCommon.LABEL, album.label)
        soundprintutils.update_dict_by_schema(album_dict, AlbumerCommon.NAME, album.name)
        soundprintutils.update_dict_by_schema(album_dict, AlbumerCommon.POPULARITY, album.popularity)
        soundprintutils.update_dict_by_schema(album_dict, AlbumerCommon.RELEASE_DATE,
                                              pd.to_datetime(album.release_date).timestamp())
        soundprintutils.update_dict_by_schema(album_dict, AlbumerCommon.TOTAL_TRACKS, album.total_tracks)

        genres = album.genres
        album_dict_list += soundprintutils.normalize_dict_field_list(album_dict, genres, AlbumerCommon.GENRE)

    return pd.DataFrame(album_dict_list, columns=AlbumerCommon.SCHEMA)


def lambda_handler(tracks_file_name, context):
    """
    Lambda handler for the action of querying spotify for all information related to spotify-albums by album-id.
    This function reads the S3 object CSV file containing the album-ids for the tracks and queries Spotify to get
    the metadata about all those albums. This metadata is compiled into a CSV file as a table with primary key being
    album-id. This CSV is uploaded to S3.
    :param tracks_file_name: S3 file containing track-metadata with album-ids for tracks recently listened to
    :param context:
    :return: uploaded S3 file name for file containing album-metadata
    """
    # Read S3 Event to get the created csv file containing track-ids to query
    tracks_df = soundprintutils.download_df_from_s3_csv(tracks_file_name, TrackerCommon.SCHEMA)

    album_ids = list(set(tracks_df[TrackerCommon.ALBUM_ID[0]].dropna()))

    # Get Spotify access token and initialize Spotify client
    access_token = soundprintutils.get_access_token()
    spotify = tk.Spotify(access_token)

    # Extract all data related to the albums
    albums_df = get_albums_data(spotify, album_ids)

    # Upload dataframe to S3 as CSV
    albums_file_name = f"{AlbumerCommon.FILE_PATH_PREFIX}{tracks_file_name.split(TrackerCommon.FILE_PATH_PREFIX)[1]}"
    soundprintutils.upload_df_to_s3_csv(df=albums_df, include_index=False, file_name=albums_file_name)

    return albums_file_name
