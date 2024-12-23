from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class ProjectType(str, Enum):
    POS = "pos"
    AI = "ai"
    BLOCKCHAIN = "blockchain"


class ProjectStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class DeveloperLevel(str, Enum):
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"


class DeveloperExpertise(BaseModel):
    primary: List[str] = Field(..., description="Primary skills of the developer")
    secondary: Optional[List[str]] = Field(default=None, description="Secondary skills")


class Developer(BaseModel):
    github_username: str
    level: DeveloperLevel
    expertise: DeveloperExpertise
    max_workload: int = Field(
        default=5, description="Maximum number of concurrent tasks"
    )
    current_projects: List[str] = Field(default_factory=list)


class ProjectIssue(BaseModel):
    title: str
    description: str
    severity: str = Field(default="medium")
    assignee: Optional[str] = None
    due_date: Optional[datetime] = None
    tags: List[str] = Field(default_factory=list)


class ProjectMetrics(BaseModel):
    open_issues: int = 0
    completed_issues: int = 0
    code_coverage: Optional[float] = None
    test_pass_rate: Optional[float] = None
    performance_score: Optional[float] = None
    last_deployment: Optional[datetime] = None


class Project(BaseModel):
    name: str
    type: ProjectType
    status: ProjectStatus = Field(default=ProjectStatus.ACTIVE)
    repository_url: str
    lead_developer: str
    team_members: List[str]
    metrics: ProjectMetrics = Field(default_factory=ProjectMetrics)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        use_enum_values = True
