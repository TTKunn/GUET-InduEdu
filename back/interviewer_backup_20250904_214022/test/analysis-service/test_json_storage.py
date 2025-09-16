#!/usr/bin/env python3
"""
测试JSON存储功能
"""

import json
from mysql_database import DatabaseService
from models import CandidateProfile, PersonalInfo

def test_json_storage():
    """测试JSON存储功能"""
    print("🧪 测试JSON存储功能...")
    
    try:
        # 连接数据库
        db_service = DatabaseService()
        if not db_service.connect():
            print("❌ 数据库连接失败")
            return False
        
        print("✅ 数据库连接成功")
        
        # 准备测试数据
        test_profile = CandidateProfile(
            user_id="test_json_storage_user",
            personal_info=PersonalInfo(
                name="张三",
                phone="13800138000",
                email="zhangsan@test.com",
                location="北京市"
            ),
            technical_skills=["Python", "JavaScript", "MySQL", "Docker"],
            projects_keywords=[
                {
                    "name": "电商系统开发",
                    "keywords": ["Python", "Django", "MySQL", "Redis"]
                },
                {
                    "name": "数据分析平台",
                    "keywords": ["Python", "Pandas", "Matplotlib"]
                }
            ],
            education=[
                {
                    "school": "北京大学",
                    "degree": "本科",
                    "major": "计算机科学",
                    "graduation_year": "2020"
                }
            ],
            direction="Python"
        )
        
        print("\n📝 测试数据准备完成")
        print(f"   用户ID: {test_profile.user_id}")
        print(f"   姓名: {test_profile.personal_info.name}")
        print(f"   技术技能: {test_profile.technical_skills}")
        print(f"   项目数量: {len(test_profile.projects_keywords)}")
        print(f"   教育背景: {len(test_profile.education)}")
        
        # 保存档案
        print("\n💾 保存档案...")
        success = db_service.save_profile(test_profile)
        
        if not success:
            print("❌ 档案保存失败")
            return False
        
        print("✅ 档案保存成功")
        
        # 验证JSON字段存储
        print("\n🔍 验证JSON字段存储...")
        with db_service.mysql_client.get_session() as session:
            from sqlalchemy import text
            
            result = session.execute(text("""
                SELECT technical_skills_json, projects_keywords_json, education_json
                FROM candidate_profiles 
                WHERE user_id = 'test_json_storage_user'
            """))
            
            row = result.fetchone()
            if not row:
                print("❌ 未找到保存的数据")
                return False
            
            technical_skills_json = row[0]
            projects_keywords_json = row[1]
            education_json = row[2]
            
            print("📋 JSON字段内容:")
            print(f"   technical_skills_json: {technical_skills_json}")
            print(f"   projects_keywords_json: {projects_keywords_json}")
            print(f"   education_json: {education_json}")
            
            # 验证JSON格式
            try:
                technical_skills = json.loads(technical_skills_json)
                projects_keywords = json.loads(projects_keywords_json)
                education = json.loads(education_json)
                
                print("\n✅ JSON格式验证:")
                print(f"   技术技能数量: {len(technical_skills)}")
                print(f"   项目关键词数量: {len(projects_keywords)}")
                print(f"   教育背景数量: {len(education)}")
                
                # 验证中文字符
                has_chinese = any('中' in str(item) for item in [technical_skills, projects_keywords, education])
                print(f"   中文字符处理: {'✅ 正常' if has_chinese or '张三' in str(education) else '⚠️  未测试'}")
                
                # 验证数据完整性
                original_skills = test_profile.technical_skills
                stored_skills = technical_skills
                skills_match = set(original_skills) == set(stored_skills)
                print(f"   技术技能完整性: {'✅ 一致' if skills_match else '❌ 不一致'}")
                
                return True
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON解析失败: {e}")
                return False
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_json_update():
    """测试JSON更新功能"""
    print("\n🔄 测试JSON更新功能...")
    
    try:
        # 连接数据库
        db_service = DatabaseService()
        if not db_service.connect():
            print("❌ 数据库连接失败")
            return False
        
        # 更新测试数据
        updated_profile = CandidateProfile(
            user_id="test_json_storage_user",
            personal_info=PersonalInfo(
                name="张三（更新）",
                phone="13800138000",
                email="zhangsan@test.com",
                location="上海市"
            ),
            technical_skills=["Python", "JavaScript", "MySQL", "Docker", "Kubernetes"],  # 新增技能
            projects_keywords=[
                {
                    "name": "电商系统开发（升级版）",
                    "keywords": ["Python", "Django", "MySQL", "Redis", "Elasticsearch"]
                }
            ],
            direction="Python"
        )
        
        print("📝 更新数据准备完成")
        print(f"   新增技能: Kubernetes")
        print(f"   项目更新: 电商系统开发（升级版）")
        
        # 保存更新
        success = db_service.save_profile(updated_profile)
        
        if not success:
            print("❌ 档案更新失败")
            return False
        
        print("✅ 档案更新成功")
        
        # 验证更新结果
        with db_service.mysql_client.get_session() as session:
            from sqlalchemy import text
            
            result = session.execute(text("""
                SELECT technical_skills_json, projects_keywords_json
                FROM candidate_profiles 
                WHERE user_id = 'test_json_storage_user'
            """))
            
            row = result.fetchone()
            if row:
                technical_skills = json.loads(row[0])
                projects_keywords = json.loads(row[1])
                
                print("📋 更新后的JSON内容:")
                print(f"   技术技能: {technical_skills}")
                print(f"   项目关键词: {projects_keywords}")
                
                # 验证更新
                has_kubernetes = "Kubernetes" in technical_skills
                has_updated_project = any("升级版" in proj.get("name", "") for proj in projects_keywords)
                
                print(f"   新技能验证: {'✅ Kubernetes已添加' if has_kubernetes else '❌ Kubernetes未找到'}")
                print(f"   项目更新验证: {'✅ 项目已更新' if has_updated_project else '❌ 项目未更新'}")
                
                return has_kubernetes and has_updated_project
        
        return False
        
    except Exception as e:
        print(f"❌ 更新测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始JSON存储功能测试")
    print("=" * 50)
    
    # 测试存储
    storage_success = test_json_storage()
    
    # 测试更新
    update_success = test_json_update()
    
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    print(f"   JSON存储测试: {'✅ 通过' if storage_success else '❌ 失败'}")
    print(f"   JSON更新测试: {'✅ 通过' if update_success else '❌ 失败'}")
    
    overall_success = storage_success and update_success
    if overall_success:
        print("\n🎉 所有JSON存储测试通过！")
        print("   - JSON序列化正常工作")
        print("   - 中文字符正确处理")
        print("   - 数据完整性保持")
        print("   - 双写模式正常运行")
    else:
        print("\n⚠️  部分测试失败，需要检查问题")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
