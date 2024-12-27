#!/usr/bin/env python3
import json
import logging
import os
import re
from datetime import datetime

from github import Github

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MasterProjectOrchestrator:
    def __init__(self, token):
        """Initialize comprehensive project management system"""
        self.gh = Github(token)

        # Define project groups with repositories
        self.project_groups = {
            "POS_SYSTEMS": [
                "ultimate-pos-system",
                "ultimate-pos",
                "modern-pos-system",
                "blazor-pos-system",
            ],
            "LANGUAGE_LEARNING": [
                "lingualearn-system-v2",
                "lingualearn-system",
                "lingualearn-platform",
                "lingualearn-wiki",
                "lingualearn-docs",
                "LinguaLearn-Documentation",
            ],
            "COLLABORATION_PLATFORMS": ["shop-together-real", "heyZub-Live", "heyZub"],
            "WRITING_TOOLS": ["wordweaver", "wordweaver-clone"],
        }

        # Initialize repositories
        self.repositories = {}
        for group, repos in self.project_groups.items():
            for repo_name in repos:
                full_repo_name = f"ZubeidHendricks/{repo_name}"
                try:
                    self.repositories[repo_name] = self.gh.get_repo(full_repo_name)
                except Exception as e:
                    logger.error(
                        f"Could not initialize repository {full_repo_name}: {e}"
                    )

    def identify_ai_development_candidates(self):
        """Identify issues suitable for AI development"""
        ai_dev_candidates = []

        for repo_name, repo in self.repositories.items():
            try:
                open_issues = repo.get_issues(state="open")

                for issue in open_issues:
                    # Determine if issue is suitable for AI development
                    if self._is_ai_development_candidate(issue):
                        # Add AI development label
                        issue.add_to_labels("ai-development")
                        ai_dev_candidates.append(issue)

            except Exception as e:
                logger.error(f"Error processing issues in {repo_name}: {e}")

        return ai_dev_candidates

    def _is_ai_development_candidate(self, issue):
        """Determine if an issue is suitable for AI development"""
        # Check issue title and body for development-related keywords
        development_keywords = [
            "implement",
            "create",
            "develop",
            "build",
            "design",
            "feature",
            "module",
            "function",
            "service",
            "component",
        ]

        # Combine title and body for keyword matching
        issue_text = f"{issue.title} {issue.body or ''}".lower()

        # Check for development keywords
        keyword_match = any(keyword in issue_text for keyword in development_keywords)

        # Exclude issues that are already labeled or seem too vague
        exclusion_labels = ["bug", "documentation", "question"]
        has_excluded_label = any(
            label.name.lower() in exclusion_labels for label in issue.labels
        )

        # Minimum text length to ensure substantive issue
        min_text_length = 50

        return (
            keyword_match
            and not has_excluded_label
            and len(issue_text) >= min_text_length
        )

    def create_new_project(self, project_name, repositories, objectives):
        """Programmatically create a new project group with repositories and issues"""
        # Add the new project group to existing groups
        project_group_key = project_name.upper().replace(" ", "_")
        self.project_groups[project_group_key] = repositories

        # Create repositories and issues
        for repo_name in repositories:
            try:
                # Create repository
                repo = self.gh.get_user().create_repo(
                    name=repo_name,
                    description=f"{project_name} - Project Repository",
                    private=True,  # Optional: set to False for public repos
                )

                # Create issues for each objective
                for objective in objectives:
                    issue = repo.create_issue(
                        title=f"Project Objective: {objective}",
                        body=f"Strategic task for {project_name} development.\n\n"
                        "Detailed Requirements:\n"
                        "- Break down into specific implementation steps\n"
                        "- Define clear acceptance criteria\n"
                        "- Align with overall project vision",
                        labels=[
                            "strategic-objective",
                            "project-setup",
                            "ai-development",
                        ],
                    )

                    logger.info(f"Created issue in {repo_name}: {issue.title}")

                # Update repositories dictionary
                self.repositories[repo_name] = repo

            except Exception as e:
                logger.error(f"Failed to create repository {repo_name}: {e}")

        return self.project_groups[project_group_key]

    def generate_project_roadmap(self):
        """Create a comprehensive roadmap for all project groups"""
        # Previous implementation...


def main():
    token = os.environ.get("GHUB_TOKEN")
    if not token:
        logger.error("GitHub token not found. Set GHUB_TOKEN environment variable.")
        return

    try:
        orchestrator = MasterProjectOrchestrator(token)

        # Identify AI development candidates
        ai_dev_candidates = orchestrator.identify_ai_development_candidates()

        logger.info(f"Identified {len(ai_dev_candidates)} AI development candidates")

    except Exception as e:
        logger.error(f"Project orchestration failed: {e}")


if __name__ == "__main__":
    main()
