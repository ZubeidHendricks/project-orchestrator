import json
import os
from datetime import datetime

from github import Github


class AlertManager:
    def __init__(self):
        self.github = Github(os.getenv("GHUB_TOKEN"))
        self.alerts_dir = "alerts"
        self.thresholds = self._load_thresholds()

    def _load_thresholds(self):
        with open("config/thresholds.json", "r") as f:
            return json.load(f)

    def check_all_projects(self):
        with open("config/project_types.json", "r") as f:
            config = json.load(f)

        alerts = []
        for project_type, settings in config["project_types"].items():
            for repo_name in settings["repositories"]:
                alerts.extend(self._check_repository(repo_name, project_type))

        self._save_alerts(alerts)
        self._create_issues_for_alerts(alerts)

    def _check_repository(self, repo_name, project_type):
        repo = self.github.get_repo(f"ZubeidHendricks/{repo_name}")
        alerts = []

        # Check common metrics
        open_issues = repo.get_issues(state="open").totalCount
        if open_issues > self.thresholds["open_issues"]:
            alerts.append(
                {
                    "severity": "high",
                    "title": f"High number of open issues in {repo_name}",
                    "message": f'There are {open_issues} open issues (threshold: {self.thresholds["open_issues"]})',
                    "project_type": project_type,
                }
            )

        # Project-specific checks
        if project_type == "pos":
            alerts.extend(self._check_pos_specific(repo))
        elif project_type == "ai":
            alerts.extend(self._check_ai_specific(repo))
        elif project_type == "blockchain":
            alerts.extend(self._check_blockchain_specific(repo))

        return alerts

    def _check_pos_specific(self, repo):
        alerts = []
        # Add POS-specific checks
        return alerts

    def _check_ai_specific(self, repo):
        alerts = []
        # Add AI-specific checks
        return alerts

    def _check_blockchain_specific(self, repo):
        alerts = []
        # Add blockchain-specific checks
        return alerts

    def _save_alerts(self, alerts):
        os.makedirs(self.alerts_dir, exist_ok=True)
        filename = (
            f"{self.alerts_dir}/alerts_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        )

        with open(filename, "w") as f:
            json.dump(alerts, f, indent=2)

    def _create_issues_for_alerts(self, alerts):
        for alert in alerts:
            if alert["severity"] == "high":
                self._create_github_issue(alert)

    def _create_github_issue(self, alert):
        repo = self.github.get_repo("ZubeidHendricks/project-orchestrator")
        repo.create_issue(
            title=f"[ALERT] {alert['title']}",
            body=f"**Alert Details**\n\n{alert['message']}\n\nProject Type: {alert['project_type']}",
            labels=["alert", alert["severity"], alert["project_type"]],
        )
