import json
import os
from datetime import datetime
from github import Github

class ProjectMonitor:
    def __init__(self):
        self.github = Github(os.getenv('GHUB_TOKEN'))
        self.data_dir = 'data/monitoring'
        os.makedirs(self.data_dir, exist_ok=True)
        self.load_config()

    def load_config(self):
        """Load monitoring configuration"""
        with open('config/monitoring.json', 'r') as f:
            self.config = json.load(f)
        with open('config/project_types.json', 'r') as f:
            self.project_types = json.load(f)['project_types']
            
    def run_monitoring(self):
        """Run all monitoring checks"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'projects': {}
        }
        
        for project_type, config in self.project_types.items():
            for repo_name in config['repositories']:
                results['projects'][repo_name] = self.check_repository(repo_name, project_type)
        
        self.save_results(results)
        return results

    def check_repository(self, repo_name, project_type):
        """Check specific repository metrics"""
        try:
            repo = self.github.get_repo(f'ZubeidHendricks/{repo_name}')
            metrics = {
                'basic_metrics': self.get_basic_metrics(repo),
                'performance_metrics': self.get_performance_metrics(repo, project_type),
                'health_check': self.get_health_metrics(repo, project_type)
            }
            return metrics
        except Exception as e:
            print(f"Error checking repository {repo_name}: {str(e)}")
            return {'error': str(e)}

    def get_basic_metrics(self, repo):
        """Get basic repository metrics"""
        return {
            'open_issues': repo.get_issues(state='open').totalCount,
            'open_prs': repo.get_pulls(state='open').totalCount,
            'stars': repo.stargazers_count,
            'forks': repo.forks_count,
            'last_update': repo.updated_at.isoformat(),
            'last_push': repo.pushed_at.isoformat() if repo.pushed_at else None
        }

    def get_performance_metrics(self, repo, project_type):
        """Get project-type specific performance metrics"""
        metrics = {}
        
        if project_type == 'pos':
            metrics.update(self.check_pos_performance(repo))
        elif project_type == 'ai':
            metrics.update(self.check_ai_performance(repo))
        elif project_type == 'blockchain':
            metrics.update(self.check_blockchain_performance(repo))
            
        return metrics

    def check_pos_performance(self, repo):
        """Check POS system specific metrics"""
        return {
            'payment_integration': self.check_payment_files(repo),
            'database_status': self.check_database_health(repo),
            'security_score': self.calculate_security_score(repo)
        }

    def check_ai_performance(self, repo):
        """Check AI project specific metrics"""
        return {
            'model_status': self.check_model_files(repo),
            'api_health': self.check_api_status(repo),
            'inference_metrics': self.check_inference_performance(repo)
        }

    def check_blockchain_performance(self, repo):
        """Check blockchain project specific metrics"""
        return {
            'smart_contract_status': self.check_smart_contracts(repo),
            'gas_optimization': self.check_gas_usage(repo),
            'security_audit': self.check_security_status(repo)
        }

    def get_health_metrics(self, repo, project_type):
        """Calculate overall health score"""
        try:
            # Check workflow runs
            workflows = repo.get_workflows()
            recent_runs = []
            for workflow in workflows:
                runs = workflow.get_runs()
                if runs.totalCount > 0:
                    recent_runs.extend(list(runs)[:5])  # Get 5 most recent runs

            # Calculate success rate
            if recent_runs:
                success_rate = len([r for r in recent_runs if r.conclusion == 'success']) / len(recent_runs) * 100
            else:
                success_rate = None

            return {
                'workflow_success_rate': success_rate,
                'has_security_scanning': self.check_security_workflows(repo),
                'has_automated_tests': self.check_test_workflows(repo)
            }
        except Exception as e:
            print(f"Error getting health metrics: {str(e)}")
            return {'error': str(e)}

    def check_payment_files(self, repo):
        """Check payment integration files"""
        try:
            contents = repo.get_contents("")
            payment_files = [f for f in contents if 'payment' in f.path.lower()]
            return {'status': 'active' if payment_files else 'missing'}
        except:
            return {'status': 'unknown'}

    def check_database_health(self, repo):
        """Check database configuration and health"""
        try:
            contents = repo.get_contents("")
            db_files = [f for f in contents if any(x in f.path.lower() for x in ['database', 'migration', 'schema'])]
            return {'status': 'configured' if db_files else 'missing'}
        except:
            return {'status': 'unknown'}

    def calculate_security_score(self, repo):
        """Calculate security score based on various factors"""
        score = 0
        try:
            # Check for security workflows
            if self.check_security_workflows(repo):
                score += 30

            # Check for dependency scanning
            if self.check_dependency_scanning(repo):
                score += 20

            # Check for code scanning alerts
            if self.check_code_scanning(repo):
                score += 50

            return {'score': score}
        except:
            return {'score': 0}

    def save_results(self, results):
        """Save monitoring results"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        filename = f"{self.data_dir}/monitoring_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)

        # Clean up old files based on retention policy
        self.cleanup_old_files()

    def cleanup_old_files(self):
        """Remove old monitoring files based on retention policy"""
        retention_days = self.config['retention']['metrics']
        cutoff = datetime.now().timestamp() - (retention_days * 86400)
        
        for filename in os.listdir(self.data_dir):
            filepath = os.path.join(self.data_dir, filename)
            if os.path.getctime(filepath) < cutoff:
                os.remove(filepath)

    def check_security_workflows(self, repo):
        """Check if repository has security workflows"""
        try:
            workflows_dir = repo.get_contents(".github/workflows")
            return any('security' in f.path.lower() for f in workflows_dir)
        except:
            return False

    def check_test_workflows(self, repo):
        """Check if repository has test workflows"""
        try:
            workflows_dir = repo.get_contents(".github/workflows")
            return any('test' in f.path.lower() for f in workflows_dir)
        except:
            return False

    def check_dependency_scanning(self, repo):
        """Check if repository has dependency scanning"""
        try:
            workflows_dir = repo.get_contents(".github/workflows")
            return any('dependabot' in f.path.lower() for f in workflows_dir)
        except:
            return False

    def check_code_scanning(self, repo):
        """Check if repository has code scanning enabled"""
        try:
            workflows_dir = repo.get_contents(".github/workflows")
            return any('codeql' in f.path.lower() for f in workflows_dir)
        except:
            return False

def main():
    monitor = ProjectMonitor()
    results = monitor.run_monitoring()
    print("Monitoring completed successfully")
    return results

if __name__ == '__main__':
    main()
