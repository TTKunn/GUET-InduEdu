#!/usr/bin/env python3
"""
查询分析结果脚本
"""

import pymongo
import json
from pprint import pprint

def query_user_profile(user_id):
    """查询指定用户的档案"""
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['interview_analysis']
    collection = db['candidate_profiles']
    
    profile = collection.find_one({"user_id": user_id})
    
    if profile:
        print(f"✅ 找到用户档案: {user_id}")
        print("\n📄 完整档案数据:")
        print("="*60)
        
        # 移除MongoDB的_id字段以便更好显示
        if '_id' in profile:
            del profile['_id']
        
        # 格式化输出
        print(json.dumps(profile, indent=2, ensure_ascii=False, default=str))
        
        return profile
    else:
        print(f"❌ 未找到用户档案: {user_id}")
        return None

if __name__ == "__main__":
    # 查询测试用户
    query_user_profile("test_user_001")
