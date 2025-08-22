"""
PDF解析API使用示例
演示如何在项目中调用PDF解析服务
"""
from api.client import PDFAnalyserClient, parse_pdf_file, parse_and_store_pdf_file, search_pdf_documents

def example_basic_usage():
    """基础使用示例"""
    print("=== 基础使用示例 ===")
    
    # 创建客户端
    client = PDFAnalyserClient("http://localhost:8000")
    
    # 健康检查
    health = client.health_check()
    print(f"服务状态: {health}")
    
    # 解析PDF文件
    pdf_path = "./data/sample.pdf"  # 替换为实际PDF文件路径
    
    result = client.parse_pdf(
        pdf_path=pdf_path,
        chunk_size=1000,
        chunk_overlap=200,
        split_text=True,
        return_content=False  # 不返回内容，只返回统计信息
    )
    
    print(f"解析结果: {result}")

def example_with_storage():
    """解析并存储示例"""
    print("=== 解析并存储示例 ===")
    
    client = PDFAnalyserClient("http://localhost:8000")
    
    # 解析并存储到Milvus
    pdf_path = "./data/sample.pdf"
    
    result = client.parse_and_store_pdf(
        pdf_path=pdf_path,
        collection_name="my_documents",
        chunk_size=800,
        chunk_overlap=100,
        embedding_model="bge"
    )
    
    print(f"解析存储结果: {result}")
    
    # 搜索文档
    if result.get("success"):
        search_result = client.search_documents(
            query="文档主要内容",
            collection_name="my_documents",
            k=3
        )
        print(f"搜索结果: {search_result}")

def example_convenience_functions():
    """便捷函数使用示例"""
    print("=== 便捷函数示例 ===")
    
    # 使用便捷函数解析PDF
    result = parse_pdf_file(
        pdf_path="./data/sample.pdf",
        api_url="http://localhost:8000",
        chunk_size=500,
        return_content=True
    )
    
    print(f"便捷解析结果: {result}")
    
    # 使用便捷函数解析并存储
    store_result = parse_and_store_pdf_file(
        pdf_path="./data/sample.pdf",
        api_url="http://localhost:8000",
        collection_name="test_docs"
    )
    
    print(f"便捷存储结果: {store_result}")
    
    # 使用便捷函数搜索
    search_result = search_pdf_documents(
        query="测试查询",
        api_url="http://localhost:8000",
        collection_name="test_docs",
        k=2
    )
    
    print(f"便捷搜索结果: {search_result}")

def example_batch_processing():
    """批量处理示例"""
    print("=== 批量处理示例 ===")
    
    import os
    from pathlib import Path
    
    client = PDFAnalyserClient("http://localhost:8000")
    
    # 批量处理目录下的所有PDF文件
    pdf_directory = "./data"
    pdf_files = [f for f in os.listdir(pdf_directory) if f.lower().endswith('.pdf')]
    
    print(f"找到 {len(pdf_files)} 个PDF文件")
    
    results = []
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_directory, pdf_file)
        print(f"处理文件: {pdf_file}")
        
        # 解析并存储
        result = client.parse_and_store_pdf(
            pdf_path=pdf_path,
            collection_name="batch_docs",
            chunk_size=1000
        )
        
        results.append({
            "file": pdf_file,
            "success": result.get("success", False),
            "message": result.get("message", ""),
            "total_documents": result.get("total_documents", 0)
        })
    
    # 统计结果
    successful = len([r for r in results if r["success"]])
    total_docs = sum(r["total_documents"] for r in results if r["success"])
    
    print(f"批量处理完成: {successful}/{len(pdf_files)} 成功, 总文档数: {total_docs}")

def example_error_handling():
    """错误处理示例"""
    print("=== 错误处理示例 ===")
    
    client = PDFAnalyserClient("http://localhost:8000")
    
    # 尝试解析不存在的文件
    result = client.parse_pdf("./nonexistent.pdf")
    
    if not result.get("success"):
        print(f"预期的错误: {result.get('message')}")
    
    # 尝试连接不存在的服务
    client_bad = PDFAnalyserClient("http://localhost:9999")
    health = client_bad.health_check()
    
    if health.get("status") == "error":
        print(f"连接错误: {health.get('message')}")

if __name__ == "__main__":
    print("PDF解析API使用示例")
    print("请确保API服务已启动: python start_api.py")
    print("=" * 50)
    
    try:
        # 运行示例
        example_basic_usage()
        print("\n" + "=" * 50 + "\n")
        
        # example_with_storage()
        # print("\n" + "=" * 50 + "\n")
        
        example_convenience_functions()
        print("\n" + "=" * 50 + "\n")
        
        # example_batch_processing()
        # print("\n" + "=" * 50 + "\n")
        
        example_error_handling()
        
    except Exception as e:
        print(f"示例运行失败: {e}")
        print("请检查API服务是否正常运行")
