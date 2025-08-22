#!/usr/bin/env python3
"""
用户知识库管理工具
用于创建和管理用户个人知识库
"""

import requests
import json
from typing import Dict, Any
from database.milvus_client import MilvusVectorStore
from loguru import logger

class UserKnowledgeManager:
    """用户知识库管理器"""
    
    def __init__(self, pdf_api_url: str = "http://localhost:8002", 
                 dify_adapter_url: str = "http://localhost:8001"):
        self.pdf_api_url = pdf_api_url
        self.dify_adapter_url = dify_adapter_url
    
    def create_user_knowledge_base(self, user_id: str) -> Dict[str, Any]:
        """
        为用户创建个人知识库
        
        Args:
            user_id: 用户ID
            
        Returns:
            Dict: 创建结果
        """
        try:
            collection_name = f"user_kb_{user_id}"
            api_key = f"dify-user-{user_id}"
            
            # 1. 创建Milvus集合
            vector_store = MilvusVectorStore(
                collection_name=collection_name,
                embedding_model_type="zhipuai"
            )
            
            if not vector_store.create_connection():
                raise Exception("无法连接到Milvus数据库")
            
            if not vector_store.create_collection_if_not_exists():
                raise Exception("无法创建Milvus集合")
            
            logger.info(f"为用户 {user_id} 创建知识库集合: {collection_name}")
            
            # 2. 测试适配器连接
            test_response = requests.get(f"{self.dify_adapter_url}/health")
            if test_response.status_code != 200:
                raise Exception("Dify适配器服务不可用")
            
            return {
                "success": True,
                "user_id": user_id,
                "collection_name": collection_name,
                "api_key": api_key,
                "dify_config": {
                    "api_url": f"{self.dify_adapter_url}/retrieval",
                    "api_key": api_key,
                    "knowledge_id": collection_name
                },
                "message": f"用户 {user_id} 的知识库创建成功"
            }
            
        except Exception as e:
            logger.error(f"创建用户知识库失败: {str(e)}")
            return {
                "success": False,
                "user_id": user_id,
                "error": str(e),
                "message": f"用户 {user_id} 的知识库创建失败"
            }
    
    def upload_user_document(self, user_id: str, file_path: str) -> Dict[str, Any]:
        """
        为用户上传文档到个人知识库
        
        Args:
            user_id: 用户ID
            file_path: 文档文件路径
            
        Returns:
            Dict: 上传结果
        """
        try:
            collection_name = f"user_kb_{user_id}"
            
            # 上传文档到PDF解析API
            with open(file_path, 'rb') as f:
                files = {'file': f}
                data = {
                    'collection_name': collection_name,
                    'chunk_size': 1000,
                    'chunk_overlap': 200,
                    'embedding_model': 'zhipuai'
                }
                
                response = requests.post(
                    f"{self.pdf_api_url}/parse-and-store",
                    files=files,
                    data=data
                )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"用户 {user_id} 文档上传成功: {file_path}")
                return {
                    "success": True,
                    "user_id": user_id,
                    "file_path": file_path,
                    "collection_name": collection_name,
                    "result": result
                }
            else:
                raise Exception(f"上传失败: {response.text}")
                
        except Exception as e:
            logger.error(f"用户文档上传失败: {str(e)}")
            return {
                "success": False,
                "user_id": user_id,
                "file_path": file_path,
                "error": str(e)
            }
    
    def test_user_retrieval(self, user_id: str, query: str) -> Dict[str, Any]:
        """
        测试用户知识库检索
        
        Args:
            user_id: 用户ID
            query: 查询内容
            
        Returns:
            Dict: 检索结果
        """
        try:
            api_key = f"dify-user-{user_id}"
            collection_name = f"user_kb_{user_id}"
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "knowledge_id": collection_name,
                "query": query,
                "retrieval_setting": {
                    "top_k": 5,
                    "score_threshold": 0.5
                }
            }
            
            response = requests.post(
                f"{self.dify_adapter_url}/retrieval",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"用户 {user_id} 检索测试成功")
                return {
                    "success": True,
                    "user_id": user_id,
                    "query": query,
                    "results": result
                }
            else:
                raise Exception(f"检索失败: {response.text}")
                
        except Exception as e:
            logger.error(f"用户检索测试失败: {str(e)}")
            return {
                "success": False,
                "user_id": user_id,
                "query": query,
                "error": str(e)
            }

def main():
    """命令行工具主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python user_manager.py create <user_id>")
        print("  python user_manager.py upload <user_id> <file_path>")
        print("  python user_manager.py test <user_id> <query>")
        return
    
    manager = UserKnowledgeManager()
    command = sys.argv[1]
    
    if command == "create" and len(sys.argv) >= 3:
        user_id = sys.argv[2]
        result = manager.create_user_knowledge_base(user_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    elif command == "upload" and len(sys.argv) >= 4:
        user_id = sys.argv[2]
        file_path = sys.argv[3]
        result = manager.upload_user_document(user_id, file_path)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    elif command == "test" and len(sys.argv) >= 4:
        user_id = sys.argv[2]
        query = sys.argv[3]
        result = manager.test_user_retrieval(user_id, query)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    else:
        print("无效的命令或参数")

if __name__ == "__main__":
    main()
