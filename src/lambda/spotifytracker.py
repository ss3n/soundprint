from typing import List
import tekore as tk
import pandas as pd

from src.common import soundprintutils
from src.common.listener import ListenerCommon
from src.common.tracker import TrackerCommon


def get_tracks_data(spotify_client: tk.Spotify, track_ids: List[str]) -> pd.DataFrame:
    """
    Given a spotify-client and a list of track-ids, compiles a data-frame with metadata for all the tracks in the list.
    The compiled metadata contains the following fields:
    1. track-id
    2. name of the track
    3. duration of the track in milliseconds
    4. album-id of the album the track belongs to
    5. artist-id for the track - if there are multiple artists, this track will have multiple rows, one for each artist
    6. track's popularity
    7. track explicit tag - true/false
    8. acousticness - probability (0-1) of track being acoustic
    9. danceability - (0-1) measure of how suitable track is for dancing
    10. energy - (0-1) measure of intensity and activity in track. Energetic tracks feel fast, loud, and noisy
    11. liveness - (0-1) confidence measure of track was performed in front of live audience
    12. loudness - The overall loudness of a track in decibels (dB)
    13. instrumentalness - (0-1) measure of confidence about track containing no vocals
    14. speechiness - (0-1) confidence measure of the presence of spoken words in a track
    15. valence - (0-1) measure of describing the musical positiveness conveyed by a track
    16. key - Integers map to pitches using standard Pitch Class notation (https://en.wikipedia.org/wiki/Pitch_class)
    17. mode - Major is represented by 1 and minor is 0.
    18. tempo - overall beats per minute
    19. time-signature - integer notational convention to specify how many beats are in each bar
    :return: DataFrame with schema according to TrackerCommon.SCHEMA
    """
    # Get track-objects and track-audio-features for all tracks from querying Spotify
    tracks_metadata = spotify_client.tracks(track_ids) if len(track_ids) > 0 else []
    tracks_audio_features = spotify_client.tracks_audio_features(track_ids) if len(track_ids) > 0 else []

    track_dict_list = []
    for index, track_id in enumerate(track_ids):
        assert tracks_metadata[index].id == track_id, f"Track metadata object mismatch at index {index}"
        assert tracks_audio_features[index].id == track_id, f"Track audio-features object mismatch at index {index}"

        track_metadata = tracks_metadata[index]
        track_audio_features = tracks_audio_features[index]

        track_dict = {}
        soundprintutils.update_dict_by_schema(track_dict, TrackerCommon.TRACK_ID, track_id)
        soundprintutils.update_dict_by_schema(track_dict, TrackerCommon.ALBUM_ID, track_metadata.album.id)
        soundprintutils.update_dict_by_schema(track_dict, TrackerCommon.DURATION_MS, track_metadata.duration_ms)
        soundprintutils.update_dict_by_schema(track_dict, TrackerCommon.NAME, track_metadata.name)
        soundprintutils.update_dict_by_schema(track_dict, TrackerCommon.POPULARITY, track_metadata.popularity)
        soundprintutils.update_dict_by_schema(track_dict, TrackerCommon.EXPLICIT, track_metadata.explicit)
        soundprintutils.update_dict_by_schema(track_dict, TrackerCommon.ACOUSTICNESS, track_audio_features.acousticness)
        soundprintutils.update_dict_by_schema(track_dict, TrackerCommon.DANCEABILITY, track_audio_features.danceability)
        soundprintutils.update_dict_by_schema(track_dict, TrackerCommon.ENERGY, track_audio_features.energy)
        soundprintutils.update_dict_by_schema(track_dict,
                                              TrackerCommon.INSTRUMENTALNESS, track_audio_features.instrumentalness)
        soundprintutils.update_dict_by_schema(track_dict, TrackerCommon.KEY, track_audio_features.key)
        soundprintutils.update_dict_by_schema(track_dict, TrackerCommon.LIVENESS, track_audio_features.liveness)
        soundprintutils.update_dict_by_schema(track_dict, TrackerCommon.LOUDNESS, track_audio_features.loudness)
        soundprintutils.update_dict_by_schema(track_dict, TrackerCommon.MODE, track_audio_features.mode)
        soundprintutils.update_dict_by_schema(track_dict, TrackerCommon.SPEECHINESS, track_audio_features.speechiness)
        soundprintutils.update_dict_by_schema(track_dict, TrackerCommon.TEMPO, track_audio_features.tempo)
        soundprintutils.update_dict_by_schema(track_dict,
                                              TrackerCommon.TIME_SIGNATURE, track_audio_features.time_signature)
        soundprintutils.update_dict_by_schema(track_dict, TrackerCommon.VALENCE, track_audio_features.valence)

        track_artists = list(map(lambda artist: artist.id, track_metadata.artists))
        track_dict_list += soundprintutils.normalize_dict_field_list(track_dict, track_artists, TrackerCommon.ARTIST_ID)

    return pd.DataFrame(track_dict_list, columns=TrackerCommon.SCHEMA)


def lambda_handler(listened_file_name, context):
    """
    Lambda handler for the action of querying spotify for all information related to spotify-soundtracks by track-id.
    This function reads the S3 object CSV file containing the track-ids for the recently heard tracks and queries
    Spotify to get the metadata about all those tracks. This metadata is compiled into a CSV file as a table with
    primary key being track-id. This CSV is uploaded to S3.
    :param listened_file_name: S3 file name containing track-ids of tracks recently listened to
    :param context:
    :return: S3 file name of tracks file containing track-metadata for tracks recently listened to
    """
    # Read S3 Event to get the created csv file containing track-ids to query
    listened_df = soundprintutils.download_df_from_s3_csv(listened_file_name, ListenerCommon.SCHEMA)

    track_ids = list(set(listened_df[ListenerCommon.TRACK_ID[0]]))

    # Get Spotify access token and initialize Spotify client
    access_token = soundprintutils.get_access_token()
    spotify = tk.Spotify(access_token)

    # Extract all data related to the recently heard tracks
    tracks_df = get_tracks_data(spotify, track_ids)

    # Upload dataframe to S3 as CSV
    tracks_file_name = f"{TrackerCommon.FILE_PATH_PREFIX}{listened_file_name.split(ListenerCommon.FILE_PATH_PREFIX)[1]}"
    soundprintutils.upload_df_to_s3_csv(df=tracks_df, include_index=False, file_name=tracks_file_name)

    return tracks_file_name
