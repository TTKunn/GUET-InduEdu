#!/bin/bash

# PDF解析器项目服务管理脚本
# 用于管理PDF解析API和Dify适配器服务

PROJECT_DIR="/home/ubuntu/workspace/project/Document-parser"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查服务状态
check_service() {
    local port=$1
    local service_name=$2
    
    if curl -s http://localhost:$port/health > /dev/null; then
        print_success "$service_name 运行正常 (端口 $port)"
        return 0
    else
        print_error "$service_name 未运行或不健康 (端口 $port)"
        return 1
    fi
}

# 显示服务状态
status() {
    print_info "检查服务状态..."
    echo ""
    
    # 检查全局Milvus
    if curl -s http://localhost:9091/healthz > /dev/null; then
        print_success "全局Milvus数据库运行正常 (端口 19530)"
    else
        print_error "全局Milvus数据库未运行"
    fi
    
    # 检查PDF解析API
    check_service 8002 "PDF解析API"
    
    # 检查Dify适配器
    check_service 8001 "Dify适配器"
    
    echo ""
    print_info "服务访问地址："
    echo "  📄 PDF解析API: http://localhost:8002"
    echo "  📄 PDF解析API文档: http://localhost:8002/docs"
    echo "  🔗 Dify适配器: http://localhost:8001"
    echo "  🔗 Dify适配器文档: http://localhost:8001/docs"
    echo "  🗄️  全局Milvus: localhost:19530"
    echo "  🗄️  MinIO控制台: http://localhost:9001"
}

# 启动PDF解析API
start_pdf_api() {
    print_info "启动PDF解析API服务..."
    cd "$PROJECT_DIR"
    
    # 检查是否已经运行
    if curl -s http://localhost:8002/health > /dev/null; then
        print_warning "PDF解析API已经在运行"
        return 0
    fi
    
    # 启动服务
    nohup python3 -c "
import uvicorn
from api.main import app
uvicorn.run(app, host='0.0.0.0', port=8002)
" > logs/pdf_api.log 2>&1 &
    
    echo $! > logs/pdf_api.pid
    sleep 3
    
    if check_service 8002 "PDF解析API"; then
        print_success "PDF解析API启动成功"
    else
        print_error "PDF解析API启动失败，请检查日志: logs/pdf_api.log"
    fi
}

# 启动Dify适配器
start_dify_adapter() {
    print_info "启动Dify适配器服务..."
    cd "$PROJECT_DIR/dify-adapter"
    
    # 检查是否已经运行
    if curl -s http://localhost:8001/health > /dev/null; then
        print_warning "Dify适配器已经在运行"
        return 0
    fi
    
    # 启动服务
    nohup python3 start_adapter.py > ../logs/dify_adapter.log 2>&1 &
    echo $! > ../logs/dify_adapter.pid
    sleep 3
    
    if check_service 8001 "Dify适配器"; then
        print_success "Dify适配器启动成功"
    else
        print_error "Dify适配器启动失败，请检查日志: logs/dify_adapter.log"
    fi
}

# 启动所有服务
start() {
    print_info "启动所有服务..."
    mkdir -p "$PROJECT_DIR/logs"
    
    start_pdf_api
    start_dify_adapter
    
    echo ""
    status
}

# 停止服务
stop_service() {
    local pid_file=$1
    local service_name=$2
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid"
            rm "$pid_file"
            print_success "$service_name 已停止"
        else
            print_warning "$service_name 进程不存在"
            rm "$pid_file"
        fi
    else
        print_warning "$service_name PID文件不存在"
    fi
}

# 停止所有服务
stop() {
    print_info "停止所有服务..."
    cd "$PROJECT_DIR"
    
    stop_service "logs/pdf_api.pid" "PDF解析API"
    stop_service "logs/dify_adapter.pid" "Dify适配器"
    
    # 强制杀死可能残留的进程
    pkill -f "api.main"
    pkill -f "start_adapter.py"
    
    print_success "所有服务已停止"
}

# 重启服务
restart() {
    print_info "重启所有服务..."
    stop
    sleep 2
    start
}

# 查看日志
logs() {
    local service=$1
    cd "$PROJECT_DIR"
    
    case "$service" in
        "pdf"|"api")
            if [ -f "logs/pdf_api.log" ]; then
                tail -f logs/pdf_api.log
            else
                print_error "PDF API日志文件不存在"
            fi
            ;;
        "dify"|"adapter")
            if [ -f "logs/dify_adapter.log" ]; then
                tail -f logs/dify_adapter.log
            else
                print_error "Dify适配器日志文件不存在"
            fi
            ;;
        *)
            print_info "可用的日志选项: pdf, dify"
            print_info "使用方法: $0 logs <service>"
            ;;
    esac
}

# 显示帮助信息
help() {
    echo ""
    echo "PDF解析器项目服务管理脚本"
    echo ""
    echo "使用方法: $0 {start|stop|restart|status|logs|help}"
    echo ""
    echo "命令:"
    echo "  start    - 启动所有服务"
    echo "  stop     - 停止所有服务"
    echo "  restart  - 重启所有服务"
    echo "  status   - 显示服务状态"
    echo "  logs     - 查看服务日志 (logs pdf|dify)"
    echo "  help     - 显示此帮助信息"
    echo ""
    echo "服务端口:"
    echo "  PDF解析API: 8002"
    echo "  Dify适配器: 8001"
    echo "  全局Milvus: 19530"
    echo ""
}

# 主逻辑
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    logs)
        logs "$2"
        ;;
    help|--help|-h)
        help
        ;;
    *)
        print_error "未知命令: $1"
        help
        exit 1
        ;;
esac
