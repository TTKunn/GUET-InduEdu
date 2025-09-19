"""
Milvus向量数据库客户端 - 独立服务版本
提供向量存储和检索功能
"""

import os
import logging
from typing import List, Optional, Dict, Any, Tuple
from langchain_core.documents import Document
from langchain_milvus import Milvus
from pymilvus import MilvusClient

# 修复相对导入问题
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from embeddings import embedding_service

logger = logging.getLogger(__name__)


class MilvusVectorStore:
    """
    Milvus向量存储管理器 - 独立服务版本
    提供文档存储、检索等功能
    """

    def __init__(self,
                 collection_name: str = "default_collection",
                 embedding_model_type: str = "zhipuai"):
        """
        初始化Milvus向量存储

        Args:
            collection_name: 集合名称
            embedding_model_type: 嵌入模型类型，'zhipuai' 或 'bge'
        """
        self.collection_name = collection_name
        self.embedding_model_type = embedding_model_type
        self.embedding_model = embedding_service.get_embedding_model(embedding_model_type)
        self.vector_store = None
        self.client = None

        # 从环境变量获取Milvus配置
        self.milvus_uri = os.getenv('MILVUS_URI', 'http://localhost:19530')
        self.milvus_token = os.getenv('MILVUS_TOKEN', '')

        logger.info(f"初始化Milvus向量存储 - 集合: {collection_name}, 模型: {embedding_model_type}")

    def create_connection(self) -> bool:
        """
        创建Milvus连接

        Returns:
            bool: 连接是否成功
        """
        try:
            logger.info(f"连接到Milvus服务器: {self.milvus_uri}")

            # 准备连接参数
            connection_args = {"uri": self.milvus_uri}
            if self.milvus_token:
                connection_args["token"] = self.milvus_token

            # 创建LangChain Milvus向量存储
            self.vector_store = Milvus(
                embedding_function=self.embedding_model,
                collection_name=self.collection_name,
                connection_args=connection_args,
                auto_id=True
            )

            # 创建PyMilvus客户端（用于高级操作）
            self.client = MilvusClient(uri=self.milvus_uri, token=self.milvus_token)

            logger.info("Milvus连接创建成功")
            return True

        except Exception as e:
            logger.error(f"Milvus连接失败: {str(e)}")
            return False

    def check_collection_exists(self) -> bool:
        """
        检查集合是否存在

        Returns:
            bool: 集合是否存在
        """
        try:
            if not self.client:
                return False
            return self.client.has_collection(self.collection_name)
        except Exception as e:
            logger.error(f"检查集合存在性失败: {str(e)}")
            return False

    def create_collection_if_not_exists(self) -> bool:
        """
        如果集合不存在则创建集合

        Returns:
            bool: 操作是否成功
        """
        try:
            if not self.client:
                logger.error("Milvus客户端未初始化")
                return False

            # 检查集合是否存在
            if self.client.has_collection(self.collection_name):
                logger.info(f"集合 {self.collection_name} 已存在")
                return True

            # 让LangChain自动创建集合
            logger.info(f"集合 {self.collection_name} 将由LangChain自动创建")
            return True

        except Exception as e:
            logger.error(f"准备集合失败: {str(e)}")
            return False

    def add_documents(self, documents: List[Document]) -> bool:
        """
        添加文档到向量存储

        Args:
            documents: 要添加的文档列表

        Returns:
            bool: 操作是否成功
        """
        try:
            if not self.vector_store:
                logger.error("向量存储未初始化")
                return False

            logger.info(f"开始添加 {len(documents)} 个文档到向量存储")

            # 使用LangChain Milvus添加文档
            self.vector_store.add_documents(documents)

            logger.info("文档添加成功")
            return True

        except Exception as e:
            logger.error(f"添加文档失败: {str(e)}")
            return False

    def add_texts(self, texts: List[str], metadatas: Optional[List[Dict[str, Any]]] = None) -> bool:
        """
        添加文本到向量存储

        Args:
            texts: 要添加的文本列表
            metadatas: 元数据列表

        Returns:
            bool: 操作是否成功
        """
        try:
            if not self.vector_store:
                logger.error("向量存储未初始化")
                return False

            logger.info(f"开始添加 {len(texts)} 个文本到向量存储")

            # 使用LangChain Milvus添加文本
            self.vector_store.add_texts(texts, metadatas=metadatas)

            logger.info("文本添加成功")
            return True

        except Exception as e:
            logger.error(f"添加文本失败: {str(e)}")
            return False

    def similarity_search(self,
                         query: str,
                         k: int = 5,
                         filter_expr: Optional[str] = None) -> List[Document]:
        """
        相似性搜索

        Args:
            query: 查询文本
            k: 返回结果数量
            filter_expr: 过滤表达式

        Returns:
            List[Document]: 搜索结果
        """
        try:
            if not self.vector_store:
                logger.error("向量存储未初始化")
                return []

            logger.info(f"执行相似性搜索: {query[:50]}...")

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

            logger.info(f"搜索完成，返回 {len(results)} 个结果")
            return results

        except Exception as e:
            logger.error(f"相似性搜索失败: {str(e)}")
            return []

    def similarity_search_with_score(self,
                                   query: str,
                                   k: int = 5,
                                   filter_expr: Optional[str] = None) -> List[Tuple[Document, float]]:
        """
        带分数的相似性搜索

        Args:
            query: 查询文本
            k: 返回结果数量
            filter_expr: 过滤表达式

        Returns:
            List[Tuple[Document, float]]: (Document, score) 元组列表
        """
        try:
            if not self.vector_store:
                logger.error("向量存储未初始化")
                return []

            logger.info(f"执行带分数的相似性搜索: {query[:50]}...")

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

            logger.info(f"带分数搜索完成，返回 {len(results)} 个结果")
            return results

        except Exception as e:
            logger.error(f"带分数相似性搜索失败: {str(e)}")
            return []

    def get_collection_stats(self) -> Dict[str, Any]:
        """
        获取集合统计信息

        Returns:
            Dict[str, Any]: 集合统计信息
        """
        try:
            if not self.client:
                logger.error("Milvus客户端未初始化")
                return {}

            if not self.client.has_collection(self.collection_name):
                return {"exists": False}

            # 获取集合信息
            stats = self.client.get_collection_stats(self.collection_name)

            return {
                "exists": True,
                "row_count": stats.get("row_count", 0),
                "collection_name": self.collection_name,
                "embedding_model": self.embedding_model_type
            }

        except Exception as e:
            logger.error(f"获取集合统计信息失败: {str(e)}")
            return {"exists": False, "error": str(e)}

    def delete_collection(self) -> bool:
        """
        删除集合

        Returns:
            bool: 操作是否成功
        """
        try:
            if not self.client:
                logger.error("Milvus客户端未初始化")
                return False

            if self.client.has_collection(self.collection_name):
                self.client.drop_collection(self.collection_name)
                logger.info(f"集合 {self.collection_name} 已删除")
                return True
            else:
                logger.info(f"集合 {self.collection_name} 不存在")
                return True

        except Exception as e:
            logger.error(f"删除集合失败: {str(e)}")
            return False