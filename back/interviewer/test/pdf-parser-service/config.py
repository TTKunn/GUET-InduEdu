"""
PDF解析服务配置文件
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# ==================== 服务配置 ====================
# API服务配置
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8003"))
API_WORKERS = int(os.getenv("API_WORKERS", "1"))

# 跨域配置
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_HEADERS = ["*"]

# ==================== PDF解析配置 ====================
# PDF解析参数
PDF_CHUNK_SIZE = int(os.getenv("PDF_CHUNK_SIZE", "1000"))
PDF_CHUNK_OVERLAP = int(os.getenv("PDF_CHUNK_OVERLAP", "200"))
PDF_MAX_FILE_SIZE = int(os.getenv("PDF_MAX_FILE_SIZE", "10"))  # MB

# 支持的文件类型
ALLOWED_FILE_EXTENSIONS = ['.pdf']
ALLOWED_MIME_TYPES = ['application/pdf']

# ==================== 日志配置 ====================
# 日志级别
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOG_DIR = os.getenv("LOG_DIR", "./logs")

# 确保日志目录存在
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)

# ==================== 安全配置 ====================
# API密钥（可选，用于接口鉴权）
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ENABLE_AUTH = os.getenv("ENABLE_AUTH", "false").lower() == "true"

# 请求限制
MAX_REQUESTS_PER_MINUTE = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "60"))
MAX_CONCURRENT_REQUESTS = int(os.getenv("MAX_CONCURRENT_REQUESTS", "10"))

# ==================== 配置验证 ====================
def validate_config():
    """验证必要的配置项"""
    errors = []

    # 检查端口配置
    if not (1 <= API_PORT <= 65535):
        errors.append(f"Invalid API_PORT: {API_PORT}")

    # 检查文件大小限制
    if PDF_MAX_FILE_SIZE <= 0:
        errors.append(f"Invalid PDF_MAX_FILE_SIZE: {PDF_MAX_FILE_SIZE}")

    if errors:
        raise ValueError(f"Configuration errors: {', '.join(errors)}")

# ==================== 配置信息显示 ====================
def get_config_info() -> dict:
    """获取配置信息（隐藏敏感信息）"""
    return {
        "service": {
            "host": API_HOST,
            "port": API_PORT,
            "workers": API_WORKERS
        },
        "pdf": {
            "chunk_size": PDF_CHUNK_SIZE,
            "chunk_overlap": PDF_CHUNK_OVERLAP,
            "max_file_size_mb": PDF_MAX_FILE_SIZE
        },
        "security": {
            "auth_enabled": ENABLE_AUTH,
            "max_requests_per_minute": MAX_REQUESTS_PER_MINUTE
        }
    }

# 启动时验证配置
if __name__ == "__main__":
    try:
        validate_config()
        print("✅ Configuration validation passed")
        print("📋 Current configuration:")
        import json
        print(json.dumps(get_config_info(), indent=2))
    except ValueError as e:
        print(f"❌ Configuration validation failed: {e}")
        exit(1)