"""
PDF解析API服务启动脚本
"""
import uvicorn

if __name__ == "__main__":
    # 启动API服务
    # 使用字符串形式传递应用程序以支持reload功能
    uvicorn.run(
        "api.main:app",  # 使用字符串形式指定应用程序
        host="0.0.0.0",
        port=8000,
        reload=True,  # 开发模式，代码变更自动重载
        log_level="info"
    )
