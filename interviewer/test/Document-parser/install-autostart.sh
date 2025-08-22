#!/bin/bash

# PDF解析器项目开机自启动安装脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

# 检查是否以root权限运行
if [[ $EUID -eq 0 ]]; then
   print_error "请不要以root权限运行此脚本"
   print_info "使用方法: ./install-autostart.sh"
   exit 1
fi

PROJECT_DIR="/home/ubuntu/workspace/project/Document-parser"
SERVICE_FILE="$PROJECT_DIR/systemd-services/pdf-parser.service"

print_info "开始安装PDF解析器项目开机自启动服务..."

# 检查服务文件是否存在
if [ ! -f "$SERVICE_FILE" ]; then
    print_error "服务文件不存在: $SERVICE_FILE"
    exit 1
fi

# 复制服务文件到systemd目录
print_info "复制服务文件到systemd目录..."
sudo cp "$SERVICE_FILE" /etc/systemd/system/

# 重新加载systemd配置
print_info "重新加载systemd配置..."
sudo systemctl daemon-reload

# 启用服务
print_info "启用PDF解析器服务..."
sudo systemctl enable pdf-parser.service

# 检查服务状态
print_info "检查服务状态..."
if sudo systemctl is-enabled pdf-parser.service >/dev/null 2>&1; then
    print_success "PDF解析器服务已成功启用开机自启动"
else
    print_error "服务启用失败"
    exit 1
fi

print_info "安装完成！"
echo ""
print_info "管理命令："
echo "  启动服务: sudo systemctl start pdf-parser"
echo "  停止服务: sudo systemctl stop pdf-parser"
echo "  重启服务: sudo systemctl restart pdf-parser"
echo "  查看状态: sudo systemctl status pdf-parser"
echo "  查看日志: sudo journalctl -u pdf-parser -f"
echo "  禁用自启: sudo systemctl disable pdf-parser"
echo ""
print_warning "注意：服务将在下次重启时自动启动"
print_info "如需立即启动服务，请运行: sudo systemctl start pdf-parser"
