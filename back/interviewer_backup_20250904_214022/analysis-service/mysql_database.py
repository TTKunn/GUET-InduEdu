"""
MySQL数据库适配层 - 保持与MongoDB版本相同的接口
"""

import logging
import sys
import os
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from contextlib import contextmanager

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from database.mysql_client import MySQLClient
from models import CandidateProfile, profile_to_dict, dict_to_profile

logger = logging.getLogger(__name__)

class DatabaseService:
    """MySQL数据库服务类 - 兼容MongoDB接口"""
    
    def __init__(self):
        self.mysql_client = None
        self._connected = False
        
    def connect(self) -> bool:
        """连接数据库"""
        try:
            logger.info("连接MySQL数据库...")
            
            self.mysql_client = MySQLClient()
            
            # 测试连接
            if not self.mysql_client.test_connection():
                raise Exception("MySQL连接测试失败")
            
            # 创建表（如果不存在）
            self.mysql_client.create_tables()
            
            self._connected = True
            logger.info("✅ MySQL连接成功")
            return True
            
        except Exception as e:
            logger.error(f"❌ MySQL连接失败: {e}")
            return False
    
    def disconnect(self):
        """断开数据库连接"""
        if self.mysql_client:
            self.mysql_client = None
            self._connected = False
            logger.info("MySQL连接已断开")
    
    def is_connected(self) -> bool:
        """检查数据库连接状态"""
        if not self._connected or not self.mysql_client:
            return False
        
        try:
            return self.mysql_client.test_connection()
        except Exception:
            self._connected = False
            return False
    
    @contextmanager
    def ensure_connection(self):
        """确保数据库连接的上下文管理器"""
        if not self.is_connected():
            if not self.connect():
                raise ConnectionError("无法连接到数据库")
        
        try:
            yield
        except Exception as e:
            logger.error(f"数据库操作失败: {e}")
            raise
    
    def save_profile(self, profile: CandidateProfile, overwrite: bool = True) -> bool:
        """保存候选人档案"""
        with self.ensure_connection():
            try:
                profile.updated_at = datetime.now()
                profile_data = profile_to_dict(profile)
                
                # 使用MySQL客户端保存数据
                success = self.mysql_client.save_profile(profile_data)
                
                if success:
                    logger.info(f"档案已保存: user_id={profile.user_id}")
                else:
                    logger.error(f"档案保存失败: user_id={profile.user_id}")
                
                return success
                
            except Exception as e:
                logger.error(f"保存档案失败: user_id={profile.user_id}, error={e}")
                return False
    
    def get_profile(self, user_id: str) -> Optional[CandidateProfile]:
        """获取候选人档案"""
        with self.ensure_connection():
            try:
                # 使用MySQL客户端获取数据
                profile_data = self.mysql_client.get_profile(user_id)
                
                if profile_data:
                    # 转换为CandidateProfile对象
                    profile = dict_to_profile(profile_data)
                    logger.info(f"档案获取成功: user_id={user_id}")
                    return profile
                else:
                    logger.info(f"档案不存在: user_id={user_id}")
                    return None
                    
            except Exception as e:
                logger.error(f"获取档案失败: user_id={user_id}, error={e}")
                return None
    
    def profile_exists(self, user_id: str) -> bool:
        """检查档案是否存在"""
        with self.ensure_connection():
            try:
                profile_data = self.mysql_client.get_profile(user_id)
                return profile_data is not None
            except Exception as e:
                logger.error(f"检查档案存在性失败: user_id={user_id}, error={e}")
                return False
    
    def delete_profile(self, user_id: str) -> bool:
        """删除候选人档案"""
        with self.ensure_connection():
            try:
                # MySQL客户端暂未实现delete方法，返回False表示不支持
                logger.warning(f"删除功能暂未实现: user_id={user_id}")
                return False
            except Exception as e:
                logger.error(f"删除档案失败: user_id={user_id}, error={e}")
                return False
    
    def get_user_count(self) -> int:
        """获取用户总数"""
        with self.ensure_connection():
            try:
                count = self.mysql_client.get_user_count()
                logger.info(f"用户总数: {count}")
                return count
            except Exception as e:
                logger.error(f"获取用户总数失败: {e}")
                return 0
    
    def list_users(self, limit: int = 100, skip: int = 0) -> List[str]:
        """获取用户ID列表"""
        with self.ensure_connection():
            try:
                # MySQL客户端暂未实现list_users方法，返回空列表
                logger.warning("用户列表功能暂未实现")
                return []
            except Exception as e:
                logger.error(f"获取用户列表失败: {e}")
                return []
    
    def get_profiles_by_keywords(self, keywords: List[str], limit: int = 10) -> List[CandidateProfile]:
        """根据关键词搜索档案"""
        with self.ensure_connection():
            try:
                # MySQL客户端暂未实现关键词搜索方法，返回空列表
                logger.warning("关键词搜索功能暂未实现")
                return []
            except Exception as e:
                logger.error(f"关键词搜索失败: {e}")
                return []
    
    def get_database_stats(self) -> Dict[str, Any]:
        """获取数据库统计信息"""
        with self.ensure_connection():
            try:
                stats = {
                    "total_users": self.get_user_count(),
                    "database_type": "MySQL",
                    "connection_status": "connected" if self.is_connected() else "disconnected"
                }
                return stats
            except Exception as e:
                logger.error(f"获取数据库统计信息失败: {e}")
                return {"error": str(e)}
