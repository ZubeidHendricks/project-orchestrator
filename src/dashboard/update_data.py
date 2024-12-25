#!/usr/bin/env python3
import json
import os
from datetime import datetime

from github import Github


def update_dashboard_data():
    """Generate comprehensive dashboard data and assign tasks"""
    # GitHub authentication
    g = Github(os.environ.get("GHUB_TOKEN"))

    # Repositories
    project_repo = g.get_repo("ZubeidHendricks/project-orchestrator")
    dev_repo = g.get_repo("ZubeidHendricks/ai-dev-orchestrator")

    # Dashboard data structure
    dashboard_data = {
        "timestamp": datetime.now().isoformat(),
        "project_tasks": [],
        "dev_assignments": [],
    }

    # Fetch open issues from project orchestrator
    open_issues = project_repo.get_issues(state="open")

    # Identify and assign unassigned tasks to developers
    for issue in open_issues:
        if not issue.assignee:
            # Find available developer
            dev_issues = dev_repo.get_issues(state="open")
            available_devs = [
                dev_issue.assignee for dev_issue in dev_issues if dev_issue.assignee
            ]

            if available_devs:
                # Assign to least busy developer
                dev_counts = {}
                for dev in available_devs:
                    dev_counts[dev.login] = sum(
                        1
                        for i in dev_issues
                        if i.assignee and i.assignee.login == dev.login
                    )

                least_busy_dev = min(dev_counts, key=dev_counts.get)

                # Assign issue
                issue.edit(assignee=least_busy_dev)

                dashboard_data["project_tasks"].append(
                    {
                        "issue_number": issue.number,
                        "title": issue.title,
                        "assigned_to": least_busy_dev,
                    }
                )

    # Write dashboard data
    os.makedirs("data", exist_ok=True)
    with open("data/task_assignments.json", "w") as f:
        json.dump(dashboard_data, f, indent=2)

    print(f"Assigned {len(dashboard_data['project_tasks'])} tasks")


if __name__ == "__main__":
    update_dashboard_data()
