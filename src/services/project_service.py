from datetime import datetime
from typing import List, Optional

from github import Github

from src.models.project_models import (Developer, Project, ProjectIssue,
                                       ProjectMetrics, ProjectStatus,
                                       ProjectType)


class ProjectService:
    def __init__(self, github_token: str):
        self.github = Github(github_token)

    async def create_project(self, project_data: dict) -> Project:
        """Create a new project with validation"""
        project = Project(**project_data)

        # Additional validation logic here
        self._validate_team_members(project.team_members)

        return project

    async def update_project_metrics(self, project: Project) -> ProjectMetrics:
        """Update project metrics from GitHub"""
        try:
            repo = self.github.get_repo(project.repository_url)

            metrics = ProjectMetrics(
                open_issues=repo.get_issues(state="open").totalCount,
                completed_issues=repo.get_issues(state="closed").totalCount,
                last_deployment=self._get_last_deployment_date(repo),
            )

            # Update project with new metrics
            project.metrics = metrics
            project.updated_at = datetime.now()

            return metrics
        except Exception as e:
            raise ValueError(f"Failed to update metrics: {str(e)}")

    def _validate_team_members(self, team_members: List[str]) -> None:
        """Validate that team members exist"""
        for member in team_members:
            try:
                self.github.get_user(member)
            except Exception:
                raise ValueError(f"Invalid team member: {member}")

    def _get_last_deployment_date(self, repo) -> Optional[datetime]:
        """Get the date of the last deployment"""
        try:
            deployments = repo.get_deployments()
            if deployments.totalCount > 0:
                return deployments[0].created_at
        except:
            pass
        return None
