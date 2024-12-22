from crewai import Crew

from src.agents.project_agents import ProjectAgents
from src.tools.devops_tools import DevOpsTools
from src.tools.github_tools import GitHubTools
from src.tools.technical_tools import TechnicalTools


class ProjectOrchestrator:
    def __init__(self):
        self.agents = ProjectAgents()
        self.github_tools = GitHubTools()
        self.technical_tools = TechnicalTools()
        self.devops_tools = DevOpsTools()

    def run_analysis(self):
        """Run complete project analysis using CrewAI"""
        # Create the crew
        crew = Crew(
            agents=[
                self.agents.create_project_manager(),
                self.agents.create_tech_lead(),
                self.agents.create_devops_specialist(),
            ],
            tasks=self.create_tasks(),
            process="sequential",
        )

        # Start the analysis
        result = crew.kickoff()
        return result

    def create_tasks(self):
        """Create tasks for the crew"""
        return [
            {
                "description": (
                    "Analyze all repositories and create work items. Consider:\n"
                    "1. Current project status\n"
                    "2. Open issues and PRs\n"
                    "3. Team workload\n"
                    "4. Priority tasks"
                ),
                "agent": self.agents.create_project_manager(),
            },
            {
                "description": (
                    "Review technical debt and architecture. Focus on:\n"
                    "1. Code quality\n"
                    "2. Architecture patterns\n"
                    "3. Technical improvements\n"
                    "4. Performance issues"
                ),
                "agent": self.agents.create_tech_lead(),
            },
            {
                "description": (
                    "Monitor infrastructure and DevOps. Check:\n"
                    "1. Pipeline status\n"
                    "2. Deployment health\n"
                    "3. Infrastructure issues\n"
                    "4. Security concerns"
                ),
                "agent": self.agents.create_devops_specialist(),
            },
        ]


def main():
    orchestrator = ProjectOrchestrator()
    results = orchestrator.run_analysis()
    print("Analysis completed!")
    print(results)


if __name__ == "__main__":
    main()
