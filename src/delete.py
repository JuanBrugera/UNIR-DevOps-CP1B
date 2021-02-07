import os
import boto3

from todoTable import TodoTable

DYNAMODB = boto3.resource('dynamodb')
DYNAMODB_TABLE = os.environ['DYNAMODB_TABLE']
table = TodoTable(DYNAMODB_TABLE, DYNAMODB)


def delete(event, context):
    # delete the todo from the database
    table.delete_todo(id=event.get('pathParameters').get('id'))

    # create a response
    response = {
        "statusCode": 200
    }

    return response
