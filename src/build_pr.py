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
            MessageBody=gh_feature_archive(body)
        )
        print(response)
    
    if action == "closed":
        sqs = boto3.client('sqs')
        response = sqs.send_message(
            QueueUrl=os.environ['BUILD_SQS_URL'],
            MessageBody=gh_dev_archive(body)
        )
        print(response)

    return {"statusCode": 200}


def gh_feature_archive(body):
    # builds url to feature/* branch archive .zip
    repo = body['pull_request']['head']['repo']['full_name']
    branch = body['pull_request']['head']['ref']
    return "https://github.com/%s/archive/%s.zip" % (repo, branch)


def gh_dev_archive(body):
    # builds url to dev branch archive .zip
    repo = body['pull_request']['head']['repo']['full_name']
    return "https://github.com/%s/archive/dev.zip" % repo