#!/usr/bin/env python3
"""
测试新添加的/profile接口
"""

import requests
import json

def test_profile_api():
    """测试profile接口"""
    url = "http://localhost:8004/profile"
    
    # 测试用例1: 存在的用户，包含关键词
    test_data_1 = {
        "user_id": "test_user_001",
        "include_keywords": True
    }
    
    print("=" * 60)
    print("测试 /profile 接口")
    print("=" * 60)
    
    try:
        response = requests.post(url, json=test_data_1, timeout=10)
        result = response.json()
        
        if result.get("success"):
            print("✅ 测试用例1 - 存在的用户（包含关键词）: 成功")
            print(f"   用户ID: {result['user_id']}")
            print(f"   档案存在: {result['exists']}")
            print(f"   姓名: {result['profile']['personal_info']['name']}")
            print(f"   技术技能数量: {len(result['profile']['technical_skills'])}")
            print(f"   项目数量: {len(result['profile']['projects_keywords'])}")
        else:
            print(f"❌ 测试用例1失败: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ 测试用例1异常: {e}")
    
    print()
    
    # 测试用例2: 存在的用户，不包含关键词
    test_data_2 = {
        "user_id": "test_user_001", 
        "include_keywords": False
    }
    
    try:
        response = requests.post(url, json=test_data_2, timeout=10)
        result = response.json()
        
        if result.get("success"):
            print("✅ 测试用例2 - 存在的用户（不包含关键词）: 成功")
            print(f"   技术技能数量: {len(result['profile']['technical_skills'])}")
            print(f"   项目数量: {len(result['profile']['projects_keywords'])}")
        else:
            print(f"❌ 测试用例2失败: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ 测试用例2异常: {e}")
    
    print()
    
    # 测试用例3: 不存在的用户
    test_data_3 = {
        "user_id": "nonexistent_user",
        "include_keywords": True
    }
    
    try:
        response = requests.post(url, json=test_data_3, timeout=10)
        result = response.json()
        
        if not result.get("success") and not result.get("exists"):
            print("✅ 测试用例3 - 不存在的用户: 成功")
            print(f"   消息: {result.get('message')}")
        else:
            print(f"❌ 测试用例3失败: 应该返回用户不存在")
            
    except Exception as e:
        print(f"❌ 测试用例3异常: {e}")
    
    print("=" * 60)
    print("✅ /profile 接口测试完成")
    print("=" * 60)

if __name__ == "__main__":
    test_profile_api()
