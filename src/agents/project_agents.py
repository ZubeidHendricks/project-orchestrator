import os

from crewai import Agent, Crew, Task
from langchain.llms import LlamaCpp


class ProjectAgents:
    def __init__(self):
        self.llm = LlamaCpp(
            model_path=os.getenv("LLAMA_MODEL_PATH", "models/llama-2-70b-chat.gguf"),
            n_gpu_layers=40,  # Utilize GPU layers for 70B model
            n_batch=512,  # Increased batch size
            n_ctx=4096,  # Context window
            f16_kv=True,  # Use half-precision for key/value cache
            temperature=0.7,
            max_tokens=2000,
            # GPU specific settings
            n_threads=8,  # Number of CPU threads
            n_threads_batch=8,  # Number of threads when batching
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

    # Rest of the code remains the same...
