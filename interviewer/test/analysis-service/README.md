# 简历分析服务

## 📋 概述

这是一个完整的PDF简历解析和结构化信息提取服务，专为面试智能体设计。服务将PDF简历解析为结构化数据并存储到MongoDB中，每个用户对应一个唯一ID，便于后续检索和使用。

## 🏗️ 系统架构

```
PDF简历 → PDF解析服务 → LLM结构化提取 → MongoDB存储 → 关键词提取 → Dify工作流检索
```

## ✨ 主要功能

- **PDF解析**：支持复杂格式的PDF简历解析
- **结构化提取**：使用LLM将简历内容提取为结构化数据
- **MongoDB存储**：一个用户一个ID，支持高效查询
- **关键词生成**：自动提取技术关键词用于知识库检索
- **RESTful API**：完整的API接口，易于集成

## 📁 项目结构

```
analysis-service/
├── config.py              # 配置文件（环境变量配置）
├── models.py              # 数据模型定义
├── mysql_database.py      # MySQL数据库服务
├── llm_service.py         # LLM服务（智谱AI/OpenAI）
├── pdf_service.py         # PDF解析服务
├── main.py               # 主API服务
├── requirements.txt       # Python依赖
├── Dockerfile            # Docker镜像构建
├── docker-compose.yml    # Docker编排配置
├── .env.example          # 环境变量模板
└── README.md            # 本文档
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 进入项目目录
cd /home/ubuntu/workspace/project/GUET-InduEdu/interviewer/test/analysis-service

# 复制环境变量配置
cp .env.example .env

# 编辑配置文件，设置必要的参数
nano .env
```

### 2. 必要配置

在 `.env` 文件中设置以下关键配置：

```bash
# MySQL数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=interview_analysis

# LLM配置（至少设置一个）
ZHIPUAI_API_KEY=your_zhipuai_api_key_here
# 或者
OPENAI_API_KEY=your_openai_api_key_here

# Document-parser服务地址
DOCUMENT_PARSER_URL=http://localhost:8002
```

### 3. 启动服务

#### 方式一：Docker Compose（推荐）

```bash
# 启动所有服务（包括MySQL）
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f analysis-service
```

#### 方式二：本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 启动MySQL（需要单独安装）
# 启动Document-parser服务（需要单独启动）

# 启动分析服务
python main.py
```

### 4. 验证服务

```bash
# 健康检查
curl http://localhost:8004/health

# 查看API文档
# 访问 http://localhost:8004/docs
```

## 🔧 配置说明

### 数据库配置位置

**文件位置**: `config.py`

**环境变量配置**:
- `MYSQL_HOST`: MySQL服务器地址
- `MYSQL_PORT`: MySQL端口（默认3306）
- `MYSQL_USER`: MySQL用户名
- `MYSQL_PASSWORD`: MySQL密码
- `MYSQL_DATABASE`: 数据库名称

### 大模型配置位置

**文件位置**: `config.py`

**环境变量配置**:
- `ZHIPUAI_API_KEY`: 智谱AI API密钥
- `OPENAI_API_KEY`: OpenAI API密钥
- `DEFAULT_LLM_PROVIDER`: 默认LLM提供商（zhipuai/openai）

### 服务配置位置

**文件位置**: `config.py`

**环境变量配置**:
- `API_HOST`: 服务监听地址
- `API_PORT`: 服务端口（默认8004）
- `DOCUMENT_PARSER_URL`: PDF解析服务地址

## 📚 API使用说明

### 1. 分析简历

```bash
curl -X POST "http://localhost:8004/analyze" \
  -F "user_id=candidate_001" \
  -F "file=@resume.pdf" \
  -F "extraction_mode=comprehensive" \
  -F "overwrite=true"
```

### 2. 获取关键词（用于Dify检索）

```bash
curl -X POST "http://localhost:8004/keywords" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "candidate_001",
    "category": "all",
    "format_type": "string"
  }'
```

### 3. 查询用户档案

```bash
curl -X POST "http://localhost:8004/profile" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "candidate_001",
    "include_keywords": true
  }'
```

## 🔗 与Dify集成

### 在Dify工作流中的使用

1. **简历分析节点**（HTTP请求）：
   ```yaml
   url: http://localhost:8004/analyze
   method: POST
   body:
     user_id: "{{#start.user_id#}}"
     file: "{{#start.resume_file#}}"
   ```

2. **关键词获取节点**（HTTP请求）：
   ```yaml
   url: http://localhost:8004/keywords
   method: POST
   body:
     user_id: "{{#start.user_id#}}"
     category: "all"
     format_type: "string"
   ```

3. **知识库检索节点**：
   ```yaml
   query_variable_selector: ["关键词获取", "keywords_string"]
   ```

## 📊 数据结构

### 候选人档案结构

```json
{
  "user_id": "candidate_001",
  "personal_info": {
    "name": "张三",
    "phone": "13800138000",
    "email": "zhang@example.com",
    "location": "北京"
  },
  "technical_skills": {
    "programming_languages": ["Java", "Python"],
    "frameworks": ["Spring Boot", "Django"],
    "databases": ["MySQL", "Redis"],
    "tools": ["Docker", "Git"]
  },
  "work_experience": [...],
  "projects": [...],
  "education": [...],
  "extracted_keywords": ["java", "spring boot", "mysql", "redis"],
  "technical_keywords": ["java", "spring boot", "mysql"],
  "domain_keywords": ["电商", "后端开发"],
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

## 🛠️ 故障排除

### 常见问题

1. **MongoDB连接失败**
   ```bash
   # 检查MongoDB服务状态
   docker-compose ps mongodb
   
   # 查看MongoDB日志
   docker-compose logs mongodb
   ```

2. **LLM调用失败**
   ```bash
   # 检查API密钥是否正确设置
   echo $ZHIPUAI_API_KEY
   
   # 查看服务日志
   docker-compose logs analysis-service
   ```

3. **PDF解析失败**
   ```bash
   # 检查Document-parser服务状态
   curl http://localhost:8002/health
   
   # 确保Document-parser服务正在运行
   cd ../Document-parser
   ./manage-services.sh status
   ```

### 日志查看

```bash
# 查看实时日志
docker-compose logs -f analysis-service

# 查看特定时间的日志
docker-compose logs --since="2024-01-01T00:00:00" analysis-service
```

## 📈 性能优化

1. **数据库索引**：已自动创建必要的索引
2. **连接池**：MongoDB连接池自动管理
3. **缓存策略**：可选择启用Redis缓存
4. **并发控制**：支持配置最大并发请求数

## 🔒 安全配置

- 支持API密钥认证（可选）
- CORS跨域配置
- 请求频率限制
- 文件大小限制

## 📞 技术支持

如有问题，请检查：
1. 环境变量配置是否正确
2. 依赖服务是否正常运行
3. 日志文件中的错误信息
4. API文档：http://localhost:8004/docs
