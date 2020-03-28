import json
import boto3
import os


def handler(event, context):
    body = json.loads(event['body'])
    action = body['action']
    repo = body['pull_request']['head']['repo']['full_name']
    branch = body['pull_request']['head']['ref']
    print(action, repo, branch)

    sqs = boto3.client('sqs')

    try:
        if action in ['opened', 'synchronize']:
            archive_url = feature_archive_url(repo, branch)
        
        if action == "closed":
            archive_url = dev_archive_url(repo)

        response = sqs.send_message(
            QueueUrl=os.environ['BUILD_SQS_URL'],
            MessageBody=archive_url
        )

        print(response)
        return {"statusCode": response['ResponseMetadata']['HTTPStatusCode']}

    except Exception as e:
        err = e.__dict__
        print(e)
        return {"statusCode": err['response']['ResponseMetadata']['HTTPStatusCode']}


def feature_archive_url(repo, branch):
    # builds url to feature/* branch archive .zip
    return "https://github.com/%s/archive/%s.zip" % (repo, branch)


def dev_archive_url(repo):
    # builds url to dev branch archive .zip
    return "https://github.com/%s/archive/dev.zip" % repo