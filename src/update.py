import json
import logging
import os

import boto3

import decimalencoder
from todoTable import TodoTable

DYNAMODB = boto3.resource('dynamodb')
DYNAMODB_TABLE = os.environ['DYNAMODB_TABLE']
table = TodoTable(DYNAMODB_TABLE, DYNAMODB)


def update(event, context):
    data = json.loads(event['body'])
    if 'text' not in data or 'checked' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't update the todo item.")

    item = table.update_todo(event.get('pathParameters').get('id'),
                             text=data.get('text'),
                             checked=data.get('checked'))

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item,
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
