"""
PDF解析服务API模型定义
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class DocumentModel(BaseModel):
    """文档模型"""
    content: str = Field(..., description="文档内容")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="文档元数据")
    content_length: int = Field(..., description="内容长度")


class ParseRequest(BaseModel):
    """解析请求模型"""
    chunk_size: int = Field(default=1000, description="文档分块大小", ge=100, le=5000)
    chunk_overlap: int = Field(default=200, description="分块重叠大小", ge=0, le=1000)
    split_text: bool = Field(default=True, description="是否进行文本分块")
    return_content: bool = Field(default=False, description="是否返回解析内容")


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


class HealthResponse(BaseModel):
    """健康检查响应模型"""
    status: str = Field(..., description="服务状态")
    service: str = Field(..., description="服务名称")
    version: str = Field(..., description="服务版本")
    timestamp: str = Field(..., description="检查时间")


class ErrorResponse(BaseModel):
    """错误响应模型"""
    success: bool = Field(default=False, description="是否成功")
    error: str = Field(..., description="错误类型")
    message: str = Field(..., description="错误消息")
    task_id: Optional[str] = Field(None, description="任务ID")