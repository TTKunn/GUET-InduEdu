#!/usr/bin/env python3
"""
检查所有微服务的运行状态
"""

import requests
import json
from datetime import datetime

def check_service(port, service_name, has_health=True):
    """检查单个服务状态"""
    try:
        if has_health:
            url = f"http://localhost:{port}/health"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                result = response.json()
                status = result.get('status', 'unknown')
                print(f"✅ {service_name} (端口{port}): {status}")
                return True
            else:
                print(f"❌ {service_name} (端口{port}): HTTP {response.status_code}")
                return False
        else:
            # 对于没有health接口的服务，检查根路径
            url = f"http://localhost:{port}/"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {service_name} (端口{port}): 运行正常")
                return True
            else:
                print(f"❌ {service_name} (端口{port}): HTTP {response.status_code}")
                return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {service_name} (端口{port}): 连接失败")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ {service_name} (端口{port}): 请求超时")
        return False
    except Exception as e:
        print(f"❌ {service_name} (端口{port}): {str(e)}")
        return False

def main():
    """主检查函数"""
    print("=" * 60)
    print("AI智能面试官项目 - 服务状态检查")
    print("=" * 60)
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    services = [
        (8000, "统一API文档服务", False),  # 可能没有health接口
        (8003, "PDF解析服务", True),
        (8004, "简历分析服务", True),
        (8005, "向量存储服务", True),
        (8006, "面试记录服务", True),
        (8007, "用户认证服务", True),
    ]
    
    success_count = 0
    total_count = len(services)
    
    for port, name, has_health in services:
        if check_service(port, name, has_health):
            success_count += 1
    
    print()
    print("=" * 60)
    print(f"检查结果: {success_count}/{total_count} 服务运行正常")
    
    if success_count == total_count:
        print("🎉 所有服务运行正常！")
    else:
        print("⚠️  部分服务未正常运行")
    
    print("=" * 60)
    
    # 显示服务访问地址
    print("\n📋 服务访问地址:")
    print("- 统一API文档: http://43.142.157.145:8000/docs")
    print("- PDF解析服务: http://43.142.157.145:8003/docs")
    print("- 简历分析服务: http://43.142.157.145:8004/docs")
    print("- 向量存储服务: http://43.142.157.145:8005/docs")
    print("- 面试记录服务: http://43.142.157.145:8006/docs")
    print("- 用户认证服务: http://43.142.157.145:8007/docs")

if __name__ == "__main__":
    main()
