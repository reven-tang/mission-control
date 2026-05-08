#!/bin/bash
# Mission Control 启动脚本

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

# 检查并创建 venv
if [ ! -d "$BACKEND_DIR/venv" ]; then
    echo "创建后端虚拟环境..."
    python3 -m venv "$BACKEND_DIR/venv"
fi

# 激活 venv 并安装依赖
echo "安装依赖..."
source "$BACKEND_DIR/venv/bin/activate"
pip install -q fastapi uvicorn sqlalchemy psutil pydantic requests streamlit

# 后台启动后端
echo "启动后端服务..."
cd "$BACKEND_DIR"
nohup python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/mission-control-backend.log 2>&1 &
BACKEND_PID=$!

echo "后端 PID: $BACKEND_PID"

# 等待后端启动
sleep 3

# 后台启动前端
echo "启动前端服务..."
cd "$FRONTEND_DIR"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -q streamlit requests psutil
nohup streamlit run app.py --server.port 8501 --server.headless true > /tmp/mission-control-frontend.log 2>&1 &
FRONTEND_PID=$!

echo "🎉 Mission Control 启动完成!"
echo "后端: http://localhost:8000 (PID: $BACKEND_PID)"
echo "前端: http://localhost:8501 (PID: $FRONTEND_PID)"
echo ""
echo "按 Ctrl+C 停止服务"

# 捕获退出信号
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT

# 保持运行
wait
