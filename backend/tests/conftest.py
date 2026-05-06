"""conftest.py — Mission Control 后端测试 fixtures

核心：使用内存 SQLite 替换生产 DB，确保所有测试用同一个引擎。
"""

import sys
from pathlib import Path

# 添加项目根路径到 sys.path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 导入应用组件
from app.database import get_db
from app.models import Base

# 延迟导入 app（在路径设置好之后）
import importlib
app = importlib.import_module("app.main")

# 内存数据库 engine（启用 foreign keys）
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

TEST_ENGINE = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False}
)


# SQLite 需要 PRAGMA foreign_keys = ON
@event.listens_for(TEST_ENGINE, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TEST_ENGINE)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# 覆盖 get_db dependency
app.app.dependency_overrides[get_db] = override_get_db


import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def setup_db():
    """每个测试前创建表，测试后删除"""
    # 在 TEST_ENGINE 上创建所有表
    Base.metadata.create_all(bind=TEST_ENGINE)
    yield
    Base.metadata.drop_all(bind=TEST_ENGINE)


@pytest.fixture
def client():
    """FastAPI TestClient"""
    with TestClient(app.app) as c:
        yield c


@pytest.fixture
def db_session():
    """测试 DB session"""
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def sample_prd():
    """模拟 prd.json 数据"""
    return {
        "project": "test-project",
        "branchName": "test-branch",
        "version": "1.0.0",
        "description": "Test project for Mission Control",
        "stories": [
            {
                "id": "US-001",
                "title": "Test Story 1",
                "description": "A test story",
                "priority": 1,
                "passes": False,
                "acceptanceCriteria": [
                    {"id": "AC-001", "description": "Test AC 1", "type": "functional"}
                ],
                "actualIterations": 0
            },
            {
                "id": "US-002",
                "title": "Test Story 2",
                "description": "Another test story",
                "priority": 2,
                "passes": True,
                "acceptanceCriteria": [],
                "actualIterations": 1
            }
        ]
    }


@pytest.fixture
def mock_crontab_output():
    """模拟 crontab -l 输出"""
    return """# Mission Control Cron Jobs
*/30 * * * * /usr/bin/python3 /home/user/heartbeat.py
0 10 * * * /usr/bin/python3 /home/user/dreaming.py
"""
