import json
import os
from datetime import datetime

from github import Github


class RepositoryManager:
    def __init__(self):
        self.github = Github(os.getenv("GHUB_TOKEN"))
        self.config_file = "config/tracked_repos.json"
        self.ensure_config_exists()

    def ensure_config_exists(self):
        """Ensure config directory and file exist"""
        os.makedirs("config", exist_ok=True)
        if not os.path.exists(self.config_file):
            with open(self.config_file, "w") as f:
                json.dump(
                    {
                        "repositories": [],
                        "last_updated": datetime.now().isoformat(),
                    },
                    f,
                    indent=2,
                )

    def add_repository(self, repo_url, category=None, priority="medium"):
        """Add a new repository to track"""
        # Extract owner and repo name from URL
        parts = repo_url.split("/")
        owner = parts[-2]
        repo_name = parts[-1].replace(".git", "")

        # Verify repository exists
        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
        except Exception as e:
            raise ValueError(f"Could not access repository: {str(e)}")

        # Load current config
        with open(self.config_file, "r") as f:
            config = json.load(f)

        # Check if already tracked
        if any(r["name"] == repo_name for r in config["repositories"]):
            raise ValueError(f"Repository {repo_name} is already being tracked")

        # Add new repository
        repo_config = {
            "name": repo_name,
            "owner": owner,
            "url": repo_url,
            "category": category,
            "priority": priority,
            "added_date": datetime.now().isoformat(),
            "status": "active",
        }

        config["repositories"].append(repo_config)
        config["last_updated"] = datetime.now().isoformat()

        # Save updated config
        with open(self.config_file, "w") as f:
            json.dump(config, f, indent=2)

        return repo_config
