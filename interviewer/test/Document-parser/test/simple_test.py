"""
简单的PDF解析API测试脚本
直接指定PDF文件路径进行测试
"""
import os
import requests
import json

# API基础URL
API_BASE_URL = "http://localhost:8000"

def simple_pdf_test(pdf_path):
    """
    简单的PDF解析测试
    
    Args:
        pdf_path: PDF文件的完整路径
    """
    print(f"开始测试PDF文件: {pdf_path}")
    
    # 检查文件是否存在
    if not os.path.exists(pdf_path):
        print(f"错误: 文件不存在 - {pdf_path}")
        return False
    
    try:
        # 1. 先测试健康检查
        print("1. 测试API健康状态...")
        health_response = requests.get(f"{API_BASE_URL}/health")
        if health_response.status_code != 200:
            print(f"API服务异常: {health_response.status_code}")
            return False
        print("✓ API服务正常")
        
        # 2. 测试PDF解析
        print("2. 开始解析PDF...")
        with open(pdf_path, 'rb') as f:
            files = {'file': (os.path.basename(pdf_path), f, 'application/pdf')}
            params = {
                'chunk_size': 1000,
                'chunk_overlap': 200,
                'split_text': True,
                'return_content': True  # 返回解析内容以便查看
            }
            
            response = requests.post(
                f"{API_BASE_URL}/parse",
                files=files,
                params=params
            )
        
        if response.status_code == 200:
            result = response.json()
            print("✓ PDF解析成功!")
            print(f"  - 任务ID: {result['task_id']}")
            print(f"  - 文档片段数: {result['total_documents']}")
            print(f"  - 总字符数: {result['total_chars']}")
            
            # 显示前几个文档片段
            if 'documents' in result and result['documents']:
                print(f"  - 解析出 {len(result['documents'])} 个文档片段")
                print("\n前3个文档片段预览:")
                for i, doc in enumerate(result['documents'][:3]):
                    print(f"\n--- 片段 {i+1} ---")
                    print(f"长度: {doc['content_length']} 字符")
                    print(f"内容: {doc['content'][:150]}...")
                    if doc['metadata']:
                        print(f"元数据: {json.dumps(doc['metadata'], ensure_ascii=False)}")
            
            return True
        else:
            print(f"✗ PDF解析失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ 测试过程中出现错误: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("PDF解析API简单测试")
    print("=" * 60)
    
    # 在这里直接指定你的PDF文件路径
    # 你可以修改下面的路径为你实际的PDF文件路径
    pdf_paths = [
        # 示例路径，请修改为你的实际PDF文件路径
        r"E:\Code\project\PDF_ANALYSER\examples\sample.pdf",
        r"C:\Users\YourName\Documents\test.pdf",
        # 添加更多PDF文件路径...
    ]
    
    # 或者让用户输入路径
    print("请输入PDF文件的完整路径:")
    user_path = input("PDF路径: ").strip().strip('"').strip("'")
    
    if user_path:
        pdf_paths = [user_path]
    
    # 测试每个PDF文件
    for pdf_path in pdf_paths:
        if os.path.exists(pdf_path):
            print(f"\n测试文件: {pdf_path}")
            if simple_pdf_test(pdf_path):
                print("✓ 测试成功!")
            else:
                print("✗ 测试失败!")
            break
        else:
            print(f"文件不存在: {pdf_path}")
    else:
        print("没有找到有效的PDF文件进行测试")
        print("请确保:")
        print("1. PDF文件路径正确")
        print("2. 文件确实存在")
        print("3. 文件是有效的PDF格式")

if __name__ == "__main__":
    main()
