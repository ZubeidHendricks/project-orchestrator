import os

from crewai import Agent
from langchain.llms import LlamaCpp


class LlamaAgent:
    def __init__(self):
        model_path = os.getenv("LLAMA_MODEL_PATH", "models/llama-2-7b-chat.gguf")
        self.llm = LlamaCpp(
            model_path=model_path,
            temperature=0.7,
            max_tokens=2000,
            n_ctx=4096,
            top_p=1,
        )

    def create_portfolio_manager(self):
        return Agent(
            role="Portfolio Manager",
            goal="Manage and coordinate development projects",
            backstory="Senior portfolio manager with expertise in multi-project coordination",
            llm=self.llm,
        )

    def create_tech_lead(self):
        return Agent(
            role="Technical Lead",
            goal="Review code and maintain technical standards",
            backstory="Senior developer with focus on code quality and architecture",
            llm=self.llm,
        )

    def create_qa_specialist(self):
        return Agent(
            role="QA Specialist",
            goal="Ensure software quality and testing",
            backstory="Quality assurance expert with automation expertise",
            llm=self.llm,
        )
