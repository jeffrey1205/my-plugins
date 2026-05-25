---
name: setup
description: Download and install RTK (Rust Token Killer) binary globally
model: haiku
effort: low
---

检测并安装 RTK。如果已安装，询问用户是否需要重新安装。

**执行步骤**：

1. 先检测 RTK 是否已安装：运行 `rtk --version`
2. 如果已安装，询问用户："RTK 已安装（版本 X），是否重新安装？"
3. 根据用户回答执行：
   - 重新安装：`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/setup-rtk.py" --force`
   - 跳过安装：告知用户已安装完成
   - 未安装：`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/setup-rtk.py"`

**参数**：
- `--force`：强制重新安装（即使已安装）

该脚本会：
- 通过 curl 下载安装脚本（90s 超时）
- 验证安装成功

Hook 已通过插件 hooks/hooks.json 自动配置，无需手动设置。
