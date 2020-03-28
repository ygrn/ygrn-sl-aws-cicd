import json
import boto3
import os


def handler(event, context):
    body = json.loads(event['body'])
    print(body)

    action = body['action']
    repo = body['pull_request']['head']['repo']['full_name']
    branch = body['pull_request']['head']['ref']
    print(action, repo, branch)

    try:
        if action in ['opened', 'synchronize']:
            sqs = boto3.client('sqs')
            response = sqs.send_message(
                QueueUrl=os.environ['BUILD_SQS_URL'],
                MessageBody=feature_archive_url(repo, branch)
            )
            print(response)
        
        if action == "closed":
            sqs = boto3.client('sqs')
            response = sqs.send_message(
                QueueUrl=os.environ['BUILD_SQS_URL'],
                MessageBody=dev_archive_url(repo)
            )
            print(response)

        return {"statusCode": 200}

    except Exception as e:
        print("[ERROR]", e)
        return {"statusCode": 500}


def feature_archive_url(repo, branch):
    # builds url to feature/* branch archive .zip
    return "https://github.com/%s/archive/%s.zip" % (repo, branch)


def dev_archive_url(repo):
    # builds url to dev branch archive .zip
    return "https://github.com/%s/archive/dev.zip" % repo