# 🦀 Mission Control

**OpenClaw 统一管理控制台** — 实时查看 Agent 状态、管理任务看板、监控 Skills 生态系统和系统资源的 Web 面板。

## 功能

| 模块 | 功能 |
|------|------|
| 📋 任务看板 | 三列看板（待办/进行中/完成），支持搜索过滤、项目筛选、一键同步 |
| 🤖 Agent 状态 | 实时展示活跃 Agent 的 ID、状态、模型、渠道和最近活动 |
| ⏰ Cron 任务 | 定时任务监控：Heartbeat / Dreaming / Brain Healthcheck |
| 💓 Healthcheck | Brain 健康检查面板，支持手动触发和历史记录查看 |
| 🧠 Skills | Skills 生态系统总览：数量/图节点/评分分级（Excellent/Good/Fair/Poor） |
| 💻 系统资源 | CPU / 内存 / 磁盘使用率实时监控 |

### ✨ 特色功能

- **双向任务同步**：看板"标记完成" → DB 更新 → 自动回写 `prd.json`
- **Skills 评分展示**：四色分级 + Poor 技能高亮警告
- **Vercel Design System**：暗色/亮色双主题（默认亮色），专业级 UI
- **交互式 Graph**：支持 pyvis 力导向图可视化 Skills 关联
- **Docker 部署**：docker-compose 一键启动前后端

## 架构

```
mission-control/
├── backend/                 # FastAPI 后端
│   └── app/
│       ├── main.py          # 入口（75行）
│       ├── database.py      # 数据库配置
│       ├── models.py        # Project / Story 模型
│       ├── logging_config.py
│       ├── routers/         # 7 个路由模块
│       └── services/        # 3 个服务模块
├── frontend/                # Streamlit 前端
│   ├── app.py               # 入口（77行）
│   ├── theme.py             # Vercel DS 主题
│   ├── api_client.py        # API 客户端
│   └── components/          # 6 个页面组件
├── docker-compose.yml       # 一键部署
├── Dockerfile.backend
├── Dockerfile.frontend
└── mission-control.sh       # CLI 启动器
```

## 快速开始

### 本地启动

```bash
./mission-control.sh
```

### Docker 部署

```bash
./mission-control.sh --docker
```

### 参数

```bash
./mission-control.sh --port 8080    # 自定义端口（默认 8501）
./mission-control.sh --no-browser   # 不自动打开浏览器
./mission-control.sh --docker       # 使用 Docker 启动
```

启动后访问：**http://localhost:8501**

## 技术栈

| 层 | 技术 |
|------|------|
| 后端 | FastAPI + SQLAlchemy + SQLite |
| 前端 | Streamlit + Pyvis |
| 设计 | Vercel Design System（默认亮色/暗色可切换） |
| 部署 | Docker + docker-compose |
| CLI | Bash 一键启动脚本 |

## 依赖

- Python ≥ 3.9
- 后端：FastAPI, uvicorn, SQLAlchemy, psutil
- 前端：Streamlit, requests
- 可选：pyvis（Skills Graph 交互可视化）

## License

MIT
