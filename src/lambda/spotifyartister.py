from typing import List
import tekore as tk
import pandas as pd

from src.common import soundprintutils
from src.common.tracker import TrackerCommon
from src.common.artister import ArtisterCommon


def get_artists_data(spotify_client: tk.Spotify, artist_ids: List[str]) -> pd.DataFrame:
    """
    Given a spotify-client and list of artist-ids, compiles a dataframe with metadata for all the artists.
    The compiled metadata contains the following fields for each artist:
    1. artist-id
    2. artist-name
    3. artist-genres - encoded list of genres associated with the artist
    4. artist-popularity - (0-100) measure of artist's popularity
    """
    # Query Spotify for artists metadata
    artists_metadata = spotify_client.artists(artist_ids) if len(artist_ids) > 0 else []

    artist_dict_list = []
    for artist in artists_metadata:
        artist_dict = {
            ArtisterCommon.ARTIST_ID: artist.id,
            ArtisterCommon.ARTIST_NAME: artist.name,
            ArtisterCommon.ARTIST_GENRES: ArtisterCommon.encode_genres(artist.genres),
            ArtisterCommon.ARTIST_POPULARITY: artist.popularity
        }

        artist_dict_list.append(artist_dict)

    return pd.DataFrame(artist_dict_list, columns=ArtisterCommon.SCHEMA)


def lambda_handler(event, context):
    """
    Lambda handler for the action of querying spotify for all information related to spotify-artists by artist-id.
    The lambda gets triggered when a new file containing track-metadata is uploaded to S3. The S3 object is passed
    into the event parameter triggering the function.
    This function reads the S3 object CSV file containing the artist-ids for the tracks and queries Spotify to get
    the metadata about all those artists. This metadata is compiled into a CSV file as a table with primary key being
    album-id. This CSV is uploaded to S3.
    :param event: S3 Event, triggering function, containing information about the object that triggered this function.
    :param context:
    :return:
    """
    # Read S3 Event to get the created csv file containing track-ids to query
    tracks_file_name = soundprintutils.extract_s3_key_sns_event(event=event)
    tracks_df = soundprintutils.download_df_from_s3_csv(tracks_file_name, TrackerCommon.SCHEMA)

    artist_ids = [
        artist_id
        for encoded_sublist in tracks_df[TrackerCommon.ARTIST_IDS]
        for artist_id in TrackerCommon.decode_artist_id_list(encoded_sublist)
    ]

    # Get Spotify access token and initialize Spotify client
    access_token = soundprintutils.get_access_token()
    spotify = tk.Spotify(access_token)

    # Extract all data related to the artists
    artists_df = get_artists_data(spotify, artist_ids)

    # Upload dataframe to S3 as CSV
    artists_file_name = f"{ArtisterCommon.FILE_PATH_PREFIX}{tracks_file_name.split(TrackerCommon.FILE_PATH_PREFIX)[1]}"
    soundprintutils.upload_df_to_s3_csv(df=artists_df, include_index=False, file_name=artists_file_name)
