"""
面试记录服务主程序
"""

import os
import logging
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# 导入配置和服务
from config import (
    API_HOST, API_PORT, API_WORKERS, CORS_ORIGINS, CORS_METHODS, CORS_HEADERS,
    LOG_LEVEL, LOG_FORMAT, LOG_FILE, validate_config, get_config_info,
    ANALYSIS_SERVICE_URL
)
from models import (
    DifyCreateInterviewRequest, DifyCreateInterviewResponse,
    DifyAddQARequest, DifyAddQAResponse,
    DifyLatestInterviewResponse, DifyInterviewSummaryResponse,
    CreateSessionRequest, InterviewSessionResponse,
    HealthCheckResponse, BaseResponse,
    DifyWrongQuestionResponse, WrongQuestionResponse
)
from interview_service import InterviewService

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

# 创建面试服务实例
interview_service = InterviewService()

# 应用启动和关闭处理
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("🚀 启动面试记录服务...")
    
    try:
        # 验证配置
        validate_config()
        logger.info("✅ 配置验证通过")
        
        # 连接数据库（允许失败，稍后可以重新连接）
        db_connected = interview_service.db.test_connection()
        if not db_connected:
            logger.warning("⚠️  数据库连接失败，服务将在有限模式下启动")
        
        # 创建数据库表
        interview_service.db.create_tables()
        
        logger.info("🎉 服务启动完成")
        
    except Exception as e:
        logger.error(f"❌ 服务启动失败: {e}")
        raise
    
    yield
    
    # 关闭时执行
    logger.info("🛑 关闭面试记录服务...")
    logger.info("✅ 服务已关闭")

# 创建FastAPI应用
app = FastAPI(
    title="面试记录服务",
    description="为Dify工作流提供面试记录管理功能的微服务",
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

# ==================== 健康检查 ====================

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """健康检查"""
    try:
        # 检查数据库连接
        db_connected = interview_service.db.test_connection()
        
        # 检查外部服务
        external_services = {
            "analysis_service": "unknown"
        }
        
        try:
            # 简单检查analysis-service是否可达
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{ANALYSIS_SERVICE_URL}/health", timeout=5)
                external_services["analysis_service"] = "available" if response.status_code == 200 else "unavailable"
        except:
            external_services["analysis_service"] = "unavailable"
        
        status = "healthy" if db_connected else "unhealthy"
        
        return HealthCheckResponse(
            status=status,
            timestamp=datetime.now().isoformat(),
            database_connected=db_connected,
            external_services=external_services,
            stats={
                "service_name": "interview-service",
                "port": API_PORT,
                "database_status": "connected" if db_connected else "disconnected"
            }
        )
        
    except Exception as e:
        logger.error(f"健康检查失败: {e}")
        return HealthCheckResponse(
            status="error",
            timestamp=datetime.now().isoformat(),
            database_connected=False,
            external_services={}
        )

# ==================== Dify专用API接口 ====================

@app.post("/dify/interview/create", response_model=DifyCreateInterviewResponse)
async def dify_create_interview(request: DifyCreateInterviewRequest):
    """Dify专用：创建面试记录"""
    try:
        logger.info(f"Dify创建面试记录: user_id={request.user_id}, session_name={request.session_name}")
        
        result = interview_service.dify_create_interview(
            user_id=request.user_id,
            session_name=request.session_name,
            session_type=request.session_type.value,
            difficulty_level=request.difficulty_level.value
        )
        
        if not result or not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("message", "创建面试记录失败"))
        
        return DifyCreateInterviewResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Dify创建面试记录失败: {e}")
        raise HTTPException(status_code=500, detail=f"创建失败: {str(e)}")

@app.post("/dify/interview/add-qa", response_model=DifyAddQAResponse)
async def dify_add_qa(request: DifyAddQARequest):
    """Dify专用：添加题目和回答记录"""
    try:
        logger.info(f"Dify添加题目和回答: session_id={request.session_id}")
        
        result = interview_service.dify_add_qa(
            session_id=request.session_id,
            question_text=request.question_text,
            question_type=request.question_type.value,
            question_category=request.question_category,
            candidate_answer=request.candidate_answer,
            interviewer_feedback=request.interviewer_feedback,
            overall_score=request.overall_score,
            knowledge_points=request.knowledge_points
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("message", "添加题目和回答失败"))
        
        return DifyAddQAResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Dify添加题目和回答失败: {e}")
        raise HTTPException(status_code=500, detail=f"添加失败: {str(e)}")

@app.get("/dify/interview/{user_id}/latest", response_model=DifyLatestInterviewResponse)
async def dify_get_latest_interview(user_id: str):
    """Dify专用：获取最新面试信息"""
    try:
        logger.info(f"Dify获取最新面试信息: user_id={user_id}")
        
        result = interview_service.dify_get_latest_interview(user_id)
        
        return DifyLatestInterviewResponse(**result)
        
    except Exception as e:
        logger.error(f"Dify获取最新面试信息失败: {e}")
        return DifyLatestInterviewResponse(
            success=False,
            user_id=user_id,
            latest_session=None,
            message=f"获取失败: {str(e)}"
        )

@app.get("/dify/interview/{session_id}/summary", response_model=DifyInterviewSummaryResponse)
async def dify_get_interview_summary(session_id: str):
    """Dify专用：获取面试总结"""
    try:
        logger.info(f"Dify获取面试总结: session_id={session_id}")
        
        result = interview_service.dify_get_interview_summary(session_id)
        
        if not result.get("success"):
            raise HTTPException(status_code=404, detail=result.get("message", "面试会话不存在"))
        
        return DifyInterviewSummaryResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Dify获取面试总结失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取失败: {str(e)}")

# ==================== 标准API接口 ====================

@app.post("/interview/sessions", response_model=InterviewSessionResponse)
async def create_session(request: CreateSessionRequest):
    """创建面试会话"""
    try:
        logger.info(f"创建面试会话: user_id={request.user_id}, session_name={request.session_name}")
        
        result = interview_service.create_session(
            user_id=request.user_id,
            session_name=request.session_name,
            session_type=request.session_type.value,
            difficulty_level=request.difficulty_level.value,
            estimated_duration=request.estimated_duration
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("message", "创建面试会话失败"))
        
        return InterviewSessionResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"创建面试会话失败: {e}")
        raise HTTPException(status_code=500, detail=f"创建失败: {str(e)}")

@app.get("/interview/sessions/{user_id}")
async def get_user_sessions(
    user_id: str,
    status: Optional[str] = Query(None, description="过滤状态"),
    limit: int = Query(10, ge=1, le=50, description="返回数量限制")
):
    """获取用户面试会话列表"""
    try:
        logger.info(f"获取用户面试会话列表: user_id={user_id}")
        
        result = interview_service.get_user_sessions(user_id, status, limit)
        
        return result
        
    except Exception as e:
        logger.error(f"获取用户面试会话列表失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取失败: {str(e)}")

@app.get("/interview/sessions/{session_id}/detail")
async def get_session_detail(session_id: str):
    """获取面试会话详情"""
    try:
        logger.info(f"获取面试会话详情: session_id={session_id}")
        
        result = interview_service.get_session_detail(session_id)
        
        if not result.get("success"):
            raise HTTPException(status_code=404, detail=result.get("message", "面试会话不存在"))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取面试会话详情失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取失败: {str(e)}")

@app.post("/interview/sessions/{session_id}/start")
async def start_session(session_id: str):
    """开始面试"""
    try:
        logger.info(f"开始面试: session_id={session_id}")
        
        result = interview_service.start_session(session_id)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("message", "开始面试失败"))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"开始面试失败: {e}")
        raise HTTPException(status_code=500, detail=f"开始失败: {str(e)}")

@app.post("/interview/sessions/{session_id}/finish")
async def finish_session(session_id: str, interviewer_notes: Optional[str] = None):
    """结束面试"""
    try:
        logger.info(f"结束面试: session_id={session_id}")
        
        result = interview_service.finish_session(session_id, interviewer_notes)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("message", "结束面试失败"))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"结束面试失败: {e}")
        raise HTTPException(status_code=500, detail=f"结束失败: {str(e)}")

# ==================== 错题查询接口 ====================

@app.get("/dify/interview/{user_id}/wrong-questions", response_model=DifyWrongQuestionResponse)
async def dify_get_wrong_questions(
    user_id: str,
    question_type: Optional[str] = Query(None, description="题目类型筛选"),
    limit: int = Query(10, ge=1, le=50, description="返回数量限制")
):
    """Dify专用：获取用户错题"""
    try:
        logger.info(f"Dify获取用户错题: user_id={user_id}")

        result = interview_service.dify_get_wrong_questions(
            user_id=user_id,
            question_type=question_type,
            limit=limit
        )

        return DifyWrongQuestionResponse(**result)

    except Exception as e:
        logger.error(f"Dify获取用户错题失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取失败: {str(e)}")

@app.get("/interview/wrong-questions/{user_id}", response_model=WrongQuestionResponse)
async def get_user_wrong_questions(
    user_id: str,
    question_type: Optional[str] = Query(None, description="题目类型筛选"),
    difficulty_level: Optional[str] = Query(None, description="题目难度筛选"),
    limit: int = Query(10, ge=1, le=50, description="返回数量限制")
):
    """获取用户错题列表"""
    try:
        logger.info(f"获取用户错题: user_id={user_id}")

        result = interview_service.get_user_wrong_questions(
            user_id=user_id,
            question_type=question_type,
            difficulty_level=difficulty_level,
            limit=limit
        )

        return WrongQuestionResponse(**result)

    except Exception as e:
        logger.error(f"获取用户错题失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取失败: {str(e)}")

@app.get("/dify/interview/{user_id}/wrong-question-keywords")
async def dify_get_wrong_question_keywords(
    user_id: str,
    required_count: int = Query(5, ge=1, le=20, description="需要的关键词组数量（对应错题数量）"),
    question_type: Optional[str] = Query(None, description="题目类型筛选")
):
    """Dify专用：获取错题关键词组合，返回m组关键词用于循环生成题目"""
    try:
        logger.info(f"Dify获取错题关键词: user_id={user_id}, count={required_count}")

        result = interview_service.get_wrong_question_keywords_for_dify(
            user_id=user_id,
            required_count=required_count,
            question_type=question_type
        )

        return result

    except Exception as e:
        logger.error(f"Dify获取错题关键词失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取关键词失败: {str(e)}")

@app.get("/")
async def root():
    """根路径"""
    return {
        "service": "面试记录服务",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "docs": "/docs",
        "health": "/health",
        "dify_apis": {
            "create_interview": "/dify/interview/create",
            "add_qa": "/dify/interview/add-qa",
            "latest_interview": "/dify/interview/{user_id}/latest",
            "interview_summary": "/dify/interview/{session_id}/summary",
            "wrong_questions": "/dify/interview/{user_id}/wrong-questions",
            "wrong_question_keywords": "/dify/interview/{user_id}/wrong-question-keywords"
        },
        "standard_apis": {
            "wrong_questions": "/interview/wrong-questions/{user_id}"
        }
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
