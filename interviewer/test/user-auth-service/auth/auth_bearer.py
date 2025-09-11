"""
JWT Bearer认证中间件
"""

import logging
from typing import Optional

from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth_handler import JWTHandler

logger = logging.getLogger(__name__)

class JWTBearer(HTTPBearer):
    """JWT Bearer认证中间件"""

    def __init__(self, jwt_handler: JWTHandler, auto_error: bool = True):
        """初始化JWT Bearer中间件"""
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.jwt_handler = jwt_handler

    async def __call__(self, request: Request) -> Optional[str]:
        """验证JWT token"""
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid authentication scheme."
                )

            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid token or expired token."
                )

            return credentials.credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization code."
            )

    def verify_jwt(self, token: str) -> bool:
        """验证JWT token"""
        try:
            payload = self.jwt_handler.verify_token(token)
            return payload is not None
        except Exception as e:
            logger.error(f"JWT验证失败: {e}")
            return False
