# [002] MongoDB到MySQL迁移详细计划

**创建时间**: 2025-08-30  
**项目**: GUET-InduEdu 面试系统  
**目标**: 将analysis-service从MongoDB平滑迁移到MySQL，保持API完全兼容

## 📋 项目概述

### 迁移背景
- 当前analysis-service使用MongoDB存储简历分析数据
- 团队对MySQL更熟悉，便于后续维护和扩展
- 为后续错题集功能提供更好的关系型数据支持
- 需要保持API完全兼容，不影响Dify调用

### 迁移目标
- 将MongoDB数据结构转换为MySQL关系型设计
- 保持所有API接口响应格式完全不变
- 实现平滑迁移，零停机时间
- 为后续功能扩展打下基础

## 🎯 核心任务分解

### 任务1: MySQL数据库设计
**目标**: 设计完整的MySQL表结构
**预计时间**: 1天

#### 子任务:
1. **分析现有MongoDB结构**
   - 分析candidate_profiles集合的字段结构
   - 识别嵌套文档和数组字段
   - 确定数据类型和约束

2. **设计MySQL表结构**
   - 主表: candidate_profiles (基本信息)
   - 关联表: work_experiences (工作经验)
   - 关联表: projects (项目经验)
   - 关联表: technical_skills (技术技能)
   - 关联表: project_keywords (项目关键词)
   - 关联表: extracted_keywords (提取关键词)

3. **创建数据库和表**
   - 连接MySQL服务器
   - 创建interview_analysis数据库
   - 执行DDL语句创建所有表
   - 创建必要的索引

### 任务2: 数据迁移脚本开发
**目标**: 开发自动化数据迁移工具
**预计时间**: 1天

#### 子任务:
1. **MongoDB数据导出**
   - 连接现有MongoDB
   - 导出candidate_profiles集合数据
   - 数据格式验证和清洗

2. **数据转换逻辑**
   - 嵌套文档拆分为关系表
   - 数组字段转换为多条记录
   - 数据类型转换和格式化

3. **MySQL数据导入**
   - 批量插入主表数据
   - 批量插入关联表数据
   - 数据完整性验证

### 任务3: 代码重构
**目标**: 重写数据访问层，保持API兼容
**预计时间**: 2天

#### 子任务:
1. **数据库连接层改造**
   - 安装SQLAlchemy依赖
   - 创建MySQL连接配置
   - 定义ORM模型类

2. **数据访问层重写**
   - 重写DatabaseService类
   - 实现save_profile方法
   - 实现get_profile方法
   - 实现查询和统计方法

3. **API响应格式适配**
   - 确保/analyze接口响应格式不变
   - 确保/keywords接口响应格式不变
   - 确保/keywords/grouped接口响应格式不变

### 任务4: 测试验证
**目标**: 全面测试迁移结果
**预计时间**: 1天

#### 子任务:
1. **数据完整性验证**
   - 对比MongoDB和MySQL数据条数
   - 验证关键字段数据一致性
   - 检查关联关系正确性

2. **API功能测试**
   - 测试简历分析完整流程
   - 测试关键词查询功能
   - 测试错误处理逻辑

3. **性能基准测试**
   - 对比查询性能
   - 测试并发处理能力
   - 监控资源使用情况

## 📊 数据库设计详情

### 表结构设计

#### 主表: candidate_profiles
```sql
CREATE TABLE candidate_profiles (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    location VARCHAR(200),
    education TEXT,
    direction VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### 关联表: technical_skills
```sql
CREATE TABLE technical_skills (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(100) NOT NULL,
    skill_name VARCHAR(100) NOT NULL,
    skill_category VARCHAR(50),
    sort_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES candidate_profiles(user_id) ON DELETE CASCADE
);
```

### 数据映射关系
```
MongoDB candidate_profiles → MySQL 多表结构

personal_info.name → candidate_profiles.name
personal_info.phone → candidate_profiles.phone
personal_info.email → candidate_profiles.email
personal_info.location → candidate_profiles.location
education → candidate_profiles.education
direction → candidate_profiles.direction
technical_skills[] → technical_skills表多条记录
projects[] → projects表多条记录
work_experience[] → work_experiences表多条记录
projects_keywords[] → project_keywords表多条记录
extracted_keywords[] → extracted_keywords表多条记录
```

## 🚀 实施计划

### 第1天: 数据库设计和创建
- [x] 分析现有MongoDB结构
- [ ] 设计MySQL表结构
- [ ] 创建数据库和表
- [ ] 创建索引

### 第2天: 数据迁移
- [ ] 开发迁移脚本
- [ ] 执行数据迁移
- [ ] 验证数据完整性

### 第3天: 代码重构
- [ ] 安装MySQL依赖
- [ ] 重写数据访问层
- [ ] 修改API接口

### 第4天: 测试验证
- [ ] 功能测试
- [ ] 性能测试
- [ ] 集成测试

### 第5天: 上线切换
- [ ] 并行验证
- [ ] 正式切换
- [ ] 监控观察

## 📝 验收标准

- [ ] MySQL表结构创建完成
- [ ] 数据迁移100%成功
- [ ] 所有API接口响应格式保持不变
- [ ] 功能测试全部通过
- [ ] 性能不低于原MongoDB方案
- [ ] 代码质量符合规范
- [ ] 文档更新完整

## ⚠️ 风险控制

### 数据安全
- 迁移前完整备份MongoDB数据
- 迁移过程保留MongoDB作为备份
- 实施回滚预案

### 服务可用性
- 采用蓝绿部署策略
- 保持API向后兼容
- 监控服务健康状态

### 性能风险
- 预先进行性能测试
- 优化SQL查询语句
- 合理设计索引策略
