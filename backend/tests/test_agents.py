"""test_agents.py — Agents API 端点测试"""


class TestAgentsAPI:
    """Agents 相关 API 测试"""

    def test_get_agents(self, client):
        """测试 /agents 返回 Agent 列表"""
        resp = client.get("/agents")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) >= 1  # 至少有降级模拟数据

    def test_agent_has_required_fields(self, client):
        """测试 Agent 数据包含必要字段"""
        resp = client.get("/agents")
        data = resp.json()
        for agent in data:
            assert "agent_id" in agent
            assert "status" in agent
            assert "model" in agent

    def test_agent_status_values(self, client):
        """测试 Agent status 字段"""
        resp = client.get("/agents")
        data = resp.json()
        for agent in data:
            assert agent["status"] in ["running", "idle", "offline", "unknown"]