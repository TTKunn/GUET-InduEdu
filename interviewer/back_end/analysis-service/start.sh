#!/bin/bash

# 简历分析服务启动脚本

set -e

echo "🚀 启动简历分析服务..."

# 检查Python环境
if ! command -v python &> /dev/null; then
    echo "❌ Python未安装，请先安装Python 3.10+"
    exit 1
fi

# 检查Python版本
python_version=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python版本过低，需要Python 3.10+，当前版本: $python_version"
    exit 1
fi

# 创建必要的目录
mkdir -p logs

# 检查并安装依赖
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python -m venv venv
fi

echo "📦 激活虚拟环境..."
source venv/bin/activate || source venv/Scripts/activate

echo "📦 安装依赖包..."
pip install -r requirements.txt

# 检查配置文件
if [ ! -f ".env" ]; then
    echo "⚠️  .env文件不存在，使用默认配置"
    echo "如需自定义配置，请创建.env文件"
fi

# 验证配置
echo "🔧 验证配置..."
python config.py

# 启动服务
echo "🎉 启动简历分析服务..."
echo "📍 本地访问: http://localhost:8004"
echo "🌐 外部访问: http://43.142.157.145:8004"
echo "📖 API文档: http://43.142.157.145:8004/docs"
echo "❤️  健康检查: http://43.142.157.145:8004/health"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

python main.py
