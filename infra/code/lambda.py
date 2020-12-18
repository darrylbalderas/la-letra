import json
import boto3


def handler(event, context):
    print(event)
    print(context)
    return {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'text/html; charset=utf-8',
        },
        "body": '<p>Bonjour au monde!</p>',
    }
