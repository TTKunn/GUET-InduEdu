#!/usr/bin/env python3
"""
错题集功能完整测试脚本
测试所有错题相关功能和API接口
"""

import sys
import os
import json
import requests
import time
import logging
from datetime import datetime
from typing import Dict, Any, List

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import DatabaseService
from config import validate_config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ComprehensiveWrongQuestionsTest:
    """错题集功能完整测试类"""
    
    def __init__(self):
        """初始化测试"""
        self.base_url = "http://localhost:8006"
        self.db = DatabaseService()
        self.test_users = []
        self.test_sessions = []
        self.test_questions = []
        
        logger.info("✅ 错题集功能测试初始化完成")
    
    def test_1_create_comprehensive_test_data(self) -> bool:
        """测试1：创建全面的测试数据"""
        logger.info("🔄 测试1：创建全面的测试数据")
        
        try:
            # 创建多个测试用户
            test_users_data = [
                {"user_id": "comprehensive_user_001", "name": "测试用户A", "level": "初级"},
                {"user_id": "comprehensive_user_002", "name": "测试用户B", "level": "中级"},
                {"user_id": "comprehensive_user_003", "name": "测试用户C", "level": "高级"}
            ]
            
            # 为每个用户创建会话和题目
            for user_data in test_users_data:
                user_id = user_data["user_id"]
                name = user_data["name"]
                level = user_data["level"]
                
                # 创建会话
                session_id = self.db.create_session(
                    user_id=user_id,
                    session_name=f"{name}的{level}技术面试",
                    session_type="technical",
                    difficulty_level=level.lower()
                )
                
                if not session_id:
                    logger.error(f"❌ 创建会话失败: {name}")
                    return False
                
                self.test_sessions.append({
                    "session_id": session_id,
                    "user_id": user_id,
                    "name": name,
                    "level": level
                })
                
                # 为每个会话创建不同类型和难度的题目
                questions_data = [
                    # Python基础题目
                    {
                        "text": "请解释Python中的列表推导式，并给出示例。",
                        "type": "technical",
                        "category": "Python基础",
                        "difficulty": "easy",
                        "good_answer": "列表推导式是Python中创建列表的简洁方式，语法为[expression for item in iterable if condition]。例如：[x*2 for x in range(5) if x%2==0]",
                        "poor_answer": "不知道"
                    },
                    # 数据结构题目
                    {
                        "text": "请说明栈和队列的区别，并分别给出应用场景。",
                        "type": "technical", 
                        "category": "数据结构",
                        "difficulty": "medium",
                        "good_answer": "栈是后进先出(LIFO)，队列是先进先出(FIFO)。栈用于函数调用、表达式求值；队列用于任务调度、广度优先搜索。",
                        "poor_answer": "栈就是堆栈，队列就是排队"
                    },
                    # 算法题目
                    {
                        "text": "请解释快速排序的原理和时间复杂度。",
                        "type": "technical",
                        "category": "算法",
                        "difficulty": "hard",
                        "good_answer": "快速排序采用分治策略，选择基准元素，将数组分为小于和大于基准的两部分，递归排序。平均时间复杂度O(nlogn)，最坏O(n²)。",
                        "poor_answer": "快速排序就是很快的排序"
                    },
                    # 数据库题目
                    {
                        "text": "请解释数据库索引的作用和类型。",
                        "type": "technical",
                        "category": "数据库",
                        "difficulty": "medium",
                        "good_answer": "索引用于加速数据查询，类型包括：主键索引、唯一索引、普通索引、复合索引。通过B+树等数据结构实现快速定位。",
                        "poor_answer": "索引就是数据库的目录"
                    },
                    # 系统设计题目
                    {
                        "text": "请设计一个简单的缓存系统，说明其核心组件。",
                        "type": "design",
                        "category": "系统设计",
                        "difficulty": "hard",
                        "good_answer": "缓存系统包括：存储层(内存/Redis)、淘汰策略(LRU/LFU)、一致性机制、监控告警。需考虑缓存穿透、雪崩、击穿问题。",
                        "poor_answer": "就是把数据存起来"
                    }
                ]
                
                # 根据用户级别决定答题质量
                if level == "初级":
                    # 初级用户：60%错题率
                    correct_rate = 0.4
                elif level == "中级":
                    # 中级用户：40%错题率
                    correct_rate = 0.6
                else:
                    # 高级用户：20%错题率
                    correct_rate = 0.8
                
                # 创建题目和回答
                for i, q_data in enumerate(questions_data):
                    # 根据正确率随机决定答题质量
                    import random
                    is_correct = random.random() < correct_rate
                    
                    if is_correct:
                        answer = q_data["good_answer"]
                        score = round(random.uniform(7.0, 9.5), 1)
                        feedback = f"回答很好！{name}对{q_data['category']}有深入理解。"
                    else:
                        answer = q_data["poor_answer"]
                        score = round(random.uniform(2.0, 5.5), 1)
                        feedback = f"回答不够准确，建议{name}加强{q_data['category']}的学习。"
                    
                    # 添加题目和回答
                    question_id = self.db.add_question_with_answer(
                        session_id=session_id,
                        question_text=q_data["text"],
                        question_type=q_data["type"],
                        question_category=q_data["category"],
                        difficulty_level=q_data["difficulty"],
                        candidate_answer=answer,
                        interviewer_feedback=feedback,
                        overall_score=score
                    )
                    
                    if question_id:
                        self.test_questions.append({
                            "question_id": question_id,
                            "session_id": session_id,
                            "user_id": user_id,
                            "category": q_data["category"],
                            "difficulty": q_data["difficulty"],
                            "score": score,
                            "is_wrong": score < 6.0
                        })
                        logger.info(f"✅ 创建题目: {name} - {q_data['category']} - 分数{score}")
                    else:
                        logger.error(f"❌ 创建题目失败: {name} - {q_data['category']}")
                        return False
            
            logger.info(f"✅ 测试数据创建完成: {len(self.test_sessions)}个会话, {len(self.test_questions)}个题目")
            return True
            
        except Exception as e:
            logger.error(f"❌ 创建测试数据失败: {e}")
            return False
    
    def test_2_dify_wrong_questions_api(self) -> bool:
        """测试2：Dify专用错题查询API"""
        logger.info("🔄 测试2：Dify专用错题查询API")
        
        try:
            for session in self.test_sessions:
                user_id = session["user_id"]
                name = session["name"]
                
                # 测试基本错题查询
                response = requests.get(f"{self.base_url}/dify/interview/{user_id}/wrong-questions")
                if response.status_code != 200:
                    logger.error(f"❌ Dify API请求失败: {user_id} - {response.status_code}")
                    return False
                
                data = response.json()
                if not data.get("success"):
                    logger.error(f"❌ Dify API返回失败: {user_id} - {data.get('message')}")
                    return False
                
                wrong_questions = data.get("wrong_questions", [])
                logger.info(f"✅ {name}的错题查询: {len(wrong_questions)}个错题")
                
                # 验证返回数据格式
                if wrong_questions:
                    first_question = wrong_questions[0]
                    required_fields = [
                        "question_id", "session_id", "question_text", "question_type",
                        "question_category", "difficulty_level", "candidate_answer",
                        "interviewer_feedback", "overall_score"
                    ]
                    
                    for field in required_fields:
                        if field not in first_question:
                            logger.error(f"❌ 缺少必要字段: {field}")
                            return False
                    
                    # 验证错题标记正确性
                    if first_question["overall_score"] >= 6.0:
                        logger.error(f"❌ 错题标记错误: 分数{first_question['overall_score']}不应标记为错题")
                        return False
                
                # 测试带参数的查询
                response = requests.get(f"{self.base_url}/dify/interview/{user_id}/wrong-questions", 
                                      params={"question_type": "technical", "limit": 3})
                if response.status_code != 200:
                    logger.error(f"❌ 带参数的Dify API请求失败: {user_id}")
                    return False
                
                data = response.json()
                filtered_questions = data.get("wrong_questions", [])
                logger.info(f"✅ {name}的技术类错题: {len(filtered_questions)}个")
            
            logger.info("✅ Dify专用错题查询API测试通过")
            return True
            
        except Exception as e:
            logger.error(f"❌ Dify API测试失败: {e}")
            return False
    
    def test_3_standard_wrong_questions_api(self) -> bool:
        """测试3：标准错题查询API"""
        logger.info("🔄 测试3：标准错题查询API")
        
        try:
            for session in self.test_sessions:
                user_id = session["user_id"]
                name = session["name"]
                
                # 测试基本错题查询
                response = requests.get(f"{self.base_url}/interview/wrong-questions/{user_id}")
                if response.status_code != 200:
                    logger.error(f"❌ 标准API请求失败: {user_id} - {response.status_code}")
                    return False
                
                data = response.json()
                if not data.get("success"):
                    logger.error(f"❌ 标准API返回失败: {user_id} - {data.get('message')}")
                    return False
                
                wrong_questions = data.get("wrong_questions", [])
                logger.info(f"✅ {name}的错题查询: {len(wrong_questions)}个错题")
                
                # 测试难度筛选
                response = requests.get(f"{self.base_url}/interview/wrong-questions/{user_id}",
                                      params={"difficulty_level": "medium"})
                if response.status_code != 200:
                    logger.error(f"❌ 难度筛选API请求失败: {user_id}")
                    return False
                
                data = response.json()
                medium_questions = data.get("wrong_questions", [])
                logger.info(f"✅ {name}的中等难度错题: {len(medium_questions)}个")
                
                # 验证筛选结果
                for question in medium_questions:
                    if question["difficulty_level"] != "medium":
                        logger.error(f"❌ 难度筛选错误: 期望medium，实际{question['difficulty_level']}")
                        return False
            
            logger.info("✅ 标准错题查询API测试通过")
            return True
            
        except Exception as e:
            logger.error(f"❌ 标准API测试失败: {e}")
            return False
    
    def test_4_wrong_question_statistics(self) -> bool:
        """测试4：错题统计功能"""
        logger.info("🔄 测试4：错题统计功能")
        
        try:
            # 统计各用户错题情况
            total_questions = len(self.test_questions)
            total_wrong = len([q for q in self.test_questions if q["is_wrong"]])
            
            logger.info(f"📊 总体统计: {total_questions}个题目, {total_wrong}个错题, 错题率{total_wrong/total_questions*100:.1f}%")
            
            # 按用户统计
            for session in self.test_sessions:
                user_id = session["user_id"]
                name = session["name"]
                level = session["level"]
                
                user_questions = [q for q in self.test_questions if q["user_id"] == user_id]
                user_wrong = [q for q in user_questions if q["is_wrong"]]
                
                wrong_rate = len(user_wrong) / len(user_questions) * 100 if user_questions else 0
                logger.info(f"📊 {name}({level}): {len(user_questions)}题, {len(user_wrong)}错题, 错题率{wrong_rate:.1f}%")
                
                # 按类别统计错题
                categories = {}
                for question in user_wrong:
                    category = question["category"]
                    if category not in categories:
                        categories[category] = 0
                    categories[category] += 1
                
                if categories:
                    logger.info(f"   错题分布: {categories}")
            
            logger.info("✅ 错题统计功能测试通过")
            return True
            
        except Exception as e:
            logger.error(f"❌ 错题统计测试失败: {e}")
            return False
    
    def test_5_performance_test(self) -> bool:
        """测试5：性能测试"""
        logger.info("🔄 测试5：性能测试")
        
        try:
            # 测试查询响应时间
            for session in self.test_sessions:
                user_id = session["user_id"]
                name = session["name"]
                
                # 测试多次查询的平均响应时间
                response_times = []
                for i in range(5):
                    start_time = time.time()
                    response = requests.get(f"{self.base_url}/dify/interview/{user_id}/wrong-questions")
                    end_time = time.time()
                    
                    if response.status_code == 200:
                        response_times.append(end_time - start_time)
                    else:
                        logger.error(f"❌ 性能测试请求失败: {user_id}")
                        return False
                
                avg_time = sum(response_times) / len(response_times) * 1000  # 转换为毫秒
                logger.info(f"✅ {name}的查询平均响应时间: {avg_time:.2f}ms")
                
                # 验证响应时间是否在合理范围内（<200ms）
                if avg_time > 200:
                    logger.warning(f"⚠️  {name}的响应时间较慢: {avg_time:.2f}ms")
            
            logger.info("✅ 性能测试通过")
            return True
            
        except Exception as e:
            logger.error(f"❌ 性能测试失败: {e}")
            return False
    
    def test_6_edge_cases(self) -> bool:
        """测试6：边界情况测试"""
        logger.info("🔄 测试6：边界情况测试")
        
        try:
            # 测试不存在的用户
            response = requests.get(f"{self.base_url}/dify/interview/nonexistent_user/wrong-questions")
            if response.status_code != 200:
                logger.error(f"❌ 不存在用户的请求应该返回200: {response.status_code}")
                return False
            
            data = response.json()
            if not data.get("success") or len(data.get("wrong_questions", [])) != 0:
                logger.error("❌ 不存在用户应该返回空错题列表")
                return False
            
            logger.info("✅ 不存在用户测试通过")
            
            # 测试无效参数
            user_id = self.test_sessions[0]["user_id"]
            response = requests.get(f"{self.base_url}/interview/wrong-questions/{user_id}",
                                  params={"limit": -1})
            if response.status_code != 422:  # 应该返回参数验证错误
                logger.warning(f"⚠️  无效参数处理: {response.status_code}")
            
            # 测试超大limit参数
            response = requests.get(f"{self.base_url}/interview/wrong-questions/{user_id}",
                                  params={"limit": 1000})
            if response.status_code == 200:
                data = response.json()
                questions = data.get("wrong_questions", [])
                logger.info(f"✅ 超大limit参数测试: 返回{len(questions)}个结果")
            
            logger.info("✅ 边界情况测试通过")
            return True
            
        except Exception as e:
            logger.error(f"❌ 边界情况测试失败: {e}")
            return False
    
    def run_all_tests(self) -> bool:
        """运行所有测试"""
        logger.info("🚀 开始错题集功能完整测试...")
        
        tests = [
            ("创建全面测试数据", self.test_1_create_comprehensive_test_data),
            ("Dify专用错题查询API", self.test_2_dify_wrong_questions_api),
            ("标准错题查询API", self.test_3_standard_wrong_questions_api),
            ("错题统计功能", self.test_4_wrong_question_statistics),
            ("性能测试", self.test_5_performance_test),
            ("边界情况测试", self.test_6_edge_cases)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            logger.info(f"\n{'='*60}")
            logger.info(f"执行测试: {test_name}")
            logger.info(f"{'='*60}")
            
            try:
                if test_func():
                    passed += 1
                    logger.info(f"✅ {test_name} - 通过")
                else:
                    logger.error(f"❌ {test_name} - 失败")
            except Exception as e:
                logger.error(f"❌ {test_name} - 异常: {e}")
        
        logger.info(f"\n{'='*60}")
        logger.info(f"测试结果: {passed}/{total} 通过")
        logger.info(f"{'='*60}")
        
        if passed == total:
            logger.info("🎉 所有测试通过！错题集功能完全正常！")
            return True
        else:
            logger.error("💥 部分测试失败，请检查错题集功能")
            return False

def main():
    """主函数"""
    try:
        tester = ComprehensiveWrongQuestionsTest()
        success = tester.run_all_tests()
        sys.exit(0 if success else 1)
        
    except Exception as e:
        logger.error(f"❌ 测试执行失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
