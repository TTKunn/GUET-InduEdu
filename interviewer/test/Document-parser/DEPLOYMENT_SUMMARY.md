# PDF解析器项目部署总结

## 🎉 部署完成状态

✅ **全局Milvus向量数据库** - 已成功部署并运行  
✅ **PDF解析API服务** - 已成功部署并运行  
✅ **Dify适配器服务** - 已成功部署并运行  

## 📋 服务信息

### 1. 全局Milvus向量数据库
- **部署位置**: `/home/ubuntu/tool/milvus`
- **服务端口**: 19530 (Milvus), 9091 (管理), 9000/9001 (MinIO)
- **版本**: Milvus 2.6.0
- **状态**: ✅ 健康运行
- **管理脚本**: `/home/ubuntu/tool/milvus/manage-milvus.sh`

**连接信息**:
```bash
# Milvus连接
Host: localhost
Port: 19530

# MinIO控制台
URL: http://localhost:9001
用户名: minioadmin
密码: minioadmin
```

### 2. PDF解析API服务
- **部署位置**: `/home/ubuntu/workspace/project/Document-parser`
- **服务端口**: 8002
- **状态**: ✅ 健康运行
- **API文档**: http://localhost:8002/docs
- **健康检查**: http://localhost:8002/health

### 3. Dify适配器服务
- **部署位置**: `/home/ubuntu/workspace/project/Document-parser/dify-adapter`
- **服务端口**: 8001
- **状态**: ✅ 健康运行
- **API文档**: http://localhost:8001/docs
- **健康检查**: http://localhost:8001/health

## 🛠️ 管理命令

### 项目服务管理
```bash
cd /home/ubuntu/workspace/project/Document-parser

# 查看服务状态
./manage-services.sh status

# 启动所有服务
./manage-services.sh start

# 停止所有服务
./manage-services.sh stop

# 重启所有服务
./manage-services.sh restart

# 查看日志
./manage-services.sh logs pdf    # PDF API日志
./manage-services.sh logs dify   # Dify适配器日志
```

### 全局Milvus管理
```bash
cd /home/ubuntu/tool/milvus

# 查看Milvus状态
./manage-milvus.sh status

# 启动Milvus
./manage-milvus.sh start

# 停止Milvus
./manage-milvus.sh stop

# 查看连接信息
./manage-milvus.sh info
```

## 🔗 服务访问地址

| 服务 | 地址 | 用途 |
|------|------|------|
| PDF解析API | http://localhost:8002 | PDF文档解析和向量化 |
| PDF解析API文档 | http://localhost:8002/docs | API接口文档 |
| Dify适配器 | http://localhost:8001 | Dify外部知识库接口 |
| Dify适配器文档 | http://localhost:8001/docs | 适配器API文档 |
| Milvus数据库 | localhost:19530 | 向量数据库连接 |
| MinIO控制台 | http://localhost:9001 | 对象存储管理界面 |

## 🔑 API密钥配置

Dify适配器支持多个API密钥，每个密钥对应不同的知识库集合：

```bash
# 默认API密钥
dify-pdf-docs-001      # 对应 pdf_documents 集合
dify-tech-docs-002     # 对应 technical_docs 集合  
dify-company-kb-003    # 对应 company_knowledge 集合
```

## 📁 重要目录结构

```
/home/ubuntu/
├── tool/milvus/                    # 全局Milvus部署
│   ├── docker-compose.yml         # Milvus容器配置
│   ├── manage-milvus.sh           # Milvus管理脚本
│   └── volumes/                   # 数据持久化目录
└── workspace/project/Document-parser/  # PDF解析器项目
    ├── api/                       # PDF解析API
    ├── dify-adapter/             # Dify适配器
    ├── manage-services.sh        # 服务管理脚本
    ├── logs/                     # 日志目录
    └── data/                     # 数据目录
```

## 🚀 使用示例

### 1. 上传PDF文档进行解析
```bash
curl -X POST "http://localhost:8002/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_document.pdf" \
  -F "collection_name=pdf_documents"
```

### 2. 通过Dify适配器检索知识
```bash
curl -X POST "http://localhost:8001/retrieval" \
  -H "Authorization: Bearer dify-pdf-docs-001" \
  -H "Content-Type: application/json" \
  -d '{
    "retrieval": {
      "query": "你的查询问题",
      "top_k": 5
    },
    "dataset": {
      "id": "pdf_documents"
    }
  }'
```

## 🔧 故障排除

### 常见问题

1. **端口冲突**
   - 确保端口 8001, 8002, 19530, 9000, 9001 没有被其他服务占用
   - 使用 `netstat -tlnp | grep <端口>` 检查端口使用情况

2. **服务无法启动**
   - 检查日志文件: `logs/pdf_api.log`, `logs/dify_adapter.log`
   - 确保Python依赖已正确安装
   - 检查全局Milvus是否正常运行

3. **连接Milvus失败**
   - 确保全局Milvus服务正在运行
   - 检查防火墙设置
   - 验证网络连接

### 日志查看
```bash
# 查看PDF API日志
tail -f /home/ubuntu/workspace/project/Document-parser/logs/pdf_api.log

# 查看Dify适配器日志  
tail -f /home/ubuntu/workspace/project/Document-parser/logs/dify_adapter.log

# 查看Milvus日志
cd /home/ubuntu/tool/milvus && sudo docker compose logs -f
```

## 📝 下一步建议

1. **配置API密钥**: 根据实际需求修改 `dify-adapter/config.py` 中的API密钥配置
2. **设置环境变量**: 在 `.env` 文件中配置OpenAI、DeepSeek、智谱AI等API密钥
3. **测试功能**: 上传测试PDF文档，验证解析和检索功能
4. **监控设置**: 考虑添加服务监控和自动重启机制
5. **备份策略**: 定期备份Milvus数据和项目配置

## 🎯 项目特点

- ✅ **全局部署**: Milvus作为全局服务，可被多个项目共享
- ✅ **服务分离**: PDF解析和Dify适配器独立运行，便于维护
- ✅ **健康检查**: 所有服务都提供健康检查接口
- ✅ **日志管理**: 完整的日志记录和管理
- ✅ **脚本管理**: 提供便捷的服务管理脚本
- ✅ **文档完整**: 详细的API文档和使用说明

---

**部署完成时间**: 2025-08-21  
**部署状态**: ✅ 成功  
**维护建议**: 定期检查服务状态，及时更新依赖包
