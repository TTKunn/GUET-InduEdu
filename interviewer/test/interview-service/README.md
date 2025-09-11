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
- **错题记录管理**：自动识别和管理错题记录
- **错题查询**：获取用户错题列表，支持筛选
- **错题关键词提取**：为Dify工作流提供错题关键词

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

### 4. 获取错题关键词（用于生成针对性题目）

**选择策略**：在最近20道错题中随机选择指定数量的题目，兼顾时效性和随机性

```yaml
name: "获取错题关键词"
type: "http"
config:
  url: "http://interview-service:8006/dify/interview/{{#start.user_id#}}/wrong-question-keywords"
  method: "GET"
  params:
    required_count: 3
    question_type: "technical"
  output_variables:
    - keywords
    - question_details
    - total_selected_questions
    - recent_pool_size
    - available_keywords_count
```

## 📚 API接口说明

### Dify专用接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/dify/interview/create` | POST | 创建面试记录 |
| `/dify/interview/add-qa` | POST | 添加题目和回答 |
| `/dify/interview/{user_id}/latest` | GET | 获取最新面试信息 |
| `/dify/interview/{session_id}/summary` | GET | 获取面试总结 |
| `/dify/interview/{user_id}/wrong-questions` | GET | 获取用户错题列表 |
| `/dify/interview/{user_id}/wrong-question-keywords` | GET | 获取错题关键词组合 |

### 标准接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/interview/sessions` | POST | 创建面试会话 |
| `/interview/sessions/{user_id}` | GET | 获取用户面试列表 |
| `/interview/sessions/{session_id}/detail` | GET | 获取会话详情 |
| `/interview/sessions/{session_id}/start` | POST | 开始面试 |
| `/interview/sessions/{session_id}/finish` | POST | 结束面试 |
| `/interview/wrong-questions/{user_id}` | GET | 获取用户错题（标准版） |

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

### 错题查询数据
```json
{
  "success": true,
  "user_id": "test_user_001",
  "wrong_questions": [
    {
      "question_id": "session_20250906_201501_7622198b_q003",
      "session_id": "session_20250906_201501_7622198b",
      "question_text": "请解释Java中的多态性，并给出一个实际的代码示例。",
      "question_type": "technical",
      "question_category": "Java编程",
      "difficulty_level": "medium",
      "candidate_answer": "多态就是一个对象有多种形态，但具体怎么实现我不太清楚。",
      "interviewer_feedback": "理解基本概念，但缺乏具体实现细节，建议学习继承、重写、接口等相关知识。",
      "overall_score": 4.0,
      "knowledge_points": "[\"Java\", \"多态\", \"继承\", \"重写\", \"接口\", \"面向对象\", \"方法重载\"]",
      "answered_at": "2025-09-07T09:28:41",
      "reviewed_at": "2025-09-07T09:28:41"
    }
  ],
  "total": 4,
  "message": "错题获取成功"
}
```

### 错题关键词数据
```json
{
  "success": true,
  "user_id": "test_user_001",
  "keywords": [
    ["数据库", "ACID", "原子性", "一致性", "隔离性", "持久性", "事务"],
    ["Java", "多态", "继承", "重写", "接口", "面向对象", "方法重载"]
  ],
  "question_details": [
    {
      "question_id": "session_20250906_201501_7622198b_q002",
      "question_text": "请解释数据库中的ACID特性，并说明每个特性的含义。",
      "score": 3.0,
      "keywords": ["数据库", "ACID", "原子性", "一致性", "隔离性", "持久性", "事务"],
      "keywords_count": 7
    }
  ],
  "total_selected_questions": 2,
  "total_wrong_questions": 4,
  "message": "成功提取2组关键词，每组对应一个错题"
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
