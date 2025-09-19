#!/bin/bash

# 简历分析服务启动脚本

echo "🚀 启动简历分析服务..."

# 检查.env文件
if [ ! -f ".env" ]; then
    echo "⚠️  .env文件不存在，从.env.example复制"
    cp .env.example .env
    echo "📝 请编辑.env文件，设置正确的API密钥"
    echo "   主要需要设置: ZHIPUAI_API_KEY 或 OPENAI_API_KEY"
    exit 1
fi

# 检查Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装"
    exit 1
fi

if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker未运行，请启动Docker"
    exit 1
fi

# 创建日志目录
mkdir -p logs

# 启动服务
echo "📦 启动Docker服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 15

# 检查服务状态
echo "🔍 检查服务状态..."

# 检查分析服务
if curl -s http://localhost:8004/health > /dev/null 2>&1; then
    echo "✅ 简历分析服务启动成功"
else
    echo "❌ 简历分析服务启动失败"
    echo "📋 查看日志: docker-compose logs analysis-service"
    exit 1
fi

echo ""
echo "🎉 服务启动完成！"
echo ""
echo "📊 服务信息："
echo "  - 简历分析服务: http://localhost:8004"
echo "  - API文档: http://localhost:8004/docs"
echo "  - MongoDB: mongodb://admin:password123@localhost:27017"
echo "  - Mongo Express: http://localhost:8081 (admin/admin123)"
echo ""
echo "🧪 测试命令："
echo "  curl http://localhost:8004/health"
echo ""
echo "🛑 停止服务："
echo "  docker-compose down"
