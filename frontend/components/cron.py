"""components/cron.py — Cron 定时任务"""

import streamlit as st
from api_client import api_get


def render():
    """渲染 Cron 任务面板"""
    st.header("⏰ Cron 定时任务")
    
    jobs = api_get("/cron") or []
    for job in jobs:
        job_name = job.get("name", "Unknown")
        with st.expander(f"📌 {job_name} · `{job.get('schedule','')}`", expanded=False):
            col1, col2 = st.columns(2)
            col1.markdown(f"**调度:** `{job.get('schedule','N/A')}`")
            col2.markdown(f"**状态:** {'✅ 正常' if job.get('status') == 'success' else '❌ 异常'}")
            
            if job.get("description"):
                st.markdown(f"**描述:** {job.get('description')}")
            
            if job.get("command"):
                st.code(job.get("command"), language="bash")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("上次运行", job.get("last_run", "未知"))
            col2.metric("下次运行", job.get("next_run", "计算中"))
            col3.metric("执行结果", job.get("status", "未知").upper())