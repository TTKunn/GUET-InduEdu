#!/usr/bin/env python3
"""
MongoDB实时监控脚本
用于观察简历分析结果
"""

import pymongo
import time
import json
from datetime import datetime
from pprint import pprint

def connect_db():
    """连接数据库"""
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['interview_analysis']
    collection = db['candidate_profiles']
    return collection

def format_datetime(dt):
    """格式化时间"""
    if dt:
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    return 'N/A'

def display_profile(doc):
    """显示档案详情"""
    print("\n" + "="*80)
    print(f"📋 用户档案: {doc.get('user_id')}")
    print("="*80)
    
    # 基本信息
    print(f"📁 文件名: {doc.get('source_filename')}")
    print(f"🕐 创建时间: {format_datetime(doc.get('created_at'))}")
    print(f"🔄 更新时间: {format_datetime(doc.get('updated_at'))}")
    print(f"⚙️  提取模式: {doc.get('extraction_mode')}")
    
    # 个人信息
    personal = doc.get('personal_info', {})
    if personal and any(personal.values()):
        print(f"\n👤 个人信息:")
        if personal.get('name'): print(f"   姓名: {personal.get('name')}")
        if personal.get('phone'): print(f"   电话: {personal.get('phone')}")
        if personal.get('email'): print(f"   邮箱: {personal.get('email')}")
        if personal.get('location'): print(f"   地址: {personal.get('location')}")
        if personal.get('age'): print(f"   年龄: {personal.get('age')}")
        if personal.get('gender'): print(f"   性别: {personal.get('gender')}")
    
    # 关键词统计
    all_keywords = doc.get('extracted_keywords', [])
    tech_keywords = doc.get('technical_keywords', [])
    domain_keywords = doc.get('domain_keywords', [])
    
    print(f"\n🔍 关键词统计:")
    print(f"   总关键词: {len(all_keywords)} 个")
    print(f"   技术关键词: {len(tech_keywords)} 个")
    print(f"   领域关键词: {len(domain_keywords)} 个")
    
    if tech_keywords:
        print(f"\n💻 技术关键词 (前15个):")
        for i, keyword in enumerate(tech_keywords[:15], 1):
            print(f"   {i:2d}. {keyword}")
    
    if domain_keywords:
        print(f"\n🏢 领域关键词 (前10个):")
        for i, keyword in enumerate(domain_keywords[:10], 1):
            print(f"   {i:2d}. {keyword}")
    
    # 教育背景
    education = doc.get('education', [])
    if education:
        print(f"\n🎓 教育背景:")
        for i, edu in enumerate(education, 1):
            print(f"   {i}. {edu.get('school', 'N/A')} - {edu.get('degree', 'N/A')} - {edu.get('major', 'N/A')}")
    
    # 工作经验
    work_exp = doc.get('work_experience', [])
    if work_exp:
        print(f"\n💼 工作经验:")
        for i, work in enumerate(work_exp, 1):
            print(f"   {i}. {work.get('company', 'N/A')} - {work.get('position', 'N/A')}")
            if work.get('duration'):
                print(f"      时间: {work.get('duration')}")
    
    # 项目经验
    projects = doc.get('projects', [])
    if projects:
        print(f"\n🚀 项目经验:")
        for i, proj in enumerate(projects, 1):
            print(f"   {i}. {proj.get('name', 'N/A')}")
            if proj.get('technologies'):
                print(f"      技术: {', '.join(proj.get('technologies', []))}")

def monitor_database():
    """监控数据库变化"""
    collection = connect_db()
    last_count = 0
    
    print("🔍 开始监控MongoDB数据库...")
    print("📊 数据库: interview_analysis")
    print("📋 集合: candidate_profiles")
    print("⏰ 监控间隔: 2秒")
    print("\n按 Ctrl+C 停止监控\n")
    
    try:
        while True:
            current_count = collection.count_documents({})
            
            if current_count != last_count:
                print(f"\n🔔 检测到数据变化! 总档案数: {last_count} → {current_count}")
                
                if current_count > last_count:
                    # 显示新增的档案
                    new_docs = collection.find().sort('created_at', -1).limit(current_count - last_count)
                    for doc in new_docs:
                        display_profile(doc)
                
                last_count = current_count
            else:
                # 显示当前状态
                print(f"⏰ {datetime.now().strftime('%H:%M:%S')} - 当前档案数: {current_count}", end='\r')
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print(f"\n\n✅ 监控结束。最终档案数: {current_count}")

if __name__ == "__main__":
    monitor_database()
