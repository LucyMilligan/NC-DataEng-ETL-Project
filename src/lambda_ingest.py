import boto3
import json
from dotenv import load_dotenv
import logging
from datetime import datetime
from botocore.exceptions import ClientError
from utils.connection import connect_to_rds, close_rds
from utils.ingest_utils import check_database_updated, retrieve_parameter


ssm = boto3.client("ssm", "eu-west-2")

# load env variables
load_dotenv()  # conditional only happens if runs in test environment

# configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# trigered by the state machine every 30min
def lambda_handler_ingest(event, context):
    try:
        updated_data_tables = check_database_updated()
        if updated_data_tables == []:
            logger.info("No new data.")
        else:
            for table in updated_data_tables:
                conn = connect_to_rds()
                cur = conn.cursor()
                previous_time = retrieve_parameter(ssm, "timestamp_prev")
                current_time = retrieve_parameter(ssm, "timestamp_now")
                query = f"""SELECT * FROM {table}
                        WHERE last_updated BETWEEN '{previous_time}'
                        and '{current_time}';"""
                cur.execute(query)
                response_date = cur.fetchall()
                close_rds(conn)
                response_dict = {f"{table}": response_date}
                s3_client = boto3.client("s3")
                body = json.dumps(response_dict)
                key = f"{datetime.now().year}/{datetime.now().month}\
                /ingested-{table}-{current_time}"
                bucket = "lullymore-west-ingested"
                s3_client.put_object(Bucket=bucket, Key=key, Body=body)
            logger.info("All data has been ingested.")
    except ClientError as e:
        logger.error(f"ClientError: {str(e)}")
        raise Exception("Error interacting with AWS services") from e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise Exception("An unexpected error occurred") from e
