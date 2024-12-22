from github import Github
import os

class SpecializedAnalyzer:
    def __init__(self):
        self.github = Github(os.getenv('GHUB_TOKEN'))

    def analyze_pos_system(self, repo_name):
        """Specialized checks for POS systems"""
        repo = self.github.get_repo(f'ZubeidHendricks/{repo_name}')
        return {
            'payment_integration': self._check_payment_files(repo),
            'security': self._check_security_measures(repo),
            'database': self._check_database_config(repo)
        }

    def analyze_ai_project(self, repo_name):
        """Specialized checks for AI projects"""
        repo = self.github.get_repo(f'ZubeidHendricks/{repo_name}')
        return {
            'model_files': self._check_model_files(repo),
            'api_endpoints': self._check_api_endpoints(repo),
            'performance': self._check_performance_metrics(repo)
        }

    def analyze_blockchain_project(self, repo_name):
        """Specialized checks for blockchain projects"""
        repo = self.github.get_repo(f'ZubeidHendricks/{repo_name}')
        return {
            'smart_contracts': self._check_smart_contracts(repo),
            'gas_usage': self._check_gas_usage(repo),
            'security_audit': self._check_security_audit(repo)
        }

    def _check_payment_files(self, repo):
        """Check payment integration files"""
        try:
            contents = repo.get_contents("")
            payment_files = [f for f in contents if 'payment' in f.path.lower()]
            return len(payment_files) > 0
        except:
            return False

    def _check_security_measures(self, repo):
        """Check security configurations"""
        try:
            security_files = repo.get_contents(".github/workflows/security")
            return len(security_files) > 0
        except:
            return False

    # Add more specialized check methods...