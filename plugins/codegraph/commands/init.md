---
name: init
description: 在当前项目初始化 codegraph 索引，构建代码知识图谱
---

运行以下命令在项目目录创建 `.codegraph/` 知识图谱索引：

```bash
codegraph init -i
```

此命令会：
1. 创建 `.codegraph/` 目录
2. 使用 tree-sitter 解析所有支持的源代码文件
3. 提取符号（函数、类、方法）和关系（调用、导入、继承）
4. 存储到本地 SQLite 数据库

完成后可使用 MCP 工具（codegraph_search、codegraph_context 等）进行代码查询。