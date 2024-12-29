import os
from datetime import datetime

from github import Github


class DevOrchestratorIntegration:
    def __init__(self):
        self.github = Github(os.getenv("GHUB_TOKEN"))
        self.project_repo = self.github.get_repo("ZubeidHendricks/project-orchestrator")
        self.dev_repo = self.github.get_repo("ZubeidHendricks/ai-dev-orchestrator")

    def assign_to_dev_orchestrator(self, issue):
        """Assign a project issue to the dev orchestrator"""
        try:
            # Add development label to original issue
            issue.add_to_labels("needs-development")

            # Create corresponding issue in dev orchestrator
            dev_issue = self.dev_repo.create_issue(
                title=f"[Dev Task] {issue.title}",
                body=self._format_dev_task_body(issue),
                labels=["ai-development", self._determine_task_type(issue)],
            )

            # Add cross-reference comment
            issue.create_comment(f"Assigned to Dev Orchestrator: {dev_issue.html_url}")

            # Log the assignment
            self._log_assignment(issue, dev_issue)

            return dev_issue

        except Exception as e:
            print(f"Error assigning to dev orchestrator: {str(e)}")
            return None

    def check_dev_progress(self):
        """Check progress of assigned development tasks"""
        try:
            issues = self.project_repo.get_issues(labels=["needs-development"])
            for issue in issues:
                self._check_issue_progress(issue)
        except Exception as e:
            print(f"Error checking dev progress: {str(e)}")

    def _format_dev_task_body(self, issue):
        return f"""## Original Issue
{issue.html_url}

## Requirements
{issue.body}

## Task Details
Priority: {self._determine_priority(issue)}
Type: {self._determine_task_type(issue)}
Assigned: {datetime.now().isoformat()}

## Additional Context
- Project: {self.project_repo.name}
- Original Issue Number: {issue.number}
- Labels: {', '.join([l.name for l in issue.labels])}
"""

    def _determine_priority(self, issue):
        for label in issue.labels:
            if "priority" in label.name.lower():
                return label.name
        return "normal"

    def _determine_task_type(self, issue):
        type_mapping = {
            "frontend": ["ui", "frontend", "react", "vue"],
            "backend": ["api", "backend", "server"],
            "database": ["db", "database", "model"],
            "devops": ["deployment", "pipeline", "ci-cd"],
        }

        issue_text = f"{issue.title.lower()} {issue.body.lower()}"
        for type_name, keywords in type_mapping.items():
            if any(keyword in issue_text for keyword in keywords):
                return type_name

        return "feature"

    def _check_issue_progress(self, issue):
        """Check progress of a specific issue"""
        try:
            # Find corresponding dev issue
            dev_issues = self.dev_repo.get_issues(state="all", labels=["ai-development"])

            for dev_issue in dev_issues:
                if f"#{issue.number}" in dev_issue.body:
                    self._update_progress(issue, dev_issue)
                    break

        except Exception as e:
            print(f"Error checking issue {issue.number}: {str(e)}")

    def _update_progress(self, project_issue, dev_issue):
        """Update progress based on dev issue status"""
        if dev_issue.state == "closed":
            # Check if PR was created and merged
            linked_prs = [pr for pr in self.dev_repo.get_pulls(state="all") if f"#{dev_issue.number}" in pr.body]

            if linked_prs and linked_prs[0].merged:
                project_issue.add_to_labels("development-completed")
                project_issue.remove_from_labels("needs-development")
                project_issue.create_comment(f"Development completed! PR: {linked_prs[0].html_url}")

    def _log_assignment(self, project_issue, dev_issue):
        """Log the assignment for tracking"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "project_issue": {
                "number": project_issue.number,
                "title": project_issue.title,
                "url": project_issue.html_url,
            },
            "dev_issue": {
                "number": dev_issue.number,
                "title": dev_issue.title,
                "url": dev_issue.html_url,
            },
        }

        # Ensure logs directory exists
        os.makedirs("logs", exist_ok=True)

        # Append to log file
        with open("logs/assignments.log", "a") as f:
            f.write(f"{str(log_entry)}\n")
