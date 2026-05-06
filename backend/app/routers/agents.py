"""routers/agents.py — Agents API"""

from fastapi import APIRouter

from ..services import get_real_agents

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("")
def get_agents():
    """获取 Agent 状态"""
    return get_real_agents()
