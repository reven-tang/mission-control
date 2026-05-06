"""components/agents.py — Agent 状态"""

import streamlit as st
from api_client import api_get


def render():
    """渲染 Agent 状态面板"""
    st.header("🤖 Agent 状态")
    
    agents = api_get("/agents") or []
    if not agents:
        st.info("暂无活跃 Agent")
        return
    
    for agent in agents:
        with st.container(border=True):
            cols = st.columns(5)
            cols[0].metric("Agent", agent.get("agent_id", "?"))
            cols[1].metric("状态", agent.get("status", "?").upper())
            cols[2].metric("模型", agent.get("model", "?"))
            cols[3].metric("渠道", agent.get("channel", "?"))
            cols[4].metric("最近活动", agent.get("last_activity", "?")[:19] if agent.get("last_activity") else "?")