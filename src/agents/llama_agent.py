import os

from crewai import Agent
from langchain.llms import LlamaCpp


class LlamaAgent:
    def __init__(self):
# model_path
        self.llm = LlamaCpp(
# model_path
# temperature
# max_tokens
# n_ctx
# top_p
        )

    def create_portfolio_manager(self):
        return Agent(
# role
# goal
# backstory
# llm
        )

    def create_tech_lead(self):
        return Agent(
# role
# goal
# backstory
# llm
        )

    def create_qa_specialist(self):
        return Agent(
# role
# goal
# backstory
# llm
        )
