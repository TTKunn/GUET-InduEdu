#!/bin/bash

# PDF解析服务启动脚本

echo "🚀 启动PDF解析服务..."

# 检查.env文件
if [ ! -f ".env" ]; then
    echo "⚠️  .env文件不存在，从.env.example复制"
    cp .env.example .env
    echo "📝 请根据需要编辑.env文件"
fi

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未安装"
    exit 1
fi

# 检查依赖
echo "📦 检查Python依赖..."
if [ ! -d "venv" ]; then
    echo "🔧 创建虚拟环境..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt

# 创建日志目录
mkdir -p logs

# 启动服务
echo "🎯 启动PDF解析服务..."
python main.py
