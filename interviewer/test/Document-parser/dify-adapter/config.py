"""
Dify适配器配置文件
管理API Key、Collection映射和服务配置
"""

import os
from typing import Dict, List, Optional

# ==================== 服务配置 ====================
# 适配器服务配置
ADAPTER_HOST = os.getenv("ADAPTER_HOST", "0.0.0.0")
ADAPTER_PORT = int(os.getenv("ADAPTER_PORT", "8001"))

# 现有PDF解析API配置 (支持Docker环境)
PDF_PARSER_API_URL = os.getenv("PDF_PARSER_API_URL", "http://localhost:8002")

# ==================== API Key管理 ====================
# API Key到Collection的映射配置
API_KEY_MAPPING = {
    "dify-pdf-docs-001": {
        "collection": "pdf_documents",
        "permissions": ["read"],
        "rate_limit": 100,
        "description": "PDF文档知识库访问"
    },
    "dify-tech-docs-002": {
        "collection": "technical_docs",
        "permissions": ["read"],
        "rate_limit": 200,
        "description": "技术文档知识库访问"
    },
    "dify-company-kb-003": {
        "collection": "company_knowledge",
        "permissions": ["read"],
        "rate_limit": 150,
        "description": "公司知识库访问"
    }
}

# 支持动态用户知识库的API Key模式
# 格式: dify-user-{user_id} -> user_kb_{user_id}
DYNAMIC_USER_KB_PREFIX = "dify-user-"
DYNAMIC_USER_COLLECTION_PREFIX = "user_kb_"

# 默认API Key（用于测试）
DEFAULT_API_KEY = os.getenv("DEFAULT_API_KEY", "dify-pdf-docs-001")

# ==================== 检索配置 ====================
# 默认检索参数
DEFAULT_TOP_K = 5
DEFAULT_SCORE_THRESHOLD = 0.5
MAX_TOP_K = 20
MIN_SCORE_THRESHOLD = 0.0
MAX_SCORE_THRESHOLD = 1.0

# 嵌入模型配置
DEFAULT_EMBEDDING_MODEL = "zhipuai"
SUPPORTED_EMBEDDING_MODELS = ["zhipuai", "bge", "openai"]

# ==================== 错误码定义 ====================
ERROR_CODES = {
    1001: "Invalid Authorization header format. Expected 'Bearer <api-key>' format.",
    1002: "Authorization failed. Invalid API key.",
    2001: "The knowledge does not exist. Invalid collection name.",
    2002: "Collection access denied. Insufficient permissions.",
    3001: "Invalid retrieval parameters.",
    500: "Internal server error."
}

# ==================== 日志配置 ====================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ==================== 辅助函数 ====================
def validate_api_key(api_key: str) -> Optional[Dict]:
    """验证API Key并返回配置信息"""
    # 检查静态配置的API Key
    if api_key in API_KEY_MAPPING:
        return API_KEY_MAPPING[api_key]

    # 检查动态用户API Key格式: dify-user-{user_id}
    if api_key.startswith(DYNAMIC_USER_KB_PREFIX):
        user_id = api_key[len(DYNAMIC_USER_KB_PREFIX):]
        if user_id and user_id.isalnum():  # 确保user_id只包含字母数字
            return {
                "collection": f"{DYNAMIC_USER_COLLECTION_PREFIX}{user_id}",
                "permissions": ["read"],
                "rate_limit": 100,
                "description": f"用户{user_id}的个人知识库",
                "user_id": user_id,
                "is_dynamic": True
            }

    return None

def get_allowed_collections(api_key: str) -> List[str]:
    """获取API Key允许访问的Collection列表"""
    config = validate_api_key(api_key)
    if config and "read" in config.get("permissions", []):
        return [config["collection"]]
    return []

def validate_collection_access(api_key: str, collection_name: str) -> bool:
    """验证API Key是否有权限访问指定Collection"""
    allowed_collections = get_allowed_collections(api_key)
    return collection_name in allowed_collections

def validate_retrieval_params(top_k: int, score_threshold: float) -> bool:
    """验证检索参数是否在有效范围内"""
    return (
        1 <= top_k <= MAX_TOP_K and
        MIN_SCORE_THRESHOLD <= score_threshold <= MAX_SCORE_THRESHOLD
    )
