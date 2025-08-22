"""
Dify外部知识库适配器主服务
提供符合Dify外部知识库API规范的接口
"""

import time
import logging
import requests
from datetime import datetime
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from models import (
    DifyRetrievalRequest,
    DifyRetrievalResponse,
    DifyErrorResponse,
    HealthCheckResponse,
    AdapterStats,
    InternalSearchParams
)
from auth import authenticate_request, authorize_collection_access, auth_stats
from converter import RequestConverter, ResponseConverter
from config import (
    ADAPTER_HOST,
    ADAPTER_PORT,
    PDF_PARSER_API_URL,
    ERROR_CODES,
    LOG_LEVEL,
    LOG_FORMAT,
    API_KEY_MAPPING
)

# ==================== 日志配置 ====================
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# ==================== FastAPI应用初始化 ====================
app = FastAPI(
    title="Dify External Knowledge Adapter",
    description="适配器服务，将PDF解析系统集成到Dify工作流平台",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该限制具体域名
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# 添加请求日志中间件
@app.middleware("http")
async def log_requests(request, call_next):
    """记录所有请求的详细信息"""
    client_ip = request.client.host
    method = request.method
    url = str(request.url)
    headers = dict(request.headers)

    logger.info(f"🌐 Incoming request: {method} {url} from {client_ip}")
    logger.info(f"📋 Headers: {headers}")

    response = await call_next(request)

    logger.info(f"📤 Response status: {response.status_code}")
    return response

# ==================== 全局变量 ====================
# 统计信息
adapter_stats = {
    "start_time": datetime.now(),
    "total_requests": 0,
    "successful_requests": 0,
    "failed_requests": 0,
    "total_response_time": 0.0
}

# ==================== 核心API端点 ====================
@app.post("/retrieval", response_model=DifyRetrievalResponse)
async def dify_external_knowledge_retrieval(
    request: DifyRetrievalRequest,
    api_key: str = Depends(authenticate_request)
):
    """
    Dify外部知识库检索接口
    符合Dify外部知识库API规范
    
    Args:
        request: Dify检索请求
        api_key: 通过认证的API Key
    
    Returns:
        DifyRetrievalResponse: 符合Dify规范的检索结果
    """
    start_time = time.time()
    adapter_stats["total_requests"] += 1
    
    try:
        logger.info(f"Processing Dify retrieval request: knowledge_id={request.knowledge_id}, query={request.query[:50]}...")
        
        # 1. 检查Collection访问权限
        authorize_collection_access(api_key, request.knowledge_id)
        
        # 2. 转换请求格式
        internal_params = RequestConverter.dify_to_internal(request)
        
        # 3. 调用内部搜索API
        search_response = await call_internal_search_api(internal_params)
        
        # 4. 转换响应格式
        dify_response = ResponseConverter.internal_to_dify(
            search_response,
            request.retrieval_setting.score_threshold,
            RequestConverter.build_metadata_filter(request.metadata_condition)
        )
        
        # 5. 记录成功统计
        response_time = time.time() - start_time
        adapter_stats["successful_requests"] += 1
        adapter_stats["total_response_time"] += response_time
        auth_stats.record_request(api_key, True)
        
        logger.info(f"Retrieval successful: returned {len(dify_response.records)} records in {response_time:.3f}s")
        return dify_response
        
    except HTTPException:
        # 重新抛出HTTP异常
        adapter_stats["failed_requests"] += 1
        auth_stats.record_request(api_key, False)
        raise
    except Exception as e:
        # 处理其他异常
        adapter_stats["failed_requests"] += 1
        auth_stats.record_request(api_key, False)
        logger.error(f"Unexpected error in retrieval: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=DifyErrorResponse(
                error_code=500,
                error_msg=f"{ERROR_CODES[500]}: {str(e)}"
            ).dict()
        )

# ==================== 辅助API端点 ====================
@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """健康检查端点"""
    try:
        # 检查内部API连接
        health_response = requests.get(f"{PDF_PARSER_API_URL}/health", timeout=5)
        pdf_api_status = "healthy" if health_response.status_code == 200 else "unhealthy"
    except Exception:
        pdf_api_status = "unreachable"
    
    return HealthCheckResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now().isoformat(),
        dependencies={
            "pdf_parser_api": pdf_api_status,
            "adapter_service": "healthy"
        }
    )

@app.get("/stats", response_model=AdapterStats)
async def get_adapter_stats():
    """获取适配器统计信息"""
    uptime = datetime.now() - adapter_stats["start_time"]
    avg_response_time = (
        adapter_stats["total_response_time"] / max(1, adapter_stats["successful_requests"])
    )
    
    return AdapterStats(
        total_requests=adapter_stats["total_requests"],
        successful_requests=adapter_stats["successful_requests"],
        failed_requests=adapter_stats["failed_requests"],
        average_response_time=avg_response_time,
        active_collections=list(set(config["collection"] for config in API_KEY_MAPPING.values()))
    )

# ==================== 内部API调用函数 ====================
async def call_internal_search_api(params: InternalSearchParams) -> Dict[str, Any]:
    """
    调用内部PDF解析API的搜索接口
    
    Args:
        params: 内部API搜索参数
    
    Returns:
        Dict: 内部API的响应数据
    
    Raises:
        HTTPException: 当内部API调用失败时
    """
    try:
        logger.debug(f"Calling internal search API: {PDF_PARSER_API_URL}/search")
        
        # 构建请求参数
        search_params = {
            "query": params.query,
            "collection_name": params.collection_name,
            "k": params.k,
            "embedding_model": params.embedding_model
        }
        
        # 调用内部API
        response = requests.get(
            f"{PDF_PARSER_API_URL}/search",
            params=search_params,
            timeout=30  # 30秒超时
        )
        
        # 检查响应状态
        if response.status_code == 404:
            logger.error(f"Collection not found: {params.collection_name}")
            raise HTTPException(
                status_code=404,
                detail=DifyErrorResponse(
                    error_code=2001,
                    error_msg=ERROR_CODES[2001]
                ).dict()
            )
        elif response.status_code != 200:
            logger.error(f"Internal API error: {response.status_code} - {response.text}")
            raise HTTPException(
                status_code=500,
                detail=DifyErrorResponse(
                    error_code=500,
                    error_msg=f"Internal search API error: {response.status_code}"
                ).dict()
            )
        
        # 解析响应
        search_data = response.json()
        logger.debug(f"Internal API returned {len(search_data.get('results', []))} results")
        
        return search_data
        
    except requests.exceptions.Timeout:
        logger.error("Internal API timeout")
        raise HTTPException(
            status_code=504,
            detail=DifyErrorResponse(
                error_code=504,
                error_msg="Search request timeout"
            ).dict()
        )
    except requests.exceptions.ConnectionError:
        logger.error(f"Cannot connect to internal API: {PDF_PARSER_API_URL}")
        raise HTTPException(
            status_code=503,
            detail=DifyErrorResponse(
                error_code=503,
                error_msg="Internal search service unavailable"
            ).dict()
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"Internal API request error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=DifyErrorResponse(
                error_code=500,
                error_msg=f"Internal API request failed: {str(e)}"
            ).dict()
        )

# ==================== 错误处理 ====================
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """统一的HTTP异常处理器"""
    logger.warning(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """通用异常处理器"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=DifyErrorResponse(
            error_code=500,
            error_msg=ERROR_CODES[500]
        ).dict()
    )

# ==================== 启动配置 ====================
if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting Dify Adapter Service on {ADAPTER_HOST}:{ADAPTER_PORT}")
    logger.info(f"PDF Parser API URL: {PDF_PARSER_API_URL}")
    
    uvicorn.run(
        "main:app",
        host=ADAPTER_HOST,
        port=ADAPTER_PORT,
        reload=True,  # 开发模式，生产环境设为False
        log_level=LOG_LEVEL.lower()
    )
