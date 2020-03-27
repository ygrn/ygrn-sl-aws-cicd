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
            MessageBody=src_zip_url(body)
        )
        print(response)

    return {"statusCode": 200}


def src_zip_url(body):
    repo = body['pull_request']['head']['repo']['full_name']
    branch = body['pull_request']['head']['ref']
    return "https://github.com/%s/archive/%s.zip" % (repo, branch)
    