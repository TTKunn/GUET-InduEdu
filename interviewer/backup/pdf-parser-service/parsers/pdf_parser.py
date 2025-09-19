"""
PDF解析器模块 - 独立服务版本
基于PyPDFLoader的基础PDF解析功能，去除向量存储依赖
"""
import os
import logging
from typing import List, Optional
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 使用标准logging，避免外部依赖
logger = logging.getLogger(__name__)

class PDFParser:
    """
    PDF文档解析器 - 独立服务版本
    使用PyPDFLoader进行基础PDF解析，专注于文本提取
    """

    def __init__(self, chunk_size: Optional[int] = None, chunk_overlap: Optional[int] = None):
        """
        初始化PDF解析器

        Args:
            chunk_size (int, optional): 文档分块大小，默认1000
            chunk_overlap (int, optional): 分块重叠大小，默认200
        """
        self.chunk_size = chunk_size or 1000
        self.chunk_overlap = chunk_overlap or 200

        # 初始化文本分割器
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

        logger.info(f"PDF解析器初始化完成 - 分块大小: {self.chunk_size}, 重叠大小: {self.chunk_overlap}")

    def load_pdf(self, pdf_path: str) -> List[Document]:
        """
        加载PDF文档

        Args:
            pdf_path (str): PDF文件路径

        Returns:
            List[Document]: 文档列表，每页对应一个Document对象

        Raises:
            FileNotFoundError: 文件不存在
            Exception: 解析失败
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")

        logger.info(f"开始加载PDF文件: {pdf_path}")

        try:
            # 使用PyPDFLoader加载PDF
            loader = PyPDFLoader(file_path=pdf_path)
            documents = loader.load()

            logger.info(f"PDF加载完成 - 总页数: {len(documents)}")

            # 添加文件路径到元数据
            for doc in documents:
                doc.metadata['file_path'] = pdf_path
                doc.metadata['file_name'] = os.path.basename(pdf_path)

            return documents

        except Exception as e:
            logger.error(f"PDF加载失败: {pdf_path}, 错误: {str(e)}")
            raise

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        对文档进行分块处理

        Args:
            documents (List[Document]): 原始文档列表

        Returns:
            List[Document]: 分块后的文档列表
        """
        logger.info(f"开始文档分块 - 原始文档数: {len(documents)}")

        try:
            # 使用文本分割器进行分块
            split_docs = self.text_splitter.split_documents(documents)

            # 为分块添加额外的元数据
            for i, doc in enumerate(split_docs):
                doc.metadata['chunk_id'] = i
                doc.metadata['chunk_size'] = len(doc.page_content)

            logger.info(f"文档分块完成 - 分块数: {len(split_docs)}")
            return split_docs

        except Exception as e:
            logger.error(f"文档分块失败: {str(e)}")
            raise

    def parse_pdf_to_documents(self, pdf_path: str, split_text: bool = True) -> List[Document]:
        """
        解析PDF文档为Document对象列表

        Args:
            pdf_path (str): PDF文件路径
            split_text (bool): 是否进行文本分块，默认True

        Returns:
            List[Document]: 解析后的文档列表
        """
        logger.info(f"开始解析PDF文档: {pdf_path}")

        # 加载PDF文档
        documents = self.load_pdf(pdf_path)

        # 如果需要分块
        if split_text:
            documents = self.split_documents(documents)

        logger.info(f"PDF文档解析完成 - 最终文档数: {len(documents)}")
        return documents

    def parse_pdf_to_text(self, pdf_path: str, split_text: bool = True) -> str:
        """
        解析PDF文档为纯文本

        Args:
            pdf_path (str): PDF文件路径
            split_text (bool): 是否进行文本分块，默认True

        Returns:
            str: 解析后的文本内容
        """
        documents = self.parse_pdf_to_documents(pdf_path, split_text)

        # 合并所有文档内容
        text_content = "\n\n".join([doc.page_content for doc in documents])

        return text_content

    def get_document_info(self, documents: List[Document]) -> dict:
        """
        获取文档信息统计

        Args:
            documents (List[Document]): 文档列表

        Returns:
            dict: 文档信息统计
        """
        if not documents:
            return {"total_docs": 0, "total_chars": 0, "avg_chars": 0}

        total_chars = sum(len(doc.page_content) for doc in documents)
        avg_chars = total_chars / len(documents)

        # 获取页数信息（如果有）
        pages = set()
        for doc in documents:
            if 'page' in doc.metadata:
                pages.add(doc.metadata['page'])

        info = {
            "total_docs": len(documents),
            "total_chars": total_chars,
            "avg_chars": round(avg_chars, 2),
            "total_pages": len(pages) if pages else "未知"
        }

        return info