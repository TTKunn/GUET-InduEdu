"""
向量存储服务API主模块
提供向量存储和检索功能
"""

import time
import logging
from datetime import datetime
from typing import Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from langchain_core.documents import Document

# 修复相对导入问题
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.models import (
    StoreRequest, StoreDocumentsRequest, SearchRequest,
    StoreResponse, SearchResponse, CollectionStatsResponse,
    HealthResponse, ErrorResponse, SearchResult
)
from database import MilvusVectorStore

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="向量存储服务",
    description="专门用于向量存储和检索的微服务",
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

# 全局向量存储实例缓存
vector_stores: Dict[str, MilvusVectorStore] = {}

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


def get_vector_store(collection_name: str, embedding_model: str) -> MilvusVectorStore:
    """
    获取或创建向量存储实例

    Args:
        collection_name: 集合名称
        embedding_model: 嵌入模型类型

    Returns:
        MilvusVectorStore: 向量存储实例
    """
    store_key = f"{collection_name}_{embedding_model}"

    if store_key not in vector_stores:
        logger.info(f"创建新的向量存储实例: {store_key}")
        vector_store = MilvusVectorStore(
            collection_name=collection_name,
            embedding_model_type=embedding_model
        )

        # 创建连接
        if not vector_store.create_connection():
            raise HTTPException(status_code=500, detail="无法连接到Milvus数据库")

        # 确保集合存在
        if not vector_store.create_collection_if_not_exists():
            raise HTTPException(status_code=500, detail="无法创建或访问集合")

        vector_stores[store_key] = vector_store

    return vector_stores[store_key]


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查接口"""
    # 测试Milvus连接
    milvus_connected = False
    try:
        test_store = MilvusVectorStore("health_check", "zhipuai")
        milvus_connected = test_store.create_connection()
    except Exception as e:
        logger.warning(f"健康检查时Milvus连接失败: {str(e)}")

    return HealthResponse(
        status="healthy" if milvus_connected else "degraded",
        service="vector-storage-service",
        version="1.0.0",
        timestamp=datetime.now().isoformat(),
        milvus_connected=milvus_connected
    )


@app.post("/store", response_model=StoreResponse)
async def store_texts(request: StoreRequest):
    """
    存储文本到向量数据库

    Args:
        request: 存储请求

    Returns:
        StoreResponse: 存储结果
    """
    start_time = time.time()

    logger.info(f"开始存储文本到集合: {request.collection_name}, 数量: {len(request.texts)}")

    try:
        # 获取向量存储实例
        vector_store = get_vector_store(request.collection_name, request.embedding_model)

        # 存储文本
        success = vector_store.add_texts(request.texts, request.metadatas)

        if not success:
            raise HTTPException(status_code=500, detail="文本存储失败")

        processing_time = time.time() - start_time

        logger.info(f"文本存储完成: {request.collection_name}, 耗时: {processing_time:.2f}秒")

        return StoreResponse(
            success=True,
            message="文本存储成功",
            collection_name=request.collection_name,
            stored_count=len(request.texts),
            processing_time=round(processing_time, 2)
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"存储文本失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"存储文本失败: {str(e)}")


@app.post("/store-documents", response_model=StoreResponse)
async def store_documents(request: StoreDocumentsRequest):
    """
    存储文档到向量数据库

    Args:
        request: 存储文档请求

    Returns:
        StoreResponse: 存储结果
    """
    start_time = time.time()

    logger.info(f"开始存储文档到集合: {request.collection_name}, 数量: {len(request.documents)}")

    try:
        # 获取向量存储实例
        vector_store = get_vector_store(request.collection_name, request.embedding_model)

        # 转换为Document对象
        documents = [
            Document(page_content=doc.content, metadata=doc.metadata)
            for doc in request.documents
        ]

        # 存储文档
        success = vector_store.add_documents(documents)

        if not success:
            raise HTTPException(status_code=500, detail="文档存储失败")

        processing_time = time.time() - start_time

        logger.info(f"文档存储完成: {request.collection_name}, 耗时: {processing_time:.2f}秒")

        return StoreResponse(
            success=True,
            message="文档存储成功",
            collection_name=request.collection_name,
            stored_count=len(request.documents),
            processing_time=round(processing_time, 2)
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"存储文档失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"存储文档失败: {str(e)}")


@app.post("/search", response_model=SearchResponse)
async def search_vectors(request: SearchRequest):
    """
    向量相似性搜索

    Args:
        request: 搜索请求

    Returns:
        SearchResponse: 搜索结果
    """
    start_time = time.time()

    logger.info(f"开始向量搜索: 集合={request.collection_name}, 查询={request.query[:50]}...")

    try:
        # 获取向量存储实例
        vector_store = get_vector_store(request.collection_name, request.embedding_model)

        # 执行搜索
        if request.with_score:
            # 带分数的搜索
            results_with_score = vector_store.similarity_search_with_score(
                query=request.query,
                k=request.k,
                filter_expr=request.filter_expr
            )

            # 转换结果格式
            search_results = [
                SearchResult(
                    content=doc.page_content,
                    metadata=doc.metadata,
                    score=score
                )
                for doc, score in results_with_score
            ]
        else:
            # 普通搜索
            results = vector_store.similarity_search(
                query=request.query,
                k=request.k,
                filter_expr=request.filter_expr
            )

            # 转换结果格式
            search_results = [
                SearchResult(
                    content=doc.page_content,
                    metadata=doc.metadata
                )
                for doc in results
            ]

        processing_time = time.time() - start_time

        logger.info(f"向量搜索完成: 集合={request.collection_name}, 结果数={len(search_results)}, 耗时={processing_time:.2f}秒")

        return SearchResponse(
            success=True,
            message="搜索完成",
            collection_name=request.collection_name,
            query=request.query,
            results=search_results,
            total_results=len(search_results),
            processing_time=round(processing_time, 2)
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"向量搜索失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"向量搜索失败: {str(e)}")


@app.get("/collections/{collection_name}/stats", response_model=CollectionStatsResponse)
async def get_collection_stats(collection_name: str, embedding_model: str = "zhipuai"):
    """
    获取集合统计信息

    Args:
        collection_name: 集合名称
        embedding_model: 嵌入模型类型

    Returns:
        CollectionStatsResponse: 集合统计信息
    """
    logger.info(f"获取集合统计信息: {collection_name}")

    try:
        # 获取向量存储实例
        vector_store = get_vector_store(collection_name, embedding_model)

        # 获取统计信息
        stats = vector_store.get_collection_stats()

        return CollectionStatsResponse(
            success=True,
            collection_name=collection_name,
            exists=stats.get("exists", False),
            row_count=stats.get("row_count"),
            embedding_model=stats.get("embedding_model")
        )

    except Exception as e:
        logger.error(f"获取集合统计信息失败: {str(e)}")
        return CollectionStatsResponse(
            success=False,
            collection_name=collection_name,
            exists=False
        )


@app.delete("/collections/{collection_name}")
async def delete_collection(collection_name: str, embedding_model: str = "zhipuai"):
    """
    删除集合

    Args:
        collection_name: 集合名称
        embedding_model: 嵌入模型类型

    Returns:
        dict: 删除结果
    """
    logger.info(f"删除集合: {collection_name}")

    try:
        # 获取向量存储实例
        vector_store = get_vector_store(collection_name, embedding_model)

        # 删除集合
        success = vector_store.delete_collection()

        if success:
            # 从缓存中移除
            store_key = f"{collection_name}_{embedding_model}"
            if store_key in vector_stores:
                del vector_stores[store_key]

            return {"success": True, "message": f"集合 {collection_name} 已删除"}
        else:
            raise HTTPException(status_code=500, detail="删除集合失败")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除集合失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"删除集合失败: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)