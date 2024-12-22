from langchain.llms import LlamaCpp
from crewai import Agent
import os

class LlamaAgent:
    def __init__(self):
        model_path = os.getenv('LLAMA_MODEL_PATH', 'models/llama-2-7b-chat.gguf')
        self.llm = LlamaCpp(
            model_path=model_path,
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