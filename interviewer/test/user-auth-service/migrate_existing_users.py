#!/usr/bin/env python3
"""
现有用户数据迁移脚本
将candidate_profiles表中的现有用户同步到users表中
为所有用户设置默认密码123456（bcrypt加密）
"""

import sys
import os
import logging
from datetime import datetime
import bcrypt
import uuid

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import DatabaseService
from config import validate_config

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class UserMigrationService:
    """用户数据迁移服务"""
    
    def __init__(self):
        """初始化迁移服务"""
        self.db = DatabaseService()
        self.default_password = "123456"
        
    def hash_password(self, password: str) -> str:
        """使用bcrypt加密密码"""
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        return password_hash.decode('utf-8')
    
    def get_existing_users_from_profiles(self):
        """从candidate_profiles表获取现有用户数据"""
        try:
            with self.db.get_session() as session:
                # 查询所有有效的用户数据
                from sqlalchemy import text
                query = text("""
                SELECT DISTINCT user_id, name, email
                FROM candidate_profiles
                WHERE user_id IS NOT NULL
                AND user_id != ''
                AND user_id NOT IN (SELECT user_id FROM users WHERE user_id IS NOT NULL)
                ORDER BY user_id
                """)
                result = session.execute(query)
                users = result.fetchall()

                logger.info(f"找到 {len(users)} 个需要迁移的用户")
                return users

        except Exception as e:
            logger.error(f"获取现有用户数据失败: {e}")
            return []
    
    def create_username_from_user_id(self, user_id: str) -> str:
        """根据user_id生成用户名"""
        # 如果user_id看起来像用户名，直接使用
        if len(user_id) <= 50 and user_id.replace('_', '').replace('-', '').isalnum():
            return user_id
        
        # 否则生成一个基于user_id的用户名
        return f"user_{user_id[:20]}"
    
    def migrate_user_to_auth_table(self, user_id: str, name: str, email: str):
        """将单个用户迁移到users表"""
        try:
            with self.db.get_session() as session:
                from sqlalchemy import text
                # 检查用户是否已存在
                existing_user = session.execute(
                    text("SELECT id FROM users WHERE user_id = :user_id"),
                    {"user_id": user_id}
                ).fetchone()

                if existing_user:
                    logger.info(f"用户 {user_id} 已存在，跳过")
                    return True
                
                # 生成用户名
                username = self.create_username_from_user_id(user_id)
                
                # 检查用户名是否重复
                counter = 1
                original_username = username
                while True:
                    existing_username = session.execute(
                        text("SELECT id FROM users WHERE username = :username"),
                        {"username": username}
                    ).fetchone()

                    if not existing_username:
                        break

                    username = f"{original_username}_{counter}"
                    counter += 1

                # 处理邮箱
                if not email or email == '':
                    email = f"{username}@example.com"

                # 检查邮箱是否重复
                counter = 1
                original_email = email
                while True:
                    existing_email = session.execute(
                        text("SELECT id FROM users WHERE email = :email"),
                        {"email": email}
                    ).fetchone()

                    if not existing_email:
                        break

                    # 在@前添加数字
                    email_parts = original_email.split('@')
                    email = f"{email_parts[0]}_{counter}@{email_parts[1]}"
                    counter += 1
                
                # 加密默认密码
                password_hash = self.hash_password(self.default_password)
                
                # 插入用户数据
                insert_query = text("""
                INSERT INTO users (
                    user_id, username, email, password_hash,
                    is_active, is_verified, created_at, updated_at
                ) VALUES (:user_id, :username, :email, :password_hash, :is_active, :is_verified, :created_at, :updated_at)
                """)

                now = datetime.now()
                session.execute(insert_query, {
                    "user_id": user_id,
                    "username": username,
                    "email": email,
                    "password_hash": password_hash,
                    "is_active": True,
                    "is_verified": False,
                    "created_at": now,
                    "updated_at": now
                })
                
                logger.info(f"成功迁移用户: {user_id} -> {username} ({email})")
                return True
                
        except Exception as e:
            logger.error(f"迁移用户 {user_id} 失败: {e}")
            return False
    
    def run_migration(self):
        """执行完整的用户迁移"""
        logger.info("开始用户数据迁移...")
        
        try:
            # 验证配置
            validate_config()
            logger.info("配置验证通过")
            
            # 获取现有用户
            existing_users = self.get_existing_users_from_profiles()
            
            if not existing_users:
                logger.info("没有需要迁移的用户")
                return True
            
            # 迁移每个用户
            success_count = 0
            failed_count = 0
            
            for user_data in existing_users:
                user_id, name, email = user_data
                
                if self.migrate_user_to_auth_table(user_id, name, email):
                    success_count += 1
                else:
                    failed_count += 1
            
            logger.info(f"迁移完成: 成功 {success_count} 个，失败 {failed_count} 个")
            
            # 显示迁移结果
            self.show_migration_results()
            
            return failed_count == 0
            
        except Exception as e:
            logger.error(f"用户迁移失败: {e}")
            return False
    
    def show_migration_results(self):
        """显示迁移结果"""
        try:
            with self.db.get_session() as session:
                from sqlalchemy import text
                # 统计users表中的用户数量
                result = session.execute(text("SELECT COUNT(*) FROM users"))
                user_count = result.fetchone()[0]

                logger.info(f"users表中现有用户总数: {user_count}")

                # 显示最近迁移的用户
                result = session.execute(text("""
                    SELECT user_id, username, email, created_at
                    FROM users
                    ORDER BY created_at DESC
                    LIMIT 10
                """))

                recent_users = result.fetchall()
                logger.info("最近的用户记录:")
                for user in recent_users:
                    logger.info(f"  {user[0]} -> {user[1]} ({user[2]}) - {user[3]}")

        except Exception as e:
            logger.error(f"显示迁移结果失败: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("用户数据迁移脚本")
    print("=" * 60)
    print(f"默认密码: 123456 (将使用bcrypt加密)")
    print("功能: 将candidate_profiles表中的用户同步到users表")
    print("=" * 60)
    
    # 确认执行
    confirm = input("确认执行迁移? (y/N): ").strip().lower()
    if confirm != 'y':
        print("迁移已取消")
        return
    
    # 执行迁移
    migration_service = UserMigrationService()
    success = migration_service.run_migration()
    
    if success:
        print("\n✅ 用户迁移成功完成!")
        print("所有现有用户已同步到users表，默认密码为: 123456")
    else:
        print("\n❌ 用户迁移过程中出现错误，请检查日志")
        sys.exit(1)

if __name__ == "__main__":
    main()
