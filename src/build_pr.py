import json
import boto3
import os
from gh_webhook_utils import GithubWebhookUtils as ghw

def handler(event, context):
    body = json.loads(event['body'])
    print(body)

    action = body['action']

    try:
        if action in ['opened', 'synchronize']:
            sqs = boto3.client('sqs')
            response = sqs.send_message(
                QueueUrl=os.environ['BUILD_SQS_URL'],
                MessageBody=ghw.feature_archive_url(body)
            )
            print(response)

        if action == "closed":
            sqs = boto3.client('sqs')
            response = sqs.send_message(
                QueueUrl=os.environ['BUILD_SQS_URL'],
                MessageBody=ghw.dev_archive_url(body)
            )
            print(response)

        return {"statusCode": 200}

    except Exception as e:
        print(e)