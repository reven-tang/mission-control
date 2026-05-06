"""routers/projects.py — Projects API"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..services import get_all_projects, sync_projects_from_openspec

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("")
def get_projects(db: Session = Depends(get_db)):
    """获取项目列表"""
    return get_all_projects(db)


@router.post("/sync")
def sync_projects(db: Session = Depends(get_db)):
    """同步 openspec 项目"""
    sync_projects_from_openspec(db)
    return {"status": "synced"}
