from src.common import soundprintutils
from src.common.listener import ListenerCommon
from src.common.tracker import TrackerCommon
from src.common.albumer import AlbumerCommon
from src.common.artister import ArtisterCommon
from src.common.joiner import JoinerCommon


def lambda_handler(file_names_map, context):
    """
    :param file_names_map: Map containing file-keyword to S3 file-name mapping with the following expected values:
    listening: <S3 file path for the file containing list of tracks recently listened to and their play-timestamp>
    tracks: <S3 file path for file containing track-metadata for recently listened to tracks>
    albums: <S3 file path for file containing album-metadata for albums recently listened to>
    artists: <S3 file path for file containing artist-metadata for artists recently listened to>
    :param context:
    :return:
    """
    listening_file_name = file_names_map['listening']
    tracks_file_name = file_names_map['tracks']
    albums_file_name = file_names_map['albums']
    artists_file_name = file_names_map['artists']

    # Download all the dataframes from S3
    listening_df = soundprintutils.download_df_from_s3_csv(listening_file_name, ListenerCommon.SCHEMA)
    tracks_df = soundprintutils.download_df_from_s3_csv(tracks_file_name, TrackerCommon.SCHEMA)
    albums_df = soundprintutils.download_df_from_s3_csv(albums_file_name, AlbumerCommon.SCHEMA)
    artists_df = soundprintutils.download_df_from_s3_csv(artists_file_name, ArtisterCommon.SCHEMA)

    # Join all the dataframes together
    joined_df = listening_df.merge(
        tracks_df, on=TrackerCommon.TRACK_ID[0]
    ).merge(
        albums_df, on=AlbumerCommon.ALBUM_ID[0]
    ).merge(
        artists_df, on=ArtisterCommon.ARTIST_ID[0]
    )

    # Rearrange data-frame to be in ascending order of listened-timestamp and follow the right schema
    assert joined_df.columns.size == len(JoinerCommon.SCHEMA)
    joined_df = joined_df[JoinerCommon.SCHEMA]
    joined_df = joined_df.sort_values(ListenerCommon.TIMESTAMP[0], ascending=True)

    # Upload to S3 as a CSV
    joint_file_name = f"{JoinerCommon.FILE_PATH_PREFIX}{listening_file_name.split(ListenerCommon.FILE_PATH_PREFIX)[1]}"
    soundprintutils.upload_df_to_s3_csv(joined_df, False, joint_file_name)

    return joint_file_name
