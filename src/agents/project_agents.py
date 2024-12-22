import os

from crewai import Agent, Crew, Task
from langchain.llms import LlamaCpp


class ProjectAgents:
    def __init__(self):
        self.llm = LlamaCpp(
            model_path="models/llama-2-7b-chat.gguf", temperature=0.7, max_tokens=2000
        )

    def create_project_manager(self):
        return Agent(
            role="Project Manager",
            goal="Oversee project development and coordinate team assignments",
            backstory="Experienced project manager with expertise in development workflows",
            llm=self.llm,
            tools=["github_issue_creation", "team_assignment", "workload_analysis"],
            verbose=True,
        )

    def create_tech_lead(self):
        return Agent(
            role="Technical Lead",
            goal="Analyze technical issues and guide development decisions",
            backstory="Senior technical lead with full-stack development expertise",
            llm=self.llm,
            tools=["code_review", "architecture_analysis", "technical_assessment"],
            verbose=True,
        )

    def create_devops_specialist(self):
        return Agent(
            role="DevOps Specialist",
            goal="Monitor and maintain development infrastructure",
            backstory="DevOps expert focused on CI/CD and infrastructure management",
            llm=self.llm,
            tools=[
                "pipeline_monitoring",
                "deployment_analysis",
                "infrastructure_check",
            ],
            verbose=True,
        )

    def get_crew(self):
        return Crew(
            agents=[
                self.create_project_manager(),
                self.create_tech_lead(),
                self.create_devops_specialist(),
            ],
            tasks=self.create_tasks(),
            process="sequential",
        )

    def create_tasks(self):
        return [
            Task(
                description="Review project status and assign tasks",
                agent=self.create_project_manager(),
            ),
            Task(
                description="Analyze technical issues and provide solutions",
                agent=self.create_tech_lead(),
            ),
            Task(
                description="Monitor infrastructure and deployment status",
                agent=self.create_devops_specialist(),
            ),
        ]
