import os
from typing import Dict, List, Optional

from pydantic import BaseSettings, Field, validator


class LLMSettings(BaseSettings):
    model_path: str = Field(..., description="Path to the LLM model file")
    n_gpu_layers: int = Field(40, description="Number of GPU layers to use")
    n_batch: int = Field(512, description="Batch size for processing")
    n_ctx: int = Field(4096, description="Context window size")
    temperature: float = Field(0.7, description="Model temperature")

    @validator("model_path")
    def validate_model_path(cls, v):
        if not os.path.exists(v):
            raise ValueError(f"Model file not found at: {v}")
        return v


class GitHubSettings(BaseSettings):
    token: str = Field(..., description="GitHub API token")
    organization: Optional[str] = None
    repositories: List[str] = Field(default_factory=list)

    @validator("token")
    def validate_token(cls, v):
        if not v.startswith("ghp_"):
            raise ValueError("Invalid GitHub token format")
        return v


class TeamSettings(BaseSettings):
    max_workload_per_dev: int = Field(5, description="Maximum concurrent tasks per developer")
    default_review_timeout: int = Field(24, description="Hours before review reminder")
    auto_assign: bool = Field(True, description="Enable automatic task assignment")


class Settings(BaseSettings):
    llm: LLMSettings
    github: GitHubSettings
    team: TeamSettings
    log_level: str = Field("INFO", description="Logging level")
    data_dir: str = Field("data", description="Directory for storing data")
    enable_monitoring: bool = Field(True, description="Enable system monitoring")

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"

    @validator("data_dir")
    def create_data_dir(cls, v):
        os.makedirs(v, exist_ok=True)
        return v


def get_settings() -> Settings:
    """Load and validate settings"""
    return Settings(
        llm=LLMSettings(model_path=os.getenv("LLAMA_MODEL_PATH", "models/llama-2-70b-chat.gguf")),
        github=GitHubSettings(token=os.getenv("GHUB_TOKEN")),
        team=TeamSettings(),
    )
