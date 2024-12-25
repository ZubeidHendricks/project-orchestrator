#!/usr/bin/env python3
import json
import os
import random
from datetime import datetime, timedelta

from github import Github


class ProjectOrchestrator:
    def __init__(self, token):
        self.gh = Github(token)
        self.project_repo = self.gh.get_repo("ZubeidHendricks/project-orchestrator")
        self.dev_repo = self.gh.get_repo("ZubeidHendricks/ai-dev-orchestrator")

    def analyze_developer_skills(self):
        """Map developers' skills and expertise"""
        dev_skills = {}
        for dev_issue in self.dev_repo.get_issues(state="closed"):
            if dev_issue.assignee:
                dev_name = dev_issue.assignee.login
                labels = [label.name for label in dev_issue.labels]

                if dev_name not in dev_skills:
                    dev_skills[dev_name] = {}

                for label in labels:
                    dev_skills[dev_name][label] = dev_skills[dev_name].get(label, 0) + 1

        return dev_skills

    def prioritize_tasks(self):
        """Advanced task prioritization"""
        tasks = []
        dev_skills = self.analyze_developer_skills()

        for issue in self.project_repo.get_issues(state="open"):
            # Complexity scoring
            complexity = len(issue.labels) * 2
            age_penalty = (datetime.now() - issue.created_at).days

            # Find best developer match
            best_dev = self._find_best_developer(issue, dev_skills)

            tasks.append(
                {
                    "issue_number": issue.number,
                    "title": issue.title,
                    "complexity": complexity,
                    "age": age_penalty,
                    "recommended_dev": best_dev,
                }
            )

        # Sort tasks by priority
        return sorted(tasks, key=lambda x: (x["complexity"], -x["age"]))

    def _find_best_developer(self, issue, dev_skills):
        """Match task to most skilled developer"""
        issue_labels = [label.name for label in issue.labels]

        best_match = None
        highest_score = 0

        for dev, skills in dev_skills.items():
            match_score = sum(skills.get(label, 0) for label in issue_labels)
            if match_score > highest_score:
                highest_score = match_score
                best_match = dev

        return best_match or random.choice(list(dev_skills.keys()))

    def generate_team_insights(self):
        """Generate comprehensive team performance insights"""
        dev_skills = self.analyze_developer_skills()
        tasks = self.prioritize_tasks()

        insights = {
            "team_skill_distribution": dev_skills,
            "task_priority_queue": tasks[:10],  # Top 10 priority tasks
            "unassigned_tasks_count": len(tasks),
            "recommended_assignments": [],
        }

        # Recommend assignments
        for task in tasks:
            if task["recommended_dev"]:
                insights["recommended_assignments"].append(
                    {"task": task["title"], "recommended_dev": task["recommended_dev"]}
                )

        return insights

    def save_insights(self, insights):
        """Save insights to file"""
        os.makedirs("data", exist_ok=True)
        with open("data/project_insights.json", "w") as f:
            json.dump(insights, f, indent=2)

        print("Project insights generated and saved.")


def main():
    token = os.environ.get("GHUB_TOKEN")
    orchestrator = ProjectOrchestrator(token)

    insights = orchestrator.generate_team_insights()
    orchestrator.save_insights(insights)


if __name__ == "__main__":
    main()
