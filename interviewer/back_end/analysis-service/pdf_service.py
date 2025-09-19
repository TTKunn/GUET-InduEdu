"""
PDF解析服务
"""

import os
import logging
import tempfile
from typing import Optional, Dict, Any
from pathlib import Path
import requests
from fastapi import UploadFile, HTTPException

from config import (
    PDF_CHUNK_SIZE, PDF_CHUNK_OVERLAP, PDF_MAX_FILE_SIZE,
    ALLOWED_FILE_EXTENSIONS, ALLOWED_MIME_TYPES
)

logger = logging.getLogger(__name__)

class PDFService:
    """PDF解析服务类"""
    
    def __init__(self):
        # PDF解析服务的URL - 使用新的pdf-parser-service
        self.pdf_parser_url = os.getenv("DOCUMENT_PARSER_URL", "http://43.142.157.145:8003")
        self.max_file_size = PDF_MAX_FILE_SIZE * 1024 * 1024  # 转换为字节
        
    def validate_file(self, file: UploadFile) -> bool:
        """验证上传的文件"""
        try:
            # 检查文件扩展名
            file_ext = Path(file.filename).suffix.lower()
            if file_ext not in ALLOWED_FILE_EXTENSIONS:
                raise HTTPException(
                    status_code=400,
                    detail=f"不支持的文件类型: {file_ext}. 支持的类型: {ALLOWED_FILE_EXTENSIONS}"
                )
            
            # 检查MIME类型
            if file.content_type not in ALLOWED_MIME_TYPES:
                raise HTTPException(
                    status_code=400,
                    detail=f"不支持的MIME类型: {file.content_type}. 支持的类型: {ALLOWED_MIME_TYPES}"
                )
            
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"文件验证失败: {e}")
            raise HTTPException(status_code=400, detail=f"文件验证失败: {str(e)}")
    
    def parse_pdf_with_parser_service(self, file: UploadFile) -> str:
        """使用pdf-parser-service解析PDF"""
        try:
            logger.info(f"开始解析PDF文件: {file.filename}")

            # 准备请求数据
            files = {
                'file': (file.filename, file.file, file.content_type)
            }

            data = {
                'chunk_size': PDF_CHUNK_SIZE,
                'chunk_overlap': PDF_CHUNK_OVERLAP,
                'split_text': True
            }

            # 调用pdf-parser-service的/parse-text接口
            response = requests.post(
                f"{self.pdf_parser_url}/parse-text",
                files=files,
                data=data,
                timeout=60
            )
            
            if response.status_code != 200:
                error_msg = f"PDF解析服务调用失败: {response.status_code}"
                logger.error(error_msg)
                raise HTTPException(status_code=500, detail=error_msg)

            result = response.json()

            # 提取文本内容 - 适配新的pdf-parser-service响应格式
            logger.info(f"PDF解析服务返回结果: {result}")
            if result.get('success') and 'text_content' in result:
                text_content = result['text_content']
                logger.info(f"PDF解析完成: {file.filename}, 内容长度: {len(text_content)}")
                return text_content.strip()
            else:
                error_msg = result.get('message', 'PDF解析服务返回空结果')
                logger.warning(f"PDF解析失败: {error_msg}")
                raise HTTPException(status_code=503, detail=f"PDF解析失败: {error_msg}")
                
        except requests.exceptions.RequestException as e:
            error_msg = f"PDF解析服务连接失败: {str(e)}"
            logger.error(error_msg)
            raise HTTPException(status_code=503, detail=error_msg)
        except HTTPException:
            raise
        except Exception as e:
            error_msg = f"PDF解析失败: {str(e)}"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
    
    def parse_pdf_local(self, file: UploadFile) -> str:
        """本地解析PDF（备用方案）"""
        try:
            logger.info(f"使用本地方法解析PDF: {file.filename}")

            # 创建临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                # 写入上传的文件内容
                content = file.file.read()
                logger.info(f"读取文件内容: {len(content) if content else 0} 字节")
                if not content:
                    raise HTTPException(status_code=400, detail="上传的文件为空")
                temp_file.write(content)
                temp_file_path = temp_file.name
            
            try:
                # 使用PyPDF2解析
                import PyPDF2
                
                text_content = ""
                with open(temp_file_path, 'rb') as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    
                    for page_num, page in enumerate(pdf_reader.pages):
                        try:
                            page_text = page.extract_text()
                            if page_text:
                                text_content += f"\n--- 第{page_num + 1}页 ---\n"
                                text_content += page_text + "\n"
                        except Exception as e:
                            logger.warning(f"解析第{page_num + 1}页失败: {e}")
                            continue
                
                if not text_content.strip():
                    raise HTTPException(status_code=500, detail="PDF文件无法提取文本内容")
                
                logger.info(f"本地PDF解析完成: {file.filename}, 内容长度: {len(text_content)}")
                return text_content.strip()
                
            finally:
                # 清理临时文件
                try:
                    os.unlink(temp_file_path)
                except Exception as e:
                    logger.warning(f"清理临时文件失败: {e}")
                    
        except ImportError:
            raise HTTPException(
                status_code=500, 
                detail="PyPDF2库未安装，无法使用本地解析功能"
            )
        except Exception as e:
            error_msg = f"本地PDF解析失败: {str(e)}"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
    
    def parse_pdf(self, file: UploadFile, use_local: bool = False) -> str:
        """解析PDF文件"""
        # 验证文件
        self.validate_file(file)

        # 重置文件指针
        file.file.seek(0)

        try:
            if use_local:
                return self.parse_pdf_local(file)
            else:
                return self.parse_pdf_with_parser_service(file)
        except (HTTPException, Exception) as e:
            # 如果PDF解析服务失败，尝试本地解析
            if not use_local:
                logger.warning(f"PDF解析服务失败: {str(e)}，尝试本地解析")
                file.file.seek(0)  # 重置文件指针
                return self.parse_pdf_local(file)
            else:
                raise
    
    def check_pdf_parser_service(self) -> Dict[str, Any]:
        """检查PDF解析服务状态"""
        try:
            response = requests.get(
                f"{self.pdf_parser_url}/health",
                timeout=5
            )

            if response.status_code == 200:
                return {
                    "available": True,
                    "status": "healthy",
                    "url": self.pdf_parser_url
                }
            else:
                return {
                    "available": False,
                    "status": f"unhealthy (status: {response.status_code})",
                    "url": self.pdf_parser_url
                }

        except requests.exceptions.RequestException as e:
            return {
                "available": False,
                "status": f"connection_failed ({str(e)})",
                "url": self.pdf_parser_url
            }

# 全局PDF服务实例
pdf_service = PDFService()
