# 用户认证服务 (User Authentication Service)

## 概述

用户认证服务是智能面试系统的核心认证模块，提供用户注册、登录、token管理等功能。采用JWT认证机制，支持access token和refresh token双token模式。

## 技术栈

- **框架**: FastAPI 0.104.1
- **数据库**: MySQL (通过SQLAlchemy ORM)
- **认证**: JWT (PyJWT)
- **密码加密**: bcrypt
- **服务器**: Uvicorn
- **Python版本**: 3.10+

## 项目结构

```
user-auth-service/
├── main.py                 # FastAPI应用入口
├── config.py              # 配置管理
├── models.py              # 数据模型定义
├── database.py            # 数据库操作
├── auth_service.py        # 认证业务逻辑
├── auth/
│   ├── auth_handler.py    # JWT处理器
│   └── auth_bearer.py     # JWT中间件
├── requirements.txt       # 依赖列表
├── .env                   # 环境配置
├── start.sh              # 启动脚本
├── stop.sh               # 停止脚本
└── README.md             # 项目文档
```

## 快速开始

### 1. 环境准备

确保已安装Python 3.10+和MySQL数据库。

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境

复制并编辑 `.env` 文件：

```bash
cp .env.example .env
# 编辑数据库连接等配置
```

### 4. 启动服务

```bash
# 使用启动脚本（推荐）
./start.sh

# 或直接启动
python3 main.py
```

### 5. 验证服务

访问 http://localhost:8007/health 检查服务状态。

## API接口文档

### 基础信息

- **服务地址**: http://localhost:8007
- **API文档**: http://localhost:8007/docs
- **健康检查**: http://localhost:8007/health

### 认证接口

#### 1. 用户注册

**POST** `/auth/register`

请求体：
```json
{
  "username": "testuser",
  "email": "test@example.com", 
  "password": "password123"
}
```

响应：
```json
{
  "success": true,
  "message": "注册成功",
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "user_id": "uuid",
    "username": "testuser",
    "email": "test@example.com",
    "is_active": true,
    "is_verified": false,
    "created_at": "2025-09-10T20:00:00",
    "last_login_at": null
  }
}
```

#### 2. 用户登录

**POST** `/auth/login`

请求体：
```json
{
  "username": "testuser",  // 支持用户名或邮箱
  "password": "password123"
}
```

响应：同注册接口

#### 3. 刷新Token

**POST** `/auth/refresh`

请求体：
```json
{
  "refresh_token": "eyJ..."
}
```

响应：
```json
{
  "success": true,
  "message": "Token刷新成功",
  "access_token": "eyJ...",
  "expires_in": 1800
}
```

#### 4. 获取当前用户信息

**GET** `/auth/me`

请求头：
```
Authorization: Bearer <access_token>
```

响应：
```json
{
  "user_id": "uuid",
  "username": "testuser",
  "email": "test@example.com",
  "is_active": true,
  "is_verified": false,
  "created_at": "2025-09-10T20:00:00",
  "last_login_at": "2025-09-10T20:30:00"
}
```

#### 5. 用户登出

**POST** `/auth/logout`

请求头：
```
Authorization: Bearer <access_token>
```

响应：
```json
{
  "success": true,
  "message": "登出成功"
}
```

### 系统接口

#### 健康检查

**GET** `/health`

响应：
```json
{
  "status": "healthy",
  "timestamp": "2025-09-10T20:00:00.000000",
  "service": "user-auth-service",
  "version": "1.0.0",
  "database_connected": true,
  "error": null
}
```

## 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `MYSQL_URL` | MySQL连接字符串 | - |
| `JWT_SECRET_KEY` | JWT密钥 | - |
| `JWT_ALGORITHM` | JWT算法 | HS256 |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Access Token过期时间(分钟) | 30 |
| `JWT_REFRESH_TOKEN_EXPIRE_DAYS` | Refresh Token过期时间(天) | 7 |
| `API_HOST` | 服务监听地址 | 0.0.0.0 |
| `API_PORT` | 服务端口 | 8007 |

## 数据库设计

### users表

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | INT | 主键，自增 |
| `user_id` | VARCHAR(36) | 用户UUID，唯一 |
| `username` | VARCHAR(50) | 用户名，唯一 |
| `email` | VARCHAR(100) | 邮箱，唯一 |
| `password_hash` | VARCHAR(255) | 密码哈希 |
| `is_active` | BOOLEAN | 是否激活 |
| `is_verified` | BOOLEAN | 是否验证邮箱 |
| `created_at` | DATETIME | 创建时间 |
| `updated_at` | DATETIME | 更新时间 |
| `last_login_at` | DATETIME | 最后登录时间 |

## 部署说明

### 生产环境部署

1. 修改 `.env` 配置文件
2. 使用 `./start.sh` 启动服务
3. 配置反向代理（如Nginx）
4. 设置进程管理（如systemd）

### Docker部署

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8007
CMD ["python3", "main.py"]
```

## 开发指南

### 添加新的API接口

1. 在 `models.py` 中定义请求/响应模型
2. 在 `auth_service.py` 中实现业务逻辑
3. 在 `main.py` 中添加路由
4. 更新文档

### 数据库迁移

使用SQLAlchemy的自动建表功能，或手动执行SQL脚本。

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查MySQL服务是否启动
   - 验证连接字符串配置
   - 确认数据库权限

2. **JWT Token无效**
   - 检查密钥配置
   - 验证token格式
   - 确认过期时间设置

3. **端口被占用**
   - 使用 `./stop.sh` 停止现有服务
   - 或修改端口配置

## 版本历史

- **v1.0.0** (2025-09-10)
  - 初始版本发布
  - 支持用户注册、登录、token管理
  - 完整的JWT认证机制

## 许可证

MIT License

## 联系方式

如有问题，请联系开发团队。
