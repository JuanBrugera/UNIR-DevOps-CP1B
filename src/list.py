import json
import os

import boto3

import decimalencoder
from todoTable import TodoTable

DYNAMODB = boto3.resource('dynamodb')
DYNAMODB_TABLE = os.environ['DYNAMODB_TABLE']
table = TodoTable(DYNAMODB_TABLE, DYNAMODB)


def list(event, context):
    # fetch all todos from the database
    items = table.scan_todo()

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(items, cls=decimalencoder.DecimalEncoder)
    }

    return response
