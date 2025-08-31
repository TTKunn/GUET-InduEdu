# GUET-InduEdu 产教融合项目

桂林电子科技大学产教融合项目：大规模人工智能模型在教育教学领域的应用与创新实践

## 📋 项目概述

本项目是桂林电子科技大学的产教融合创新项目，旨在将大规模人工智能模型技术应用于教育教学领域，构建智能化的教育生态系统。项目包含三个核心子系统，实现院校管理、项目协作和智能面试的全流程数字化。

**项目相关资料和部分学长代码见群文件**

## 🏗️ 项目架构

### 三大核心子系统

1. **院校社团管理系统** (`Club-Management/`)
   - 学生端：浏览社团、申请加入，查看公告活动，参与考勤与活动。
   - 社团负责人：管理社团信息、成员、考勤，发布公告活动，申报成果。
   - 管理员：审核社团、公告、活动及成果，管理分类、用户与数据。
   - 多端协同：Web端供管理员和负责人使用，小程序端服务学生。
   - 技术上可以参考结合BI数据分析相关内容和Text2Sql相关内容

2. **揭榜挂帅项目系统** (`ProjectBid/`)
   - 先搞基本的项目发布、申请、评审的信息化流程
   - 需求解析：基于大模型提取企业项目书技术指标（如 “熟练使用java语言”），构建技术标签的能力图谱。
   - 智能匹配：学生端支持 一键智能匹配，企业端可按 “专业排名”“竞赛获奖经历” 等条件进行筛选
   - 游戏化激励：设置多级挂帅段位。
   - 全流程管理：覆盖 “如项目发布、承接、申报、评审等核心内容” 闭环。

3. **企业AI面试官系统** (`interviewer/`)
   - 用户的登录注册及个人信息维护
   - 公司题库面试模块，大模型基于用户所选择的公司，智能的生成相关的定制化面试题
   - 自选知识点面试模块，用户可以根据自己需要准备的技术知识点或技能关键词来设定面试题
   - 薄弱知识点强化面试模块，系统则根据用户的回答情况，形成用户错题册，从错题册出发智能识别用户的薄弱点，生成相对应的专项训练题

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

当前分支创建关系：
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

| 分支名称 | 用途 |
|---------|------|
| `main` | 生产环境稳定版本 |
| `develop` | 集成开发主线 |
| `club-management-dev` | 院校社团管理系统开发 |
| `ProjectBid-dev` | 揭榜挂帅项目系统开发 |
| `Interviewer-dev` | 企业AI面试官系统开发 |
| `Interviewer_test_dev` | 企业AI面试官系统开发测试 |

### 当前开发状态

- **当前活跃分支**: `Interviewer_test_dev` (HEAD)
- **最新提交**: `5e0ef6a` - 新增个人知识库的dify外部引用（已部署）测试
- **基础提交**: `98ab340` - Initial commit (所有主要分支的起点)
- **远程仓库**: `git@github.com:TTKunn/GUET-InduEdu.git`
- **分支同步状态**: 所有分支已推送到远程仓库

### 分支开发进度

## 📁 项目目录结构

> 仅供参考，尽量规范保证不冲突不混乱即可

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

## 📋 开发规范

### 团队分工

| 团队 | 负责系统 | 主要分支 |
|------|----------|----------|
| **项目负责人** | 整体架构和进度管理 | `main`, `develop` |
| **院校管理团队** | 社团管理系统 | `club-management-dev` |
| **项目平台团队** | 揭榜挂帅系统 | `ProjectBid-dev` |
| **AI面试团队** | 智能面试系统 | `Interviewer-dev` |

### 分支管理规范

#### 🌿 分支命名规范

```plaintext
分支类型和命名：
===============

主要分支：
├── main                    # 生产环境，禁止直接推送
├── develop                 # 集成开发主线
├── {system}-dev           # 子系统开发分支
└── hotfix/{bug-name}      # 紧急修复分支

功能分支：
├── feature/{system}-{function}     # 功能开发
├── bugfix/{system}-{bug-name}      # Bug修复
├── test/{system}-{test-name}       # 测试分支
└── docs/{doc-name}                 # 文档更新

示例：
├── feature/club-user-management    # 院校系统用户管理
├── feature/bid-project-publish     # 项目系统发布功能
├── feature/ai-voice-interaction    # AI系统语音交互
├── bugfix/club-login-error         # 院校系统登录Bug
└── test/ai-interview-flow          # AI面试流程测试
```

#### 🔄 标准开发流程

#### ⚠️ 重要注意事项

```plaintext
常见误操作防范：
===============

❌ 错误操作：
├── 直接在main分支开发
├── 忘记pull就push导致冲突
├── 在错误的分支上开发
├── 提交信息不规范
└── 删除了重要分支

✅ 正确做法：
├── 开发前确认当前分支：git branch
├── 推送前先拉取：git pull origin {branch}
├── 提交前检查状态：git status
├── 合并前备份分支：git branch backup-{branch}
└── 重要操作前先沟通
```

### Git操作规范

#### 📝 提交信息规范

> 看看就行，不要用太抽象的comment，看不懂的

```bash
# 提交信息格式：{type类型}({scope影响模块}): {description描述}

# type类型说明：
feat:     新功能
fix:      Bug修复
docs:     文档更新
style:    代码格式调整
refactor: 代码重构
test:     测试相关
chore:    构建/工具相关

# 示例：
git commit -m "feat(club): 添加社团注册功能"
git commit -m "fix(ai): 修复语音识别异常问题"
git commit -m "docs: 更新API文档"
git commit -m "refactor(bid): 重构项目发布模块"
```

#### 🔍 代码提交检查清单

```plaintext
提交前必检项：
=============

□ 确认当前分支正确
□ 代码已测试无明显错误
□ 提交信息符合规范
□ 没有提交敏感信息（密码、密钥等）
□ 没有提交临时文件和调试代码
□ 大文件已添加到.gitignore

推送前必检项：
=============

□ 执行 git pull 获取最新代码
□ 解决所有合并冲突
□ 本地测试通过
□ 确认推送到正确分支
```

#### 🚨 冲突解决流程

```bash
# 当出现合并冲突时：

# 1. 拉取最新代码
git pull origin {branch}
# 如果有冲突，Git会提示冲突文件

# 2. 手动解决冲突
# 编辑冲突文件，删除冲突标记：
# <<<<<<< HEAD
# 你的代码
# =======
# 别人的代码
# >>>>>>> commit-hash

# 3. 标记冲突已解决
git add {conflict-file}

# 4. 完成合并
git commit -m "resolve: 解决合并冲突"

# 5. 推送
git push origin {branch}
```

### 协作规范

#### 👥 代码审查/Pull Request规范

```plaintext
Pull Request规范：
=================

PR标题格式：
[{system}] {type}: {description}

PR描述模板：
## 功能描述
- 实现了什么功能
- 解决了什么问题

## 修改内容
- [ ] 前端界面
- [ ] 后端API
- [ ] 数据库结构
- [ ] 文档更新

## 测试情况
- [ ] 单元测试通过
- [ ] 功能测试通过
- [ ] 兼容性测试通过

## 注意事项
- 需要特别关注的地方
- 可能的风险点
```


## 📊 项目进展

### 当前状态

- ✅ 项目架构设计完成
- ✅ Git分支结构建立
- 🔄 AI面试官系统开发中
- ⏳ 院校管理系统待开发
- ⏳ 项目平台系统待开发

## 📝 文档链接（待补充）

- [项目架构文档](./docs/architecture.md)
- [开发规范](./docs/development-guide.md)
- [API文档](./docs/api-reference.md)
- [部署指南](./docs/deployment.md)

---

**桂林电子科技大学产教融合项目组**
*让AI技术赋能教育创新*
