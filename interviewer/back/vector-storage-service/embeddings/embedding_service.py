"""
嵌入模型服务 - 独立版本
支持BGE和智谱AI嵌入模型
"""

import os
import logging
from typing import List, Optional
from langchain_huggingface import HuggingFaceEmbeddings

logger = logging.getLogger(__name__)

# 智谱AI嵌入模型类
class ZhipuAIEmbeddings:
    """智谱AI嵌入模型"""

    def __init__(self, api_key: str, model: str = "embedding-2"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://open.bigmodel.cn/api/paas/v4/"

        # 检查是否安装了zhipuai库
        try:
            from zhipuai import ZhipuAI
            self.client = ZhipuAI(api_key=api_key)
            logger.info(f"智谱AI嵌入模型初始化成功: {model}")
        except ImportError:
            raise ImportError("请安装zhipuai库: pip install zhipuai")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """嵌入多个文档"""
        embeddings = []
        for text in texts:
            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=text
                )
                embeddings.append(response.data[0].embedding)
            except Exception as e:
                logger.error(f"智谱AI嵌入失败: {str(e)}")
                raise
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        """嵌入单个查询"""
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"智谱AI查询嵌入失败: {str(e)}")
            raise


class EmbeddingService:
    """嵌入模型服务管理器"""

    def __init__(self):
        self._bge_embedding = None
        self._zhipuai_embedding = None

        # 从环境变量获取配置
        self.zhipuai_api_key = os.getenv('ZHIPUAI_API_KEY', '')
        self.zhipuai_model = os.getenv('ZHIPUAI_EMBEDDING_MODEL', 'embedding-2')
        self.bge_model_name = os.getenv('BGE_MODEL_NAME', 'BAAI/bge-small-zh-v1.5')
        self.bge_device = os.getenv('BGE_DEVICE', 'cpu')
        self.bge_normalize = os.getenv('BGE_NORMALIZE_EMBEDDINGS', 'True').lower() == 'true'
        self.default_model = os.getenv('DEFAULT_EMBEDDING_MODEL', 'zhipuai')

    def get_bge_embedding(self):
        """获取BGE嵌入模型"""
        if self._bge_embedding is None:
            logger.info(f"初始化BGE嵌入模型: {self.bge_model_name}")

            model_kwargs = {"device": self.bge_device}
            encode_kwargs = {"normalize_embeddings": self.bge_normalize}

            self._bge_embedding = HuggingFaceEmbeddings(
                model_name=self.bge_model_name,
                model_kwargs=model_kwargs,
                encode_kwargs=encode_kwargs
            )
            logger.info("BGE嵌入模型初始化完成")

        return self._bge_embedding

    def get_zhipuai_embedding(self):
        """获取智谱AI嵌入模型"""
        if self._zhipuai_embedding is None:
            if not self.zhipuai_api_key:
                raise ValueError("ZHIPUAI_API_KEY未配置，无法使用智谱AI嵌入模型")

            self._zhipuai_embedding = ZhipuAIEmbeddings(
                api_key=self.zhipuai_api_key,
                model=self.zhipuai_model
            )

        return self._zhipuai_embedding

    def get_embedding_model(self, model_type: Optional[str] = None):
        """
        获取指定类型的嵌入模型

        Args:
            model_type: 模型类型 ('bge', 'zhipuai')，默认使用配置的默认模型

        Returns:
            嵌入模型实例
        """
        model_type = model_type or self.default_model

        if model_type == 'bge':
            return self.get_bge_embedding()
        elif model_type == 'zhipuai':
            return self.get_zhipuai_embedding()
        else:
            raise ValueError(f"不支持的嵌入模型类型: {model_type}")

    def embed_texts(self, texts: List[str], model_type: Optional[str] = None) -> List[List[float]]:
        """
        嵌入文本列表

        Args:
            texts: 要嵌入的文本列表
            model_type: 模型类型

        Returns:
            嵌入向量列表
        """
        embedding_model = self.get_embedding_model(model_type)
        return embedding_model.embed_documents(texts)

    def embed_query(self, text: str, model_type: Optional[str] = None) -> List[float]:
        """
        嵌入查询文本

        Args:
            text: 要嵌入的查询文本
            model_type: 模型类型

        Returns:
            嵌入向量
        """
        embedding_model = self.get_embedding_model(model_type)
        return embedding_model.embed_query(text)


# 全局嵌入服务实例
embedding_service = EmbeddingService()