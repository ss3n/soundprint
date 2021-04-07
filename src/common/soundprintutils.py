import boto3
from datetime import datetime
import tekore as tk
import pandas as pd
import io


def get_access_token():
    """
    Returns an access token for interfacing with Spotify Web API. Refreshes it if needed.
    :return: String access token
    """
    ddb_token_item_key = {'spotify': 'prod'}
    ddb_credentials_item_key = {'spotify': 'Soundprint'}

    access_token_ddb_key = 'accessToken'
    expires_at_ddb_key = 'expiresAt'

    client_id_ddb_key = 'clientId'
    client_secret_ddb_key = 'clientSecret'
    refresh_token_ddb_key = 'refreshToken'

    ddb_table = boto3.resource('dynamodb').Table('SpotifyTokenState')

    # Get currently stored access token
    current_token_item = ddb_table.get_item(Key=ddb_token_item_key)['Item']

    if current_token_item[expires_at_ddb_key] > datetime.now().timestamp():
        # If current token has not expired yet, return it
        return current_token_item[access_token_ddb_key]
    else:
        # If current token has expired, refresh it and update token store,
        # then attempt getting stored token again
        credentials_item = ddb_table.get_item(Key=ddb_credentials_item_key)['Item']
        client_id = credentials_item[client_id_ddb_key]
        client_secret = credentials_item[client_secret_ddb_key]
        refresh_token = credentials_item[refresh_token_ddb_key]

        refreshing_token = tk.refresh_user_token(client_id, client_secret, refresh_token)

        new_token_item = {
            access_token_ddb_key: refreshing_token.access_token,
            expires_at_ddb_key: int(datetime.now().timestamp()) + 3200
        }
        new_token_item.update(ddb_token_item_key)

        ddb_table.put_item(Item=new_token_item)
        return get_access_token()


def upload_df_to_s3_csv(df: pd.DataFrame, include_index: bool, file_name: str):
    """
    Uploads a pandas dataframe to S3 bucket spotify-listener-bucket as a CSV file
    :param df: dataframe to upload
    :param include_index: if true, includes index values of dataframe into the csv file as a column
    :param file_name: s3 file path for CSV file in the bucket
    """
    csv_string_buffer = io.StringIO()
    df.to_csv(csv_string_buffer, index=include_index)
    csv_string = csv_string_buffer.getvalue()
    csv_string_buffer.close()

    s3_connection = boto3.resource('s3')
    s3_connection.Object('soundprint-bucket', file_name).put(Body=bytes(csv_string, 'utf-8'))
