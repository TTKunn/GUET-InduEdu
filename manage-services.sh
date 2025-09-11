#!/bin/bash

# 统一服务管理脚本
# 管理8003-8006端口的微服务

set -e

# 服务配置：服务名:端口:目录
SERVICES=(
    "pdf-parser-service:8003:interviewer/test/pdf-parser-service"
    "analysis-service:8004:interviewer/test/analysis-service"
    "vector-storage-service:8005:interviewer/test/vector-storage-service"
    "interview-service:8006:interviewer/test/interview-service"
)

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查Docker环境
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker未安装"
        exit 1
    fi

    if ! docker info > /dev/null 2>&1; then
        log_error "Docker未运行，请启动Docker"
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose未安装"
        exit 1
    fi

    log_success "Docker环境检查通过"
}

# 等待服务健康检查
wait_for_health() {
    local port=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1

    log_info "等待 $service_name (端口:$port) 启动..."

    while [ $attempt -le $max_attempts ]; do
        if curl -s -f "http://localhost:$port/health" > /dev/null 2>&1; then
            log_success "$service_name 启动成功"
            return 0
        fi
        
        echo -n "."
        sleep 2
        ((attempt++))
    done

    log_error "$service_name 启动超时"
    return 1
}

# 启动单个服务
start_service() {
    local service_info=$1
    local service_name=$(echo $service_info | cut -d: -f1)
    local port=$(echo $service_info | cut -d: -f2)
    local directory=$(echo $service_info | cut -d: -f3)

    log_info "启动 $service_name..."

    # 进入服务目录
    if [ ! -d "$directory" ]; then
        log_error "服务目录不存在: $directory"
        return 1
    fi

    cd "$directory"

    # 检查docker-compose.yml文件
    if [ ! -f "docker-compose.yml" ]; then
        log_error "$service_name 缺少 docker-compose.yml 文件"
        return 1
    fi

    # 启动服务
    if docker-compose up -d; then
        # 等待健康检查
        if wait_for_health $port $service_name; then
            log_success "$service_name 启动完成"
            return 0
        else
            log_error "$service_name 健康检查失败"
            return 1
        fi
    else
        log_error "$service_name 启动失败"
        return 1
    fi
}

# 停止单个服务
stop_service() {
    local service_info=$1
    local service_name=$(echo $service_info | cut -d: -f1)
    local directory=$(echo $service_info | cut -d: -f3)

    log_info "停止 $service_name..."

    cd "$directory"
    
    if docker-compose down; then
        log_success "$service_name 停止完成"
    else
        log_warning "$service_name 停止时出现警告"
    fi
}

# 检查单个服务状态
check_service_status() {
    local service_info=$1
    local service_name=$(echo $service_info | cut -d: -f1)
    local port=$(echo $service_info | cut -d: -f2)

    echo -n "检查 $service_name (端口:$port) ... "
    
    if curl -s -f "http://localhost:$port/health" > /dev/null 2>&1; then
        echo -e "${GREEN}运行中${NC}"
        return 0
    else
        echo -e "${RED}未运行${NC}"
        return 1
    fi
}

# 启动所有服务
start_all() {
    log_info "开始启动所有服务..."
    check_docker

    local failed_services=()

    for service in "${SERVICES[@]}"; do
        if ! start_service "$service"; then
            service_name=$(echo $service | cut -d: -f1)
            failed_services+=("$service_name")
        fi
        # 返回根目录
        cd "$(dirname "$0")"
    done

    if [ ${#failed_services[@]} -eq 0 ]; then
        log_success "所有服务启动完成！"
        echo ""
        show_service_info
    else
        log_error "以下服务启动失败: ${failed_services[*]}"
        exit 1
    fi
}

# 停止所有服务
stop_all() {
    log_info "开始停止所有服务..."

    # 反向停止服务
    for ((i=${#SERVICES[@]}-1; i>=0; i--)); do
        stop_service "${SERVICES[i]}"
        cd "$(dirname "$0")"
    done

    log_success "所有服务已停止"
}

# 重启所有服务
restart_all() {
    log_info "重启所有服务..."
    stop_all
    sleep 5
    start_all
}

# 检查所有服务状态
status_all() {
    log_info "检查所有服务状态..."
    echo ""

    local running_count=0
    for service in "${SERVICES[@]}"; do
        if check_service_status "$service"; then
            ((running_count++))
        fi
    done

    echo ""
    log_info "运行中的服务: $running_count/${#SERVICES[@]}"
}

# 显示服务信息
show_service_info() {
    echo "📊 服务信息："
    echo "  - PDF解析服务: http://localhost:8003 (API文档: http://localhost:8003/docs)"
    echo "  - 简历分析服务: http://localhost:8004 (API文档: http://localhost:8004/docs)"
    echo "  - 向量存储服务: http://localhost:8005 (API文档: http://localhost:8005/docs)"
    echo "  - 面试记录服务: http://localhost:8006 (API文档: http://localhost:8006/docs)"
    echo ""
    echo "🧪 健康检查："
    for service in "${SERVICES[@]}"; do
        port=$(echo $service | cut -d: -f2)
        echo "  curl http://localhost:$port/health"
    done
}

# 显示帮助信息
show_help() {
    echo "微服务管理脚本"
    echo ""
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  start    启动所有服务"
    echo "  stop     停止所有服务"
    echo "  restart  重启所有服务"
    echo "  status   检查服务状态"
    echo "  info     显示服务信息"
    echo "  help     显示帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 start     # 启动所有服务"
    echo "  $0 status    # 检查服务状态"
}

# 主函数
main() {
    case "${1:-help}" in
        start)
            start_all
            ;;
        stop)
            stop_all
            ;;
        restart)
            restart_all
            ;;
        status)
            status_all
            ;;
        info)
            show_service_info
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "未知命令: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"
