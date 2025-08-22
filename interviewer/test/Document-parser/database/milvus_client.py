"""
Milvus向量数据库客户端
提供向量存储和检索功能
"""
from typing import List, Optional, Dict, Any
from langchain_core.documents import Document
from langchain_milvus import Milvus
from pymilvus import MilvusClient, DataType, Function, FunctionType
from pymilvus.client.types import IndexType, MetricType

from models.embeddings import embedding_manager
from utils.log_utils import log

try:
    from config import MILVUS_URI, MILVUS_TOKEN, COLLECTION_NAME
except ImportError:
    # 如果无法导入配置，使用默认值
    import os
    MILVUS_URI = os.getenv('MILVUS_URI', 'http://localhost:19530')
    MILVUS_TOKEN = os.getenv('MILVUS_TOKEN', '')
    COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'pdf_documents')

class MilvusVectorStore:
    """
    Milvus向量存储管理器
    提供文档存储、检索等功能
    """
    
    def __init__(self, 
                 collection_name: Optional[str] = None,
                 embedding_model_type: str = "bge"):
        """
        初始化Milvus向量存储
        
        Args:
            collection_name (str, optional): 集合名称，默认使用配置文件中的值
            embedding_model_type (str): 嵌入模型类型，'openai' 或 'bge'
        """
        self.collection_name = collection_name or COLLECTION_NAME
        self.embedding_model = embedding_manager.get_embedding_model(embedding_model_type)
        self.vector_store = None
        self.client = None
        
        log.info(f"初始化Milvus向量存储 - 集合: {self.collection_name}, 模型: {embedding_model_type}")
    
    def create_connection(self) -> bool:
        """
        创建Milvus连接
        
        Returns:
            bool: 连接是否成功
        """
        try:
            log.info(f"连接到Milvus服务器: {MILVUS_URI}")
            
            # 准备连接参数
            connection_args = {"uri": MILVUS_URI}
            if MILVUS_TOKEN:
                connection_args["token"] = MILVUS_TOKEN
            
            # 创建LangChain Milvus向量存储
            self.vector_store = Milvus(
                embedding_function=self.embedding_model,
                collection_name=self.collection_name,
                connection_args=connection_args,
                auto_id=True
                # 移除consistency_level设置，使用默认值以避免与已存在集合冲突
            )
            
            # 创建PyMilvus客户端（用于高级操作）
            self.client = MilvusClient(uri=MILVUS_URI, token=MILVUS_TOKEN)
            
            log.info("Milvus连接创建成功")
            return True
            
        except Exception as e:
            log.error(f"Milvus连接失败: {str(e)}")
            return False
    
    def create_collection_if_not_exists(self) -> bool:
        """
        如果集合不存在则创建集合

        Returns:
            bool: 操作是否成功
        """
        try:
            if not self.client:
                log.error("Milvus客户端未初始化")
                return False

            # 检查集合是否存在
            if self.client.has_collection(self.collection_name):
                log.info(f"集合 {self.collection_name} 已存在，删除后重新创建以避免配置冲突")
                # 删除已存在的集合以避免consistency_level冲突
                self.client.drop_collection(self.collection_name)
                log.info(f"已删除集合 {self.collection_name}")

            # 让LangChain自动创建集合，不手动创建
            log.info(f"集合 {self.collection_name} 将由LangChain自动创建")
            return True

        except Exception as e:
            log.error(f"准备集合失败: {str(e)}")
            return False
    
    def add_documents(self, documents: List[Document]) -> bool:
        """
        添加文档到向量存储
        
        Args:
            documents (List[Document]): 要添加的文档列表
            
        Returns:
            bool: 操作是否成功
        """
        try:
            if not self.vector_store:
                log.error("向量存储未初始化")
                return False
            
            log.info(f"开始添加 {len(documents)} 个文档到向量存储")
            
            # 使用LangChain Milvus添加文档
            self.vector_store.add_documents(documents)
            
            log.info("文档添加成功")
            return True
            
        except Exception as e:
            log.error(f"添加文档失败: {str(e)}")
            return False
    
    def similarity_search(self, 
                         query: str, 
                         k: int = 5,
                         filter_expr: Optional[str] = None) -> List[Document]:
        """
        相似性搜索
        
        Args:
            query (str): 查询文本
            k (int): 返回结果数量
            filter_expr (str, optional): 过滤表达式
            
        Returns:
            List[Document]: 搜索结果
        """
        try:
            if not self.vector_store:
                log.error("向量存储未初始化")
                return []
            
            log.info(f"执行相似性搜索: {query[:50]}...")
            
            # 执行搜索
            if filter_expr:
                results = self.vector_store.similarity_search(
                    query=query,
                    k=k,
                    expr=filter_expr
                )
            else:
                results = self.vector_store.similarity_search(
                    query=query,
                    k=k
                )
            
            log.info(f"搜索完成，返回 {len(results)} 个结果")
            return results
            
        except Exception as e:
            log.error(f"相似性搜索失败: {str(e)}")
            return []
    
    def similarity_search_with_score(self, 
                                   query: str, 
                                   k: int = 5,
                                   filter_expr: Optional[str] = None) -> List[tuple]:
        """
        带分数的相似性搜索
        
        Args:
            query (str): 查询文本
            k (int): 返回结果数量
            filter_expr (str, optional): 过滤表达式
            
        Returns:
            List[tuple]: (Document, score) 元组列表
        """
        try:
            if not self.vector_store:
                log.error("向量存储未初始化")
                return []
            
            log.info(f"执行带分数的相似性搜索: {query[:50]}...")
            
            # 执行搜索
            if filter_expr:
                results = self.vector_store.similarity_search_with_score(
                    query=query,
                    k=k,
                    expr=filter_expr
                )
            else:
                results = self.vector_store.similarity_search_with_score(
                    query=query,
                    k=k
                )
            
            log.info(f"搜索完成，返回 {len(results)} 个结果")
            return results
            
        except Exception as e:
            log.error(f"带分数的相似性搜索失败: {str(e)}")
            return []
    
    def get_collection_info(self) -> Dict[str, Any]:
        """
        获取集合信息
        
        Returns:
            Dict[str, Any]: 集合信息
        """
        try:
            if not self.client:
                return {"error": "客户端未初始化"}
            
            if not self.client.has_collection(self.collection_name):
                return {"error": "集合不存在"}
            
            # 获取集合统计信息
            stats = self.client.get_collection_stats(self.collection_name)
            
            # 获取集合描述
            desc = self.client.describe_collection(self.collection_name)
            
            return {
                "collection_name": self.collection_name,
                "stats": stats,
                "description": desc
            }
            
        except Exception as e:
            log.error(f"获取集合信息失败: {str(e)}")
            return {"error": str(e)}

if __name__ == '__main__':
    # 测试Milvus向量存储
    vector_store = MilvusVectorStore()
    
    # 测试连接
    if vector_store.create_connection():
        log.info("连接测试成功")
        
        # 测试创建集合
        if vector_store.create_collection_if_not_exists():
            log.info("集合创建测试成功")
            
            # 获取集合信息
            info = vector_store.get_collection_info()
            log.info(f"集合信息: {info}")
        else:
            log.error("集合创建测试失败")
    else:
        log.error("连接测试失败")
