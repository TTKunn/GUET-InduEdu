"""
PDF解析API服务
提供PDF文档解析的REST API接口
"""
import os
import uuid
import tempfile
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from parsers.pdf_parser import PDFParser
from database.milvus_client import MilvusVectorStore
from utils.log_utils import log

# 创建FastAPI应用
app = FastAPI(
    title="PDF解析API",
    description="提供PDF文档解析和向量存储服务",
    version="1.0.0"
)

# 全局解析器实例
pdf_parser = PDFParser()

# 响应模型
class ParseResponse(BaseModel):
    """PDF解析响应模型"""
    success: bool
    message: str
    task_id: str
    total_documents: int
    total_chars: int
    documents: Optional[List[Dict[str, Any]]] = None

class SearchResponse(BaseModel):
    """搜索响应模型"""
    success: bool
    message: str
    total_results: int
    results: List[Dict[str, Any]]

class HealthResponse(BaseModel):
    """健康检查响应模型"""
    status: str
    version: str
    message: str

@app.get("/", response_model=HealthResponse)
async def root():
    """根路径 - 健康检查"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        message="PDF解析API服务运行正常"
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查接口"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        message="服务运行正常"
    )

@app.post("/parse", response_model=ParseResponse)
async def parse_pdf(
    file: UploadFile = File(...),
    chunk_size: int = Query(1000, description="文档分块大小"),
    chunk_overlap: int = Query(200, description="分块重叠大小"),
    split_text: bool = Query(True, description="是否进行文本分块"),
    return_content: bool = Query(False, description="是否返回解析内容")
):
    """
    解析PDF文件
    
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
    log.info(f"开始解析PDF文件: {file.filename}, 任务ID: {task_id}")
    
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
        
        # 准备响应数据
        response_data = {
            "success": True,
            "message": "PDF解析成功",
            "task_id": task_id,
            "total_documents": doc_info["total_docs"],
            "total_chars": doc_info["total_chars"]
        }
        
        # 如果需要返回内容
        if return_content:
            response_data["documents"] = [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "content_length": len(doc.page_content)
                }
                for doc in documents
            ]
        
        log.info(f"PDF解析完成: {file.filename}, 文档数: {doc_info['total_docs']}")
        
        # 清理临时文件
        os.unlink(temp_file_path)
        
        return ParseResponse(**response_data)
        
    except Exception as e:
        log.error(f"PDF解析失败: {file.filename}, 错误: {str(e)}")
        
        # 清理临时文件
        if 'temp_file_path' in locals():
            try:
                os.unlink(temp_file_path)
            except:
                pass
        
        raise HTTPException(status_code=500, detail=f"PDF解析失败: {str(e)}")

@app.post("/parse-and-store", response_model=ParseResponse)
async def parse_and_store_pdf(
    file: UploadFile = File(...),
    collection_name: str = Query("pdf_documents", description="Milvus集合名称"),
    chunk_size: int = Query(1000, description="文档分块大小"),
    chunk_overlap: int = Query(200, description="分块重叠大小"),
    embedding_model: str = Query("zhipuai", description="嵌入模型类型")
):
    """
    解析PDF文件并存储到Milvus向量数据库
    
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
    log.info(f"开始解析并存储PDF文件: {file.filename}, 任务ID: {task_id}")
    
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
        
        # 创建向量存储
        vector_store = MilvusVectorStore(
            collection_name=collection_name,
            embedding_model_type=embedding_model
        )
        
        # 连接数据库
        if not vector_store.create_connection():
            raise Exception("无法连接到Milvus数据库")
        
        # 创建集合（如果不存在）
        if not vector_store.create_collection_if_not_exists():
            raise Exception("无法创建Milvus集合")
        
        # 存储文档
        if not vector_store.add_documents(documents):
            raise Exception("文档存储到Milvus失败")
        
        # 获取文档信息
        doc_info = parser.get_document_info(documents)
        
        log.info(f"PDF解析并存储完成: {file.filename}, 文档数: {doc_info['total_docs']}")
        
        # 清理临时文件
        os.unlink(temp_file_path)
        
        return ParseResponse(
            success=True,
            message="PDF解析并存储成功",
            task_id=task_id,
            total_documents=doc_info["total_docs"],
            total_chars=doc_info["total_chars"]
        )
        
    except Exception as e:
        log.error(f"PDF解析并存储失败: {file.filename}, 错误: {str(e)}")
        
        # 清理临时文件
        if 'temp_file_path' in locals():
            try:
                os.unlink(temp_file_path)
            except:
                pass
        
        raise HTTPException(status_code=500, detail=f"PDF解析并存储失败: {str(e)}")

@app.get("/search", response_model=SearchResponse)
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
        SearchResponse: 搜索结果
    """
    log.info(f"开始搜索文档: {query}")
    
    try:
        # 创建向量存储
        vector_store = MilvusVectorStore(
            collection_name=collection_name,
            embedding_model_type=embedding_model
        )
        
        # 连接数据库
        if not vector_store.create_connection():
            raise Exception("无法连接到Milvus数据库")
        
        # 执行搜索
        results = vector_store.similarity_search_with_score(query=query, k=k)
        
        # 格式化结果
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "similarity_score": float(score),
                "content_length": len(doc.page_content)
            })
        
        log.info(f"搜索完成: {query}, 结果数: {len(results)}")
        
        return SearchResponse(
            success=True,
            message="搜索完成",
            total_results=len(results),
            results=formatted_results
        )
        
    except Exception as e:
        log.error(f"搜索失败: {query}, 错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
