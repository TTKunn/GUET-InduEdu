"""
向量存储服务API模型定义
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class DocumentModel(BaseModel):
    """文档模型"""
    content: str = Field(..., description="文档内容")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="文档元数据")


class StoreRequest(BaseModel):
    """存储请求模型"""
    texts: List[str] = Field(..., description="要存储的文本列表")
    metadatas: Optional[List[Dict[str, Any]]] = Field(None, description="元数据列表")
    collection_name: str = Field(..., description="集合名称")
    embedding_model: str = Field(default="zhipuai", description="嵌入模型类型")


class StoreDocumentsRequest(BaseModel):
    """存储文档请求模型"""
    documents: List[DocumentModel] = Field(..., description="要存储的文档列表")
    collection_name: str = Field(..., description="集合名称")
    embedding_model: str = Field(default="zhipuai", description="嵌入模型类型")


class SearchRequest(BaseModel):
    """搜索请求模型"""
    query: str = Field(..., description="查询文本")
    collection_name: str = Field(..., description="集合名称")
    k: int = Field(default=5, description="返回结果数量", ge=1, le=100)
    embedding_model: str = Field(default="zhipuai", description="嵌入模型类型")
    filter_expr: Optional[str] = Field(None, description="过滤表达式")
    with_score: bool = Field(default=False, description="是否返回相似度分数")


class SearchResult(BaseModel):
    """搜索结果模型"""
    content: str = Field(..., description="文档内容")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="文档元数据")
    score: Optional[float] = Field(None, description="相似度分数")


class StoreResponse(BaseModel):
    """存储响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    collection_name: str = Field(..., description="集合名称")
    stored_count: int = Field(..., description="存储的文档数量")
    processing_time: float = Field(..., description="处理时间(秒)")


class SearchResponse(BaseModel):
    """搜索响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    collection_name: str = Field(..., description="集合名称")
    query: str = Field(..., description="查询文本")
    results: List[SearchResult] = Field(..., description="搜索结果")
    total_results: int = Field(..., description="结果总数")
    processing_time: float = Field(..., description="处理时间(秒)")


class CollectionStatsResponse(BaseModel):
    """集合统计响应模型"""
    success: bool = Field(..., description="是否成功")
    collection_name: str = Field(..., description="集合名称")
    exists: bool = Field(..., description="集合是否存在")
    row_count: Optional[int] = Field(None, description="文档数量")
    embedding_model: Optional[str] = Field(None, description="嵌入模型类型")


class HealthResponse(BaseModel):
    """健康检查响应模型"""
    status: str = Field(..., description="服务状态")
    service: str = Field(..., description="服务名称")
    version: str = Field(..., description="服务版本")
    timestamp: str = Field(..., description="检查时间")
    milvus_connected: bool = Field(..., description="Milvus连接状态")


class ErrorResponse(BaseModel):
    """错误响应模型"""
    success: bool = Field(default=False, description="是否成功")
    error: str = Field(..., description="错误类型")
    message: str = Field(..., description="错误消息")
    collection_name: Optional[str] = Field(None, description="集合名称")