"""
面试记录服务配置文件
"""

import os
from typing import Optional
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# ==================== 数据库配置 ====================
# MySQL配置
MYSQL_URL = os.getenv("MYSQL_URL", "mysql+pymysql://root:Xzk200411.@43.142.157.145:3306/interview_analysis")
MYSQL_POOL_SIZE = int(os.getenv("MYSQL_POOL_SIZE", "10"))
MYSQL_MAX_OVERFLOW = int(os.getenv("MYSQL_MAX_OVERFLOW", "20"))
MYSQL_POOL_TIMEOUT = int(os.getenv("MYSQL_POOL_TIMEOUT", "30"))

# ==================== 服务配置 ====================
# API服务配置
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8006"))
API_WORKERS = int(os.getenv("API_WORKERS", "1"))

# 跨域配置
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_HEADERS = ["*"]

# ==================== 外部服务配置 ====================
# analysis-service配置
ANALYSIS_SERVICE_URL = os.getenv("ANALYSIS_SERVICE_URL", "http://localhost:8004")

# ==================== 日志配置 ====================
# 日志级别
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOG_FILE = os.getenv("LOG_FILE", "logs/interview_service.log")

# 日志轮转配置
LOG_MAX_BYTES = int(os.getenv("LOG_MAX_BYTES", "10485760"))  # 10MB
LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "5"))

# ==================== 安全配置 ====================
# API密钥（可选，用于接口鉴权）
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ENABLE_AUTH = os.getenv("ENABLE_AUTH", "false").lower() == "true"

# 请求限制
MAX_REQUESTS_PER_MINUTE = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "60"))
MAX_CONCURRENT_REQUESTS = int(os.getenv("MAX_CONCURRENT_REQUESTS", "10"))

# ==================== 业务配置 ====================
# 面试会话配置
DEFAULT_SESSION_DURATION = int(os.getenv("DEFAULT_SESSION_DURATION", "60"))  # 默认面试时长（分钟）
MAX_QUESTIONS_PER_SESSION = int(os.getenv("MAX_QUESTIONS_PER_SESSION", "20"))  # 每次面试最大题目数
DEFAULT_QUESTION_DURATION = int(os.getenv("DEFAULT_QUESTION_DURATION", "10"))  # 默认题目回答时长（分钟）

# ==================== 配置验证 ====================
def validate_config():
    """验证必要的配置项"""
    errors = []

    # 检查数据库配置
    if not MYSQL_URL:
        errors.append("MYSQL_URL is required")

    # 检查端口配置
    if not (1024 <= API_PORT <= 65535):
        errors.append("API_PORT must be between 1024 and 65535")

    if errors:
        raise ValueError(f"Configuration errors: {', '.join(errors)}")

# ==================== 配置信息显示 ====================
def get_config_info() -> dict:
    """获取配置信息（隐藏敏感信息）"""
    return {
        "database": {
            "mysql_url": MYSQL_URL.split('@')[1] if '@' in MYSQL_URL else "localhost:3306/interview_analysis",
            "pool_size": MYSQL_POOL_SIZE,
            "max_overflow": MYSQL_MAX_OVERFLOW
        },
        "api": {
            "host": API_HOST,
            "port": API_PORT,
            "workers": API_WORKERS
        },
        "external_services": {
            "analysis_service": ANALYSIS_SERVICE_URL
        },
        "business": {
            "default_session_duration": DEFAULT_SESSION_DURATION,
            "max_questions_per_session": MAX_QUESTIONS_PER_SESSION,
            "default_question_duration": DEFAULT_QUESTION_DURATION
        },
        "security": {
            "auth_enabled": ENABLE_AUTH
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
