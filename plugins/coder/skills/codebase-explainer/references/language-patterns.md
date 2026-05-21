# 语言识别规则参考

本文档定义 codebase-explainer skill 对各语言的入口、模块、依赖识别规则。

---

## Go

### 入口识别

| 特征 | 文件模式 |
|------|----------|
| 主程序入口 | `func main()` 在 `package main` 文件中 |
| 常见入口文件名 | `main.go`, `cmd/*/main.go`, `app.go` |

**识别命令**：
```bash
grep -r "func main()" --include="*.go"
grep -r "package main" --include="*.go"
```

### 模块识别

| 特征 | 说明 |
|------|------|
| `go.mod` | 模块定义文件，包含模块名和 Go 版本 |
| `package <name>` | 每个目录一个 package |
| 子模块 | `cmd/`, `internal/`, `pkg/` 目录结构 |

**目录结构惯例**：
- `cmd/`：主程序入口
- `internal/`：私有代码
- `pkg/`：公开库
- `api/`：API 定义

### 依赖提取

| 来源 | 说明 |
|------|----------|
| `go.mod` | 外部依赖清单 |
| `import` 语句 | 内部/外部依赖引用 |

---

## Python

### 入口识别

| 特征 | 文件模式 |
|------|----------|
| 主程序入口 | `if __name__ == "__main__":` |
| 包入口 | `__init__.py` 中的 `__all__` 或导出 |
| CLI 入口 | `pyproject.toml` 中的 `scripts` 或 `entry_points` |

**识别命令**：
```bash
grep -r "if __name__" --include="*.py"
grep -r "__all__" --include="*.py"
```

### 模块识别

| 特征 | 说明 |
|------|------|
| `__init__.py` | 包标识，目录成为 Python 包 |
| `setup.py` / `pyproject.toml` | 项目配置 |
| 目录结构 | 模块即目录 |

**目录结构惯例**：
- `src/<包名>/`：源码目录（现代风格）
- `<包名>/`：源码目录（传统风格）
- `tests/`：测试目录

### 依赖提取

| 来源 | 说明 |
|------|----------|
| `requirements.txt` | 外部依赖清单 |
| `pyproject.toml` dependencies | 现代依赖声明 |
| `import` 语句 | 依赖引用 |

---

## C

### 入口识别

| 特征 | 文件模式 |
|------|----------|
| 主程序入口 | `int main(int argc, char *argv[])` |
| 库入口 | 无入口，通过头文件导出 |
| 内核模块 | `module_init()` 宏 |

**识别命令**：
```bash
grep -r "int main" --include="*.c"
grep -r "module_init" --include="*.c"
```

### 模块识别

| 特征 | 说明 |
|------|------|
| `Makefile` / `CMakeLists.txt` | 构建配置，定义编译目标 |
| 头文件目录 | `include/`, `inc/` |
| 源文件目录 | `src/`, `lib/` |

### 依赖提取

| 来源 | 说明 |
|------|----------|
| `#include "..."` | 项目内部头文件 |
| `#include <...>` | 系统/外部库头文件 |
| `Makefile` | 链接依赖 (`-lxxx`) |

---

## JavaScript / TypeScript

### 入口识别

| 特征 | 文件模式 |
|------|----------|
| 主程序入口 | `package.json` 的 `main` 或 `scripts.start` |
| Node.js 入口 | `index.js`, `index.ts`, `app.js`, `app.ts`, `server.ts` |
| Web 前端入口 | `src/index.tsx`, `src/main.tsx`, `src/App.tsx` |

**框架入口模式**：

| 框架 | 入口特征 |
|------|----------|
| Express | `app.listen()`, `express()` 调用 |
| NestJS | `NestFactory.create()`, `@Module` 装饰器 |
| Next.js | `pages/` 或 `app/` 目录结构 |
| Fastify | `fastify.listen()`, `fastify()` 调用 |

**识别命令**：
```bash
# package.json 入口
grep -E '"main"|"scripts"' package.json

# tsconfig.json 配置
cat tsconfig.json | grep -E '"rootDir"|"outDir"|"entry"'

# 框架入口
grep -r "listen\|NestFactory\|express()" --include="*.ts" --include="*.js"
```

### 模块识别

| 特征 | 说明 |
|------|----------|
| `package.json` | 项目配置，定义 name、dependencies |
| `tsconfig.json` | TypeScript 配置，定义编译选项和路径映射 |
| `src/` 目录 | 源码目录 |
| ES Modules | `import`/`export` 语句 |
| CommonJS | `require`/`module.exports` |

**目录结构惯例**：

| 项目类型 | 目录结构 |
|---------|---------|
| Node.js 后端 | `src/`, `routes/`, `controllers/`, `services/`, `models/` |
| NestJS | `src/modules/`, `src/controllers/`, `src/services/` |
| Next.js | `pages/` 或 `app/`, `components/`, `lib/` |
| React SPA | `src/components/`, `src/hooks/`, `src/utils/` |

### 依赖提取

| 来源 | 说明 |
|------|----------|
| `package.json` dependencies | 外部依赖清单 |
| `package.json` devDependencies | 开发依赖 |
| `import` / `require` | 依赖引用 |
| `tsconfig.json` paths | 路径别名映射 |

**提取方式**：
```bash
# 外部依赖
cat package.json | grep -A 50 "dependencies"

# TypeScript 路径别名
cat tsconfig.json | grep -A 20 "paths"

# 内部 import
grep -r "from '\.\|from \"\." --include="*.js" --include="*.ts" --include="*.tsx"
```

---

## Bash

### 入口识别

| 特征 | 文件模式 |
|------|----------|
| 主脚本 | 脚本文件本身，通常无函数入口 |
| 函数入口 | 脚本末尾直接调用函数 |
| 库脚本 | 只定义函数，被 `source` 引用 |

### 模块识别

| 特征 | 说明 |
|------|------|
| 脚本文件 | 每个脚本通常是独立功能单元 |
| `scripts/` 目录 | 脚本集合 |
| 函数定义 | `function name()` 或 `name() {}` |

### 依赖提取

| 来源 | 说明 |
|------|----------|
| `source` / `.` | 引用其他脚本 |
| 命令调用 | 外部工具依赖 |

---

## 通用识别技巧

### 文件扫描命令集合
```bash
# 语言栈识别
find . -name "*.go" -o -name "*.py" -o -name "*.c" -o -name "*.js" -o -name "*.ts" -o -name "*.sh"

# 依赖扫描
grep -r "import\|require" --include="*.go" --include="*.py" --include="*.js" --include="*.ts"
grep -r "#include" --include="*.c" --include="*.h"
grep -r "source\|\." --include="*.sh"
```

### 目录结构通用惯例
| 目录 | 用途 |
|------|------|
| `cmd/` | 命令行入口 |
| `internal/` | 内部私有代码 |
| `pkg/` | 公开库 |
| `src/` | 源代码 |
| `tests/` | 测试代码 |
| `scripts/` | 构建/部署脚本 |
| `examples/` | 示例代码 |
| `docs/` | 文档 |