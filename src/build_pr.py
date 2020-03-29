import json
import boto3
import os


def handler(event, context):
    # POST from github webhook triggered by Pull Request 
    _ = json.loads(event['body'])
    repo = _['pull_request']['head']['repo']['full_name']
    branch = _['pull_request']['head']['ref']
    print(_['action'], repo, branch)

    sqs = boto3.client('sqs')

    try:
        archive_url = None

        if _['action'] in ['opened', 'synchronize']:
            archive_url = feature_archive_url(repo, branch)
        
        if _['action'] == "closed":
            archive_url = dev_archive_url(repo)

        if archive_url:
            r = sqs.send_message(
                QueueUrl=os.environ['BUILD_SQS_URL'],
                MessageBody=json.dumps({
                    "archive_url": archive_url,
                    "deploy_type": deploy_type(repo)
                })
            )

        print(r)
        return {"statusCode": r['ResponseMetadata']['HTTPStatusCode']}

    except Exception as e:
        _ = e.__dict__
        print(e)
        return {"statusCode": _['response']['ResponseMetadata']['HTTPStatusCode']}


def deploy_type(repo_full_name):
    repo_name = repo_full_name.split("/")[-1]
    return repo_name.split("-")[1]


def feature_archive_url(repo, branch):
    # builds url to feature/* branch archive .zip
    return "https://github.com/%s/archive/%s.zip" % (repo, branch)


def dev_archive_url(repo):
    # builds url to dev branch archive .zip
    return "https://github.com/%s/archive/dev.zip" % repo