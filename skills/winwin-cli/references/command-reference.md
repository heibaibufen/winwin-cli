# winwin-cli 命令参考

完整的 winwin-cli 命令行工具参考手册。

## 目录

- [主命令](#主命令)
- [convert 命令](#convert-命令)
- [kb-search 命令](#kb-search-命令)
- [skills 命令](#skills-命令)
- [退出码](#退出码)
- [环境变量](#环境变量)

## 主命令

### winwin-cli

```bash
winwin-cli [OPTIONS] COMMAND [ARGS]...
```

**选项**：
- `--version`：显示版本号并退出
- `--help`：显示帮助信息并退出

**子命令**：
- `convert`：文档转换
- `kb-search`：知识库检索
- `skills`：技能管理

## convert 命令

### winwin-cli convert

```bash
winwin-cli convert [OPTIONS] INPUT_PATH
```

**参数**：
- `INPUT_PATH`：输入文件或目录路径（必需）

**选项**：
- `-o, --output PATH`：输出目录或文件路径（可选）
- `-e, --ext TEXT`：文件扩展名过滤（可多次使用）
- `-f, --overwrite`：覆盖已存在的 Markdown 文件

**退出码**：
- `0`：成功
- `1`：转换失败

### 使用示例

```bash
# 转换单个文件
winwin-cli convert document.docx

# 指定输出路径
winwin-cli convert document.docx -o output.md

# 批量转换
winwin-cli convert ./docs -o ./markdown

# 过滤扩展名
winwin-cli convert ./docs --ext .pdf --ext .docx

# 覆盖已存在文件
winwin-cli convert ./docs --overwrite
```

## kb-search 命令

### winwin-cli kb-search add

```bash
winwin-cli kb-search add [PATH] --name [NAME]
```

**参数**：
- `PATH`：文档目录路径（必需）
- `--name NAME`：知识库名称（必需）

### winwin-cli kb-search remove

```bash
winwin-cli kb-search remove [KB_NAME]
```

**参数**：
- `KB_NAME`：知识库名称（必需）

### winwin-cli kb-search enable/disable

```bash
winwin-cli kb-search enable [KB_NAME]
winwin-cli kb-search disable [KB_NAME]
```

**参数**：
- `KB_NAME`：知识库名称（必需）

### winwin-cli kb-search index

```bash
winwin-cli kb-search index [KB_NAME]
```

**参数**：
- `KB_NAME`：知识库名称（可选，默认所有）

### winwin-cli kb-search search

```bash
winwin-cli kb-search search [OPTIONS] [QUERY]
```

**参数**：
- `QUERY`：搜索关键词（可选）

**选项**：
- `-k, --kb TEXT`：指定知识库（默认：所有启用的知识库）
- `-l, --limit INTEGER`：最大结果数（默认：10）
- `-j, --json`：JSON 输出
- `-c, --content`：返回完整内容

### winwin-cli kb-search list

```bash
winwin-cli kb-search list
```

显示所有知识库列表。

### winwin-cli kb-search status

```bash
winwin-cli kb-search status
```

显示知识库状态信息。

### winwin-cli kb-search info

```bash
winwin-cli kb-search info
```

显示系统信息。

## skills 命令

### winwin-cli skills list

```bash
winwin-cli skills list [--json]
```

**选项**：
- `--json`：以 JSON 格式输出

### winwin-cli skills info

```bash
winwin-cli skills info [SKILL_NAME]
```

**参数**：
- `SKILL_NAME`：技能名称（必需）

### winwin-cli skills install

```bash
winwin-cli skills install [SKILL_NAME] [PATH] [OPTIONS]
```

**参数**：
- `SKILL_NAME`：技能名称（可选）
- `PATH`：安装路径（可选，默认当前目录）

**选项**：
- `--platform [claude-code|opencode]`：目标平台

## 退出码

所有 winwin-cli 命令使用标准退出码：

| 退出码 | 含义 |
|--------|------|
| 0 | 成功 |
| 1 | 一般错误 |
| 2 | 参数错误 |
| 127 | 命令未找到 |

## 错误处理

### 标准错误输出

错误信息输出到 stderr：

```bash
winwin-cli convert document.docx 2>&1
```

### 检查退出码

```bash
winwin-cli convert document.docx
if [ $? -eq 0 ]; then
    echo "成功"
else
    echo "失败"
fi
```

### Python 错误处理

```python
import subprocess

result = subprocess.run(
    ["winwin-cli", "convert", "document.docx"],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print(f"错误: {result.stderr}")
    sys.exit(1)
```

## 环境变量

winwin-cli 支持以下环境变量：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `WINWIN_CLI_HOME` | 配置目录 | `~/.winwin-cli` |
| `WINWIN_CLI_LOG_LEVEL` | 日志级别 | `INFO` |
| `WINWIN_CLI_NO_COLOR` | 禁用颜色 | `false` |

### 使用示例

```bash
# 设置配置目录
export WINWIN_CLI_HOME=/custom/path

# 启用调试日志
export WINWIN_CLI_LOG_LEVEL=DEBUG

# 禁用颜色输出
export WINWIN_CLI_NO_COLOR=true
```

## 常见问题

### Q: 如何查看命令帮助？

```bash
winwin-cli --help
winwin-cli convert --help
winwin-cli kb-search --help
winwin-cli skills --help
```

### Q: 如何升级 winwin-cli？

```bash
# 使用 uv
uv tool upgrade winwin-cli

# 使用 pip
pip install --upgrade winwin-cli
```

### Q: 配置文件在哪里？

配置文件位于 `$WINWIN_CLI_HOME/config.yaml`（默认 `~/.winwin-cli/config.yaml`）

### Q: 如何启用调试模式？

```bash
export WINWIN_CLI_LOG_LEVEL=DEBUG
winwin-cli convert document.docx
```

### Q: 批量转换时如何避免文件覆盖？

```bash
# 默认行为：跳过已存在的文件
winwin-cli convert ./docs

# 显式使用默认行为
winwin-cli convert ./docs --no-overwrite
```
