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
    return
