"""models.py — 数据模型"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Project(Base):
    """项目模型"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    path = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)


class Story(Base):
    """Story 模型（复合主键）"""
    __tablename__ = "stories"
    
    project_id = Column(Integer, primary_key=True, index=True)
    id = Column(String, primary_key=True)  # story id within project
    
    project_name = Column(String, index=True)
    title = Column(String)
    description = Column(Text)
    priority = Column(Integer, default=5)
    passes = Column(Boolean, default=False)
    acceptance_criteria = Column(JSON, default=list)
    actual_iterations = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
