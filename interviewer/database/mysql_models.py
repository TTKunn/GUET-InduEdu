"""
MySQL数据库ORM模型定义
用于analysis-service的MySQL数据存储
"""

from sqlalchemy import Column, Integer, BigInteger, String, Text, TIMESTAMP, DECIMAL, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import List, Optional

Base = declarative_base()

class CandidateProfile(Base):
    """候选人档案主表"""
    __tablename__ = 'candidate_profiles'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='自增主键')
    user_id = Column(String(100), unique=True, nullable=False, comment='用户唯一标识')
    
    # 个人信息字段
    name = Column(String(100), comment='姓名')
    phone = Column(String(20), comment='电话')
    email = Column(String(100), comment='邮箱')
    location = Column(String(200), comment='地址')
    
    # 教育背景
    education = Column(Text, comment='教育背景')
    
    # 技术方向
    direction = Column(String(100), comment='技术方向')
    
    # 时间字段
    created_at = Column(TIMESTAMP, server_default=func.now(), comment='创建时间')
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment='更新时间')
    
    # 关联关系
    work_experiences = relationship("WorkExperience", back_populates="profile", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="profile", cascade="all, delete-orphan")
    technical_skills = relationship("TechnicalSkill", back_populates="profile", cascade="all, delete-orphan")
    project_keywords = relationship("ProjectKeyword", back_populates="profile", cascade="all, delete-orphan")
    extracted_keywords = relationship("ExtractedKeyword", back_populates="profile", cascade="all, delete-orphan")

class WorkExperience(Base):
    """工作经验表"""
    __tablename__ = 'work_experiences'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='自增主键')
    user_id = Column(String(100), ForeignKey('candidate_profiles.user_id', ondelete='CASCADE'), nullable=False, comment='用户ID')
    company = Column(String(200), comment='公司名称')
    position = Column(String(100), comment='职位')
    start_date = Column(String(50), comment='开始时间')
    end_date = Column(String(50), comment='结束时间')
    description = Column(Text, comment='工作描述')
    technologies = Column(Text, comment='使用技术')
    sort_order = Column(Integer, default=0, comment='排序序号')
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # 关联关系
    profile = relationship("CandidateProfile", back_populates="work_experiences")

class Project(Base):
    """项目经验表"""
    __tablename__ = 'projects'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='自增主键')
    user_id = Column(String(100), ForeignKey('candidate_profiles.user_id', ondelete='CASCADE'), nullable=False, comment='用户ID')
    name = Column(String(200), nullable=False, comment='项目名称')
    description = Column(Text, comment='项目描述')
    technologies = Column(Text, comment='使用技术')
    role = Column(String(100), comment='担任角色')
    achievements = Column(Text, comment='项目成果')
    sort_order = Column(Integer, default=0, comment='排序序号')
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # 关联关系
    profile = relationship("CandidateProfile", back_populates="projects")

class TechnicalSkill(Base):
    """技术技能表"""
    __tablename__ = 'technical_skills'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='自增主键')
    user_id = Column(String(100), ForeignKey('candidate_profiles.user_id', ondelete='CASCADE'), nullable=False, comment='用户ID')
    skill_name = Column(String(100), nullable=False, comment='技能名称')
    skill_category = Column(String(50), comment='技能分类')
    proficiency_level = Column(String(20), comment='熟练程度')
    sort_order = Column(Integer, default=0, comment='排序序号')
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # 关联关系
    profile = relationship("CandidateProfile", back_populates="technical_skills")

class ProjectKeyword(Base):
    """项目关键词表"""
    __tablename__ = 'project_keywords'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='自增主键')
    user_id = Column(String(100), ForeignKey('candidate_profiles.user_id', ondelete='CASCADE'), nullable=False, comment='用户ID')
    project_name = Column(String(200), nullable=False, comment='项目名称')
    keyword = Column(String(100), nullable=False, comment='关键词')
    keyword_type = Column(String(50), comment='关键词类型')
    relevance_score = Column(DECIMAL(3,2), comment='相关性得分')
    sort_order = Column(Integer, default=0, comment='排序序号')
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # 关联关系
    profile = relationship("CandidateProfile", back_populates="project_keywords")

class ExtractedKeyword(Base):
    """提取关键词表"""
    __tablename__ = 'extracted_keywords'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='自增主键')
    user_id = Column(String(100), ForeignKey('candidate_profiles.user_id', ondelete='CASCADE'), nullable=False, comment='用户ID')
    keyword = Column(String(100), nullable=False, comment='关键词')
    keyword_category = Column(String(50), comment='关键词分类')
    extraction_source = Column(String(50), comment='提取来源')
    frequency = Column(Integer, default=1, comment='出现频次')
    importance_score = Column(DECIMAL(3,2), comment='重要性得分')
    sort_order = Column(Integer, default=0, comment='排序序号')
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # 关联关系
    profile = relationship("CandidateProfile", back_populates="extracted_keywords")
