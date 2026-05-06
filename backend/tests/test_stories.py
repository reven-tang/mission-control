"""test_stories.py — Stories API 端点测试"""

import json
from pathlib import Path


class TestStoriesAPI:
    """Stories 相关 API 测试"""

    def test_root_endpoint(self, client):
        """测试 / 根端点"""
        resp = client.get("/")
        assert resp.status_code == 200
        data = resp.json()
        assert "message" in data
        assert "version" in data
        assert data["version"] == "1.0.0"

    def test_get_stories_empty(self, client):
        """测试空 DB 时 /stories 返回空列表"""
        resp = client.get("/stories")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_sync_projects(self, client, sample_prd):
        """测试 /sync/projects 同步"""
        resp = client.post("/sync/projects")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "synced"

    def test_get_projects_empty(self, client):
        """测试空 DB 时 /projects 返回空列表"""
        resp = client.get("/projects")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_get_stories_with_filter(self, client):
        """测试 /stories?status=todo 过滤"""
        resp = client.get("/stories?status=todo")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

    def test_get_stories_with_project_filter(self, client):
        """测试 /stories?project=gtap 过滤"""
        resp = client.get("/stories?project=gtap")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

    def test_get_story_not_found(self, client):
        """测试 /stories/{id} 返回 404"""
        resp = client.get("/stories/US-NONEXIST")
        assert resp.status_code == 404