#!/usr/bin/env python3
"""
检查MySQL数据库中的数据
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.mysql_client import MySQLClient
from sqlalchemy import text

def check_mysql_data():
    """检查MySQL数据库中的数据"""
    print("🔍 检查MySQL数据库中的数据...")
    
    try:
        # 创建MySQL客户端
        client = MySQLClient()
        
        # 检查连接
        if not client.test_connection():
            print("❌ MySQL连接失败")
            return False
        
        print("✅ MySQL连接成功")
        
        # 查询候选人档案表
        with client.get_session() as session:
            # 查询候选人档案数量
            result = session.execute(text("SELECT COUNT(*) as count FROM candidate_profiles"))
            profile_count = result.fetchone()[0]
            print(f"📊 候选人档案总数: {profile_count}")
            
            # 查询最近的几个档案
            result = session.execute(text("""
                SELECT user_id, name, email, direction, created_at 
                FROM candidate_profiles 
                ORDER BY created_at DESC 
                LIMIT 5
            """))
            
            profiles = result.fetchall()
            print(f"\n📋 最近的{len(profiles)}个档案:")
            for profile in profiles:
                print(f"   - 用户ID: {profile[0]}")
                print(f"     姓名: {profile[1] or '未知'}")
                print(f"     邮箱: {profile[2] or '未知'}")
                print(f"     方向: {profile[3] or '未知'}")
                print(f"     创建时间: {profile[4]}")
                print()
            
            # 查询技术技能表
            result = session.execute(text("SELECT COUNT(*) as count FROM technical_skills"))
            skills_count = result.fetchone()[0]
            print(f"🛠️  技术技能记录数: {skills_count}")
            
            # 查询项目表
            result = session.execute(text("SELECT COUNT(*) as count FROM projects"))
            projects_count = result.fetchone()[0]
            print(f"📁 项目记录数: {projects_count}")
            
            # 查询项目关键词表
            result = session.execute(text("SELECT COUNT(*) as count FROM project_keywords"))
            project_keywords_count = result.fetchone()[0]
            print(f"🔑 项目关键词记录数: {project_keywords_count}")
            
            # 查询提取关键词表
            result = session.execute(text("SELECT COUNT(*) as count FROM extracted_keywords"))
            extracted_keywords_count = result.fetchone()[0]
            print(f"🎯 提取关键词记录数: {extracted_keywords_count}")
            
            # 查询test_mysql_user的详细信息
            print(f"\n👤 查询test_mysql_user的详细信息:")
            result = session.execute(text("""
                SELECT user_id, name, phone, email, location, direction
                FROM candidate_profiles 
                WHERE user_id = 'test_mysql_user'
            """))
            
            user_profile = result.fetchone()
            if user_profile:
                print(f"   ✅ 找到用户档案:")
                print(f"     用户ID: {user_profile[0]}")
                print(f"     姓名: {user_profile[1]}")
                print(f"     电话: {user_profile[2]}")
                print(f"     邮箱: {user_profile[3]}")
                print(f"     地址: {user_profile[4]}")
                print(f"     方向: {user_profile[5]}")
                
                # 查询该用户的技术技能
                result = session.execute(text("""
                    SELECT skill_name FROM technical_skills 
                    WHERE user_id = 'test_mysql_user' 
                    ORDER BY sort_order
                """))
                skills = [row[0] for row in result.fetchall()]
                print(f"     技术技能({len(skills)}): {', '.join(skills)}")
                
                # 查询该用户的项目
                result = session.execute(text("""
                    SELECT name, description FROM projects 
                    WHERE user_id = 'test_mysql_user' 
                    ORDER BY sort_order
                """))
                projects = result.fetchall()
                print(f"     项目数量: {len(projects)}")
                for i, project in enumerate(projects, 1):
                    print(f"       {i}. {project[0]}")
                
            else:
                print("   ❌ 未找到test_mysql_user的档案")
        
        return True
        
    except Exception as e:
        print(f"❌ 检查数据失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始检查MySQL数据库数据")
    print("=" * 50)
    
    success = check_mysql_data()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 数据检查完成！")
    else:
        print("⚠️  数据检查失败！")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
