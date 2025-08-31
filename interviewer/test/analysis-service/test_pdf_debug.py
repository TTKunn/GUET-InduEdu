#!/usr/bin/env python3
"""
PDF解析调试脚本
"""

from fastapi import UploadFile
from pdf_service import pdf_service
import io

def test_pdf_parsing():
    """测试PDF解析"""
    try:
        # 读取PDF文件
        with open('test_resume.pdf', 'rb') as f:
            pdf_content = f.read()
        
        # 创建UploadFile对象
        file_obj = io.BytesIO(pdf_content)
        upload_file = UploadFile(
            filename="test_resume.pdf",
            file=file_obj
        )
        upload_file.content_type = "application/pdf"
        
        print("开始测试PDF解析...")
        
        # 测试本地解析
        print("\n=== 测试本地解析 ===")
        try:
            result = pdf_service.parse_pdf(upload_file, use_local=True)
            print(f"✅ 本地解析成功")
            print(f"内容长度: {len(result)}")
            print(f"前200字符: {result[:200]}")
        except Exception as e:
            print(f"❌ 本地解析失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 重置文件指针
        file_obj.seek(0)
        
        # 测试Document-parser解析
        print("\n=== 测试Document-parser解析 ===")
        try:
            result = pdf_service.parse_pdf(upload_file, use_local=False)
            print(f"✅ Document-parser解析成功")
            print(f"内容长度: {len(result)}")
            print(f"前200字符: {result[:200]}")
        except Exception as e:
            print(f"❌ Document-parser解析失败: {e}")
            import traceback
            traceback.print_exc()
            
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pdf_parsing()
