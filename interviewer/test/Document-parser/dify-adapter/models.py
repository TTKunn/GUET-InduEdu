"""
Dify适配器数据模型
定义符合Dify外部知识库API规范的请求和响应模型
"""

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional, Union
from enum import Enum

# ==================== 枚举类型 ====================
class LogicalOperator(str, Enum):
    """逻辑操作符枚举"""
    AND = "and"
    OR = "or"

class ConditionOperator(str, Enum):
    """条件操作符枚举"""
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    IN = "in"
    NOT_IN = "not_in"

# ==================== 请求模型 ====================
class MetadataCondition(BaseModel):
    """元数据条件模型"""
    key: str = Field(..., description="元数据字段名")
    operator: ConditionOperator = Field(..., description="条件操作符")
    value: Union[str, int, float, List[Any]] = Field(..., description="条件值")

class MetadataFilter(BaseModel):
    """元数据过滤器模型"""
    logical_operator: LogicalOperator = Field(LogicalOperator.AND, description="逻辑操作符")
    conditions: List[MetadataCondition] = Field([], description="过滤条件列表")

class RetrievalSetting(BaseModel):
    """检索设置模型"""
    top_k: int = Field(5, ge=1, le=20, description="返回结果数量")
    score_threshold: float = Field(0.5, ge=0.0, le=1.0, description="相似度阈值")
    
    @validator('top_k')
    def validate_top_k(cls, v):
        if not 1 <= v <= 20:
            raise ValueError('top_k must be between 1 and 20')
        return v
    
    @validator('score_threshold')
    def validate_score_threshold(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('score_threshold must be between 0.0 and 1.0')
        return v

class DifyRetrievalRequest(BaseModel):
    """Dify外部知识库检索请求模型"""
    knowledge_id: str = Field(..., description="知识库ID（对应Collection名称）")
    query: str = Field(..., min_length=1, description="搜索查询内容")
    retrieval_setting: RetrievalSetting = Field(..., description="检索设置")
    metadata_condition: Optional[MetadataFilter] = Field(None, description="元数据过滤条件")
    
    @validator('knowledge_id')
    def validate_knowledge_id(cls, v):
        if not v or not v.strip():
            raise ValueError('knowledge_id cannot be empty')
        return v.strip()
    
    @validator('query')
    def validate_query(cls, v):
        if not v or not v.strip():
            raise ValueError('query cannot be empty')
        return v.strip()

# ==================== 响应模型 ====================
class DifyRetrievalRecord(BaseModel):
    """Dify检索结果记录模型"""
    content: str = Field(..., description="文档内容")
    score: float = Field(..., ge=0.0, le=1.0, description="相似度分数")
    title: str = Field(..., description="文档标题")
    metadata: Optional[Dict[str, Any]] = Field(None, description="文档元数据")
    
    @validator('score')
    def validate_score(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('score must be between 0.0 and 1.0')
        return v

class DifyRetrievalResponse(BaseModel):
    """Dify外部知识库检索响应模型"""
    records: List[DifyRetrievalRecord] = Field(..., description="检索结果记录列表")

# ==================== 错误响应模型 ====================
class DifyErrorResponse(BaseModel):
    """Dify错误响应模型"""
    error_code: int = Field(..., description="错误码")
    error_msg: str = Field(..., description="错误信息")

# ==================== 内部API模型 ====================
class InternalSearchParams(BaseModel):
    """内部搜索API参数模型"""
    query: str
    collection_name: str
    k: int = 5
    embedding_model: str = "zhipuai"

class InternalSearchResult(BaseModel):
    """内部搜索API结果模型"""
    content: str
    similarity_score: float
    metadata: Dict[str, Any]

class InternalSearchResponse(BaseModel):
    """内部搜索API响应模型"""
    results: List[InternalSearchResult]
    total_count: int
    query_time: float

# ==================== 健康检查模型 ====================
class HealthCheckResponse(BaseModel):
    """健康检查响应模型"""
    status: str = Field("healthy", description="服务状态")
    version: str = Field("1.0.0", description="服务版本")
    timestamp: str = Field(..., description="检查时间戳")
    dependencies: Dict[str, str] = Field(..., description="依赖服务状态")

# ==================== 统计信息模型 ====================
class AdapterStats(BaseModel):
    """适配器统计信息模型"""
    total_requests: int = Field(0, description="总请求数")
    successful_requests: int = Field(0, description="成功请求数")
    failed_requests: int = Field(0, description="失败请求数")
    average_response_time: float = Field(0.0, description="平均响应时间（秒）")
    active_collections: List[str] = Field([], description="活跃的Collection列表")
