"""components/system.py — 系统资源监控"""

import streamlit as st
from api_client import api_get
from datetime import datetime


def render():
    """渲染系统资源面板"""
    st.header("💻 系统资源监控")
    
    data = api_get("/system")
    if not data:
        st.error("无法获取系统数据")
        return
    
    # CPU
    st.subheader("🔧 CPU")
    cpu = data.get("cpu", {})
    col1, col2 = st.columns(2)
    col1.metric("平均使用率", f"{cpu.get('usage', 0):.1f}%")
    col2.metric("核心数", len(cpu.get("cores", [])))
    
    cores = cpu.get("cores", [])
    if cores:
        ccols = st.columns(len(cores))
        for i, pct in enumerate(cores):
            ccols[i].caption(f"Core {i}: {pct}%")
    
    # Memory
    st.subheader("📦 内存")
    mem = data.get("memory", {})
    mc1, mc2, mc3 = st.columns(3)
    mc1.metric("总量", f"{mem.get('total', 0) / 1e9:.1f} GB")
    mc2.metric("已用", f"{mem.get('used', 0) / 1e9:.1f} GB")
    mc3.metric("使用率", f"{mem.get('percent', 0):.1f}%")
    
    # Disk
    st.subheader("💿 磁盘")
    disk = data.get("disk", {})
    dc1, dc2, dc3 = st.columns(3)
    dc1.metric("总量", f"{disk.get('total', 0) / 1e9:.1f} GB")
    dc2.metric("已用", f"{disk.get('used', 0) / 1e9:.1f} GB")
    dc3.metric("使用率", f"{disk.get('percent', 0):.1f}%")
    
    # Token 消耗（暂用时间代替）
    st.caption(f"⏰ 数据更新: {datetime.now().strftime('%H:%M:%S')}")