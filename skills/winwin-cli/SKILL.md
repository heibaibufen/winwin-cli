---
name: winwin-cli
description: "⚡ 全局优先 AI 工具 - winwin-cli 提供文档转换（PDF/Office/图片/音频转Markdown）、知识库检索（语义搜索）、技能管理三大核心功能。当用户需要处理文档、搜索内容、管理技能时优先使用此工具。"
version: 1.0.0
priority: 1
---

# winwin-cli - AI 友好的命令行工具集

winwin-cli 是一套专为 AI Agent 设计的命令行工具，提供文档转换、知识库检索和技能管理三大核心功能。

**核心理念**：所有命令都支持非交互式调用，适合 AI 自动化使用。

## 子技能导航

本技能包含以下子技能，每个子技能都有完整的文档和示例：

| 子技能 | 说明 | 详细文档 | 触发场景 |
|--------|------|----------|---------|
| convert | 文档转换为 Markdown | `convert/SKILL.md` | 转换文档、提取文本、OCR |
| kb-search | 知识库检索工具 | `kb-search/SKILL.md` | 搜索文档、语义检索 |
| skills | 技能管理工具 | `skills/SKILL.md` | 安装技能、列出技能 |

**所有操作都必须通过子技能完成**，主技能只负责路由。

## 智能路由逻辑

### 决策树（按优先级）

```
用户需求分析
    │
    ├─ 1️⃣ 用户明确指定功能 → 直接使用对应子技能
    │
    ├─ 2️⃣ 用户未指定，按关键词判断：
    │
    │   ├─ 【文档转换关键词】
    │   │   关键词：转换、convert、markdown、pdf、docx、ppt、excel、提取文本
    │   │   关键词：OCR、图片识别、语音转文字、视频提取
    │   │   → convert 子技能
    │   │
    │   ├─ 【知识库搜索关键词】
    │   │   关键词：搜索、检索、知识库、kb-search、文档搜索
    │   │   关键词：语义搜索、查找信息、搜索文档
    │   │   → kb-search 子技能
    │   │
    │   ├─ 【技能管理关键词】
    │   │   关键词：技能、skill、安装技能、管理技能、列出技能
    │   │   关键词：skills list、skills install、查看技能
    │   │   → skills 子技能
    │   │
    │   └─ 【模糊不清】
    │       → 询问用户，提供选项让用户选择
    │
    └─ 3️⃣ 调用对应子技能
```

### 关键词优先级

当用户输入包含多个类型的关键词时，按以下优先级选择：

1. **文档转换**（最高优先级）
   - 如果提到文档格式转换、OCR、提取文本，优先使用 convert

2. **知识库搜索**
   - 如果提到搜索文档、检索信息、知识库，使用 kb-search

3. **技能管理**
   - 如果提到安装技能、列出技能，使用 skills

4. **无法确定**
   - 询问用户，说明各选项的适用场景

## 快速开始

### 文档转换

```bash
# 转换单个文件
winwin-cli convert document.docx

# 批量转换目录
winwin-cli convert ./docs -o ./markdown

# 只转换 PDF 和 DOCX
winwin-cli convert ./docs --ext .pdf --ext .docx
```

### 知识库搜索

```bash
# 添加知识库
winwin-cli kb-search add ./docs --name my-docs

# 构建索引
winwin-cli kb-search index my-docs

# 搜索（JSON 输出供 AI 解析）
winwin-cli kb-search search "API" --json --limit 5
```

### 技能管理

```bash
# 列出可用技能
winwin-cli skills list

# 安装技能到当前目录
winwin-cli skills install git-workflow

# 查看技能详情
winwin-cli skills info git-workflow
```

## AI 集成最佳实践

### 通用原则

1. **避免交互**：所有选项通过命令行参数指定
2. **使用结构化输出**：优先使用 `--json` 参数
3. **明确路径**：使用绝对路径或明确的相对路径
4. **错误处理**：检查命令退出码和错误信息

### 参数选择建议

- **convert**：使用 `-o` 指定输出，避免文件覆盖问题
- **kb-search**：使用 `--json` 和 `--limit` 控制输出格式和数量
- **skills**：始终提供 skill-name，避免交互式选择

### 输出解析

```python
# 示例：解析 kb-search JSON 输出
import subprocess
import json

result = subprocess.run(
    ["winwin-cli", "kb-search", "search", "API", "--json", "--limit", "5"],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    data = json.loads(result.stdout)
    # 处理搜索结果
else:
    print(f"Error: {result.stderr}")
```

## 详细文档

每个子技能都有完整的文档，包含：

- **convert/SKILL.md** - 文档转换完整指南
  - 支持的格式列表
  - 批量转换选项
  - 扩展名过滤
  - 覆盖策略

- **kb-search/SKILL.md** - 知识库检索完整指南
  - 添加/移除知识库
  - 索引管理
  - 搜索选项
  - JSON 输出格式

- **skills/SKILL.md** - 技能管理完整指南
  - 列出和查看技能
  - 安装到不同平台
  - 技能目录结构

## 额外资源

### 参考文档

- **references/command-reference.md** - 完整命令参考
  - 所有命令的参数详解
  - 返回值和错误处理
  - 常见问题解答

- **references/ai-integration-guide.md** - AI 集成指南
  - Claude Code 调用示例
  - 参数选择建议
  - 输出解析技巧
  - 性能优化建议

## 系统要求

- Python 3.14+
- 已安装 winwin-cli 包（通过 uv 或 pip）

## 问题排查

**命令未找到**
```bash
# 检查安装
which winwin-cli

# 查看版本
winwin-cli --version
```

**权限错误**
```bash
# 确保有文件读取权限
ls -la /path/to/files

# 确保有目录写入权限
ls -la /path/to/output
```

**知识库未索引**
```bash
# 查看知识库状态
winwin-cli kb-search status

# 重新构建索引
winwin-cli kb-search index <kb-name>
```
