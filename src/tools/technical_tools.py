import os
from datetime import datetime, timedelta

from github import Github


class TechnicalTools:
    def __init__(self):
        self.github = Github(os.getenv("GHUB_TOKEN"))

    def code_review(self, pull_request_url):
        """Analyze a pull request for code quality and issues"""
        try:
            # Extract PR details from URL
            _, _, repo_full_name, _, pr_number = pull_request_url.split("/")
# repo
# pr

# analysis
                "files_changed": pr.changed_files,
                "additions": pr.additions,
                "deletions": pr.deletions,
                "comments": pr.comments,
                "review_comments": pr.review_comments,
            }

            return analysis
        except Exception as e:
            return f"Error analyzing PR: {str(e)}"

    def architecture_analysis(self, repo_name):
        """Analyze repository architecture and structure"""
        try:
# repo
# contents

# structure

            for content in contents:
                if content.type == "dir":
                    structure["directories"].append(content.path)
                elif content.type == "file":
                    if content.path.endswith((".json", ".yml", ".yaml")):
                        structure["config_files"].append(content.path)
                    elif content.path in [
                        "README.md",
                        "package.json",
                        "requirements.txt",
                    ]:
                        structure["key_files"].append(content.path)

            return structure
        except Exception as e:
            return f"Error analyzing architecture: {str(e)}"

    def technical_assessment(self, repo_name, context):
        """Assess technical aspects of a repository"""
        try:
# repo

            # Get recent commits
            commits = repo.get_commits(since=datetime.now() - timedelta(days=30))

            # Get languages used
# languages

            # Get open issues and PRs
            issues = repo.get_issues(state="open")
            prs = repo.get_pulls(state="open")

# assessment
                "recent_activity": {
                    "commits": commits.totalCount,
                    "active_days": len(set(c.commit.author.date.date() for c in commits)),
                },
                "languages": languages,
                "open_issues": issues.totalCount,
                "open_prs": prs.totalCount,
                "context": context,
            }

            return assessment
        except Exception as e:
            return f"Error in technical assessment: {str(e)}"
