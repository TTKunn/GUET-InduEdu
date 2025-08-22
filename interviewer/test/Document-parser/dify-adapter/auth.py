"""
Dify适配器认证和权限管理模块
处理API Key验证、权限检查和访问控制
"""

import time
import logging
from typing import Optional, Dict, List, Any
from fastapi import HTTPException, Header
from collections import defaultdict
from datetime import datetime, timedelta

from config import API_KEY_MAPPING, ERROR_CODES
from models import DifyErrorResponse

# 配置日志
logger = logging.getLogger(__name__)

# ==================== 速率限制管理 ====================
class RateLimiter:
    """简单的速率限制器"""
    
    def __init__(self):
        self.requests = defaultdict(list)  # api_key -> [timestamp, ...]
    
    def is_allowed(self, api_key: str, limit: int, window_seconds: int = 3600) -> bool:
        """
        检查API Key是否在速率限制内
        
        Args:
            api_key: API密钥
            limit: 每小时请求限制
            window_seconds: 时间窗口（秒）
        
        Returns:
            bool: 是否允许请求
        """
        now = time.time()
        cutoff = now - window_seconds
        
        # 清理过期的请求记录
        self.requests[api_key] = [
            timestamp for timestamp in self.requests[api_key] 
            if timestamp > cutoff
        ]
        
        # 检查是否超过限制
        if len(self.requests[api_key]) >= limit:
            return False
        
        # 记录当前请求
        self.requests[api_key].append(now)
        return True
    
    def get_remaining_requests(self, api_key: str, limit: int, window_seconds: int = 3600) -> int:
        """获取剩余请求次数"""
        now = time.time()
        cutoff = now - window_seconds
        
        current_requests = [
            timestamp for timestamp in self.requests[api_key] 
            if timestamp > cutoff
        ]
        
        return max(0, limit - len(current_requests))

# 全局速率限制器实例
rate_limiter = RateLimiter()

# ==================== 认证函数 ====================
def extract_bearer_token(authorization: Optional[str]) -> Optional[str]:
    """
    从Authorization头中提取Bearer Token
    
    Args:
        authorization: Authorization头的值
    
    Returns:
        str: 提取的API Key，如果格式无效则返回None
    """
    if not authorization:
        return None
    
    if not authorization.startswith("Bearer "):
        return None
    
    return authorization.replace("Bearer ", "").strip()

def validate_api_key(api_key: str) -> Optional[Dict]:
    """
    验证API Key并返回配置信息
    
    Args:
        api_key: 要验证的API Key
    
    Returns:
        Dict: API Key配置信息，如果无效则返回None
    """
    return API_KEY_MAPPING.get(api_key)

def check_collection_permission(api_key: str, collection_name: str) -> bool:
    """
    检查API Key是否有权限访问指定Collection
    
    Args:
        api_key: API密钥
        collection_name: Collection名称
    
    Returns:
        bool: 是否有权限访问
    """
    config = validate_api_key(api_key)
    if not config:
        return False
    
    # 检查是否有读取权限
    if "read" not in config.get("permissions", []):
        return False
    
    # 检查Collection是否匹配
    return config.get("collection") == collection_name

def check_rate_limit(api_key: str) -> bool:
    """
    检查API Key的速率限制
    
    Args:
        api_key: API密钥
    
    Returns:
        bool: 是否在速率限制内
    """
    config = validate_api_key(api_key)
    if not config:
        return False
    
    limit = config.get("rate_limit", 100)
    return rate_limiter.is_allowed(api_key, limit)

# ==================== 认证装饰器 ====================
def authenticate_request(authorization: Optional[str] = Header(None, alias="Authorization")):
    """
    认证请求装饰器
    
    Args:
        authorization: Authorization头
    
    Returns:
        str: 验证通过的API Key
    
    Raises:
        HTTPException: 认证失败时抛出异常
    """
    # 1. 检查Authorization头格式
    api_key = extract_bearer_token(authorization)
    if not api_key:
        logger.warning("Invalid Authorization header format")
        raise HTTPException(
            status_code=403,
            detail=DifyErrorResponse(
                error_code=1001,
                error_msg=ERROR_CODES[1001]
            ).dict()
        )
    
    # 2. 验证API Key
    config = validate_api_key(api_key)
    if not config:
        logger.warning(f"Invalid API key: {api_key[:8]}...")
        raise HTTPException(
            status_code=403,
            detail=DifyErrorResponse(
                error_code=1002,
                error_msg=ERROR_CODES[1002]
            ).dict()
        )
    
    # 3. 检查速率限制
    if not check_rate_limit(api_key):
        logger.warning(f"Rate limit exceeded for API key: {api_key[:8]}...")
        raise HTTPException(
            status_code=429,
            detail=DifyErrorResponse(
                error_code=4001,
                error_msg="Rate limit exceeded. Please try again later."
            ).dict()
        )
    
    logger.info(f"Authentication successful for API key: {api_key[:8]}...")
    return api_key

# ==================== 权限检查函数 ====================
def authorize_collection_access(api_key: str, collection_name: str):
    """
    检查Collection访问权限
    
    Args:
        api_key: 已验证的API Key
        collection_name: 要访问的Collection名称
    
    Raises:
        HTTPException: 权限不足时抛出异常
    """
    if not check_collection_permission(api_key, collection_name):
        logger.warning(f"Collection access denied: {api_key[:8]}... -> {collection_name}")
        raise HTTPException(
            status_code=403,
            detail=DifyErrorResponse(
                error_code=2002,
                error_msg=ERROR_CODES[2002]
            ).dict()
        )
    
    logger.info(f"Collection access authorized: {api_key[:8]}... -> {collection_name}")

# ==================== 统计和监控 ====================
class AuthStats:
    """认证统计信息"""
    
    def __init__(self):
        self.total_requests = 0
        self.successful_auths = 0
        self.failed_auths = 0
        self.rate_limit_hits = 0
        self.api_key_usage = defaultdict(int)
    
    def record_request(self, api_key: Optional[str], success: bool, rate_limited: bool = False):
        """记录请求统计"""
        self.total_requests += 1
        
        if rate_limited:
            self.rate_limit_hits += 1
        elif success and api_key:
            self.successful_auths += 1
            self.api_key_usage[api_key] += 1
        else:
            self.failed_auths += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "total_requests": self.total_requests,
            "successful_auths": self.successful_auths,
            "failed_auths": self.failed_auths,
            "rate_limit_hits": self.rate_limit_hits,
            "success_rate": self.successful_auths / max(1, self.total_requests),
            "top_api_keys": dict(sorted(
                self.api_key_usage.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5])
        }

# 全局统计实例
auth_stats = AuthStats()
