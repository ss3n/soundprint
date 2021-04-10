from typing import List
import urllib.parse
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
    4. genres - list of genres to classify album, empty if unclassified
    5. album-release-date
    6. label - Music label for releasing the album
    7. album-track-count - total number of tracks in album
    8. album-popularity - (0-100) number signifying album's popularity
    """
    # Query Spotify for albums metadata
    albums_metadata = spotify_client.albums(album_ids)

    album_dict_list = []
    for album in albums_metadata:
        album_dict = {
            AlbumerCommon.ALBUM_ID: album.id,
            AlbumerCommon.TYPE: album.album_type,
            AlbumerCommon.GENRES: AlbumerCommon.encode_genres(album.genres),
            AlbumerCommon.LABEL: album.label,
            AlbumerCommon.NAME: album.name,
            AlbumerCommon.POPULARITY: album.popularity,
            AlbumerCommon.RELEASE_DATE: pd.to_datetime(album.release_date),
            AlbumerCommon.TOTAL_TRACKS: album.total_tracks
        }

        album_dict_list.append(album_dict)

    return pd.DataFrame(album_dict_list, columns=AlbumerCommon.SCHEMA)


def lambda_handler(event, context):
    """
    Lambda handler for the action of querying spotify for all information related to spotify-albums by album-id.
    The lambda gets triggered when a new file containing track-metadata is uploaded to S3. The S3 object is passed
    into the event parameter triggering the function.
    This function reads the S3 object CSV file containing the album-ids for the tracks and queries Spotify to get
    the metadata about all those albums. This metadata is compiled into a CSV file as a table with primary key being
    album-id. This CSV is uploaded to S3.
    :param event:
    :param context:
    :return:
    """
    # Read S3 Event to get the created csv file containing track-ids to query
    tracks_file_name = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    tracks_df = soundprintutils.download_df_from_s3_csv(tracks_file_name, TrackerCommon.SCHEMA)

    album_ids = list(set(tracks_df[TrackerCommon.ALBUM_ID]))

    # Get Spotify access token and initialize Spotify client
    access_token = soundprintutils.get_access_token()
    spotify = tk.Spotify(access_token)

    # Extract all data related to the albums
    albums_df = get_albums_data(spotify, album_ids)

    # Upload dataframe to S3 as CSV
    albums_file_name = f"{AlbumerCommon.FILE_PATH_PREFIX}{tracks_file_name.split(TrackerCommon.FILE_PATH_PREFIX)[1]}"
    soundprintutils.upload_df_to_s3_csv(df=albums_df, include_index=False, file_name=albums_file_name)
