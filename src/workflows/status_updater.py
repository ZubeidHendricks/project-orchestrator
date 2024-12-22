import os
from datetime import datetime
from github import Github
import json

class StatusUpdater:
    def __init__(self):
        self.github = Github(os.getenv('GITHUB_TOKEN'))
        self.base_path = 'status'

    def update_project_status(self):
        # Get all repositories
        repositories = self.get_active_repositories()
        status_report = {}

        for repo in repositories:
            status = self.analyze_repository(repo)
            status_report[repo.name] = status

        self.save_status_report(status_report)

    def get_active_repositories(self):
        user = self.github.get_user('ZubeidHendricks')
        return user.get_repos()

    def analyze_repository(self, repo):
        return {
            'open_issues': repo.get_issues(state='open').totalCount,
            'open_prs': repo.get_pulls(state='open').totalCount,
            'last_commit': repo.get_commits().totalCount,
            'last_updated': repo.updated_at.isoformat()
        }

    def save_status_report(self, report):
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

        filename = f"{self.base_path}/status_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)

if __name__ == '__main__':
    updater = StatusUpdater()
    updater.update_project_status()