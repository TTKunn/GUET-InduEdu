#!/usr/bin/env python3
"""
测试MySQL版本的analysis-service
"""

import requests
import json
import os
import sys

def test_health():
    """测试健康检查"""
    print("🔍 测试健康检查...")
    try:
        response = requests.get("http://localhost:8004/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 健康检查通过: {data['status']}")
            print(f"   数据库连接: {data['database_connected']}")
            print(f"   LLM可用: {data['llm_available']}")
            print(f"   依赖服务: {data['dependencies']}")
            if 'stats' in data and data['stats']:
                print(f"   统计信息: {data['stats']}")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return False

def test_analyze_resume():
    """测试简历分析"""
    print("\n📄 测试简历分析...")
    
    # 检查PDF文件是否存在
    pdf_path = "../../../xzk.pdf"
    if not os.path.exists(pdf_path):
        print(f"❌ PDF文件不存在: {pdf_path}")
        return False
    
    try:
        # 准备请求数据
        files = {
            'file': ('xzk.pdf', open(pdf_path, 'rb'), 'application/pdf')
        }
        data = {
            'user_id': 'test_mysql_user',
            'extraction_mode': 'comprehensive',
            'overwrite': 'true'
        }
        
        print("   发送分析请求...")
        response = requests.post("http://localhost:8004/analyze", files=files, data=data, timeout=120)
        
        files['file'][1].close()  # 关闭文件
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print(f"✅ 简历分析成功!")
                print(f"   用户ID: {result['user_id']}")
                print(f"   处理时间: {result.get('processing_time', 0):.2f}秒")
                print(f"   技术技能: {result.get('technical_skills', [])}")
                print(f"   技术方向: {result.get('direction', '未知')}")
                print(f"   项目关键词数量: {len(result.get('projects_keywords', []))}")
                return True
            else:
                print(f"❌ 简历分析失败: {result['message']}")
                return False
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"   响应内容: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 简历分析异常: {e}")
        return False

def test_get_keywords():
    """测试获取关键词"""
    print("\n🔑 测试获取关键词...")
    
    try:
        # 测试获取关键词
        response = requests.post("http://localhost:8004/keywords", 
                               json={"user_id": "test_mysql_user", "category": "all", "format_type": "list"})
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print(f"✅ 关键词获取成功!")
                print(f"   技术技能: {result.get('technical_skills', [])}")
                print(f"   技术方向: {result.get('direction', '未知')}")
                print(f"   项目数量: {len(result.get('projects_keywords', []))}")
                return True
            else:
                print(f"❌ 关键词获取失败: {result['message']}")
                return False
        else:
            print(f"❌ 请求失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 关键词获取异常: {e}")
        return False

def test_dify_keywords():
    """测试Dify专用关键词接口"""
    print("\n🎯 测试Dify关键词接口...")
    
    try:
        response = requests.get("http://localhost:8004/keywords/grouped/test_mysql_user")
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print(f"✅ Dify关键词获取成功!")
                print(f"   技术技能: {result.get('technical_skills', [])}")
                print(f"   技术方向: {result.get('direction', '未知')}")
                print(f"   项目数量: {len(result.get('projects_keywords', []))}")
                return True
            else:
                print(f"❌ Dify关键词获取失败: {result['message']}")
                return False
        else:
            print(f"❌ 请求失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Dify关键词获取异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试MySQL版本的analysis-service")
    print("=" * 50)
    
    # 测试步骤
    tests = [
        ("健康检查", test_health),
        ("简历分析", test_analyze_resume),
        ("获取关键词", test_get_keywords),
        ("Dify关键词接口", test_dify_keywords)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
            results.append((test_name, False))
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    success_count = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {test_name}: {status}")
        if result:
            success_count += 1
    
    print(f"\n🎯 总体结果: {success_count}/{len(results)} 项测试通过")
    
    if success_count == len(results):
        print("🎉 所有测试通过！MySQL版本运行正常！")
        return True
    else:
        print("⚠️  部分测试失败，请检查相关问题")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
