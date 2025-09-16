#!/usr/bin/env python3
"""
测试迁移用户的登录功能
"""

import requests
import json
import sys

def test_user_login(username, password="123456"):
    """测试用户登录"""
    url = "http://localhost:8007/auth/login"
    data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        result = response.json()
        
        if result.get("success"):
            print(f"✅ 用户 {username} 登录成功")
            print(f"   用户ID: {result['user']['user_id']}")
            print(f"   邮箱: {result['user']['email']}")
            print(f"   Token: {result['access_token'][:50]}...")
            return True
        else:
            print(f"❌ 用户 {username} 登录失败: {result.get('message')}")
            return False
            
    except Exception as e:
        print(f"❌ 测试用户 {username} 时出错: {e}")
        return False

def test_health_check():
    """测试健康检查"""
    try:
        response = requests.get("http://localhost:8007/health", timeout=5)
        result = response.json()
        
        if result.get("status") == "healthy":
            print("✅ 服务健康检查通过")
            return True
        else:
            print("❌ 服务健康检查失败")
            return False
            
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("测试迁移用户登录功能")
    print("=" * 60)
    
    # 测试健康检查
    if not test_health_check():
        print("服务未正常运行，退出测试")
        sys.exit(1)
    
    print()
    
    # 测试几个迁移的用户
    test_users = [
        "test_user_001",
        "test_user_002", 
        "test_xzk_001",
        "deployment_test_user",
        "test_json_storage_user"
    ]
    
    success_count = 0
    total_count = len(test_users)
    
    for username in test_users:
        if test_user_login(username):
            success_count += 1
        print()
    
    print("=" * 60)
    print(f"测试结果: {success_count}/{total_count} 用户登录成功")
    
    if success_count == total_count:
        print("🎉 所有迁移用户登录测试通过！")
    else:
        print("⚠️  部分用户登录测试失败")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
