"""
PDF解析服务API主模块
提供纯粹的PDF文档解析功能
"""

import os
import uuid
import time
import tempfile
import logging
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .models import (
    ParseResponse, TextParseResponse, HealthResponse,
    ErrorResponse, DocumentModel
)

# 修复相对导入问题
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers import PDFParser

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="PDF解析服务",
    description="专门用于PDF文档解析的微服务",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"全局异常: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="InternalServerError",
            message=f"服务内部错误: {str(exc)}"
        ).dict()
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查接口"""
    return HealthResponse(
        status="healthy",
        service="pdf-parser-service",
        version="1.0.0",
        timestamp=datetime.now().isoformat()
    )


@app.post("/parse", response_model=ParseResponse)
async def parse_pdf(
    file: UploadFile = File(...),
    chunk_size: int = Query(1000, description="文档分块大小", ge=100, le=5000),
    chunk_overlap: int = Query(200, description="分块重叠大小", ge=0, le=1000),
    split_text: bool = Query(True, description="是否进行文本分块"),
    return_content: bool = Query(False, description="是否返回解析内容")
):
    """
    解析PDF文件并返回结构化数据

    Args:
        file: 上传的PDF文件
        chunk_size: 文档分块大小
        chunk_overlap: 分块重叠大小
        split_text: 是否进行文本分块
        return_content: 是否在响应中返回解析内容

    Returns:
        ParseResponse: 解析结果
    """
    # 验证文件类型
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="只支持PDF文件")

    task_id = str(uuid.uuid4())
    start_time = time.time()

    logger.info(f"开始解析PDF文件: {file.filename}, 任务ID: {task_id}")

    try:
        # 保存上传的文件到临时目录
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        # 创建解析器实例
        parser = PDFParser(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

        # 解析PDF
        documents = parser.parse_pdf_to_documents(temp_file_path, split_text=split_text)

        # 获取文档信息
        doc_info = parser.get_document_info(documents)

        processing_time = time.time() - start_time

        # 准备响应数据
        response_data = {
            "success": True,
            "message": "PDF解析成功",
            "task_id": task_id,
            "total_documents": doc_info["total_docs"],
            "total_chars": doc_info["total_chars"],
            "avg_chars": doc_info["avg_chars"],
            "total_pages": doc_info.get("total_pages"),
            "processing_time": round(processing_time, 2)
        }

        # 如果需要返回内容
        if return_content:
            response_data["documents"] = [
                DocumentModel(
                    content=doc.page_content,
                    metadata=doc.metadata,
                    content_length=len(doc.page_content)
                )
                for doc in documents
            ]

        logger.info(f"PDF解析完成: {file.filename}, 耗时: {processing_time:.2f}秒")

        return ParseResponse(**response_data)

    except Exception as e:
        logger.error(f"PDF解析失败: {file.filename}, 错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PDF解析失败: {str(e)}")

    finally:
        # 清理临时文件
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


@app.post("/parse-text", response_model=TextParseResponse)
async def parse_pdf_to_text(
    file: UploadFile = File(...),
    chunk_size: int = Query(1000, description="文档分块大小", ge=100, le=5000),
    chunk_overlap: int = Query(200, description="分块重叠大小", ge=0, le=1000),
    split_text: bool = Query(True, description="是否进行文本分块")
):
    """
    解析PDF文件并返回纯文本内容

    Args:
        file: 上传的PDF文件
        chunk_size: 文档分块大小
        chunk_overlap: 分块重叠大小
        split_text: 是否进行文本分块

    Returns:
        TextParseResponse: 文本解析结果
    """
    # 验证文件类型
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="只支持PDF文件")

    task_id = str(uuid.uuid4())
    start_time = time.time()

    logger.info(f"开始解析PDF文件为文本: {file.filename}, 任务ID: {task_id}")

    try:
        # 保存上传的文件到临时目录
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        # 创建解析器实例
        parser = PDFParser(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

        # 解析PDF为文本
        text_content = parser.parse_pdf_to_text(temp_file_path, split_text=split_text)

        processing_time = time.time() - start_time

        logger.info(f"PDF文本解析完成: {file.filename}, 耗时: {processing_time:.2f}秒")

        return TextParseResponse(
            success=True,
            message="PDF文本解析成功",
            task_id=task_id,
            text_content=text_content,
            total_chars=len(text_content),
            processing_time=round(processing_time, 2)
        )

    except Exception as e:
        logger.error(f"PDF文本解析失败: {file.filename}, 错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PDF文本解析失败: {str(e)}")

    finally:
        # 清理临时文件
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


@app.post("/parse-and-store", response_model=ParseResponse)
async def parse_and_store_pdf(
    file: UploadFile = File(...),
    collection_name: str = Query("pdf_documents", description="Milvus集合名称"),
    chunk_size: int = Query(1000, description="文档分块大小", ge=100, le=5000),
    chunk_overlap: int = Query(200, description="分块重叠大小", ge=0, le=1000),
    embedding_model: str = Query("zhipuai", description="嵌入模型类型")
):
    """
    解析PDF文件并存储到向量数据库

    Args:
        file: 上传的PDF文件
        collection_name: Milvus集合名称
        chunk_size: 文档分块大小
        chunk_overlap: 分块重叠大小
        embedding_model: 嵌入模型类型

    Returns:
        ParseResponse: 解析和存储结果
    """
    # 验证文件类型
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="只支持PDF文件")

    task_id = str(uuid.uuid4())
    start_time = time.time()

    logger.info(f"开始解析并存储PDF文件: {file.filename}, 任务ID: {task_id}")

    try:
        # 保存上传的文件到临时目录
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        # 创建解析器实例
        parser = PDFParser(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

        # 解析PDF
        documents = parser.parse_pdf_to_documents(temp_file_path, split_text=True)

        # 添加文件信息到元数据
        for doc in documents:
            doc.metadata['source_filename'] = file.filename
            doc.metadata['task_id'] = task_id

        # 调用vector-storage-service存储
        import httpx
        async with httpx.AsyncClient() as client:
            store_data = {
                "texts": [doc.page_content for doc in documents],
                "metadatas": [doc.metadata for doc in documents],
                "collection_name": collection_name,
                "embedding_model": embedding_model
            }

            response = await client.post(
                "http://localhost:8005/store",
                json=store_data,
                timeout=120
            )

            if response.status_code != 200:
                raise Exception(f"向量存储失败: {response.text}")

        # 获取文档信息
        doc_info = parser.get_document_info(documents)
        processing_time = time.time() - start_time

        logger.info(f"PDF解析并存储完成: {file.filename}, 耗时: {processing_time:.2f}秒")

        return ParseResponse(
            success=True,
            message="PDF解析并存储成功",
            task_id=task_id,
            total_documents=doc_info["total_docs"],
            total_chars=doc_info["total_chars"],
            avg_chars=doc_info["avg_chars"],
            total_pages=doc_info.get("total_pages"),
            processing_time=round(processing_time, 2),
            documents=None  # 不返回文档内容以节省带宽
        )

    except Exception as e:
        logger.error(f"PDF解析并存储失败: {file.filename}, 错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PDF解析并存储失败: {str(e)}")

    finally:
        # 清理临时文件
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


@app.get("/search")
async def search_documents(
    query: str = Query(..., description="搜索查询"),
    collection_name: str = Query("pdf_documents", description="Milvus集合名称"),
    k: int = Query(5, description="返回结果数量"),
    embedding_model: str = Query("zhipuai", description="嵌入模型类型")
):
    """
    在向量数据库中搜索文档

    Args:
        query: 搜索查询
        collection_name: Milvus集合名称
        k: 返回结果数量
        embedding_model: 嵌入模型类型

    Returns:
        搜索结果
    """
    logger.info(f"开始搜索文档: {query}")

    try:
        # 调用vector-storage-service搜索
        import httpx
        async with httpx.AsyncClient() as client:
            search_data = {
                "query": query,
                "collection_name": collection_name,
                "k": k,
                "embedding_model": embedding_model,
                "with_score": True
            }

            response = await client.post(
                "http://43.142.157.145:8005/search",
                json=search_data,
                timeout=60
            )

            if response.status_code != 200:
                raise Exception(f"向量搜索失败: {response.text}")

            search_result = response.json()

            # 格式化结果以匹配原项目格式
            formatted_results = []
            for result in search_result.get("results", []):
                formatted_results.append({
                    "content": result["content"],
                    "metadata": result["metadata"],
                    "score": result.get("score", 0.0)
                })

            return {
                "success": True,
                "query": query,
                "results": formatted_results,
                "total_results": len(formatted_results),
                "collection_name": collection_name,
                "processing_time": search_result.get("processing_time", 0.0)
            }

    except Exception as e:
        logger.error(f"文档搜索失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"文档搜索失败: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)