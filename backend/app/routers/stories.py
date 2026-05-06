"""routers/stories.py — Stories API"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..services import get_project_stories, update_story_status, sync_projects_from_openspec
from pydantic import BaseModel

router = APIRouter(prefix="/stories", tags=["stories"])


@router.get("")
def get_stories(
    project: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取 Story 列表"""
    stories = get_project_stories(db, project=project, status=status)
    return stories


@router.get("/{story_id}")
def get_story(story_id: str, db: Session = Depends(get_db)):
    """获取单个 Story 详情"""
    story = get_story_by_id(db, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


@router.post("/sync")
def sync_stories(db: Session = Depends(get_db)):
    """同步 openspec 项目数据"""
    result = sync_projects_from_openspec(db)
    return {"status": "synced", **result}


class StatusUpdate(BaseModel):
    passes: bool


@router.post("/{story_id}/status")
def update_status(story_id: str, update: StatusUpdate, db: Session = Depends(get_db)):
    """更新 Story 状态"""
    result = update_story_status(db, story_id, update.passes)
    if not result:
        raise HTTPException(status_code=404, detail="Story not found")
    return result
