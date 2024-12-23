from datetime import datetime

from sqlalchemy import (Column, DateTime, Enum, Float, ForeignKey, Integer,
                        String, Table)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from src.models.project_models import (DeveloperLevel, ProjectStatus,
                                       ProjectType)

Base = declarative_base()

# Association tables for many-to-many relationships
project_developers = Table(
    "project_developers",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id")),
    Column("developer_id", Integer, ForeignKey("developers.id")),
)


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    type = Column(Enum(ProjectType))
    status = Column(Enum(ProjectStatus), default=ProjectStatus.ACTIVE)
    repository_url = Column(String)
    lead_developer_id = Column(Integer, ForeignKey("developers.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    lead_developer = relationship("Developer", foreign_keys=[lead_developer_id])
    team_members = relationship("Developer", secondary=project_developers)
    metrics = relationship("ProjectMetrics", back_populates="project", uselist=False)
    issues = relationship("ProjectIssue", back_populates="project")


class Developer(Base):
    __tablename__ = "developers"

    id = Column(Integer, primary_key=True)
    github_username = Column(String, unique=True)
    level = Column(Enum(DeveloperLevel))
    max_workload = Column(Integer, default=5)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    led_projects = relationship("Project", foreign_keys=[Project.lead_developer_id])
    projects = relationship("Project", secondary=project_developers)
    assigned_issues = relationship("ProjectIssue", back_populates="assignee")


class ProjectMetrics(Base):
    __tablename__ = "project_metrics"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), unique=True)
    open_issues = Column(Integer, default=0)
    completed_issues = Column(Integer, default=0)
    code_coverage = Column(Float)
    test_pass_rate = Column(Float)
    performance_score = Column(Float)
    last_deployment = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="metrics")


class ProjectIssue(Base):
    __tablename__ = "project_issues"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    assignee_id = Column(Integer, ForeignKey("developers.id"))
    title = Column(String)
    description = Column(String)
    severity = Column(String, default="medium")
    status = Column(String, default="open")
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="issues")
    assignee = relationship("Developer", back_populates="assigned_issues")
