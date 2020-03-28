import json
import boto3
import os


def handler(event, context):
    body = json.loads(event['body'])
    print(body)

    action = body['action']

    try:
        if action in ['opened', 'synchronize']:
            sqs = boto3.client('sqs')
            response = sqs.send_message(
                QueueUrl=os.environ['BUILD_SQS_URL'],
                MessageBody=feature_archive_url(body)
            )
            print(response)

        if action == "closed":
            sqs = boto3.client('sqs')
            response = sqs.send_message(
                QueueUrl=os.environ['BUILD_SQS_URL'],
                MessageBody=dev_archive_url(body)
            )
            print(response)

        return {"statusCode": 200}

    except Exception as e:
        print(e)


def feature_archive_url(body):
    # builds url to feature/* branch archive .zip
    repo = body['pull_request']['head']['repo']['full_name']
    branch = body['pull_request']['head']['ref']
    return "https://github.com/%s/archive/%s.zip" % (repo, branch)

    
def dev_archive_url(body):
    # builds url to dev branch archive .zip
    repo = body['pull_request']['head']['repo']['full_name']
    return "https://github.com/%s/archive/dev.zip" % repo