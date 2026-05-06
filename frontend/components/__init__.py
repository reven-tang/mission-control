"""components/__init__.py — 前端组件索引"""

from .kanban import render as render_kanban
from .agents import render as render_agents
from .cron import render as render_cron
from .healthcheck import render as render_healthcheck
from .skills import render as render_skills
from .system import render as render_system

__all__ = [
    "render_kanban",
    "render_agents",
    "render_cron",
    "render_healthcheck",
    "render_skills",
    "render_system",
]