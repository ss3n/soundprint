import time
from typing import List
import pandas as pd
import logging

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from src.common import soundprintutils
from src.common.joiner import JoinerCommon

SECRETS_ARN = soundprintutils.get_db_secrets_arn()
AURORA_CLUSTER_ARN = soundprintutils.get_rds_cluster_arn()

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)


def create_table_if_not_exists(rds_client):
    """
    CREATE Aurora Table for Soundprint if it doesn't already exist. Returns the CREATE call response.
    """
    schema_str = ""
    for ts in JoinerCommon.TYPED_SCHEMA:
        schema_str += f"{ts[0]} {data_type_to_sql_type(ts[1], schema_type=True)},\n"

    primary_key_str = f"PRIMARY KEY ({JoinerCommon.LISTEN_TIMESTAMP[0]}, {JoinerCommon.TRACK_ID[0]}, " \
                      f"{JoinerCommon.ALBUM_ID[0]}, {JoinerCommon.ALBUM_GENRE[0]}, " \
                      f"{JoinerCommon.ARTIST_ID[0]}, {JoinerCommon.ARTIST_GENRE[0]})"

    create_table_sql = f"CREATE TABLE IF NOT EXISTS {soundprintutils.AURORA_HISTORY_TABLE}(\n" \
                       f"{schema_str}\n" \
                       f"{primary_key_str}\n" \
                       f")"

    return execute_sql(rds_client, create_table_sql)


def insert_data_rows(joined_df: pd.DataFrame, rds_client):
    """
    Inserts rows from the DataFrame following JoinerCommon.TYPED_SCHEMA into the Aurora Table.
    Returns the insertion batch request response
    """
    insert_columns_str = ""
    insert_values_str = ""
    for col_num, col_name in enumerate(JoinerCommon.SCHEMA):
        insert_columns_str += col_name
        insert_values_str += f":{col_name}"
        if col_num != len(JoinerCommon.SCHEMA) - 1:
            insert_columns_str += ', '
            insert_values_str += ', '

    sql_statement = \
        f"INSERT INTO {soundprintutils.AURORA_HISTORY_TABLE} ({insert_columns_str}) values ({insert_values_str})"

    sql_parameter_sets = []
    for index, row in joined_df.iterrows():
        row_entry = []
        for ts in JoinerCommon.TYPED_SCHEMA:
            row_entry.append({
                'name': ts[0],
                'value': {data_type_to_sql_type(ts[1], schema_type=False): ts[1](row[ts[0]])}
            })
        sql_parameter_sets.append(row_entry)

    return execute_batch_sql(rds_client, sql_statement, sql_parameter_sets)


def data_type_to_sql_type(dtype: classmethod, schema_type=False) -> str:
    """
    Convert from Python data-type to SQL identified data-type specification.
    If schema_type is true, the returned SQL data-type will be type for defining the column schema.
    Else, it will be the data-type for specifying the value-type in an SQL insert statement
    """
    if dtype == int:
        return 'INTEGER' if schema_type else 'longValue'
    elif dtype == float:
        return 'FLOAT' if schema_type else 'doubleValue'
    elif dtype == str:
        return 'VARCHAR(256)' if schema_type else 'stringValue'
    elif dtype == bool:
        return 'BOOLEAN' if schema_type else 'booleanValue'
    else:
        raise ValueError(f"Unexpected schema data-type: {dtype}")


def wakeup_serverless(rds_client):
    """
    Wait for Aurora Serverless cluster to wake up with arithmetic backoff of 5 seconds.
    Starts with 1 second, waits for a max of 4 minutes
    """
    delay_secs = 1
    for attempt in range(10):
        try:
            execute_sql(rds_client, 'show tables')
            return
        except ClientError as ce:
            error_code = ce.response.get('Error').get('Code')
            error_msg = ce.response.get('Error').get('Message')
            if error_code == 'BadRequestException' and 'Communications link failure' in error_msg:
                time.sleep(delay_secs)
                delay_secs += 5
            else:
                raise ce
    raise Exception(f"Aurora RDS did not wake up for {delay_secs * 2} seconds")


def execute_sql(rds_client, sql: str, sql_parameters: List[dict] = None) -> dict:
    """
    Given an RDSDataService Client, and SQL string and a list of SQL parameters,
    executes the SQL statement on the Aurora cluster and returns the response
    """
    if sql_parameters is None:
        sql_parameters = []
    return rds_client.execute_statement(
        secretArn=SECRETS_ARN,
        database=soundprintutils.AURORA_DB,
        resourceArn=AURORA_CLUSTER_ARN,
        sql=sql,
        parameters=sql_parameters
    )


def execute_batch_sql(rds_client, sql: str, sql_parameter_sets: List[List[dict]]) -> dict:
    """
    Given an RDSDataService Client, and SQL string and a list of SQL parameter-sets,
    executes a batch SQL statement on the Aurora cluster and returns the response
    """
    if sql_parameter_sets is None:
        sql_parameter_sets = [[]]
    return rds_client.batch_execute_statement(
        secretArn=SECRETS_ARN,
        database=soundprintutils.AURORA_DB,
        resourceArn=AURORA_CLUSTER_ARN,
        sql=sql,
        parameterSets=sql_parameter_sets
    )


def lambda_handler(data_file_name, context):
    """
    Lambda handler for the action of taking the recently generated Spotify-history data and archiving the records
    into Aurora DB. Gets triggered after joining multiple types of metadata is complete and the joined file name
    is provided.
    If the Aurora table does not exist, it creates the table. If there are records to be inserted, the Aurora serverless
    cluster is first woken up with an arithmetic backoff until it is ready to receive SQL requests.
    :param data_file_name: S3-key containing the file-name for the joined dataframe
    :param context:
    """
    # Download historical snapshot file from S3
    df = soundprintutils.download_df_from_s3_csv(data_file_name, JoinerCommon.SCHEMA)
    LOGGER.info(f"Downloaded joined data file from S3: {data_file_name}")
    LOGGER.debug(f"DataFrame dimensions: {df.shape}")

    # Return if there is no data to update table
    if len(df.index) == 0:
        LOGGER.info(f"No records in dataframe downloaded - returning")
        return

    # Get the RDSDataService client and wake up the cluster
    rds_data_client = boto3.client('rds-data', config=Config(retries={'max_attempts': 10, 'mode': 'standard'}))
    LOGGER.debug(f"Created RDS DataService Client")

    wakeup_serverless(rds_data_client)
    LOGGER.info(f"Woken up Aurora Serverless Cluster: {soundprintutils.AURORA_DB}")

    # Create table if not exists
    create_response = create_table_if_not_exists(rds_data_client)
    LOGGER.debug(f"Executed CREATE-TABLE-IF-NOT-EXISTS. Response: {create_response}")
    if create_response['ResponseMetadata']['HTTPStatusCode'] != 200:
        LOGGER.error(f"Table creation failed")
        raise Exception(f"Table creation-if-exists failed: {create_response}")

    # Insert soundprint records into table
    insert_response = insert_data_rows(df, rds_data_client)
    LOGGER.debug(f"Executed data insertion for {df.shape[0]} rows. Response: {insert_response}")
    if insert_response['ResponseMetadata']['HTTPStatusCode'] != 200:
        LOGGER.error(f"Insertion failed: {insert_response}")
        raise Exception(f"Record(s) insertion failed: {insert_response}")

    return 
