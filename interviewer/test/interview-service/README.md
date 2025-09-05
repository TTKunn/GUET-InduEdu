# 面试记录服务 (Interview Service)

## 📋 概述

面试记录服务是一个专为Dify工作流设计的微服务，提供完整的面试记录管理功能。服务支持面试会话创建、题目管理、回答记录和统计分析等功能。

## 🏗️ 系统架构

```
Dify工作流 → 面试记录服务 → MySQL数据库
           ↓
       analysis-service (获取用户档案)
```

## ✨ 主要功能

### Dify专用API（核心功能）
- **创建面试记录**：一键创建面试会话
- **添加题目和回答**：原子操作记录完整问答
- **获取最新面试信息**：查询用户最新面试状态
- **获取面试总结**：生成结构化面试报告

### 标准API功能
- **面试会话管理**：创建、开始、结束面试
- **题目管理**：批量添加、更新题目
- **回答管理**：提交回答、反馈评价
- **统计查询**：面试历史、统计分析

## 📁 项目结构

```
interview-service/
├── config.py              # 配置文件
├── models.py              # 数据模型定义
├── database.py            # 数据库操作层
├── interview_service.py   # 核心业务逻辑
├── main.py               # FastAPI主服务
├── requirements.txt       # Python依赖
├── Dockerfile            # Docker镜像构建
├── docker-compose.yml    # Docker编排配置
├── init.sql              # 数据库初始化脚本
├── start.sh              # 启动脚本
└── README.md            # 本文档
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 进入项目目录
cd interviewer/test/interview-service

# 安装依赖
pip install -r requirements.txt
```

### 2. 数据库配置

确保MySQL数据库运行，并创建数据库：

```sql
CREATE DATABASE interview_analysis CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 环境变量配置

创建 `.env` 文件（可选）：

```bash
# 数据库配置
MYSQL_URL=mysql+pymysql://root:password@localhost:3306/interview_analysis

# 服务配置
API_HOST=0.0.0.0
API_PORT=8006

# 外部服务配置
ANALYSIS_SERVICE_URL=http://localhost:8004

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/interview_service.log
```

### 4. 启动服务

#### 方式一：使用启动脚本（推荐）

```bash
./start.sh
```

#### 方式二：Docker Compose

```bash
docker-compose up -d
```

#### 方式三：直接运行

```bash
python main.py
```

### 5. 验证服务

```bash
# 健康检查
curl http://localhost:8006/health

# 查看API文档
# 访问 http://localhost:8006/docs
```

## 🔌 Dify工作流集成

### 1. 创建面试记录

```yaml
name: "创建面试记录"
type: "http"
config:
  url: "http://interview-service:8006/dify/interview/create"
  method: "POST"
  headers:
    Content-Type: "application/json"
  body:
    user_id: "{{#start.user_id#}}"
    session_name: "{{#start.position#}}技术面试"
    session_type: "technical"
    difficulty_level: "medium"
  output_variables:
    - session_id
    - status
```

### 2. 添加题目和回答

```yaml
name: "记录面试问答"
type: "http"
config:
  url: "http://interview-service:8006/dify/interview/add-qa"
  method: "POST"
  headers:
    Content-Type: "application/json"
  body:
    session_id: "{{#创建面试记录.session_id#}}"
    question_text: "{{#LLM生成题目.question#}}"
    question_type: "technical"
    question_category: "{{#LLM生成题目.category#}}"
    candidate_answer: "{{#用户输入.answer#}}"
    interviewer_feedback: "{{#LLM评价.feedback#}}"
    overall_score: "{{#LLM评价.score#}}"
```

### 3. 获取面试总结

```yaml
name: "获取面试总结"
type: "http"
config:
  url: "http://interview-service:8006/dify/interview/{{#创建面试记录.session_id#}}/summary"
  method: "GET"
  output_variables:
    - summary
    - questions_summary
    - overall_evaluation
```

## 📚 API接口说明

### Dify专用接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/dify/interview/create` | POST | 创建面试记录 |
| `/dify/interview/add-qa` | POST | 添加题目和回答 |
| `/dify/interview/{user_id}/latest` | GET | 获取最新面试信息 |
| `/dify/interview/{session_id}/summary` | GET | 获取面试总结 |

### 标准接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/interview/sessions` | POST | 创建面试会话 |
| `/interview/sessions/{user_id}` | GET | 获取用户面试列表 |
| `/interview/sessions/{session_id}/detail` | GET | 获取会话详情 |
| `/interview/sessions/{session_id}/start` | POST | 开始面试 |
| `/interview/sessions/{session_id}/finish` | POST | 结束面试 |

## 📊 数据结构

### 面试会话数据
```json
{
  "session_id": "session_20250904_001",
  "user_id": "candidate_001",
  "session_name": "Java后端开发面试",
  "session_type": "technical",
  "status": "completed",
  "total_questions": 5,
  "completed_questions": 5,
  "average_score": 8.4,
  "created_at": "2025-09-04T21:40:00Z"
}
```

### 面试总结数据
```json
{
  "summary": {
    "session_name": "Java后端开发面试",
    "total_questions": 5,
    "completed_questions": 5,
    "average_score": 8.4,
    "duration_minutes": 45,
    "strengths": ["框架理解深入", "代码实现能力强"],
    "improvements": ["需要更多实际项目经验"],
    "overall_evaluation": "优秀"
  },
  "questions_summary": [
    {
      "question_text": "Spring Boot自动配置原理",
      "score": 8.5,
      "feedback": "理解深入但缺少实例"
    }
  ]
}
```

## 🛠️ 故障排除

### 常见问题

1. **数据库连接失败**
   ```bash
   # 检查MySQL服务状态
   systemctl status mysql
   
   # 检查数据库配置
   python config.py
   ```

2. **服务启动失败**
   ```bash
   # 查看日志
   tail -f logs/interview_service.log
   
   # 检查端口占用
   netstat -tulpn | grep 8006
   ```

3. **API调用失败**
   ```bash
   # 检查服务健康状态
   curl http://localhost:8006/health
   
   # 查看API文档
   # 访问 http://localhost:8006/docs
   ```

## 📈 性能优化

1. **数据库索引**：已自动创建必要的索引
2. **连接池**：MySQL连接池自动管理
3. **异步处理**：使用FastAPI异步特性
4. **缓存策略**：可选择启用Redis缓存

## 🔒 安全配置

- 支持API密钥认证（可选）
- CORS跨域配置
- 请求频率限制
- SQL注入防护

## 📞 技术支持

如有问题，请检查：
1. 环境变量配置是否正确
2. 数据库服务是否正常运行
3. 日志文件中的错误信息
4. API文档：http://localhost:8006/docs

## 🔄 与其他服务的关系

- **analysis-service (8004)**：获取用户档案信息
- **pdf-parser-service (8003)**：无直接依赖
- **vector-storage-service (8005)**：无直接依赖

## 📝 开发说明

- Python 3.10+
- FastAPI框架
- SQLAlchemy ORM
- MySQL数据库
- Docker支持
