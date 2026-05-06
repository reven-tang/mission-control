"""components/skills.py — Skills 生态系统"""

import streamlit as st
from api_client import api_get


def render():
    """渲染 Skills 面板"""
    st.header("🧠 Skills 生态系统")
    
    skills_data = api_get("/skills")
    if not skills_data:
        st.info("暂无 Skills 数据")
        return
    
    col1, col2, col3 = st.columns(3)
    col1.metric("总 Skills", skills_data.get("total"))
    col2.metric("Graph 节点", skills_data.get("graph_nodes"))
    col3.metric("Graph 边", skills_data.get("graph_edges"))
    
    recent = skills_data.get("recent", [])
    if recent:
        st.subheader("📌 最近更新")
        for skill in recent:
            name = skill.get("name", "?")
            modified = skill.get("modified", "?")[:19]
            st.markdown(f"- **{name}** · {modified}")
    
    # 评分分级展示
    evaluations = skills_data.get("evaluations", [])
    if evaluations:
        st.subheader("📊 评分分级")
        grade_counts = {"Excellent": 0, "Good": 0, "Fair": 0, "Poor": 0}
        for ev in evaluations:
            grade_counts[ev.get("grade", "Poor")] += 1
        
        g1, g2, g3, g4 = st.columns(4)
        g1.metric("🏆 Excellent (≥90)", grade_counts["Excellent"])
        g2.metric("👍 Good (≥70)", grade_counts["Good"])
        g3.metric("⚠️ Fair (≥55)", grade_counts["Fair"])
        g4.metric("❌ Poor (<55)", grade_counts["Poor"])
        
        # 低分高亮
        poor_skills = [ev for ev in evaluations if ev.get("grade") == "Poor"]
        if poor_skills:
            st.warning(f"⚠️ {len(poor_skills)} 个 Poor 评分技能需要改进：")
            for ps in poor_skills[:5]:
                st.markdown(f"- **{ps['name']}** ({ps['score']}分)")
    
    # Graph 可视化
    graph_data = api_get("/skills/graph")
    if graph_data and graph_data.get("nodes"):
        st.subheader("🔗 Skills Graph")
        
        nodes = graph_data.get("nodes", {})
        edges = graph_data.get("edges", [])
        
        if nodes and edges:
            # 用 pyvis 生成交互力导向图
            try:
                from pyvis.network import Network
                import tempfile
                import os
                
                net = Network(
                    height="500px", width="100%",
                    bgcolor="#0a0a0a" if st.session_state.dark_mode else "#fafafa",
                    font_color="#fafafa" if st.session_state.dark_mode else "#333"
                )
                
                for nid, node in nodes.items():
                    label = node.get("label", nid)
                    net.add_node(nid, label=label, title=label)
                
                for edge in edges:
                    src = edge.get("source")
                    tgt = edge.get("target")
                    if src and tgt:
                        net.add_edge(src, tgt)
                
                net.toggle_physics(True)
                
                with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
                    net.save_graph(f.name)
                    html_path = f.name
                
                html_content = open(html_path).read()
                st.components.v1.html(html_content, height=520)
                os.unlink(html_path)
            except ImportError:
                st.info("安装 pyvis 以查看交互图: `pip install pyvis`")
                
                # 文本模式 fallback
                st.markdown("**节点:** " + ", ".join(n.get("label", k) for k, n in nodes.items()[:10]))
                st.markdown(f"**边数:** {len(edges)}")