import json
import os

import boto3

import decimalencoder
from todoTable import TodoTable

DYNAMODB = boto3.resource('dynamodb')
DYNAMODB_TABLE = os.environ['DYNAMODB_TABLE']
table = TodoTable(DYNAMODB_TABLE, DYNAMODB)


def get(event, context):
    # fetch from the database
    item = table.get_todo(id=event.get('pathParameters').get('id'))

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item,
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
