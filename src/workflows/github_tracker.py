from github import Github


class GitHubTracker:
    def __init__(self, token):
        self.github = Github(token)

    def track_repository(self, repo_name):
# repo
        return {
            "issues": repo.get_issues(state="open").totalCount,
            "prs": repo.get_pulls(state="open").totalCount,
        }
