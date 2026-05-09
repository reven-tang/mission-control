"""routers/system.py — System Stats API"""

import psutil
from fastapi import APIRouter

from ..services.health_aggregator import aggregator

router = APIRouter(prefix="/system", tags=["system"])


@router.get("")
def get_system_stats():
    """获取系统资源使用情况"""
    cpu_percent = psutil.cpu_percent(interval=0.5, percpu=True)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return {
        "cpu": {
            "usage": sum(cpu_percent) / len(cpu_percent),
            "cores": cpu_percent
        },
        "memory": {
            "total": mem.total,
            "used": mem.used,
            "free": mem.free,
            "percent": mem.percent
        },
        "disk": {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent
        }
    }


@router.get("/health")
def get_health_dashboard():
    """获取萨莉 OS 三系统健康仪表盘"""
    return aggregator.get_full_health()


@router.get("/health/summary")
def get_health_summary():
    """获取健康简版摘要"""
    return aggregator.get_summary()
