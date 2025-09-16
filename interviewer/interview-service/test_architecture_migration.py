#!/usr/bin/env python3
"""
架构迁移测试脚本
用于验证从分离表结构到合并表结构的迁移是否成功
"""

import sys
import os
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

class ArchitectureMigrationTest:
    """架构迁移测试类"""
    
    def __init__(self):
        """初始化测试"""
        try:
            # 验证配置
            validate_config()
            
            # 初始化数据库服务
            self.db = DatabaseService()
            logger.info("✅ 数据库连接初始化成功")
            
        except Exception as e:
            logger.error(f"❌ 初始化失败: {e}")
            raise
    
    def test_table_structure(self) -> bool:
        """测试表结构"""
        try:
            logger.info("🔍 测试表结构...")
            
            with self.db.engine.connect() as conn:
                # 检查新表是否存在
                result = conn.execute("SHOW TABLES LIKE 'interview_qa_records'")
                if not result.fetchone():
                    logger.error("❌ interview_qa_records表不存在")
                    return False
                
                # 检查表结构
                result = conn.execute("DESCRIBE interview_qa_records")
                columns = [row[0] for row in result.fetchall()]
                
                required_columns = [
                    'id', 'session_id', 'question_id', 'question_text',
                    'question_type', 'candidate_answer', 'interviewer_feedback',
                    'overall_score', 'is_wrong_question', 'status',
                    'answered_at', 'reviewed_at', 'created_at', 'updated_at'
                ]
                
                missing_columns = [col for col in required_columns if col not in columns]
                if missing_columns:
                    logger.error(f"❌ 缺少必要字段: {missing_columns}")
                    return False
                
                logger.info("✅ 表结构验证通过")
                return True
                
        except Exception as e:
            logger.error(f"❌ 表结构测试失败: {e}")
            return False
    
    def test_data_migration(self) -> bool:
        """测试数据迁移"""
        try:
            logger.info("🔍 测试数据迁移...")
            
            with self.db.engine.connect() as conn:
                # 检查迁移的数据量
                result = conn.execute("SELECT COUNT(*) FROM interview_qa_records")
                qa_count = result.fetchone()[0]
                
                if qa_count == 0:
                    logger.warning("⚠️  没有迁移的数据，可能是新安装")
                    return True
                
                # 检查错题标记
                result = conn.execute("SELECT COUNT(*) FROM interview_qa_records WHERE is_wrong_question = TRUE")
                wrong_count = result.fetchone()[0]
                
                result = conn.execute("SELECT COUNT(*) FROM interview_qa_records WHERE overall_score < 6.0")
                should_be_wrong = result.fetchone()[0]
                
                if wrong_count != should_be_wrong:
                    logger.error(f"❌ 错题标记不正确: 标记为错题{wrong_count}个，应该标记{should_be_wrong}个")
                    return False
                
                logger.info(f"✅ 数据迁移验证通过: 总记录{qa_count}个，错题{wrong_count}个")
                return True
                
        except Exception as e:
            logger.error(f"❌ 数据迁移测试失败: {e}")
            return False
    
    def test_wrong_question_functionality(self) -> bool:
        """测试错题功能"""
        try:
            logger.info("🔍 测试错题功能...")
            
            # 创建测试会话
            session_id = self.db.create_session(
                user_id="test_user_001",
                session_name="架构测试会话",
                session_type="technical"
            )
            
            if not session_id:
                logger.error("❌ 创建测试会话失败")
                return False
            
            # 添加测试题目和回答（低分，应该被标记为错题）
            question_id = self.db.add_question_with_answer(
                session_id=session_id,
                question_text="测试题目：什么是Python？",
                question_type="technical",
                question_category="基础知识",
                candidate_answer="不知道",
                interviewer_feedback="回答不完整，需要加强基础知识学习",
                overall_score=4.5  # 低于6.0，应该被标记为错题
            )
            
            if not question_id:
                logger.error("❌ 添加测试题目失败")
                return False
            
            # 查询错题
            wrong_questions = self.db.get_user_wrong_questions("test_user_001", limit=10)
            
            # 验证错题查询结果
            found_test_question = False
            for wq in wrong_questions:
                if wq['question_id'] == question_id:
                    found_test_question = True
                    if wq['overall_score'] != 4.5:
                        logger.error(f"❌ 错题分数不正确: 期望4.5，实际{wq['overall_score']}")
                        return False
                    break
            
            if not found_test_question:
                logger.error("❌ 测试错题未被正确查询到")
                return False
            
            # 清理测试数据
            self.db.end_session(session_id)
            
            logger.info("✅ 错题功能测试通过")
            return True
            
        except Exception as e:
            logger.error(f"❌ 错题功能测试失败: {e}")
            return False
    
    def test_api_compatibility(self) -> bool:
        """测试API兼容性"""
        try:
            logger.info("🔍 测试API兼容性...")
            
            # 测试创建会话
            session_id = self.db.create_session(
                user_id="test_user_002",
                session_name="API兼容性测试",
                session_type="technical"
            )
            
            if not session_id:
                logger.error("❌ 创建会话API失败")
                return False
            
            # 测试添加题目
            question_id = self.db.add_question(
                session_id=session_id,
                question_text="API测试题目",
                question_type="technical"
            )
            
            if not question_id:
                logger.error("❌ 添加题目API失败")
                return False
            
            # 测试提交回答
            if not self.db.submit_answer(question_id, "API测试回答"):
                logger.error("❌ 提交回答API失败")
                return False
            
            # 测试提交反馈
            if not self.db.submit_feedback(
                question_id=question_id,
                interviewer_feedback="API测试反馈",
                overall_score=8.5
            ):
                logger.error("❌ 提交反馈API失败")
                return False
            
            # 测试获取会话题目
            questions = self.db.get_session_questions(session_id)
            if not questions or len(questions) != 1:
                logger.error("❌ 获取会话题目API失败")
                return False
            
            # 测试获取回答详情
            answer_detail = self.db.get_answer_detail(question_id)
            if not answer_detail:
                logger.error("❌ 获取回答详情API失败")
                return False
            
            # 清理测试数据
            self.db.end_session(session_id)
            
            logger.info("✅ API兼容性测试通过")
            return True
            
        except Exception as e:
            logger.error(f"❌ API兼容性测试失败: {e}")
            return False
    
    def run_all_tests(self) -> bool:
        """运行所有测试"""
        logger.info("🚀 开始架构迁移测试...")
        
        tests = [
            ("表结构测试", self.test_table_structure),
            ("数据迁移测试", self.test_data_migration),
            ("错题功能测试", self.test_wrong_question_functionality),
            ("API兼容性测试", self.test_api_compatibility)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            logger.info(f"\n{'='*50}")
            logger.info(f"执行测试: {test_name}")
            logger.info(f"{'='*50}")
            
            try:
                if test_func():
                    passed += 1
                    logger.info(f"✅ {test_name} - 通过")
                else:
                    logger.error(f"❌ {test_name} - 失败")
            except Exception as e:
                logger.error(f"❌ {test_name} - 异常: {e}")
        
        logger.info(f"\n{'='*50}")
        logger.info(f"测试结果: {passed}/{total} 通过")
        logger.info(f"{'='*50}")
        
        if passed == total:
            logger.info("🎉 所有测试通过！架构迁移成功！")
            return True
        else:
            logger.error("💥 部分测试失败，请检查架构迁移")
            return False

def main():
    """主函数"""
    try:
        tester = ArchitectureMigrationTest()
        success = tester.run_all_tests()
        sys.exit(0 if success else 1)
        
    except Exception as e:
        logger.error(f"❌ 测试执行失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
