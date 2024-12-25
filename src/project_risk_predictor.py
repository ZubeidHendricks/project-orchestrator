#!/usr/bin/env python3
import json
import os
from datetime import datetime, timedelta

import numpy as np
from github import Github
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split


class ProjectRiskPredictor:
    def __init__(self, token):
        self.gh = Github(token)
        self.project_repo = self.gh.get_repo("ZubeidHendricks/project-orchestrator")

    def extract_project_features(self):
        """Extract comprehensive project risk features"""
        features = []
        risk_labels = []

        for issue in self.project_repo.get_issues(state="closed"):
            feature_vector = [
                len(issue.labels),
                issue.comments,
                len(issue.body or ""),
                (issue.closed_at - issue.created_at).days,
                1 if any("bug" in label.name.lower() for label in issue.labels) else 0,
            ]
            features.append(feature_vector)

            # Risk classification (based on time to close and complexity)
            risk_level = "low"
            days_to_close = (issue.closed_at - issue.created_at).days
            if days_to_close > 30 or len(issue.labels) > 3:
                risk_level = "medium"
            if days_to_close > 60 or len(issue.labels) > 5:
                risk_level = "high"

            risk_labels.append(risk_level)

        return features, risk_labels

    def predict_project_risks(self):
        """Predict risks for ongoing projects"""
        features, labels = self.extract_project_features()

        # Prepare data
        X = np.array(features)
        y = np.array(labels)

        # Split and train risk classification model
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        risk_model = RandomForestClassifier(n_estimators=100)
        risk_model.fit(X_train, y_train)

        # Predict risks for open issues
        open_issues_risks = []
        for issue in self.project_repo.get_issues(state="open"):
            issue_features = [
                len(issue.labels),
                issue.comments,
                len(issue.body or ""),
                (datetime.now() - issue.created_at).days,
                1 if any("bug" in label.name.lower() for label in issue.labels) else 0,
            ]

            predicted_risk = risk_model.predict([issue_features])[0]
            open_issues_risks.append(
                {
                    "issue_number": issue.number,
                    "title": issue.title,
                    "predicted_risk": predicted_risk,
                }
            )

        return open_issues_risks

    def generate_project_health_report(self):
        """Create comprehensive project health report"""
        risk_predictions = self.predict_project_risks()

        health_report = {
            "timestamp": datetime.now().isoformat(),
            "overall_risk_assessment": {
                "high_risk_issues": sum(
                    1 for r in risk_predictions if r["predicted_risk"] == "high"
                ),
                "medium_risk_issues": sum(
                    1 for r in risk_predictions if r["predicted_risk"] == "medium"
                ),
                "low_risk_issues": sum(
                    1 for r in risk_predictions if r["predicted_risk"] == "low"
                ),
            },
            "risk_details": risk_predictions,
        }

        # Save report
        os.makedirs("reports", exist_ok=True)
        with open("reports/project_health_report.json", "w") as f:
            json.dump(health_report, f, indent=2)

        return health_report


def main():
    token = os.environ.get("GHUB_TOKEN")
    risk_predictor = ProjectRiskPredictor(token)
    health_report = risk_predictor.generate_project_health_report()
    print("Project Health Report Generated")


if __name__ == "__main__":
    main()
