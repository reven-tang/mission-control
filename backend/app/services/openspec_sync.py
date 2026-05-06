"""services/openspec_sync.py — 从 openspec 同步项目数据"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from ..models import Project, Story
from ..database import get_workspace
from ..logging_config import get_logger

logger = get_logger("openspec_sync")


def sync_projects_from_openspec(db: Session) -> Dict[str, int]:
    """从 openspec/changes/*/prd.json 同步项目到数据库
    
    Returns:
        {"projects": N, "stories": M}
    """
    logger.info("开始同步 openspec 项目数据")
    workspace = get_workspace()
    openspec = workspace / "openspec/changes"
    
    project_count = 0
    story_count = 0
    
    if not openspec.exists():
        logger.warning("openspec 目录不存在")
        return {"projects": 0, "stories": 0}
    
    for prd_file in openspec.glob("*/prd.json"):
        try:
            with open(prd_file) as f:
                prd = json.load(f)
        except (json.JSONDecodeError, IOError):
            continue
        
        project_name = prd.get("project", prd_file.parent.name)
        
        # 查找或创建项目
        project = db.query(Project).filter(Project.name == project_name).first()
        if not project:
            project = Project(
                name=project_name,
                path=str(prd_file.parent),
                description=prd.get("description", "")
            )
            db.add(project)
            db.flush()
            project_count += 1
        
        # 同步 Stories
        for story_data in prd.get("stories", []):
            story_id = story_data.get("id")
            
            # 使用复合键查找
            story = db.query(Story).filter(
                Story.project_id == project.id,
                Story.id == story_id
            ).first()
            
            if story:
                story.title = story_data.get("title", story.title)
                story.description = story_data.get("description", story.description)
                story.priority = story_data.get("priority", story.priority)
                story.passes = story_data.get("passes", story.passes)
                story.acceptance_criteria = story_data.get("acceptanceCriteria", [])
                story.actual_iterations = story_data.get("actualIterations", 0)
                story.project_name = project_name
                story.updated_at = datetime.now()
            else:
                story = Story(
                    project_id=project.id,
                    id=story_id,
                    project_name=project_name,
                    title=story_data.get("title", ""),
                    description=story_data.get("description", ""),
                    priority=story_data.get("priority", 5),
                    passes=story_data.get("passes", False),
                    acceptance_criteria=story_data.get("acceptanceCriteria", []),
                    actual_iterations=story_data.get("actualIterations", 0)
                )
                db.add(story)
                story_count += 1
        
        db.commit()
    
    return {"projects": project_count, "stories": story_count}


def get_all_projects(db: Session) -> List[Dict[str, Any]]:
    """获取所有项目"""
    projects = db.query(Project).all()
    return [
        {"id": p.id, "name": p.name, "path": p.path, "description": p.description}
        for p in projects
    ]


def get_project_stories(
    db: Session,
    project: Optional[str] = None,
    status: Optional[str] = None
) -> List[Dict[str, Any]]:
    """获取 Stories 列表"""
    query = db.query(Story)
    
    if project:
        query = query.filter(Story.project_name == project)
    if status == "todo":
        query = query.filter(Story.passes == False)
    elif status == "done":
        query = query.filter(Story.passes == True)
    
    stories = query.order_by(Story.project_id, Story.priority, Story.id).all()
    return [
        {
            "id": s.id,
            "project_id": s.project_id,
            "project_name": s.project_name,
            "title": s.title,
            "description": s.description,
            "priority": s.priority,
            "passes": s.passes,
            "acceptance_criteria": s.acceptance_criteria,
            "actual_iterations": s.actual_iterations
        }
        for s in stories
    ]


def update_story_status(db: Session, story_id: str, passes: bool) -> Optional[Dict[str, Any]]:
    """更新 Story 的 passes 状态，并回写到 prd.json
    
    Args:
        story_id: Story ID（如 US-001）
        passes: 新状态
    
    Returns:
        更新后的 Story dict，如果找不到返回 None
    """
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        logger.warning(f"Story {story_id} 不存在")
        return None
    
    # 更新 DB
    story.passes = passes
    story.updated_at = datetime.now()
    db.commit()
    db.refresh(story)
    logger.info(f"Story {story_id} 状态更新为 passes={passes}")
    
    # 回写到 prd.json
    _write_back_to_prd(db, story.project_name)
    
    return {
        "id": story.id,
        "project_name": story.project_name,
        "title": story.title,
        "passes": story.passes,
        "updated_at": story.updated_at.isoformat() if story.updated_at else None
    }


def _write_back_to_prd(db: Session, project_name: str):
    """将 DB 变更回写到 prd.json"""
    workspace = get_workspace()
    openspec = workspace / "openspec/changes"
    
    project = db.query(Project).filter(Project.name == project_name).first()
    if not project:
        return
    
    prd_path = Path(project.path) / "prd.json"
    if not prd_path.exists():
        logger.warning(f"prd.json 不存在: {prd_path}")
        return
    
    try:
        with open(prd_path) as f:
            prd = json.load(f)
        
        stories_in_db = db.query(Story).filter(Story.project_id == project.id).all()
        for story_db in stories_in_db:
            for story_prd in prd.get("stories", []):
                if story_prd.get("id") == story_db.id:
                    story_prd["passes"] = story_db.passes
                    story_prd["actualIterations"] = story_db.actual_iterations
        
        with open(prd_path, "w") as f:
            json.dump(prd, f, indent=2, ensure_ascii=False)
        logger.info(f"回写 prd.json: {prd_path}")
    except Exception as e:
        logger.error(f"回写 prd.json 失败: {e}")
