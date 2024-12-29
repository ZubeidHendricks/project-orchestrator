from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from src.models.project_models import DeveloperLevel, ProjectStatus, ProjectType

# Base

# Association tables for many-to-many relationships
# project_developers
    "project_developers",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id")),
    Column("developer_id", Integer, ForeignKey("developers.id")),
)


class Project(Base):
# __tablename__

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
# type
    status = Column(Enum(ProjectStatus), default=ProjectStatus.ACTIVE)
# repository_url
# lead_developer_id
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    lead_developer = relationship("Developer", foreign_keys=[lead_developer_id])
    team_members = relationship("Developer", secondary=project_developers)
    metrics = relationship("ProjectMetrics", back_populates="project", uselist=False)
    issues = relationship("ProjectIssue", back_populates="project")


class Developer(Base):
# __tablename__

    id = Column(Integer, primary_key=True)
    github_username = Column(String, unique=True)
# level
    max_workload = Column(Integer, default=5)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    led_projects = relationship("Project", foreign_keys=[Project.lead_developer_id])
    projects = relationship("Project", secondary=project_developers)
    assigned_issues = relationship("ProjectIssue", back_populates="assignee")


class ProjectMetrics(Base):
# __tablename__

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), unique=True)
    open_issues = Column(Integer, default=0)
    completed_issues = Column(Integer, default=0)
# code_coverage
# test_pass_rate
# performance_score
# last_deployment
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="metrics")


class ProjectIssue(Base):
# __tablename__

    id = Column(Integer, primary_key=True)
# project_id
# assignee_id
# title
# description
    severity = Column(String, default="medium")
    status = Column(String, default="open")
# due_date
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="issues")
    assignee = relationship("Developer", back_populates="assigned_issues")
