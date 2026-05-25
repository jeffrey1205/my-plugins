---
name: reindex
description: 全量重建当前项目的代码索引（清除旧索引后重建）
model: haiku
effort: low
---

执行 `codegraph index --force` 全量重建索引：
- 清除现有索引
- 重新解析所有源文件
- 重建知识图谱

适用于索引损坏或大规模重构后需要完全重建的场景。日常更新请使用 `/codegraph:sync`。
