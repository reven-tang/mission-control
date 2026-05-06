"""api_client.py — 统一 API 请求封装"""

import requests
import streamlit as st

API_BASE = "http://localhost:8000"


@st.cache_data(ttl=5)
def api_get(endpoint: str):
    """GET 请求，带缓存"""
    try:
        resp = requests.get(f"{API_BASE}{endpoint}", timeout=5)
        return resp.json()
    except Exception:
        return None


def api_post(endpoint: str, data=None):
    """POST 请求，无缓存"""
    try:
        resp = requests.post(f"{API_BASE}{endpoint}", json=data, timeout=10)
        return resp.json()
    except Exception:
        return None