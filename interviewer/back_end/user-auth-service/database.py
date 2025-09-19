"""
数据库操作服务
"""

import logging
from contextlib import contextmanager
from typing import Optional

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from config import MYSQL_URL, MYSQL_POOL_SIZE, MYSQL_MAX_OVERFLOW, MYSQL_POOL_TIMEOUT
from models import Base, User

logger = logging.getLogger(__name__)

class DatabaseService:
    """数据库服务类"""
    
    def __init__(self):
        """初始化数据库连接"""
        self.engine = None
        self.SessionLocal = None
        self._initialize_connection()
    
    def _initialize_connection(self):
        """初始化数据库连接"""
        try:
            # 创建数据库引擎
            self.engine = create_engine(
                MYSQL_URL,
                pool_pre_ping=True,  # 连接池预检查
                pool_recycle=3600,   # 连接回收时间
                pool_size=MYSQL_POOL_SIZE,
                max_overflow=MYSQL_MAX_OVERFLOW,
                pool_timeout=MYSQL_POOL_TIMEOUT,
                echo=False           # 不打印SQL语句
            )
            
            # 创建会话工厂
            self.SessionLocal = sessionmaker(bind=self.engine)
            
            # 测试连接
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            logger.info("✅ MySQL连接初始化成功")
            
        except Exception as e:
            logger.error(f"❌ MySQL连接初始化失败: {e}")
            logger.warning("⚠️  数据库服务将在离线模式下启动")
            self.engine = None
            self.SessionLocal = None
    
    @contextmanager
    def get_session(self):
        """获取数据库会话的上下文管理器"""
        if not self.SessionLocal:
            raise Exception("数据库连接未初始化")
            
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"数据库操作失败: {e}")
            raise
        finally:
            session.close()
    
    def test_connection(self) -> bool:
        """测试数据库连接"""
        try:
            with self.get_session() as session:
                session.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"数据库连接测试失败: {e}")
            return False
    
    def create_tables(self):
        """创建数据库表"""
        try:
            if self.engine:
                Base.metadata.create_all(bind=self.engine)
                logger.info("✅ 数据库表创建成功")
            else:
                logger.error("❌ 数据库引擎未初始化，无法创建表")
        except Exception as e:
            logger.error(f"❌ 数据库表创建失败: {e}")
    
    # ==================== 用户相关数据库操作 ====================

    def create_user(self, user_data: dict) -> Optional[User]:
        """创建用户"""
        try:
            with self.get_session() as session:
                user = User(**user_data)
                session.add(user)
                session.flush()  # 获取自动生成的ID
                # 刷新对象以获取数据库生成的字段
                session.refresh(user)
                logger.info(f"用户创建成功: user_id={user.user_id}, username={user.username}")
                # 返回用户数据的字典，避免会话问题
                return {
                    'id': user.id,
                    'user_id': user.user_id,
                    'username': user.username,
                    'email': user.email,
                    'is_active': user.is_active,
                    'is_verified': user.is_verified,
                    'created_at': user.created_at,
                    'last_login_at': user.last_login_at
                }
        except Exception as e:
            logger.error(f"创建用户失败: {e}")
            return None

    def get_user_by_username(self, username: str) -> Optional[dict]:
        """根据用户名获取用户"""
        try:
            with self.get_session() as session:
                user = session.query(User).filter(User.username == username).first()
                if user:
                    logger.info(f"根据用户名获取用户成功: username={username}")
                    return {
                        'id': user.id,
                        'user_id': user.user_id,
                        'username': user.username,
                        'email': user.email,
                        'password_hash': user.password_hash,
                        'is_active': user.is_active,
                        'is_verified': user.is_verified,
                        'created_at': user.created_at,
                        'last_login_at': user.last_login_at
                    }
                return None
        except Exception as e:
            logger.error(f"根据用户名获取用户失败: username={username}, error={e}")
            return None

    def get_user_by_email(self, email: str) -> Optional[dict]:
        """根据邮箱获取用户"""
        try:
            with self.get_session() as session:
                user = session.query(User).filter(User.email == email).first()
                if user:
                    logger.info(f"根据邮箱获取用户成功: email={email}")
                    return {
                        'id': user.id,
                        'user_id': user.user_id,
                        'username': user.username,
                        'email': user.email,
                        'password_hash': user.password_hash,
                        'is_active': user.is_active,
                        'is_verified': user.is_verified,
                        'created_at': user.created_at,
                        'last_login_at': user.last_login_at
                    }
                return None
        except Exception as e:
            logger.error(f"根据邮箱获取用户失败: email={email}, error={e}")
            return None

    def get_user_by_user_id(self, user_id: str) -> Optional[dict]:
        """根据user_id获取用户"""
        try:
            with self.get_session() as session:
                user = session.query(User).filter(User.user_id == user_id).first()
                if user:
                    logger.info(f"根据user_id获取用户成功: user_id={user_id}")
                    return {
                        'id': user.id,
                        'user_id': user.user_id,
                        'username': user.username,
                        'email': user.email,
                        'password_hash': user.password_hash,
                        'is_active': user.is_active,
                        'is_verified': user.is_verified,
                        'created_at': user.created_at,
                        'last_login_at': user.last_login_at
                    }
                return None
        except Exception as e:
            logger.error(f"根据user_id获取用户失败: user_id={user_id}, error={e}")
            return None

    def update_last_login(self, user_id: str) -> bool:
        """更新最后登录时间"""
        try:
            from datetime import datetime
            with self.get_session() as session:
                user = session.query(User).filter(User.user_id == user_id).first()
                if user:
                    user.last_login_at = datetime.now()
                    logger.info(f"更新最后登录时间成功: user_id={user_id}")
                    return True
                else:
                    logger.warning(f"用户不存在，无法更新登录时间: user_id={user_id}")
                    return False
        except Exception as e:
            logger.error(f"更新最后登录时间失败: user_id={user_id}, error={e}")
            return False

    def activate_user(self, user_id: str) -> bool:
        """激活用户"""
        try:
            with self.get_session() as session:
                user = session.query(User).filter(User.user_id == user_id).first()
                if user:
                    user.is_active = True
                    logger.info(f"用户激活成功: user_id={user_id}")
                    return True
                else:
                    logger.warning(f"用户不存在，无法激活: user_id={user_id}")
                    return False
        except Exception as e:
            logger.error(f"用户激活失败: user_id={user_id}, error={e}")
            return False

    def deactivate_user(self, user_id: str) -> bool:
        """停用用户"""
        try:
            with self.get_session() as session:
                user = session.query(User).filter(User.user_id == user_id).first()
                if user:
                    user.is_active = False
                    logger.info(f"用户停用成功: user_id={user_id}")
                    return True
                else:
                    logger.warning(f"用户不存在，无法停用: user_id={user_id}")
                    return False
        except Exception as e:
            logger.error(f"用户停用失败: user_id={user_id}, error={e}")
            return False

    def verify_user_email(self, user_id: str) -> bool:
        """验证用户邮箱"""
        try:
            with self.get_session() as session:
                user = session.query(User).filter(User.user_id == user_id).first()
                if user:
                    user.is_verified = True
                    logger.info(f"用户邮箱验证成功: user_id={user_id}")
                    return True
                else:
                    logger.warning(f"用户不存在，无法验证邮箱: user_id={user_id}")
                    return False
        except Exception as e:
            logger.error(f"用户邮箱验证失败: user_id={user_id}, error={e}")
            return False
