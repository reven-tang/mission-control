"""database.py — 数据库配置"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pathlib import Path
from typing import Generator

DATABASE_URL = "sqlite:///./mission_control.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Generator[Session, None, None]:
    """FastAPI 依赖：获取 DB session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_workspace() -> Path:
    """获取 OpenClaw workspace 路径"""
    return Path.home() / ".openclaw/workspace"
