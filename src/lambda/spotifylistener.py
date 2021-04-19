from typing import List
from datetime import datetime, timezone
import tekore as tk
import pandas as pd

from src.common import soundprintutils
from src.common.listener import ListenerCommon

TRACK_DURATION_MS = {}


def extract_playback_info(playback_items: List[tk.model.PlayHistory]) -> List[dict]:
    """
    Given a list of playback track items, extracts the following fields from each track in that list:
        1. When that track was played
        2. Spotify ID for that track
        3. Duration of that track
    :param playback_items: List of tracks
    :return: List of dictionaries, each dict containing extracted fields for a track
    """
    items_dict_list = []

    for item in playback_items:
        item_dict = {}
        soundprintutils.update_dict_by_schema(item_dict, ListenerCommon.TIMESTAMP,
                                              item.played_at.replace(tzinfo=timezone.utc).timestamp())
        soundprintutils.update_dict_by_schema(item_dict, ListenerCommon.TRACK_ID, item.track.id)

        TRACK_DURATION_MS[item.track.id] = item.track.duration_ms

        items_dict_list.append(item_dict)

    return items_dict_list


def get_tracks_played_after(spotify_client: tk.Spotify, after_timestamp_ms: int) -> pd.DataFrame:
    """
    Using the spotify-client, this function will query Spotify Web API to get recently played tracks after the
    point of time specified by the provided timestamp.
    The results are extracted, parsed and returned in a pandas DataFrame with schema according to ListenerCommon#SCHEMA.
    The column for ListenerCommon#LISTENED_TIME is not populated for any row and is NaN
    :param spotify_client: Client with access token to query Spotify Web API
    :param after_timestamp_ms: Epoch time in milliseconds after which recently played tracks are to be queried
    :return: pandas DataFrame with relevant fields of recently played soundtracks on Spotify
    """
    df = pd.DataFrame([], columns=ListenerCommon.SCHEMA)

    response = spotify_client.playback_recently_played(limit=50, after=after_timestamp_ms)
    while len(response.items) > 0:
        df = df.append(pd.DataFrame(extract_playback_info(response.items), columns=ListenerCommon.SCHEMA))
        if response.cursors is None:
            break
        else:
            next_after_ms = int(response.cursors.after)
            response = spotify_client.playback_recently_played(limit=50, after=next_after_ms)

    return df


def update_listened_to_durations(playtracks_df: pd.DataFrame, current_timestamp_ms: int) -> pd.DataFrame:
    """
    Given a populated pandas DataFrame containing extracted data from recently played tracks according to
    ListenerCommon#SCHEMA, calculate the time in milliseconds spent in listening to each track.
    Returns an updated pandas DataFrame with ListenerCommon#LISTENED_TIME filled in with results of the calculation.
    The returned dataframe is sorted in ascending order of timestamp of when the track was played.
    :param playtracks_df: The input pandas DataFrame
    :param current_timestamp_ms: The timestamp of the time when query was run
    :return: Output pandas DataFrame with calculated ListenerCommon#LISTENED_TIME, sorted by when track was played in
    ascending order
    """
    playtracks_df = playtracks_df.sort_values(ListenerCommon.TIMESTAMP[0], ascending=False)

    listened_ms_list = []
    more_recent_timestamp_ms = current_timestamp_ms

    for index, row in playtracks_df.iterrows():
        track_duration_ms = TRACK_DURATION_MS[row[ListenerCommon.TRACK_ID[0]]]
        played_at_timestamp_ms = int(row[ListenerCommon.TIMESTAMP[0]]*1000)

        # If the time-gap between when this track was played and when next track was played is longer than the
        # track's duration, assume the entire track was listened to and use track-duration as value
        # Else, use time-gap between when this track was played and when next track was played
        if (more_recent_timestamp_ms - played_at_timestamp_ms) > track_duration_ms:
            listened_ms_list.append(ListenerCommon.LISTENED_TIME[1](track_duration_ms))
        else:
            listened_ms_list.append(ListenerCommon.LISTENED_TIME[1](more_recent_timestamp_ms - played_at_timestamp_ms))

        more_recent_timestamp_ms = played_at_timestamp_ms

    listened_ms_series = pd.Series(listened_ms_list, name=ListenerCommon.LISTENED_TIME[0], index=playtracks_df.index)
    playtracks_df.update(listened_ms_series)

    return playtracks_df.sort_values(ListenerCommon.TIMESTAMP[0], ascending=True)


def lambda_handler(event, context):
    """
    Lambda handler for the action of querying most recently heard tracks in the last 1 hour from Spotify
    and uploading the results into a CSV file in the S3 bucket.
    The CSV file follows the schema for ListenerCommon#SCHEMA.
    :return uploaded S3 file name with listening history
    """
    # First, get access token
    access_token = soundprintutils.get_access_token()

    # Initialize Spotify client and query tracks played in the last hour
    spotify = tk.Spotify(access_token)
    current_timestamp_ms = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
    snapshot_begin_timestamp_ms = current_timestamp_ms - 3600*1000
    tracks_df = get_tracks_played_after(spotify, snapshot_begin_timestamp_ms)

    # Calculate time spent in listening to each track
    tracks_df = update_listened_to_durations(tracks_df, current_timestamp_ms)

    # Upload to S3 as a CSV
    dt = datetime.fromtimestamp(current_timestamp_ms/1000, tz=timezone.utc)
    s3_file_name = f"{ListenerCommon.FILE_PATH_PREFIX}{dt.year}/{dt.month}/{dt.day}/" \
                   f"{dt.hour}-{dt.day}-{dt.month}-{dt.year}.csv"
    soundprintutils.upload_df_to_s3_csv(df=tracks_df, include_index=False, file_name=s3_file_name)

    return s3_file_name
