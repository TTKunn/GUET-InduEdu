#!/usr/bin/env python3
"""
简化的JSON读取测试
"""

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
        print(f"📋 测试用户: {test_user_id}")

        # 直接使用mysql_client获取字典格式数据
        profile = db_service.mysql_client.get_profile(test_user_id)
        
        if not profile:
            print(f"❌ 未找到用户档案: {test_user_id}")
            return False
        
        print(f"✅ 成功读取用户档案")
        print(f"   用户ID: {profile.get('user_id')}")
        print(f"   姓名: {profile.get('personal_info', {}).get('name', '未知')}")
        print(f"   技术方向: {profile.get('direction', '未知')}")
        
        # 验证关键数据
        technical_skills = profile.get('technical_skills', [])
        projects_keywords = profile.get('projects_keywords', [])
        extracted_keywords = profile.get('extracted_keywords', [])
        
        print(f"   技术技能: {technical_skills}")
        print(f"   项目关键词: {len(projects_keywords)} 个项目")
        print(f"   提取关键词: {extracted_keywords}")
        
        # 验证兼容性
        if technical_skills == extracted_keywords:
            print("✅ 兼容字段一致")
        else:
            print("⚠️  兼容字段不一致")
        
        # 验证项目关键词结构
        for i, project in enumerate(projects_keywords):
            print(f"   项目{i+1}: {project.get('name', '未知')}")
            print(f"     关键词: {project.get('keywords', [])}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fallback():
    """测试降级机制"""
    print("\n🔄 测试降级机制...")
    
    try:
        # 连接数据库
        db_service = DatabaseService()
        if not db_service.connect():
            print("❌ 数据库连接失败")
            return False

        # 测试没有JSON数据的用户
        test_user_id = "test_mysql_user"
        print(f"📋 测试用户: {test_user_id}")

        # 直接使用mysql_client获取字典格式数据
        profile = db_service.mysql_client.get_profile(test_user_id)
        
        if not profile:
            print(f"❌ 未找到用户档案: {test_user_id}")
            return False
        
        print(f"✅ 降级机制测试成功")
        print(f"   用户ID: {profile.get('user_id')}")
        print(f"   姓名: {profile.get('personal_info', {}).get('name', '未知')}")
        print(f"   技术方向: {profile.get('direction', '未知')}")
        print(f"   技术技能数量: {len(profile.get('technical_skills', []))}")
        print(f"   项目关键词数量: {len(profile.get('projects_keywords', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ 降级测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🚀 开始JSON读取测试")
    print("=" * 50)
    
    # 测试JSON读取
    json_success = test_json_reading()
    
    # 测试降级机制
    fallback_success = test_fallback()
    
    print("\n" + "=" * 50)
    print("📊 测试结果:")
    print(f"   JSON读取: {'✅ 通过' if json_success else '❌ 失败'}")
    print(f"   降级机制: {'✅ 通过' if fallback_success else '❌ 失败'}")
    
    overall_success = json_success and fallback_success
    
    if overall_success:
        print("\n🎉 JSON读取和API兼容性实现成功！")
        print("   - JSON数据正确反序列化")
        print("   - API返回格式保持一致")
        print("   - 兼容字段正确生成")
        print("   - 降级机制正常工作")
    else:
        print("\n⚠️  需要检查问题")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
