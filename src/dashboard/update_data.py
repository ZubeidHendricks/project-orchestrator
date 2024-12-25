#!/usr/bin/env python3
import os
import json
from datetime import datetime
from github import Github

def update_dashboard_data():
    """
    Generate comprehensive dashboard data for project-orchestrator
    """
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # GitHub authentication
    g = Github(os.environ.get('GHUB_TOKEN'))
    
    # Get the specific repository
    repo = g.get_repo('ZubeidHendricks/project-orchestrator')
    
    # Dashboard data structure
    dashboard_data = {
        'timestamp': datetime.now().isoformat(),
        'repository_info': {
            'name': repo.name,
            'description': repo.description,
            'stars': repo.stargazers_count,
            'forks': repo.forks_count
        },
        'issues': {
            'total_open': 0,
            'total_closed': 0,
            'assignments': []
        },
        'workflows': []
    }
    
    # Fetch issues
    open_issues = repo.get_issues(state='open')
    closed_issues = repo.get_issues(state='closed')
    
    dashboard_data['issues']['total_open'] = open_issues.totalCount
    dashboard_data['issues']['total_closed'] = closed_issues.totalCount
    
    # Collect issue details
    for issue in open_issues:
        issue_info = {
            'number': issue.number,
            'title': issue.title,
            'assignee': issue.assignee.login if issue.assignee else 'Unassigned',
            'created_at': issue.created_at.isoformat(),
            'labels': [label.name for label in issue.labels]
        }
        dashboard_data['issues']['assignments'].append(issue_info)
    
    # Fetch workflows
    workflow_files = repo.get_contents('.github/workflows')
    for workflow_file in workflow_files:
        workflow_name = workflow_file.name.replace('.yml', '')
        dashboard_data['workflows'].append(workflow_name)
    
    # Write dashboard data to file
    with open('data/dashboard.json', 'w') as f:
        json.dump(dashboard_data, f, indent=2)
    
    print(f"Dashboard updated: {len(dashboard_data['issues']['assignments'])} active issues")

if __name__ == '__main__':
    update_dashboard_data()