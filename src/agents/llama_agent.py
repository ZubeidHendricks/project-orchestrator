from langchain.llms import LlamaCpp
from crewai import Agent
import os

class LlamaAgent:
    def __init__(self):
        self.llm = LlamaCpp(
            model_path="path/to/your/llama/model.gguf",  # Update with your model path
            temperature=0.7,
            max_tokens=2000,
            n_ctx=4096,
            top_p=1
        )

    def create_portfolio_manager(self):
        return Agent(
            role='Portfolio Manager',
            goal='Manage and coordinate development projects',
            backstory='Senior portfolio manager with expertise in multi-project coordination',
            llm=self.llm
        )

    def create_tech_lead(self):
        return Agent(
            role='Technical Lead',
            goal='Review code and maintain technical standards',
            backstory='Senior developer with focus on code quality and architecture',
            llm=self.llm
        )

    def create_qa_specialist(self):
        return Agent(
            role='QA Specialist',
            goal='Ensure software quality and testing',
            backstory='Quality assurance expert with automation expertise',
            llm=self.llm
        )