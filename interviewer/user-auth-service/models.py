"""
数据库模型和Pydantic模型定义
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, BigInteger, String, Boolean, TIMESTAMP, func, Index
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field, EmailStr, validator

# SQLAlchemy基类
Base = declarative_base()

# ==================== SQLAlchemy数据库模型 ====================

class User(Base):
    """用户认证表"""
    __tablename__ = 'users'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='自增主键')
    user_id = Column(String(100), unique=True, nullable=False, comment='用户唯一标识，关联candidate_profiles')
    username = Column(String(50), unique=True, nullable=False, comment='用户名')
    email = Column(String(100), unique=True, nullable=False, comment='邮箱')
    password_hash = Column(String(255), nullable=False, comment='密码哈希')
    is_active = Column(Boolean, default=True, comment='账户状态')
    is_verified = Column(Boolean, default=False, comment='邮箱验证状态')
    last_login_at = Column(TIMESTAMP, nullable=True, comment='最后登录时间')
    created_at = Column(TIMESTAMP, server_default=func.now(), comment='创建时间')
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment='更新时间')
    
    # 索引
    __table_args__ = (
        Index('idx_username', 'username'),
        Index('idx_email', 'email'),
        Index('idx_user_id', 'user_id'),
        Index('idx_active', 'is_active'),
    )

# ==================== Pydantic请求模型 ====================

class UserRegisterRequest(BaseModel):
    """用户注册请求"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱地址")
    password: str = Field(..., min_length=6, max_length=128, description="密码")

    @validator('username')
    def validate_username(cls, v):
        """验证用户名格式"""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('用户名只能包含字母、数字、下划线和连字符')
        return v.lower()

    @validator('password')
    def validate_password(cls, v):
        """验证密码强度"""
        if len(v) < 6:
            raise ValueError('密码长度至少6位')
        return v

class UserLoginRequest(BaseModel):
    """用户登录请求"""
    username: str = Field(..., description="用户名或邮箱")
    password: str = Field(..., description="密码")

class TokenRefreshRequest(BaseModel):
    """刷新token请求"""
    refresh_token: str = Field(..., description="刷新token")

# ==================== Pydantic响应模型 ====================

class UserResponse(BaseModel):
    """用户信息响应"""
    user_id: str
    username: str
    email: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login_at: Optional[datetime] = None

class AuthResponse(BaseModel):
    """认证响应"""
    success: bool
    message: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: Optional[int] = None
    user: Optional[UserResponse] = None

class TokenResponse(BaseModel):
    """Token响应"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class MessageResponse(BaseModel):
    """通用消息响应"""
    success: bool
    message: str

class HealthCheckResponse(BaseModel):
    """健康检查响应"""
    status: str
    timestamp: str
    service: str
    version: str
    database_connected: Optional[bool] = None
    error: Optional[str] = None

class UserStatusResponse(BaseModel):
    """用户状态响应"""
    success: bool
    user_id: str
    is_active: bool
    is_verified: bool
    message: str
