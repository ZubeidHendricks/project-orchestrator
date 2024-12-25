import os
import slack
from github import Github

class CollaborationIntegrator:
    def __init__(self, github_token, slack_token):
        self.gh = Github(github_token)
        self.slack_client = slack.WebClient(token=slack_token)
        self.project_repo = self.gh.get_repo('ZubeidHendricks/project-orchestrator')
    
    def sync_issue_updates(self):
        """Sync GitHub issues to Slack"""
        for issue in self.project_repo.get_issues(state='open'):
            # Send Slack notification for new/updated issues
            message = f"New Issue: {issue.title}\n{issue.html_url}"
            self.slack_client.chat_postMessage(
                channel='#project-updates',
                text=message
            )
    
    def create_collaboration_thread(self, issue):
        """Create a Slack thread for issue collaboration"""
        thread_ts = self.slack_client.chat_postMessage(
            channel='#project-discussions',
            text=f"Collaborative Discussion: {issue.title}"
        )['ts']
        
        return thread_ts

def main():
    github_token = os.environ.get('GHUB_TOKEN')
    slack_token = os.environ.get('SLACK_TOKEN')
    
    integrator = CollaborationIntegrator(github_token, slack_token)
    integrator.sync_issue_updates()

if __name__ == '__main__':
    main()