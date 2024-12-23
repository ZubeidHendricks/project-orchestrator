import os
import sys
import logging
from datetime import datetime
from github import Github

def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def setup_logging():
    project_root = get_project_root()
    logs_dir = os.path.join(project_root, "logs")
    
    # Create logs directory if it doesn't exist
    os.makedirs(logs_dir, exist_ok=True)
    
    logger = logging.getLogger('alert_checker')
    logger.setLevel(logging.INFO)
    
    # File handler
    fh = logging.FileHandler(os.path.join(logs_dir, "check_alerts.log"))
    fh.setLevel(logging.INFO)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger

def check_repository_alerts(repo, logger):
    alerts = []
    try:
        open_issues = repo.get_issues(state='open')
        if open_issues.totalCount > 10:
            alerts.append({
                'type': 'high_issues',
                'repo': repo.name,
                'count': open_issues.totalCount
            })
            
        workflows = repo.get_workflows()
        for workflow in workflows:
            runs = workflow.get_runs()
            if runs.totalCount > 0 and runs[0].conclusion == 'failure':
                alerts.append({
                    'type': 'workflow_failure',
                    'repo': repo.name,
                    'workflow': workflow.name
                })
                
    except Exception as e:
        logger.error(f"Error checking repository {repo.name}: {str(e)}")
    
    return alerts

def main():
    logger = setup_logging()
    
    try:
        g = Github(os.getenv('GHUB_TOKEN'))
        user = g.get_user('ZubeidHendricks')
        repos = user.get_repos()
        
        all_alerts = []
        for repo in repos:
            alerts = check_repository_alerts(repo, logger)
            all_alerts.extend(alerts)
            
        if all_alerts:
            logger.info(f"Found {len(all_alerts)} alerts")
            for alert in all_alerts:
                logger.info(f"Alert: {alert}")
        else:
            logger.info("No alerts found")
            
        return 0
            
    except Exception as e:
        logger.error(f"Error in alert checker: {str(e)}")
        return 1

if __name__ == '__main__':
    sys.exit(main())