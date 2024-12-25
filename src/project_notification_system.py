#!/usr/bin/env python3
import json
import os
from datetime import datetime

import requests
from github import Github


class ProjectNotificationSystem:
    def __init__(self, tokens):
        self.gh = Github(tokens["github"])
        self.slack_token = tokens["slack"]
        self.repositories = [
            "ZubeidHendricks/project-orchestrator",
            "ZubeidHendricks/ai-dev-orchestrator",
        ]

    def track_repository_events(self):
        """Monitor and log significant events across repositories"""
        events_log = {"timestamp": datetime.now().isoformat(), "events": []}

        for repo_name in self.repositories:
            repo = self.gh.get_repo(repo_name)

            # Fetch recent events
            for event in repo.get_events()[:10]:
                event_details = {
                    "repository": repo_name,
                    "type": event.type,
                    "actor": event.actor.login,
                    "created_at": event.created_at.isoformat(),
                }
                events_log["events"].append(event_details)

        return events_log

    def send_slack_notifications(self, events_log):
        """Send notifications to Slack for critical events"""
        slack_webhook_url = os.environ.get("SLACK_WEBHOOK_URL")

        for event in events_log["events"]:
            # Filter for important events
            if event["type"] in ["IssuesEvent", "PullRequestEvent", "DeploymentEvent"]:
                message = (
                    f"*{event['type']}* in {event['repository']}\n"
                    f"Actor: {event['actor']}\n"
                    f"Timestamp: {event['created_at']}"
                )

                # Send to Slack
                requests.post(slack_webhook_url, json={"text": message})

    def generate_comprehensive_report(self):
        """Create detailed project tracking report"""
        events_log = self.track_repository_events()
        self.send_slack_notifications(events_log)

        # Save report
        os.makedirs("reports", exist_ok=True)
        with open("reports/repository_events.json", "w") as f:
            json.dump(events_log, f, indent=2)

        return events_log


def main():
    tokens = {
        "github": os.environ.get("GHUB_TOKEN"),
        "slack": os.environ.get("SLACK_TOKEN"),
    }

    notification_system = ProjectNotificationSystem(tokens)
    notification_system.generate_comprehensive_report()
    print("Project Notification System Executed")


if __name__ == "__main__":
    main()
