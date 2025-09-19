"""
简历分析服务主程序
"""

import os
import logging
import time
from datetime import datetime
from typing import List, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# 导入配置和服务
from config import (
    API_HOST, API_PORT, API_WORKERS, CORS_ORIGINS, CORS_METHODS, CORS_HEADERS,
    LOG_LEVEL, LOG_FORMAT, LOG_FILE, validate_config, get_config_info
)
from models import (
    AnalysisResponse, KeywordsRequest, KeywordsResponse,
    ProfileQueryRequest, ProfileQueryResponse, HealthCheckResponse,
    CandidateProfile, ExtractionMode
)
from mysql_database import DatabaseService
from llm_service import llm_service
from pdf_service import pdf_service

# 配置日志
def setup_logging():
    """设置日志配置"""
    # 创建日志目录
    log_dir = os.path.dirname(LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 配置日志
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper()),
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

# 设置日志
setup_logging()
logger = logging.getLogger(__name__)

# 创建MySQL数据库服务实例
db_service = DatabaseService()

# 应用启动和关闭处理
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("🚀 启动简历分析服务...")
    
    try:
        # 验证配置
        validate_config()
        logger.info("✅ 配置验证通过")
        
        # 连接数据库
        if not db_service.connect():
            raise Exception("数据库连接失败")
        
        # 检查LLM服务
        if not llm_service.is_available():
            raise Exception("LLM服务不可用")
        
        logger.info("🎉 服务启动完成")
        
    except Exception as e:
        logger.error(f"❌ 服务启动失败: {e}")
        raise
    
    yield
    
    # 关闭时执行
    logger.info("🛑 关闭简历分析服务...")
    db_service.disconnect()
    logger.info("✅ 服务已关闭")

# 创建FastAPI应用
app = FastAPI(
    title="简历分析服务",
    description="PDF简历解析、结构化信息提取和存储服务",
    version="1.0.0",
    lifespan=lifespan
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS,
)

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """健康检查"""
    try:
        # 检查数据库连接
        db_connected = db_service.is_connected()
        
        # 检查LLM服务
        llm_available = llm_service.is_available()
        
        # 检查PDF服务
        pdf_status = pdf_service.check_pdf_parser_service()
        
        # 获取统计信息
        stats = None
        if db_connected:
            try:
                profile_count = db_service.get_user_count()
                stats = {
                    "total_profiles": profile_count,
                    "database_status": "connected",
                    "llm_provider": llm_service.provider
                }
            except Exception as e:
                logger.warning(f"获取统计信息失败: {e}")
        
        status = "healthy" if (db_connected and llm_available) else "unhealthy"
        
        return HealthCheckResponse(
            status=status,
            timestamp=datetime.now().isoformat(),
            database_connected=db_connected,
            llm_available=llm_available,
            dependencies={
                "mysql": "connected" if db_connected else "disconnected",
                "llm_service": llm_service.provider if llm_available else "unavailable",
                "pdf_parser_service": "available" if pdf_status["available"] else "unavailable"
            },
            stats=stats
        )
        
    except Exception as e:
        logger.error(f"健康检查失败: {e}")
        return HealthCheckResponse(
            status="error",
            timestamp=datetime.now().isoformat(),
            database_connected=False,
            llm_available=False
        )

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    user_id: str = Form(...),
    file: UploadFile = File(...),
    extraction_mode: str = Form("comprehensive"),
    overwrite: bool = Form(True)
):
    """分析简历文件"""
    start_time = time.time()
    
    try:
        logger.info(f"开始分析简历: user_id={user_id}, filename={file.filename}")
        
        # 检查用户是否已存在
        if not overwrite and db_service.profile_exists(user_id):
            return AnalysisResponse(
                success=False,
                user_id=user_id,
                message="用户档案已存在，设置overwrite=true以覆盖"
            )
        
        # 1. 解析PDF文件
        logger.info("步骤1: 解析PDF文件")
        resume_text = pdf_service.parse_pdf(file, use_local=True)  # 强制使用本地解析
        
        if not resume_text or len(resume_text.strip()) < 50:
            raise HTTPException(status_code=400, detail="PDF文件内容过少或解析失败")
        
        # 2. LLM结构化提取
        logger.info("步骤2: LLM结构化信息提取")
        structured_info = llm_service.extract_resume_info(resume_text)
        
        # 3. 提取关键词
        logger.info("步骤3: 提取关键词")
        keywords_data = llm_service.extract_keywords(structured_info)
        
        # 4. 构建候选人档案
        logger.info("步骤4: 构建候选人档案")
        profile = CandidateProfile(
            user_id=user_id,
            extraction_mode=ExtractionMode(extraction_mode),
            source_filename=file.filename,
            # 简化的关键词字段
            technical_skills=keywords_data.get("technical_skills", []),
            projects_keywords=keywords_data.get("projects", []),
            direction=keywords_data.get("direction", "未知"),
            # 兼容旧版本字段
            extracted_keywords=keywords_data.get("technical_skills", []),
            technical_keywords=keywords_data.get("technical_skills", []),
            domain_keywords=[]
        )
        
        # 填充结构化信息
        if "personal_info" in structured_info:
            profile.personal_info = profile.personal_info.parse_obj(structured_info["personal_info"])
        
        # 5. 保存到数据库
        logger.info("步骤5: 保存到数据库")
        if not db_service.save_profile(profile, overwrite):
            raise HTTPException(status_code=500, detail="保存到数据库失败")
        
        processing_time = time.time() - start_time
        
        logger.info(f"简历分析完成: user_id={user_id}, 耗时={processing_time:.2f}秒")
        
        return AnalysisResponse(
            success=True,
            user_id=user_id,
            message="简历分析完成",
            profile=profile,
            keywords=keywords_data.get("technical_skills", []),
            processing_time=processing_time,
            # 新增字段
            technical_skills=keywords_data.get("technical_skills", []),
            projects_keywords=keywords_data.get("projects", []),
            direction=keywords_data.get("direction", "未知")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        processing_time = time.time() - start_time
        error_msg = f"简历分析失败: {str(e)}"
        logger.error(f"{error_msg}, 耗时={processing_time:.2f}秒")
        
        return AnalysisResponse(
            success=False,
            user_id=user_id,
            message=error_msg,
            processing_time=processing_time
        )

@app.post("/keywords", response_model=KeywordsResponse)
async def get_keywords(request: KeywordsRequest):
    """获取用户关键词"""
    try:
        profile = db_service.get_profile(request.user_id)
        
        if not profile:
            return KeywordsResponse(
                success=False,
                user_id=request.user_id,
                message="用户档案不存在"
            )
        
        # 获取简化的关键词结构
        technical_skills = profile.technical_skills if hasattr(profile, 'technical_skills') else profile.technical_keywords
        projects_info = profile.projects_keywords if hasattr(profile, 'projects_keywords') else []
        direction = profile.direction if hasattr(profile, 'direction') else "未知"

        # 根据类别返回关键词（保持兼容性）
        if request.category == "technical":
            keywords = technical_skills
        elif request.category == "projects":
            keywords = [f"{proj['name']}: {', '.join(proj['keywords'])}" for proj in projects_info if isinstance(proj, dict)]
        else:  # all
            keywords = technical_skills

        keywords_string = ", ".join(keywords) if request.format_type == "string" else ""

        return KeywordsResponse(
            success=True,
            user_id=request.user_id,
            keywords=keywords,
            keywords_string=keywords_string,
            technical_keywords=technical_skills,
            domain_keywords=[],  # 简化后不再使用
            message="关键词获取成功",
            # 新增字段
            technical_skills=technical_skills,
            projects_keywords=projects_info,
            direction=direction
        )
        
    except Exception as e:
        logger.error("获取关键词失败: user_id=%s, error=%s", request.user_id, e)
        return KeywordsResponse(
            success=False,
            user_id=request.user_id,
            message="获取关键词失败: " + str(e)
        )

@app.get("/keywords/grouped/{user_id}")
async def get_keywords_for_dify(user_id: str):
    """专门为Dify工作流提供的关键词接口"""
    try:
        profile = db_service.get_profile(user_id)

        if not profile:
            return {
                "success": False,
                "user_id": user_id,
                "message": "用户档案不存在"
            }

        # 获取技术技能、项目信息和方向
        technical_skills = profile.technical_skills if hasattr(profile, 'technical_skills') else profile.technical_keywords
        projects_info = profile.projects_keywords if hasattr(profile, 'projects_keywords') else []
        direction = profile.direction if hasattr(profile, 'direction') else "未知"

        # 格式化项目信息，便于检索
        formatted_projects = []
        for project in projects_info:
            project_name = project.get('name', '')
            keywords = project.get('keywords', [])

            # 为每个项目创建检索友好的格式
            formatted_projects.append({
                "project_name": project_name,
                "keywords": keywords,
                "keywords_text": ", ".join(keywords),
                "search_text": f"{project_name} {' '.join(keywords)}"  # 用于检索的文本
            })

        return {
            "success": True,
            "user_id": user_id,
            "technical_skills": technical_skills,
            "technical_skills_text": ", ".join(technical_skills),
            "projects_keywords": formatted_projects,
            "direction": direction,
            "dify_usage_guide": {
                "technical_skills": "技术技能列表，可以整体检索或分组检索",
                "projects": "每个项目单独检索，使用search_text字段作为检索内容",
                "direction": "个人技术方向，用于专门的方向检索"
            },
            "message": "Dify关键词获取成功"
        }

    except Exception as e:
        logger.error("获取分组关键词失败: user_id=%s, error=%s", user_id, e)
        return {
            "success": False,
            "user_id": user_id,
            "message": "获取分组关键词失败: " + str(e)
        }

@app.post("/parse-pdf")
async def parse_pdf_only(file: UploadFile = File(...)):
    """
    仅解析PDF文件，返回文本内容
    """
    try:
        logger.info(f"开始解析PDF文件: {file.filename}")

        # 验证文件类型
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="只支持PDF文件")

        # 解析PDF文件
        resume_text = pdf_service.parse_pdf(file, use_local=False)  # 使用pdf-parser-service

        return {
            "success": True,
            "filename": file.filename,
            "text_content": resume_text,
            "content_length": len(resume_text),
            "message": "PDF解析成功"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"PDF解析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PDF解析失败: {str(e)}")

@app.post("/profile", response_model=ProfileQueryResponse)
async def query_user_profile(request: ProfileQueryRequest):
    """查询用户档案"""
    try:
        logger.info(f"查询用户档案: user_id={request.user_id}")

        # 获取用户档案
        profile = db_service.get_profile(request.user_id)

        if not profile:
            return ProfileQueryResponse(
                success=False,
                user_id=request.user_id,
                exists=False,
                message="用户档案不存在"
            )

        # 如果不需要关键词，清空相关字段以减少响应大小
        if not request.include_keywords:
            profile.technical_skills = []
            profile.projects_keywords = []
            profile.extracted_keywords = []
            profile.technical_keywords = []
            profile.domain_keywords = []

        return ProfileQueryResponse(
            success=True,
            user_id=request.user_id,
            profile=profile,
            exists=True,
            message="用户档案获取成功"
        )

    except Exception as e:
        logger.error(f"查询用户档案失败: user_id={request.user_id}, error={e}")
        return ProfileQueryResponse(
            success=False,
            user_id=request.user_id,
            exists=False,
            message=f"查询用户档案失败: {str(e)}"
        )

@app.get("/analyze/status/{user_id}")
async def get_analysis_status(user_id: str):
    """
    查询分析状态（简单实现）
    """
    try:
        # 检查用户是否存在
        profile_exists = db_service.profile_exists(user_id)

        return {
            "user_id": user_id,
            "status": "completed" if profile_exists else "not_found",
            "message": "分析已完成" if profile_exists else "用户档案不存在或分析未完成"
        }
    except Exception as e:
        logger.error(f"查询分析状态失败: {e}")
        return {
            "user_id": user_id,
            "status": "error",
            "message": f"查询失败: {str(e)}"
        }

@app.get("/")
async def root():
    """根路径"""
    return {
        "service": "简历分析服务",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "docs": "/docs",
        "health": "/health"
    }

# ==================== 启动服务 ====================
if __name__ == "__main__":
    logger.info(f"启动服务: {API_HOST}:{API_PORT}")
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        workers=API_WORKERS,
        reload=False,
        log_level=LOG_LEVEL.lower(),
        timeout_keep_alive=600,  # 10分钟保持连接
        timeout_graceful_shutdown=30
    )
