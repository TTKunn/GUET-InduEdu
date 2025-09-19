#!/usr/bin/env python3
"""
创建测试数据脚本
用于验证错题集功能和架构重构
"""

import sys
import os
import logging
from datetime import datetime, timedelta
import random

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

class TestDataCreator:
    """测试数据创建器"""
    
    def __init__(self):
        """初始化"""
        try:
            validate_config()
            self.db = DatabaseService()
            logger.info("✅ 数据库连接初始化成功")
        except Exception as e:
            logger.error(f"❌ 初始化失败: {e}")
            raise
    
    def create_test_sessions(self):
        """创建测试会话"""
        logger.info("🔄 创建测试会话...")
        
        test_users = [
            {"user_id": "test_user_001", "name": "张三"},
            {"user_id": "test_user_002", "name": "李四"},
            {"user_id": "test_user_003", "name": "王五"}
        ]
        
        sessions = []
        for user in test_users:
            session_id = self.db.create_session(
                user_id=user["user_id"],
                session_name=f"{user['name']}的技术面试",
                session_type="technical",
                difficulty_level="medium"
            )
            if session_id:
                sessions.append({
                    "session_id": session_id,
                    "user_id": user["user_id"],
                    "name": user["name"]
                })
                logger.info(f"✅ 创建会话成功: {user['name']} - {session_id}")
            else:
                logger.error(f"❌ 创建会话失败: {user['name']}")
        
        return sessions
    
    def create_test_questions_and_answers(self, sessions):
        """创建测试题目和回答"""
        logger.info("🔄 创建测试题目和回答...")
        
        # 测试题目模板
        questions_templates = [
            {
                "text": "请解释Python中的装饰器是什么，并给出一个使用示例。",
                "type": "technical",
                "category": "Python基础",
                "difficulty": "medium",
                "good_answers": [
                    "装饰器是Python中的一种设计模式，用于在不修改原函数代码的情况下扩展函数功能。它本质上是一个接受函数作为参数并返回新函数的高阶函数。",
                    "装饰器可以用@语法糖来使用，例如@property、@staticmethod等。自定义装饰器可以用来实现日志记录、性能监控、权限验证等功能。"
                ],
                "poor_answers": [
                    "不知道",
                    "装饰器就是用来装饰的",
                    "Python的一个功能"
                ]
            },
            {
                "text": "什么是RESTful API？请说明其主要特点。",
                "type": "technical", 
                "category": "Web开发",
                "difficulty": "medium",
                "good_answers": [
                    "RESTful API是基于REST架构风格的Web API设计规范。主要特点包括：无状态、统一接口、资源导向、分层系统等。",
                    "使用HTTP方法（GET、POST、PUT、DELETE）对应CRUD操作，URL表示资源，状态码表示操作结果。"
                ],
                "poor_answers": [
                    "就是API",
                    "不太清楚",
                    "用来传输数据的"
                ]
            },
            {
                "text": "请解释数据库事务的ACID特性。",
                "type": "technical",
                "category": "数据库",
                "difficulty": "hard",
                "good_answers": [
                    "ACID是数据库事务的四个基本特性：原子性(Atomicity)、一致性(Consistency)、隔离性(Isolation)、持久性(Durability)。",
                    "原子性确保事务要么全部执行要么全部回滚；一致性保证数据库从一个一致状态转换到另一个一致状态；隔离性确保并发事务不会相互干扰；持久性保证已提交事务的修改永久保存。"
                ],
                "poor_answers": [
                    "不知道ACID是什么",
                    "数据库的一些特性",
                    "听说过但不记得了"
                ]
            },
            {
                "text": "请说明JavaScript中的闭包概念。",
                "type": "technical",
                "category": "JavaScript",
                "difficulty": "medium",
                "good_answers": [
                    "闭包是指函数能够访问其外部作用域中变量的特性，即使外部函数已经执行完毕。闭包由函数和其词法环境组成。",
                    "闭包常用于数据封装、模块化编程、回调函数等场景。需要注意内存泄漏问题。"
                ],
                "poor_answers": [
                    "不了解闭包",
                    "JavaScript的一个概念",
                    "函数相关的东西"
                ]
            },
            {
                "text": "请解释什么是微服务架构，以及它的优缺点。",
                "type": "technical",
                "category": "系统架构",
                "difficulty": "hard",
                "good_answers": [
                    "微服务架构是将单一应用程序分解为多个小型、独立服务的架构模式。每个服务运行在自己的进程中，通过轻量级通信机制交互。",
                    "优点：独立部署、技术栈灵活、故障隔离、团队自治。缺点：系统复杂度增加、网络延迟、数据一致性挑战、运维复杂。"
                ],
                "poor_answers": [
                    "不知道微服务",
                    "就是很小的服务",
                    "听说过但不了解"
                ]
            }
        ]
        
        created_questions = []
        
        for session in sessions:
            session_id = session["session_id"]
            user_name = session["name"]
            
            # 为每个会话创建3-5个题目
            num_questions = random.randint(3, 5)
            selected_questions = random.sample(questions_templates, num_questions)
            
            for i, q_template in enumerate(selected_questions):
                # 随机选择好答案或差答案
                is_good_answer = random.choice([True, False])
                if is_good_answer:
                    answer = random.choice(q_template["good_answers"])
                    score = round(random.uniform(7.0, 9.5), 1)  # 好答案高分
                else:
                    answer = random.choice(q_template["poor_answers"])
                    score = round(random.uniform(2.0, 5.5), 1)  # 差答案低分
                
                # 生成反馈
                if score >= 7.0:
                    feedback = f"回答很好！{user_name}对{q_template['category']}有深入理解。"
                elif score >= 6.0:
                    feedback = f"回答基本正确，但{user_name}可以更详细地解释一些概念。"
                else:
                    feedback = f"回答不够准确，建议{user_name}加强{q_template['category']}的学习。"
                
                # 添加题目和回答
                question_id = self.db.add_question_with_answer(
                    session_id=session_id,
                    question_text=q_template["text"],
                    question_type=q_template["type"],
                    question_category=q_template["category"],
                    candidate_answer=answer,
                    interviewer_feedback=feedback,
                    overall_score=score
                )
                
                if question_id:
                    created_questions.append({
                        "question_id": question_id,
                        "session_id": session_id,
                        "user_name": user_name,
                        "score": score,
                        "is_wrong": score < 6.0
                    })
                    logger.info(f"✅ 创建题目成功: {user_name} - 分数{score} - {'错题' if score < 6.0 else '正确'}")
                else:
                    logger.error(f"❌ 创建题目失败: {user_name}")
        
        return created_questions
    
    def verify_wrong_questions(self, sessions):
        """验证错题功能"""
        logger.info("🔍 验证错题功能...")
        
        for session in sessions:
            user_id = session["user_id"]
            user_name = session["name"]
            
            # 查询用户错题
            wrong_questions = self.db.get_user_wrong_questions(user_id, limit=10)
            
            logger.info(f"📊 {user_name}的错题统计:")
            logger.info(f"   错题数量: {len(wrong_questions)}")
            
            for wq in wrong_questions:
                logger.info(f"   - {wq['question_type']}: {wq['overall_score']}分")
    
    def create_all_test_data(self):
        """创建所有测试数据"""
        logger.info("🚀 开始创建测试数据...")
        
        try:
            # 创建测试会话
            sessions = self.create_test_sessions()
            if not sessions:
                logger.error("❌ 没有成功创建任何会话")
                return False
            
            # 创建测试题目和回答
            questions = self.create_test_questions_and_answers(sessions)
            if not questions:
                logger.error("❌ 没有成功创建任何题目")
                return False
            
            # 验证错题功能
            self.verify_wrong_questions(sessions)
            
            # 统计结果
            total_questions = len(questions)
            wrong_questions = [q for q in questions if q["is_wrong"]]
            correct_questions = [q for q in questions if not q["is_wrong"]]
            
            logger.info(f"\n{'='*50}")
            logger.info(f"📊 测试数据创建完成")
            logger.info(f"{'='*50}")
            logger.info(f"总会话数: {len(sessions)}")
            logger.info(f"总题目数: {total_questions}")
            logger.info(f"错题数量: {len(wrong_questions)}")
            logger.info(f"正确题目: {len(correct_questions)}")
            logger.info(f"错题率: {len(wrong_questions)/total_questions*100:.1f}%")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ 创建测试数据失败: {e}")
            return False

def main():
    """主函数"""
    try:
        creator = TestDataCreator()
        success = creator.create_all_test_data()
        
        if success:
            logger.info("🎉 测试数据创建成功！")
        else:
            logger.error("💥 测试数据创建失败！")
            
        sys.exit(0 if success else 1)
        
    except Exception as e:
        logger.error(f"❌ 执行失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
