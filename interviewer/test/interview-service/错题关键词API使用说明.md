# 错题关键词API使用说明

## 概述

这个API专门为Dify工作流设计，用于从用户的错题记录中提取关键词，供Dify进行知识库检索和题目生成。

## API接口

### 获取错题关键词

**接口地址：** `GET /dify/interview/{user_id}/wrong-question-keywords`

**参数：**
- `user_id` (路径参数): 用户ID
- `required_count` (查询参数): 需要的关键词组数量（对应错题数量），默认5个，范围1-20
- `question_type` (查询参数，可选): 题目类型筛选

**选择策略：**
- **第一步**：获取最近的n道错题（n=20，可配置）
- **第二步**：筛选出包含knowledge_points字段的错题
- **第三步**：从筛选后的错题中随机选择m道（m=required_count参数）
- **优势**：兼顾时效性（最近错题）和随机性（避免重复）

**返回示例：**
```json
{
  "success": true,
  "user_id": "test_user_001",
  "keywords": [
    ["Java", "多态", "继承", "重写", "接口", "面向对象", "方法重载"],
    ["数据库", "ACID", "原子性", "一致性", "隔离性", "持久性", "事务"]
  ],
  "question_details": [
    {
      "question_id": "session_20250906_201501_7622198b_q003",
      "question_text": "请解释Java中的多态性，并给出一个实际的代码示例。",
      "score": 4.0,
      "keywords": ["Java", "多态", "继承", "重写", "接口", "面向对象", "方法重载"],
      "keywords_count": 7
    }
  ],
  "total_selected_questions": 2,
  "total_wrong_questions": 4,
  "recent_pool_size": 20,
  "available_keywords_count": 2,
  "message": "从最近4道错题中随机选择2组关键词"
}
```

## 在Dify中的使用方案（二维数组模式）

### 推荐工作流：循环生成题目

**核心思路：** 获取m组关键词，循环m次，每次用一组关键词生成1道题目

### 示例Dify工作流步骤：

1. **HTTP请求节点**
   ```
   GET /dify/interview/{user_id}/wrong-question-keywords?required_count=3
   ```
   返回：`keywords: [["Docker", "容器技术"], ["Redis", "缓存"], ["Python", "面向对象"]]`

2. **循环节点**
   - 遍历 `keywords` 数组
   - 每次循环处理一组关键词

3. **知识库检索节点**（在循环内）
   - 使用当前组的关键词进行精准检索
   - 例如：第一次循环用 `["Docker", "容器技术"]` 检索

4. **LLM节点**（在循环内）
   - 基于当前组关键词的检索结果生成1道题目
   - 确保题目聚焦于当前知识点

5. **结果收集**
   - 将每次循环生成的题目收集起来
   - 最终得到m道针对性强的题目

### 优势：
- **精准性**：每个关键词组都能得到专门的检索和生成
- **覆盖性**：确保每个错题知识点都被充分覆盖
- **质量**：避免关键词混合导致的检索结果不准确

## 总体优势

1. **轻量级**：代码只负责关键词提取，主要逻辑在Dify中完成
2. **精准性**：二维数组确保每个错题知识点都能精准检索
3. **可控性**：支持错题数量控制和类型筛选
4. **架构清晰**：符合您的Dify主导、代码辅助的设计理念

## 测试命令

```bash
# 获取3组关键词（对应3个错题）
curl -X GET "http://localhost:8006/dify/interview/test_user_001/wrong-question-keywords?required_count=3"

# 获取技术类错题的关键词组
curl -X GET "http://localhost:8006/dify/interview/test_user_001/wrong-question-keywords?required_count=5&question_type=technical"

# 格式化输出查看结构
curl -X GET "http://localhost:8006/dify/interview/test_user_001/wrong-question-keywords?required_count=2" | python3 -m json.tool
```

## 最新测试结果

### 当前测试数据状态
- **用户ID**: `test_user_001`
- **总错题数量**: 4条
- **有关键词的错题**: 2条
- **错题判定阈值**: 6.0分

### 错题分布详情
1. **数据库ACID特性题目** - 评分3.0分 ✅ 有关键词
   - 关键词: `["数据库", "ACID", "原子性", "一致性", "隔离性", "持久性", "事务"]`
2. **Java多态性题目** - 评分4.0分 ✅ 有关键词
   - 关键词: `["Java", "多态", "继承", "重写", "接口", "面向对象", "方法重载"]`
3. **其他技术题目** - 评分4.5分和3.6分 ❌ 无关键词

### 实际API响应示例
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
    },
    {
      "question_id": "session_20250906_201501_7622198b_q003",
      "question_text": "请解释Java中的多态性，并给出一个实际的代码示例。",
      "score": 4.0,
      "keywords": ["Java", "多态", "继承", "重写", "接口", "面向对象", "方法重载"],
      "keywords_count": 7
    }
  ],
  "total_selected_questions": 2,
  "total_wrong_questions": 4,
  "message": "成功提取2组关键词，每组对应一个错题"
}
```

### 功能验证结果 ✅
- ✅ 错题自动识别（评分<6.0分）
- ✅ 关键词JSON格式解析
- ✅ 二维数组关键词返回
- ✅ 错题详情完整返回
- ✅ 支持数量控制和类型筛选
