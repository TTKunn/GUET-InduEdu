"""
智谱AI API测试脚本
用于诊断智谱AI API连接问题
"""
import os
import sys
import traceback

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_zhipuai_direct():
    """直接测试智谱AI API"""
    print("=" * 50)
    print("直接测试智谱AI API")
    print("=" * 50)
    
    try:
        from config import ZHIPUAI_API_KEY, ZHIPUAI_EMBEDDING_MODEL
        
        print(f"API Key: {ZHIPUAI_API_KEY[:10]}...{ZHIPUAI_API_KEY[-10:] if len(ZHIPUAI_API_KEY) > 20 else ZHIPUAI_API_KEY}")
        print(f"模型: {ZHIPUAI_EMBEDDING_MODEL}")
        
        # 直接使用zhipuai库测试
        from zhipuai import ZhipuAI
        
        print("正在创建ZhipuAI客户端...")
        client = ZhipuAI(api_key=ZHIPUAI_API_KEY)
        
        print("正在测试嵌入API...")
        response = client.embeddings.create(
            model=ZHIPUAI_EMBEDDING_MODEL,
            input="测试文本"
        )
        
        print("✓ 智谱AI API测试成功!")
        print(f"  - 响应数据长度: {len(response.data)}")
        print(f"  - 嵌入维度: {len(response.data[0].embedding)}")
        print(f"  - 前5个嵌入值: {response.data[0].embedding[:5]}")
        
        return True
        
    except Exception as e:
        print(f"✗ 智谱AI API测试失败: {e}")
        print("详细错误信息:")
        traceback.print_exc()
        return False

def test_different_models():
    """测试不同的智谱AI嵌入模型"""
    print("\n" + "=" * 50)
    print("测试不同的智谱AI嵌入模型")
    print("=" * 50)
    
    try:
        from config import ZHIPUAI_API_KEY
        from zhipuai import ZhipuAI
        
        client = ZhipuAI(api_key=ZHIPUAI_API_KEY)
        
        # 尝试不同的模型
        models_to_test = [
            "embedding-2",
            "embedding-3", 
            "text-embedding-3-small",
            "text-embedding-3-large"
        ]
        
        for model in models_to_test:
            print(f"\n测试模型: {model}")
            try:
                response = client.embeddings.create(
                    model=model,
                    input="测试文本"
                )
                print(f"✓ 模型 {model} 可用，嵌入维度: {len(response.data[0].embedding)}")
            except Exception as e:
                print(f"✗ 模型 {model} 不可用: {e}")
        
        return True
        
    except Exception as e:
        print(f"✗ 模型测试失败: {e}")
        return False

def test_api_key_format():
    """检查API密钥格式"""
    print("\n" + "=" * 50)
    print("检查API密钥格式")
    print("=" * 50)
    
    try:
        from config import ZHIPUAI_API_KEY
        
        print(f"API Key长度: {len(ZHIPUAI_API_KEY)}")
        print(f"API Key前缀: {ZHIPUAI_API_KEY[:10]}")
        print(f"API Key是否以sk-开头: {'是' if ZHIPUAI_API_KEY.startswith('sk-') else '否'}")
        
        # 检查是否包含特殊字符
        import string
        valid_chars = string.ascii_letters + string.digits + '-_'
        invalid_chars = [c for c in ZHIPUAI_API_KEY if c not in valid_chars]
        
        if invalid_chars:
            print(f"⚠️  API Key包含可能的无效字符: {set(invalid_chars)}")
        else:
            print("✓ API Key格式看起来正常")
        
        return True
        
    except Exception as e:
        print(f"✗ API密钥检查失败: {e}")
        return False

def test_network_connectivity():
    """测试网络连接"""
    print("\n" + "=" * 50)
    print("测试网络连接")
    print("=" * 50)
    
    try:
        import requests
        
        # 测试智谱AI API端点
        api_url = "https://open.bigmodel.cn"
        print(f"测试连接到: {api_url}")
        
        response = requests.get(api_url, timeout=10)
        print(f"✓ 网络连接正常，状态码: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"✗ 网络连接测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("智谱AI API诊断工具")
    print("=" * 60)
    
    # 1. 检查API密钥格式
    test_api_key_format()
    
    # 2. 测试网络连接
    test_network_connectivity()
    
    # 3. 直接测试API
    if test_zhipuai_direct():
        print("\n✅ 智谱AI API工作正常!")
    else:
        print("\n❌ 智谱AI API有问题")
        
        # 4. 测试不同模型
        print("\n尝试测试其他模型...")
        test_different_models()
    
    print("\n" + "=" * 60)
    print("诊断完成")
    print("=" * 60)
    
    print("\n可能的解决方案:")
    print("1. 检查智谱AI API密钥是否正确")
    print("2. 确认API密钥是否有足够的余额")
    print("3. 检查API密钥是否有嵌入模型的使用权限")
    print("4. 尝试重新生成API密钥")
    print("5. 如果问题持续，可以临时使用BGE本地模型")

if __name__ == "__main__":
    main()
