import time
import uuid
from typing import List

import boto3


class TodoTable(object):

    def __init__(self, table, dynamodb=None):
        self.tableName = table
        if dynamodb:
            self.dynamodb = dynamodb
        else:
            self.dynamodb = boto3.resource('dynamodb',
                                           endpoint_url='http://localhost:8000'
                                           )

        self.table = self.dynamodb.Table(self.tableName)

    def create_todo_table(self):
        table = self.dynamodb.create_table(
            TableName=self.tableName,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )

        # Wait until the table exists.
        table.meta.client.get_waiter(
            'table_exists').wait(TableName=self.tableName)
        if table.table_status != 'ACTIVE':
            raise AssertionError()

        return table

    def delete_todo_table(self):
        self.table.delete()
        return True

    def get_todo(self, id: str) -> dict:
        result = self.table.get_item(
            Key={
                'id': id
            }
        )
        return result['Item']

    def put_todo(self, text: str, id: str = None) -> dict:
        timestamp = str(time.time())
        item = {
            'id': id if id else str(uuid.uuid1()),
            'text': text,
            'checked': False,
            'createdAt': timestamp,
            'updatedAt': timestamp,
        }
        self.table.put_item(Item=item)
        return item

    def update_todo(self, id: str, text: str, checked: bool) -> dict:
        timestamp = int(time.time() * 1000)
        result = self.table.update_item(
            Key={
                'id': id
            },
            ExpressionAttributeNames={
                '#todo_text': 'text',
            },
            ExpressionAttributeValues={
                ':text': text,
                ':checked': checked,
                ':updatedAt': timestamp,
            },
            UpdateExpression='SET #todo_text = :text, '
                             'checked = :checked, '
                             'updatedAt = :updatedAt',
            ReturnValues='ALL_NEW',
        )
        return result['Attributes']

    def delete_todo(self, id: str) -> bool:
        self.table.delete_item(
            Key={
                'id': id
            }
        )
        return True

    def scan_todo(self) -> List[dict]:
        scan = self.table.scan()
        return scan['Items']
