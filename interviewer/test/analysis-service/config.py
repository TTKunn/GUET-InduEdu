"""
配置文件 - 所有敏感信息通过环境变量配置
"""

import os
from typing import Optional
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# ==================== 数据库配置 ====================
# MySQL配置
MYSQL_URL = os.getenv("MYSQL_URL", "mysql+pymysql://root:password@43.142.157.145:3306/interview_analysis")
MYSQL_POOL_SIZE = int(os.getenv("MYSQL_POOL_SIZE", "10"))
MYSQL_MAX_OVERFLOW = int(os.getenv("MYSQL_MAX_OVERFLOW", "20"))
MYSQL_POOL_TIMEOUT = int(os.getenv("MYSQL_POOL_TIMEOUT", "30"))

# 已迁移到MySQL，MongoDB配置已移除

# ==================== 大模型配置 ====================
# 智谱AI配置
ZHIPUAI_API_KEY = os.getenv("ZHIPUAI_API_KEY")
ZHIPUAI_MODEL = os.getenv("ZHIPUAI_MODEL", "glm-4")
ZHIPUAI_BASE_URL = os.getenv("ZHIPUAI_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/")

# OpenAI配置（备用）
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

# 默认使用的LLM提供商
DEFAULT_LLM_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "zhipuai")  # zhipuai, openai

# LLM调用参数
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "4000"))
LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "60"))

# ==================== PDF解析配置 ====================
# PDF解析参数
PDF_CHUNK_SIZE = int(os.getenv("PDF_CHUNK_SIZE", "1000"))
PDF_CHUNK_OVERLAP = int(os.getenv("PDF_CHUNK_OVERLAP", "200"))
PDF_MAX_FILE_SIZE = int(os.getenv("PDF_MAX_FILE_SIZE", "10"))  # MB

# 支持的文件类型
ALLOWED_FILE_EXTENSIONS = ['.pdf']
ALLOWED_MIME_TYPES = ['application/pdf']

# ==================== 服务配置 ====================
# API服务配置
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8004"))
API_WORKERS = int(os.getenv("API_WORKERS", "1"))

# 跨域配置
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_HEADERS = ["*"]

# ==================== 日志配置 ====================
# 日志级别
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOG_FILE = os.getenv("LOG_FILE", "logs/analysis_service.log")

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

# ==================== 配置验证 ====================
def validate_config():
    """验证必要的配置项"""
    errors = []

    # 检查数据库配置
    if not MYSQL_URL:
        errors.append("MYSQL_URL is required")

    # 检查LLM配置
    if DEFAULT_LLM_PROVIDER == "zhipuai" and not ZHIPUAI_API_KEY:
        errors.append("ZHIPUAI_API_KEY is required when using zhipuai provider")
    elif DEFAULT_LLM_PROVIDER == "openai" and not OPENAI_API_KEY:
        errors.append("OPENAI_API_KEY is required when using openai provider")

    if errors:
        raise ValueError(f"Configuration errors: {', '.join(errors)}")

# ==================== 配置信息显示 ====================
def get_config_info() -> dict:
    """获取配置信息（隐藏敏感信息）"""
    return {
        "database": {
            "mysql_url": MYSQL_URL.split('@')[1] if '@' in MYSQL_URL else "43.142.157.145:3306/interview_analysis",
            "pool_size": MYSQL_POOL_SIZE,
            "max_overflow": MYSQL_MAX_OVERFLOW
        },
        "llm": {
            "provider": DEFAULT_LLM_PROVIDER,
            "model": ZHIPUAI_MODEL if DEFAULT_LLM_PROVIDER == "zhipuai" else OPENAI_MODEL,
            "temperature": LLM_TEMPERATURE,
            "max_tokens": LLM_MAX_TOKENS
        },
        "api": {
            "host": API_HOST,
            "port": API_PORT,
            "workers": API_WORKERS
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
