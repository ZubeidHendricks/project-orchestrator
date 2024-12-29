import os
from datetime import datetime, timedelta

from github import Github


class IssueHandler:
    def __init__(self):
        self.github = Github(os.getenv("GHUB_TOKEN"))
        self.load_team_config()

    def load_team_config(self):
        with open("config/devops_team.json", "r") as f:
            self.team_config = json.load(f)

    def create_issue(self, repo_name, issue_data):
        """Create and assign issue based on type and severity"""
        repo = self.github.get_repo(f"ZubeidHendricks/{repo_name}")

        # Determine assignee
        assignee = self.get_best_assignee(issue_data["type"])

        # Create issue with template
        issue = repo.create_issue(
            title=self.format_title(issue_data),
            body=self.format_body(issue_data),
            assignee=assignee,
            labels=self.get_labels(issue_data),
        )

        return issue

    def get_best_assignee(self, issue_type):
        """Select best assignee based on workload and expertise"""
        team_type = "devops_team" if issue_type in ["pipeline_failures", "deployment_issues"] else "developers"
        team = self.team_config[team_type]

        # Get workload for each team member
        workloads = {}
        for member in team:
            issues = self.github.search_issues(f"assignee:{member} is:open")
            workloads[member] = {
                "total": issues.totalCount,
                "critical": len([i for i in issues if "critical" in i.labels]),
            }

        # Select based on workload limits and expertise
        for member, workload in workloads.items():
            if (
                workload["total"] < self.team_config["workload_limits"]["max_open_issues"]
                and workload["critical"] < self.team_config["workload_limits"]["max_critical_issues"]
            ):
                return member

        # If all members are at capacity, select least loaded
        return min(workloads.items(), key=lambda x: x[1]["total"])[0]

    def format_title(self, issue_data):
        return f"[{issue_data['type'].upper()}] {issue_data['summary']}"

    def format_body(self, issue_data):
        template = f"""## Issue Details

**Type:** {issue_data['type']}
**Severity:** {issue_data.get('severity', 'medium')}
**Detected:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### Description
{issue_data['description']}

### Technical Details
```
{issue_data.get('technical_details', 'No technical details provided')}
```

### Action Items
{self.format_action_items(issue_data)}

### Resolution Steps
1. Investigate root cause
2. Implement fix
3. Test solution
4. Update documentation
5. Mark as resolved

### Notes
- Update this issue with progress
- Link related PRs
- Document any configuration changes
"""
        return template

    def format_action_items(self, issue_data):
        action_items = issue_data.get("action_items", [])
        if not action_items:
            if issue_data["type"] == "pipeline_failures":
                action_items = [
                    "Check pipeline logs",
                    "Verify build steps",
                    "Test locally",
                    "Update pipeline if needed",
                ]
            elif issue_data["type"] == "deployment_issues":
                action_items = [
                    "Check deployment logs",
                    "Verify environment configuration",
                    "Test deployment locally",
                    "Update deployment scripts if needed",
                ]

        return "\n".join(f"- [ ] {item}" for item in action_items)

    def get_labels(self, issue_data):
        """Get appropriate labels based on issue type and severity"""
        labels = ["automated", issue_data["type"]]

        if "severity" in issue_data:
            labels.append(f"priority-{issue_data['severity']}")

        if issue_data["type"] in ["pipeline_failures", "deployment_issues"]:
            labels.append("devops")

        return labels
