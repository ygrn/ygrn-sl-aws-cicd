import json
import boto3
import os


def handler(event, context):
    # POST from github webhook triggered by PR 
    _ = json.loads(event['body'])
    repo = _['pull_request']['head']['repo']['full_name']
    branch = _['pull_request']['head']['ref']
    print(_['action'], repo, branch)

    if branch_name_invalid(branch):
        print("branch name invalid")
        return {"statusCode": "406"}

    try:
        sqs = boto3.client('sqs')
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
        
        else:
            # only build on opening, committing to, or closing PR
            return {"statusCode": "200"}
    

    except Exception as e:
        _ = e.__dict__
        print(e)
        return {"statusCode": _['response']['ResponseMetadata']['HTTPStatusCode']}

# UTILS

def branch_name_invalid(branch):
    if branch.split("/")[0] in ["feature", "bugfix", "release"]:
        return False
    return True


def deploy_type(repo_full_name):
    repo_name = repo_full_name.split("/")[-1]
    return repo_name.split("-")[1]


def feature_archive_url(repo, branch):
    # builds url to feature/* branch archive .zip
    return "https://github.com/%s/archive/%s.zip" % (repo, branch)


def dev_archive_url(repo):
    # builds url to dev branch archive .zip
    return "https://github.com/%s/archive/dev.zip" % repo