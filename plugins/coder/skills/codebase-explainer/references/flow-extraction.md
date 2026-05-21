# 流程提取策略

从代码中提取核心业务流程、数据流向和调用链的策略。

## 概述

流程提取是代码理解的关键环节，目标是：
1. 识别核心业务流程
2. 跟踪数据从输入到输出的路径
3. 提取关键函数调用链

**原则**：
- 从入口跟踪，而非从任意位置开始
- 关注高频调用路径，而非所有路径
- 优先提取业务逻辑，而非技术细节

## 入口跟踪方法

### 通用流程图

```
┌─────────────┐
│  入口点     │
│ (Handler)   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  函数解析   │
│  参数分析   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  逐层展开   │
│  调用链跟踪 │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  边界识别   │
│  外部/内部  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  生成调用链 │
│  文档输出   │
└─────────────┘
```

### 跟踪步骤

| 步骤 | 说明 | 输出 |
|------|------|------|
| 1. 识别入口 | 定位请求/事件处理函数 | 入口函数名、文件路径 |
| 2. 解析函数 | 分析函数参数、返回值、依赖 | 函数签名、依赖列表 |
| 3. 逐层展开 | 追踪每一次函数调用 | 调用栈、执行顺序 |
| 4. 标记边界 | 区分内部/外部调用 | 边界标记、调用类型 |
| 5. 生成调用链 | 整合为完整调用链 | 调用链文档 |

### 边界识别

| 边界类型 | 标识特征 | 处理方式 |
|----------|----------|----------|
| 外部库 | 第三方依赖包 | 标记为外部边界，不展开 |
| 系统调用 | OS 级操作 (open,读写等) | 标记为系统边界 |
| 数据层 | DB/缓存操作 | 提取为数据层调用 |
| 网络层 | HTTP/gRPC 请求 | 标记为外部服务调用 |

## Go 流程提取规则

### 入口跟踪示例代码

```go
// HTTP 入口
router.HandleFunc("/api/users", handleUsers).Methods("GET")

// 消息队列入口
go func() {
    for msg := range queue.Chan() {
        processMessage(msg)
    }
}()

// 定时任务入口
func StartScheduledTask() {
    ticker := time.NewTicker(5 * time.Minute)
    for range ticker.C {
        runBatchJob()
    }
}
```

### 关键模式

| 模式 | 示例 | 说明 |
|------|------|------|
| Router 注册 | `router.HandleFunc("/path", handler)` | HTTP 请求入口 |
| 并发启动 | `go func() { ... }()` | 异步任务入口 |
| 通道处理 | `for msg := range ch` | 消息队列消费 |
| 定时任务 | `time.NewTicker()` | 周期性任务 |
| `defer` | `defer mu.Unlock()` | 资源清理时机 |
| `chan` 操作 | `ch <- data`, `<-ch` | 并发同步点 |

### 数据层识别

Go 项目中常见的数据层模式：
- `db.Query()`, `db.Exec()` - SQL 数据库
- `redis.Get()`, `redis.Set()` - Redis 缓存
- `c.DB()` - GORM 数据库操作
- `mgo.collection.Find()` - MongoDB

## Python 流程提取规则

### 入口跟踪示例代码

```python
# Flask 路由入口
@app.route('/api/users', methods=['GET'])
def get_users():
    return Users.query.all()

# FastAPI 路由入口
@router.get("/api/users")
async def read_users():
    return await db.fetch_all("SELECT * FROM users")

# 异步任务入口
async def process_background(job: Job):
    await execute(job)

# 类方法入口
class UserService:
    def get_user(self, user_id: int) -> User:
        return Session.query(User).get(user_id)
```

### 关键模式

| 模式 | 示例 | 说明 |
|------|------|------|
| Flask 路由 | `@app.route('/path')` | Flask 请求入口 |
| FastAPI 路由 | `@router.get("/path")` | FastAPI 请求入口 |
| 异步函数 | `async def func()` | 异步任务入口 |
| 类方法 | `class cls: def method()` | 面向对象入口 |
| 装饰器 | `@decorator` | 功能增强包装 |

### 数据层识别

Python 项目中常见的数据层模式：
- `session.query()`, `db.execute()` - SQLAlchemy
- `redis.get()`, `redis.set()` - Redis
- `collection.find()`, `collection.insert()` - PyMongo
- `cursor.execute()` - 原生数据库连接

## 数据流向提取方法

### 数据流模式图

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   输入层    │────▶│   处理层    │────▶│   输出层    │
│ (Source)    │     │ (Transform) │     │ (Sink)      │
└─────────────┘     └─────────────┘     └─────────────┘
      │                    │                  │
      ▼                    ▼                  ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ HTTP 请求   │     │ 业务逻辑    │     │ HTTP 响应   │
│ 消息队列    │     │ 数据转换    │     │ 数据库写入  │
│ 文件输入    │     │ 计算处理    │     │ 缓存更新    │
└─────────────┘     └─────────────┘     └─────────────┘
```

### 输入识别

| 输入类型 | Go 标识 | Python 标识 |
|----------|---------|---------------|
| HTTP | `r.Body`, `form.Value` | `request.json`, `request.query` |
| 消息队列 | `msg := <-ch` | `consumer.consume()` |
| 定时任务 | `ticker.C` | `asyncio.sleep()` |
| 文件 | `os.Open()`, `ioutil.ReadFile()` | `open()`, `read()` |

### 处理识别

| 处理类型 | Go 特征 | Python 特征 |
|----------|---------|---------------|
| 数据验证 | `validate.Struct()` | `pydantic.validate()` |
| 业务计算 | 自定义计算逻辑 | 业务函数调用 |
| 数据转换 | 类型转换、映射 | map/filter comprehension |
| 权限检查 | `checkPermission()` | `@require_role` |

### 输出识别

| 输出类型 | Go 标识 | Python 标识 |
|----------|---------|---------------|
| HTTP 响应 | `w.Write()`, `json.NewEncoder()` | `Response()`, `return` |
| 数据库 | `db.Exec()`, `tx.Commit()` | `session.commit()`, `execute()` |
| 日志 | `log.Info()`, `fmt.Print()` | `logging.info()`, `print()` |
| 消息队列 | `ch <- msg` | `producer.send()` |

### 数据模型跟踪要点

1. **定义位置**：记录结构体/类定义文件路径
2. **转换链条**：跟踪数据格式的每次转换
3. **空值处理**：标记可能的 nil/None 处理点
4. **类型校验**：记录类型转换和校验逻辑

### 各语言数据模型识别特征

| 语言 | 数据模型特征 | 识别方式 |
|------|--------------|----------|
| Go | `type StructName struct {}` | `grep "type.*struct"` |
| Python | `class ClassName:` / `@dataclass` | `grep "class\|@dataclass"` |
| C | `struct StructName {};` / `typedef struct` | `grep "struct\|typedef"` |
| JavaScript/TypeScript | `interface IName {}` / `type TName =` / `class ClassName {}` | `grep "interface\|type.*=\|class"` |
| Bash | 无结构化类型，变量名约定 | 分析变量赋值 |

**Go 数据模型示例**：
```go
type User struct {
    ID       int       `json:"id"`
    Name     string    `json:"name"`
    Email    string    `json:"email"`
    Created  time.Time `json:"created_at"`
}
```

**Python 数据模型示例**：
```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
```

**TypeScript 数据模型示例**：
```typescript
interface User {
  id: number;
  name: string;
  email: string;
  createdAt: Date;
}

// 或使用 type
type User = {
  id: number;
  name: string;
  email: string;
  createdAt: Date;
};
```

## 调用链生成方法

### 调用链格式示例

```
HTTP GET /api/users
├─ handlerUsers (handlers/users.go:23)
│  ├─ validateUserRequest (utils/validator.go:45)
│  ├─ userService.GetUsers (service/user.go:67)
│  │  ├─ db.QueryContext (db/query.go:12)
│  │  └─ redis.Get (cache/redis.go:89)
│  └─ formatUserResponse (handlers/formatter.go:34)
└─ json.NewEncoder(w).Encode (encoding/json.go:156)
```

### 简化规则

| 规则 | 说明 | 示例 |
|------|------|------|
| 跳过辅助函数 | 简单 getter/setter 不展开 | `getUserID()` |
| 合并相似调用 | 连续相同类型调用合并 | 多次 DB 查询合并 |
| 标注外部边界 | 外部库操作标记说明 | `[外部] Redis.Get()` |

### 深度控制

| 项目规模 | 推荐深度 | 说明 |
|----------|----------|------|
| 小型项目 (≤10 文件) | 5-7 层 | 保持完整细节 |
| 中型项目 (10-50 文件) | 3-5 层 | 平衡细节与可读性 |
| 大型项目 (>50 文件) | 2-3 层 | 仅展示关键路径 |
