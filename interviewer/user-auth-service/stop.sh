#!/bin/bash

# 用户认证服务停止脚本
# 作者: AI Assistant
# 版本: 1.0.0

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_debug() {
    echo -e "${BLUE}[DEBUG]${NC} $1"
}

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

log_info "🛑 停止用户认证服务..."

# 从配置文件获取端口
PORT=8007
if [[ -f ".env" ]]; then
    ENV_PORT=$(grep "API_PORT" .env | cut -d'=' -f2 | tr -d ' ')
    if [[ -n "$ENV_PORT" ]]; then
        PORT=$ENV_PORT
    fi
fi

log_debug "检查端口: $PORT"

# 查找运行在指定端口的进程
PID=$(lsof -Pi :$PORT -sTCP:LISTEN -t 2>/dev/null)

if [[ -z "$PID" ]]; then
    log_info "✅ 没有发现运行在端口 $PORT 的服务"
    exit 0
fi

log_info "发现进程 PID: $PID"

# 尝试优雅停止
log_info "尝试优雅停止服务..."
kill -TERM $PID 2>/dev/null

# 等待进程停止
for i in {1..10}; do
    if ! kill -0 $PID 2>/dev/null; then
        log_info "✅ 服务已成功停止"
        exit 0
    fi
    log_debug "等待进程停止... ($i/10)"
    sleep 1
done

# 如果优雅停止失败，强制停止
log_warn "优雅停止失败，强制停止服务..."
kill -KILL $PID 2>/dev/null

# 再次检查
if ! kill -0 $PID 2>/dev/null; then
    log_info "✅ 服务已强制停止"
else
    log_error "❌ 无法停止服务"
    exit 1
fi
