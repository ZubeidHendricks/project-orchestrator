from github import Github
import json
import os
from datetime import datetime

class RepositoryManager:
    def __init__(self):
        self.github = Github(os.getenv('GITHUB_TOKEN'))
        self.config_file = 'config/tracked_repos.json'
        self.ensure_config_exists()

    def ensure_config_exists(self):
        """Ensure config directory and file exist"""
        os.makedirs('config', exist_ok=True)
        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w') as f:
                json.dump({
                    'repositories': [],
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)

    def add_repository(self, repo_url, category=None, priority='medium'):
        """Add a new repository to track"""
        # Extract owner and repo name from URL
        parts = repo_url.split('/')
        owner = parts[-2]
        repo_name = parts[-1].replace('.git', '')

        # Verify repository exists
        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
        except Exception as e:
            raise ValueError(f"Could not access repository: {str(e)}")

        # Load current config
        with open(self.config_file, 'r') as f:
            config = json.load(f)

        # Check if already tracked
        if any(r['name'] == repo_name for r in config['repositories']):
            raise ValueError(f"Repository {repo_name} is already being tracked")

        # Add new repository
        repo_config = {
            'name': repo_name,
            'owner': owner,
            'url': repo_url,
            'category': category,
            'priority': priority,
            'added_date': datetime.now().isoformat(),
            'status': 'active'
        }

        config['repositories'].append(repo_config)
        config['last_updated'] = datetime.now().isoformat()

        # Save updated config
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)

        return repo_config

    def remove_repository(self, repo_name):
        """Remove a repository from tracking"""
        with open(self.config_file, 'r') as f:
            config = json.load(f)

        config['repositories'] = [r for r in config['repositories'] if r['name'] != repo_name]
        config['last_updated'] = datetime.now().isoformat()

        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)

    def update_repository(self, repo_name, updates):
        """Update repository configuration"""
        with open(self.config_file, 'r') as f:
            config = json.load(f)

        for repo in config['repositories']:
            if repo['name'] == repo_name:
                repo.update(updates)
                break

        config['last_updated'] = datetime.now().isoformat()

        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)

    def list_repositories(self, category=None, status=None):
        """List tracked repositories with optional filtering"""
        with open(self.config_file, 'r') as f:
            config = json.load(f)

        repos = config['repositories']

        if category:
            repos = [r for r in repos if r.get('category') == category]
        if status:
            repos = [r for r in repos if r.get('status') == status]

        return repos

    def get_repository_details(self, repo_name):
        """Get detailed information about a tracked repository"""
        with open(self.config_file, 'r') as f:
            config = json.load(f)

        for repo in config['repositories']:
            if repo['name'] == repo_name:
                # Get live GitHub data
                gh_repo = self.github.get_repo(f"{repo['owner']}/{repo['name']}")
                repo['github_data'] = {
                    'open_issues': gh_repo.open_issues_count,
                    'stars': gh_repo.stargazers_count,
                    'forks': gh_repo.forks_count,
                    'last_updated': gh_repo.updated_at.isoformat()
                }
                return repo

        raise ValueError(f"Repository {repo_name} not found")