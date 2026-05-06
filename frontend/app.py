import streamlit as st
from datetime import datetime
from theme import apply_theme
from api_client import api_get
import components

# ── 主题状态 ──
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

apply_theme(st)

st.set_page_config(
    page_title="🦀 Mission Control",
    page_icon="🦀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── 侧边栏 ──
st.sidebar.title("🦀 Mission Control")

col_t1, col_t2 = st.sidebar.columns([1, 1])
label = "🌙 暗色" if st.session_state.dark_mode else "☀️ 亮色"
if col_t2.button(f"切换{label}", use_container_width=True, key="theme_toggle"):
    st.session_state.dark_mode = not st.session_state.dark_mode
    st.rerun()

st.sidebar.markdown("---")

refresh_map = {"5 秒": 5, "10 秒": 10, "30 秒": 30, "60 秒": 60, "手动": 0}
refresh_label = st.sidebar.selectbox("🔄 刷新间隔", list(refresh_map.keys()), index=1)
refresh_sec = refresh_map[refresh_label]

if refresh_sec == 0:
    if st.sidebar.button("🔃 手动刷新", use_container_width=True, key="manual_refresh"):
        st.cache_data.clear()
        st.rerun()

st.sidebar.markdown("---")
module = st.sidebar.radio(
    "导航",
    ["📋 任务看板", "🤖 Agent 状态", "⏰ Cron 任务", "💓 Healthcheck", "🧠 Skills", "💻 系统资源"]
)

# ── 主内容区 ──
st.title("🦀 OpenClaw Mission Control")

# 状态栏
health = api_get("/")
if not health:
    st.error("🔴 后端未连接")
    st.stop()

stories_data = api_get("/stories") or []
todo_count = len([s for s in stories_data if not s.get("passes")])
done_count = len([s for s in stories_data if s.get("passes")])

cols = st.columns(4)
cols[0].success("🟢 后端连接正常")
cols[1].info(f"📥 {todo_count} 待办")
cols[2].info(f"✅ {done_count} 完成")
cols[3].caption(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
st.markdown("---")

# ── 模块路由 ──
if "任务看板" in module:
    components.render_kanban(stories_data)
elif "Agent" in module:
    components.render_agents()
elif "Cron" in module:
    components.render_cron()
elif "Healthcheck" in module:
    components.render_healthcheck()
elif "Skills" in module:
    components.render_skills()
elif "系统资源" in module:
    components.render_system()