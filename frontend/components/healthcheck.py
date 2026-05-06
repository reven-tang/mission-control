"""components/healthcheck.py — Brain Healthcheck"""

import streamlit as st
from api_client import api_get, api_post


def render():
    """渲染 Healthcheck 面板"""
    st.header("💓 Brain Healthcheck")
    
    status = api_get("/healthcheck")
    if status:
        col1, col2 = st.columns(2)
        col1.metric("上次运行", status.get("last_run", "?")[:30])
        col2.metric("状态", status.get("status", "?").upper())
        
        checks = status.get("checks", {})
        if checks:
            st.subheader("📊 检查项概览")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Brain 文件", checks.get("brain_files"))
            c2.metric("QMD 索引", checks.get("qmd_index"))
            c3.metric("Skills", checks.get("skills"))
            c4.metric("Graph 节点", checks.get("graph_nodes"))
        
        runs_data = api_get("/healthcheck/runs") or {}
        runs = runs_data.get("runs", [])
        if runs:
            st.subheader("📜 历史记录")
            for run in runs[:10]:
                st.caption(f"`{run.get('timestamp','')}` {run.get('message','')[:80]}")
        
        if st.button("🔄 运行 Healthcheck", type="primary", key="run_hc"):
            with st.spinner("运行中..."):
                result = api_post("/healthcheck/run")
                if result:
                    st.success(result.get("status"))
                    st.code(result.get("output", "")[:800])