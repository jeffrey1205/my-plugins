---
name: lsp-setup
description: 交互式安装语言服务器和开发工具，支持 C/C++、Go、TypeScript/JS、Python、Bash、HTML/CSS/JSON
---

# LSP 安装

检测并安装语言服务器和开发工具。

## 支持的语言和工具

**按语言分组**：

### 1. C/C++（apt）
- clangd: C/C++ 语言服务器
- 安装命令: `sudo apt install clangd`
- 验证命令: `clangd --version`

### 2. Go（go install）
**安装前设置代理**：`go env -w GOPROXY=https://goproxy.cn,direct`

**工具列表**：
- gopls: Go 语言服务器
- dlv: Go 调试器
- golangci-lint: Go linter
- gotests: 测试生成
- impl: 接口实现
- goplay: Go playground

**安装命令**（批量）：
```bash
go env -w GOPROXY=https://goproxy.cn,direct
tools=(
    "golang.org/x/tools/gopls"
    "github.com/go-delve/delve/cmd/dlv"
    "github.com/golangci/golangci-lint/cmd/golangci-lint"
    "github.com/cweill/gotests/gotests"
    "github.com/josharian/impl"
    "github.com/haya14busa/goplay/cmd/goplay"
)
for tool in "${tools[@]}"; do
    go install "$tool@latest"
done
```

**验证命令**: `gopls version`

### 3. TypeScript/JavaScript（npm）
- typescript-language-server: TypeScript/JS 语言服务器
- 安装命令: `npm install -g typescript typescript-language-server`
- 验证命令: `typescript-language-server --version`

### 4. Python（npm）
- basedpyright: Python 语言服务器（比 pyright 更强）
- 安装命令: `npm install -g basedpyright`
- 验证命令: `basedpyright --version`

### 5. Bash（npm）
- bash-language-server: Bash 语言服务器
- shellcheck: Shell 静态分析
- 安装命令: `npm install -g bash-language-server shellcheck`
- 验证命令: `bash-language-server --version`

### 6. HTML/CSS/JSON（npm）
- vscode-langservers-extracted: HTML、CSS、JSON 语言服务器集合
- 安装命令: `npm install -g @zed-industries/vscode-langservers-extracted`
- 验证命令: `vscode-html-language-server --version`

## 执行流程

**步骤 1：询问用户**
- 向用户展示上述语言分组
- 询问："请选择要安装的语言（可多选），例如：Go、Python、C/C++"

**步骤 2：检测已安装状态**
- 对用户选择的语言，运行对应的验证命令检测是否已安装
- 如果已安装，询问用户是否需要重新安装

**步骤 3：执行安装**
- Go: 先设置 GOPROXY，再批量安装工具
- C/C++: 执行 apt install（可能需要 sudo）
- 其他语言: 执行 npm install -g

**步骤 4：验证安装成功**
- 运行验证命令确认安装成功
- 显示安装的版本信息

## 参数

- 用户可直接指定语言，如 "/coder:lsp-setup Go Python"
- 系统仅支持 Debian/apt，不支持 macOS/Windows