class GithubWebhookUtils():


    @staticmethod
    def feature_archive_url(body):
        # builds url to feature/* branch archive .zip
        repo = body['pull_request']['head']['repo']['full_name']
        branch = body['pull_request']['head']['ref']
        return "https://github.com/%s/archive/%s.zip" % (repo, branch)


    @staticmethod
    def dev_archive_url(body):
        # builds url to dev branch archive .zip
        repo = body['pull_request']['head']['repo']['full_name']
        return "https://github.com/%s/archive/dev.zip" % repo