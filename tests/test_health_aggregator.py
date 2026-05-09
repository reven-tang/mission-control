"""tests/test_health_aggregator.py — HealthAggregator 单元测试"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend" / "app" / "services"))

from health_aggregator import (
    HealthAggregator,
    MemoryHealth,
    SkillsHealth,
    SelfLoopHealth
)


class TestHealthAggregator:
    """HealthAggregator 测试"""
    
    def setup_method(self):
        """每个测试前重置"""
        self.aggregator = HealthAggregator()
        self.aggregator.cache = {}
        self.aggregator.cache_time = None
    
    def test_memory_health_structure(self):
        """测试 MemoryHealth 数据结构"""
        health = MemoryHealth(
            score=78,
            pages=46,
            links=190,
            typed_links=179,
            hub_pages=12,
            lint_issues=0,
            last_compile="2026-05-09 10:00"
        )
        assert health.score == 78
        assert health.pages == 46
        assert health.links == 190
        assert health.lint_issues == 0
    
    def test_skills_health_structure(self):
        """测试 SkillsHealth 数据结构"""
        health = SkillsHealth(
            score=82,
            total=144,
            compliant=144,
            over_limit=0,
            graph_density=3.45,
            density_baseline=3.50,
            retirement_candidates=5
        )
        assert health.score == 82
        assert health.total == 144
        assert health.over_limit == 0
        assert health.graph_density < health.density_baseline
    
    def test_self_loop_health_structure(self):
        """测试 SelfLoopHealth 数据结构"""
        health = SelfLoopHealth(
            score=85,
            gate_check_pass_rate=95,
            compound_coverage=85,
            active_projects=3
        )
        assert health.score == 85
        assert health.gate_check_pass_rate == 95
        assert health.active_projects == 3
    
    @patch('health_aggregator.subprocess.run')
    def test_get_memory_health_mocked(self, mock_run):
        """测试 get_memory_health (mocked)"""
        # Mock brain-healthcheck.sh 输出
        mock_run.return_value = Mock(
            stdout="页面数: 50\n链接关系: 200\nHub 页面: 15",
            stderr="",
            returncode=0
        )
        
        health = self.aggregator.get_memory_health()
        
        assert health.pages == 50
        assert health.links == 200
        assert health.hub_pages == 15
        assert health.score > 0
    
    @patch('health_aggregator.subprocess.run')
    def test_get_skills_health_mocked(self, mock_run):
        """测试 get_skills_health (mocked)"""
        health = self.aggregator.get_skills_health()
        
        assert health.total > 0
        assert health.compliant >= 0
        assert health.over_limit >= 0
        assert 0 <= health.score <= 100
    
    @patch('health_aggregator.subprocess.run')
    def test_get_self_loop_health_mocked(self, mock_run):
        """测试 get_self_loop_health (mocked)"""
        health = self.aggregator.get_self_loop_health()
        
        assert health.active_projects >= 0
        assert 0 <= health.compound_coverage <= 100
        assert 0 <= health.score <= 100
    
    def test_get_full_health_caching(self):
        """测试缓存机制"""
        # First call - no cache
        with patch.object(self.aggregator, 'get_memory_health') as mock_mem, \
             patch.object(self.aggregator, 'get_skills_health') as mock_skills, \
             patch.object(self.aggregator, 'get_self_loop_health') as mock_loop:
            
            mock_mem.return_value = MemoryHealth(78, 46, 190, 179, 12, 0, "now")
            mock_skills.return_value = SkillsHealth(82, 144, 144, 0, 3.45, 3.50, 5)
            mock_loop.return_value = SelfLoopHealth(85, 95, 85, 3)
            
            result1 = self.aggregator.get_full_health()
            
            # Verify overall score calculation
            expected = int(78 * 0.25 + 82 * 0.35 + 85 * 0.40)
            assert result1["overall_score"] == expected
            
            # Second call - should use cache
            result2 = self.aggregator.get_full_health()
            assert result1 == result2
            
            # Methods should only be called once (cached)
            mock_mem.assert_called_once()
    
    def test_get_summary(self):
        """测试 get_summary"""
        with patch.object(self.aggregator, 'get_full_health') as mock_full:
            mock_full.return_value = {
                "overall_score": 90,
                "timestamp": "2026-05-09T10:00:00"
            }
            
            summary = self.aggregator.get_summary()
            
            assert summary["overall_score"] == 90
            assert summary["status"] == "healthy"
            assert "last_update" in summary
    
    def test_overall_score_calculation(self):
        """测试综合分数计算"""
        # Test weighted calculation
        # Memory: 80 * 0.25 = 20
        # Skills: 80 * 0.35 = 28
        # Self-loop: 80 * 0.40 = 32
        # Total: 80
        
        with patch.object(self.aggregator, 'get_memory_health') as mock_mem, \
             patch.object(self.aggregator, 'get_skills_health') as mock_skills, \
             patch.object(self.aggregator, 'get_self_loop_health') as mock_loop:
            
            mock_mem.return_value = MemoryHealth(80, 50, 200, 180, 15, 0, "now")
            mock_skills.return_value = SkillsHealth(80, 150, 150, 0, 3.5, 3.5, 0)
            mock_loop.return_value = SelfLoopHealth(80, 90, 80, 5)
            
            result = self.aggregator.get_full_health()
            
            expected = int(80 * 0.25 + 80 * 0.35 + 80 * 0.40)
            assert result["overall_score"] == expected == 80


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "--tb=short"])