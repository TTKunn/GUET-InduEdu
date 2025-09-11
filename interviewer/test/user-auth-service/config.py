"""
用户认证服务配置文件
"""

import os
from typing import Optional
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# ==================== 服务配置 ====================
# API服务配置
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8007"))
API_WORKERS = int(os.getenv("API_WORKERS", "1"))

# 跨域配置
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_HEADERS = ["*"]

# ==================== 数据库配置 ====================
# MySQL配置
MYSQL_URL = os.getenv("MYSQL_URL", "mysql+pymysql://root:password@localhost:3306/interview_analysis")
MYSQL_POOL_SIZE = int(os.getenv("MYSQL_POOL_SIZE", "10"))
MYSQL_MAX_OVERFLOW = int(os.getenv("MYSQL_MAX_OVERFLOW", "20"))
MYSQL_POOL_TIMEOUT = int(os.getenv("MYSQL_POOL_TIMEOUT", "30"))

# ==================== 日志配置 ====================
# 日志级别
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOG_FILE = os.getenv("LOG_FILE", "logs/user_auth_service.log")

# 日志轮转配置
LOG_MAX_BYTES = int(os.getenv("LOG_MAX_BYTES", "10485760"))  # 10MB
LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "5"))

# ==================== JWT配置 ====================
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
JWT_REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", "7"))

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

    # 检查JWT密钥
    if not JWT_SECRET_KEY or JWT_SECRET_KEY == "your-secret-key-here":
        errors.append("JWT_SECRET_KEY must be set to a secure value")

    if errors:
        raise ValueError(f"Configuration errors: {', '.join(errors)}")

# ==================== 配置信息显示 ====================
def get_config_info() -> dict:
    """获取配置信息（隐藏敏感信息）"""
    return {
        "service": {
            "name": "user-auth-service",
            "version": "1.0.0",
            "host": API_HOST,
            "port": API_PORT,
            "workers": API_WORKERS
        },
        "database": {
            "mysql_url": MYSQL_URL.split('@')[1] if '@' in MYSQL_URL else "localhost:3306/interview_analysis",
            "pool_size": MYSQL_POOL_SIZE,
            "max_overflow": MYSQL_MAX_OVERFLOW,
            "pool_timeout": MYSQL_POOL_TIMEOUT
        },
        "jwt": {
            "algorithm": JWT_ALGORITHM,
            "access_token_expire_minutes": JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
            "refresh_token_expire_days": JWT_REFRESH_TOKEN_EXPIRE_DAYS
        },
        "logging": {
            "level": LOG_LEVEL,
            "file": LOG_FILE,
            "max_bytes": LOG_MAX_BYTES,
            "backup_count": LOG_BACKUP_COUNT
        },
        "security": {
            "auth_enabled": ENABLE_AUTH,
            "max_requests_per_minute": MAX_REQUESTS_PER_MINUTE,
            "max_concurrent_requests": MAX_CONCURRENT_REQUESTS
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
