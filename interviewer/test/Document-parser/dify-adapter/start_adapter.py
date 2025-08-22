"""
Dify适配器服务启动脚本
确保在PDF_ANALYSER conda环境中正确启动服务
"""

import os
import sys
import logging
import uvicorn
from pathlib import Path

# 添加当前目录到Python路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# 导入配置
from config import ADAPTER_HOST, ADAPTER_PORT, LOG_LEVEL

def setup_logging():
    """设置日志配置"""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("dify_adapter.log")
        ]
    )

def check_environment():
    """检查运行环境"""
    logger = logging.getLogger(__name__)
    
    # 检查conda环境
    conda_env = os.environ.get('CONDA_DEFAULT_ENV')
    if conda_env != 'PDF_ANALYSER':
        logger.warning(f"当前conda环境: {conda_env}, 建议使用: PDF_ANALYSER")
    else:
        logger.info(f"✓ 正在使用正确的conda环境: {conda_env}")
    
    # 检查Python版本
    python_version = sys.version_info
    logger.info(f"Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # 检查必要的依赖
    try:
        import fastapi
        import uvicorn
        import requests
        import pydantic
        logger.info("✓ 所有必要依赖已安装")
    except ImportError as e:
        logger.error(f"✗ 缺少依赖: {e}")
        logger.error("请运行: pip install -r requirements.txt")
        sys.exit(1)

def main():
    """主启动函数"""
    print("=" * 60)
    print("🚀 启动 Dify 外部知识库适配器服务")
    print("=" * 60)
    
    # 设置日志
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # 检查环境
    check_environment()
    
    # 显示配置信息
    logger.info(f"服务地址: http://{ADAPTER_HOST}:{ADAPTER_PORT}")
    logger.info(f"API文档: http://{ADAPTER_HOST}:{ADAPTER_PORT}/docs")
    logger.info(f"健康检查: http://{ADAPTER_HOST}:{ADAPTER_PORT}/health")
    logger.info(f"日志级别: {LOG_LEVEL}")
    
    # 启动服务
    try:
        uvicorn.run(
            "main:app",
            host=ADAPTER_HOST,
            port=ADAPTER_PORT,
            reload=True,  # 开发模式
            log_level=LOG_LEVEL.lower(),
            access_log=True
        )
    except KeyboardInterrupt:
        logger.info("服务已停止")
    except Exception as e:
        logger.error(f"服务启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
