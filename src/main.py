from crewai import Crew, Process

from src.agents.llama_agent import LlamaAgent
from src.reporting.report_generator import ReportGenerator
from src.workflows.project_tracker import ProjectTracker


class ProjectOrchestrator:
    def __init__(self):
        self.llama = LlamaAgent()
        self.setup_components()

    def setup_components(self):
        self.portfolio_manager = self.llama.create_portfolio_manager()
        self.tech_lead = self.llama.create_tech_lead()
        self.qa_specialist = self.llama.create_qa_specialist()
        self.tracker = ProjectTracker()

    def create_daily_tasks(self):
        return [
            {
                "role": "Portfolio Manager",
                "task": "Review project status and assign tasks",
                "priority": "high",
            },
            {
                "role": "Tech Lead",
                "task": "Code review and architecture assessment",
                "priority": "high",
            },
            {
                "role": "QA Specialist",
                "task": "Test coverage and quality metrics review",
                "priority": "medium",
            },
        ]

    def run_daily_review(self):
        crew = Crew(
            agents=[self.portfolio_manager, self.tech_lead, self.qa_specialist],
            tasks=self.create_daily_tasks(),
            process=Process.sequential,
            verbose=True,
        )
        return crew.kickoff()


if __name__ == "__main__":
    orchestrator = ProjectOrchestrator()
    result = orchestrator.run_daily_review()
    print("Daily Review Complete!\n")
    print(result)