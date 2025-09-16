#!/usr/bin/env python3
"""
解释JSON读取 vs 表读取的区别
"""

import json
import time
from mysql_database import DatabaseService
from sqlalchemy import text

def demonstrate_reading_methods():
    """演示两种读取方式的区别"""
    print("🔍 演示JSON读取 vs 表读取的区别")
    print("=" * 60)
    
    try:
        # 连接数据库
        db_service = DatabaseService()
        if not db_service.connect():
            print("❌ 数据库连接失败")
            return
        
        test_user_id = "test_json_storage_user"
        
        # 方式1: JSON读取（新方式）
        print("📊 方式1: JSON读取（新方式）")
        start_time = time.time()
        
        with db_service.mysql_client.get_session() as session:
            # 一次查询获取所有JSON数据
            result = session.execute(text("""
                SELECT technical_skills_json, projects_keywords_json, education_json
                FROM candidate_profiles 
                WHERE user_id = :user_id
            """), {"user_id": test_user_id})
            
            row = result.fetchone()
            if row:
                # 解析JSON数据
                technical_skills = json.loads(row[0] or '[]')
                projects_keywords = json.loads(row[1] or '[]')
                education = json.loads(row[2] or '[]')
                
                json_time = time.time() - start_time
                print(f"   ⏱️  查询时间: {json_time:.4f}秒")
                print(f"   📝 SQL查询次数: 1次")
                print(f"   🎯 技术技能: {technical_skills}")
                print(f"   🎯 项目数量: {len(projects_keywords)}")
                print(f"   🎯 教育记录: {len(education)}")
        
        print("\n" + "-" * 60)
        
        # 方式2: 表读取（传统方式）
        print("📊 方式2: 表读取（传统方式）")
        start_time = time.time()
        
        with db_service.mysql_client.get_session() as session:
            # 查询1: 技术技能表
            result1 = session.execute(text("""
                SELECT skill_name FROM technical_skills 
                WHERE user_id = :user_id 
                ORDER BY sort_order
            """), {"user_id": test_user_id})
            technical_skills_table = [row[0] for row in result1.fetchall()]
            
            # 查询2: 项目关键词表
            result2 = session.execute(text("""
                SELECT project_name, keyword FROM project_keywords 
                WHERE user_id = :user_id 
                ORDER BY project_name, sort_order
            """), {"user_id": test_user_id})
            
            # 组装项目关键词数据
            projects_kw_dict = {}
            for row in result2.fetchall():
                project_name, keyword = row
                if project_name not in projects_kw_dict:
                    projects_kw_dict[project_name] = []
                projects_kw_dict[project_name].append(keyword)
            
            projects_keywords_table = [
                {'name': name, 'keywords': keywords}
                for name, keywords in projects_kw_dict.items()
            ]
            
            # 查询3: 提取关键词表
            result3 = session.execute(text("""
                SELECT keyword FROM extracted_keywords 
                WHERE user_id = :user_id 
                ORDER BY sort_order
            """), {"user_id": test_user_id})
            extracted_keywords_table = [row[0] for row in result3.fetchall()]
            
            table_time = time.time() - start_time
            print(f"   ⏱️  查询时间: {table_time:.4f}秒")
            print(f"   📝 SQL查询次数: 3次")
            print(f"   🎯 技术技能: {technical_skills_table}")
            print(f"   🎯 项目数量: {len(projects_keywords_table)}")
            print(f"   🎯 提取关键词: {extracted_keywords_table}")
        
        print("\n" + "=" * 60)
        print("📈 性能对比:")
        if 'json_time' in locals() and 'table_time' in locals():
            improvement = ((table_time - json_time) / table_time) * 100
            print(f"   JSON读取时间: {json_time:.4f}秒")
            print(f"   表读取时间: {table_time:.4f}秒")
            print(f"   性能提升: {improvement:.1f}%")
            print(f"   查询次数减少: 3次 → 1次 (减少67%)")
        
        print("\n📋 存储空间对比:")
        print("   JSON方式: 3个TEXT字段")
        print("   表方式: 可能数百行记录分散在3个表中")
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    demonstrate_reading_methods()
