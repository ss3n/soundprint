from typing import List

import boto3
from datetime import datetime
import tekore as tk
import pandas as pd
import io
import json

S3_BUCKET = 'soundprint-bucket'


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
    assert file_name.endswith('.csv'), f"{file_name} does not end with .csv"

    csv_string_buffer = io.StringIO()
    df.to_csv(csv_string_buffer, index=include_index)
    csv_string = csv_string_buffer.getvalue()
    csv_string_buffer.close()

    s3 = boto3.client('s3')
    s3.put_object(Bucket=S3_BUCKET, Key=file_name, Body=bytes(csv_string, 'utf-8'))


def download_df_from_s3_csv(file_name: str, expected_schema: List[str]) -> pd.DataFrame:
    """
    Downloads a CSV file from S3 and creates a pandas dataframe with the contents
    :param file_name: bucket key name for the file to be downloaded
    :param expected_schema: Expected schema of the dataframe
    :return: pandas DataFrame object populated with the file's contents
    """
    assert file_name.endswith('.csv'), f"{file_name} does not end with .csv"

    s3 = boto3.client('s3')
    s3_response = s3.get_object(Bucket=S3_BUCKET, Key=file_name)

    csv_string = str(s3_response.get('Body').read(), encoding='utf-8')
    csv_string_buffer = io.StringIO(csv_string)
    df = pd.read_csv(csv_string_buffer)
    csv_string_buffer.close()

    assert list(df.columns) == expected_schema, \
        f"{file_name} does not match expected schema; expected: {expected_schema}, actual: {df.columns}"

    return df


def extract_s3_key_sns_event(event, expected_bucket=S3_BUCKET):
    """
    Upon receiving an SNS notification, extracts the S3 key in the event
    """
    message = json.loads(event['Records'][0]['Sns']['Message'])
    bucket = message['Records'][0]['s3']['bucket']['name']
    assert bucket == expected_bucket, \
        f"event bucket does not match expectation: expected: {expected_bucket}, actual: {bucket}"
    return message['Records'][0]['s3']['object']['key']


def normalize_dict_field_list(dictt: dict, field_values: List, field_key) -> List[dict]:
    """
    Given a dictionary, a field-key and a list of values for the field, returns a list of dictionaries where each
    dictionary has a mapping of field-key to one of the values in the list of field-values
    :param dictt: Common dictionary that will feature in the list of normalized dictionaries
    :param field_values: List of field-values to normalize the common dictionary by
    :param field_key: The field's key
    :return: List of normalized dictionaries where each dictionary contains a unique field-value mapped to the field-key
    """
    if len(field_values) == 0:
        return [dictt]
    else:
        normalized_list = []
        for value in field_values:
            normalized_dict = {field_key: value}
            normalized_dict.update(dictt)
            normalized_list.append(normalized_dict)
        return normalized_list
