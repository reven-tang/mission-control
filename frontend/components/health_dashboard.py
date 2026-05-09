"""components/health_dashboard.py — 萨莉 OS 系统健康仪表盘"""

import streamlit as st
from api_client import api_get
from datetime import datetime


def render_memory_card(data: dict):
    """渲染记忆系统卡片"""
    st.subheader("🧠 记忆系统")
    
    # 分数大数字
    score = data.get("score", 0)
    color = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
    st.metric(f"{color} 健康度", f"{score}/100")
    
    # 关键指标
    c1, c2 = st.columns(2)
    with c1:
        st.caption(f"📄 页面: {data.get('pages', 0)}")
        st.caption(f"🔗 链接: {data.get('links', 0)}")
    with c2:
        st.caption(f"📌 Hub: {data.get('hub_pages', 0)}")
        st.caption(f"⚠️ Lint: {data.get('lint_issues', 0)}")
    
    st.caption(f"🕐 编译: {data.get('last_compile', '?')}")


def render_skills_card(data: dict):
    """渲染技能系统卡片"""
    st.subheader("🔗 技能系统")
    
    score = data.get("score", 0)
    color = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
    st.metric(f"{color} 健康度", f"{score}/100")
    
    c1, c2 = st.columns(2)
    with c1:
        total = data.get("total", 0)
        compliant = data.get("compliant", 0)
        st.caption(f"📦 技能: {compliant}/{total}")
        st.caption(f"✅ 合规: {compliant} ({int(compliant/total*100) if total else 0}%)")
    with c2:
        density = data.get("graph_density", 0)
        baseline = data.get("density_baseline", 0)
        delta = density - baseline
        st.caption(f"📊 密度: {density:.2f}%")
        st.caption(f"Δ 基线: {delta:+.2f}%")
    
    over = data.get("over_limit", 0)
    if over > 0:
        st.warning(f"⚠️ {over} 个技能超标 (>100行)")
    
    retire = data.get("retirement_candidates", 0)
    if retire > 0:
        st.info(f"ℹ️ {retire} 个退役候选")


def render_self_loop_card(data: dict):
    """渲染 AI 自闭环卡片"""
    st.subheader("🔁 自闭环系统")
    
    score = data.get("score", 0)
    color = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
    st.metric(f"{color} 健康度", f"{score}/100")
    
    c1, c2 = st.columns(2)
    with c1:
        gate = data.get("gate_check_pass_rate", 0)
        st.caption(f"🚪 Gate通过率: {gate}%")
        compound = data.get("compound_coverage", 0)
        st.caption(f"📝 复利覆盖: {compound}%")
    with c2:
        active = data.get("active_projects", 0)
        st.caption(f"📂 活跃项目: {active}")
    
    if gate < 90:
        st.warning(f"⚠️ Gate-check 通过率偏低")


def render():
    """渲染系统健康仪表盘"""
    st.header("🦀 萨莉 OS 系统健康")
    
    # 获取数据
    data = api_get("/system/health")
    if not data:
        st.error("❌ 无法获取健康数据")
        return
    
    # 综合评分大数字
    overall = data.get("overall_score", 0)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        status_color = "🟢" if overall >= 80 else "🟡" if overall >= 60 else "🔴"
        st.metric(
            f"{status_color} 综合健康度",
            f"{overall}/100",
            delta="P0-P2 修复后",
            delta_color="normal"
        )
    
    st.divider()
    
    # 三系统卡片
    systems = data.get("systems", {})
    cols = st.columns(3)
    
    with cols[0]:
        render_memory_card(systems.get("memory", {}))
    
    with cols[1]:
        render_skills_card(systems.get("skills", {}))
    
    with cols[2]:
        render_self_loop_card(systems.get("ai_self_loop", {}))
    
    st.divider()
    
    # 刷新按钮
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 刷新数据", type="primary", use_container_width=True):
            st.rerun()
        
        timestamp = data.get("timestamp", "?")
        st.caption(f"🕐 更新时间: {timestamp[:19] if timestamp != '?' else '?'}")
        st.caption("⏱️ 缓存: 30秒")