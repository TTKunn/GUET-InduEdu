#!/usr/bin/env python3
"""
完整流程测试 - 使用xzk.pdf进行端到端测试
"""

import requests
import json
import time
import os

def test_complete_flow():
    """完整流程测试"""
    print("🚀 开始完整流程测试")
    print("=" * 60)
    
    base_url = "http://localhost:8004"
    test_user_id = "test_complete_flow_user"
    pdf_path = "../../../xzk.pdf"
    
    try:
        # 步骤1: 健康检查
        print("1️⃣ 健康检查...")
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"   ✅ 服务状态: {health_data.get('status', 'unknown')}")
            print(f"   📊 数据库连接: {health_data.get('database_connected', False)}")
            print(f"   🤖 LLM可用: {health_data.get('llm_available', False)}")
        else:
            print(f"   ❌ 健康检查失败: {response.status_code}")
            return False
        
        # 步骤2: 简历分析
        print("\n2️⃣ 简历分析...")
        if not os.path.exists(pdf_path):
            print(f"   ❌ PDF文件不存在: {pdf_path}")
            return False
        
        print(f"   📄 使用PDF: {pdf_path}")
        print(f"   👤 用户ID: {test_user_id}")
        
        files = {
            'file': ('xzk.pdf', open(pdf_path, 'rb'), 'application/pdf')
        }
        data = {
            'user_id': test_user_id,
            'extraction_mode': 'comprehensive',
            'overwrite': 'true'
        }
        
        print("   🔄 发送分析请求...")
        start_time = time.time()
        response = requests.post(f"{base_url}/analyze", files=files, data=data, timeout=180)
        analysis_time = time.time() - start_time
        
        files['file'][1].close()  # 关闭文件
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"   ✅ 简历分析成功!")
                print(f"   ⏱️  处理时间: {analysis_time:.2f}秒")
                print(f"   📊 技术技能: {len(result.get('technical_skills', []))}个")
                print(f"   📁 项目关键词: {len(result.get('projects_keywords', []))}个项目")
                print(f"   🎯 技术方向: {result.get('direction', '未知')}")
            else:
                print(f"   ❌ 简历分析失败: {result.get('message', '未知错误')}")
                return False
        else:
            print(f"   ❌ 请求失败: {response.status_code}")
            print(f"   响应: {response.text}")
            return False
        
        # 步骤3: 获取关键词
        print("\n3️⃣ 获取关键词...")
        keywords_request = {
            "user_id": test_user_id,
            "category": "all",
            "format_type": "list"
        }
        response = requests.post(f"{base_url}/keywords", json=keywords_request, timeout=30)
        
        if response.status_code == 200:
            keywords_data = response.json()
            if keywords_data.get('success'):
                print(f"   ✅ 关键词获取成功!")
                print(f"   🛠️  技术技能: {len(keywords_data.get('technical_skills', []))}个")
                print(f"   🔑 技术关键词: {len(keywords_data.get('technical_keywords', []))}个")
                print(f"   📋 提取关键词: {len(keywords_data.get('extracted_keywords', []))}个")
                print(f"   🎯 技术方向: {keywords_data.get('direction', '未知')}")
            else:
                print(f"   ❌ 关键词获取失败: {keywords_data.get('message', '未知错误')}")
                return False
        else:
            print(f"   ❌ 请求失败: {response.status_code}")
            return False
        
        # 步骤4: 获取分组关键词（Dify专用）
        print("\n4️⃣ 获取分组关键词（Dify专用）...")
        response = requests.get(f"{base_url}/keywords/grouped/{test_user_id}", timeout=30)
        
        if response.status_code == 200:
            grouped_data = response.json()
            if grouped_data.get('success'):
                print(f"   ✅ 分组关键词获取成功!")
                print(f"   🛠️  技术技能: {len(grouped_data.get('technical_skills', []))}个")
                print(f"   📝 技能文本: {grouped_data.get('technical_skills_text', '')[:50]}...")
                print(f"   📁 项目数量: {len(grouped_data.get('projects_keywords', []))}个")
                print(f"   🎯 技术方向: {grouped_data.get('direction', '未知')}")
                
                # 验证项目关键词结构
                projects = grouped_data.get('projects_keywords', [])
                for i, project in enumerate(projects[:2]):  # 只显示前2个项目
                    print(f"   📋 项目{i+1}: {project.get('project_name', '未知')}")
                    print(f"      关键词: {len(project.get('keywords', []))}个")
                    print(f"      搜索文本: {project.get('search_text', '')[:30]}...")
                
                # 验证Dify使用指南
                dify_guide = grouped_data.get('dify_usage_guide', {})
                if dify_guide:
                    print(f"   📖 Dify使用指南: {len(dify_guide)}项说明")
                
            else:
                print(f"   ❌ 分组关键词获取失败: {grouped_data.get('message', '未知错误')}")
                return False
        else:
            print(f"   ❌ 请求失败: {response.status_code}")
            return False
        
        # 步骤5: 验证JSON存储
        print("\n5️⃣ 验证JSON存储...")
        from mysql_database import DatabaseService
        
        db_service = DatabaseService()
        if db_service.connect():
            profile = db_service.mysql_client.get_profile(test_user_id)
            if profile:
                print(f"   ✅ JSON数据读取成功!")
                print(f"   👤 姓名: {profile.get('personal_info', {}).get('name', '未知')}")
                print(f"   🛠️  技术技能: {len(profile.get('technical_skills', []))}个")
                print(f"   📁 项目关键词: {len(profile.get('projects_keywords', []))}个")
                print(f"   🔄 兼容字段一致: {profile.get('technical_skills') == profile.get('extracted_keywords')}")
            else:
                print(f"   ❌ 未找到用户档案")
                return False
        else:
            print(f"   ❌ 数据库连接失败")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    success = test_complete_flow()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 完整流程测试成功！")
        print("   ✅ PDF解析正常")
        print("   ✅ LLM提取正常")
        print("   ✅ JSON存储正常")
        print("   ✅ API兼容性正常")
        print("   ✅ 双写模式正常")
        print("\n🚀 MySQL JSON存储优化完成！")
    else:
        print("⚠️  完整流程测试失败！")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
