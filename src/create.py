import json
import logging
import os

import boto3

from todoTable import TodoTable

DYNAMODB = boto3.resource('dynamodb')
DYNAMODB_TABLE = os.environ['DYNAMODB_TABLE']
table = TodoTable(DYNAMODB_TABLE, DYNAMODB)


def create(event, context):
    data = json.loads(event['body'])
    if 'text' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the todo item.")

    # write the todo to the database
    item = table.put_todo(data.get('text'))

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response
