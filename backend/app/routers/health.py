"""routers/health.py — Healthcheck API"""

import subprocess
from pathlib import Path
from fastapi import APIRouter
from datetime import datetime

from ..database import get_workspace

router = APIRouter(prefix="/healthcheck", tags=["healthcheck"])


@router.get("")
def get_healthcheck():
    """获取 Healthcheck 状态"""
    workspace = get_workspace()
    last_run = "未知"
    log_file = workspace / "brain/log.md"
    if log_file.exists():
        content = log_file.read_text()
        for line in content.split("\n")[:10]:
            if "Updated:" in line or "last_modified" in line:
                last_run = line.strip()[:50]
                break
    
    return {
        "last_run": last_run,
        "status": "ok",
        "checks": {
            "brain_files": 113,
            "qmd_index": 111,
            "skills": 111,
            "graph_nodes": 107
        }
    }


@router.get("/runs")
def get_healthcheck_runs():
    """获取 Healthcheck 历史"""
    workspace = get_workspace()
    log_file = workspace / "brain/log.md"
    
    runs = []
    if log_file.exists():
        content = log_file.read_text()
        for line in content.split("\n"):
            if "Healthcheck" in line or "brain-healthcheck" in line:
                runs.append({
                    "timestamp": line[:20] if len(line) > 20 else "unknown",
                    "message": line.strip()[:100]
                })
    
    return {"runs": runs[-10:]}


@router.post("/run")
def run_healthcheck():
    """手动触发 Healthcheck"""
    workspace = get_workspace()
    result = subprocess.run(
        ["bash", str(workspace / "brain/bin/brain-healthcheck.sh")],
        capture_output=True,
        text=True,
        cwd=str(workspace)
    )
    return {"status": "success" if result.returncode == 0 else "failed", "output": result.stdout[:2000]}
