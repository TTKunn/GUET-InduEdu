"""
嵌入模型模块
支持OpenAI、BGE和智谱AI嵌入模型
"""
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

try:
    from config import (
        OPENAI_API_KEY, OPENAI_API_BASE,
        BGE_MODEL_NAME, BGE_DEVICE, BGE_NORMALIZE_EMBEDDINGS,
        ZHIPUAI_API_KEY, ZHIPUAI_EMBEDDING_MODEL, DEFAULT_EMBEDDING_MODEL
    )
except ImportError:
    # 如果无法导入配置，使用默认值
    import os
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_API_BASE = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
    BGE_MODEL_NAME = os.getenv('BGE_MODEL_NAME', 'BAAI/bge-small-zh-v1.5')
    BGE_DEVICE = os.getenv('BGE_DEVICE', 'cpu')
    BGE_NORMALIZE_EMBEDDINGS = os.getenv('BGE_NORMALIZE_EMBEDDINGS', 'True').lower() == 'true'
    ZHIPUAI_API_KEY = os.getenv('ZHIPUAI_API_KEY', '')
    ZHIPUAI_EMBEDDING_MODEL = os.getenv('ZHIPUAI_EMBEDDING_MODEL', 'embedding-2')
    DEFAULT_EMBEDDING_MODEL = os.getenv('DEFAULT_EMBEDDING_MODEL', 'zhipuai')

from utils.log_utils import log

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
        except ImportError:
            raise ImportError("请安装zhipuai库: pip install zhipuai")

    def embed_documents(self, texts):
        """嵌入多个文档"""
        embeddings = []
        for text in texts:
            response = self.client.embeddings.create(
                model=self.model,
                input=text
            )
            embeddings.append(response.data[0].embedding)
        return embeddings

    def embed_query(self, text):
        """嵌入单个查询"""
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding

class EmbeddingModelManager:
    """嵌入模型管理器"""

    def __init__(self):
        self._openai_embedding = None
        self._bge_embedding = None
        self._zhipuai_embedding = None
    
    @property
    def openai_embedding(self):
        """获取OpenAI嵌入模型"""
        if self._openai_embedding is None:
            if not OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY未配置，无法使用OpenAI嵌入模型")
            
            log.info("初始化OpenAI嵌入模型...")
            self._openai_embedding = OpenAIEmbeddings(
                openai_api_key=OPENAI_API_KEY,
                openai_api_base=OPENAI_API_BASE
            )
            log.info("OpenAI嵌入模型初始化完成")
        
        return self._openai_embedding
    
    @property
    def bge_embedding(self):
        """获取BGE嵌入模型"""
        if self._bge_embedding is None:
            log.info(f"初始化BGE嵌入模型: {BGE_MODEL_NAME}")
            
            model_kwargs = {"device": BGE_DEVICE}
            encode_kwargs = {"normalize_embeddings": BGE_NORMALIZE_EMBEDDINGS}
            
            self._bge_embedding = HuggingFaceEmbeddings(
                model_name=BGE_MODEL_NAME,
                model_kwargs=model_kwargs,
                encode_kwargs=encode_kwargs
            )
            log.info("BGE嵌入模型初始化完成")
        
        return self._bge_embedding

    @property
    def zhipuai_embedding(self):
        """获取智谱AI嵌入模型"""
        if self._zhipuai_embedding is None:
            if not ZHIPUAI_API_KEY:
                raise ValueError("ZHIPUAI_API_KEY未配置，无法使用智谱AI嵌入模型")

            log.info(f"初始化智谱AI嵌入模型: {ZHIPUAI_EMBEDDING_MODEL}")
            self._zhipuai_embedding = ZhipuAIEmbeddings(
                api_key=ZHIPUAI_API_KEY,
                model=ZHIPUAI_EMBEDDING_MODEL
            )
            log.info("智谱AI嵌入模型初始化完成")

        return self._zhipuai_embedding

    def get_embedding_model(self, model_type=None):
        """
        获取指定类型的嵌入模型

        Args:
            model_type (str): 模型类型，'openai'、'bge' 或 'zhipuai'
                            如果为None，使用默认配置

        Returns:
            嵌入模型实例
        """
        if model_type is None:
            model_type = DEFAULT_EMBEDDING_MODEL

        model_type = model_type.lower()

        if model_type == "openai":
            return self.openai_embedding
        elif model_type == "bge":
            return self.bge_embedding
        elif model_type == "zhipuai":
            return self.zhipuai_embedding
        else:
            raise ValueError(f"不支持的模型类型: {model_type}，支持的类型: openai, bge, zhipuai")

# 创建全局嵌入模型管理器实例
embedding_manager = EmbeddingModelManager()

# 便捷访问接口
def get_default_embedding():
    """获取默认嵌入模型"""
    return embedding_manager.get_embedding_model()

# 兼容性接口
openai_embedding = lambda: embedding_manager.openai_embedding
bge_embedding = lambda: embedding_manager.bge_embedding
zhipuai_embedding = lambda: embedding_manager.zhipuai_embedding

if __name__ == '__main__':
    # 测试嵌入模型
    try:
        # 测试默认模型（智谱AI）
        log.info("测试默认嵌入模型...")
        default_model = get_default_embedding()
        test_texts = ["这是一个测试文本", "Hello World"]
        embeddings = default_model.embed_documents(test_texts)
        log.info(f"默认模型嵌入结果维度: {len(embeddings[0])}")

        # 测试查询嵌入
        query_embedding = default_model.embed_query("测试查询")
        log.info(f"查询嵌入维度: {len(query_embedding)}")

        # 测试智谱AI模型
        if ZHIPUAI_API_KEY:
            log.info("测试智谱AI嵌入模型...")
            zhipuai_model = embedding_manager.get_embedding_model("zhipuai")
            zhipuai_embeddings = zhipuai_model.embed_documents(["智谱AI测试文本"])
            log.info(f"智谱AI嵌入结果维度: {len(zhipuai_embeddings[0])}")
        else:
            log.warning("ZHIPUAI_API_KEY未配置，跳过智谱AI模型测试")

    except Exception as e:
        log.error(f"嵌入模型测试失败: {e}")
        log.exception(e)
