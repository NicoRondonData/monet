import logging
from typing import List

from boto3.dynamodb.types import TypeDeserializer
from django.conf import settings

logger = logging.getLogger(__name__)
import time

import boto3


class AwsDynamodb:
    def __init__(self, parti_sql: bool = True):
        aws_settings = {
            "aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
            "region_name": settings.AWS_REGION_NAME,
            "endpoint_url": settings.DYNAMO_ENDPOINT,
            "aws_session_token": settings.AWS_SESSION_TOKEN,
        }
        self.client = self.connect_aws_dynamodb(parti_sql, aws_settings)
        if self.client:
            logger.debug("dynamodb connect successfully")
        else:
            logger.debug("dynamodb can't connect.")

    def connect_aws_dynamodb(self, parti_sql, aws_settings):
        try:
            if parti_sql:
                aws_dynamodb_client = boto3.client("dynamodb", **aws_settings)
            else:
                aws_dynamodb_client = boto3.resource("dynamodb", **aws_settings)
            return aws_dynamodb_client
        except Exception:
            logger.exception("Error connecting aws dynamodb")
            return None


class ServicesDynamoDb:
    @classmethod
    def parti_sql(cls, fields: list, query: str):  # pragma: no cover
        client = AwsDynamodb().client
        parti_sql_result = client.execute_statement(Statement=query)
        data = parti_sql_result.get("Items")
        deserialized_data = ServicesDynamoDb.deserialize(data, fields)
        data_without_duplicates = [
            dict(t) for t in {tuple(d.items()) for d in deserialized_data}
        ]
        return data_without_duplicates

    @classmethod
    def deserialize(cls, data: list, fields: list):  # pragma: no cover
        type_deserializer = TypeDeserializer()

        if data and fields:
            result = []

            for value in data:
                batch = {k: type_deserializer.deserialize(v) for k, v in data[value]}
                prev_result = {}

                for field in fields:
                    prev_result[field] = cls._decimal_to_int(batch.get(field))

                result.append(prev_result)

        return result

    @classmethod
    def deserialize_dict(cls, data: list, fields: list):  # pragma: no cover
        prev_result = {}

        if data and fields:
            for value in data:
                prev_result[value] = list(data[value].values())[0]

        return prev_result

    @classmethod
    def _decimal_to_int(cls, value):  # pragma: no cover
        result = None

        try:
            if value:
                float_str = float(value)
                result = int(float_str)

        except Exception:
            result = value

        return result

    @classmethod
    def send_batch_data_dynamo_db(cls, table, data: list) -> List:  # pragma: no cover
        """
        Send to dynamo db data in bacth
        :return: List
        """
        try:
            with table.batch_writer() as batch_writer:
                for item in data:
                    batch_writer.put_item(item)
                return table
        except Exception:
            logger.exception(f"Error sending {table} data to dynamo db")
            return []

    @classmethod
    def insert_item_to_dynamo_db_table(cls, table, item: dict) -> bool:
        try:
            input = item
            table.put_item(Item=input)
        except Exception:
            logger.exception(f"Error sending {table.__name__} data item to dynamo db")
            return False
        else:
            return True

    @classmethod
    def scan_table(cls, table, table_name) -> List:
        scan_response = table.scan(TableName=table_name)
        return scan_response["Items"]

    @classmethod
    def read_batch_items_by_keys(cls, client, batch_keys) -> dict:
        result = cls.__do_batch_get(client, batch_keys)
        return result

    @classmethod
    def __do_batch_get(cls, client, batch_keys):
        """
        Gets a batch of items from Amazon DynamoDB. Batches can contain keys from
        more than one table.
        When Amazon DynamoDB cannot process all items in a batch, a set of unprocessed
        keys is returned. This function uses an exponential backoff algorithm to retry
        getting the unprocessed keys until all are retrieved or the specified
        number of tries is reached.
        :param batch_keys: The set of keys to retrieve. A batch can contain at most 100
                           keys. Otherwise, Amazon DynamoDB returns an error.
        :return: The dictionary of retrieved items grouped under their respective
                 table names.
        """
        tries = 0
        max_tries = 5
        sleepy_time = 1  # Start with 1 second of sleep, then exponentially increase.
        retrieved = {key: [] for key in batch_keys}
        while tries < max_tries:
            response = client.batch_get_item(RequestItems=batch_keys)
            # Collect any retrieved items and retry unprocessed keys.
            for key in response.get("Responses", []):
                retrieved[key] += response["Responses"][key]
            unprocessed = response["UnprocessedKeys"]
            if len(unprocessed) > 0:
                batch_keys = unprocessed
                unprocessed_count = sum(
                    [len(batch_key["Keys"]) for batch_key in batch_keys.values()]
                )
                logger.info(
                    "%s unprocessed keys returned. Sleep, then retry.",
                    unprocessed_count,
                )
                tries += 1
                if tries < max_tries:
                    logger.info("Sleeping for %s seconds.", sleepy_time)
                    time.sleep(sleepy_time)
                    sleepy_time = min(sleepy_time * 2, 32)
            else:
                break

        return retrieved
