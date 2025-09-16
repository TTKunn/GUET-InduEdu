#!/usr/bin/env python3
"""
简单验证JSON字段
"""

from mysql_database import DatabaseService
from sqlalchemy import text

def main():
    print("🔍 验证JSON字段...")
    
    try:
        # 连接数据库
        db_service = DatabaseService()
        if not db_service.connect():
            print("❌ 数据库连接失败")
            return False
        
        print("✅ 数据库连接成功")
        
        # 获取表结构
        with db_service.mysql_client.get_session() as session:
            # 先尝试添加字段
            try:
                session.execute(text("""
                    ALTER TABLE candidate_profiles 
                    ADD COLUMN IF NOT EXISTS technical_skills_json TEXT COMMENT '技术技能JSON存储',
                    ADD COLUMN IF NOT EXISTS projects_keywords_json TEXT COMMENT '项目关键词JSON存储',
                    ADD COLUMN IF NOT EXISTS education_json TEXT COMMENT '教育背景JSON存储'
                """))
                print("✅ JSON字段添加尝试完成")
            except Exception as e:
                print(f"⚠️  字段可能已存在: {e}")
            
            # 验证字段
            result = session.execute(text("DESCRIBE candidate_profiles"))
            columns = [row[0] for row in result.fetchall()]
            
            json_fields = ['technical_skills_json', 'projects_keywords_json', 'education_json']
            found_fields = []
            
            for field in json_fields:
                if field in columns:
                    found_fields.append(field)
                    print(f"   ✅ {field}: 已存在")
                else:
                    print(f"   ❌ {field}: 未找到")
            
            # 检查数据
            result = session.execute(text("SELECT COUNT(*) FROM candidate_profiles"))
            count = result.fetchone()[0]
            print(f"\n📊 候选人档案数量: {count}")
            
            success = len(found_fields) == len(json_fields)
            if success:
                print("\n🎉 JSON字段验证成功！")
            else:
                print(f"\n❌ 缺失字段: {set(json_fields) - set(found_fields)}")
            
            return success
            
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n结果: {'成功' if success else '失败'}")
