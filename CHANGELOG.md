# Mission Control — CHANGELOG

## v2.0.0 (2026-05-06)

### 新增
- Docker 化部署：Dockerfile.backend + Dockerfile.frontend + docker-compose.yml
- CLI 启动器：mission-control.sh（支持 --port/--no-browser/--docker 参数）

## v1.5.0 (2026-05-06)

### 新增
- 任务状态双向同步：前端"标记完成"按钮 → POST /stories/{id}/status → 回写 prd.json
- Skills 评分展示：四级分类（Excellent/Good/Fair/Poor）+ Poor 高亮警告
- 搜索过滤：看板支持关键词搜索 + 项目下拉过滤

## v1.4.0 (2026-05-06)

### 重构
- 后端模块拆分：main.py 412→75 行，拆为 database/models/routers(7)/services(3)
- 前端组件拆分：app.py 535→77 行，拆为 theme/api_client/components(6)

## v1.3.0 (2026-05-06)

### 新增
- 补齐 SPEC 三文件（proposal.md / design.md / tasks.md），spec quality 86.5/100
- 添加后端测试（16 pytest tests），覆盖 stories/agents/system/cron/healthcheck/skills API
- 创建 gate-check-mission-control.py，接入自闭环系统
- 添加 ROADMAP.md + CHANGELOG.md

### 修复
- gate-check.py NameError: `PROJECT_ROOT` → `project_root`（第186行）

## v1.2.0 (2026-05-04)

### 新增
- Cron 任务详情展开（Expander 组件）
- Healthcheck 详情展开
- Skills Graph pyvis 力导向图可视化
- Vercel Design System 暗色主题完整 CSS

## v1.1.0 (2026-05-04)

### 新增
- 接入真实 Agent 状态（sessions_list API）
- 侧边栏刷新间隔选择（5s/10s/30s/手动）
- 暗色/亮色主题切换

## v1.0.0 (2026-05-04)

### 新增
- 项目基础结构（Streamlit 前端 + FastAPI 后端 + SQLite）
- 6 个核心模块：任务看板、Agent 状态、Cron、Healthcheck、Skills、系统资源
- 启动脚本 start.sh