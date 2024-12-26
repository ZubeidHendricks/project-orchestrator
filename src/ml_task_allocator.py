#!/usr/bin/env python3
import json
import os
from datetime import datetime

import numpy as np
from github import Github
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler


class AITaskAllocator:
    def __init__(self, token):
        """Initialize the task allocation system"""
        self.gh = Github(token)
        self.project_repo = self.gh.get_repo("ZubeidHendricks/project-orchestrator")
        self.dev_repo = self.gh.get_repo("ZubeidHendricks/ai-dev-orchestrator")

    def extract_developer_skills(self):
        """Extract developer skills from ai-dev-orchestrator issues"""
        developer_skills = {}

        for issue in self.dev_repo.get_issues(state="closed"):
            if issue.assignee:
                dev_name = issue.assignee.login

                if dev_name not in developer_skills:
                    developer_skills[dev_name] = {}

                for label in issue.labels:
                    skill = label.name.lower()
                    developer_skills[dev_name][skill] = (
                        developer_skills[dev_name].get(skill, 0) + 1
                    )

        return developer_skills

    def featurize_issue(self, issue):
        """Convert an issue into a numerical feature vector"""
        features = [
            len(issue.labels),
            issue.comments,
            len(issue.body or ""),
            (datetime.now() - issue.created_at).days,
            1 if any("bug" in label.name.lower() for label in issue.labels) else 0,
            1 if any("feature" in label.name.lower() for label in issue.labels) else 0,
        ]

        return features

    def recommend_developer(self, issue, developer_skills):
        """Recommend the best developer for an issue"""
        issue_skills = [label.name.lower() for label in issue.labels]

        developer_scores = {}
        for dev, skills in developer_skills.items():
            score = sum(skills.get(skill, 0) for skill in issue_skills)
            developer_scores[dev] = score

        if not developer_scores or max(developer_scores.values()) == 0:
            return self.ml_developer_allocation(issue, developer_skills)

        return max(developer_scores, key=developer_scores.get)

    def ml_developer_allocation(self, issue, developer_skills):
        """Machine learning-based developer allocation"""
        X_train, y_train = self.prepare_training_data(developer_skills)

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)

        classifier = RandomForestClassifier(n_estimators=100)
        classifier.fit(X_train_scaled, y_train)

        issue_features = self.featurize_issue(issue)
        issue_features_scaled = scaler.transform([issue_features])

        prediction = classifier.predict(issue_features_scaled)[0]
        return prediction

    def prepare_training_data(self, developer_skills):
        """Prepare training data for ML allocation"""
        X_train, y_train = [], []

        for dev_repo_issue in self.dev_repo.get_issues(state="closed"):
            if dev_repo_issue.assignee:
                features = self.featurize_issue(dev_repo_issue)
                X_train.append(features)
                y_train.append(dev_repo_issue.assignee.login)

        return X_train, y_train

    def allocate_tasks(self):
        """Main method to allocate tasks across repositories"""
        developer_skills = self.extract_developer_skills()

        for issue in self.project_repo.get_issues(state="open"):
            if not issue.assignee:
                recommended_dev = self.recommend_developer(issue, developer_skills)

                try:
                    issue.edit(assignee=recommended_dev)
                    print(
                        f"Assigned Issue #{issue.number} '{issue.title}' to {recommended_dev}"
                    )
                except Exception as e:
                    print(f"Could not assign issue: {e}")


def main():
    token = os.environ.get("GHUB_TOKEN")
    if not token:
        print("GitHub token not found. Set GHUB_TOKEN environment variable.")
        return

    allocator = AITaskAllocator(token)
    allocator.allocate_tasks()


if __name__ == "__main__":
    main()
