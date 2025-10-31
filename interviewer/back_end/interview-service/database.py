"""
面试记录服务数据库操作管理器
"""

from sqlalchemy import create_engine, text, func
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
import json

from config import MYSQL_URL, MYSQL_POOL_SIZE, MYSQL_MAX_OVERFLOW, MYSQL_POOL_TIMEOUT, DEFAULT_WRONG_QUESTION_THRESHOLD
from models import Base, InterviewSession, InterviewQARecord

logger = logging.getLogger(__name__)

class DatabaseService:
    """数据库服务类"""
    
    def __init__(self):
        """初始化数据库连接"""
        self.engine = None
        self.SessionLocal = None
        self._initialize_connection()
    
    def _initialize_connection(self):
        """初始化数据库连接"""
        try:
            # 创建数据库引擎
            self.engine = create_engine(
                MYSQL_URL,
                pool_pre_ping=True,  # 连接池预检查
                pool_recycle=3600,   # 连接回收时间
                pool_size=MYSQL_POOL_SIZE,
                max_overflow=MYSQL_MAX_OVERFLOW,
                pool_timeout=MYSQL_POOL_TIMEOUT,
                echo=False           # 不打印SQL语句
            )
            
            # 创建会话工厂
            self.SessionLocal = sessionmaker(bind=self.engine)
            
            # 测试连接
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            logger.info("✅ MySQL连接初始化成功")
            
        except Exception as e:
            logger.error(f"❌ MySQL连接初始化失败: {e}")
            logger.warning("⚠️  数据库服务将在离线模式下启动")
            self.engine = None
            self.SessionLocal = None
    
    @contextmanager
    def get_session(self):
        """获取数据库会话的上下文管理器"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"数据库操作失败: {e}")
            raise
        finally:
            session.close()
    
    def test_connection(self) -> bool:
        """测试数据库连接"""
        try:
            with self.get_session() as session:
                session.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"数据库连接测试失败: {e}")
            return False
    
    def create_tables(self):
        """创建所有表（如果不存在）"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("✅ 数据库表创建/验证完成")

            # 执行表结构迁移
            self.migrate_to_qa_records_table()

            # 确保知识点字段存在
            self.ensure_knowledge_points_field()

        except Exception as e:
            logger.error(f"❌ 数据库表创建失败: {e}")
            raise

    def migrate_to_qa_records_table(self):
        """迁移到新的问答记录表结构"""
        try:
            with self.engine.connect() as conn:
                # 检查是否需要迁移
                result = conn.execute(text("SHOW TABLES LIKE 'interview_qa_records'"))
                qa_table_exists = result.fetchone() is not None

                result = conn.execute(text("SHOW TABLES LIKE 'interview_questions'"))
                questions_table_exists = result.fetchone() is not None

                result = conn.execute(text("SHOW TABLES LIKE 'interview_answers'"))
                answers_table_exists = result.fetchone() is not None

                if qa_table_exists:
                    logger.info("✅ interview_qa_records表已存在，跳过迁移")
                    return

                if not questions_table_exists or not answers_table_exists:
                    logger.info("✅ 旧表不存在，无需迁移数据")
                    return

                logger.info("🔄 开始迁移数据到interview_qa_records表...")

                # 迁移数据：将interview_questions和interview_answers合并
                migration_sql = """
                INSERT INTO interview_qa_records (
                    session_id, question_id, question_text, question_type, question_category,
                    difficulty_level, expected_duration, reference_answer, scoring_criteria,
                    sort_order, is_required, candidate_answer, interviewer_feedback,
                    answer_quality, technical_accuracy, communication_clarity, problem_solving,
                    overall_score, answer_duration, status, is_wrong_question,
                    answered_at, reviewed_at, created_at, updated_at
                )
                SELECT
                    q.session_id, q.question_id, q.question_text, q.question_type, q.question_category,
                    q.difficulty_level, q.expected_duration, q.reference_answer, q.scoring_criteria,
                    q.sort_order, q.is_required, a.candidate_answer, a.interviewer_feedback,
                    a.answer_quality, a.technical_accuracy, a.communication_clarity, a.problem_solving,
                    a.overall_score, a.answer_duration, a.status,
                    CASE WHEN a.overall_score < %s THEN TRUE ELSE FALSE END as is_wrong_question,
                    a.answered_at, a.reviewed_at, q.created_at, a.updated_at
                FROM interview_questions q
                LEFT JOIN interview_answers a ON q.question_id = a.question_id
                """

                conn.execute(text(migration_sql), (DEFAULT_WRONG_QUESTION_THRESHOLD,))

                # 获取迁移的记录数
                result = conn.execute(text("SELECT COUNT(*) FROM interview_qa_records"))
                migrated_count = result.fetchone()[0]

                logger.info(f"✅ 数据迁移完成，共迁移 {migrated_count} 条记录")

                # 创建索引
                try:
                    conn.execute(text(
                        "CREATE INDEX idx_qa_session_wrong ON interview_qa_records(session_id, is_wrong_question)"
                    ))
                    conn.execute(text(
                        "CREATE INDEX idx_qa_question_type ON interview_qa_records(question_type, difficulty_level)"
                    ))
                    logger.info("✅ 创建索引成功")
                except Exception as idx_e:
                    logger.warning(f"⚠️  创建索引失败（可能已存在）: {idx_e}")

                conn.commit()
                logger.info("🎉 表结构迁移完成！")

        except Exception as e:
            logger.error(f"❌ 表结构迁移失败: {e}")
            # 不抛出异常，避免影响服务启动
            logger.warning("⚠️  迁移失败，将使用新表结构但可能缺少历史数据")

    def ensure_knowledge_points_field(self):
        """确保interview_qa_records表中存在knowledge_points字段"""
        try:
            with self.engine.connect() as conn:
                # 检查字段是否存在
                result = conn.execute(text("""
                    SELECT COLUMN_NAME
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_SCHEMA = DATABASE()
                    AND TABLE_NAME = 'interview_qa_records'
                    AND COLUMN_NAME = 'knowledge_points'
                """))

                field_exists = result.fetchone() is not None

                if field_exists:
                    logger.info("✅ knowledge_points字段已存在")
                    return

                logger.info("🔄 添加knowledge_points字段...")

                # 添加字段
                conn.execute(text("""
                    ALTER TABLE interview_qa_records
                    ADD COLUMN knowledge_points JSON COMMENT '题目具体知识点关键词，JSON格式存储'
                """))

                # 创建索引（可选，用于优化查询）
                try:
                    conn.execute(text("""
                        CREATE INDEX idx_knowledge_points
                        ON interview_qa_records((CAST(knowledge_points AS CHAR(255))))
                    """))
                    logger.info("✅ knowledge_points索引创建成功")
                except Exception as idx_e:
                    logger.warning(f"⚠️  knowledge_points索引创建失败（可能不支持）: {idx_e}")

                conn.commit()
                logger.info("🎉 knowledge_points字段添加完成！")

        except Exception as e:
            logger.error(f"❌ 添加knowledge_points字段失败: {e}")
            # 不抛出异常，避免影响服务启动
            logger.warning("⚠️  字段添加失败，新功能可能无法正常工作")

    def generate_session_id(self) -> str:
        """生成唯一的会话ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        return f"session_{timestamp}_{unique_id}"
    
    def generate_question_id(self, session_id: str, order: int) -> str:
        """生成题目ID"""
        return f"{session_id}_q{order:03d}"
    
    # ==================== 面试会话操作 ====================
    
    def create_session(self, user_id: str, session_name: str, session_type: str = "technical", 
                      difficulty_level: str = "medium", estimated_duration: int = 60,
                      total_questions: int = 0) -> Optional[str]:
        """创建面试会话
        
        Args:
            user_id: 用户ID
            session_name: 会话名称
            session_type: 面试类型
            difficulty_level: 面试难度
            estimated_duration: 预计时长（分钟）
            total_questions: 总题目数量
        """
        try:
            with self.get_session() as session:
                session_id = self.generate_session_id()
                
                interview_session = InterviewSession(
                    user_id=user_id,
                    session_id=session_id,
                    session_name=session_name,
                    session_type=session_type,
                    status="pending",
                    difficulty_level=difficulty_level,
                    estimated_duration=estimated_duration,
                    total_questions=total_questions
                )
                
                session.add(interview_session)
                session.flush()
                
                logger.info(f"✅ 创建面试会话成功: {session_id}, 预计题目数: {total_questions}")
                return session_id
                
        except Exception as e:
            logger.error(f"❌ 创建面试会话失败: {e}")
            return None
    
    def get_interview_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """获取面试会话详情"""
        try:
            with self.get_session() as session:
                interview_session = session.query(InterviewSession).filter_by(session_id=session_id).first()
                
                if not interview_session:
                    return None
                
                return {
                    "session_id": interview_session.session_id,
                    "user_id": interview_session.user_id,
                    "session_name": interview_session.session_name,
                    "session_type": interview_session.session_type,
                    "status": interview_session.status,
                    "difficulty_level": interview_session.difficulty_level,
                    "estimated_duration": interview_session.estimated_duration,
                    "actual_duration": interview_session.actual_duration,
                    "start_time": interview_session.start_time,
                    "end_time": interview_session.end_time,
                    "total_questions": interview_session.total_questions,
                    "completed_questions": interview_session.completed_questions,
                    "average_score": float(interview_session.average_score) if interview_session.average_score else None,
                    "interviewer_notes": interview_session.interviewer_notes,
                    "created_at": interview_session.created_at,
                    "updated_at": interview_session.updated_at
                }
                
        except Exception as e:
            logger.error(f"❌ 获取面试会话失败: {e}")
            return None
    
    def update_session_status(self, session_id: str, status: str, **kwargs) -> bool:
        """更新面试会话状态"""
        try:
            with self.get_session() as session:
                interview_session = session.query(InterviewSession).filter_by(session_id=session_id).first()
                
                if not interview_session:
                    return False
                
                interview_session.status = status
                
                # 更新其他字段
                for key, value in kwargs.items():
                    if hasattr(interview_session, key):
                        setattr(interview_session, key, value)
                
                logger.info(f"✅ 更新面试会话状态成功: {session_id} -> {status}")
                return True
                
        except Exception as e:
            logger.error(f"❌ 更新面试会话状态失败: {e}")
            return False
    
    def get_user_sessions(self, user_id: str, status: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """获取用户的面试会话列表"""
        try:
            with self.get_session() as session:
                query = session.query(InterviewSession).filter_by(user_id=user_id)
                
                if status:
                    query = query.filter_by(status=status)
                
                sessions = query.order_by(InterviewSession.created_at.desc()).limit(limit).all()
                
                return [
                    {
                        "session_id": s.session_id,
                        "session_name": s.session_name,
                        "session_type": s.session_type,
                        "status": s.status,
                        "difficulty_level": s.difficulty_level,
                        "total_questions": s.total_questions,
                        "completed_questions": s.completed_questions,
                        "average_score": float(s.average_score) if s.average_score else None,
                        "created_at": s.created_at,
                        "updated_at": s.updated_at
                    }
                    for s in sessions
                ]
                
        except Exception as e:
            logger.error(f"❌ 获取用户面试会话列表失败: {e}")
            return []
    
    # ==================== 题目操作 ====================
    
    def add_question(self, session_id: str, question_text: str, question_type: str = "technical",
                    question_category: Optional[str] = None, difficulty_level: str = "medium",
                    expected_duration: int = 10, reference_answer: Optional[str] = None,
                    scoring_criteria: Optional[str] = None) -> Optional[str]:
        """添加面试题目"""
        try:
            with self.get_session() as session:
                # 获取当前题目数量，用于生成题目ID和排序
                current_count = session.query(InterviewQARecord).filter_by(session_id=session_id).count()
                question_id = self.generate_question_id(session_id, current_count + 1)

                # 创建问答记录（仅包含题目信息，回答部分为空）
                qa_record = InterviewQARecord(
                    session_id=session_id,
                    question_id=question_id,
                    question_text=question_text,
                    question_type=question_type,
                    question_category=question_category,
                    difficulty_level=difficulty_level,
                    expected_duration=expected_duration,
                    reference_answer=reference_answer,
                    scoring_criteria=scoring_criteria,
                    sort_order=current_count + 1,
                    status="pending"  # 等待回答
                )

                session.add(qa_record)
                session.flush()
                
                # 更新会话的题目总数
                interview_session = session.query(InterviewSession).filter_by(session_id=session_id).first()
                if interview_session:
                    interview_session.total_questions = current_count + 1
                
                logger.info(f"✅ 添加面试题目成功: {question_id}")
                return question_id
                
        except Exception as e:
            logger.error(f"❌ 添加面试题目失败: {e}")
            return None
    
    def get_session_questions(self, session_id: str) -> List[Dict[str, Any]]:
        """获取会话的所有题目"""
        try:
            with self.get_session() as session:
                qa_records = session.query(InterviewQARecord).filter_by(session_id=session_id)\
                    .order_by(InterviewQARecord.sort_order).all()
                
                return [
                    {
                        "question_id": q.question_id,
                        "question_text": q.question_text,
                        "question_type": q.question_type,
                        "question_category": q.question_category,
                        "difficulty_level": q.difficulty_level,
                        "expected_duration": q.expected_duration,
                        "reference_answer": q.reference_answer,
                        "scoring_criteria": q.scoring_criteria,
                        "sort_order": q.sort_order,
                        "is_required": q.is_required,
                        "created_at": q.created_at
                    }
                    for q in qa_records
                ]
                
        except Exception as e:
            logger.error(f"❌ 获取会话题目失败: {e}")
            return []

    # ==================== 回答操作 ====================

    def submit_answer(self, question_id: str, candidate_answer: str, answer_duration: Optional[int] = None) -> bool:
        """提交面试回答"""
        try:
            with self.get_session() as session:
                # 获取问答记录
                qa_record = session.query(InterviewQARecord).filter_by(question_id=question_id).first()
                if not qa_record:
                    logger.error(f"问答记录不存在: {question_id}")
                    return False

                # 更新回答信息
                qa_record.candidate_answer = candidate_answer
                qa_record.answer_duration = answer_duration
                qa_record.status = "answered"
                qa_record.answered_at = datetime.now()

                session.commit()
                logger.info(f"✅ 提交面试回答成功: {question_id}")
                return True

        except Exception as e:
            logger.error(f"❌ 提交面试回答失败: {e}")
            return False

    def submit_feedback(self, question_id: str, interviewer_feedback: str, overall_score: float,
                       technical_accuracy: Optional[float] = None, communication_clarity: Optional[float] = None,
                       problem_solving: Optional[float] = None, answer_quality: Optional[str] = None) -> bool:
        """提交面试官反馈"""
        try:
            with self.get_session() as session:
                qa_record = session.query(InterviewQARecord).filter_by(question_id=question_id).first()

                if not qa_record:
                    logger.error(f"问答记录不存在: {question_id}")
                    return False

                # 更新反馈信息
                qa_record.interviewer_feedback = interviewer_feedback
                qa_record.overall_score = overall_score
                qa_record.technical_accuracy = technical_accuracy
                qa_record.communication_clarity = communication_clarity
                qa_record.problem_solving = problem_solving
                qa_record.answer_quality = answer_quality
                qa_record.status = "reviewed"
                qa_record.reviewed_at = datetime.now()

                # 判定是否为错题
                qa_record.is_wrong_question = overall_score < DEFAULT_WRONG_QUESTION_THRESHOLD

                # 更新会话的完成题目数和平均分
                self._update_session_stats(session, qa_record.session_id)

                logger.info(f"✅ 提交面试官反馈成功: {question_id}")
                return True

        except Exception as e:
            logger.error(f"❌ 提交面试官反馈失败: {e}")
            return False

    def add_question_with_answer(self, session_id: str, question_text: str, question_type: str,
                                question_category: Optional[str], candidate_answer: str,
                                interviewer_feedback: str, overall_score: float,
                                difficulty_level: str = "medium",
                                knowledge_points: Optional[str] = None) -> Optional[str]:
        """一次性添加题目和回答（Dify专用）"""
        try:
            with self.get_session() as session:
                # 获取当前题目数量
                current_count = session.query(InterviewQARecord).filter_by(session_id=session_id).count()
                question_id = self.generate_question_id(session_id, current_count + 1)

                # 判定是否为错题
                is_wrong = overall_score < DEFAULT_WRONG_QUESTION_THRESHOLD

                # 处理知识点字段 - 统一为字符串格式
                processed_knowledge_points = None
                if knowledge_points:
                    if isinstance(knowledge_points, str):
                        # 如果已经是字符串，直接使用
                        processed_knowledge_points = knowledge_points
                    elif isinstance(knowledge_points, list):
                        # 如果是列表，转换为JSON字符串格式
                        processed_knowledge_points = json.dumps(knowledge_points, ensure_ascii=False)
                    else:
                        # 其他类型，转换为字符串
                        processed_knowledge_points = str(knowledge_points)

                # 创建问答记录（合并题目和回答）
                qa_record = InterviewQARecord(
                    session_id=session_id,
                    question_id=question_id,
                    question_text=question_text,
                    question_type=question_type,
                    question_category=question_category,
                    difficulty_level=difficulty_level,
                    sort_order=current_count + 1,
                    candidate_answer=candidate_answer,
                    interviewer_feedback=interviewer_feedback,
                    overall_score=overall_score,
                    status="reviewed",
                    is_wrong_question=is_wrong,
                    knowledge_points=processed_knowledge_points,
                    answered_at=datetime.now(),
                    reviewed_at=datetime.now()
                )
                session.add(qa_record)
                session.flush()

                # 更新会话统计
                interview_session = session.query(InterviewSession).filter_by(session_id=session_id).first()
                if interview_session:
                    interview_session.total_questions = current_count + 1
                    interview_session.completed_questions = interview_session.completed_questions + 1

                self._update_session_stats(session, session_id)

                logger.info(f"✅ 添加题目和回答成功: {question_id}")
                return question_id

        except Exception as e:
            logger.error(f"❌ 添加题目和回答失败: {e}")
            return None

    def _update_session_stats(self, session: Session, session_id: str):
        """更新会话统计信息"""
        try:
            # 计算平均分
            avg_score = session.query(func.avg(InterviewQARecord.overall_score))\
                .filter_by(session_id=session_id)\
                .filter(InterviewQARecord.overall_score.isnot(None))\
                .scalar()

            # 计算完成题目数
            completed_count = session.query(InterviewQARecord)\
                .filter_by(session_id=session_id)\
                .filter(InterviewQARecord.status == "reviewed")\
                .count()

            # 更新会话
            interview_session = session.query(InterviewSession).filter_by(session_id=session_id).first()
            if interview_session:
                interview_session.completed_questions = completed_count
                if avg_score:
                    interview_session.average_score = round(avg_score, 2)

        except Exception as e:
            logger.error(f"更新会话统计失败: {e}")

    def get_answer_detail(self, question_id: str) -> Optional[Dict[str, Any]]:
        """获取回答详情"""
        try:
            with self.get_session() as session:
                qa_record = session.query(InterviewQARecord).filter_by(question_id=question_id).first()

                if not qa_record:
                    return None

                return {
                    "question_id": qa_record.question_id,
                    "session_id": qa_record.session_id,
                    "candidate_answer": qa_record.candidate_answer,
                    "interviewer_feedback": qa_record.interviewer_feedback,
                    "answer_quality": qa_record.answer_quality,
                    "technical_accuracy": float(qa_record.technical_accuracy) if qa_record.technical_accuracy else None,
                    "communication_clarity": float(qa_record.communication_clarity) if qa_record.communication_clarity else None,
                    "problem_solving": float(qa_record.problem_solving) if qa_record.problem_solving else None,
                    "overall_score": float(qa_record.overall_score) if qa_record.overall_score else None,
                    "answer_duration": qa_record.answer_duration,
                    "status": qa_record.status,
                    "answered_at": qa_record.answered_at,
                    "reviewed_at": qa_record.reviewed_at,
                    "created_at": qa_record.created_at,
                    "updated_at": qa_record.updated_at
                }

        except Exception as e:
            logger.error(f"❌ 获取回答详情失败: {e}")
            return None

    # ==================== 统计查询 ====================

    def get_user_latest_session(self, user_id: str) -> Optional[Dict[str, Any]]:
        """获取用户最新面试会话"""
        try:
            with self.get_session() as session:
                latest_session = session.query(InterviewSession)\
                    .filter_by(user_id=user_id)\
                    .order_by(InterviewSession.created_at.desc())\
                    .first()

                if not latest_session:
                    return None

                return {
                    "session_id": latest_session.session_id,
                    "session_name": latest_session.session_name,
                    "status": latest_session.status,
                    "total_questions": latest_session.total_questions,
                    "completed_questions": latest_session.completed_questions,
                    "average_score": float(latest_session.average_score) if latest_session.average_score else None,
                    "created_at": latest_session.created_at.isoformat() if latest_session.created_at else None
                }

        except Exception as e:
            logger.error(f"❌ 获取用户最新面试会话失败: {e}")
            return None

    def get_session_summary(self, session_id: str) -> Optional[Dict[str, Any]]:
        """获取面试会话总结"""
        try:
            with self.get_session() as session:
                # 获取会话信息
                interview_session = session.query(InterviewSession).filter_by(session_id=session_id).first()
                if not interview_session:
                    return None

                # 获取所有问答记录
                qa_records = session.query(InterviewQARecord)\
                    .filter_by(session_id=session_id)\
                    .order_by(InterviewQARecord.sort_order)\
                    .all()

                questions_summary = []
                scores = []

                for qa_record in qa_records:
                    question_data = {
                        "question_text": qa_record.question_text,
                        "question_type": qa_record.question_type,
                        "question_category": qa_record.question_category,
                        "score": float(qa_record.overall_score) if qa_record.overall_score else None,
                        "feedback": qa_record.interviewer_feedback,
                        "answer_quality": qa_record.answer_quality
                    }

                    if qa_record.overall_score:
                        scores.append(float(qa_record.overall_score))

                    questions_summary.append(question_data)

                # 计算总结信息
                duration_minutes = None
                if interview_session.start_time and interview_session.end_time:
                    duration = interview_session.end_time - interview_session.start_time
                    duration_minutes = int(duration.total_seconds() / 60)

                summary = {
                    "session_name": interview_session.session_name,
                    "total_questions": interview_session.total_questions,
                    "completed_questions": interview_session.completed_questions,
                    "average_score": round(sum(scores) / len(scores), 1) if scores else None,
                    "duration_minutes": duration_minutes,
                    "status": interview_session.status
                }

                return {
                    "summary": summary,
                    "questions_summary": questions_summary
                }

        except Exception as e:
            logger.error(f"❌ 获取面试会话总结失败: {e}")
            return None

    # ==================== 错题查询操作 ====================

    def get_user_wrong_questions(self, user_id: str, question_type: Optional[str] = None,
                                difficulty_level: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """获取用户的错题列表"""
        try:
            with self.get_session() as session:
                # 构建查询：基于新的合并表，无需JOIN
                query = session.query(InterviewQARecord)\
                    .join(InterviewSession, InterviewQARecord.session_id == InterviewSession.session_id)\
                    .filter(InterviewSession.user_id == user_id)\
                    .filter(InterviewQARecord.is_wrong_question == True)

                # 添加筛选条件
                if question_type:
                    query = query.filter(InterviewQARecord.question_type == question_type)

                if difficulty_level:
                    query = query.filter(InterviewQARecord.difficulty_level == difficulty_level)

                # 按时间倒序排列并限制数量
                results = query.order_by(InterviewQARecord.reviewed_at.desc()).limit(limit).all()

                # 格式化返回结果
                wrong_questions = []
                for qa_record in results:
                    # 处理知识点字段 - 现在统一为字符串格式
                    knowledge_points_data = qa_record.knowledge_points if qa_record.knowledge_points else None

                    wrong_questions.append({
                        "question_id": qa_record.question_id,
                        "session_id": qa_record.session_id,
                        "question_text": qa_record.question_text,
                        "question_type": qa_record.question_type,
                        "question_category": qa_record.question_category,
                        "difficulty_level": qa_record.difficulty_level,
                        "candidate_answer": qa_record.candidate_answer,
                        "interviewer_feedback": qa_record.interviewer_feedback,
                        "overall_score": float(qa_record.overall_score) if qa_record.overall_score else None,
                        "knowledge_points": knowledge_points_data,
                        "answered_at": qa_record.answered_at.isoformat() if qa_record.answered_at else None,
                        "reviewed_at": qa_record.reviewed_at.isoformat() if qa_record.reviewed_at else None
                    })

                logger.info(f"✅ 获取用户错题成功: user_id={user_id}, count={len(wrong_questions)}")
                return wrong_questions

        except Exception as e:
            logger.error(f"❌ 获取用户错题失败: {e}")
            return []
