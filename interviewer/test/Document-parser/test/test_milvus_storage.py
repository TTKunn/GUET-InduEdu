"""
测试PDF解析并存储到Milvus的脚本
"""
import os
import requests
import json
import time

# API基础URL
API_BASE_URL = "http://localhost:8000"

def test_parse_and_store(pdf_path, collection_name="test_resume_collection"):
    """
    测试PDF解析并存储到Milvus
    
    Args:
        pdf_path: PDF文件路径
        collection_name: Milvus集合名称
    """
    print(f"开始测试PDF解析并存储: {pdf_path}")
    print(f"目标集合: {collection_name}")
    
    # 检查文件是否存在
    if not os.path.exists(pdf_path):
        print(f"错误: 文件不存在 - {pdf_path}")
        return False, None
    
    try:
        # 1. 健康检查
        print("1. 检查API服务状态...")
        health_response = requests.get(f"{API_BASE_URL}/health")
        if health_response.status_code != 200:
            print(f"API服务异常: {health_response.status_code}")
            return False, None
        print("✓ API服务正常")
        
        # 2. 解析并存储PDF
        print("2. 开始解析并存储PDF到Milvus...")
        with open(pdf_path, 'rb') as f:
            files = {'file': (os.path.basename(pdf_path), f, 'application/pdf')}
            params = {
                'collection_name': collection_name,
                'chunk_size': 1000,
                'chunk_overlap': 200,
                'embedding_model': 'zhipuai'  # 使用智谱AI嵌入模型
            }
            
            response = requests.post(
                f"{API_BASE_URL}/parse-and-store",
                files=files,
                params=params,
                timeout=60  # 增加超时时间，因为嵌入计算可能需要时间
            )
        
        if response.status_code == 200:
            result = response.json()
            print("✓ PDF解析并存储成功!")
            print(f"  - 任务ID: {result['task_id']}")
            print(f"  - 文档片段数: {result['total_documents']}")
            print(f"  - 总字符数: {result['total_chars']}")
            print(f"  - 存储到集合: {collection_name}")
            
            return True, result['task_id']
        else:
            print(f"✗ PDF解析并存储失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"✗ 测试过程中出现错误: {e}")
        return False, None

def test_search(query, collection_name="test_resume_collection", k=3):
    """
    测试文档搜索功能
    
    Args:
        query: 搜索查询
        collection_name: Milvus集合名称
        k: 返回结果数量
    """
    print(f"\n开始搜索测试: '{query}'")
    print(f"搜索集合: {collection_name}")
    
    try:
        params = {
            'query': query,
            'collection_name': collection_name,
            'k': k,
            'embedding_model': 'zhipuai'
        }
        
        response = requests.get(f"{API_BASE_URL}/search", params=params)
        
        if response.status_code == 200:
            result = response.json()
            print("✓ 搜索成功!")
            print(f"  - 找到 {result['total_results']} 个相关结果")
            
            for i, doc in enumerate(result['results']):
                print(f"\n--- 搜索结果 {i+1} ---")
                print(f"相似度分数: {doc['similarity_score']:.4f}")
                print(f"内容长度: {doc['content_length']} 字符")
                print(f"内容预览: {doc['content'][:200]}...")
                
                # 显示关键元数据
                metadata = doc['metadata']
                if 'source_filename' in metadata:
                    print(f"来源文件: {metadata['source_filename']}")
                if 'page' in metadata:
                    print(f"页码: {metadata['page'] + 1}")
            
            return True
        else:
            print(f"✗ 搜索失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ 搜索过程中出现错误: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("PDF解析并存储到Milvus测试")
    print("=" * 60)
    
    # 获取PDF文件路径
    print("请输入PDF文件的完整路径:")
    pdf_path = input("PDF路径: ").strip().strip('"').strip("'")
    
    if not pdf_path:
        print("未提供PDF文件路径")
        return
    
    # 生成唯一的集合名称（基于文件名和时间戳）
    file_name = os.path.splitext(os.path.basename(pdf_path))[0]
    timestamp = int(time.time())

    # 将中文和特殊字符转换为安全的集合名称
    import re
    import hashlib

    # 如果文件名包含非ASCII字符，使用哈希值
    if not file_name.isascii():
        # 对中文文件名生成哈希
        hash_name = hashlib.md5(file_name.encode('utf-8')).hexdigest()[:8]
        collection_name = f"test_doc_{hash_name}_{timestamp}"
    else:
        # ASCII文件名，清理特殊字符
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)
        collection_name = f"test_{safe_name}_{timestamp}"
    
    print(f"\n将使用集合名称: {collection_name}")
    
    # 测试解析并存储
    success, task_id = test_parse_and_store(pdf_path, collection_name)
    
    if success:
        print(f"\n✓ PDF已成功存储到Milvus集合: {collection_name}")
        print("现在你可以在Attu中查看这个集合了!")
        
        # 等待一下确保数据完全写入
        print("\n等待3秒确保数据写入完成...")
        time.sleep(3)
        
        # 测试搜索功能
        print("\n" + "=" * 40)
        print("测试搜索功能")
        print("=" * 40)
        
        # 提供一些搜索建议
        print("请输入搜索查询（例如：技能、经验、教育背景等）:")
        query = input("搜索查询: ").strip()
        
        if query:
            test_search(query, collection_name)
        
        # 提供更多搜索示例
        print("\n你也可以尝试这些搜索:")
        example_queries = ["技能", "经验", "教育", "项目", "工作"]
        for example_query in example_queries:
            print(f"\n测试搜索: '{example_query}'")
            test_search(example_query, collection_name, k=2)
    else:
        print("✗ 存储失败，无法进行搜索测试")
    
    print(f"\n测试完成! 集合名称: {collection_name}")
    print("你现在可以在Attu中查看这个集合的数据了。")

if __name__ == "__main__":
    main()
