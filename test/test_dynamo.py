import unittest

from moto import mock_dynamodb

from utils.aws_dynamodb import AwsDynamodb, ServicesDynamoDb


@mock_dynamodb
class TestDatabaseFunctions(unittest.TestCase):
    table_name = "TestTableDynamoDb"

    def setUp(self):
        """Create the mock database and table"""

        ddb = AwsDynamodb(parti_sql=False).client
        ddb.create_table(
            TableName=self.table_name,
            KeySchema=[{"AttributeName": "TestTableDynamoDbId", "KeyType": "HASH"}],
            AttributeDefinitions=[
                {"AttributeName": "TestTableDynamoDbId", "AttributeType": "S"}
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        self.table = ddb.Table(self.table_name)

    def tearDown(self):
        """Delete mock database and table after test is run"""
        self.table.delete()
        self.dynamodb = None

    def test_insert_one_item_dynamo_db(self):
        result = ServicesDynamoDb.insert_item_to_dynamo_db_table(
            self.table,
            {
                "TestTableDynamoDbId": "9a0",
                "State": "PENDING",
                "Amount": 50,
                "otro": {"a": 1},
            },
        )
        assert result

    def test_scan_table(self):
        ServicesDynamoDb.insert_item_to_dynamo_db_table(
            self.table,
            {
                "TestTableDynamoDbId": "9a0",
                "State": "PENDING",
                "Amount": 50,
                "otro": {"a": 1},
            },
        )
        result = ServicesDynamoDb.scan_table(self.table, "TestTableDynamoDb")
        assert len(result) > 0

    def test_insert_batch_items(self):
        items = [
            {
                "TestTableDynamoDbId": f"id {x}",
                "Amount": x,
            }
            for x in range(999)
        ]

        result = ServicesDynamoDb.send_batch_data_dynamo_db(self.table, items)
        assert len(result.scan()["Items"]) > 500

    def test_get_batch_items_by_keys(self):
        client = AwsDynamodb(parti_sql=False).client
        ServicesDynamoDb.insert_item_to_dynamo_db_table(
            self.table,
            {
                "TestTableDynamoDbId": "id 3",
                "State": "PENDING",
                "Amount": 50,
                "otro": {"a": 1},
            },
        )
        batch_keys = {
            self.table.name: {
                "Keys": [{"TestTableDynamoDbId": f"id {x}"} for x in range(1, 10)]
            }
        }
        result = ServicesDynamoDb.read_batch_items_by_keys(client, batch_keys)
        assert len(result["TestTableDynamoDb"]) == 1
