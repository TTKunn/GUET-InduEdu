"""
数据库服务
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, DuplicateKeyError, PyMongoError
from contextlib import contextmanager

from config import (
    MONGO_URI, MONGO_DB, MONGO_COLLECTION,
    MONGO_CONNECT_TIMEOUT, MONGO_SERVER_SELECTION_TIMEOUT
)
from models import CandidateProfile, profile_to_dict, dict_to_profile

logger = logging.getLogger(__name__)

class DatabaseService:
    """数据库服务类"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self._connected = False
        
    def connect(self) -> bool:
        """连接数据库"""
        try:
            logger.info(f"连接MongoDB: {MONGO_URI}")
            
            self.client = MongoClient(
                MONGO_URI,
                connectTimeoutMS=MONGO_CONNECT_TIMEOUT,
                serverSelectionTimeoutMS=MONGO_SERVER_SELECTION_TIMEOUT
            )
            
            # 测试连接
            self.client.server_info()
            
            self.db = self.client[MONGO_DB]
            self.collection = self.db[MONGO_COLLECTION]
            
            # 创建索引
            self._create_indexes()
            
            self._connected = True
            logger.info("✅ MongoDB连接成功")
            return True
            
        except ConnectionFailure as e:
            logger.error(f"❌ MongoDB连接失败: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ 数据库初始化失败: {e}")
            return False
    
    def _create_indexes(self):
        """创建数据库索引"""
        try:
            # 用户ID唯一索引
            self.collection.create_index([("user_id", ASCENDING)], unique=True)
            
            # 创建时间索引
            self.collection.create_index([("created_at", DESCENDING)])
            
            # 更新时间索引
            self.collection.create_index([("updated_at", DESCENDING)])
            
            # 关键词索引（用于搜索）
            self.collection.create_index([("extracted_keywords", ASCENDING)])
            self.collection.create_index([("technical_keywords", ASCENDING)])
            
            logger.info("✅ 数据库索引创建完成")
            
        except Exception as e:
            logger.warning(f"⚠️ 索引创建失败: {e}")
    
    def disconnect(self):
        """断开数据库连接"""
        if self.client:
            self.client.close()
            self._connected = False
            logger.info("数据库连接已断开")
    
    def is_connected(self) -> bool:
        """检查数据库连接状态"""
        if not self._connected or not self.client:
            return False
        
        try:
            self.client.server_info()
            return True
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
                
                if overwrite:
                    # 使用upsert更新或插入
                    result = self.collection.replace_one(
                        {"user_id": profile.user_id},
                        profile_data,
                        upsert=True
                    )
                    logger.info(f"档案已保存: user_id={profile.user_id}")
                else:
                    # 仅在不存在时插入
                    try:
                        result = self.collection.insert_one(profile_data)
                        logger.info(f"新档案已创建: user_id={profile.user_id}")
                    except DuplicateKeyError:
                        logger.warning(f"档案已存在，跳过保存: user_id={profile.user_id}")
                        return False
                
                return True
                
            except Exception as e:
                logger.error(f"保存档案失败: user_id={profile.user_id}, error={e}")
                return False
    
    def get_profile(self, user_id: str) -> Optional[CandidateProfile]:
        """获取候选人档案"""
        with self.ensure_connection():
            try:
                profile_data = self.collection.find_one({"user_id": user_id})
                
                if profile_data:
                    return dict_to_profile(profile_data)
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
                count = self.collection.count_documents({"user_id": user_id}, limit=1)
                return count > 0
            except Exception as e:
                logger.error(f"检查档案存在性失败: user_id={user_id}, error={e}")
                return False
    
    def delete_profile(self, user_id: str) -> bool:
        """删除候选人档案"""
        with self.ensure_connection():
            try:
                result = self.collection.delete_one({"user_id": user_id})
                
                if result.deleted_count > 0:
                    logger.info(f"档案已删除: user_id={user_id}")
                    return True
                else:
                    logger.warning(f"档案不存在，无法删除: user_id={user_id}")
                    return False
                    
            except Exception as e:
                logger.error(f"删除档案失败: user_id={user_id}, error={e}")
                return False
    
    def get_profile_count(self) -> int:
        """获取档案总数"""
        with self.ensure_connection():
            try:
                count = self.collection.count_documents({})
                return count
            except Exception as e:
                logger.error(f"获取档案总数失败: error={e}")
                return 0
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取数据库统计信息"""
        with self.ensure_connection():
            try:
                stats = {
                    "total_profiles": self.get_profile_count(),
                    "last_updated": None
                }
                
                # 获取最近更新时间
                latest = self.collection.find_one(sort=[("updated_at", DESCENDING)])
                if latest:
                    stats["last_updated"] = latest.get("updated_at")
                
                return stats
                
            except Exception as e:
                logger.error(f"获取统计信息失败: error={e}")
                return {}

# 全局数据库实例
db_service = DatabaseService()
