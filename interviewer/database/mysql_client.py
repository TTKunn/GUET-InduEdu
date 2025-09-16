"""
MySQL数据库连接和操作管理器
用于analysis-service的MySQL数据存储
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
import logging
from typing import Optional, List, Dict, Any

from config import MYSQL_URL
from .mysql_models import Base, CandidateProfile, WorkExperience, Project, TechnicalSkill, ProjectKeyword, ExtractedKeyword

logger = logging.getLogger(__name__)

class MySQLClient:
    """MySQL数据库客户端"""
    
    def __init__(self):
        """初始化MySQL连接"""
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
            raise
    
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
    
    def save_profile(self, profile_data: Dict[str, Any]) -> bool:
        """保存用户档案到MySQL"""
        try:
            with self.get_session() as session:
                # 检查用户是否已存在
                existing_profile = session.query(CandidateProfile).filter_by(
                    user_id=profile_data['user_id']
                ).first()
                
                if existing_profile:
                    # 更新现有档案
                    self._update_profile(session, existing_profile, profile_data)
                    logger.info(f"✅ 更新用户档案: {profile_data['user_id']}")
                else:
                    # 创建新档案
                    self._create_profile(session, profile_data)
                    logger.info(f"✅ 创建用户档案: {profile_data['user_id']}")
                
                return True
                
        except Exception as e:
            logger.error(f"❌ 保存用户档案失败: {e}")
            return False
    
    def _create_profile(self, session: Session, profile_data: Dict[str, Any]):
        """创建新的用户档案"""
        import json

        # 创建主表记录
        personal_info = profile_data.get('personal_info', {})

        # 序列化复杂字段为JSON字符串
        education_json = json.dumps(profile_data.get('education', []), ensure_ascii=False)

        # JSON存储优化：序列化关键词数据
        try:
            technical_skills_json = json.dumps(
                profile_data.get('technical_skills', []),
                ensure_ascii=False
            )
            projects_keywords_json = json.dumps(
                profile_data.get('projects_keywords', []),
                ensure_ascii=False
            )
            education_json_optimized = json.dumps(
                profile_data.get('education', []),
                ensure_ascii=False
            )
            logger.info(f"✅ JSON序列化成功: {profile_data['user_id']}")
        except Exception as e:
            logger.error(f"⚠️  JSON序列化失败: {e}")
            # 使用空JSON作为默认值
            technical_skills_json = "[]"
            projects_keywords_json = "[]"
            education_json_optimized = "[]"

        profile = CandidateProfile(
            user_id=profile_data['user_id'],
            name=personal_info.get('name'),
            phone=personal_info.get('phone'),
            email=personal_info.get('email'),
            location=personal_info.get('location'),
            education=education_json,
            direction=profile_data.get('direction'),
            # 新增JSON字段
            technical_skills_json=technical_skills_json,
            projects_keywords_json=projects_keywords_json,
            education_json=education_json_optimized
        )
        session.add(profile)
        session.flush()  # 获取主键ID
        
        # 保存工作经验
        work_experiences = profile_data.get('work_experience', [])
        for i, work in enumerate(work_experiences):
            work_exp = WorkExperience(
                user_id=profile_data['user_id'],
                company=work.get('company'),
                position=work.get('position'),
                start_date=work.get('start_date'),
                end_date=work.get('end_date'),
                description=work.get('description'),
                technologies=work.get('technologies'),
                sort_order=i
            )
            session.add(work_exp)
        
        # 保存项目经验
        projects = profile_data.get('projects', [])
        for i, proj in enumerate(projects):
            project = Project(
                user_id=profile_data['user_id'],
                name=proj.get('name', ''),
                description=proj.get('description'),
                technologies=proj.get('technologies'),
                role=proj.get('role'),
                achievements=proj.get('achievements'),
                sort_order=i
            )
            session.add(project)
        
        # 保存技术技能
        technical_skills = profile_data.get('technical_skills', [])
        for i, skill in enumerate(technical_skills):
            if isinstance(skill, str):
                skill_record = TechnicalSkill(
                    user_id=profile_data['user_id'],
                    skill_name=skill,
                    sort_order=i
                )
                session.add(skill_record)
        
        # 保存项目关键词
        projects_keywords = profile_data.get('projects_keywords', [])
        for proj_kw in projects_keywords:
            if isinstance(proj_kw, dict):
                project_name = proj_kw.get('name', '')
                keywords = proj_kw.get('keywords', [])
                for i, keyword in enumerate(keywords):
                    kw_record = ProjectKeyword(
                        user_id=profile_data['user_id'],
                        project_name=project_name,
                        keyword=keyword,
                        sort_order=i
                    )
                    session.add(kw_record)
        
        # 保存提取的关键词
        extracted_keywords = profile_data.get('extracted_keywords', [])
        for i, keyword in enumerate(extracted_keywords):
            if isinstance(keyword, str):
                kw_record = ExtractedKeyword(
                    user_id=profile_data['user_id'],
                    keyword=keyword,
                    extraction_source='resume_analysis',
                    sort_order=i
                )
                session.add(kw_record)
    
    def _update_profile(self, session: Session, existing_profile: CandidateProfile, profile_data: Dict[str, Any]):
        """更新现有用户档案"""
        import json

        # 更新主表信息
        personal_info = profile_data.get('personal_info', {})
        existing_profile.name = personal_info.get('name')
        existing_profile.phone = personal_info.get('phone')
        existing_profile.email = personal_info.get('email')
        existing_profile.location = personal_info.get('location')
        # 将education列表转换为JSON字符串
        education_data = profile_data.get('education', [])
        existing_profile.education = json.dumps(education_data, ensure_ascii=False) if education_data else None
        existing_profile.direction = profile_data.get('direction')

        # JSON存储优化：更新JSON字段
        try:
            existing_profile.technical_skills_json = json.dumps(
                profile_data.get('technical_skills', []),
                ensure_ascii=False
            )
            existing_profile.projects_keywords_json = json.dumps(
                profile_data.get('projects_keywords', []),
                ensure_ascii=False
            )
            existing_profile.education_json = json.dumps(
                profile_data.get('education', []),
                ensure_ascii=False
            )
            logger.info(f"✅ JSON字段更新成功: {profile_data['user_id']}")
        except Exception as e:
            logger.error(f"⚠️  JSON序列化失败: {e}")
            # 继续执行，不影响主流程
        
        # 删除旧的关联数据
        session.query(WorkExperience).filter_by(user_id=profile_data['user_id']).delete()
        session.query(Project).filter_by(user_id=profile_data['user_id']).delete()
        session.query(TechnicalSkill).filter_by(user_id=profile_data['user_id']).delete()
        session.query(ProjectKeyword).filter_by(user_id=profile_data['user_id']).delete()
        session.query(ExtractedKeyword).filter_by(user_id=profile_data['user_id']).delete()

        # 重新创建关联数据（仅子表，不新建主表）
        # 保存工作经验
        work_experiences = profile_data.get('work_experience', [])
        for i, work in enumerate(work_experiences):
            work_exp = WorkExperience(
                user_id=profile_data['user_id'],
                company=work.get('company'),
                position=work.get('position'),
                start_date=work.get('start_date'),
                end_date=work.get('end_date'),
                description=work.get('description'),
                technologies=work.get('technologies'),
                sort_order=i
            )
            session.add(work_exp)

        # 保存项目经验
        projects = profile_data.get('projects', [])
        for i, proj in enumerate(projects):
            project = Project(
                user_id=profile_data['user_id'],
                name=proj.get('name', ''),
                description=proj.get('description'),
                technologies=proj.get('technologies'),
                role=proj.get('role'),
                achievements=proj.get('achievements'),
                sort_order=i
            )
            session.add(project)

        # 保存技术技能
        technical_skills = profile_data.get('technical_skills', [])
        for i, skill in enumerate(technical_skills):
            if isinstance(skill, str):
                skill_record = TechnicalSkill(
                    user_id=profile_data['user_id'],
                    skill_name=skill,
                    sort_order=i
                )
                session.add(skill_record)

        # 保存项目关键词
        projects_keywords = profile_data.get('projects_keywords', [])
        for proj_kw in projects_keywords:
            if isinstance(proj_kw, dict):
                project_name = proj_kw.get('name', '')
                keywords = proj_kw.get('keywords', [])
                for i, keyword in enumerate(keywords):
                    kw_record = ProjectKeyword(
                        user_id=profile_data['user_id'],
                        project_name=project_name,
                        keyword=keyword,
                        sort_order=i
                    )
                    session.add(kw_record)

        # 保存提取的关键词
        extracted_keywords = profile_data.get('extracted_keywords', [])
        for i, keyword in enumerate(extracted_keywords):
            if isinstance(keyword, str):
                kw_record = ExtractedKeyword(
                    user_id=profile_data['user_id'],
                    keyword=keyword,
                    extraction_source='resume_analysis',
                    sort_order=i
                )
                session.add(kw_record)

    def get_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """获取用户档案（JSON优化版）"""
        import json

        try:
            with self.get_session() as session:
                profile = session.query(CandidateProfile).filter_by(user_id=user_id).first()

                if not profile:
                    return None

                # 构建返回数据结构（保持与MongoDB格式一致）
                result = {
                    'user_id': profile.user_id,
                    'personal_info': {
                        'name': profile.name,
                        'phone': profile.phone,
                        'email': profile.email,
                        'location': profile.location
                    },
                    'education': profile.education,
                    'direction': profile.direction,
                    'work_experience': [],
                    'projects': [],
                    'technical_skills': [],
                    'projects_keywords': [],
                    'extracted_keywords': [],
                    'created_at': profile.created_at,
                    'updated_at': profile.updated_at
                }

                # JSON优化：优先从JSON字段读取数据
                json_data_available = False

                # 尝试从JSON字段读取技术技能
                if profile.technical_skills_json:
                    try:
                        technical_skills = json.loads(profile.technical_skills_json)
                        result['technical_skills'] = technical_skills
                        result['extracted_keywords'] = technical_skills  # 兼容字段
                        json_data_available = True
                        logger.debug(f"✅ 从JSON读取技术技能: {len(technical_skills)}个")
                    except json.JSONDecodeError as e:
                        logger.warning(f"⚠️  技术技能JSON解析失败: {e}")

                # 尝试从JSON字段读取项目关键词
                if profile.projects_keywords_json:
                    try:
                        projects_keywords = json.loads(profile.projects_keywords_json)
                        result['projects_keywords'] = projects_keywords
                        json_data_available = True
                        logger.debug(f"✅ 从JSON读取项目关键词: {len(projects_keywords)}个项目")
                    except json.JSONDecodeError as e:
                        logger.warning(f"⚠️  项目关键词JSON解析失败: {e}")

                # 尝试从JSON字段读取教育背景
                if profile.education_json:
                    try:
                        education = json.loads(profile.education_json)
                        result['education'] = education
                        logger.debug(f"✅ 从JSON读取教育背景: {len(education)}条记录")
                    except json.JSONDecodeError as e:
                        logger.warning(f"⚠️  教育背景JSON解析失败: {e}")

                # 如果JSON数据可用，直接返回（性能优化）
                if json_data_available and result['technical_skills'] and result['projects_keywords']:
                    logger.info(f"✅ JSON数据读取成功: {user_id}")
                    return result

                # 降级机制：从关键词表读取数据
                logger.info(f"⚠️  降级到关键词表查询: {user_id}")

                # 如果JSON中没有技术技能，从表中读取
                if not result['technical_skills']:
                    technical_skills = session.query(TechnicalSkill).filter_by(user_id=user_id).order_by(TechnicalSkill.sort_order).all()
                    result['technical_skills'] = [skill.skill_name for skill in technical_skills]
                    result['extracted_keywords'] = result['technical_skills']  # 兼容字段

                # 如果JSON中没有项目关键词，从表中读取
                if not result['projects_keywords']:
                    project_keywords = session.query(ProjectKeyword).filter_by(user_id=user_id).order_by(ProjectKeyword.project_name, ProjectKeyword.sort_order).all()
                    projects_kw_dict = {}
                    for kw in project_keywords:
                        if kw.project_name not in projects_kw_dict:
                            projects_kw_dict[kw.project_name] = []
                        projects_kw_dict[kw.project_name].append(kw.keyword)

                    result['projects_keywords'] = [
                        {'name': name, 'keywords': keywords}
                        for name, keywords in projects_kw_dict.items()
                    ]

                # 获取工作经验（始终从表中读取，因为通常数据量不大）
                work_experiences = session.query(WorkExperience).filter_by(user_id=user_id).order_by(WorkExperience.sort_order).all()
                result['work_experience'] = [
                    {
                        'company': work.company,
                        'position': work.position,
                        'start_date': work.start_date,
                        'end_date': work.end_date,
                        'description': work.description,
                        'technologies': work.technologies
                    }
                    for work in work_experiences
                ]

                # 获取项目经验（始终从表中读取，因为通常数据量不大）
                projects = session.query(Project).filter_by(user_id=user_id).order_by(Project.sort_order).all()
                result['projects'] = [
                    {
                        'name': proj.name,
                        'description': proj.description,
                        'technologies': proj.technologies,
                        'role': proj.role,
                        'achievements': proj.achievements
                    }
                    for proj in projects
                ]

                logger.info(f"✅ 用户档案读取完成: {user_id}")
                return result
                
        except Exception as e:
            logger.error(f"❌ 获取用户档案失败: {e}")
            return None
    
    def get_user_count(self) -> int:
        """获取用户总数"""
        try:
            with self.get_session() as session:
                return session.query(CandidateProfile).count()
        except Exception as e:
            logger.error(f"❌ 获取用户总数失败: {e}")
            return 0
