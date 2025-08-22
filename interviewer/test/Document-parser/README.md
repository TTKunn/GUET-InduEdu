# PDF_ANALYSER API

一个基于FastAPI的PDF文档解析服务，提供REST API接口用于PDF文档解析和向量存储。

## 功能特性

- � **REST API服务**: 基于FastAPI的高性能API接口
- 🔍 **PDF解析**: 使用PyPDFLoader进行PDF文档解析
- 📝 **智能文本分块**: 支持可配置的文本分块策略
- 🗄️ **向量存储**: 集成Milvus向量数据库存储和检索
- 🤖 **嵌入模型**: 支持BGE嵌入模型
- 🔧 **客户端SDK**: 提供Python客户端便于集成
- 📊 **日志系统**: 完整的API请求日志记录
- ⚙️ **配置化设计**: 环境变量配置，易于部署

## 项目结构

```
PDF_ANALYSER/
├── config.py              # 配置文件
├── requirements.txt       # 依赖包列表
├── start_api.py           # API服务启动脚本
├── example_usage.py       # 使用示例
├── README.md             # 项目说明
├── zhipuai_setup.md      # 智谱AI配置说明
├── Dockerfile            # Docker构建文件
├── __init__.py           # 包初始化文件
├── api/                  # API模块
│   ├── __init__.py
│   ├── main.py           # FastAPI应用主文件
│   └── client.py         # Python客户端SDK
├── utils/                # 工具模块
│   ├── __init__.py
│   └── log_utils.py      # 日志工具
├── models/               # 模型模块
│   ├── __init__.py
│   └── embeddings.py     # 嵌入模型封装
├── parsers/              # 解析器模块
│   ├── __init__.py
│   └── pdf_parser.py     # PDF解析器
├── database/             # 数据库模块
│   ├── __init__.py
│   └── milvus_client.py  # Milvus向量数据库客户端
├── test/                 # 测试模块
│   ├── __init__.py
│   ├── README.md         # 测试说明文档
│   ├── simple_test.py    # 简单功能测试
│   ├── test_api.py       # API接口测试
│   ├── test_milvus_connection.py    # Milvus连接测试
│   ├── test_milvus_storage.py       # Milvus存储测试
│   └── test_zhipuai_api.py          # 智谱AI API测试
└── logs/                 # 应用日志目录
    └── pdf_analyser.log  # 主要日志文件
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并填入配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置必要的参数：

```env
# Milvus数据库配置
MILVUS_URI=http://localhost:19530
COLLECTION_NAME=pdf_documents

# 智谱AI配置（推荐）
ZHIPUAI_API_KEY=your_zhipuai_api_key_here
ZHIPUAI_EMBEDDING_MODEL=embedding-2
DEFAULT_EMBEDDING_MODEL=zhipuai

# BGE嵌入模型配置（可选）
BGE_MODEL_NAME=BAAI/bge-small-zh-v1.5
BGE_DEVICE=cpu
```

### 3. 启动API服务

```bash
python start_api.py
```

服务启动后，API文档可在以下地址访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 4. 使用API

#### 方式一：HTTP请求

```bash
# 解析PDF文件
curl -X POST "http://localhost:8000/parse" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_file.pdf" \
  -F "chunk_size=1000" \
  -F "split_text=true"

# 搜索文档（需要先存储）
curl -X GET "http://localhost:8000/search?query=你的查询&k=5"
```

#### 方式二：Python客户端

```python
from api.client import PDFAnalyserClient

# 创建客户端
client = PDFAnalyserClient("http://localhost:8000")

# 解析PDF
result = client.parse_pdf("path/to/your.pdf")
print(result)

# 解析并存储到Milvus
result = client.parse_and_store_pdf("path/to/your.pdf")

# 搜索文档
search_result = client.search_documents("查询内容")
```

## API接口文档

### 基础信息

- **Base URL**: `http://localhost:8000`
- **Content-Type**: `application/json` (除文件上传接口)
- **API文档**:
  - Swagger UI: http://localhost:8000/docs
  - ReDoc: http://localhost:8000/redoc

### 接口概览

| 接口 | 方法 | 功能 | 说明 |
|------|------|------|------|
| `/` | GET | 根路径 | 服务状态检查 |
| `/health` | GET | 健康检查 | 详细的服务状态信息 |
| `/parse` | POST | PDF解析 | 解析PDF文件，返回文档内容 |
| `/parse-and-store` | POST | 解析并存储 | 解析PDF并存储到向量数据库 |
| `/search` | GET | 语义搜索 | 在向量数据库中搜索相关文档 |

---

### 1. 健康检查

#### `GET /health`

检查API服务状态。

**请求示例：**
```bash
curl -X GET "http://localhost:8000/health"
```

**响应示例：**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "message": "服务运行正常"
}
```

**响应字段：**
- `status`: 服务状态 (`healthy` | `unhealthy`)
- `version`: API版本号
- `message`: 状态描述信息

---

### 2. PDF解析

#### `POST /parse`

解析PDF文件，提取文本内容并进行分块处理。

**请求参数：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `file` | File | ✅ | - | PDF文件 (multipart/form-data) |
| `chunk_size` | int | ❌ | 1000 | 文档分块大小（字符数） |
| `chunk_overlap` | int | ❌ | 200 | 分块重叠大小（字符数） |
| `split_text` | bool | ❌ | true | 是否进行文本分块 |
| `return_content` | bool | ❌ | false | 是否在响应中返回解析内容 |

**请求示例：**
```bash
curl -X POST "http://localhost:8000/parse" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/document.pdf" \
  -F "chunk_size=1000" \
  -F "chunk_overlap=200" \
  -F "split_text=true" \
  -F "return_content=true"
```

**响应示例：**
```json
{
  "success": true,
  "message": "PDF解析成功",
  "task_id": "12345678-1234-1234-1234-123456789abc",
  "total_documents": 15,
  "total_chars": 12500,
  "documents": [
    {
      "content": "这是文档的第一段内容...",
      "metadata": {
        "page": 0,
        "source": "document.pdf",
        "chunk_id": 0
      },
      "content_length": 850
    }
  ]
}
```

**响应字段：**
- `success`: 操作是否成功
- `message`: 操作结果描述
- `task_id`: 任务唯一标识符
- `total_documents`: 解析出的文档片段总数
- `total_chars`: 文档总字符数
- `documents`: 文档片段列表（仅当`return_content=true`时返回）

---

### 3. 解析并存储

#### `POST /parse-and-store`

解析PDF文件并将结果存储到Milvus向量数据库中，支持后续的语义搜索。

**请求参数：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `file` | File | ✅ | - | PDF文件 (multipart/form-data) |
| `collection_name` | string | ❌ | pdf_documents | Milvus集合名称 |
| `chunk_size` | int | ❌ | 1000 | 文档分块大小 |
| `chunk_overlap` | int | ❌ | 200 | 分块重叠大小 |
| `embedding_model` | string | ❌ | zhipuai | 嵌入模型类型 (`zhipuai` \| `bge` \| `openai`) |

**请求示例：**
```bash
curl -X POST "http://localhost:8000/parse-and-store" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/document.pdf" \
  -F "collection_name=my_documents" \
  -F "chunk_size=1000" \
  -F "embedding_model=zhipuai"
```

**响应示例：**
```json
{
  "success": true,
  "message": "PDF解析并存储成功",
  "task_id": "87654321-4321-4321-4321-123456789def",
  "total_documents": 20,
  "total_chars": 15800
}
```

**响应字段：**
- `success`: 操作是否成功
- `message`: 操作结果描述
- `task_id`: 任务唯一标识符
- `total_documents`: 存储的文档片段数量
- `total_chars`: 文档总字符数

---

### 4. 语义搜索

#### `GET /search`

在向量数据库中进行语义搜索，找到与查询最相关的文档片段。

**请求参数：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `query` | string | ✅ | - | 搜索查询文本 |
| `collection_name` | string | ❌ | pdf_documents | Milvus集合名称 |
| `k` | int | ❌ | 5 | 返回结果数量 |
| `embedding_model` | string | ❌ | zhipuai | 嵌入模型类型 |

**请求示例：**
```bash
curl -X GET "http://localhost:8000/search?query=高并发网络编程&collection_name=my_documents&k=3"
```

**响应示例：**
```json
{
  "success": true,
  "message": "搜索完成",
  "total_results": 3,
  "results": [
    {
      "content": "高并发网络模型：基于MuduoReactor网络模型实现网络层...",
      "metadata": {
        "source_filename": "resume.pdf",
        "page": 1,
        "task_id": "12345678-1234-1234-1234-123456789abc"
      },
      "similarity_score": 1.3070,
      "content_length": 987
    },
    {
      "content": "熟悉常见的网络通信协议，如：TCP、UDP、HTTP等...",
      "metadata": {
        "source_filename": "resume.pdf",
        "page": 0,
        "task_id": "12345678-1234-1234-1234-123456789abc"
      },
      "similarity_score": 1.4975,
      "content_length": 459
    }
  ]
}
```

**响应字段：**
- `success`: 操作是否成功
- `message`: 操作结果描述
- `total_results`: 返回的结果数量
- `results`: 搜索结果列表
  - `content`: 文档片段内容
  - `metadata`: 文档元数据信息
  - `similarity_score`: 相似度分数（越小越相似）
  - `content_length`: 内容长度

**相似度分数说明：**
- `1.0-1.5`: 高度相关
- `1.5-2.0`: 中等相关
- `2.0+`: 低相关

---

### 错误处理

所有接口在出错时都会返回统一的错误格式：

```json
{
  "detail": "错误描述信息"
}
```

**常见错误码：**

| HTTP状态码 | 错误类型 | 说明 |
|------------|----------|------|
| 400 | Bad Request | 请求参数错误 |
| 500 | Internal Server Error | 服务器内部错误 |

**错误示例：**

```bash
# 文件格式错误
curl -X POST "http://localhost:8000/parse" -F "file=@document.txt"
```

```json
{
  "detail": "只支持PDF文件"
}
```

```bash
# Milvus连接失败
curl -X POST "http://localhost:8000/parse-and-store" -F "file=@document.pdf"
```

```json
{
  "detail": "PDF解析并存储失败: 无法连接到Milvus数据库"
}
```

---

### 使用示例

#### Python示例

```python
import requests

# 1. 健康检查
response = requests.get("http://localhost:8000/health")
print(response.json())

# 2. 解析PDF文件
with open("document.pdf", "rb") as f:
    files = {"file": ("document.pdf", f, "application/pdf")}
    params = {
        "chunk_size": 1000,
        "chunk_overlap": 200,
        "return_content": True
    }
    response = requests.post(
        "http://localhost:8000/parse",
        files=files,
        params=params
    )
    result = response.json()
    print(f"解析成功，共{result['total_documents']}个文档片段")

# 3. 解析并存储到向量数据库
with open("document.pdf", "rb") as f:
    files = {"file": ("document.pdf", f, "application/pdf")}
    params = {
        "collection_name": "my_collection",
        "embedding_model": "zhipuai"
    }
    response = requests.post(
        "http://localhost:8000/parse-and-store",
        files=files,
        params=params
    )
    result = response.json()
    print(f"存储成功，任务ID: {result['task_id']}")

# 4. 搜索文档
params = {
    "query": "高并发网络编程",
    "collection_name": "my_collection",
    "k": 3
}
response = requests.get("http://localhost:8000/search", params=params)
results = response.json()

print(f"找到{results['total_results']}个相关结果:")
for i, result in enumerate(results['results']):
    print(f"{i+1}. 相似度: {result['similarity_score']:.4f}")
    print(f"   内容: {result['content'][:100]}...")
    print()
```

#### JavaScript示例

```javascript
// 1. 健康检查
fetch('http://localhost:8000/health')
  .then(response => response.json())
  .then(data => console.log(data));

// 2. 解析PDF文件
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('chunk_size', '1000');
formData.append('return_content', 'true');

fetch('http://localhost:8000/parse', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  console.log(`解析成功，共${data.total_documents}个文档片段`);
});

// 3. 搜索文档
const searchParams = new URLSearchParams({
  query: '高并发网络编程',
  collection_name: 'my_collection',
  k: 3
});

fetch(`http://localhost:8000/search?${searchParams}`)
  .then(response => response.json())
  .then(data => {
    console.log(`找到${data.total_results}个相关结果`);
    data.results.forEach((result, index) => {
      console.log(`${index + 1}. 相似度: ${result.similarity_score.toFixed(4)}`);
      console.log(`   内容: ${result.content.substring(0, 100)}...`);
    });
  });
```

#### cURL示例

```bash
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 解析PDF（不返回内容）
curl -X POST "http://localhost:8000/parse" \
  -F "file=@document.pdf" \
  -F "chunk_size=1000"

# 3. 解析PDF（返回内容）
curl -X POST "http://localhost:8000/parse" \
  -F "file=@document.pdf" \
  -F "return_content=true"

# 4. 解析并存储
curl -X POST "http://localhost:8000/parse-and-store" \
  -F "file=@document.pdf" \
  -F "collection_name=my_docs" \
  -F "embedding_model=zhipuai"

# 5. 搜索文档
curl -X GET "http://localhost:8000/search" \
  -G \
  -d "query=技术栈" \
  -d "collection_name=my_docs" \
  -d "k=5"
```

---

### 性能优化建议

#### 1. 文档分块策略

```python
# 根据文档类型调整分块大小
params = {
    "chunk_size": 1500,    # 长文档使用更大的分块
    "chunk_overlap": 300   # 增加重叠以保持语义连续性
}
```

#### 2. 批量处理

```python
# 批量上传多个文档
import os
import glob

pdf_files = glob.glob("documents/*.pdf")
for pdf_file in pdf_files:
    collection_name = f"docs_{os.path.basename(pdf_file).split('.')[0]}"
    # 上传到不同的集合
    with open(pdf_file, "rb") as f:
        files = {"file": f}
        params = {"collection_name": collection_name}
        response = requests.post(
            "http://localhost:8000/parse-and-store",
            files=files,
            params=params
        )
```

#### 3. 搜索优化

```python
# 使用更具体的查询词
queries = [
    "Python编程经验",      # 具体技能
    "项目管理经验",        # 具体经验
    "机器学习算法",        # 具体技术
]

# 调整返回结果数量
params = {
    "query": query,
    "k": 10,  # 获取更多结果进行筛选
}
```

## 配置说明

### 主要配置项

| 配置项 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| `MILVUS_URI` | Milvus数据库连接地址 | `http://localhost:19530` | ✅ |
| `MILVUS_TOKEN` | Milvus认证令牌 | `` | ❌ |
| `COLLECTION_NAME` | 默认集合名称 | `pdf_documents` | ❌ |
| `ZHIPUAI_API_KEY` | 智谱AI API密钥 | `` | ✅* |
| `ZHIPUAI_EMBEDDING_MODEL` | 智谱AI嵌入模型 | `embedding-2` | ❌ |
| `DEFAULT_EMBEDDING_MODEL` | 默认嵌入模型类型 | `zhipuai` | ❌ |
| `BGE_MODEL_NAME` | BGE嵌入模型名称 | `BAAI/bge-small-zh-v1.5` | ❌ |
| `BGE_DEVICE` | BGE模型运行设备 | `cpu` | ❌ |
| `PDF_CHUNK_SIZE` | 文档分块大小 | `1000` | ❌ |
| `PDF_CHUNK_OVERLAP` | 分块重叠大小 | `200` | ❌ |
| `LOG_LEVEL` | 日志级别 | `INFO` | ❌ |

*注：使用智谱AI模型时必填

### 嵌入模型选择

#### 1. 智谱AI模型 (推荐)
- **优点**: 中文效果好，维度高(1024)，API稳定
- **缺点**: 需要API密钥，有使用成本
- **配置**: 需要设置`ZHIPUAI_API_KEY`

#### 2. BGE模型
- **优点**: 本地运行，无需API密钥，支持中文
- **缺点**: 首次下载模型较大，维度较低(384)
- **配置**: 自动下载，可配置运行设备

#### 3. OpenAI模型
- **优点**: 效果优秀，多语言支持
- **缺点**: 需要API密钥，成本较高
- **配置**: 需要设置`OPENAI_API_KEY`

### 环境变量配置示例

```env
# Milvus数据库配置
MILVUS_URI=http://localhost:19530
MILVUS_TOKEN=
COLLECTION_NAME=pdf_documents

# 智谱AI配置（推荐）
ZHIPUAI_API_KEY=your_zhipuai_api_key_here
ZHIPUAI_EMBEDDING_MODEL=embedding-2
DEFAULT_EMBEDDING_MODEL=zhipuai

# BGE模型配置（备选）
BGE_MODEL_NAME=BAAI/bge-small-zh-v1.5
BGE_DEVICE=cpu
BGE_NORMALIZE_EMBEDDINGS=True

# OpenAI配置（可选）
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1

# 文档处理配置
PDF_CHUNK_SIZE=1000
PDF_CHUNK_OVERLAP=200
PDF_ENCODING=utf-8

# 日志配置
LOG_LEVEL=INFO
LOG_FORMAT=detailed

# 性能配置
BATCH_SIZE=20
MAX_WORKERS=4
```

## Milvus数据库配置

### 本地Docker部署

```bash
# 下载docker-compose文件
wget https://github.com/milvus-io/milvus/releases/download/v2.4.0/milvus-standalone-docker-compose.yml -O docker-compose.yml

# 启动Milvus
docker-compose up -d

# 检查状态
docker-compose ps
```

### 连接测试

```python
from database.milvus_client import MilvusVectorStore

vector_store = MilvusVectorStore()
if vector_store.create_connection():
    print("Milvus连接成功！")
else:
    print("Milvus连接失败，请检查配置")
```

---

## 部署指南

### 开发环境部署

1. **克隆项目**
```bash
git clone <repository-url>
cd PDF_ANALYSER
```

2. **创建虚拟环境**
```bash
# 使用conda
conda create -n PDF_ANALYSER python=3.9
conda activate PDF_ANALYSER

# 或使用venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
cp .env.example .env
# 编辑.env文件，填入必要的配置
```

5. **启动Milvus**
```bash
# 使用Docker Compose
docker-compose up -d
```

6. **启动API服务**
```bash
python start_api.py
```

### 生产环境部署

#### 使用Docker部署

1. **创建Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "start_api.py"]
```

2. **构建镜像**
```bash
docker build -t pdf-analyser .
```

3. **运行容器**
```bash
docker run -d \
  --name pdf-analyser \
  -p 8000:8000 \
  -e MILVUS_URI=http://milvus:19530 \
  -e ZHIPUAI_API_KEY=your_api_key \
  pdf-analyser
```

#### 使用Docker Compose

```yaml
version: '3.8'

services:
  pdf-analyser:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MILVUS_URI=http://milvus:19530
      - ZHIPUAI_API_KEY=${ZHIPUAI_API_KEY}
    depends_on:
      - milvus

  milvus:
    image: milvusdb/milvus:v2.6.0
    ports:
      - "19530:19530"
    volumes:
      - milvus_data:/var/lib/milvus

volumes:
  milvus_data:
```

---

## 测试指南

### 自动化测试

项目提供了完整的测试套件：

```bash
# 运行所有测试
cd test

# 1. 测试Milvus连接
python test_milvus_connection.py

# 2. 测试完整存储流程
python test_milvus_storage.py

# 3. 测试API接口
python test_api.py

# 4. 简单快速测试
python simple_test.py
```

### 手动测试步骤

1. **检查服务状态**
```bash
curl http://localhost:8000/health
```

2. **测试PDF解析**
```bash
curl -X POST "http://localhost:8000/parse" \
  -F "file=@test.pdf" \
  -F "return_content=true"
```

3. **测试存储功能**
```bash
curl -X POST "http://localhost:8000/parse-and-store" \
  -F "file=@test.pdf" \
  -F "collection_name=test_collection"
```

4. **测试搜索功能**
```bash
curl -X GET "http://localhost:8000/search?query=测试&collection_name=test_collection"
```

### 性能测试

```python
import time
import requests
import concurrent.futures

def test_concurrent_requests():
    """测试并发请求性能"""
    def make_request():
        response = requests.get("http://localhost:8000/health")
        return response.status_code == 200

    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(100)]
        results = [future.result() for future in futures]

    end_time = time.time()
    success_rate = sum(results) / len(results)

    print(f"并发测试结果:")
    print(f"- 总请求数: {len(results)}")
    print(f"- 成功率: {success_rate:.2%}")
    print(f"- 总耗时: {end_time - start_time:.2f}秒")
    print(f"- 平均QPS: {len(results) / (end_time - start_time):.2f}")

if __name__ == "__main__":
    test_concurrent_requests()
```

## 常见问题

### 1. Milvus连接失败

- 检查Milvus服务是否启动
- 确认连接地址和端口是否正确
- 检查防火墙设置

### 2. 嵌入模型下载慢

- BGE模型首次使用会自动下载，请耐心等待
- 可以手动下载模型到本地缓存目录

### 3. PDF解析失败

- 确认PDF文件格式正确
- 检查文件路径是否存在
- 查看日志获取详细错误信息

## 扩展功能

### 添加新的解析器

在 `parsers/` 目录下创建新的解析器类，继承基础接口。

### 添加新的向量数据库

在 `database/` 目录下实现新的数据库客户端。

### 自定义嵌入模型

在 `models/embeddings.py` 中添加新的嵌入模型支持。

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！
