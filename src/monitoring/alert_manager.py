import json
import os
from datetime import datetime

from github import Github


class AlertManager:
    def __init__(self):
        self.github = Github(os.getenv("GITHUB_TOKEN"))
        self.thresholds = {
            "open_issues": 10,
            "open_prs": 5,
            "stale_branches": 30,  # days
        }

    def check_alerts(self):
        alerts = []
        repositories = self.get_repositories()

        for repo in repositories:
            repo_alerts = self.check_repository(repo)
            if repo_alerts:
                alerts.extend(repo_alerts)

        self.process_alerts(alerts)

    def check_repository(self, repo):
        alerts = []

        # Check open issues
        open_issues = repo.get_issues(state="open").totalCount
        if open_issues > self.thresholds["open_issues"]:
            alerts.append(
                {"type": "high_issues", "repo": repo.name, "count": open_issues}
            )

        # Check open PRs
        open_prs = repo.get_pulls(state="open").totalCount
        if open_prs > self.thresholds["open_prs"]:
            alerts.append({"type": "high_prs", "repo": repo.name, "count": open_prs})

        return alerts

    def process_alerts(self, alerts):
        if not alerts:
            return

        # Save alerts
        self.save_alerts(alerts)

        # Create issues for new alerts
        self.create_alert_issues(alerts)

    def save_alerts(self, alerts):
        alerts_path = "monitoring/alerts"
        if not os.path.exists(alerts_path):
            os.makedirs(alerts_path)

        filename = f"{alerts_path}/alerts_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(filename, "w") as f:
            json.dump(alerts, f, indent=2)

    def create_alert_issues(self, alerts):
        for alert in alerts:
            title = f"Alert: {alert['type']} in {alert['repo']}"
            body = f"Alert triggered for {alert['repo']}:\n\n"
            body += f"Type: {alert['type']}\n"
            body += f"Count: {alert['count']}"

            # Create issue in the project-orchestrator repo
            orchestrator_repo = self.github.get_repo(
                "ZubeidHendricks/project-orchestrator"
            )
            orchestrator_repo.create_issue(title=title, body=body, labels=["alert"])


if __name__ == "__main__":
    manager = AlertManager()
    manager.check_alerts()
