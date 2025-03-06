# import os
# import sys
import boto3
# import json
from dotenv import load_dotenv
import logging
from datetime import datetime
from botocore.exceptions import ClientError


# Set this environment variable before running the script locally
# os.environ['ENV'] = 'local'  # or 'production' for Lambda

# if os.getenv("ENV") == "development":
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from connection import connect_to_rds, close_rds
from ingest_utils import (
    check_database_updated,
    retrieve_parameter,
    format_raw_data_into_json
)
# else:
#     sys.path.append(
#         os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     )
    # from util_func.python.connection import connect_to_rds, close_rds
    # from util_func.python.ingest_utils import (
    #     check_database_updated,
    #     retrieve_parameter,
    # )

ssm=boto3.client("ssm", "eu-west-2")

# load env variables
load_dotenv()  # conditional only happens if runs in test environment

# configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# trigered by the state machine every 30min
def lambda_handler_ingest(event, context):
    try:
        conn = connect_to_rds()
        cur = conn.cursor()
        updated_data_tables = check_database_updated()
        previous_time = retrieve_parameter(ssm, "timestamp_prev")
        print(previous_time, "prev in lambda_handler")
        current_time = retrieve_parameter(ssm, "timestamp_now")
        print(current_time, "current in lambda_handler")
        if updated_data_tables == []:
            logger.info("No new data.")
        else:
            for table in updated_data_tables:
                query = f"""SELECT * FROM {table}
                        WHERE last_updated BETWEEN '{previous_time}'
                        and '{current_time}';"""
                cur.execute(query)
                row_data = cur.fetchall()
                column_names = [desc[0] for desc in cur.description] 
                json_body = format_raw_data_into_json(table, column_names, row_data)
                s3_client = boto3.client("s3")
                key = f"{datetime.now().year}/{datetime.now().month}\
                /ingested-{table}-{current_time}"
                bucket = "etl-lullymore-west-ingested"
                s3_client.put_object(Bucket=bucket, Key=key, Body=json_body)
            logger.info("All data has been ingested.")
    except ClientError as e:
        logger.error(f"ClientError: {str(e)}")
        raise Exception("Error interacting with AWS services") from e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise Exception("An unexpected error occurred") from e
    finally:
        close_rds(conn)