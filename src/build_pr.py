import json
import boto3
import os


def handler(event, context):
    body = json.loads(event['body'])
    action = body['action']
    print(body)

    if action in ['opened', 'synchronize']:
        sqs = boto3.client('sqs')
        response = sqs.send_message(
            QueueUrl=os.environ['BUILD_SQS_URL'],
            MessageBody=event['body']
        )
        print(response)

    return {"statusCode": 200}
