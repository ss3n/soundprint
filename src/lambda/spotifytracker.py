def lambda_handler(event, context):
    """
    Lambda handler for the action of querying spotify for all information related to spotify-soundtracks by track-id.
    The lambda gets triggered when a new file containing the recently played tracks is uploaded to S3. The S3 object
    is passed into the event parameter triggering the function.
    This function reads the S3 object CSV file containing the track-ids for the recently heard tracks and queries
    Spotify to get the metadata about all those tracks. This metadata is compiled into a CSV file as a table with
    primary key being track-id. This CSV is uploaded to S3.
    :param event: S3 Event, triggering function, containing information about the object that triggered this function.
    :param context:
    """
    pass
