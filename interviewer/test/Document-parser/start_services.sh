#!/bin/bash

# 服务启动脚本 - 同时启动PDF解析API和Dify适配器

set -e

echo "🚀 启动PDF解析和Dify适配器服务..."

# 等待Milvus服务就绪
echo "⏳ 等待Milvus服务启动..."
while ! curl -s http://milvus:19530/health > /dev/null 2>&1; do
    echo "等待Milvus服务..."
    sleep 5
done
echo "✅ Milvus服务已就绪"

# 启动PDF解析API服务（后台运行）
echo "🔧 启动PDF解析API服务..."
cd /app
python start_api.py &
PDF_API_PID=$!

# 等待PDF解析API启动
echo "⏳ 等待PDF解析API启动..."
sleep 10
while ! curl -s http://localhost:8000/health > /dev/null 2>&1; do
    echo "等待PDF解析API..."
    sleep 5
done
echo "✅ PDF解析API服务已启动"

# 启动Dify适配器服务（后台运行）
echo "🔧 启动Dify适配器服务..."
cd /app/dify-adapter
python start_adapter.py &
ADAPTER_PID=$!

# 等待Dify适配器启动
echo "⏳ 等待Dify适配器启动..."
sleep 10
while ! curl -s http://localhost:8001/health > /dev/null 2>&1; do
    echo "等待Dify适配器..."
    sleep 5
done
echo "✅ Dify适配器服务已启动"

echo "🎉 所有服务启动完成！"
echo "📋 服务状态："
echo "   - PDF解析API: http://localhost:8000"
echo "   - Dify适配器: http://localhost:8001"

# 创建一个函数来优雅地关闭服务
cleanup() {
    echo "🛑 正在关闭服务..."
    kill $PDF_API_PID $ADAPTER_PID 2>/dev/null || true
    wait $PDF_API_PID $ADAPTER_PID 2>/dev/null || true
    echo "✅ 服务已关闭"
    exit 0
}

# 捕获信号以优雅关闭
trap cleanup SIGTERM SIGINT

# 保持脚本运行
wait
