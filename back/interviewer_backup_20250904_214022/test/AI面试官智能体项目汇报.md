我来查看相关文件，重新撰写一份聚焦架构和技术思路的项目汇报。

# AI面试官智能体项目汇报

## 项目架构概览

本项目采用分层架构设计，由Dify Chatflow前端和外部知识库服务后端组成，实现智能化面试流程。

```mermaid
graph TB
    subgraph "用户交互层"
        A[用户输入] --> B[Dify Chatflow]
    end
    
    subgraph "Dify工作流层"
        B --> C[模式判断]
        C --> D[知识检索]
        C --> E[岗位检索]
        D --> F[上下文融合]
        E --> F
        F --> G[题目生成LLM]
        G --> H[题目拆分]
        H --> I[循环面试]
        I --> J[最终评价]
    end
    
    subgraph "外部服务层"
        K[Document-parser API<br/>端口:8002]
        L[Dify适配器<br/>端口:8001]
        M[Milvus向量库<br/>端口:19530]
    end
    
    D -.-> L
    E -.-> L
    L -.-> K
    K -.-> M
```

## 核心模块设计

### 1. Dify Chatflow工作流

#### 主要节点流程
```mermaid
flowchart TD
    Start[开始节点] --> Judge{模式判断}
    Judge -->|keywords非空| KnowRet[知识点检索]
    Judge -->|company+position非空| PosRet[岗位检索]
    Judge -->|默认| GenRet[通用检索]
    
    KnowRet --> Merge[模板融合]
    PosRet --> Merge
    GenRet --> Merge
    
    Merge --> LLMGen[题目生成LLM]
    LLMGen --> Split[题目拆分Code]
    Split --> Init[循环初始化]
    
    Init --> Loop{循环控制}
    Loop --> Extract[提取当前题Code]
    Extract --> Show[展示题目Answer]
    Show --> Collect[收集回答sys.query]
    Collect --> Eval[评价LLM]
    Eval --> Update[更新状态Assigner]
    Update --> Inc[索引递增Code]
    Inc --> Loop
    
    Loop -->|结束| Final[最终评价LLM]
    Final --> End[结束]
```

#### 对话变量状态管理
```yaml
conversation_variables:
  - questions_array: array[string]  # 题目数组
  - que_count: integer             # 题目总数
  - cur_index: integer             # 当前题号(1开始)
  - last_question: string          # 上一题内容
  - answers_array: array[string]   # 用户回答历史
```

### 2. 外部知识库服务架构

#### Document-parser服务 (端口8002)
```mermaid
graph LR
    subgraph "PDF解析服务"
        A[FastAPI接口] --> B[PDF解析器]
        B --> C[文本分块]
        C --> D[向量化]
        D --> E[Milvus存储]
    end
    
    subgraph "核心组件"
        F[智谱AI嵌入模型]
        G[BGE本地模型]
        H[用户知识库管理]
    end
    
    D --> F
    D --> G
    A --> H
```

**技术栈**：
- **API框架**：FastAPI + Uvicorn
- **PDF解析**：PyPDFLoader
- **向量化**：智谱AI embedding-2 / BGE-small-zh-v1.5
- **向量存储**：Milvus 2.4+
- **文本分块**：RecursiveCharacterTextSplitter

#### Dify适配器服务 (端口8001)
```mermaid
graph LR
    A[Dify工作流] --> B[适配器API]
    B --> C[API Key验证]
    C --> D[集合路由]
    D --> E[PDF解析API调用]
    E --> F[结果格式转换]
    F --> A
```

**核心功能**：
- API Key到Milvus集合的映射
- Dify检索格式适配
- 用户知识库隔离
- 请求频率限制

## 关键技术实现

### 1. 知识库检索机制

#### 双路检索策略
```python
# 知识点检索路径
keywords → 知识点检索节点 → Milvus集合查询 → Top-K=4结果

# 岗位检索路径  
company_name + position → 模板拼接 → 岗位检索节点 → Milvus集合查询 → Top-K=4结果

# 结果融合
两路结果 → Jinja2模板 → 统一上下文文本 → LLM题目生成
```

#### 检索配置
- **重排序**：weighted_score模式，向量权重0.7，关键词权重0.3
- **Top-K**：4条最相关结果
- **嵌入模型**：智谱AI embedding-2 (1024维)

### 2. 循环面试实现机制

#### 状态机设计
```mermaid
stateDiagram-v2
    [*] --> 题目拆分: LLM生成完成
    题目拆分 --> 循环初始化: questions_array + que_count
    循环初始化 --> 提取题目: cur_index=1
    提取题目 --> 展示题目: questions_array[cur_index-1]
    展示题目 --> 等待回答: Answer节点暂停
    等待回答 --> 生成评价: sys.query获取用户输入
    生成评价 --> 更新状态: 保存到answers_array
    更新状态 --> 索引递增: cur_index++
    索引递增 --> 判断继续: cur_index vs que_count
    判断继续 --> 提取题目: 继续循环
    判断继续 --> 最终评价: 循环结束
    最终评价 --> [*]
```

#### 核心代码节点
```python
# 题目拆分器 (Code节点)
def main(questions_text: str) -> dict:
    lines = questions_text.strip().split('\n')
    questions = [line.split('：', 1)[1].strip() 
                for line in lines if '题：' in line]
    return {"questions_array": questions, "total_count": len(questions)}

# 题目提取器 (Code节点)  
def main(questions_array: list, current_index: int) -> dict:
    question_index = current_index - 1
    return {"current_question": questions_array[question_index]}

# 索引递增器 (Code节点)
def main(current_index: int) -> dict:
    return {"next_index": current_index + 1}
```

### 3. 外部知识库集成

#### 用户知识库管理
```python
# 用户ID到集合的映射
user_id: "user123" → collection: "user_kb_user123" → api_key: "dify-user-user123"

# API Key权限控制
{
  "dify-user-user123": {
    "collection": "user_kb_user123",
    "permissions": ["read"],
    "rate_limit": 100,
    "user_id": "user123"
  }
}
```

#### 文档处理流程
```mermaid
sequenceDiagram
    participant U as 用户
    participant D as Dify工作流
    participant A as 适配器(8001)
    participant P as PDF解析(8002)
    participant M as Milvus

    U->>D: 上传简历/文档
    D->>A: 检索请求(API Key)
    A->>A: 验证API Key
    A->>P: 调用解析API
    P->>P: PDF解析+分块
    P->>M: 向量化存储
    M-->>P: 存储确认
    P-->>A: 解析结果
    A->>A: 格式转换
    A-->>D: Dify格式结果
    D-->>U: 检索结果
```

## 项目进度与待完成内容

### ✅ 已完成 (90%)
- **核心面试流程**：模式判断、知识检索、题目生成、循环问答
- **状态管理**：对话变量、循环控制、历史记录
- **外部服务**：PDF解析API、Dify适配器、Milvus集成
- **用户知识库**：个人文档管理、API Key隔离

### 🔄 待完成 (10%)
- **综合评价报告**：基于answers_array生成最终评价
- **错题分析**：低分题目整理和复习建议
- **导出功能**：面试记录PDF报告生成

### 🔧 优化方向
1. **RAGFlow迁移**：将Document-parser替换为RAGFlow，提升文档解析质量
2. **检索优化**：调整Top-K、重排权重，提升题目相关性
3. **评价算法**：多维度评分体系，个性化反馈机制

## 技术特点总结

1. **Chatflow状态管理**：巧妙利用对话变量实现复杂循环逻辑
2. **双路检索融合**：知识点+岗位检索，提升题目定制化程度  
3. **微服务架构**：PDF解析、适配器、向量库分离，便于扩展
4. **用户隔离**：基于API Key的多租户知识库管理
5. **可视化配置**：纯Dify节点实现，无需编程即可调整流程

该项目成功实现了智能面试的核心功能，在技术架构上具有良好的扩展性，为后续功能迭代提供了坚实基础。