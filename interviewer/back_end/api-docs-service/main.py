#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI智能面试官项目 - 统一API文档服务
端口: 8000
功能: 提供所有微服务的统一API文档
"""

from fastapi import FastAPI, HTTPException, Query, Path, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uvicorn
from datetime import datetime

# 创建FastAPI应用
app = FastAPI(
    title="AI智能面试官项目 - 统一API文档",
    description="""
    ## 项目概述
    AI智能面试官项目是一个基于微服务架构的智能面试系统，包含4个核心微服务：
    
    - **PDF解析服务** (端口8003) - 解析简历PDF文件
    - **简历分析服务** (端口8004) - 使用LLM分析简历内容  
    - **向量存储服务** (端口8005) - 向量化存储和检索
    - **面试记录服务** (端口8006) - 面试记录管理
    
    ## 技术栈
    - **后端框架**: FastAPI + Python 3.10+
    - **数据库**: MySQL 8.0 + Milvus 2.3+
    - **LLM服务**: 智谱AI GLM-4
    - **部署方式**: 直接运行（非Docker）
    
    ## 服务地址
    - PDF解析服务: http://43.142.157.145:8003
    - 简历分析服务: http://43.142.157.145:8004
    - 向量存储服务: http://43.142.157.145:8005
    - 面试记录服务: http://43.142.157.145:8006
    
    本文档整合了所有服务的API接口，提供统一的查阅入口。
    """,
    version="1.0.0",
    contact={
        "name": "AI智能面试官项目团队",
        "url": "http://43.142.157.145:8000",
    },
    license_info={
        "name": "MIT License",
    },
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== 通用模型 ====================

class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str = Field(..., description="服务状态")
    timestamp: str = Field(..., description="检查时间")
    service: Optional[str] = Field(None, description="服务名称")
    version: Optional[str] = Field(None, description="服务版本")
    database_connected: Optional[bool] = Field(None, description="数据库连接状态")
    external_services: Optional[Dict[str, str]] = Field(None, description="外部服务状态")
    stats: Optional[Dict[str, Any]] = Field(None, description="统计信息")

class BaseResponse(BaseModel):
    """基础响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")

# ==================== PDF解析服务模型 ====================

class DocumentModel(BaseModel):
    """文档模型"""
    page_content: str = Field(..., description="页面内容")
    metadata: Dict[str, Any] = Field(..., description="元数据")

class ParseResponse(BaseModel):
    """解析响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    task_id: str = Field(..., description="任务ID")
    total_documents: int = Field(..., description="文档总数")
    total_chars: int = Field(..., description="总字符数")
    avg_chars: float = Field(..., description="平均字符数")
    total_pages: Optional[int] = Field(None, description="总页数")
    processing_time: float = Field(..., description="处理时间(秒)")
    documents: Optional[List[DocumentModel]] = Field(None, description="文档列表")

class TextParseResponse(BaseModel):
    """文本解析响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    task_id: str = Field(..., description="任务ID")
    text_content: str = Field(..., description="解析后的文本内容")
    total_chars: int = Field(..., description="总字符数")
    processing_time: float = Field(..., description="处理时间(秒)")

class SearchResponse(BaseModel):
    """搜索响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    collection_name: str = Field(..., description="集合名称")
    query: str = Field(..., description="查询内容")
    total_results: int = Field(..., description="结果总数")
    results: List[Dict[str, Any]] = Field(..., description="搜索结果")
    processing_time: float = Field(..., description="处理时间(秒)")

# ==================== 简历分析服务模型 ====================

class AnalysisResponse(BaseModel):
    """分析响应模型"""
    success: bool = Field(..., description="是否成功")
    user_id: str = Field(..., description="用户ID")
    analysis_result: Dict[str, Any] = Field(..., description="分析结果")
    message: str = Field(..., description="响应消息")

class KeywordsResponse(BaseModel):
    """关键词响应"""
    success: bool = Field(..., description="是否成功")
    user_id: str = Field(..., description="用户ID")
    keywords: List[str] = Field(default_factory=list, description="关键词列表")
    keywords_string: str = Field(default="", description="关键词字符串")
    technical_keywords: List[str] = Field(default_factory=list, description="技术关键词")
    domain_keywords: List[str] = Field(default_factory=list, description="领域关键词")
    technical_skills: List[str] = Field(default_factory=list, description="技术技能列表")
    projects_keywords: List[Dict[str, Any]] = Field(default_factory=list, description="项目关键词信息")
    direction: str = Field(default="未知", description="技术方向")
    message: str = Field(default="", description="响应消息")

class ProfileResponse(BaseModel):
    """档案响应模型"""
    success: bool = Field(..., description="是否成功")
    user_id: str = Field(..., description="用户ID")
    profile: Optional[Dict[str, Any]] = Field(None, description="用户档案")
    exists: bool = Field(default=False, description="档案是否存在")
    message: str = Field(default="", description="响应消息")

# ==================== 向量存储服务模型 ====================

class StoreResponse(BaseModel):
    """存储响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    collection_name: str = Field(..., description="集合名称")
    stored_count: int = Field(..., description="存储数量")
    processing_time: float = Field(..., description="处理时间(秒)")

class VectorSearchResponse(BaseModel):
    """向量搜索响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    collection_name: str = Field(..., description="集合名称")
    query: str = Field(..., description="查询内容")
    total_results: int = Field(..., description="结果总数")
    results: List[Dict[str, Any]] = Field(..., description="搜索结果")
    processing_time: float = Field(..., description="处理时间(秒)")

class CollectionStatsResponse(BaseModel):
    """集合统计响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    collection_name: str = Field(..., description="集合名称")
    row_count: int = Field(..., description="行数")
    embedding_model: str = Field(..., description="嵌入模型")
    processing_time: float = Field(..., description="处理时间(秒)")

# ==================== 面试记录服务模型 ====================

class DifyCreateInterviewResponse(BaseModel):
    """Dify创建面试记录响应"""
    success: bool = Field(..., description="是否成功")
    session_id: str = Field(..., description="会话ID")
    user_id: str = Field(..., description="用户ID")
    session_name: str = Field(..., description="会话名称")
    status: str = Field(..., description="会话状态")
    created_at: str = Field(..., description="创建时间")
    message: str = Field(..., description="响应消息")

class DifyAddQAResponse(BaseModel):
    """Dify添加题目和回答响应"""
    success: bool = Field(..., description="是否成功")
    question_id: str = Field(..., description="题目ID")
    session_id: str = Field(..., description="会话ID")
    status: str = Field(..., description="状态")
    message: str = Field(..., description="响应消息")

class WrongQuestionItem(BaseModel):
    """错题项目模型"""
    question_id: str = Field(..., description="题目ID")
    session_id: str = Field(..., description="会话ID")
    question_text: str = Field(..., description="题目内容")
    question_type: str = Field(..., description="题目类型")
    question_category: Optional[str] = Field(None, description="题目分类")
    difficulty_level: str = Field(..., description="难度级别")
    candidate_answer: str = Field(..., description="候选人回答")
    interviewer_feedback: str = Field(..., description="面试官反馈")
    overall_score: float = Field(..., description="综合评分")
    knowledge_points: Optional[str] = Field(None, description="知识点关键词，字符串格式存储")
    answered_at: Optional[str] = Field(None, description="回答时间")
    reviewed_at: Optional[str] = Field(None, description="审查时间")

class WrongQuestionResponse(BaseModel):
    """错题查询响应"""
    success: bool = Field(..., description="是否成功")
    user_id: str = Field(..., description="用户ID")
    wrong_questions: List[WrongQuestionItem] = Field(..., description="错题列表")
    total: int = Field(..., description="总数")
    message: str = Field(..., description="响应消息")

# ==================== 健康检查接口 ====================

@app.get("/health", response_model=HealthResponse, tags=["系统监控"])
async def health_check():
    """
    统一API文档服务健康检查
    
    检查API文档服务的运行状态
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        service="api-docs-service",
        version="1.0.0"
    )

# ==================== PDF解析服务接口 ====================

@app.post("/pdf-parser/parse", response_model=ParseResponse, tags=["PDF解析服务"])
async def parse_pdf(
    file: UploadFile = File(..., description="上传的PDF文件，最大10MB"),
    chunk_size: int = Query(1000, description="文档分块大小，范围100-5000", ge=100, le=5000),
    chunk_overlap: int = Query(200, description="分块重叠大小，范围0-1000", ge=0, le=1000),
    split_text: bool = Query(True, description="是否进行文本分块"),
    return_content: bool = Query(False, description="是否返回解析内容")
):
    """
    解析PDF文件（完整结构化数据）
    
    将PDF文件解析为结构化的文档对象，支持分块处理
    
    **实际服务地址**: http://43.142.157.145:8003/parse
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8003/parse")

@app.post("/pdf-parser/parse-text", response_model=TextParseResponse, tags=["PDF解析服务"])
async def parse_pdf_text(
    file: UploadFile = File(..., description="上传的PDF文件，最大10MB"),
    split_text: bool = Query(False, description="是否分割文本")
):
    """
    解析PDF文件（纯文本）
    
    将PDF文件解析为纯文本内容，适用于简单的文本提取需求
    
    **实际服务地址**: http://43.142.157.145:8003/parse-text
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8003/parse-text")

@app.post("/pdf-parser/parse-and-store", response_model=ParseResponse, tags=["PDF解析服务"])
async def parse_and_store_pdf(
    file: UploadFile = File(..., description="上传的PDF文件"),
    collection_name: str = Query("pdf_documents", description="Milvus集合名称"),
    chunk_size: int = Query(1000, description="文档分块大小", ge=100, le=5000),
    chunk_overlap: int = Query(200, description="分块重叠大小", ge=0, le=1000),
    embedding_model: str = Query("zhipuai", description="嵌入模型类型")
):
    """
    解析PDF文件并存储到向量数据库

    解析PDF文件并将结果存储到Milvus向量数据库中，支持后续的语义搜索

    **实际服务地址**: http://43.142.157.145:8003/parse-and-store
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8003/parse-and-store")

@app.get("/pdf-parser/search", response_model=SearchResponse, tags=["PDF解析服务"])
async def search_documents(
    query: str = Query(..., description="搜索查询内容"),
    collection_name: str = Query("pdf_documents", description="Milvus集合名称"),
    top_k: int = Query(5, description="返回结果数量", ge=1, le=50)
):
    """
    搜索文档

    在指定的集合中搜索与查询内容相关的文档

    **实际服务地址**: http://43.142.157.145:8003/search
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8003/search")

# ==================== 简历分析服务接口 ====================

@app.post("/analysis/analyze", response_model=AnalysisResponse, tags=["简历分析服务"])
async def analyze_resume(
    user_id: str = Query(..., description="用户唯一标识符"),
    file: UploadFile = File(..., description="PDF简历文件"),
    extraction_mode: str = Query("comprehensive", description="提取模式，可选值comprehensive/basic"),
    overwrite: bool = Query(True, description="是否覆盖已存在的档案")
):
    """
    分析简历文件

    使用LLM对简历内容进行智能分析，提取关键信息和技能

    **实际服务地址**: http://43.142.157.145:8004/analyze
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8004/analyze")

@app.post("/analysis/keywords", response_model=KeywordsResponse, tags=["简历分析服务"])
async def get_keywords(
    user_id: str = Query(..., description="用户唯一标识符"),
    category: str = Query("all", description="关键词类别：technical, domain, all"),
    format_type: str = Query("list", description="返回格式：list, string")
):
    """
    获取用户关键词

    获取指定用户的技能关键词，支持不同类别和格式

    **实际服务地址**: http://43.142.157.145:8004/keywords
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8004/keywords")

@app.get("/analysis/keywords/grouped/{user_id}", response_model=KeywordsResponse, tags=["简历分析服务"])
async def get_grouped_keywords(
    user_id: str = Path(..., description="用户唯一标识符")
):
    """
    获取Dify格式关键词

    获取适用于Dify工作流的格式化关键词数据

    **实际服务地址**: http://43.142.157.145:8004/keywords/grouped/{user_id}
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8004/keywords/grouped/{user_id}")

@app.post("/analysis/profile", response_model=ProfileResponse, tags=["简历分析服务"])
async def query_profile(
    user_id: str = Query(..., description="用户唯一标识符")
):
    """
    查询用户档案

    查询指定用户的完整档案信息

    **实际服务地址**: http://43.142.157.145:8004/profile
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8004/profile")

@app.get("/analysis/analyze/status/{user_id}", response_model=Dict[str, Any], tags=["简历分析服务"])
async def get_analysis_status(
    user_id: str = Path(..., description="用户唯一标识符")
):
    """
    查询分析状态

    查询指定用户的简历分析状态和进度

    **实际服务地址**: http://43.142.157.145:8004/analyze/status/{user_id}
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8004/analyze/status/{user_id}")

@app.post("/analysis/parse-pdf", response_model=TextParseResponse, tags=["简历分析服务"])
async def parse_pdf_only(
    file: UploadFile = File(..., description="上传的PDF文件")
):
    """
    仅解析PDF文件

    只进行PDF文件解析，不进行LLM分析

    **实际服务地址**: http://43.142.157.145:8004/parse-pdf
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8004/parse-pdf")

# ==================== 向量存储服务接口 ====================

class StoreVectorRequest(BaseModel):
    """存储向量请求模型"""
    texts: List[str] = Field(..., description="文本列表")
    metadatas: Optional[List[Dict[str, Any]]] = Field(None, description="元数据列表")
    collection_name: str = Field("default_collection", description="集合名称")
    embedding_model: str = Field("zhipuai", description="嵌入模型")

@app.post("/vector-storage/store", response_model=StoreResponse, tags=["向量存储服务"])
async def store_vectors(request: StoreVectorRequest):
    """
    存储文本向量

    将文本转换为向量并存储到Milvus数据库

    **实际服务地址**: http://43.142.157.145:8005/store
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8005/store")

class StoreDocumentRequest(BaseModel):
    """存储文档请求模型"""
    documents: List[Dict[str, Any]] = Field(..., description="文档列表")
    collection_name: str = Field("default_collection", description="集合名称")
    embedding_model: str = Field("zhipuai", description="嵌入模型")

@app.post("/vector-storage/store-documents", response_model=StoreResponse, tags=["向量存储服务"])
async def store_documents(request: StoreDocumentRequest):
    """
    存储文档向量

    将文档对象转换为向量并存储到Milvus数据库

    **实际服务地址**: http://43.142.157.145:8005/store-documents
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8005/store-documents")

@app.post("/vector-storage/search", response_model=VectorSearchResponse, tags=["向量存储服务"])
async def search_vectors(
    query: str = Query(..., description="搜索查询"),
    collection_name: str = Query("default_collection", description="集合名称"),
    top_k: int = Query(5, description="返回结果数量", ge=1, le=50),
    embedding_model: str = Query("zhipuai", description="嵌入模型")
):
    """
    向量相似性搜索

    在指定集合中进行向量相似性搜索

    **实际服务地址**: http://43.142.157.145:8005/search
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8005/search")

@app.get("/vector-storage/collections/{collection_name}/stats", response_model=CollectionStatsResponse, tags=["向量存储服务"])
async def get_collection_stats(
    collection_name: str = Path(..., description="集合名称"),
    embedding_model: str = Query("zhipuai", description="嵌入模型")
):
    """
    获取集合统计信息

    获取指定集合的统计信息，包括文档数量等

    **实际服务地址**: http://43.142.157.145:8005/collections/{collection_name}/stats
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8005/collections/{collection_name}/stats")

@app.delete("/vector-storage/collections/{collection_name}", response_model=BaseResponse, tags=["向量存储服务"])
async def delete_collection(
    collection_name: str = Path(..., description="集合名称"),
    embedding_model: str = Query("zhipuai", description="嵌入模型")
):
    """
    删除集合

    删除指定的向量集合及其所有数据

    **实际服务地址**: http://43.142.157.145:8005/collections/{collection_name}
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8005/collections/{collection_name}")

# ==================== 面试记录服务接口 - Dify专用 ====================

class DifyCreateInterviewRequest(BaseModel):
    """Dify创建面试记录请求"""
    user_id: str = Field(..., description="用户唯一标识符")
    session_name: Optional[str] = Field(None, description="面试会话名称")
    session_type: str = Field(..., description="面试类型，可选值：knowledge_based/company_position/resume_customized/wrong_questions")
    difficulty_level: str = Field(..., description="面试难度级别，可选值：easy/medium/hard")

@app.post("/interview/dify/create", response_model=DifyCreateInterviewResponse, tags=["面试记录服务-Dify专用"])
async def create_interview_dify(request: DifyCreateInterviewRequest):
    """
    创建面试记录（Dify专用）

    为Dify工作流创建新的面试记录会话

    **实际服务地址**: http://43.142.157.145:8006/dify/interview/create
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8006/dify/interview/create")

@app.post("/interview/dify/add-qa", response_model=DifyAddQAResponse, tags=["面试记录服务-Dify专用"])
async def add_qa_dify(
    session_id: str = Query(..., description="面试会话ID"),
    question_text: str = Query(..., description="题目内容"),
    question_type: str = Query(..., description="题目类型"),
    candidate_answer: str = Query(..., description="候选人回答"),
    interviewer_feedback: str = Query(..., description="面试官反馈"),
    overall_score: float = Query(..., description="综合评分", ge=0, le=10),
    question_category: str = Query(None, description="题目分类"),
    difficulty_level: str = Query("medium", description="题目难度"),
    knowledge_points: str = Query(None, description="知识点关键词")
):
    """
    添加题目和回答（Dify专用）

    向指定面试会话添加题目和候选人回答记录

    **实际服务地址**: http://43.142.157.145:8006/dify/interview/add-qa
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8006/dify/interview/add-qa")

@app.get("/interview/dify/{user_id}/latest", response_model=Dict[str, Any], tags=["面试记录服务-Dify专用"])
async def get_latest_interview_dify(
    user_id: str = Path(..., description="用户唯一标识符")
):
    """
    获取最新面试信息（Dify专用）

    获取指定用户的最新面试会话信息

    **实际服务地址**: http://43.142.157.145:8006/dify/interview/{user_id}/latest
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8006/dify/interview/{user_id}/latest")

@app.get("/interview/dify/{session_id}/summary", response_model=Dict[str, Any], tags=["面试记录服务-Dify专用"])
async def get_interview_summary_dify(
    session_id: str = Path(..., description="面试会话ID")
):
    """
    获取面试总结（Dify专用）

    获取指定面试会话的统计总结信息

    **实际服务地址**: http://43.142.157.145:8006/dify/interview/{session_id}/summary
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8006/dify/interview/{session_id}/summary")

@app.get("/interview/dify/{user_id}/wrong-questions", response_model=WrongQuestionResponse, tags=["面试记录服务-Dify专用"])
async def get_wrong_questions_dify(
    user_id: str = Path(..., description="用户唯一标识符"),
    question_type: str = Query(None, description="题目类型筛选"),
    difficulty_level: str = Query(None, description="题目难度筛选"),
    limit: int = Query(10, description="返回数量限制", ge=1, le=50)
):
    """
    获取用户错题列表（Dify专用）

    获取指定用户的错题记录，支持类型和难度筛选

    **实际服务地址**: http://43.142.157.145:8006/dify/interview/{user_id}/wrong-questions
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8006/dify/interview/{user_id}/wrong-questions")

@app.get("/interview/dify/{user_id}/wrong-question-keywords", response_model=Dict[str, Any], tags=["面试记录服务-Dify专用"])
async def get_wrong_question_keywords_dify(
    user_id: str = Path(..., description="用户唯一标识符"),
    required_count: int = Query(5, description="需要的关键词组数量", ge=1, le=20),
    question_type: str = Query(None, description="题目类型筛选")
):
    """
    获取错题关键词组合（Dify专用）

    获取用户错题的关键词组合，用于Dify工作流中的检索

    **实际服务地址**: http://43.142.157.145:8006/dify/interview/{user_id}/wrong-question-keywords
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8006/dify/interview/{user_id}/wrong-question-keywords")

# ==================== 面试记录服务接口 - 标准API ====================

@app.post("/interview/sessions", response_model=Dict[str, Any], tags=["面试记录服务-标准API"])
async def create_interview_session(
    user_id: str = Query(..., description="用户唯一标识符"),
    session_name: str = Query(None, description="面试会话名称"),
    difficulty_level: str = Query("medium", description="面试难度级别"),
    estimated_duration: int = Query(60, description="预计面试时长（分钟）", ge=10, le=300)
):
    """
    创建面试会话（标准API）

    创建新的面试会话，支持更多配置选项

    **实际服务地址**: http://43.142.157.145:8006/interview/sessions
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8006/interview/sessions")

@app.get("/interview/sessions/{user_id}", response_model=Dict[str, Any], tags=["面试记录服务-标准API"])
async def get_user_sessions(
    user_id: str = Path(..., description="用户唯一标识符"),
    status: str = Query(None, description="会话状态筛选"),
    limit: int = Query(10, description="返回数量限制", ge=1, le=50),
    offset: int = Query(0, description="偏移量", ge=0)
):
    """
    获取用户会话列表（标准API）

    获取指定用户的所有面试会话，支持分页和状态筛选

    **实际服务地址**: http://43.142.157.145:8006/interview/sessions/{user_id}
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8006/interview/sessions/{user_id}")

@app.get("/interview/sessions/{session_id}/detail", response_model=Dict[str, Any], tags=["面试记录服务-标准API"])
async def get_session_detail(
    session_id: str = Path(..., description="面试会话ID")
):
    """
    获取会话详情（标准API）

    获取指定面试会话的详细信息，包括所有题目和回答

    **实际服务地址**: http://43.142.157.145:8006/interview/sessions/{session_id}/detail
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8006/interview/sessions/{session_id}/detail")

@app.post("/interview/sessions/{session_id}/start", response_model=BaseResponse, tags=["面试记录服务-标准API"])
async def start_interview_session(
    session_id: str = Path(..., description="面试会话ID")
):
    """
    开始面试（标准API）

    将面试会话状态设置为进行中

    **实际服务地址**: http://43.142.157.145:8006/interview/sessions/{session_id}/start
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8006/interview/sessions/{session_id}/start")

@app.post("/interview/sessions/{session_id}/finish", response_model=Dict[str, Any], tags=["面试记录服务-标准API"])
async def finish_interview_session(
    session_id: str = Path(..., description="面试会话ID"),
    interviewer_notes: str = Query(None, description="面试官备注")
):
    """
    结束面试（标准API）

    完成面试并计算最终统计数据

    **实际服务地址**: http://43.142.157.145:8006/interview/sessions/{session_id}/finish
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8006/interview/sessions/{session_id}/finish")

@app.get("/interview/wrong-questions/{user_id}", response_model=WrongQuestionResponse, tags=["面试记录服务-标准API"])
async def get_wrong_questions_standard(
    user_id: str = Path(..., description="用户唯一标识符"),
    question_type: str = Query(None, description="题目类型筛选"),
    difficulty_level: str = Query(None, description="题目难度筛选"),
    limit: int = Query(10, description="返回数量限制", ge=1, le=50)
):
    """
    获取用户错题（标准版）

    标准API版本的错题查询接口

    **实际服务地址**: http://43.142.157.145:8006/interview/wrong-questions/{user_id}
    """
    raise HTTPException(status_code=501, detail="这是文档服务，请访问实际服务地址: http://43.142.157.145:8006/interview/wrong-questions/{user_id}")

# ==================== 服务健康检查接口 ====================

@app.get("/services/health/all", response_model=Dict[str, Any], tags=["系统监控"])
async def check_all_services():
    """
    检查所有服务健康状态

    检查所有4个微服务的健康状态
    """
    return {
        "success": True,
        "message": "这是文档服务，请分别访问各服务的健康检查接口",
        "services": {
            "pdf_parser": "http://43.142.157.145:8003/health",
            "analysis": "http://43.142.157.145:8004/health",
            "vector_storage": "http://43.142.157.145:8005/health",
            "interview": "http://43.142.157.145:8006/health"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
