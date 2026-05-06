"""services/sessions_client.py — OpenClaw Agent 状态查询"""

from datetime import datetime
from typing import List, Dict, Any, Optional
import sys

# 添加 OpenClaw tools 路径
sys.path.insert(0, '/Users/jhwu/.openclaw/workspace/tools')

try:
    from sessions_list import sessions_list
    HAS_SESSIONS_LIST = True
except ImportError:
    HAS_SESSIONS_LIST = False


def get_real_agents() -> List[Dict[str, Any]]:
    """获取真实 Agent 状态
    
    Returns:
        Agent 列表，如果不可用则返回降级数据
    """
    if not HAS_SESSIONS_LIST:
        return _get_fallback_agents()
    
    try:
        # 获取活跃 sessions
        result = sessions_list.list_sessions(include_inactive=False, limit=20)
        agents = []
        for sess in result or []:
            agent = {
                "agent_id": sess.get('agent_id', 'unknown'),
                "name": sess.get('label', 'Agent'),
                "status": sess.get('status', 'unknown'),
                "model": sess.get('model', 'N/A'),
                "channel": sess.get('channel', 'N/A'),
                "started_at": sess.get('started_at', ''),
                "last_activity": sess.get('last_message_at', '')
            }
            agents.append(agent)
        return agents if agents else _get_fallback_agents()
    except Exception as e:
        print(f"Error fetching agents: {e}")
        return _get_fallback_agents()


def _get_fallback_agents() -> List[Dict[str, Any]]:
    """降级：返回模拟 Agent 数据"""
    return [{
        "agent_id": "main",
        "name": "Main Agent",
        "status": "running",
        "model": "MiniMax-M2.5",
        "channel": "feishu",
        "last_activity": datetime.now().isoformat()
    }]
