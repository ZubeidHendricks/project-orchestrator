#!/usr/bin/env python3
import os
import json
from datetime import datetime
from github import Github
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity

class DeveloperSkillOrchestrator:
    def __init__(self, token):
        """Initialize Developer Skill Management System"""
        self.gh = Github(token)
        self.project_repo = self.gh.get_repo('ZubeidHendricks/project-orchestrator')
        self.dev_repo = self.gh.get_repo('ZubeidHendricks/ai-dev-orchestrator')
    
    def create_developer_profile(self, github_username):
        """Create a comprehensive developer profile"""
        try:
            # Fetch user details
            user = self.gh.get_user(github_username)
            
            # Analyze repositories
            repos = user.get_repos()
            
            # Extract skills from repositories
            skills = self._extract_skills_from_repos(repos)
            
            # Analyze contributions
            contributions = self._analyze_contributions(user)
            
            # Build developer profile
            profile = {
                'username': github_username,
                'name': user.name or github_username,
                'avatar': user.avatar_url,
                'bio': user.bio,
                'skills': skills,
                'contributions': contributions,
                'skill_weights': self._calculate_skill_weights(skills)
            }
            
            # Save profile to AI Dev Orchestrator
            self._save_developer_profile(profile)
            
            return profile
        
        except Exception as e:
            print(f"Error creating profile for {github_username}: {e}")
            return {}
    
    def _extract_skills_from_repos(self, repos):
        """Extract skills from developer's repositories"""
        skills = {}
        language_skills = {}
        tech_skills = {}
        
        # Predefined technology categories
        tech_categories = {
            'frontend': ['react', 'vue', 'angular', 'svelte', 'html', 'css', 'javascript'],
            'backend': ['python', 'node', 'django', 'flask', 'fastapi', 'java', 'spring'],
            'ml': ['tensorflow', 'pytorch', 'scikit', 'keras', 'machine-learning', 'data-science'],
            'devops': ['docker', 'kubernetes', 'aws', 'azure', 'gcp', 'ci-cd', 'jenkins']
        }
        
        for repo in repos:
            # Extract languages and technologies
            languages = repo.get_languages()
            for lang, lines in languages.items():
                language_skills[lang.lower()] = language_skills.get(lang.lower(), 0) + lines
            
            # Match against tech categories
            for category, category_skills in tech_categories.items():
                for skill in category_skills:
                    if skill in repo.name.lower() or skill in (repo.description or '').lower():
                        tech_skills[skill] = tech_skills.get(skill, 0) + 1
        
        # Normalize and weight skills
        total_language_lines = sum(language_skills.values())
        skills = {
            'languages': {k: v/total_language_lines for k, v in language_skills.items()},
            'technologies': tech_skills
        }
        
        return skills
    
    def _analyze_contributions(self, user):
        """Analyze developer's GitHub contributions"""
        contributions = {
            'total_repos': user.public_repos,
            'total_gists': user.public_gists,
            'followers': user.followers,
            'following': user.following
        }
        
        return contributions
    
    def _calculate_skill_weights(self, skills):
        """Calculate weighted skill scores"""
        weighted_skills = {}
        
        # Weight language skills
        for lang, score in skills.get('languages', {}).items():
            weighted_skills[lang] = score * 0.6  # Language proficiency weight
        
        # Weight technology skills
        for tech, count in skills.get('technologies', {}).items():
            weighted_skills[tech] = count * 0.4  # Technology exposure weight
        
        return weighted_skills
    
    def _save_developer_profile(self, profile):
        """Save developer profile to AI Dev Orchestrator repository"""
        try:
            # Create or update developer profile issue
            issue = self.dev_repo.create_issue(
                title=f"Developer Profile: {profile['username']}",
                body=json.dumps(profile, indent=2),
                labels=['developer-profile', 'skill-tracking']
            )
            print(f"Saved profile for {profile['username']}")
        except Exception as e:
            print(f"Error saving profile: {e}")
    
    def match_developer_to_issue(self, issue):
        """Intelligent developer matching for an issue"""
        # Extract issue skills from labels and description
        issue_skills = [label.name.lower() for label in issue.labels]
        
        # Add skills from issue description
        description_skills = self._extract_skills_from_description(issue.body or '')
        issue_skills.extend(description_skills)
        
        # Get all developer profiles
        developer_profiles = self._get_developer_profiles()
        
        # Compute skill matching
        best_match = self._compute_skill_match(issue_skills, developer_profiles)
        
        return best_match
    
    def _extract_skills_from_description(self, description):
        """Extract skills from issue description"""
        # Predefined skill keywords
        skill_keywords = [
            'python', 'javascript', 'react', 'backend', 'frontend', 
            'machine learning', 'data science', 'docker', 'kubernetes'
        ]
        
        skills = [
            skill for skill in skill_keywords 
            if skill.lower() in description.lower()
        ]
        
        return skills
    
    def _get_developer_profiles(self):
        """Retrieve all developer profiles from AI Dev Orchestrator"""
        profiles = []
        for issue in self.dev_repo.get_issues(labels=['developer-profile']):
            try:
                profile = json.loads(issue.body)
                profiles.append(profile)
            except Exception as e:
                print(f"Error parsing profile: {e}")
        
        return profiles
    
    def _compute_skill_match(self, issue_skills, developer_profiles):
        """Compute best developer match using skill similarity"""
        if not developer_profiles:
            return None
        
        # Prepare multi-label encoding
        mlb = MultiLabelBinarizer()
        
        # Prepare issue skills
        issue_skills_encoded = mlb.fit_transform([issue_skills])
        
        # Prepare developer skills
        developer_skill_matrices = []
        developer_usernames = []
        
        for profile in developer_profiles:
            profile_skills = list(profile.get('skill_weights', {}).keys())
            developer_skill_matrices.append(
                mlb.transform([profile_skills])
            )
            developer_usernames.append(profile['username'])
        
        # Compute cosine similarity
        similarities = [
            cosine_similarity(issue_skills_encoded, dev_skills)[0][0]
            for dev_skills in developer_skill_matrices
        ]
        
        # Return developer with highest skill match
        best_match_index = np.argmax(similarities)
        return developer_usernames[best_match_index]

def main():
    token = os.environ.get('GHUB_TOKEN')
    if not token:
        print("GitHub token not found. Set GHUB_TOKEN environment variable.")
        return
    
    orchestrator = DeveloperSkillOrchestrator(token)
    
    # Example: Create developer profiles
    developers = ['username1', 'username2']  # Replace with actual GitHub usernames
    for dev in developers:
        orchestrator.create_developer_profile(dev)

if __name__ == '__main__':
    main()