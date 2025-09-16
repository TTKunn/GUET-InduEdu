"""
PDF解析服务主启动文件
"""

import uvicorn
from config import API_HOST, API_PORT, API_WORKERS, validate_config, get_config_info

def main():
    """启动PDF解析服务"""
    try:
        # 验证配置
        validate_config()
        print("✅ 配置验证通过")

        # 显示配置信息
        config_info = get_config_info()
        print("📋 服务配置:")
        for section, values in config_info.items():
            print(f"  {section}:")
            for key, value in values.items():
                print(f"    {key}: {value}")

        print(f"\n🚀 启动PDF解析服务...")
        print(f"📍 服务地址: http://{API_HOST}:{API_PORT}")
        print(f"📖 API文档: http://{API_HOST}:{API_PORT}/docs")

        # 启动服务
        uvicorn.run(
            "api.main:app",
            host=API_HOST,
            port=API_PORT,
            workers=API_WORKERS,
            reload=False,
            log_level="info"
        )

    except Exception as e:
        print(f"❌ 服务启动失败: {e}")
        exit(1)

if __name__ == "__main__":
    main()