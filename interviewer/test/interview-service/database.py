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

from config import MYSQL_URL, MYSQL_POOL_SIZE, MYSQL_MAX_OVERFLOW, MYSQL_POOL_TIMEOUT
from models import Base, InterviewSession, InterviewQuestion, InterviewAnswer

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
        except Exception as e:
            logger.error(f"❌ 数据库表创建失败: {e}")
            raise
    
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
                      difficulty_level: str = "medium", estimated_duration: int = 60) -> Optional[str]:
        """创建面试会话"""
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
                    estimated_duration=estimated_duration
                )
                
                session.add(interview_session)
                session.flush()
                
                logger.info(f"✅ 创建面试会话成功: {session_id}")
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
                current_count = session.query(InterviewQuestion).filter_by(session_id=session_id).count()
                question_id = self.generate_question_id(session_id, current_count + 1)
                
                question = InterviewQuestion(
                    session_id=session_id,
                    question_id=question_id,
                    question_text=question_text,
                    question_type=question_type,
                    question_category=question_category,
                    difficulty_level=difficulty_level,
                    expected_duration=expected_duration,
                    reference_answer=reference_answer,
                    scoring_criteria=scoring_criteria,
                    sort_order=current_count + 1
                )
                
                session.add(question)
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
                questions = session.query(InterviewQuestion).filter_by(session_id=session_id)\
                    .order_by(InterviewQuestion.sort_order).all()
                
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
                    for q in questions
                ]
                
        except Exception as e:
            logger.error(f"❌ 获取会话题目失败: {e}")
            return []

    # ==================== 回答操作 ====================

    def submit_answer(self, question_id: str, candidate_answer: str, answer_duration: Optional[int] = None) -> bool:
        """提交面试回答"""
        try:
            with self.get_session() as session:
                # 获取题目信息
                question = session.query(InterviewQuestion).filter_by(question_id=question_id).first()
                if not question:
                    logger.error(f"题目不存在: {question_id}")
                    return False

                # 检查是否已有回答
                existing_answer = session.query(InterviewAnswer).filter_by(question_id=question_id).first()

                if existing_answer:
                    # 更新现有回答
                    existing_answer.candidate_answer = candidate_answer
                    existing_answer.answer_duration = answer_duration
                    existing_answer.status = "answered"
                    existing_answer.answered_at = datetime.now()
                else:
                    # 创建新回答
                    answer = InterviewAnswer(
                        question_id=question_id,
                        session_id=question.session_id,
                        candidate_answer=candidate_answer,
                        answer_duration=answer_duration,
                        status="answered",
                        answered_at=datetime.now()
                    )
                    session.add(answer)

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
                answer = session.query(InterviewAnswer).filter_by(question_id=question_id).first()

                if not answer:
                    logger.error(f"回答不存在: {question_id}")
                    return False

                # 更新反馈信息
                answer.interviewer_feedback = interviewer_feedback
                answer.overall_score = overall_score
                answer.technical_accuracy = technical_accuracy
                answer.communication_clarity = communication_clarity
                answer.problem_solving = problem_solving
                answer.answer_quality = answer_quality
                answer.status = "reviewed"
                answer.reviewed_at = datetime.now()

                # 更新会话的完成题目数和平均分
                self._update_session_stats(session, answer.session_id)

                logger.info(f"✅ 提交面试官反馈成功: {question_id}")
                return True

        except Exception as e:
            logger.error(f"❌ 提交面试官反馈失败: {e}")
            return False

    def add_question_with_answer(self, session_id: str, question_text: str, question_type: str,
                                question_category: Optional[str], candidate_answer: str,
                                interviewer_feedback: str, overall_score: float) -> Optional[str]:
        """一次性添加题目和回答（Dify专用）"""
        try:
            with self.get_session() as session:
                # 添加题目
                current_count = session.query(InterviewQuestion).filter_by(session_id=session_id).count()
                question_id = self.generate_question_id(session_id, current_count + 1)

                question = InterviewQuestion(
                    session_id=session_id,
                    question_id=question_id,
                    question_text=question_text,
                    question_type=question_type,
                    question_category=question_category,
                    sort_order=current_count + 1
                )
                session.add(question)
                session.flush()

                # 添加回答
                answer = InterviewAnswer(
                    question_id=question_id,
                    session_id=session_id,
                    candidate_answer=candidate_answer,
                    interviewer_feedback=interviewer_feedback,
                    overall_score=overall_score,
                    status="reviewed",
                    answered_at=datetime.now(),
                    reviewed_at=datetime.now()
                )
                session.add(answer)
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
            avg_score = session.query(func.avg(InterviewAnswer.overall_score))\
                .filter_by(session_id=session_id)\
                .filter(InterviewAnswer.overall_score.isnot(None))\
                .scalar()

            # 计算完成题目数
            completed_count = session.query(InterviewAnswer)\
                .filter_by(session_id=session_id)\
                .filter(InterviewAnswer.status == "reviewed")\
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
                answer = session.query(InterviewAnswer).filter_by(question_id=question_id).first()

                if not answer:
                    return None

                return {
                    "question_id": answer.question_id,
                    "session_id": answer.session_id,
                    "candidate_answer": answer.candidate_answer,
                    "interviewer_feedback": answer.interviewer_feedback,
                    "answer_quality": answer.answer_quality,
                    "technical_accuracy": float(answer.technical_accuracy) if answer.technical_accuracy else None,
                    "communication_clarity": float(answer.communication_clarity) if answer.communication_clarity else None,
                    "problem_solving": float(answer.problem_solving) if answer.problem_solving else None,
                    "overall_score": float(answer.overall_score) if answer.overall_score else None,
                    "answer_duration": answer.answer_duration,
                    "status": answer.status,
                    "answered_at": answer.answered_at,
                    "reviewed_at": answer.reviewed_at,
                    "created_at": answer.created_at,
                    "updated_at": answer.updated_at
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

                # 获取所有题目和回答
                questions_with_answers = session.query(InterviewQuestion, InterviewAnswer)\
                    .outerjoin(InterviewAnswer, InterviewQuestion.question_id == InterviewAnswer.question_id)\
                    .filter(InterviewQuestion.session_id == session_id)\
                    .order_by(InterviewQuestion.sort_order)\
                    .all()

                questions_summary = []
                scores = []

                for question, answer in questions_with_answers:
                    question_data = {
                        "question_text": question.question_text,
                        "question_type": question.question_type,
                        "question_category": question.question_category
                    }

                    if answer:
                        question_data.update({
                            "score": float(answer.overall_score) if answer.overall_score else None,
                            "feedback": answer.interviewer_feedback,
                            "answer_quality": answer.answer_quality
                        })
                        if answer.overall_score:
                            scores.append(float(answer.overall_score))

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
