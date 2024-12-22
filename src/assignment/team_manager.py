import json
import os

from github import Github


class TeamManager:
    def __init__(self):
        self.github = Github(os.getenv("GHUB_TOKEN"))
        self.load_team_structure()

    def load_team_structure(self):
        with open("config/team_structure.json", "r") as f:
            self.team_structure = json.load(f)

    def assign_issue(self, issue_data):
        """Assign issue to appropriate team member"""
        project_type = issue_data["project_type"]  # pos, ai, blockchain
        issue_type = issue_data["issue_type"]  # frontend, backend, model, etc.
        severity = issue_data["severity"]  # critical, high, medium, low

        # Get assignment rules for this project type
        rules = self.team_structure["assignment_rules"][project_type]

        # For critical issues, assign to team lead
        if severity == "critical":
            assignee = rules["critical_issues"][0]
        else:
            # Get appropriate assignee based on issue type
            assignee_path = rules.get(issue_type, [])[0]
            assignee = self.get_assignee_from_path(assignee_path)

        return self.get_developer_details(assignee)

    def get_assignee_from_path(self, path):
        """Convert path like 'pos_team.developers[0]' to actual developer"""
        parts = path.split(".")
        current = self.team_structure["teams"]

        for part in parts:
            if "[" in part:
                # Handle array index
                name, index = part.split("[")
                index = int(index.replace("]", ""))
                current = current[name][index]
            else:
                current = current[part]

        return current

    def get_developer_details(self, developer):
        """Get full details for a developer"""
        return {
            "github_username": developer["github"],
            "expertise": developer["expertise"],
            "level": developer["level"],
        }

    def get_team_workload(self, team_name):
        """Get current workload for team members"""
        team = self.team_structure["teams"][team_name]
        workload = {}

        # Get workload for team lead
        lead_issues = self.github.search_issues(f'assignee:{team["lead"]} is:open')
        workload[team["lead"]] = {"open_issues": lead_issues.totalCount, "role": "lead"}

        # Get workload for developers
        for dev in team.get("developers", []):
            dev_issues = self.github.search_issues(f'assignee:{dev["github"]} is:open')
            workload[dev["github"]] = {
                "open_issues": dev_issues.totalCount,
                "expertise": dev["expertise"],
                "role": "developer",
            }

        return workload
