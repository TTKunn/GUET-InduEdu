"""
PDF解析器模块
基于PyPDFLoader的基础PDF解析功能
"""
import os
from typing import List, Optional
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.log_utils import log

try:
    from config import PDF_CHUNK_SIZE, PDF_CHUNK_OVERLAP, PDF_ENCODING
except ImportError:
    # 如果无法导入配置，使用默认值
    PDF_CHUNK_SIZE = 1000
    PDF_CHUNK_OVERLAP = 200
    PDF_ENCODING = 'utf-8'

class PDFParser:
    """
    PDF文档解析器
    使用PyPDFLoader进行基础PDF解析
    """
    
    def __init__(self, chunk_size: Optional[int] = None, chunk_overlap: Optional[int] = None):
        """
        初始化PDF解析器
        
        Args:
            chunk_size (int, optional): 文档分块大小，默认使用配置文件中的值
            chunk_overlap (int, optional): 分块重叠大小，默认使用配置文件中的值
        """
        self.chunk_size = chunk_size or PDF_CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or PDF_CHUNK_OVERLAP
        
        # 初始化文本分割器
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        log.info(f"PDF解析器初始化完成 - 分块大小: {self.chunk_size}, 重叠大小: {self.chunk_overlap}")
    
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
        
        log.info(f"开始加载PDF文件: {pdf_path}")
        
        try:
            # 使用PyPDFLoader加载PDF
            loader = PyPDFLoader(file_path=pdf_path)
            documents = loader.load()
            
            log.info(f"PDF加载完成 - 总页数: {len(documents)}")
            
            # 添加文件路径到元数据
            for doc in documents:
                doc.metadata['file_path'] = pdf_path
                doc.metadata['file_name'] = os.path.basename(pdf_path)
            
            return documents
            
        except Exception as e:
            log.error(f"PDF加载失败: {pdf_path}, 错误: {str(e)}")
            raise
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        对文档进行分块处理
        
        Args:
            documents (List[Document]): 原始文档列表
            
        Returns:
            List[Document]: 分块后的文档列表
        """
        log.info(f"开始文档分块 - 原始文档数: {len(documents)}")
        
        try:
            # 使用文本分割器进行分块
            split_docs = self.text_splitter.split_documents(documents)
            
            # 为分块添加额外的元数据
            for i, doc in enumerate(split_docs):
                doc.metadata['chunk_id'] = i
                doc.metadata['chunk_size'] = len(doc.page_content)
            
            log.info(f"文档分块完成 - 分块数: {len(split_docs)}")
            return split_docs
            
        except Exception as e:
            log.error(f"文档分块失败: {str(e)}")
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
        log.info(f"开始解析PDF文档: {pdf_path}")
        
        # 加载PDF文档
        documents = self.load_pdf(pdf_path)
        
        # 如果需要分块
        if split_text:
            documents = self.split_documents(documents)
        
        log.info(f"PDF文档解析完成 - 最终文档数: {len(documents)}")
        return documents
    
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

if __name__ == '__main__':
    # 测试PDF解析器
    parser = PDFParser()
    
    # 这里需要一个实际的PDF文件路径进行测试
    test_pdf_path = "./data/test.pdf"  # 请替换为实际的PDF文件路径
    
    if os.path.exists(test_pdf_path):
        try:
            # 解析PDF
            documents = parser.parse_pdf_to_documents(test_pdf_path)
            
            # 显示文档信息
            info = parser.get_document_info(documents)
            log.info(f"文档信息: {info}")
            
            # 显示前几个文档的内容
            for i, doc in enumerate(documents[:3]):
                log.info(f"文档 {i+1} 元数据: {doc.metadata}")
                log.info(f"文档 {i+1} 内容预览: {doc.page_content[:200]}...")
                
        except Exception as e:
            log.error(f"测试失败: {e}")
    else:
        log.warning(f"测试文件不存在: {test_pdf_path}")
