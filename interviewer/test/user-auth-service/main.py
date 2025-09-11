"""
用户认证服务 - FastAPI应用主文件
"""

import logging
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

# 导入配置和服务
from config import (
    API_HOST, API_PORT, API_WORKERS,
    CORS_ORIGINS, CORS_METHODS, CORS_HEADERS,
    validate_config, get_config_info,
    JWT_SECRET_KEY, JWT_ALGORITHM
)
from models import (
    UserRegisterRequest, UserLoginRequest, TokenRefreshRequest,
    AuthResponse, UserResponse, MessageResponse, HealthCheckResponse
)
from database import DatabaseService
from auth_service import AuthService
from auth.auth_handler import JWTHandler
from auth.auth_bearer import JWTBearer

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 初始化服务实例
db_service = DatabaseService()
jwt_handler = JWTHandler(JWT_SECRET_KEY, JWT_ALGORITHM)
auth_service = AuthService(db_service, jwt_handler)
jwt_bearer = JWTBearer(jwt_handler)

# 应用启动和关闭处理
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("🚀 启动用户认证服务...")

    try:
        # 验证配置
        validate_config()
        logger.info("✅ 配置验证通过")

        # 创建数据库表
        db_service.create_tables()
        logger.info("✅ 数据库表检查完成")

        logger.info("🎉 服务启动完成")

    except Exception as e:
        logger.error(f"❌ 服务启动失败: {e}")
        raise

    yield

    # 关闭时执行
    logger.info("🛑 关闭用户认证服务...")
    logger.info("✅ 服务已关闭")

# 创建FastAPI应用
app = FastAPI(
    title="用户认证服务",
    description="AI智能面试官项目的用户注册、登录和认证服务",
    version="1.0.0",
    lifespan=lifespan
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS,
)

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """健康检查"""
    try:
        # 检查数据库连接
        db_connected = db_service.test_connection()

        status = "healthy" if db_connected else "unhealthy"

        return HealthCheckResponse(
            status=status,
            timestamp=datetime.now().isoformat(),
            service="user-auth-service",
            version="1.0.0",
            database_connected=db_connected
        )

    except Exception as e:
        logger.error(f"健康检查失败: {e}")
        return HealthCheckResponse(
            status="error",
            timestamp=datetime.now().isoformat(),
            service="user-auth-service",
            version="1.0.0",
            database_connected=False,
            error=str(e)
        )

# ==================== 认证相关API ====================

@app.post("/auth/register", response_model=AuthResponse)
async def register(request: UserRegisterRequest):
    """用户注册"""
    try:
        result = auth_service.register_user(request)
        return result
    except Exception as e:
        logger.error(f"注册接口异常: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"注册失败: {str(e)}"
        )

@app.post("/auth/login", response_model=AuthResponse)
async def login(request: UserLoginRequest):
    """用户登录"""
    try:
        result = auth_service.login_user(request)
        return result
    except Exception as e:
        logger.error(f"登录接口异常: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"登录失败: {str(e)}"
        )

@app.post("/auth/refresh", response_model=AuthResponse)
async def refresh_token(request: TokenRefreshRequest):
    """刷新token"""
    try:
        result = auth_service.refresh_token(request.refresh_token)
        return result
    except Exception as e:
        logger.error(f"刷新token接口异常: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"刷新token失败: {str(e)}"
        )

@app.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(token: str = Depends(jwt_bearer)):
    """获取当前用户信息"""
    try:
        user = auth_service.get_current_user(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取用户信息接口异常: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取用户信息失败: {str(e)}"
        )

@app.post("/auth/logout", response_model=MessageResponse)
async def logout(token: str = Depends(jwt_bearer)):
    """用户登出"""
    try:
        success = auth_service.logout_user(token)
        return MessageResponse(
            success=success,
            message="登出成功" if success else "登出失败"
        )
    except Exception as e:
        logger.error(f"登出接口异常: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"登出失败: {str(e)}"
        )

@app.get("/")
async def root():
    """根路径"""
    return {
        "service": "用户认证服务",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "register": "/auth/register",
            "login": "/auth/login",
            "refresh": "/auth/refresh",
            "me": "/auth/me",
            "logout": "/auth/logout"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        workers=API_WORKERS,
        reload=True
    )
