#!/usr/bin/env python3
import os
import json
import numpy as np
from datetime import datetime
from github import Github
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

class AIProjectOrchestrator:
    def __init__(self, token):
        self.gh = Github(token)
        self.project_repo = self.gh.get_repo('ZubeidHendricks/project-orchestrator')
        self.dev_repo = self.gh.get_repo('ZubeidHendricks/ai-dev-orchestrator')
    
    def extract_issue_features(self):
        """Extract comprehensive features from issues"""
        issues_data = []
        for issue in self.project_repo.get_issues(state='closed'):
            features = {
                'labels_count': len(issue.labels),
                'comments_count': issue.comments,
                'age_days': (issue.closed_at - issue.created_at).days,
                'complexity_score': len(issue.body or '') / 100 if issue.body else 0,
                'completion_time': (issue.closed_at - issue.created_at).total_seconds() / 3600  # hours
            }
            issues_data.append(features)
        
        return issues_data
    
    def predict_task_completion_time(self):
        """Machine learning model to predict task completion time"""
        issues_data = self.extract_issue_features()
        
        # Convert to numpy array
        X = np.array([list(issue.values())[:-1] for issue in issues_data])
        y = np.array([issue['completion_time'] for issue in issues_data])
        
        # Normalize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2)
        
        # Train Random Forest Regressor
        model = RandomForestRegressor(n_estimators=100)
        model.fit(X_train, y_train)
        
        # Predict for open issues
        open_issues = list(self.project_repo.get_issues(state='open'))
        predictions = []
        
        for issue in open_issues:
            issue_features = [
                len(issue.labels),
                issue.comments,
                (datetime.now() - issue.created_at).days,
                len(issue.body or '') / 100 if issue.body else 0
            ]
            
            # Scale features
            scaled_features = scaler.transform([issue_features])
            predicted_time = model.predict(scaled_features)[0]
            
            predictions.append({
                'issue_number': issue.number,
                'title': issue.title,
                'predicted_completion_hours': predicted_time
            })
        
        return predictions
    
    def cluster_developer_skills(self):
        """Cluster developers based on their skills and performance"""
        dev_features = []
        dev_names = []
        
        # Collect developer performance data
        for dev_issue in self.dev_repo.get_issues(state='closed'):
            if dev_issue.assignee:
                features = [
                    len(dev_issue.labels),
                    dev_issue.comments,
                    (dev_issue.closed_at - dev_issue.created_at).days
                ]
                dev_features.append(features)
                dev_names.append(dev_issue.assignee.login)
        
        # Normalize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(dev_features)
        
        # Cluster developers
        kmeans = KMeans(n_clusters=3, random_state=42)
        dev_clusters = kmeans.fit_predict(X_scaled)
        
        # Create cluster mapping
        cluster_mapping = {}
        for name, cluster in zip(dev_names, dev_clusters):
            cluster_mapping[name] = int(cluster)
        
        return cluster_mapping
    
    def generate_comprehensive_insights(self):
        """Generate advanced project insights"""
        task_predictions = self.predict_task_completion_time()
        dev_clusters = self.cluster_developer_skills()
        
        insights = {
            'timestamp': datetime.now().isoformat(),
            'task_completion_predictions': task_predictions,
            'developer_skill_clusters': dev_clusters,
            'recommended_actions': []
        }
        
        # Generate recommendations
        for prediction in task_predictions:
            if prediction['predicted_completion_hours'] > 80:  # High complexity tasks
                insights['recommended_actions'].append({
                    'issue': prediction['title'],
                    'recommendation': 'Consider breaking down or reassigning'
                })
        
        # Save insights
        os.makedirs('data', exist_ok=True)
        with open('data/ai_project_insights.json', 'w') as f:
            json.dump(insights, f, indent=2)
        
        return insights

def main():
    token = os.environ.get('GHUB_TOKEN')
    orchestrator = AIProjectOrchestrator(token)
    insights = orchestrator.generate_comprehensive_insights()
    print("AI Project Insights Generated Successfully")

if __name__ == '__main__':
    main()