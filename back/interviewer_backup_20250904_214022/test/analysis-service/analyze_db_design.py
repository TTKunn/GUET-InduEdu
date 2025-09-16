#!/usr/bin/env python3
"""
分析MySQL数据库设计和使用情况
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.mysql_client import MySQLClient
from sqlalchemy import text

def analyze_database_usage():
    """分析数据库使用情况"""
    print("🔍 分析MySQL数据库设计和使用情况...")
    
    try:
        client = MySQLClient()
        
        with client.get_session() as session:
            # 分析各表的数据分布
            tables = [
                ('candidate_profiles', '候选人档案主表'),
                ('work_experiences', '工作经验表'),
                ('projects', '项目经验表'),
                ('technical_skills', '技术技能表'),
                ('project_keywords', '项目关键词表'),
                ('extracted_keywords', '提取关键词表')
            ]
            
            print("📊 各表数据统计:")
            for table_name, description in tables:
                result = session.execute(text(f"SELECT COUNT(*) as count FROM {table_name}"))
                count = result.fetchone()[0]
                print(f"   {description}: {count} 条记录")
            
            # 分析字段使用情况
            print("\n🔍 字段使用情况分析:")
            
            # 候选人档案表字段使用情况
            print("\n1. candidate_profiles 表字段使用情况:")
            result = session.execute(text("""
                SELECT 
                    COUNT(*) as total,
                    COUNT(name) as name_count,
                    COUNT(phone) as phone_count,
                    COUNT(email) as email_count,
                    COUNT(location) as location_count,
                    COUNT(education) as education_count,
                    COUNT(direction) as direction_count
                FROM candidate_profiles
            """))
            row = result.fetchone()
            total = row[0]
            if total > 0:
                print(f"   总记录数: {total}")
                print(f"   name 使用率: {row[1]}/{total} ({row[1]/total*100:.1f}%)")
                print(f"   phone 使用率: {row[2]}/{total} ({row[2]/total*100:.1f}%)")
                print(f"   email 使用率: {row[3]}/{total} ({row[3]/total*100:.1f}%)")
                print(f"   location 使用率: {row[4]}/{total} ({row[4]/total*100:.1f}%)")
                print(f"   education 使用率: {row[5]}/{total} ({row[5]/total*100:.1f}%)")
                print(f"   direction 使用率: {row[6]}/{total} ({row[6]/total*100:.1f}%)")
            
            # 技术技能表字段使用情况
            print("\n2. technical_skills 表字段使用情况:")
            result = session.execute(text("""
                SELECT 
                    COUNT(*) as total,
                    COUNT(skill_category) as category_count,
                    COUNT(proficiency_level) as proficiency_count
                FROM technical_skills
            """))
            row = result.fetchone()
            total = row[0]
            if total > 0:
                print(f"   总记录数: {total}")
                print(f"   skill_category 使用率: {row[1]}/{total} ({row[1]/total*100:.1f}%)")
                print(f"   proficiency_level 使用率: {row[2]}/{total} ({row[2]/total*100:.1f}%)")
            
            # 项目关键词表字段使用情况
            print("\n3. project_keywords 表字段使用情况:")
            result = session.execute(text("""
                SELECT 
                    COUNT(*) as total,
                    COUNT(keyword_type) as type_count,
                    COUNT(relevance_score) as score_count
                FROM project_keywords
            """))
            row = result.fetchone()
            total = row[0]
            if total > 0:
                print(f"   总记录数: {total}")
                print(f"   keyword_type 使用率: {row[1]}/{total} ({row[1]/total*100:.1f}%)")
                print(f"   relevance_score 使用率: {row[2]}/{total} ({row[2]/total*100:.1f}%)")
            
            # 提取关键词表字段使用情况
            print("\n4. extracted_keywords 表字段使用情况:")
            result = session.execute(text("""
                SELECT 
                    COUNT(*) as total,
                    COUNT(keyword_category) as category_count,
                    COUNT(extraction_source) as source_count,
                    COUNT(frequency) as frequency_count,
                    COUNT(importance_score) as importance_count
                FROM extracted_keywords
            """))
            row = result.fetchone()
            total = row[0]
            if total > 0:
                print(f"   总记录数: {total}")
                print(f"   keyword_category 使用率: {row[1]}/{total} ({row[1]/total*100:.1f}%)")
                print(f"   extraction_source 使用率: {row[2]}/{total} ({row[2]/total*100:.1f}%)")
                print(f"   frequency 使用率: {row[3]}/{total} ({row[3]/total*100:.1f}%)")
                print(f"   importance_score 使用率: {row[4]}/{total} ({row[4]/total*100:.1f}%)")
            
            # 查看实际数据样例
            print("\n📋 实际数据样例:")
            
            # 技术技能样例
            result = session.execute(text("""
                SELECT skill_name, skill_category, proficiency_level 
                FROM technical_skills 
                LIMIT 5
            """))
            skills = result.fetchall()
            print(f"\n   技术技能样例:")
            for skill in skills:
                print(f"     - {skill[0]} | 分类: {skill[1] or 'NULL'} | 熟练度: {skill[2] or 'NULL'}")
            
            # 项目关键词样例
            result = session.execute(text("""
                SELECT project_name, keyword, keyword_type, relevance_score 
                FROM project_keywords 
                LIMIT 5
            """))
            keywords = result.fetchall()
            print(f"\n   项目关键词样例:")
            for kw in keywords:
                print(f"     - 项目: {kw[0]} | 关键词: {kw[1]} | 类型: {kw[2] or 'NULL'} | 得分: {kw[3] or 'NULL'}")
            
            # 提取关键词样例
            result = session.execute(text("""
                SELECT keyword, keyword_category, extraction_source, frequency, importance_score 
                FROM extracted_keywords 
                LIMIT 5
            """))
            extracted = result.fetchall()
            print(f"\n   提取关键词样例:")
            for ext in extracted:
                print(f"     - {ext[0]} | 分类: {ext[1] or 'NULL'} | 来源: {ext[2] or 'NULL'} | 频次: {ext[3] or 'NULL'} | 重要性: {ext[4] or 'NULL'}")
        
        return True
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始分析MySQL数据库设计")
    print("=" * 60)
    
    success = analyze_database_usage()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 数据库分析完成！")
    else:
        print("⚠️  数据库分析失败！")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
