"""Mission Control Backend — FastAPI 入口

模块化重构后的主入口，仅负责：
1. FastAPI 应用初始化
2. CORS 中间件
3. 路由注册
4. 表创建（启动时）

核心业务逻辑已拆分到 routers/ 和 services/
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.models import Base
from app.logging_config import setup_logging
from app.routers import (
    stories_router,
    projects_router,
    agents_router,
    cron_router,
    health_router,
    skills_router,
    system_router,
)

# 创建数据库表（如果不存在）
setup_logging()

Base.metadata.create_all(bind=engine)

# FastAPI 应用
app = FastAPI(
    title="OpenClaw Mission Control API",
    version="1.0.0"
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 根端点
@app.get("/")
def root():
    return {"message": "OpenClaw Mission Control API", "version": "1.0.0"}


# 注册路由
app.include_router(projects_router)
app.include_router(stories_router)
app.include_router(agents_router)
app.include_router(cron_router)
app.include_router(health_router)
app.include_router(skills_router)
app.include_router(system_router)


# 启动事件
@app.on_event("startup")
async def startup():
    from app.logging_config import get_logger
    logger = get_logger("main")
    logger.info("Mission Control Backend started")


# 关闭事件
@app.on_event("shutdown")
async def shutdown():
    from app.logging_config import get_logger
    logger = get_logger("main")
    logger.info("Mission Control Backend stopped")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
