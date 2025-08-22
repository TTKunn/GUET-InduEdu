"""
PDF_ANALYSER 配置文件
包含所有可配置的参数，避免硬编码
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(override=True)

# ==================== API配置 ====================
# OpenAI API配置
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_API_BASE = os.getenv('OPENAI_API_BASE', 'https://xiaoai.plus/v1')

# DeepSeek API配置
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')

# 智谱AI API配置
ZHIPUAI_API_KEY = os.getenv('ZHIPUAI_API_KEY', '')

# ==================== Milvus数据库配置 ====================
# Milvus连接配置（可选，仅在需要向量存储时使用）
MILVUS_URI = os.getenv('MILVUS_URI', 'http://localhost:19530')
MILVUS_TOKEN = os.getenv('MILVUS_TOKEN', '')  # 如果需要认证
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'pdf_documents')

# ==================== 嵌入模型配置 ====================
# 默认嵌入模型类型
DEFAULT_EMBEDDING_MODEL = os.getenv('DEFAULT_EMBEDDING_MODEL', 'zhipuai')

# BGE嵌入模型配置
BGE_MODEL_NAME = os.getenv('BGE_MODEL_NAME', 'BAAI/bge-small-zh-v1.5')
BGE_DEVICE = os.getenv('BGE_DEVICE', 'cpu')  # 可选: cpu, cuda
BGE_NORMALIZE_EMBEDDINGS = os.getenv('BGE_NORMALIZE_EMBEDDINGS', 'True').lower() == 'true'

# 智谱AI嵌入模型配置
ZHIPUAI_EMBEDDING_MODEL = os.getenv('ZHIPUAI_EMBEDDING_MODEL', 'embedding-2')

# ==================== 文档处理配置 ====================
# PDF解析配置
PDF_CHUNK_SIZE = int(os.getenv('PDF_CHUNK_SIZE', '1000'))  # 文档分块大小
PDF_CHUNK_OVERLAP = int(os.getenv('PDF_CHUNK_OVERLAP', '200'))  # 分块重叠大小
PDF_ENCODING = os.getenv('PDF_ENCODING', 'utf-8')

# 文件路径配置
DATA_DIR = os.getenv('DATA_DIR', './data')
OUTPUT_DIR = os.getenv('OUTPUT_DIR', './output')
LOG_DIR = os.getenv('LOG_DIR', './logs')

# ==================== 日志配置 ====================
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')  # DEBUG, INFO, WARNING, ERROR
LOG_FORMAT = os.getenv('LOG_FORMAT', 'detailed')  # simple, detailed

# ==================== 其他配置 ====================
# 批处理配置
BATCH_SIZE = int(os.getenv('BATCH_SIZE', '20'))
MAX_WORKERS = int(os.getenv('MAX_WORKERS', '4'))

# 创建必要的目录
for directory in [DATA_DIR, OUTPUT_DIR, LOG_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
