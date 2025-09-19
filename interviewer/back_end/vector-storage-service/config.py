"""
向量存储服务配置文件
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# ==================== 服务配置 ====================
# API服务配置
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8005"))
API_WORKERS = int(os.getenv("API_WORKERS", "1"))

# 跨域配置
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_HEADERS = ["*"]

# ==================== Milvus配置 ====================
# Milvus连接配置
MILVUS_URI = os.getenv("MILVUS_URI", "http://localhost:19530")
MILVUS_TOKEN = os.getenv("MILVUS_TOKEN", "")

# 默认集合配置
DEFAULT_COLLECTION_NAME = os.getenv("DEFAULT_COLLECTION_NAME", "default_collection")

# ==================== 嵌入模型配置 ====================
# 智谱AI配置
ZHIPUAI_API_KEY = os.getenv("ZHIPUAI_API_KEY", "")
ZHIPUAI_EMBEDDING_MODEL = os.getenv("ZHIPUAI_EMBEDDING_MODEL", "embedding-2")

# BGE嵌入模型配置
BGE_MODEL_NAME = os.getenv("BGE_MODEL_NAME", "BAAI/bge-small-zh-v1.5")
BGE_DEVICE = os.getenv("BGE_DEVICE", "cpu")
BGE_NORMALIZE_EMBEDDINGS = os.getenv("BGE_NORMALIZE_EMBEDDINGS", "True").lower() == "true"

# 默认嵌入模型
DEFAULT_EMBEDDING_MODEL = os.getenv("DEFAULT_EMBEDDING_MODEL", "zhipuai")

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

# ==================== 向量存储配置 ====================
# 搜索参数
DEFAULT_SEARCH_K = int(os.getenv("DEFAULT_SEARCH_K", "5"))
MAX_SEARCH_K = int(os.getenv("MAX_SEARCH_K", "100"))

# 批处理配置
MAX_BATCH_SIZE = int(os.getenv("MAX_BATCH_SIZE", "1000"))

# ==================== 配置验证 ====================
def validate_config():
    """验证必要的配置项"""
    errors = []

    # 检查端口配置
    if not (1 <= API_PORT <= 65535):
        errors.append(f"Invalid API_PORT: {API_PORT}")

    # 检查Milvus配置
    if not MILVUS_URI:
        errors.append("MILVUS_URI is required")

    # 检查嵌入模型配置
    if DEFAULT_EMBEDDING_MODEL == "zhipuai" and not ZHIPUAI_API_KEY:
        errors.append("ZHIPUAI_API_KEY is required when using zhipuai as default embedding model")

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
        "milvus": {
            "uri": MILVUS_URI,
            "default_collection": DEFAULT_COLLECTION_NAME
        },
        "embedding": {
            "default_model": DEFAULT_EMBEDDING_MODEL,
            "zhipuai_model": ZHIPUAI_EMBEDDING_MODEL,
            "bge_model": BGE_MODEL_NAME,
            "bge_device": BGE_DEVICE
        },
        "search": {
            "default_k": DEFAULT_SEARCH_K,
            "max_k": MAX_SEARCH_K,
            "max_batch_size": MAX_BATCH_SIZE
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