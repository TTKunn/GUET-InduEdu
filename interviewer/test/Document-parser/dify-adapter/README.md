# Dify外部知识库适配器

这是一个适配器服务，用于将PDF解析系统集成到Dify工作流平台中。

## 🚀 快速启动

### 1. 环境准备
```bash
# 激活PDF_ANALYSER conda环境
conda activate PDF_ANALYSER

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量
```bash
# 复制配置文件
cp .env.example .env

# 编辑配置文件
# 修改 PDF_PARSER_API_URL 为你的PDF解析API地址
```

### 3. 启动服务
```bash
# 方式1：使用启动脚本（推荐）
python start_adapter.py

# 方式2：直接使用uvicorn
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### 4. 验证服务
```bash
# 健康检查
curl http://localhost:8001/health

# 查看API文档
# 浏览器访问: http://localhost:8001/docs
```

## 📋 API端点

- `POST /retrieval` - Dify外部知识库检索接口
- `GET /health` - 健康检查
- `GET /stats` - 服务统计信息
- `GET /docs` - API文档

## 🔑 API Key配置

在 `config.py` 中配置API Key映射：

```python
API_KEY_MAPPING = {
    "your-api-key": {
        "collection": "pdf_documents",
        "permissions": ["read"],
        "rate_limit": 100
    }
}
```

## 🔧 在Dify中配置

1. 登录Dify工作台
2. 进入知识库管理
3. 选择"连接外部知识库"
4. 填写配置：
   - API端点: `http://your-server:8001/retrieval`
   - API Key: `your-api-key`
   - 知识库ID: `pdf_documents`

## 📊 监控和调试

- 查看日志文件: `dify_adapter.log`
- 访问统计信息: `GET /stats`
- 健康检查: `GET /health`
