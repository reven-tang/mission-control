"""routers/cron.py — Cron API"""

from fastapi import APIRouter

from ..services import get_cron_jobs

router = APIRouter(prefix="/cron", tags=["cron"])


@router.get("")
def get_cron():
    """获取 Cron 任务"""
    return get_cron_jobs()
