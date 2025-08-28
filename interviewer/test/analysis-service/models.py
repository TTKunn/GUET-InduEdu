"""
数据模型定义
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum

# ==================== 枚举类型 ====================
class ExtractionMode(str, Enum):
    """提取模式"""
    BASIC = "basic"
    COMPREHENSIVE = "comprehensive"
    KEYWORDS_ONLY = "keywords_only"

# ==================== 基础数据模型 ====================
class PersonalInfo(BaseModel):
    """个人基本信息"""
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    location: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None

class Education(BaseModel):
    """教育经历"""
    school: Optional[str] = None
    degree: Optional[str] = None
    major: Optional[str] = None
    graduation_year: Optional[str] = None
    gpa: Optional[str] = None
    description: Optional[str] = None

class WorkExperience(BaseModel):
    """工作经历"""
    company: Optional[str] = None
    position: Optional[str] = None
    duration: Optional[str] = None
    responsibilities: Optional[str] = None
    achievements: Optional[str] = None
    skills_used: List[str] = Field(default_factory=list)

class Project(BaseModel):
    """项目经历"""
    name: Optional[str] = None
    description: Optional[str] = None
    role: Optional[str] = None
    duration: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)
    achievements: Optional[str] = None
    team_size: Optional[str] = None

class TechnicalSkills(BaseModel):
    """技术技能"""
    programming_languages: List[str] = Field(default_factory=list)
    frameworks: List[str] = Field(default_factory=list)
    databases: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)

class AdditionalInfo(BaseModel):
    """附加信息"""
    languages: List[str] = Field(default_factory=list)
    hobbies: List[str] = Field(default_factory=list)
    awards: List[str] = Field(default_factory=list)
    publications: List[str] = Field(default_factory=list)
    volunteer_experience: List[str] = Field(default_factory=list)

# ==================== 主要数据模型 ====================
class CandidateProfile(BaseModel):
    """候选人完整档案"""
    user_id: str = Field(..., description="用户唯一标识符")
    personal_info: PersonalInfo = Field(default_factory=PersonalInfo)
    education: List[Education] = Field(default_factory=list)
    work_experience: List[WorkExperience] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    technical_skills: TechnicalSkills = Field(default_factory=TechnicalSkills)
    additional_info: AdditionalInfo = Field(default_factory=AdditionalInfo)
    
    # 简化的关键词结构（用于Dify工作流检索）
    technical_skills: List[str] = Field(default_factory=list, description="个人技术点")
    projects_keywords: List[Dict[str, Any]] = Field(default_factory=list, description="个人项目信息")
    direction: str = Field(default="未知", description="个人技术方向（一个词）")

    # 兼容旧版本字段
    extracted_keywords: List[str] = Field(default_factory=list, description="兼容字段")
    technical_keywords: List[str] = Field(default_factory=list, description="兼容字段")
    domain_keywords: List[str] = Field(default_factory=list, description="兼容字段")
    
    # 元数据
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    extraction_mode: ExtractionMode = ExtractionMode.COMPREHENSIVE
    source_filename: Optional[str] = None

# ==================== 请求/响应模型 ====================
class AnalysisRequest(BaseModel):
    """分析请求"""
    user_id: str = Field(..., description="用户唯一标识符")
    extraction_mode: ExtractionMode = ExtractionMode.COMPREHENSIVE
    overwrite: bool = Field(default=True, description="是否覆盖已存在的数据")

class AnalysisResponse(BaseModel):
    """分析响应"""
    success: bool
    user_id: str
    message: str
    profile: Optional[CandidateProfile] = None
    keywords: Optional[List[str]] = None
    processing_time: Optional[float] = None

    # 新增字段
    technical_skills: Optional[List[str]] = None
    projects_keywords: Optional[List[Dict[str, Any]]] = None
    direction: Optional[str] = None

class KeywordsRequest(BaseModel):
    """关键词请求"""
    user_id: str = Field(..., description="用户唯一标识符")
    category: str = Field(default="all", description="关键词类别：technical, domain, all")
    format_type: str = Field(default="list", description="返回格式：list, string")

class KeywordsResponse(BaseModel):
    """关键词响应"""
    success: bool
    user_id: str
    keywords: List[str] = Field(default_factory=list)
    keywords_string: str = ""
    technical_keywords: List[str] = Field(default_factory=list)
    domain_keywords: List[str] = Field(default_factory=list)
    message: str = ""

    # 新增字段
    technical_skills: List[str] = Field(default_factory=list, description="技术技能列表")
    projects_keywords: List[Dict[str, Any]] = Field(default_factory=list, description="项目关键词信息")
    direction: str = Field(default="未知", description="技术方向")

class ProfileQueryRequest(BaseModel):
    """档案查询请求"""
    user_id: str = Field(..., description="用户唯一标识符")
    include_keywords: bool = Field(default=True, description="是否包含关键词")

class ProfileQueryResponse(BaseModel):
    """档案查询响应"""
    success: bool
    user_id: str
    profile: Optional[CandidateProfile] = None
    exists: bool = False
    message: str = ""

class HealthCheckResponse(BaseModel):
    """健康检查响应"""
    status: str
    timestamp: str
    version: str = "1.0.0"
    database_connected: bool = False
    llm_available: bool = False
    dependencies: Dict[str, str] = Field(default_factory=dict)
    stats: Optional[Dict[str, Any]] = None

# ==================== 数据库模型转换 ====================
def profile_to_dict(profile: CandidateProfile) -> Dict[str, Any]:
    """将Profile模型转换为字典（用于MongoDB存储）"""
    data = profile.dict()
    data['created_at'] = profile.created_at
    data['updated_at'] = profile.updated_at
    return data

def dict_to_profile(data: Dict[str, Any]) -> CandidateProfile:
    """将字典转换为Profile模型（从MongoDB读取）"""
    data.pop('_id', None)
    return CandidateProfile(**data)
