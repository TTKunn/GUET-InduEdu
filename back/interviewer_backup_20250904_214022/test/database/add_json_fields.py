#!/usr/bin/env python3
"""
使用SQLAlchemy添加JSON字段到candidate_profiles表
"""

import sys
import os

# 添加analysis-service目录到路径
analysis_service_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'analysis-service')
sys.path.insert(0, analysis_service_dir)

from mysql_database import DatabaseService
from sqlalchemy import text

def add_json_fields():
    """添加JSON字段到candidate_profiles表"""
    print("🔧 添加JSON字段到candidate_profiles表...")

    try:
        # 创建数据库服务
        db_service = DatabaseService()

        # 连接数据库
        if not db_service.connect():
            print("❌ MySQL连接失败")
            return False

        print("✅ MySQL连接成功")
        client = db_service.mysql_client
        
        with client.get_session() as session:
            # 检查字段是否已存在
            result = session.execute(text("DESCRIBE candidate_profiles"))
            existing_columns = [row[0] for row in result.fetchall()]
            
            json_fields = {
                'technical_skills_json': 'TEXT COMMENT "技术技能JSON存储"',
                'projects_keywords_json': 'TEXT COMMENT "项目关键词JSON存储"',
                'education_json': 'TEXT COMMENT "教育背景JSON存储"'
            }
            
            fields_to_add = []
            for field_name, field_def in json_fields.items():
                if field_name not in existing_columns:
                    fields_to_add.append(f"ADD COLUMN {field_name} {field_def}")
                else:
                    print(f"   ⚠️  字段 {field_name} 已存在，跳过")
            
            if fields_to_add:
                # 构建ALTER TABLE语句
                alter_sql = f"ALTER TABLE candidate_profiles {', '.join(fields_to_add)}"
                print(f"\n🔧 执行SQL: {alter_sql}")
                
                # 执行ALTER TABLE
                session.execute(text(alter_sql))
                session.commit()
                print("✅ JSON字段添加成功")
            else:
                print("✅ 所有JSON字段已存在，无需添加")
            
            # 验证字段添加结果
            result = session.execute(text("DESCRIBE candidate_profiles"))
            columns = result.fetchall()
            
            print("\n📋 更新后的表结构:")
            json_fields_found = []
            for column in columns:
                field_name = column[0]
                field_type = column[1]
                if field_name in ['technical_skills_json', 'projects_keywords_json', 'education_json']:
                    json_fields_found.append(field_name)
                    print(f"   ✅ {field_name}: {field_type}")
            
            # 检查现有数据
            result = session.execute(text("SELECT COUNT(*) as count FROM candidate_profiles"))
            profile_count = result.fetchone()[0]
            print(f"\n📊 数据完整性验证:")
            print(f"   候选人档案总数: {profile_count}")
            
            # 验证结果
            expected_fields = ['technical_skills_json', 'projects_keywords_json', 'education_json']
            success = all(field in json_fields_found for field in expected_fields)
            
            if success:
                print("\n🎉 JSON字段添加完成！")
                print("   - 所有JSON字段已正确添加")
                print("   - 现有数据完整保留")
                print("   - 可以开始下一阶段的开发")
            else:
                missing_fields = set(expected_fields) - set(json_fields_found)
                print(f"\n❌ 部分字段添加失败: {missing_fields}")
            
            return success
        
    except Exception as e:
        print(f"❌ 添加JSON字段失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始添加JSON字段")
    print("=" * 50)
    
    success = add_json_fields()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 JSON字段添加成功！可以继续下一个任务。")
    else:
        print("⚠️  JSON字段添加失败！需要检查问题。")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
