import json
import os
from datetime import datetime

from github import Github


class DevOpsMonitor:
    def __init__(self):
        self.github = Github(os.getenv("GHUB_TOKEN"))
        self.data_dir = "data/devops"
        os.makedirs(self.data_dir, exist_ok=True)
        self.load_config()

    def load_config(self):
        """Load DevOps configuration and team assignments"""
        with open("config/devops_team.json", "r") as f:
            self.team_config = json.load(f)

    def check_ci_cd_health(self, repo_name):
        """Check CI/CD pipeline health"""
        repo = self.github.get_repo(f"ZubeidHendricks/{repo_name}")
        issues = []

        # Check workflows
        workflows = repo.get_workflows()
        for workflow in workflows:
            recent_runs = list(workflow.get_runs()[:5])  # Last 5 runs
            failures = [run for run in recent_runs if run.conclusion == "failure"]

            if failures:
                issue = {
                    "type": "workflow_failure",
                    "name": workflow.name,
                    "failures": len(failures),
                    "last_failure": failures[0].created_at.isoformat(),
                    "error_logs": self.get_failure_logs(failures[0]),
                }
                self.create_devops_issue(repo, issue)

    def get_failure_logs(self, run):
        """Get failure logs from workflow run"""
        try:
            logs = run.get_logs()
            return logs
        except:
            return "Logs not available"

    def create_devops_issue(self, repo, issue):
        """Create issue and assign to appropriate team member"""
        assignee = self.select_assignee(issue["type"])
        title = f"[DevOps Alert] {issue['name']} Pipeline Failure"
        body = f"""## Pipeline Failure Detected

**Workflow:** {issue['name']}
**Number of Recent Failures:** {issue['failures']}
**Last Failure:** {issue['last_failure']}

### Error Logs
```
{issue['error_logs']}
```

### Action Required
- [ ] Investigate pipeline failure
- [ ] Fix underlying issues
- [ ] Update pipeline if necessary
- [ ] Verify fix with new run

### Notes
- Please update this issue with findings
- Mark any related PRs
- Document any configuration changes
        """

        repo.create_issue(
            title=title,
            body=body,
            assignee=assignee,
            labels=["devops", "pipeline-failure", "high-priority"],
        )

    def select_assignee(self, issue_type):
        """Select appropriate team member based on issue type and workload"""
        team = self.team_config["devops_team"]

        # Find least loaded team member
        assigned_issues = {}
        for member in team:
            user = self.github.get_user(member)
            issues = self.github.search_issues(f"assignee:{member} is:open")
            assigned_issues[member] = issues.totalCount

        # Select team member with least open issues
        return min(assigned_issues.items(), key=lambda x: x[1])[0]