#!/usr/bin/env python3
import os
import json
import numpy as np
import logging
from datetime import datetime
from github import Github
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AITaskAllocator:
    def __init__(self, token):
        """Initialize the task allocation system with detailed logging"""
        try:
            self.gh = Github(token)
            self.project_repo = self.gh.get_repo('ZubeidHendricks/project-orchestrator')
            self.dev_repo = self.gh.get_repo('ZubeidHendricks/ai-dev-orchestrator')
            
            logger.info("Repositories initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize repositories: {e}")
            raise
    
    def extract_developer_skills(self):
        """Extract detailed developer skills with comprehensive logging"""
        developer_skills = {}
        
        try:
            # Log total issues in dev repository
            total_issues = self.dev_repo.get_issues(state='closed').totalCount
            logger.info(f"Total closed issues in ai-dev-orchestrator: {total_issues}")
            
            # Analyze closed issues to build skill profiles
            for issue in self.dev_repo.get_issues(state='closed'):
                if issue.assignee:
                    dev_name = issue.assignee.login
                    
                    # Initialize developer if not exists
                    if dev_name not in developer_skills:
                        developer_skills[dev_name] = {}
                    
                    # Extract skills from issue labels
                    for label in issue.labels:
                        skill = label.name.lower()
                        developer_skills[dev_name][skill] = \
                            developer_skills[dev_name].get(skill, 0) + 1
            
            # Log discovered developer skills
            logger.info("Discovered Developer Skills:")
            for dev, skills in developer_skills.items():
                logger.info(f"{dev}: {skills}")
            
            return developer_skills
        
        except Exception as e:
            logger.error(f"Error extracting developer skills: {e}")
            return {}
    
    def create_dev_issue(self, recommended_dev, project_issue):
        """Create a mirroring issue in ai-dev-orchestrator"""
        try:
            # Create new issue in ai-dev-orchestrator
            new_issue = self.dev_repo.create_issue(
                title=f"Task: {project_issue.title}",
                body=(
                    f"Assigned from project-orchestrator\n\n"
                    f"Original Issue: {project_issue.html_url}\n\n"
                    f"Description:\n{project_issue.body or 'No description provided'}"
                ),
                assignees=[recommended_dev],
                labels=project_issue.labels
            )
            
            logger.info(f"Created issue #{new_issue.number} in ai-dev-orchestrator for {recommended_dev}")
        except Exception as e:
            logger.error(f"Failed to create issue for {recommended_dev}: {e}")
    
    def allocate_tasks(self):
        """Comprehensive task allocation with detailed logging"""
        # Extract developer skills
        developer_skills = self.extract_developer_skills()
        
        # Log project repository issues
        open_issues_count = self.project_repo.get_issues(state='open').totalCount
        logger.info(f"Total open issues in project-orchestrator: {open_issues_count}")
        
        # Process unassigned issues
        for issue in self.project_repo.get_issues(state='open'):
            if not issue.assignee:
                try:
                    # Recommend developer
                    recommended_dev = self.recommend_developer(issue, developer_skills)
                    
                    # Assign issue in project-orchestrator
                    issue.edit(assignee=recommended_dev)
                    logger.info(f"Assigned Issue #{issue.number} '{issue.title}' to {recommended_dev}")
                    
                    # Create mirroring issue in ai-dev-orchestrator
                    self.create_dev_issue(recommended_dev, issue)
                
                except Exception as e:
                    logger.error(f"Could not process issue #{issue.number}: {e}")
    
    def recommend_developer(self, issue, developer_skills):
        """Recommend the best developer for an issue"""
        issue_skills = [label.name.lower() for label in issue.labels]
        
        developer_scores = {}
        for dev, skills in developer_skills.items():
            score = sum(skills.get(skill, 0) for skill in issue_skills)
            developer_scores[dev] = score
        
        # Fallback to first developer if no match
        if not developer_scores:
            developers = list(developer_skills.keys())
            return developers[0] if developers else None
        
        return max(developer_scores, key=developer_scores.get)

def main():
    token = os.environ.get('GHUB_TOKEN')
    if not token:
        logger.error("GitHub token not found. Set GHUB_TOKEN environment variable.")
        return
    
    try:
        allocator = AITaskAllocator(token)
        allocator.allocate_tasks()
        logger.info("Task allocation process completed successfully")
    except Exception as e:
        logger.error(f"Task allocation failed: {e}")

if __name__ == '__main__':
    main()