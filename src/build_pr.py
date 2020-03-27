import json
import boto3


def handler(event, context):
    body = json.loads(event['body'])
    action = body['action']
    print(body)

    if action in ['opened', 'synchronize']:
        sqs = boto3.client('sqs')
        print('push to sqs')

    return {"statusCode": 200}
