"""
面试记录服务功能测试脚本
"""

import asyncio
import httpx
import json
from datetime import datetime

# 测试配置
BASE_URL = "http://localhost:8006"
TEST_USER_ID = "test_user_001"

class InterviewServiceTester:
    """面试记录服务测试类"""
    
    def __init__(self):
        self.base_url = BASE_URL
        self.session_id = None
        self.question_id = None
    
    async def test_health_check(self):
        """测试健康检查"""
        print("🔍 测试健康检查...")
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}/health", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ 健康检查通过: {data['status']}")
                    print(f"   数据库连接: {data['database_connected']}")
                    return True
                else:
                    print(f"❌ 健康检查失败: {response.status_code}")
                    return False
            except Exception as e:
                print(f"❌ 健康检查异常: {e}")
                return False
    
    async def test_dify_create_interview(self):
        """测试Dify创建面试记录"""
        print("\n🔍 测试Dify创建面试记录...")
        
        data = {
            "user_id": TEST_USER_ID,
            "session_name": "Python后端开发面试",
            "session_type": "technical",
            "difficulty_level": "medium"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/dify/interview/create",
                    json=data,
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result["success"]:
                        self.session_id = result["session_id"]
                        print(f"✅ 创建面试记录成功: {self.session_id}")
                        print(f"   会话名称: {result['session_name']}")
                        print(f"   创建时间: {result['created_at']}")
                        return True
                    else:
                        print(f"❌ 创建面试记录失败: {result['message']}")
                        return False
                else:
                    print(f"❌ 创建面试记录失败: HTTP {response.status_code}")
                    return False
                    
            except Exception as e:
                print(f"❌ 创建面试记录异常: {e}")
                return False
    
    async def test_dify_add_qa(self):
        """测试Dify添加题目和回答"""
        print("\n🔍 测试Dify添加题目和回答...")
        
        if not self.session_id:
            print("❌ 需要先创建面试会话")
            return False
        
        data = {
            "session_id": self.session_id,
            "question_text": "请介绍一下Python的GIL机制及其影响",
            "question_type": "technical",
            "question_category": "Python核心",
            "candidate_answer": "GIL（Global Interpreter Lock）是Python解释器中的一个全局锁，它确保同一时间只有一个线程执行Python字节码。这意味着即使在多线程程序中，Python代码也不能真正并行执行。GIL的存在主要是为了保护Python对象的引用计数不被多线程破坏。",
            "interviewer_feedback": "回答准确，理解深入。能够清楚解释GIL的作用和影响，但可以进一步讨论如何绕过GIL的限制。",
            "overall_score": 8.5
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/dify/interview/add-qa",
                    json=data,
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result["success"]:
                        self.question_id = result["question_id"]
                        print(f"✅ 添加题目和回答成功: {self.question_id}")
                        print(f"   会话ID: {result['session_id']}")
                        print(f"   状态: {result['status']}")
                        return True
                    else:
                        print(f"❌ 添加题目和回答失败: {result['message']}")
                        return False
                else:
                    print(f"❌ 添加题目和回答失败: HTTP {response.status_code}")
                    return False
                    
            except Exception as e:
                print(f"❌ 添加题目和回答异常: {e}")
                return False
    
    async def test_dify_get_latest_interview(self):
        """测试Dify获取最新面试信息"""
        print("\n🔍 测试Dify获取最新面试信息...")
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/dify/interview/{TEST_USER_ID}/latest",
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result["success"]:
                        latest = result["latest_session"]
                        if latest:
                            print(f"✅ 获取最新面试信息成功:")
                            print(f"   会话ID: {latest['session_id']}")
                            print(f"   会话名称: {latest['session_name']}")
                            print(f"   状态: {latest['status']}")
                            print(f"   题目数: {latest['total_questions']}")
                            print(f"   完成数: {latest['completed_questions']}")
                            print(f"   平均分: {latest['average_score']}")
                            return True
                        else:
                            print("✅ 获取成功，但暂无面试记录")
                            return True
                    else:
                        print(f"❌ 获取最新面试信息失败: {result['message']}")
                        return False
                else:
                    print(f"❌ 获取最新面试信息失败: HTTP {response.status_code}")
                    return False
                    
            except Exception as e:
                print(f"❌ 获取最新面试信息异常: {e}")
                return False
    
    async def test_dify_get_interview_summary(self):
        """测试Dify获取面试总结"""
        print("\n🔍 测试Dify获取面试总结...")
        
        if not self.session_id:
            print("❌ 需要先创建面试会话")
            return False
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/dify/interview/{self.session_id}/summary",
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result["success"]:
                        summary = result["summary"]
                        questions = result["questions_summary"]
                        
                        print(f"✅ 获取面试总结成功:")
                        print(f"   会话名称: {summary['session_name']}")
                        print(f"   总题目数: {summary['total_questions']}")
                        print(f"   完成题目数: {summary['completed_questions']}")
                        print(f"   平均分: {summary['average_score']}")
                        print(f"   总体评价: {summary['overall_evaluation']}")
                        print(f"   优势: {summary.get('strengths', [])}")
                        print(f"   改进点: {summary.get('improvements', [])}")
                        print(f"   题目详情数: {len(questions)}")
                        return True
                    else:
                        print(f"❌ 获取面试总结失败: {result['message']}")
                        return False
                else:
                    print(f"❌ 获取面试总结失败: HTTP {response.status_code}")
                    return False
                    
            except Exception as e:
                print(f"❌ 获取面试总结异常: {e}")
                return False
    
    async def test_standard_apis(self):
        """测试标准API接口"""
        print("\n🔍 测试标准API接口...")
        
        # 测试获取用户面试会话列表
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/interview/sessions/{TEST_USER_ID}",
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result["success"]:
                        sessions = result["sessions"]
                        print(f"✅ 获取用户面试会话列表成功: {len(sessions)}个会话")
                        return True
                    else:
                        print(f"❌ 获取用户面试会话列表失败: {result['message']}")
                        return False
                else:
                    print(f"❌ 获取用户面试会话列表失败: HTTP {response.status_code}")
                    return False
                    
            except Exception as e:
                print(f"❌ 获取用户面试会话列表异常: {e}")
                return False
    
    async def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始面试记录服务功能测试")
        print("=" * 50)
        
        tests = [
            ("健康检查", self.test_health_check),
            ("Dify创建面试记录", self.test_dify_create_interview),
            ("Dify添加题目和回答", self.test_dify_add_qa),
            ("Dify获取最新面试信息", self.test_dify_get_latest_interview),
            ("Dify获取面试总结", self.test_dify_get_interview_summary),
            ("标准API接口", self.test_standard_apis)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                result = await test_func()
                if result:
                    passed += 1
                else:
                    print(f"❌ {test_name} 测试失败")
            except Exception as e:
                print(f"❌ {test_name} 测试异常: {e}")
        
        print("\n" + "=" * 50)
        print(f"🎯 测试完成: {passed}/{total} 通过")
        
        if passed == total:
            print("🎉 所有测试通过！")
            return True
        else:
            print("⚠️  部分测试失败，请检查服务状态")
            return False

async def main():
    """主函数"""
    tester = InterviewServiceTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
