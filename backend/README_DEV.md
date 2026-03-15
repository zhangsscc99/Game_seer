# Game Seer Backend – 开发启动指南

## 环境要求

- Python 3.10+
- pip

## 快速启动

### 1. 进入 backend 目录

```bash
cd backend
```

### 2. 创建并激活虚拟环境

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

> 注意：`core/config.py` 使用 `pydantic-settings`，需要单独安装：
>
> ```bash
> pip install pydantic-settings
> ```

### 4. 配置环境变量

复制 `.env.example` 为 `.env` 并填写值：

```bash
cp .env.example .env
```

`.env` 内容示例：

```
SECRET_KEY=change-this-to-a-long-random-string
DATABASE_URL=sqlite:///./game_seer.db
```

生成安全的 SECRET_KEY：

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. 启动开发服务器

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

首次启动时会自动执行 `Base.metadata.create_all()`，在当前目录生成 `game_seer.db`。

### 6. 访问 API 文档

- Swagger UI：http://localhost:8000/docs
- ReDoc：http://localhost:8000/redoc

---

## 项目结构说明

| 目录 / 文件 | 说明 |
|---|---|
| `main.py` | FastAPI 入口，注册路由、CORS、静态文件 |
| `core/config.py` | pydantic-settings 读取 `.env` 配置 |
| `core/database.py` | SQLAlchemy engine、SessionLocal、Base、get_db |
| `core/security.py` | 密码 hash/verify、JWT 签发与解析 |
| `models/` | SQLAlchemy ORM 模型 |
| `schemas/` | Pydantic 请求/响应 schema |
| `routers/` | 各业务路由（auth/tasks/elves/boss/profile/achievements） |
| `services/` | 业务逻辑（奖励结算、连续天数、Boss 挑战） |
| `static/elves/` | 精灵图片静态资源目录 |

## API 端点概览

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/api/v1/auth/register` | 注册 |
| POST | `/api/v1/auth/login` | 登录，返回 JWT |
| GET | `/api/v1/auth/me` | 当前用户信息 |
| GET | `/api/v1/tasks/` | 任务列表（支持 type/status 筛选） |
| POST | `/api/v1/tasks/` | 创建任务 |
| PUT | `/api/v1/tasks/{id}` | 更新任务 |
| DELETE | `/api/v1/tasks/{id}` | 删除任务 |
| POST | `/api/v1/tasks/{id}/complete` | 完成任务，结算奖励 |
| GET | `/api/v1/elves/` | 精灵图鉴 |
| GET | `/api/v1/elves/{id}` | 精灵详情 |
| GET | `/api/v1/elves/my` | 我的精灵 |
| POST | `/api/v1/elves/my/{template_id}` | 解锁精灵 |
| PUT | `/api/v1/elves/my/{id}/active` | 设为主战精灵 |
| GET | `/api/v1/boss/` | Boss 列表 |
| GET | `/api/v1/boss/{id}` | Boss 详情 |
| POST | `/api/v1/boss/{id}/challenge` | 挑战 Boss |
| GET | `/api/v1/profile/` | 个人资料 |
| GET | `/api/v1/profile/stats` | 任务统计 |
| GET | `/api/v1/achievements/` | 全部成就 |
| GET | `/api/v1/achievements/my` | 我的成就 |

## 数据库迁移（Alembic）

项目已安装 alembic，如需管理迁移：

```bash
alembic init alembic
# 修改 alembic.ini 中的 sqlalchemy.url 或在 env.py 中读取 .env
alembic revision --autogenerate -m "init"
alembic upgrade head
```

开发阶段也可直接依赖启动时的 `create_all`，无需配置 alembic。
