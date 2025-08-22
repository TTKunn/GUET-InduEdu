"""
PDF解析API测试脚本
直接使用本地PDF文件路径测试API功能
"""
import os
import requests
import json
from pathlib import Path

# API基础URL
API_BASE_URL = "http://localhost:8000"

def test_health_check():
    """测试健康检查接口"""
    print("=" * 50)
    print("测试健康检查接口")
    print("=" * 50)
    
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"健康检查失败: {e}")
        return False

def test_parse_pdf(pdf_path, return_content=False):
    """
    测试PDF解析接口
    
    Args:
        pdf_path: PDF文件路径
        return_content: 是否返回解析内容
    """
    print("=" * 50)
    print(f"测试PDF解析接口: {pdf_path}")
    print("=" * 50)
    
    if not os.path.exists(pdf_path):
        print(f"错误: PDF文件不存在 - {pdf_path}")
        return False
    
    try:
        # 准备文件
        with open(pdf_path, 'rb') as f:
            files = {'file': (os.path.basename(pdf_path), f, 'application/pdf')}
            
            # 准备参数
            params = {
                'chunk_size': 1000,
                'chunk_overlap': 200,
                'split_text': True,
                'return_content': return_content
            }
            
            # 发送请求
            response = requests.post(
                f"{API_BASE_URL}/parse",
                files=files,
                params=params
            )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"解析成功!")
            print(f"任务ID: {result['task_id']}")
            print(f"文档数量: {result['total_documents']}")
            print(f"总字符数: {result['total_chars']}")
            
            if return_content and 'documents' in result:
                print(f"返回了 {len(result['documents'])} 个文档片段")
                # 显示前两个文档片段的内容预览
                for i, doc in enumerate(result['documents'][:2]):
                    print(f"\n--- 文档片段 {i+1} ---")
                    print(f"内容长度: {doc['content_length']}")
                    print(f"内容预览: {doc['content'][:200]}...")
                    print(f"元数据: {json.dumps(doc['metadata'], ensure_ascii=False, indent=2)}")
            
            return True
        else:
            print(f"解析失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"请求失败: {e}")
        return False

def test_parse_and_store_pdf(pdf_path, collection_name="test_collection"):
    """
    测试PDF解析并存储接口
    
    Args:
        pdf_path: PDF文件路径
        collection_name: Milvus集合名称
    """
    print("=" * 50)
    print(f"测试PDF解析并存储接口: {pdf_path}")
    print("=" * 50)
    
    if not os.path.exists(pdf_path):
        print(f"错误: PDF文件不存在 - {pdf_path}")
        return False
    
    try:
        # 准备文件
        with open(pdf_path, 'rb') as f:
            files = {'file': (os.path.basename(pdf_path), f, 'application/pdf')}
            
            # 准备参数
            params = {
                'collection_name': collection_name,
                'chunk_size': 1000,
                'chunk_overlap': 200,
                'embedding_model': 'zhipuai'
            }
            
            # 发送请求
            response = requests.post(
                f"{API_BASE_URL}/parse-and-store",
                files=files,
                params=params
            )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"解析并存储成功!")
            print(f"任务ID: {result['task_id']}")
            print(f"文档数量: {result['total_documents']}")
            print(f"总字符数: {result['total_chars']}")
            return True
        else:
            print(f"解析并存储失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"请求失败: {e}")
        return False

def test_search_documents(query, collection_name="test_collection", k=3):
    """
    测试文档搜索接口
    
    Args:
        query: 搜索查询
        collection_name: Milvus集合名称
        k: 返回结果数量
    """
    print("=" * 50)
    print(f"测试文档搜索接口: {query}")
    print("=" * 50)
    
    try:
        # 准备参数
        params = {
            'query': query,
            'collection_name': collection_name,
            'k': k,
            'embedding_model': 'zhipuai'
        }
        
        # 发送请求
        response = requests.get(f"{API_BASE_URL}/search", params=params)
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"搜索成功!")
            print(f"结果数量: {result['total_results']}")
            
            for i, doc in enumerate(result['results']):
                print(f"\n--- 搜索结果 {i+1} ---")
                print(f"相似度分数: {doc['similarity_score']:.4f}")
                print(f"内容长度: {doc['content_length']}")
                print(f"内容预览: {doc['content'][:200]}...")
                print(f"元数据: {json.dumps(doc['metadata'], ensure_ascii=False, indent=2)}")
            
            return True
        else:
            print(f"搜索失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"请求失败: {e}")
        return False

def main():
    """主测试函数"""
    print("PDF解析API测试开始")
    print("请确保API服务已启动 (python start_api.py)")
    
    # 1. 健康检查
    if not test_health_check():
        print("API服务未正常运行，请检查服务状态")
        return
    
    # 2. 获取PDF文件路径
    print("\n请输入要测试的PDF文件路径:")
    pdf_path = input("PDF路径: ").strip().strip('"').strip("'")
    
    if not pdf_path:
        print("未提供PDF文件路径，使用示例路径测试")
        # 你可以在这里设置一个默认的PDF文件路径
        pdf_path = "examples/sample.pdf"  # 示例路径
    
    # 3. 测试PDF解析（不返回内容）
    print(f"\n开始测试PDF文件: {pdf_path}")
    if test_parse_pdf(pdf_path, return_content=False):
        print("✓ PDF解析测试通过")
    else:
        print("✗ PDF解析测试失败")
        return
    
    # 4. 测试PDF解析（返回内容）
    if test_parse_pdf(pdf_path, return_content=True):
        print("✓ PDF解析（含内容）测试通过")
    else:
        print("✗ PDF解析（含内容）测试失败")
    
    # 5. 测试PDF解析并存储（需要Milvus）
    print("\n是否测试PDF解析并存储功能？(需要Milvus数据库) [y/N]:")
    test_store = input().strip().lower()
    
    if test_store in ['y', 'yes']:
        collection_name = f"test_collection_{int(os.path.getmtime(pdf_path))}"
        if test_parse_and_store_pdf(pdf_path, collection_name):
            print("✓ PDF解析并存储测试通过")
            
            # 6. 测试搜索功能
            print("\n请输入搜索查询:")
            query = input("搜索查询: ").strip()
            if query:
                if test_search_documents(query, collection_name):
                    print("✓ 文档搜索测试通过")
                else:
                    print("✗ 文档搜索测试失败")
        else:
            print("✗ PDF解析并存储测试失败")
    
    print("\n测试完成!")

if __name__ == "__main__":
    main()
