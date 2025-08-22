#!/bin/bash

# PDF知识库服务Docker部署脚本

set -e

echo "🚀 开始部署PDF知识库服务..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查Docker是否安装
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker未安装，请先安装Docker"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose未安装，请先安装Docker Compose"
        exit 1
    fi
    
    print_message "Docker环境检查通过"
}

# 检查端口是否被占用
check_ports() {
    local ports=(8000 8001 19530 9000 9001 9091 2379)
    for port in "${ports[@]}"; do
        if netstat -tuln | grep -q ":$port "; then
            print_warning "端口 $port 已被占用，可能会导致服务启动失败"
        fi
    done
}

# 创建必要的目录
create_directories() {
    print_message "创建必要的目录..."
    mkdir -p logs data output
    chmod 755 start_services.sh
}

# 复制环境配置
setup_environment() {
    print_message "设置环境配置..."
    if [ ! -f .env ]; then
        cp .env.docker .env
        print_message "已复制Docker环境配置文件"
    else
        print_warning ".env文件已存在，请确认配置正确"
    fi
}

# 构建和启动服务
deploy_services() {
    print_message "构建Docker镜像..."
    docker-compose build --no-cache
    
    print_message "启动服务..."
    docker-compose up -d
    
    print_message "等待服务启动..."
    sleep 30
}

# 检查服务状态
check_services() {
    print_message "检查服务状态..."
    
    # 检查容器状态
    if docker-compose ps | grep -q "Up"; then
        print_message "容器启动成功"
    else
        print_error "容器启动失败"
        docker-compose logs
        exit 1
    fi
    
    # 检查服务健康状态
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        print_message "检查服务健康状态 (尝试 $attempt/$max_attempts)..."
        
        # 检查PDF解析API
        if curl -s http://localhost:8000/health > /dev/null; then
            print_message "✅ PDF解析API服务正常"
            pdf_api_ok=true
        else
            pdf_api_ok=false
        fi
        
        # 检查Dify适配器
        if curl -s http://localhost:8001/health > /dev/null; then
            print_message "✅ Dify适配器服务正常"
            adapter_ok=true
        else
            adapter_ok=false
        fi
        
        if [ "$pdf_api_ok" = true ] && [ "$adapter_ok" = true ]; then
            break
        fi
        
        sleep 10
        ((attempt++))
    done
    
    if [ $attempt -gt $max_attempts ]; then
        print_error "服务健康检查超时"
        print_error "请检查日志: docker-compose logs"
        exit 1
    fi
}

# 显示部署信息
show_deployment_info() {
    print_message "🎉 部署完成！"
    echo ""
    echo -e "${BLUE}服务信息:${NC}"
    echo "  📋 PDF解析API:    http://localhost:8000"
    echo "  🔗 Dify适配器:    http://localhost:8001"
    echo "  🗄️  Milvus数据库:  http://localhost:19530"
    echo "  📦 MinIO控制台:   http://localhost:9001"
    echo ""
    echo -e "${BLUE}Dify配置信息:${NC}"
    echo "  🌐 API端点:       http://你的服务器IP:8001"
    echo "  🔑 API Key:       dify-pdf-docs-001"
    echo "  📚 知识库ID:      pdf_documents"
    echo ""
    echo -e "${BLUE}常用命令:${NC}"
    echo "  查看日志:         docker-compose logs -f"
    echo "  停止服务:         docker-compose down"
    echo "  重启服务:         docker-compose restart"
    echo "  查看状态:         docker-compose ps"
}

# 主函数
main() {
    print_message "开始部署PDF知识库服务..."
    
    check_docker
    check_ports
    create_directories
    setup_environment
    deploy_services
    check_services
    show_deployment_info
    
    print_message "部署完成！"
}

# 执行主函数
main "$@"
