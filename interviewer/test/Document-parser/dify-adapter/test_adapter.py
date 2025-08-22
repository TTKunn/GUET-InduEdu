"""
Dify适配器测试脚本
验证适配器服务的各项功能
"""

import asyncio
import json
import requests
import time
from typing import Dict, Any

# 测试配置
ADAPTER_URL = "http://localhost:8001"
PDF_PARSER_URL = "http://localhost:8000"
TEST_API_KEY = "dify-pdf-docs-001"

def test_health_check():
    """测试健康检查端点"""
    print("🔍 测试健康检查...")
    try:
        response = requests.get(f"{ADAPTER_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 健康检查通过: {data['status']}")
            print(f"   依赖状态: {data['dependencies']}")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return False

def test_pdf_parser_connection():
    """测试PDF解析API连接"""
    print("🔍 测试PDF解析API连接...")
    try:
        response = requests.get(f"{PDF_PARSER_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ PDF解析API连接正常")
            return True
        else:
            print(f"❌ PDF解析API连接失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ PDF解析API连接异常: {e}")
        print("💡 请确保PDF解析服务正在运行: python start_api.py")
        return False

def test_authentication():
    """测试认证功能"""
    print("🔍 测试认证功能...")
    
    # 测试无效的Authorization头
    print("  测试无效Authorization头...")
    response = requests.post(
        f"{ADAPTER_URL}/retrieval",
        json={
            "knowledge_id": "pdf_documents",
            "query": "test query",
            "retrieval_setting": {"top_k": 5, "score_threshold": 0.5}
        }
    )
    if response.status_code == 403:
        print("  ✅ 无效Authorization头被正确拒绝")
    else:
        print(f"  ❌ 无效Authorization头测试失败: {response.status_code}")
    
    # 测试无效的API Key
    print("  测试无效API Key...")
    response = requests.post(
        f"{ADAPTER_URL}/retrieval",
        headers={"Authorization": "Bearer invalid-key"},
        json={
            "knowledge_id": "pdf_documents", 
            "query": "test query",
            "retrieval_setting": {"top_k": 5, "score_threshold": 0.5}
        }
    )
    if response.status_code == 403:
        print("  ✅ 无效API Key被正确拒绝")
    else:
        print(f"  ❌ 无效API Key测试失败: {response.status_code}")
    
    # 测试有效的API Key（但可能没有数据）
    print("  测试有效API Key...")
    response = requests.post(
        f"{ADAPTER_URL}/retrieval",
        headers={"Authorization": f"Bearer {TEST_API_KEY}"},
        json={
            "knowledge_id": "pdf_documents",
            "query": "test query", 
            "retrieval_setting": {"top_k": 5, "score_threshold": 0.5}
        }
    )
    if response.status_code in [200, 404]:  # 200成功或404没有数据都是正常的
        print("  ✅ 有效API Key认证通过")
        return True
    else:
        print(f"  ❌ 有效API Key测试失败: {response.status_code} - {response.text}")
        return False

def test_retrieval_api():
    """测试检索API功能"""
    print("🔍 测试检索API功能...")
    
    test_request = {
        "knowledge_id": "pdf_documents",
        "query": "人工智能",
        "retrieval_setting": {
            "top_k": 3,
            "score_threshold": 0.3
        },
        "metadata_condition": None
    }
    
    try:
        response = requests.post(
            f"{ADAPTER_URL}/retrieval",
            headers={"Authorization": f"Bearer {TEST_API_KEY}"},
            json=test_request,
            timeout=30
        )
        
        print(f"  响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            records = data.get("records", [])
            print(f"  ✅ 检索成功，返回 {len(records)} 条记录")
            
            # 显示第一条记录的详情
            if records:
                first_record = records[0]
                print(f"  📄 第一条记录:")
                print(f"     标题: {first_record.get('title', 'N/A')}")
                print(f"     相似度: {first_record.get('score', 0):.3f}")
                print(f"     内容预览: {first_record.get('content', '')[:100]}...")
            
            return True
        elif response.status_code == 404:
            print("  ⚠️  Collection不存在或无数据")
            print("  💡 请先上传PDF文档到向量数据库")
            return True  # 这是正常情况
        else:
            print(f"  ❌ 检索失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"  ❌ 检索API测试异常: {e}")
        return False

def test_stats_api():
    """测试统计API"""
    print("🔍 测试统计API...")
    try:
        response = requests.get(f"{ADAPTER_URL}/stats", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ 统计API正常")
            print(f"   总请求数: {data.get('total_requests', 0)}")
            print(f"   成功请求数: {data.get('successful_requests', 0)}")
            return True
        else:
            print(f"❌ 统计API失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 统计API异常: {e}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("🧪 开始Dify适配器服务测试")
    print("=" * 50)
    
    tests = [
        ("健康检查", test_health_check),
        ("PDF解析API连接", test_pdf_parser_connection),
        ("认证功能", test_authentication),
        ("检索API", test_retrieval_api),
        ("统计API", test_stats_api)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        result = test_func()
        results.append((test_name, result))
        time.sleep(1)  # 避免请求过快
    
    # 汇总结果
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 总体结果: {passed}/{len(tests)} 项测试通过")
    
    if passed == len(tests):
        print("🎉 所有测试通过！适配器服务运行正常")
        print("\n📝 下一步:")
        print("   1. 在Dify中配置外部知识库")
        print("   2. API端点: http://localhost:8001/retrieval")
        print("   3. API Key: dify-pdf-docs-001")
        print("   4. 知识库ID: pdf_documents")
    else:
        print("⚠️  部分测试失败，请检查服务配置")

if __name__ == "__main__":
    run_all_tests()
