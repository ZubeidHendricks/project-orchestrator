#!/usr/bin/env python3
import json
import os

import numpy as np
from github import Github
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler


class AITaskAllocator:
    def __init__(self, token):
        self.gh = Github(token)
        self.project_repo = self.gh.get_repo("ZubeidHendricks/project-orchestrator")
        self.dev_repo = self.gh.get_repo("ZubeidHendricks/ai-dev-orchestrator")

    def extract_task_features(self):
        """Extract features from historical tasks"""
        features = []
        labels = []

        for issue in self.project_repo.get_issues(state="closed"):
            feature_vector = [
                len(issue.labels),
                issue.comments,
                len(issue.body or ""),
                (issue.closed_at - issue.created_at).days,
            ]
            features.append(feature_vector)
            labels.append(issue.assignee.login if issue.assignee else "unassigned")

        return features, labels

    def train_allocation_model(self):
        """Train ML model for task allocation"""
        features, labels = self.extract_task_features()

        # Prepare data
        X = StandardScaler().fit_transform(features)

        # Train model
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X, labels)

        return model

    def recommend_developer(self, issue):
        """Recommend best developer for a task"""
        model = self.train_allocation_model()

        # Extract issue features
        feature_vector = [
            len(issue.labels),
            issue.comments,
            len(issue.body or ""),
            0,  # placeholder for age
        ]

        # Predict developer
        X = StandardScaler().fit_transform([feature_vector])
        recommended_dev = model.predict(X)[0]

        return recommended_dev


def main():
    token = os.environ.get("GHUB_TOKEN")
    allocator = AITaskAllocator(token)

    # Process unassigned issues
    for issue in allocator.project_repo.get_issues(state="open"):
        if not issue.assignee:
            recommended_dev = allocator.recommend_developer(issue)
            issue.edit(assignee=recommended_dev)
            print(f"Assigned {issue.title} to {recommended_dev}")


if __name__ == "__main__":
    main()
