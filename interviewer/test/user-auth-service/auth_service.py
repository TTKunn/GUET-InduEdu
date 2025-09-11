"""
认证业务逻辑服务
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import uuid

from models import UserRegisterRequest, UserLoginRequest, AuthResponse, UserResponse
from database import DatabaseService
from auth.auth_handler import JWTHandler
from config import JWT_ACCESS_TOKEN_EXPIRE_MINUTES, JWT_REFRESH_TOKEN_EXPIRE_DAYS

logger = logging.getLogger(__name__)

class AuthService:
    """认证业务逻辑服务"""

    def __init__(self, db_service: DatabaseService, jwt_handler: JWTHandler):
        """初始化认证服务"""
        self.db = db_service
        self.jwt = jwt_handler

    def register_user(self, request: UserRegisterRequest) -> AuthResponse:
        """用户注册"""
        try:
            # 检查用户名是否已存在
            existing_user = self.db.get_user_by_username(request.username)
            if existing_user:
                return AuthResponse(
                    success=False,
                    message="用户名已存在"
                )

            # 检查邮箱是否已存在
            existing_email = self.db.get_user_by_email(request.email)
            if existing_email:
                return AuthResponse(
                    success=False,
                    message="邮箱已被注册"
                )

            # 生成用户ID和哈希密码
            user_id = self._generate_user_id()
            password_hash = self.jwt.hash_password(request.password)

            # 创建用户数据
            user_data = {
                "user_id": user_id,
                "username": request.username,
                "email": request.email,
                "password_hash": password_hash,
                "is_active": True,
                "is_verified": False
            }

            # 保存用户到数据库
            user_dict = self.db.create_user(user_data)
            if not user_dict:
                return AuthResponse(
                    success=False,
                    message="用户创建失败"
                )

            # 生成token
            token_data = {"user_id": user_dict["user_id"], "username": user_dict["username"]}
            access_token = self.jwt.create_access_token(
                token_data,
                timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
            )
            refresh_token = self.jwt.create_refresh_token(
                token_data,
                timedelta(days=JWT_REFRESH_TOKEN_EXPIRE_DAYS)
            )

            # 构建用户响应
            user_response = UserResponse(
                user_id=user_dict["user_id"],
                username=user_dict["username"],
                email=user_dict["email"],
                is_active=user_dict["is_active"],
                is_verified=user_dict["is_verified"],
                created_at=user_dict["created_at"],
                last_login_at=user_dict["last_login_at"]
            )

            return AuthResponse(
                success=True,
                message="注册成功",
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                user=user_response
            )

        except Exception as e:
            logger.error(f"用户注册失败: {e}")
            return AuthResponse(
                success=False,
                message=f"注册失败: {str(e)}"
            )

    def login_user(self, request: UserLoginRequest) -> AuthResponse:
        """用户登录"""
        try:
            # 根据用户名或邮箱查找用户
            user_dict = None
            if "@" in request.username:
                user_dict = self.db.get_user_by_email(request.username)
            else:
                user_dict = self.db.get_user_by_username(request.username)

            if not user_dict:
                return AuthResponse(
                    success=False,
                    message="用户名或密码错误"
                )

            # 检查用户状态
            if not user_dict["is_active"]:
                return AuthResponse(
                    success=False,
                    message="账户已被停用"
                )

            # 验证密码
            if not self.jwt.verify_password(request.password, user_dict["password_hash"]):
                return AuthResponse(
                    success=False,
                    message="用户名或密码错误"
                )

            # 更新最后登录时间
            self.db.update_last_login(user_dict["user_id"])

            # 生成token
            token_data = {"user_id": user_dict["user_id"], "username": user_dict["username"]}
            access_token = self.jwt.create_access_token(
                token_data,
                timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
            )
            refresh_token = self.jwt.create_refresh_token(
                token_data,
                timedelta(days=JWT_REFRESH_TOKEN_EXPIRE_DAYS)
            )

            # 构建用户响应
            user_response = UserResponse(
                user_id=user_dict["user_id"],
                username=user_dict["username"],
                email=user_dict["email"],
                is_active=user_dict["is_active"],
                is_verified=user_dict["is_verified"],
                created_at=user_dict["created_at"],
                last_login_at=datetime.now()  # 使用当前时间
            )

            return AuthResponse(
                success=True,
                message="登录成功",
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                user=user_response
            )

        except Exception as e:
            logger.error(f"用户登录失败: {e}")
            return AuthResponse(
                success=False,
                message=f"登录失败: {str(e)}"
            )

    def refresh_token(self, refresh_token: str) -> AuthResponse:
        """刷新token"""
        try:
            # 验证refresh token
            payload = self.jwt.verify_token(refresh_token)
            if not payload:
                return AuthResponse(
                    success=False,
                    message="刷新token无效或已过期"
                )

            # 检查token类型
            if payload.get("type") != "refresh":
                return AuthResponse(
                    success=False,
                    message="无效的token类型"
                )

            # 获取用户信息
            user_id = payload.get("user_id")
            user_dict = self.db.get_user_by_user_id(user_id)
            if not user_dict or not user_dict["is_active"]:
                return AuthResponse(
                    success=False,
                    message="用户不存在或已被停用"
                )

            # 生成新的access token
            token_data = {"user_id": user_dict["user_id"], "username": user_dict["username"]}
            access_token = self.jwt.create_access_token(
                token_data,
                timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
            )

            return AuthResponse(
                success=True,
                message="Token刷新成功",
                access_token=access_token,
                expires_in=JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
            )

        except Exception as e:
            logger.error(f"Token刷新失败: {e}")
            return AuthResponse(
                success=False,
                message=f"Token刷新失败: {str(e)}"
            )

    def get_current_user(self, token: str) -> Optional[UserResponse]:
        """根据token获取当前用户信息"""
        try:
            # 验证token
            payload = self.jwt.verify_token(token)
            if not payload:
                return None

            # 获取用户信息
            user_id = payload.get("user_id")
            user_dict = self.db.get_user_by_user_id(user_id)
            if not user_dict:
                return None

            return UserResponse(
                user_id=user_dict["user_id"],
                username=user_dict["username"],
                email=user_dict["email"],
                is_active=user_dict["is_active"],
                is_verified=user_dict["is_verified"],
                created_at=user_dict["created_at"],
                last_login_at=user_dict["last_login_at"]
            )

        except Exception as e:
            logger.error(f"获取当前用户失败: {e}")
            return None

    def logout_user(self, token: str) -> bool:
        """用户登出"""
        try:
            # 验证token
            payload = self.jwt.verify_token(token)
            if not payload:
                return False

            # 这里可以实现token黑名单机制
            # 目前简单返回True，表示登出成功
            logger.info(f"用户登出成功: user_id={payload.get('user_id')}")
            return True

        except Exception as e:
            logger.error(f"用户登出失败: {e}")
            return False

    def _generate_user_id(self) -> str:
        """生成用户ID"""
        return str(uuid.uuid4())
