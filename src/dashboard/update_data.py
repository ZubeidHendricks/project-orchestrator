#!/usr/bin/env python3
import json
import os
from datetime import datetime

import networkx as nx
from github import Github


class CrossRepositoryOrchestrator:
    def __init__(self, token):
        self.gh = Github(token)
        self.repositories = [
            "ZubeidHendricks/project-orchestrator",
            "ZubeidHendricks/ai-dev-orchestrator",
        ]

    def build_dependency_graph(self):
        """Create a dependency network between repositories"""
        G = nx.DiGraph()

        for repo_name in self.repositories:
            repo = self.gh.get_repo(repo_name)
            G.add_node(
                repo_name,
                total_issues=repo.get_issues().totalCount,
                open_issues=repo.get_issues(state="open").totalCount,
                last_updated=repo.updated_at.isoformat(),
            )

            # Analyze inter-repository references
            for issue in repo.get_issues(state="open"):
                # Check for cross-repository references in issue body
                for ref_repo in self.repositories:
                    if ref_repo in issue.body:
                        G.add_edge(
                            repo_name,
                            ref_repo,
                            issue_number=issue.number,
                            reference_type="issue_link",
                        )

        return G

    def generate_project_health_report(self):
        """Generate comprehensive project health insights"""
        dependency_graph = self.build_dependency_graph()

        health_report = {
            "timestamp": datetime.now().isoformat(),
            "repositories": {},
            "cross_repo_dependencies": [],
        }

        # Repository-level insights
        for repo_name in self.repositories:
            repo_data = dependency_graph.nodes[repo_name]
            health_report["repositories"][repo_name] = {
                "total_issues": repo_data["total_issues"],
                "open_issues": repo_data["open_issues"],
                "last_updated": repo_data["last_updated"],
                "health_score": self._calculate_repo_health(repo_name),
            }

        # Cross-repository dependency insights
        for edge in dependency_graph.edges(data=True):
            health_report["cross_repo_dependencies"].append(
                {
                    "source": edge[0],
                    "target": edge[1],
                    "issue_number": edge[2].get("issue_number"),
                }
            )

        # Save insights
        os.makedirs("data", exist_ok=True)
        with open("data/cross_repo_health.json", "w") as f:
            json.dump(health_report, f, indent=2)

        return health_report

    def _calculate_repo_health(self, repo_name):
        """Calculate repository health score"""
        repo = self.gh.get_repo(repo_name)
        open_issues = repo.get_issues(state="open").totalCount
        closed_issues = repo.get_issues(state="closed").totalCount

        # Simple health calculation
        if closed_issues == 0:
            return 0

        health_score = (closed_issues / (open_issues + closed_issues)) * 100
        return round(health_score, 2)

    def synchronize_project_status(self):
        """Synchronize status across repositories"""
        health_report = self.generate_project_health_report()

        # Example synchronization logic
        for repo_name, repo_data in health_report["repositories"].items():
            repo = self.gh.get_repo(repo_name)

            # Update repository description with health insights
            new_description = (
                f"Project Health: {repo_data['health_score']}% | "
                f"Open Issues: {repo_data['open_issues']}"
            )

            # Only update if description has changed
            if repo.description != new_description:
                repo.edit(description=new_description)


def main():
    token = os.environ.get("GHUB_TOKEN")
    orchestrator = CrossRepositoryOrchestrator(token)
    orchestrator.synchronize_project_status()
    print("Cross-Repository Synchronization Complete")


if __name__ == "__main__":
    main()
