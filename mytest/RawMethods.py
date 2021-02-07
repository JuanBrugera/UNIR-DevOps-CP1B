import boto3
import uuid
import sys

sys.path.insert(1, '../src/')

DYNAMODB_TABLE_NAME = 'todoTable'

TODO_TEXT = "Developing test"
TODO_NEW_TEXT = "Developing more test"
TODO_ID = str(uuid.uuid4())


def _get_dynamo():
    return boto3.resource('dynamodb', region_name='us-west-1')


def _get_table():
    import todoTable
    return todoTable.TodoTable(DYNAMODB_TABLE_NAME, _get_dynamo())


def create_table():
    return _get_table().create_todo_table()


def delete_table():
    return _get_table().delete_todo_table()


def create_todo():
    return _get_table().put_todo(TODO_TEXT, TODO_ID)


def get_todo():
    return _get_table().get_todo(TODO_ID)


def list_todo():
    return _get_table().scan_todo()


def update_todo():
    return _get_table().update_todo(TODO_ID, TODO_NEW_TEXT, True)


def delete_todo():
    return _get_table().delete_todo(TODO_ID)
