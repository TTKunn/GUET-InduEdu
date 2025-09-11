#!/bin/bash

# 用户认证服务启动脚本
# 作者: AI Assistant
# 版本: 1.0.0

set -e  # 遇到错误立即退出

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

log_info "🚀 启动用户认证服务..."
log_debug "工作目录: $SCRIPT_DIR"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    log_error "Python3 未安装或不在PATH中"
    exit 1
fi

log_info "✅ Python3 环境检查通过"

# 检查必要文件
REQUIRED_FILES=("main.py" "config.py" "models.py" "database.py" "auth_service.py" "requirements.txt" ".env")
for file in "${REQUIRED_FILES[@]}"; do
    if [[ ! -f "$file" ]]; then
        log_error "必要文件不存在: $file"
        exit 1
    fi
done

log_info "✅ 必要文件检查通过"

# 检查并安装依赖
log_info "📦 检查Python依赖..."
if [[ -f "requirements.txt" ]]; then
    # 检查是否需要安装依赖
    if ! python3 -c "import fastapi, uvicorn, sqlalchemy, pymysql, pydantic, bcrypt, jwt" &> /dev/null; then
        log_warn "检测到缺少依赖，正在安装..."
        pip3 install --user -r requirements.txt
        if [[ $? -eq 0 ]]; then
            log_info "✅ 依赖安装完成"
        else
            log_error "❌ 依赖安装失败"
            exit 1
        fi
    else
        log_info "✅ 依赖检查通过"
    fi
else
    log_warn "requirements.txt 文件不存在，跳过依赖检查"
fi

# 检查环境配置
log_info "🔧 检查环境配置..."
if [[ -f ".env" ]]; then
    log_info "✅ 环境配置文件存在"
else
    log_error "❌ .env 文件不存在"
    exit 1
fi

# 检查端口是否被占用
PORT=$(grep "API_PORT" .env | cut -d'=' -f2 | tr -d ' ')
if [[ -z "$PORT" ]]; then
    PORT=8007
fi

log_debug "检查端口: $PORT"
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    log_warn "端口 $PORT 已被占用，尝试停止现有进程..."
    # 尝试优雅停止
    PID=$(lsof -Pi :$PORT -sTCP:LISTEN -t)
    if [[ -n "$PID" ]]; then
        kill -TERM $PID 2>/dev/null || true
        sleep 2
        # 如果还在运行，强制停止
        if kill -0 $PID 2>/dev/null; then
            kill -KILL $PID 2>/dev/null || true
            log_warn "强制停止了进程 $PID"
        fi
    fi
fi

# 启动服务
log_info "🎯 启动用户认证服务..."
log_info "服务地址: http://0.0.0.0:$PORT"
log_info "API文档: http://0.0.0.0:$PORT/docs"
log_info "健康检查: http://0.0.0.0:$PORT/health"
log_info ""
log_info "按 Ctrl+C 停止服务"
log_info "=================================="

# 启动应用
exec python3 main.py
