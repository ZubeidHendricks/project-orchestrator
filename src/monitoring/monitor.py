#!/usr/bin/env python3
import json
import logging
import os
from datetime import datetime

from github import Github

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class RepositoryMonitor:
    def __init__(self, token):
        """Initialize repository monitoring system"""
        self.gh = Github(token)
        self.username = "ZubeidHendricks"
        self.repositories = self._get_repositories()

    def _get_repositories(self):
        """Fetch all repositories for the user"""
        try:
            return list(self.gh.get_user().get_repos())
        except Exception as e:
            logger.error(f"Failed to fetch repositories: {e}")
            return []

    def generate_repository_status(self):
        """Generate comprehensive status for all repositories"""
        repository_status = {
            "timestamp": datetime.now().isoformat(),
            "total_repositories": len(self.repositories),
            "repositories": [],
        }

        for repo in self.repositories:
            try:
                repo_info = {
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "description": repo.description,
                    "stars": repo.stargazers_count,
                    "forks": repo.forks_count,
                    "open_issues": repo.open_issues_count,
                    "last_updated": repo.updated_at.isoformat(),
                    "is_private": repo.private,
                }
                repository_status["repositories"].append(repo_info)
            except Exception as e:
                logger.error(f"Error processing repository {repo.name}: {e}")

        return repository_status

    def track_workflow_runs(self):
        """Track recent workflow runs across repositories"""
        workflow_runs = {"timestamp": datetime.now().isoformat(), "workflow_runs": []}

        for repo in self.repositories:
            try:
                # Fetch recent workflow runs
                runs = repo.get_workflow_runs(status="completed")

                for run in runs[:10]:  # Last 10 runs
                    run_info = {
                        "repository": repo.full_name,
                        "workflow_name": run.name,
                        "conclusion": run.conclusion,
                        "created_at": run.created_at.isoformat(),
                        "updated_at": run.updated_at.isoformat(),
                    }
                    workflow_runs["workflow_runs"].append(run_info)
            except Exception as e:
                logger.error(f"Error tracking workflows for {repo.name}: {e}")

        return workflow_runs

    def generate_comprehensive_report(self):
        """Generate a comprehensive monitoring report"""
        report = {
            "repository_status": self.generate_repository_status(),
            "workflow_runs": self.track_workflow_runs(),
        }

        # Ensure data directory exists
        os.makedirs("data/monitoring", exist_ok=True)

        # Save report
        report_path = (
            f'data/monitoring/report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        logger.info(f"Monitoring report generated: {report_path}")
        return report


def main():
    token = os.environ.get("GHUB_TOKEN")
    if not token:
        logger.error("GitHub token not found. Set GHUB_TOKEN environment variable.")
        return

    try:
        monitor = RepositoryMonitor(token)

        # Generate comprehensive report
        report = monitor.generate_comprehensive_report()

        # Print summary
        print(
            f"Monitored {len(report['repository_status']['repositories'])} repositories"
        )
        print(f"Tracked {len(report['workflow_runs']['workflow_runs'])} workflow runs")

    except Exception as e:
        logger.error(f"Monitoring failed: {e}")


if __name__ == "__main__":
    main()
