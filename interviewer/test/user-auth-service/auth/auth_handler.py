"""
JWT认证处理器
"""

import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

import jwt
import bcrypt

logger = logging.getLogger(__name__)

class JWTHandler:
    """JWT认证处理器"""

    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        """初始化JWT处理器"""
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """创建访问token"""
        try:
            to_encode = data.copy()
            if expires_delta:
                expire = datetime.utcnow() + expires_delta
            else:
                expire = datetime.utcnow() + timedelta(minutes=30)

            to_encode.update({"exp": expire, "type": "access"})
            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            logger.info(f"访问token创建成功: user_id={data.get('user_id', 'unknown')}")
            return encoded_jwt
        except Exception as e:
            logger.error(f"创建访问token失败: {e}")
            raise

    def create_refresh_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """创建刷新token"""
        try:
            to_encode = data.copy()
            if expires_delta:
                expire = datetime.utcnow() + expires_delta
            else:
                expire = datetime.utcnow() + timedelta(days=7)

            to_encode.update({"exp": expire, "type": "refresh"})
            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            logger.info(f"刷新token创建成功: user_id={data.get('user_id', 'unknown')}")
            return encoded_jwt
        except Exception as e:
            logger.error(f"创建刷新token失败: {e}")
            raise

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """验证token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token已过期")
            return None
        except jwt.JWTError as e:
            logger.warning(f"Token验证失败: {e}")
            return None
        except Exception as e:
            logger.error(f"Token验证异常: {e}")
            return None

    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        """解码token（不验证过期时间）"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm], options={"verify_exp": False})
            return payload
        except jwt.JWTError as e:
            logger.warning(f"Token解码失败: {e}")
            return None
        except Exception as e:
            logger.error(f"Token解码异常: {e}")
            return None

    def hash_password(self, password: str) -> str:
        """哈希密码"""
        try:
            # 生成盐并哈希密码
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        except Exception as e:
            logger.error(f"密码哈希失败: {e}")
            raise

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """验证密码"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception as e:
            logger.error(f"密码验证失败: {e}")
            return False
