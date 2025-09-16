"""
简化的服务启动脚本
用于Windows环境下启动interview-service
"""

import sys
import os
import uvicorn

def main():
    print("🚀 启动interview-service...")
    print("📍 服务地址: http://localhost:8006")
    print("📖 API文档: http://localhost:8006/docs")
    print("❤️  健康检查: http://localhost:8006/health")
    print("")
    print("🎯 Dify专用API接口:")
    print("   POST /dify/interview/create - 创建面试记录")
    print("   POST /dify/interview/add-qa - 添加题目和回答")
    print("   GET  /dify/interview/{user_id}/latest - 获取最新面试信息")
    print("   GET  /dify/interview/{session_id}/summary - 获取面试总结")
    print("")
    print("按 Ctrl+C 停止服务")
    print("")
    
    try:
        # 启动服务
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8006,
            reload=False,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 服务已停止")
    except Exception as e:
        print(f"❌ 服务启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
