# CodeGraph Plugin

代码图谱MCP服务器，为 Claude Code 提供语义代码理解能力。

## 功能

- **语义搜索**：按名称快速查找符号（函数、类、方法）
- **调用图分析**：追踪调用者和被调用者
- **影响分析**：分析修改代码的影响范围
- **代码上下文**：一键获取相关代码片段
- **支持 19+ 语言**：TypeScript、JavaScript、Python、Go、Rust、Java、C#、PHP、Ruby、C、C++、Swift、Kotlin、Scala、Dart、Svelte、Vue、Liquid、Pascal/Delphi、Lua、Luau

## 使用方法

### 1. 安装 CLI

```bash
/codegraph:install
```

或手动安装：
```bash
npm i -g @colbymchenry/codegraph
```

### 2. 初始化项目索引

```bash
/codegraph:init
```

### 3. 同步索引

代码变更后，增量更新索引：

```bash
/codegraph:sync
```

### 4. 使用 MCP 工具

初始化并同步后，以下 MCP 工具会自动可用：

| 工具 | 用途 |
|------|------|
| `codegraph_search` | 按名称搜索符号 |
| `codegraph_context` | 构建任务相关代码上下文 |
| `codegraph_trace` | 追踪两个符号间的调用路径 |
| `codegraph_callers` | 查找调用者 |
| `codegraph_callees` | 查找被调用者 |
| `codegraph_impact` | 分析修改影响范围 |
| `codegraph_explore` | 批量获取相关符号源码 |
| `codegraph_node` | 获取单个符号详情 |
| `codegraph_files` | 获取项目文件结构 |
| `codegraph_status` | 获取索引状态 |

## 其他命令

- `/codegraph:status` - 查看索引状态
- `/codegraph:reindex` - 全量重建索引（索引损坏或大规模重构后使用）

## 参考资料

- [CodeGraph 官方文档](https://colbymchenry.github.io/codegraph/)
- [GitHub 仓库](https://github.com/colbymchenry/codegraph)
