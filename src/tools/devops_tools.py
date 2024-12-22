from github import Github
import os
from datetime import datetime, timedelta

class DevOpsTools:
    def __init__(self):
        self.github = Github(os.getenv('GHUB_TOKEN'))

    def infrastructure_check(self, repo_name):
        """Check infrastructure configuration and status"""
        try:
            repo = self.github.get_repo(f'ZubeidHendricks/{repo_name}')
            
            results = {
                'config_files': [],
                'dependencies': [],
                'security': {
                    'has_security_scanning': False,
                    'has_dependency_scanning': False,
                    'has_secret_scanning': False
                }
            }

            # Check for infrastructure files
            infra_files = [
                '.github/workflows',
                'docker-compose.yml',
                'Dockerfile',
                'kubernetes/',
                'terraform/',
                'ansible/'
            ]

            for file_path in infra_files:
                try:
                    content = repo.get_contents(file_path)
                    if isinstance(content, list):  # Directory
                        results['config_files'].extend([f.path for f in content])
                    else:  # Single file
                        results['config_files'].append(content.path)
                except:
                    continue

            # Check security workflows
            try:
                workflows = repo.get_contents('.github/workflows')
                for workflow in workflows:
                    content = repo.get_contents(workflow.path).decoded_content.decode()
                    if 'codeql' in content.lower():
                        results['security']['has_security_scanning'] = True
                    if 'dependabot' in content.lower():
                        results['security']['has_dependency_scanning'] = True
                    if 'secret' in content.lower():
                        results['security']['has_secret_scanning'] = True
            except:
                pass

            return results
        except Exception as e:
            return f"Error checking infrastructure: {str(e)}"