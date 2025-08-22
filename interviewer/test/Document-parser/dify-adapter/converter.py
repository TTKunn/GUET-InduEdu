"""
Dify适配器格式转换器
处理Dify格式与内部API格式之间的转换
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from models import (
    DifyRetrievalRequest,
    DifyRetrievalResponse,
    DifyRetrievalRecord,
    InternalSearchParams,
    InternalSearchResponse,
    MetadataFilter,
    LogicalOperator,
    ConditionOperator
)
from config import DEFAULT_EMBEDDING_MODEL

logger = logging.getLogger(__name__)

# ==================== 请求转换器 ====================
class RequestConverter:
    """请求格式转换器"""
    
    @staticmethod
    def dify_to_internal(dify_request: DifyRetrievalRequest) -> InternalSearchParams:
        """
        将Dify请求格式转换为内部API格式
        
        Args:
            dify_request: Dify格式的检索请求
        
        Returns:
            InternalSearchParams: 内部API格式的搜索参数
        """
        logger.debug(f"Converting Dify request: knowledge_id={dify_request.knowledge_id}, query={dify_request.query[:50]}...")
        
        internal_params = InternalSearchParams(
            query=dify_request.query,
            collection_name=dify_request.knowledge_id,
            k=dify_request.retrieval_setting.top_k,
            embedding_model=DEFAULT_EMBEDDING_MODEL
        )
        
        logger.debug(f"Converted to internal params: collection={internal_params.collection_name}, k={internal_params.k}")
        return internal_params
    
    @staticmethod
    def build_metadata_filter(metadata_condition: Optional[MetadataFilter]) -> Optional[Dict[str, Any]]:
        """
        构建元数据过滤条件（如果你的内部API支持）
        
        Args:
            metadata_condition: Dify的元数据过滤条件
        
        Returns:
            Dict: 内部API格式的过滤条件
        """
        if not metadata_condition or not metadata_condition.conditions:
            return None
        
        # 这里可以根据你的内部API支持的过滤格式进行转换
        # 目前先返回原始格式，后续可以扩展
        filter_dict = {
            "logical_operator": metadata_condition.logical_operator.value,
            "conditions": []
        }
        
        for condition in metadata_condition.conditions:
            filter_dict["conditions"].append({
                "key": condition.key,
                "operator": condition.operator.value,
                "value": condition.value
            })
        
        logger.debug(f"Built metadata filter: {filter_dict}")
        return filter_dict

# ==================== 响应转换器 ====================
class ResponseConverter:
    """响应格式转换器"""
    
    @staticmethod
    def internal_to_dify(
        internal_response: Dict[str, Any], 
        score_threshold: float,
        metadata_filter: Optional[Dict[str, Any]] = None
    ) -> DifyRetrievalResponse:
        """
        将内部API响应转换为Dify格式
        
        Args:
            internal_response: 内部API的响应数据
            score_threshold: 相似度阈值
            metadata_filter: 元数据过滤条件
        
        Returns:
            DifyRetrievalResponse: Dify格式的响应
        """
        logger.debug(f"Converting internal response with {len(internal_response.get('results', []))} results")
        
        dify_records = []
        results = internal_response.get("results", [])
        
        for result in results:
            # 1. 检查相似度阈值
            similarity_score = result.get("similarity_score", 0.0)
            if similarity_score < score_threshold:
                logger.debug(f"Filtering out result with score {similarity_score} < {score_threshold}")
                continue
            
            # 2. 应用元数据过滤（如果需要）
            if metadata_filter and not ResponseConverter._matches_metadata_filter(result.get("metadata", {}), metadata_filter):
                logger.debug("Filtering out result due to metadata condition")
                continue
            
            # 3. 转换为Dify格式
            dify_record = ResponseConverter._convert_single_result(result)
            if dify_record:
                dify_records.append(dify_record)
        
        logger.info(f"Converted {len(dify_records)} records for Dify response")
        return DifyRetrievalResponse(records=dify_records)
    
    @staticmethod
    def _convert_single_result(result: Dict[str, Any]) -> Optional[DifyRetrievalRecord]:
        """
        转换单个搜索结果
        
        Args:
            result: 内部API的单个结果
        
        Returns:
            DifyRetrievalRecord: Dify格式的记录
        """
        try:
            metadata = result.get("metadata", {})
            
            # 提取标题（优先级：source_filename > file_name > source > 默认值）
            title = (
                metadata.get("source_filename") or 
                metadata.get("file_name") or 
                metadata.get("source") or 
                "Unknown Document"
            )
            
            # 确保content不为空
            content = result.get("content", "").strip()
            if not content:
                logger.warning("Skipping result with empty content")
                return None
            
            # 确保score在有效范围内
            score = max(0.0, min(1.0, result.get("similarity_score", 0.0)))
            
            # 清理和丰富元数据
            clean_metadata = ResponseConverter._clean_metadata(metadata)
            
            return DifyRetrievalRecord(
                content=content,
                score=score,
                title=title,
                metadata=clean_metadata
            )
            
        except Exception as e:
            logger.error(f"Error converting result: {e}")
            return None
    
    @staticmethod
    def _clean_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        清理和标准化元数据
        
        Args:
            metadata: 原始元数据
        
        Returns:
            Dict: 清理后的元数据
        """
        clean_meta = {}
        
        # 标准化字段名
        field_mapping = {
            "source": "source",
            "source_filename": "filename", 
            "file_name": "filename",
            "page": "page_number",
            "chunk_id": "chunk_index",
            "file_path": "file_path",
            "task_id": "task_id"
        }
        
        for old_key, new_key in field_mapping.items():
            if old_key in metadata:
                clean_meta[new_key] = metadata[old_key]
        
        # 添加处理时间戳
        clean_meta["processed_at"] = datetime.now().isoformat()
        
        return clean_meta
    
    @staticmethod
    def _matches_metadata_filter(metadata: Dict[str, Any], filter_condition: Dict[str, Any]) -> bool:
        """
        检查元数据是否匹配过滤条件
        
        Args:
            metadata: 文档元数据
            filter_condition: 过滤条件
        
        Returns:
            bool: 是否匹配
        """
        if not filter_condition or not filter_condition.get("conditions"):
            return True
        
        logical_op = filter_condition.get("logical_operator", "and")
        conditions = filter_condition.get("conditions", [])
        
        results = []
        for condition in conditions:
            key = condition.get("key")
            operator = condition.get("operator")
            value = condition.get("value")
            
            if key not in metadata:
                results.append(False)
                continue
            
            meta_value = metadata[key]
            match_result = ResponseConverter._evaluate_condition(meta_value, operator, value)
            results.append(match_result)
        
        # 应用逻辑操作符
        if logical_op == "and":
            return all(results)
        else:  # or
            return any(results)
    
    @staticmethod
    def _evaluate_condition(meta_value: Any, operator: str, condition_value: Any) -> bool:
        """评估单个条件"""
        try:
            if operator == "equals":
                return meta_value == condition_value
            elif operator == "not_equals":
                return meta_value != condition_value
            elif operator == "contains":
                return str(condition_value).lower() in str(meta_value).lower()
            elif operator == "not_contains":
                return str(condition_value).lower() not in str(meta_value).lower()
            elif operator == "in":
                return meta_value in condition_value
            elif operator == "not_in":
                return meta_value not in condition_value
            else:
                logger.warning(f"Unknown operator: {operator}")
                return True
        except Exception as e:
            logger.error(f"Error evaluating condition: {e}")
            return False

# ==================== 工具函数 ====================
def validate_conversion_result(dify_response: DifyRetrievalResponse) -> bool:
    """
    验证转换结果的有效性
    
    Args:
        dify_response: 转换后的Dify响应
    
    Returns:
        bool: 是否有效
    """
    try:
        # 检查基本结构
        if not isinstance(dify_response.records, list):
            return False
        
        # 检查每个记录的有效性
        for record in dify_response.records:
            if not record.content or not isinstance(record.score, (int, float)):
                return False
            if not 0.0 <= record.score <= 1.0:
                return False
        
        return True
    except Exception as e:
        logger.error(f"Error validating conversion result: {e}")
        return False
