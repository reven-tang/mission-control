"""routers/skills.py — Skills API"""

import json
from pathlib import Path
from fastapi import APIRouter
from datetime import datetime

from ..database import get_workspace

router = APIRouter(prefix="/skills", tags=["skills"])


@router.get("")
def get_skills():
    """获取 Skills 状态"""
    workspace = get_workspace()
    skills_dir = workspace / "skills"
    graph_file = workspace / "tools/skill_graph.json"
    
    total = 0
    if skills_dir.exists():
        total = len(list(skills_dir.glob("*/SKILL.md")))
    
    graph_nodes = graph_edges = 0
    graph = {"nodes": {}, "edges": []}
    if graph_file.exists():
        try:
            with open(graph_file) as f:
                graph = json.load(f)
                graph_nodes = len(graph.get("nodes", {}))
                graph_edges = len(graph.get("edges", []))
        except json.JSONDecodeError:
            pass
    
    recent = []
    if skills_dir.exists():
        recent_skills = sorted(
            skills_dir.glob("*/SKILL.md"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )[:5]
        for skill in recent_skills:
            recent.append({
                "name": skill.parent.name,
                "modified": datetime.fromtimestamp(skill.stat().st_mtime).isoformat()
            })
    
    # 评分数据
    evaluations_dir = workspace / "skill-evaluations-v5"
    evaluations = []
    if evaluations_dir.exists():
        for report in evaluations_dir.glob("*.json"):
            try:
                with open(report) as f:
                    data = json.load(f)
                    name = report.stem
                    score = data.get("overall_score", 0)
                    grade = "Excellent" if score >= 90 else "Good" if score >= 70 else "Fair" if score >= 55 else "Poor"
                    evaluations.append({"name": name, "score": score, "grade": grade})
            except (json.JSONDecodeError, IOError):
                pass
    
    return {
        "total": total,
        "graph_nodes": graph_nodes,
        "graph_edges": graph_edges,
        "recent": recent,
        "evaluations": evaluations,
        "graph": graph
    }


@router.get("/graph")
def get_skills_graph():
    """获取 Skills Graph 数据"""
    workspace = get_workspace()
    graph_file = workspace / "tools/skill_graph.json"
    
    if not graph_file.exists():
        return {"nodes": {}, "edges": []}
    
    try:
        with open(graph_file) as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"nodes": {}, "edges": []}
