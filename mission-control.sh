#!/bin/bash
# Mission Control CLI Launcher
# Usage: ./mission-control.sh [--port PORT] [--no-browser] [--docker]

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 默认配置
PORT=8501
BACKEND_PORT=8000
NO_BROWSER=false
USE_DOCKER=false

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --port)
            PORT="$2"
            BACKEND_PORT=$((PORT + 1000))
            shift 2
            ;;
        --no-browser)
            NO_BROWSER=true
            shift
            ;;
        --docker)
            USE_DOCKER=true
            shift
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

if [ "$USE_DOCKER" = true ]; then
    echo "🐳 使用 Docker 启动..."
    docker-compose up -d
    echo "✅ Mission Control 启动完成"
    echo "   前端: http://localhost:$PORT"
    echo "   后端: http://localhost:$BACKEND_PORT"
    exit 0
fi

# 启动后端
echo "🚀 启动后端 (端口 $BACKEND_PORT)..."
cd "$SCRIPT_DIR/backend"
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port $BACKEND_PORT &
BACKEND_PID=$!

sleep 3

# 启动前端
echo "🎨 启动前端 (端口 $PORT)..."
cd "$SCRIPT_DIR/frontend"
if [ "$NO_BROWSER" = true ]; then
    streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true &
else
    streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 &
fi

echo "✅ Mission Control 启动完成"
echo "   前端: http://localhost:$PORT"
echo "   后端: http://localhost:$BACKEND_PORT"
echo ""
echo "按 Ctrl+C 停止服务"

# 等待退出
trap "kill $BACKEND_PID 2>/dev/null; pkill -f 'streamlit run'; exit 0" INT
wait
