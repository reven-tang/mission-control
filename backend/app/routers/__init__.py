"""routers/__init__.py — API 路由聚合"""

from .stories import router as stories_router
from .projects import router as projects_router
from .agents import router as agents_router
from .cron import router as cron_router
from .health import router as health_router
from .skills import router as skills_router
from .system import router as system_router

__all__ = [
    "stories_router",
    "projects_router", 
    "agents_router",
    "cron_router",
    "health_router",
    "skills_router",
    "system_router",
]
