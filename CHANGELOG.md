# Mission Control — CHANGELOG

## v2.2.0 (2026-05-09)

### 新增
- **萨莉 OS 系统健康仪表盘**：新增三系统综合健康监控
  - 🧠 记忆系统：页面数、链接数、Hub页、lint问题、搜索分
  - 🔗 技能系统：合规率、超标数、图密度(当前/基线)、退役候选
  - 🔁 自闭环系统：gate-check通过率、复利覆盖率、活跃项目
  - 📊 综合评分：三系统加权总分 (记忆25%/技能35%/自闭环40%)

### 新增文件
- `backend/app/services/health_aggregator.py` — 三系统健康数据聚合服务
- `frontend/components/health_dashboard.py` — 仪表盘组件
- `openspec/changes/mission-control/proposal-phase4.md` — SPEC 文档
- `openspec/changes/mission-control/design-phase4.md` — 设计文档
- `openspec/changes/mission-control/tasks-phase4.md` — 任务清单

### 修改文件
- `backend/app/routers/system.py` — 新增 `/system/health` 和 `/system/health/summary`
- `frontend/app.py` — 侧栏新增「🦀 系统健康」入口
- `frontend/components/__init__.py` — 注册 health_dashboard 组件

### 验证
- 9/9 pytest 通过，覆盖率 88%
- 浏览器验证 0 console error
- gate-check BUILD + QA 门禁通过

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
