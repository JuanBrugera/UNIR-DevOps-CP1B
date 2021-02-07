import json
import os

import boto3

import decimalencoder
from todoTable import TodoTable

DYNAMODB = boto3.resource('dynamodb')
DYNAMODB_TABLE = os.environ['DYNAMODB_TABLE']

# comprehend
COMPREHEND = boto3.client('comprehend')

# translate
TRANSLATOR = boto3.client('translate')

table = TodoTable(DYNAMODB_TABLE, DYNAMODB)


def translate(event, context):
    # fetch todo from the database
    item = table.get_todo(id=event.get('pathParameters').get('id'))
    text = item.get('text')

    target_language = event.get('pathParameters').get('language')
    source_language = COMPREHEND.detect_dominant_language(Text=text)\
        .get('Languages')[0]\
        .get('LanguageCode')

    translation = TRANSLATOR.translate_text(
        Text=text,
        TerminologyNames=[],
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )
    translated_text = translation.get('TranslatedText')
    item.update({'text': translated_text})

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item,
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
