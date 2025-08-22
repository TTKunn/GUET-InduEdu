"""
Milvus连接测试脚本
用于诊断Milvus连接问题
"""
import os
import sys
import traceback

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_basic_connection():
    """测试基础的Milvus连接"""
    print("=" * 50)
    print("测试基础Milvus连接")
    print("=" * 50)
    
    try:
        from pymilvus import MilvusClient
        from config import MILVUS_URI, MILVUS_TOKEN
        
        print(f"Milvus URI: {MILVUS_URI}")
        print(f"Milvus Token: {'已设置' if MILVUS_TOKEN else '未设置'}")
        
        # 创建客户端
        print("正在创建Milvus客户端...")
        client = MilvusClient(uri=MILVUS_URI, token=MILVUS_TOKEN if MILVUS_TOKEN else None)
        
        # 测试连接
        print("正在测试连接...")
        collections = client.list_collections()
        print(f"✓ 连接成功! 现有集合数量: {len(collections)}")
        
        if collections:
            print("现有集合:")
            for collection in collections:
                print(f"  - {collection}")
        
        return True, client
        
    except Exception as e:
        print(f"✗ 基础连接失败: {e}")
        print("详细错误信息:")
        traceback.print_exc()
        return False, None

def test_embedding_model():
    """测试嵌入模型"""
    print("\n" + "=" * 50)
    print("测试嵌入模型")
    print("=" * 50)
    
    try:
        from models.embeddings import embedding_manager
        
        print("正在初始化智谱AI嵌入模型...")
        embedding_model = embedding_manager.get_embedding_model("zhipuai")
        
        print("正在测试嵌入生成...")
        test_text = "这是一个测试文本"
        embeddings = embedding_model.embed_query(test_text)
        
        print(f"✓ 嵌入模型测试成功!")
        print(f"  - 测试文本: {test_text}")
        print(f"  - 嵌入维度: {len(embeddings)}")
        print(f"  - 嵌入向量前5个值: {embeddings[:5]}")
        
        return True, embedding_model
        
    except Exception as e:
        print(f"✗ 嵌入模型测试失败: {e}")
        print("详细错误信息:")
        traceback.print_exc()
        return False, None

def test_milvus_vector_store():
    """测试MilvusVectorStore类"""
    print("\n" + "=" * 50)
    print("测试MilvusVectorStore类")
    print("=" * 50)
    
    try:
        from database.milvus_client import MilvusVectorStore
        
        # 创建测试集合名称
        test_collection = "connection_test_collection"
        print(f"创建MilvusVectorStore实例，集合名称: {test_collection}")
        
        vector_store = MilvusVectorStore(
            collection_name=test_collection,
            embedding_model_type="zhipuai"
        )
        
        print("正在测试连接...")
        if vector_store.create_connection():
            print("✓ MilvusVectorStore连接成功!")
            
            print("正在测试集合创建...")
            if vector_store.create_collection_if_not_exists():
                print("✓ 集合创建成功!")
                
                # 获取集合信息
                info = vector_store.get_collection_info()
                print(f"集合信息: {info}")
                
                return True
            else:
                print("✗ 集合创建失败")
                return False
        else:
            print("✗ MilvusVectorStore连接失败")
            return False
            
    except Exception as e:
        print(f"✗ MilvusVectorStore测试失败: {e}")
        print("详细错误信息:")
        traceback.print_exc()
        return False

def check_milvus_service():
    """检查Milvus服务是否运行"""
    print("=" * 50)
    print("检查Milvus服务状态")
    print("=" * 50)
    
    try:
        import requests
        from config import MILVUS_URI
        
        # 尝试访问Milvus健康检查端点
        # Milvus通常在19530端口提供gRPC服务，但也可能有HTTP端点
        print(f"检查Milvus服务: {MILVUS_URI}")
        
        # 解析URI获取主机和端口
        if MILVUS_URI.startswith('http://'):
            host_port = MILVUS_URI[7:]  # 移除 'http://'
        else:
            host_port = MILVUS_URI
        
        if ':' in host_port:
            host, port = host_port.split(':')
        else:
            host, port = host_port, '19530'
        
        print(f"主机: {host}, 端口: {port}")
        
        # 尝试简单的TCP连接测试
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, int(port)))
        sock.close()
        
        if result == 0:
            print("✓ Milvus服务端口可访问")
            return True
        else:
            print(f"✗ 无法连接到Milvus服务端口 {host}:{port}")
            print("请检查:")
            print("1. Milvus服务是否已启动")
            print("2. 端口配置是否正确")
            print("3. 防火墙设置")
            return False
            
    except Exception as e:
        print(f"✗ 服务检查失败: {e}")
        return False

def main():
    """主测试函数"""
    print("Milvus连接诊断工具")
    print("=" * 60)
    
    # 1. 检查Milvus服务
    if not check_milvus_service():
        print("\n❌ Milvus服务不可访问，请先启动Milvus服务")
        return
    
    # 2. 测试基础连接
    success, client = test_basic_connection()
    if not success:
        print("\n❌ 基础连接失败")
        return
    
    # 3. 测试嵌入模型
    success, embedding_model = test_embedding_model()
    if not success:
        print("\n❌ 嵌入模型测试失败")
        return
    
    # 4. 测试MilvusVectorStore
    if test_milvus_vector_store():
        print("\n✅ 所有测试通过! Milvus连接正常")
        print("\n现在你可以运行 test_milvus_storage.py 来测试PDF存储功能了")
    else:
        print("\n❌ MilvusVectorStore测试失败")

if __name__ == "__main__":
    main()
