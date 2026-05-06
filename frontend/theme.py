"""theme.py — Vercel Design System CSS 主题"""

DARK_CSS = """
<style>
/* ─── Foundation: Vercel Dark ─── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }

.stApp {
    background-color: #000000;
}

/* ─── Typography ─── */
h1, h2, h3, h4, h5, h6 {
    color: #fafafa !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em !important;
}
h1 { font-size: 2rem !important; margin-bottom: 0.25rem !important; }
h2 { font-size: 1.5rem !important; }
h3 { font-size: 1.25rem !important; }
p, label, span, div, li { color: #eaeaea !important; }
.stCaption { color: #888 !important; }

/* ─── Code blocks ─── */
code {
    background: #1a1a1a !important;
    border: 1px solid #222 !important;
    border-radius: 4px !important;
    padding: 2px 6px !important;
    color: #eaeaea !important;
    font-family: 'SF Mono', 'Fira Code', monospace !important;
}
.stCodeBlock {
    background: #0a0a0a !important;
    border: 1px solid #222 !important;
    border-radius: 6px !important;
}

/* ─── Sidebar ─── */
[data-testid="stSidebar"] {
    background: #050505 !important;
    border-right: 1px solid #1a1a1a !important;
}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
[data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
    color: #fafafa !important;
}
[data-testid="stSidebar"] .stRadio label span {
    color: #aaa !important;
}

/* ─── Containers / Cards ─── */
.stContainer, [data-testid="stExpander"] {
    border: 1px solid #1a1a1a !important;
    border-radius: 6px !important;
    padding: 20px !important;
    margin: 8px 0 !important;
    background: #050505 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.5) !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
}
.stContainer:hover, [data-testid="stExpander"]:hover {
    border-color: #333 !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.6) !important;
}
[data-testid="stExpander"] summary {
    color: #fafafa !important;
}

/* ─── Metrics ─── */
[data-testid="stMetric"] {
    background: transparent !important;
}
[data-testid="stMetric"] label {
    color: #888 !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    font-weight: 500 !important;
}
[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    color: #fafafa !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
}

/* ─── Buttons ─── */
.stButton button {
    border-radius: 6px !important;
    border: 1px solid #333 !important;
    background: #0a0a0a !important;
    color: #fafafa !important;
    font-size: 0.8125rem !important;
    font-weight: 500 !important;
    padding: 6px 14px !important;
    transition: all 0.15s ease !important;
    box-shadow: none !important;
}
.stButton button:hover {
    border-color: #555 !important;
    background: #111 !important;
    color: #fff !important;
}
.stButton button[kind="primary"] {
    background: #0070f3 !important;
    border-color: #0070f3 !important;
    color: #fff !important;
}
.stButton button[kind="primary"]:hover {
    background: #0761d1 !important;
    border-color: #0761d1 !important;
}

/* ─── Select / Radio / Input ─── */
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: #0a0a0a !important;
    border: 1px solid #333 !important;
    border-radius: 6px !important;
    color: #fafafa !important;
}
.stRadio label {
    color: #aaa !important;
    padding: 4px 0 !important;
    transition: color 0.1s ease !important;
}
.stRadio label:hover { color: #fafafa !important; }

/* ─── Tabs ─── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0 !important;
    border-bottom: 1px solid #1a1a1a !important;
}
.stTabs [data-baseweb="tab"] {
    color: #888 !important;
    font-weight: 500 !important;
    border-bottom: 2px solid transparent !important;
    transition: color 0.15s ease, border-color 0.15s ease !important;
}
.stTabs [data-baseweb="tab"]:hover { color: #fafafa !important; }
.stTabs [aria-selected="true"] {
    color: #fafafa !important;
    border-bottom-color: #fafafa !important;
}

/* ─── Status indicators ─── */
.stSuccess, .stInfo, .stWarning, .stError {
    border-radius: 6px !important;
    border: 1px solid #1a1a1a !important;
    background: #050505 !important;
}
.stSuccess { border-left: 3px solid #0070f3 !important; }
.stError   { border-left: 3px solid #e00 !important; }
.stInfo    { border-left: 3px solid #888 !important; }

/* ─── Dividers ─── */
hr { border-color: #1a1a1a !important; }

/* ─── Scrollbar ─── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #000; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #555; }

/* ─── Expander detail ─── */
.streamlit-expanderHeader { color: #fafafa !important; }
</style>
"""

LIGHT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }

.stApp { background-color: #fafafa; }
h1, h2, h3, h4, h5, h6 { color: #000 !important; font-weight: 600 !important; letter-spacing: -0.02em !important; }
p, label, span, div, li { color: #333 !important; }
.stCaption { color: #666 !important; }
code { background: #f0f0f0 !important; border: 1px solid #e5e5e5 !important; border-radius: 4px !important; padding: 2px 6px !important; color: #333 !important; }
.stCodeBlock { background: #fff !important; border: 1px solid #e5e5e5 !important; border-radius: 6px !important; }
[data-testid="stSidebar"] { background: #fff !important; border-right: 1px solid #e5e5e5 !important; }
.stContainer, [data-testid="stExpander"] {
    border: 1px solid #e5e5e5 !important; border-radius: 6px !important; padding: 20px !important;
    margin: 8px 0 !important; background: #fff !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
}
.stContainer:hover, [data-testid="stExpander"]:hover {
    border-color: #d0d0d0 !important; box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
}
[data-testid="stExpander"] summary { color: #000 !important; }
[data-testid="stMetric"] label { color: #888 !important; font-size: 0.75rem !important; text-transform: uppercase !important; letter-spacing: 0.05em !important; }
[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #000 !important; font-size: 1.5rem !important; font-weight: 700 !important; }
.stButton button {
    border-radius: 6px !important; border: 1px solid #d5d5d5 !important; background: #fff !important;
    color: #000 !important; font-size: 0.8125rem !important; font-weight: 500 !important;
    padding: 6px 14px !important; transition: all 0.15s ease !important;
}
.stButton button:hover { border-color: #aaa !important; background: #f5f5f5 !important; }
.stButton button[kind="primary"] { background: #0070f3 !important; border-color: #0070f3 !important; color: #fff !important; }
.stButton button[kind="primary"]:hover { background: #0761d1 !important; }
[data-testid="stSelectbox"] div[data-baseweb="select"] > div { background: #fff !important; border: 1px solid #d5d5d5 !important; border-radius: 6px !important; }
.stTabs [data-baseweb="tab-list"] { border-bottom: 1px solid #e5e5e5 !important; }
.stTabs [data-baseweb="tab"] { color: #888 !important; }
.stTabs [data-baseweb="tab"]:hover { color: #000 !important; }
.stTabs [aria-selected="true"] { color: #000 !important; border-bottom-color: #000 !important; }
.stSuccess, .stInfo, .stWarning, .stError { border-radius: 6px !important; border: 1px solid #e5e5e5 !important; background: #fff !important; }
.stSuccess { border-left: 3px solid #0070f3 !important; }
hr { border-color: #e5e5e5 !important; }
.streamlit-expanderHeader { color: #000 !important; }
</style>
"""


def apply_theme(st):
    """应用当前主题 CSS"""
    import streamlit as st_mod
    if st.session_state.dark_mode:
        st_mod.markdown(DARK_CSS, unsafe_allow_html=True)
    else:
        st_mod.markdown(LIGHT_CSS, unsafe_allow_html=True)