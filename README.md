# GUET-InduEdu 产教融合项目

桂林电子科技大学产教融合项目：大规模人工智能模型在教育教学领域的应用与创新实践

## 📋 项目概述

本项目是桂林电子科技大学的产教融合创新项目，旨在将大规模人工智能模型技术应用于教育教学领域，构建智能化的教育生态系统。项目包含三个核心子系统，实现院校管理、项目协作和智能面试的全流程数字化。

## 🏗️ 项目架构

### 三大核心子系统

1. **院校社团管理系统** (`Club-Management/`)
   - 社团注册与管理
   - 成员管理与权限控制
   - 活动组织与参与
   - 基地资源管理

2. **揭榜挂帅项目系统** (`ProjectBid/`)
   - 项目发布与展示
   - 团队申请与匹配
   - 项目评估与选拔
   - 合同管理与执行

3. **企业AI面试官系统** (`interviewer/`)
   - 智能题目生成
   - 语音交互面试
   - 实时评估分析
   - 面试报告生成

## 🌿 Git分支管理结构

### 分支架构图

```plaintext
实际Git分支结构：
================

main (生产环境) - commit: 98ab340 "Initial commit"
 │
 ├── develop (集成开发主线) - commit: 98ab340 "Initial commit"
 │    │
 │    ├── club-management-dev (院校社团管理系统) - commit: 98ab340 "Initial commit"
 │    │    └── [待创建功能分支]
 │    │
 │    ├── ProjectBid-dev (揭榜挂帅项目系统) - commit: 98ab340 "Initial commit"
 │    │    └── [待创建功能分支]
 │    │
 │    ├── Interviewer-dev (企业AI面试官系统) - commit: 98ab340 "Initial commit"
 │    │    │
 │    │    └── Interviewer_test_dev (AI面试测试开发) - commit: 5e0ef6a ⭐ 当前活跃
 │    │         └── "新增个人知识库的dify外部引用（已部署）测试"
 │    │
 │    └── [未来扩展分支]
 │
 └── [未来hotfix分支]

分支创建关系：
=============
main (初始提交)
 ↓
 ├── develop (从main创建)
 ├── club-management-dev (从main创建)
 ├── ProjectBid-dev (从main创建)
 └── Interviewer-dev (从main创建)
      ↓
      └── Interviewer_test_dev (从Interviewer-dev创建并推进开发)
```

### 分支说明

| 分支名称 | 用途 | 负责团队 |
|---------|------|----------|
| `main` | 生产环境稳定版本 | 项目负责人 |
| `develop` | 集成开发主线 | 技术负责人 |
| `club-management-dev` | 院校社团管理系统开发 | 社团管理团队 |
| `ProjectBid-dev` | 揭榜挂帅项目系统开发 | 项目平台团队 |
| `Interviewer-dev` | 企业AI面试官系统开发 | AI面试团队 |
| `Interviewer_test_dev` | AI面试官测试开发 | AI面试团队 |

### 当前开发状态

- **当前活跃分支**: `Interviewer_test_dev` (HEAD)
- **最新提交**: `5e0ef6a` - 新增个人知识库的dify外部引用（已部署）测试
- **基础提交**: `98ab340` - Initial commit (所有主要分支的起点)
- **远程仓库**: `git@github.com:TTKunn/GUET-InduEdu.git`
- **分支同步状态**: 所有分支已推送到远程仓库

### 分支开发进度

| 分支名称 | 状态 | 最新提交 | 开发进度 |
|---------|------|----------|----------|
| `main` | 🔒 稳定 | 98ab340 | 项目初始化 |
| `develop` | ⏸️ 待集成 | 98ab340 | 等待子系统合并 |
| `club-management-dev` | ⏳ 待开发 | 98ab340 | 院校社团管理系统 |
| `ProjectBid-dev` | ⏳ 待开发 | 98ab340 | 揭榜挂帅项目系统 |
| `Interviewer-dev` | 📝 基础完成 | 98ab340 | AI面试官系统基础 |
| `Interviewer_test_dev` | 🚀 活跃开发 | 5e0ef6a | AI面试测试功能 |

## 📁 项目目录结构

```
GUET-InduEdu/
├── Club-Management/          # 院校社团管理系统
│   ├── frontend/            # 前端应用
│   ├── backend/             # 后端API
│   └── docs/                # 系统文档
├── ProjectBid/              # 揭榜挂帅项目系统
│   ├── frontend/            # 前端应用
│   ├── backend/             # 后端API
│   └── docs/                # 系统文档
├── interviewer/             # 企业AI面试官系统
│   ├── frontend/            # 前端应用
│   ├── backend/             # 后端API
│   ├── ai-models/           # AI模型
│   └── test/                # 测试相关
├── shared/                  # 共享组件和工具
│   ├── components/          # 共享UI组件
│   ├── utils/               # 工具函数
│   └── configs/             # 配置文件
├── docs/                    # 项目文档
├── scripts/                 # 构建和部署脚本
└── README.md               # 项目说明
```

## 🚀 快速开始

### 环境要求

- Node.js 16+
- Python 3.8+
- Git 2.0+
- Docker (可选)

### 克隆项目

```bash
# 克隆项目
git clone git@github.com:TTKunn/GUET-InduEdu.git
cd GUET-InduEdu

# 查看所有分支
git branch -a

# 切换到开发分支
git checkout develop
```

### 开发流程

1. **功能开发**
   ```bash
   # 从对应子系统分支创建功能分支
   git checkout club-management-dev
   git checkout -b feature/club-new-feature

   # 开发完成后推送
   git push origin feature/club-new-feature
   ```

2. **代码集成**
   ```bash
   # 合并到子系统开发分支
   git checkout club-management-dev
   git merge feature/club-new-feature

   # 定期合并到develop分支
   git checkout develop
   git merge club-management-dev
   ```

## 🔧 技术栈

### 前端技术
- Vue.js 3.x
- Element Plus
- TypeScript
- Vite

### 后端技术
- Python FastAPI
- Node.js Express
- MySQL/PostgreSQL
- Redis

### AI技术
- OpenAI GPT
- 智谱AI
- 语音识别/合成
- 自然语言处理

### 部署技术
- Docker
- Nginx
- CI/CD Pipeline

## 👥 团队协作

### 开发团队

- **项目负责人**: 整体架构和进度管理
- **院校管理团队**: 社团管理系统开发
- **项目平台团队**: 揭榜挂帅系统开发
- **AI面试团队**: 智能面试系统开发

### 协作规范

1. **分支命名**: `feature/系统前缀-功能描述`
2. **提交信息**: 使用语义化提交规范
3. **代码审查**: 所有PR需要至少1人审查
4. **测试要求**: 新功能必须包含单元测试

## 📊 项目进展

### 当前状态

- ✅ 项目架构设计完成
- ✅ Git分支结构建立
- 🔄 AI面试官系统开发中
- ⏳ 院校管理系统待开发
- ⏳ 项目平台系统待开发

### 里程碑

- **Phase 1**: AI面试官MVP版本 (进行中)
- **Phase 2**: 院校管理系统开发
- **Phase 3**: 项目平台系统开发
- **Phase 4**: 系统集成与优化
- **Phase 5**: 生产环境部署

## 📝 文档链接

- [项目架构文档](./docs/architecture.md)
- [开发规范](./docs/development-guide.md)
- [API文档](./docs/api-reference.md)
- [部署指南](./docs/deployment.md)

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交代码
4. 创建 Pull Request
5. 等待代码审查

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系我们

- 项目仓库: https://github.com/TTKunn/GUET-InduEdu
- 问题反馈: [Issues](https://github.com/TTKunn/GUET-InduEdu/issues)
- 邮箱: [项目邮箱]

---

**桂林电子科技大学产教融合项目组**
*让AI技术赋能教育创新*
