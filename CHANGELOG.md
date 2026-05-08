# Mission Control — CHANGELOG

## v2.1.0 (2026-05-08)

### 修复
- **start.sh 前端启动缺失**：原脚本只安装前端依赖未执行 `streamlit run`，现已补上后台启动命令 + PID 管理
- **默认主题改为亮色**：首次打开默认使用亮色主题（`dark_mode = False`）

### 文档更新
- README 更新主题描述为「默认亮色/暗色可切换」

## v1.0.0 (2026-05-06)

### 首次发布
- 后端：FastAPI + SQLAlchemy + SQLite，模块化结构（routers/ + services/）
- 前端：Streamlit + Vercel Design System 暗色主题，组件化（6 个页面组件）
- 任务看板：三列布局 + 搜索过滤 + 项目筛选 + 双向状态同步
- Agent 状态：实时展示活跃 Agent 的 ID、模型、渠道、最近活动
- Cron 任务：Heartbeat / Dreaming / Brain Healthcheck 监控
- Healthcheck：Brain 健康检查面板 + 手动触发 + 历史记录
- Skills：总数/图节点/评分分级（Excellent/Good/Fair/Poor）+ pyvis 力导向图
- 系统资源：CPU / 内存 / 磁盘使用率实时监控
- 部署：Docker + docker-compose + CLI 启动器（mission-control.sh）
- 代码优化：后端入口 75 行，前端入口 77 行
