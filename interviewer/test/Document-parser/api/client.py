"""
PDF解析API客户端
用于在其他项目中调用PDF解析服务
"""
import requests
import json
from typing import Dict, Any, List, Optional
from pathlib import Path

class PDFAnalyserClient:
    """PDF解析API客户端"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        初始化客户端
        
        Args:
            base_url: API服务地址
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """
        健康检查
        
        Returns:
            Dict: 健康状态信息
        """
        try:
            response = self.session.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"status": "error", "message": str(e)}
    
    def parse_pdf(self, 
                  pdf_path: str,
                  chunk_size: int = 1000,
                  chunk_overlap: int = 200,
                  split_text: bool = True,
                  return_content: bool = False) -> Dict[str, Any]:
        """
        解析PDF文件
        
        Args:
            pdf_path: PDF文件路径
            chunk_size: 文档分块大小
            chunk_overlap: 分块重叠大小
            split_text: 是否进行文本分块
            return_content: 是否返回解析内容
        
        Returns:
            Dict: 解析结果
        """
        if not Path(pdf_path).exists():
            return {"success": False, "message": f"文件不存在: {pdf_path}"}
        
        try:
            with open(pdf_path, 'rb') as f:
                files = {'file': (Path(pdf_path).name, f, 'application/pdf')}
                params = {
                    'chunk_size': chunk_size,
                    'chunk_overlap': chunk_overlap,
                    'split_text': split_text,
                    'return_content': return_content
                }
                
                response = self.session.post(
                    f"{self.base_url}/parse",
                    files=files,
                    params=params
                )
                response.raise_for_status()
                return response.json()
                
        except requests.RequestException as e:
            return {"success": False, "message": f"请求失败: {str(e)}"}
        except Exception as e:
            return {"success": False, "message": f"解析失败: {str(e)}"}
    
    def parse_and_store_pdf(self,
                           pdf_path: str,
                           collection_name: str = "pdf_documents",
                           chunk_size: int = 1000,
                           chunk_overlap: int = 200,
                           embedding_model: str = "zhipuai") -> Dict[str, Any]:
        """
        解析PDF文件并存储到向量数据库
        
        Args:
            pdf_path: PDF文件路径
            collection_name: Milvus集合名称
            chunk_size: 文档分块大小
            chunk_overlap: 分块重叠大小
            embedding_model: 嵌入模型类型
        
        Returns:
            Dict: 解析和存储结果
        """
        if not Path(pdf_path).exists():
            return {"success": False, "message": f"文件不存在: {pdf_path}"}
        
        try:
            with open(pdf_path, 'rb') as f:
                files = {'file': (Path(pdf_path).name, f, 'application/pdf')}
                params = {
                    'collection_name': collection_name,
                    'chunk_size': chunk_size,
                    'chunk_overlap': chunk_overlap,
                    'embedding_model': embedding_model
                }
                
                response = self.session.post(
                    f"{self.base_url}/parse-and-store",
                    files=files,
                    params=params
                )
                response.raise_for_status()
                return response.json()
                
        except requests.RequestException as e:
            return {"success": False, "message": f"请求失败: {str(e)}"}
        except Exception as e:
            return {"success": False, "message": f"解析存储失败: {str(e)}"}
    
    def search_documents(self,
                        query: str,
                        collection_name: str = "pdf_documents",
                        k: int = 5,
                        embedding_model: str = "zhipuai") -> Dict[str, Any]:
        """
        搜索文档
        
        Args:
            query: 搜索查询
            collection_name: Milvus集合名称
            k: 返回结果数量
            embedding_model: 嵌入模型类型
        
        Returns:
            Dict: 搜索结果
        """
        try:
            params = {
                'query': query,
                'collection_name': collection_name,
                'k': k,
                'embedding_model': embedding_model
            }
            
            response = self.session.get(
                f"{self.base_url}/search",
                params=params
            )
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            return {"success": False, "message": f"请求失败: {str(e)}"}
        except Exception as e:
            return {"success": False, "message": f"搜索失败: {str(e)}"}

# 便捷函数
def create_client(base_url: str = "http://localhost:8000") -> PDFAnalyserClient:
    """创建PDF解析客户端"""
    return PDFAnalyserClient(base_url)

def parse_pdf_file(pdf_path: str, 
                   api_url: str = "http://localhost:8000",
                   **kwargs) -> Dict[str, Any]:
    """
    便捷函数：解析PDF文件
    
    Args:
        pdf_path: PDF文件路径
        api_url: API服务地址
        **kwargs: 其他参数
    
    Returns:
        Dict: 解析结果
    """
    client = create_client(api_url)
    return client.parse_pdf(pdf_path, **kwargs)

def parse_and_store_pdf_file(pdf_path: str,
                            api_url: str = "http://localhost:8000",
                            **kwargs) -> Dict[str, Any]:
    """
    便捷函数：解析PDF文件并存储
    
    Args:
        pdf_path: PDF文件路径
        api_url: API服务地址
        **kwargs: 其他参数
    
    Returns:
        Dict: 解析和存储结果
    """
    client = create_client(api_url)
    return client.parse_and_store_pdf(pdf_path, **kwargs)

def search_pdf_documents(query: str,
                        api_url: str = "http://localhost:8000",
                        **kwargs) -> Dict[str, Any]:
    """
    便捷函数：搜索文档
    
    Args:
        query: 搜索查询
        api_url: API服务地址
        **kwargs: 其他参数
    
    Returns:
        Dict: 搜索结果
    """
    client = create_client(api_url)
    return client.search_documents(query, **kwargs)

if __name__ == "__main__":
    # 测试客户端
    client = create_client()
    
    # 健康检查
    health = client.health_check()
    print("健康检查:", health)
    
    # 如果有测试PDF文件，可以测试解析
    test_pdf = "./data/test.pdf"
    if Path(test_pdf).exists():
        result = client.parse_pdf(test_pdf, return_content=True)
        print("解析结果:", result)
