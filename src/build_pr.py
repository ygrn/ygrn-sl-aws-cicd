import json


def handler(event, context):
    body = json.loads(event['body'])
    action = body['action']
    print(body)

    if action in ['opened', 'synchronize']:
        print('push to sqs')

    return {"statusCode": 200}