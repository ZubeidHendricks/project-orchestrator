import json
import os

from github import Github
from github.GithubException import GithubException


class AIDevWorkflowTrigger:
    def __init__(self, github_token):
        self.gh = Github(github_token)
        self.project_repo = self.gh.get_repo("ZubeidHendricks/project-orchestrator")
        self.aidev_repo = self.gh.get_repo("ZubeidHendricks/ai-dev-orchestrator")

    def find_unprocessed_issues(self):
        """Find issues in project-orchestrator that haven't been processed by AI dev"""
        unprocessed_issues = []
        for issue in self.project_repo.get_issues(state="open", labels=["ai-development"]):
            try:
                # Check if issue has already been processed
                processed = any("Processed by AI Dev" in comment.body for comment in issue.get_comments())

                if not processed:
                    unprocessed_issues.append(issue)

            except Exception as e:
                print(f"Error checking issue {issue.number}: {e}")

        return unprocessed_issues

    def trigger_ai_dev_workflow(self, issue):
        """Trigger AI development workflow for a specific issue"""
        try:
            # Prepare workflow dispatch payload
            workflow_inputs = {
                "issue_number": str(issue.number),
                "issue_title": issue.title,
                "issue_body": issue.body or "",
                "repository": issue.repository.full_name,
            }

            # Dispatch workflow in ai-dev-orchestrator
            workflow_file = self.aidev_repo.get_workflow("ai_development.yml")
            workflow_file.create_dispatch(ref="main", inputs=workflow_inputs)

            # Add comment to original issue
            issue.create_comment("🤖 AI Development workflow triggered. " "Processing started in ai-dev-orchestrator.")

            print(f"Triggered workflow for issue {issue.number}: {issue.title}")

        except GithubException as e:
            print(f"GitHub workflow dispatch error: {e}")
        except Exception as e:
            print(f"Error triggering workflow for issue {issue.number}: {e}")

    def process_pending_issues(self):
        """Process all unassigned issues marked for AI development"""
        unprocessed_issues = self.find_unprocessed_issues()

        for issue in unprocessed_issues:
            self.trigger_ai_dev_workflow(issue)


def main():
    github_token = os.environ.get("GHUB_TOKEN")
    if not github_token:
        print("GitHub token not found. Set GHUB_TOKEN environment variable.")
        return

    try:
        workflow_trigger = AIDevWorkflowTrigger(github_token)
        workflow_trigger.process_pending_issues()
    except Exception as e:
        print(f"Workflow trigger failed: {e}")


if __name__ == "__main__":
    main()
