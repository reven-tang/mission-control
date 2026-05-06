"""test_system.py — System & Cron & Healthcheck & Skills API 测试"""


class TestSystemAPI:
    """系统资源 API 测试"""

    def test_get_system_stats(self, client):
        """测试 /system 返回系统资源数据"""
        resp = client.get("/system")
        assert resp.status_code == 200
        data = resp.json()
        assert "cpu" in data
        assert "memory" in data
        assert "disk" in data
        assert "usage" in data["cpu"]
        assert "percent" in data["memory"]
        assert "percent" in data["disk"]

    def test_cpu_usage_range(self, client):
        """测试 CPU 使用率范围"""
        resp = client.get("/system")
        data = resp.json()
        assert 0 <= data["cpu"]["usage"] <= 100

    def test_memory_percent_range(self, client):
        """测试内存使用率范围"""
        resp = client.get("/system")
        data = resp.json()
        assert 0 <= data["memory"]["percent"] <= 100

    def test_disk_percent_range(self, client):
        """测试磁盘使用率范围"""
        resp = client.get("/system")
        data = resp.json()
        assert 0 <= data["disk"]["percent"] <= 100


class TestCronAPI:
    """Cron 任务 API 测试"""

    def test_get_cron_jobs(self, client):
        """测试 /cron 返回任务列表"""
        resp = client.get("/cron")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_cron_job_has_required_fields(self, client):
        """测试 Cron 任务包含必要字段"""
        resp = client.get("/cron")
        data = resp.json()
        for job in data:
            assert "name" in job
            assert "schedule" in job


class TestHealthcheckAPI:
    """Healthcheck API 测试"""

    def test_get_healthcheck(self, client):
        """测试 /healthcheck 返回状态"""
        resp = client.get("/healthcheck")
        assert resp.status_code == 200
        data = resp.json()
        assert "last_run" in data
        assert "status" in data
        assert "checks" in data

    def test_healthcheck_checks_fields(self, client):
        """测试 Healthcheck checks 包含必要字段"""
        resp = client.get("/healthcheck")
        data = resp.json()
        checks = data.get("checks", {})
        assert "brain_files" in checks
        assert "skills" in checks

    def test_get_healthcheck_runs(self, client):
        """测试 /healthcheck/runs 返回历史"""
        resp = client.get("/healthcheck/runs")
        assert resp.status_code == 200
        data = resp.json()
        assert "runs" in data


class TestSkillsAPI:
    """Skills API 测试"""

    def test_get_skills(self, client):
        """测试 /skills 返回 Skills 数据"""
        resp = client.get("/skills")
        assert resp.status_code == 200
        data = resp.json()
        assert "total" in data
        assert "graph_nodes" in data
        assert "graph_edges" in data

    def test_skills_graph_endpoint(self, client):
        """测试 /skills/graph 返回图谱数据"""
        resp = client.get("/skills/graph")
        assert resp.status_code == 200
        data = resp.json()
        assert "nodes" in data
        assert "edges" in data