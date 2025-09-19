"""
面试记录服务数据模型定义
"""

from sqlalchemy import Column, Integer, BigInteger, String, Text, TIMESTAMP, DECIMAL, ForeignKey, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

# SQLAlchemy Base
Base = declarative_base()

# ==================== 枚举类型定义 ====================
class SessionStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class SessionType(str, Enum):
    KNOWLEDGE_BASED = "knowledge_based"  # 自选知识点面试
    COMPANY_POSITION = "company_position"  # 自选公司岗位面试
    RESUME_CUSTOMIZED = "resume_customized"  # 个人简历定制面试
    WRONG_QUESTIONS = "wrong_questions"  # 错题面试

class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class QuestionType(str, Enum):
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    LOGICAL = "logical"
    PROJECT_BASED = "project_based"

class AnswerStatus(str, Enum):
    PENDING = "pending"
    ANSWERED = "answered"
    REVIEWED = "reviewed"
    SKIPPED = "skipped"

class AnswerQuality(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    POOR = "poor"

# ==================== SQLAlchemy ORM 模型 ====================

class InterviewSession(Base):
    """面试会话表"""
    __tablename__ = 'interview_sessions'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='自增主键')
    user_id = Column(String(100), nullable=False, comment='用户ID，关联candidate_profiles.user_id')
    session_id = Column(String(100), unique=True, nullable=False, comment='面试会话唯一标识')
    session_name = Column(String(200), comment='面试名称')
    session_type = Column(String(50), default='knowledge_based', comment='面试类型')
    status = Column(String(20), default='pending', comment='面试状态')
    difficulty_level = Column(String(20), default='medium', comment='面试难度')
    estimated_duration = Column(Integer, default=60, comment='预计时长（分钟）')
    actual_duration = Column(Integer, comment='实际时长（分钟）')
    start_time = Column(TIMESTAMP, comment='开始时间')
    end_time = Column(TIMESTAMP, comment='结束时间')
    total_questions = Column(Integer, default=0, comment='总题目数')
    completed_questions = Column(Integer, default=0, comment='已完成题目数')
    average_score = Column(DECIMAL(3,2), comment='平均得分')
    interviewer_notes = Column(Text, comment='面试官总体评价')
    created_at = Column(TIMESTAMP, server_default=func.now(), comment='创建时间')
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment='更新时间')
    
    # 关联关系
    qa_records = relationship("InterviewQARecord", back_populates="session", cascade="all, delete-orphan")

class InterviewQARecord(Base):
    """面试问答记录表（合并题目和回答）"""
    __tablename__ = 'interview_qa_records'

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='自增主键')
    session_id = Column(String(100), ForeignKey('interview_sessions.session_id', ondelete='CASCADE'),
                        nullable=False, comment='面试会话ID')
    question_id = Column(String(100), nullable=False, comment='题目唯一标识')

    # 题目相关字段
    question_text = Column(Text, nullable=False, comment='题目原文')
    question_type = Column(String(50), default='technical', comment='题目类型')
    question_category = Column(String(100), comment='题目分类')
    difficulty_level = Column(String(20), default='medium', comment='题目难度')
    expected_duration = Column(Integer, default=10, comment='预期时长（分钟）')
    reference_answer = Column(Text, comment='参考答案')
    scoring_criteria = Column(Text, comment='评分标准')
    sort_order = Column(Integer, default=0, comment='题目顺序')
    is_required = Column(Boolean, default=True, comment='是否必答')

    # 回答相关字段
    candidate_answer = Column(Text, comment='面试者回答')
    interviewer_feedback = Column(Text, comment='面试官反馈')
    answer_quality = Column(String(20), comment='回答质量')
    technical_accuracy = Column(DECIMAL(3,2), comment='技术准确性评分')
    communication_clarity = Column(DECIMAL(3,2), comment='表达清晰度评分')
    problem_solving = Column(DECIMAL(3,2), comment='问题解决能力评分')
    overall_score = Column(DECIMAL(3,2), comment='综合评分')
    answer_duration = Column(Integer, comment='回答时长（分钟）')
    status = Column(String(20), default='pending', comment='回答状态')

    # 错题标记字段
    is_wrong_question = Column(Boolean, default=False, comment='是否为错题')

    # 知识点字段
    knowledge_points = Column(Text, comment='题目具体知识点关键词，字符串格式存储')

    # 时间字段
    answered_at = Column(TIMESTAMP, comment='回答时间')
    reviewed_at = Column(TIMESTAMP, comment='评价时间')
    created_at = Column(TIMESTAMP, server_default=func.now(), comment='创建时间')
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    # 关联关系
    session = relationship("InterviewSession", back_populates="qa_records")

# ==================== Pydantic 请求/响应模型 ====================

# Dify专用请求模型
class DifyCreateInterviewRequest(BaseModel):
    """Dify创建面试记录请求"""
    user_id: str = Field(..., description="用户ID")
    session_name: Optional[str] = Field(None, description="面试名称（可选）")
    session_type: SessionType = Field(..., description="面试类型（必填）")
    difficulty_level: DifficultyLevel = Field(..., description="面试难度（必填）")

class DifyAddQARequest(BaseModel):
    """Dify添加题目和回答请求"""
    session_id: str = Field(..., description="面试会话ID")
    question_text: str = Field(..., description="题目内容")
    question_type: QuestionType = Field(QuestionType.TECHNICAL, description="题目类型")
    question_category: Optional[str] = Field(None, description="题目分类")
    candidate_answer: str = Field(..., description="面试者回答")
    interviewer_feedback: str = Field(..., description="面试官反馈")
    overall_score: float = Field(..., ge=0, le=10, description="综合评分")
    knowledge_points: Optional[str] = Field(None, description="题目知识点关键词，JSON格式")

# Dify专用响应模型
class DifyCreateInterviewResponse(BaseModel):
    """Dify创建面试记录响应"""
    success: bool
    session_id: str
    user_id: str
    session_name: str
    status: str
    created_at: str
    message: str

class DifyAddQAResponse(BaseModel):
    """Dify添加题目和回答响应"""
    success: bool
    question_id: str
    session_id: str
    status: str
    message: str

class DifyLatestInterviewResponse(BaseModel):
    """Dify最新面试信息响应"""
    success: bool
    user_id: str
    latest_session: Optional[dict]
    message: str

class DifyInterviewSummaryResponse(BaseModel):
    """Dify面试总结响应"""
    success: bool
    session_id: str
    summary: dict
    questions_summary: List[dict]
    message: str

# 标准请求模型
class CreateSessionRequest(BaseModel):
    """创建面试会话请求"""
    user_id: str
    session_name: Optional[str] = None
    session_type: SessionType  # 必填字段
    difficulty_level: DifficultyLevel  # 必填字段
    estimated_duration: int = Field(60, ge=10, le=300)

class BatchQuestionRequest(BaseModel):
    """批量添加题目请求"""
    session_id: str
    questions: List[dict]

class SubmitAnswerRequest(BaseModel):
    """提交回答请求"""
    question_id: str
    candidate_answer: str
    answer_duration: Optional[int] = None

class SubmitFeedbackRequest(BaseModel):
    """提交反馈请求"""
    interviewer_feedback: str
    technical_accuracy: Optional[float] = Field(None, ge=0, le=10)
    communication_clarity: Optional[float] = Field(None, ge=0, le=10)
    problem_solving: Optional[float] = Field(None, ge=0, le=10)
    overall_score: float = Field(..., ge=0, le=10)
    answer_quality: Optional[AnswerQuality] = None

# 标准响应模型
class BaseResponse(BaseModel):
    """基础响应模型"""
    success: bool
    message: str

class InterviewSessionResponse(BaseResponse):
    """面试会话响应"""
    session_id: Optional[str] = None
    data: Optional[dict] = None

class HealthCheckResponse(BaseModel):
    """健康检查响应"""
    status: str
    timestamp: str
    database_connected: bool
    external_services: dict
    stats: Optional[dict] = None

# ==================== 错题相关模型 ====================

class WrongQuestionItem(BaseModel):
    """错题项目模型"""
    question_id: str
    session_id: str
    question_text: str
    question_type: str
    question_category: Optional[str] = None
    difficulty_level: str
    candidate_answer: str
    interviewer_feedback: str
    overall_score: float
    knowledge_points: Optional[str] = None
    answered_at: Optional[str] = None
    reviewed_at: Optional[str] = None

class DifyWrongQuestionResponse(BaseModel):
    """Dify错题查询响应"""
    success: bool
    user_id: str
    wrong_questions: List[WrongQuestionItem]
    total: int
    message: str

class WrongQuestionResponse(BaseModel):
    """标准错题查询响应"""
    success: bool
    user_id: str
    wrong_questions: List[WrongQuestionItem]
    total: int
    message: str
