"""components/kanban.py — 任务看板"""

import streamlit as st
from api_client import api_get, api_post


def render(stories_data):
    """渲染任务看板"""
    st.header("📋 任务看板")
    
    if st.button("🔄 同步项目", key="sync_stories"):
        with st.spinner("同步中..."):
            api_post("/sync/projects")
            st.cache_data.clear()
            st.rerun()
    
    stories = stories_data
    if not stories:
        st.info("暂无项目数据")
        return
    
    # 搜索过滤
    search = st.text_input("🔍 搜索任务", "", key="search_stories")
    project_filter = st.selectbox("📁 项目过滤", ["全部"] + sorted(set(s.get("project_name", "") for s in stories)), key="project_filter")
    
    # 过滤逻辑
    filtered = stories
    if search:
        filtered = [s for s in filtered if search.lower() in s.get("title", "").lower() or search.lower() in s.get("id", "").lower()]
    if project_filter != "全部":
        filtered = [s for s in filtered if s.get("project_name") == project_filter]
    
    todo = [s for s in filtered if not s.get("passes")]
    done = [s for s in filtered if s.get("passes")]
    
    # 详情展开
    selected = st.session_state.get('selected_story')
    if selected:
        with st.expander(f"📋 {selected['id']}: {selected.get('title')}", expanded=True):
            c1, c2 = st.columns(2)
            c1.metric("项目", selected.get('project_name'))
            c1.metric("优先级", selected.get('priority'))
            c2.metric("状态", "✅ 完成" if selected.get('passes') else "📥 待办")
            c2.metric("迭代", selected.get('actual_iterations', 0))
            st.markdown("---")
            st.markdown(f"**描述:** {selected.get('description', '无')}")
            st.markdown("**验收标准:**")
            for i, ac in enumerate(selected.get('acceptance_criteria', []), 1):
                if isinstance(ac, dict):
                    st.markdown(f"{i}. `{ac.get('id','')}` {ac.get('description','')}")
                else:
                    st.markdown(f"{i}. {ac}")
            
            # 标记完成/取消完成按钮
            if not selected.get('passes'):
                if st.button("✅ 标记完成", type="primary", key="mark_done"):
                    result = api_post(f"/stories/{selected['id']}/status", {"passes": True})
                    if result:
                        st.success(f"Story {selected['id']} 已标记完成")
                        st.cache_data.clear()
                        st.session_state.selected_story = None
                        st.rerun()
            else:
                if st.button("📥 取消完成", key="mark_todo"):
                    result = api_post(f"/stories/{selected['id']}/status", {"passes": False})
                    if result:
                        st.info(f"Story {selected['id']} 已取消完成")
                        st.cache_data.clear()
                        st.session_state.selected_story = None
                        st.rerun()
            
            if st.button("关闭", key="close_story"):
                st.session_state.selected_story = None
                st.rerun()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader(f"📥 待办 ({len(todo)})")
        for s in todo[:20]:
            p = s.get("priority", 5)
            emoji = "🔴" if p == 1 else ("🟡" if p <= 3 else "🟢")
            with st.container(border=True):
                key = f"t_{s['project_id']}_{s['id']}"
                if st.button(f"**{s['id']}** {emoji}", key=key):
                    st.session_state.selected_story = s
                    st.rerun()
                st.caption(f"{s.get('title','')} · {s.get('project_name')}")
    
    with col2:
        st.subheader("🔄 进行中 (0)")
        st.info("开发中...")
    
    with col3:
        st.subheader(f"✅ 完成 ({len(done)})")
        for s in done[:20]:
            with st.container(border=True):
                key = f"d_{s['project_id']}_{s['id']}"
                if st.button(f"**{s['id']}** ✅", key=key):
                    st.session_state.selected_story = s
                    st.rerun()
                st.caption(f"{s.get('title','')} · {s.get('project_name')}")