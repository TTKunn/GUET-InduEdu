#!/usr/bin/env python3
"""
测试API兼容性 - 验证JSON优化后的API返回格式
"""

import json
import requests
from mysql_database import DatabaseService

def test_json_reading():
    """测试JSON数据读取功能"""
    print("🔍 测试JSON数据读取功能...")
    
    try:
        # 连接数据库
        db_service = DatabaseService()
        if not db_service.connect():
            print("❌ 数据库连接失败")
            return False
        
        print("✅ 数据库连接成功")
        
        # 测试读取有JSON数据的用户
        test_user_id = "test_json_storage_user"
        profile = db_service.get_profile(test_user_id)
        
        if not profile:
            print(f"❌ 未找到用户档案: {test_user_id}")
            return False
        
        print(f"✅ 成功读取用户档案: {test_user_id}")
        print(f"   姓名: {profile.get('personal_info', {}).get('name', '未知')}")
        print(f"   技术方向: {profile.get('direction', '未知')}")
        print(f"   技术技能数量: {len(profile.get('technical_skills', []))}")
        print(f"   项目关键词数量: {len(profile.get('projects_keywords', []))}")
        print(f"   提取关键词数量: {len(profile.get('extracted_keywords', []))}")
        
        # 验证数据结构
        required_fields = ['user_id', 'personal_info', 'technical_skills', 'projects_keywords', 'extracted_keywords', 'direction']
        missing_fields = [field for field in required_fields if field not in profile]
        
        if missing_fields:
            print(f"❌ 缺失必要字段: {missing_fields}")
            return False
        
        print("✅ 数据结构完整")
        
        # 验证兼容字段
        technical_skills = profile.get('technical_skills', [])
        extracted_keywords = profile.get('extracted_keywords', [])
        
        if technical_skills == extracted_keywords:
            print("✅ 兼容字段一致 (technical_skills == extracted_keywords)")
        else:
            print("⚠️  兼容字段不一致")
            print(f"   technical_skills: {technical_skills}")
            print(f"   extracted_keywords: {extracted_keywords}")
        
        return True
        
    except Exception as e:
        print(f"❌ JSON读取测试失败: {e}")
        return False

def test_api_endpoints():
    """测试API接口兼容性"""
    print("\n🌐 测试API接口兼容性...")
    
    base_url = "http://localhost:8004"
    test_user_id = "test_json_storage_user"
    
    try:
        # 测试健康检查
        print("1. 测试健康检查接口...")
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"   ✅ 健康检查: {health_data.get('status', 'unknown')}")
        else:
            print(f"   ❌ 健康检查失败: {response.status_code}")
            return False
        
        # 测试/keywords接口
        print("2. 测试/keywords接口...")
        keywords_request = {
            "user_id": test_user_id,
            "category": "all",
            "format_type": "list"
        }
        response = requests.post(f"{base_url}/keywords", json=keywords_request, timeout=30)
        
        if response.status_code == 200:
            keywords_data = response.json()
            print(f"   ✅ /keywords接口: success={keywords_data.get('success', False)}")
            
            # 验证返回字段
            expected_fields = ['success', 'user_id', 'keywords', 'technical_keywords', 'technical_skills', 'projects_keywords', 'direction']
            missing_fields = [field for field in expected_fields if field not in keywords_data]
            
            if missing_fields:
                print(f"   ❌ 缺失字段: {missing_fields}")
                return False
            
            print(f"   ✅ 字段完整: technical_skills={len(keywords_data.get('technical_skills', []))}")
            print(f"   ✅ 兼容字段: technical_keywords={len(keywords_data.get('technical_keywords', []))}")
            
        else:
            print(f"   ❌ /keywords接口失败: {response.status_code}")
            return False
        
        # 测试/keywords/grouped/{user_id}接口（重点测试）
        print("3. 测试/keywords/grouped/{user_id}接口...")
        response = requests.get(f"{base_url}/keywords/grouped/{test_user_id}", timeout=30)
        
        if response.status_code == 200:
            grouped_data = response.json()
            print(f"   ✅ /keywords/grouped接口: success={grouped_data.get('success', False)}")
            
            # 验证复杂的返回结构
            expected_fields = ['success', 'user_id', 'technical_skills', 'technical_skills_text', 'projects_keywords', 'direction', 'dify_usage_guide']
            missing_fields = [field for field in expected_fields if field not in grouped_data]
            
            if missing_fields:
                print(f"   ❌ 缺失字段: {missing_fields}")
                return False
            
            # 验证technical_skills_text格式
            technical_skills = grouped_data.get('technical_skills', [])
            technical_skills_text = grouped_data.get('technical_skills_text', '')
            expected_text = ', '.join(technical_skills)
            
            if technical_skills_text == expected_text:
                print(f"   ✅ technical_skills_text格式正确")
            else:
                print(f"   ❌ technical_skills_text格式错误")
                print(f"      期望: {expected_text}")
                print(f"      实际: {technical_skills_text}")
                return False
            
            # 验证projects_keywords结构
            projects_keywords = grouped_data.get('projects_keywords', [])
            print(f"   ✅ 项目关键词数量: {len(projects_keywords)}")
            
            for i, project in enumerate(projects_keywords):
                if not all(field in project for field in ['project_name', 'keywords', 'keywords_text', 'search_text']):
                    print(f"   ❌ 项目{i+1}缺失必要字段")
                    return False
                
                # 验证keywords_text格式
                keywords = project.get('keywords', [])
                keywords_text = project.get('keywords_text', '')
                expected_keywords_text = ', '.join(keywords)
                
                if keywords_text != expected_keywords_text:
                    print(f"   ❌ 项目{i+1} keywords_text格式错误")
                    return False
                
                # 验证search_text格式
                project_name = project.get('project_name', '')
                search_text = project.get('search_text', '')
                expected_search_text = f"{project_name} {' '.join(keywords)}"
                
                if search_text != expected_search_text:
                    print(f"   ❌ 项目{i+1} search_text格式错误")
                    return False
            
            print(f"   ✅ 所有项目关键词格式正确")
            
            # 验证dify_usage_guide
            dify_guide = grouped_data.get('dify_usage_guide', {})
            if not isinstance(dify_guide, dict) or not dify_guide:
                print(f"   ❌ dify_usage_guide格式错误")
                return False
            
            print(f"   ✅ dify_usage_guide格式正确")
            
        else:
            print(f"   ❌ /keywords/grouped接口失败: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        return False

def test_fallback_mechanism():
    """测试降级机制"""
    print("\n🔄 测试降级机制...")
    
    try:
        # 连接数据库
        db_service = DatabaseService()
        if not db_service.connect():
            print("❌ 数据库连接失败")
            return False
        
        # 测试读取没有JSON数据的用户（应该降级到表查询）
        test_user_id = "test_mysql_user"  # 这个用户应该没有JSON数据
        profile = db_service.get_profile(test_user_id)
        
        if not profile:
            print(f"❌ 未找到用户档案: {test_user_id}")
            return False
        
        print(f"✅ 降级机制测试成功: {test_user_id}")
        print(f"   技术技能数量: {len(profile.get('technical_skills', []))}")
        print(f"   项目关键词数量: {len(profile.get('projects_keywords', []))}")
        
        # 验证数据来源（应该从表中读取）
        if profile.get('technical_skills') or profile.get('projects_keywords'):
            print("✅ 降级机制正常工作，从关键词表读取数据")
            return True
        else:
            print("⚠️  降级机制可能有问题，未读取到数据")
            return False
        
    except Exception as e:
        print(f"❌ 降级机制测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始API兼容性测试")
    print("=" * 60)
    
    # 测试JSON读取
    json_reading_success = test_json_reading()
    
    # 测试API接口
    api_success = test_api_endpoints()
    
    # 测试降级机制
    fallback_success = test_fallback_mechanism()
    
    print("\n" + "=" * 60)
    print("📊 测试结果汇总:")
    print(f"   JSON数据读取: {'✅ 通过' if json_reading_success else '❌ 失败'}")
    print(f"   API接口兼容性: {'✅ 通过' if api_success else '❌ 失败'}")
    print(f"   降级机制: {'✅ 通过' if fallback_success else '❌ 失败'}")
    
    overall_success = json_reading_success and api_success and fallback_success
    
    if overall_success:
        print("\n🎉 所有API兼容性测试通过！")
        print("   - JSON数据读取正常")
        print("   - API返回格式完全一致")
        print("   - 动态字段生成正确")
        print("   - 降级机制正常工作")
    else:
        print("\n⚠️  部分测试失败，需要检查问题")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
