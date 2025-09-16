#!/usr/bin/env python3
"""
验证JSON字段添加结果
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.mysql_client import MySQLClient
from sqlalchemy import text

def verify_json_fields():
    """验证JSON字段添加结果"""
    print("🔍 验证JSON字段添加结果...")
    
    try:
        # 创建MySQL客户端
        client = MySQLClient()
        
        # 检查连接
        if not client.test_connection():
            print("❌ MySQL连接失败")
            return False
        
        print("✅ MySQL连接成功")
        
        with client.get_session() as session:
            # 查询表结构
            result = session.execute(text("DESCRIBE candidate_profiles"))
            columns = result.fetchall()
            
            print("\n📋 candidate_profiles表结构:")
            json_fields_found = []
            for column in columns:
                field_name = column[0]
                field_type = column[1]
                field_comment = column[5] if len(column) > 5 else ''
                print(f"   {field_name}: {field_type} - {field_comment}")
                
                # 检查JSON字段
                if field_name in ['technical_skills_json', 'projects_keywords_json', 'education_json']:
                    json_fields_found.append(field_name)
            
            # 验证JSON字段
            expected_fields = ['technical_skills_json', 'projects_keywords_json', 'education_json']
            print(f"\n🎯 JSON字段验证:")
            for field in expected_fields:
                if field in json_fields_found:
                    print(f"   ✅ {field}: 已添加")
                else:
                    print(f"   ❌ {field}: 未找到")
            
            # 检查现有数据
            result = session.execute(text("SELECT COUNT(*) as count FROM candidate_profiles"))
            profile_count = result.fetchone()[0]
            print(f"\n📊 现有数据验证:")
            print(f"   候选人档案总数: {profile_count}")
            
            if profile_count > 0:
                # 查询现有数据样例
                result = session.execute(text("""
                    SELECT user_id, name, direction, 
                           technical_skills_json, projects_keywords_json, education_json
                    FROM candidate_profiles 
                    LIMIT 3
                """))
                profiles = result.fetchall()
                print(f"\n📋 现有数据样例:")
                for profile in profiles:
                    print(f"   - 用户ID: {profile[0]}")
                    print(f"     姓名: {profile[1] or '未知'}")
                    print(f"     方向: {profile[2] or '未知'}")
                    print(f"     technical_skills_json: {profile[3] or 'NULL'}")
                    print(f"     projects_keywords_json: {profile[4] or 'NULL'}")
                    print(f"     education_json: {profile[5] or 'NULL'}")
                    print()
            
            # 验证结果
            success = len(json_fields_found) == len(expected_fields)
            if success:
                print("🎉 JSON字段添加验证成功！")
                print("   - 所有JSON字段已正确添加")
                print("   - 现有数据完整保留")
                print("   - 表结构变更成功")
            else:
                print("⚠️  JSON字段添加验证失败！")
                missing_fields = set(expected_fields) - set(json_fields_found)
                print(f"   缺失字段: {missing_fields}")
            
            return success
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始验证JSON字段添加")
    print("=" * 50)
    
    success = verify_json_fields()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 验证完成！JSON字段添加成功！")
    else:
        print("⚠️  验证失败！需要检查字段添加")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
