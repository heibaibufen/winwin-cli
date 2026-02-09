---
name: winwin-cli-kb-search
description: "⚡ 知识库检索优先工具 - 本地文档语义搜索、知识库管理。当用户需要搜索文档、检索信息、管理知识库时优先使用 winwin-cli kb-search。提供 JSON 输出便于 AI 解析。"
version: 1.0.0
priority: 1
---

# winwin-cli kb-search - 知识库检索工具

本地文档知识库管理和语义搜索工具，专为 AI 集成设计。

## 核心特性

- **语义搜索**：基于向量相似度的智能搜索
- **多知识库管理**：支持添加、启用、禁用多个知识库
- **AI 友好**：JSON 输出格式，便于程序解析
- **灵活索引**：手动或自动构建搜索索引

## 子命令列表

| 命令 | 说明 | AI 友好 |
|------|------|---------|
| `add` | 添加知识库 | ✅ |
| `remove` | 移除知识库 | ✅ |
| `enable` | 启用知识库 | ✅ |
| `disable` | 禁用知识库 | ✅ |
| `index` | 构建索引 | ✅ |
| `search` | 搜索知识库 | ✅（支持 JSON） |
| `list` | 列出知识库 | ✅（支持 JSON） |
| `status` | 查看状态 | ✅ |
| `info` | 显示系统信息 | ✅ |

## 常用命令

### 管理知识库

```bash
# 添加知识库
winwin-cli kb-search add /path/to/docs --name my-docs

# 列出所有知识库
winwin-cli kb-search list

# 查看知识库状态
winwin-cli kb-search status

# 移除知识库
winwin-cli kb-search remove my-docs

# 启用/禁用知识库
winwin-cli kb-search enable my-docs
winwin-cli kb-search disable my-docs
```

### 构建索引

```bash
# 为指定知识库构建索引
winwin-cli kb-search index my-docs

# 重建所有知识库索引
winwin-cli kb-search index --all
```

### 搜索知识库

```bash
# 简单搜索
winwin-cli kb-search search "API 设计"

# 指定知识库搜索
winwin-cli kb-search search "API" --kb my-docs

# 限制结果数量
winwin-cli kb-search search "API" --limit 5

# JSON 输出（供 AI 解析）
winwin-cli kb-search search "API" --json

# 返回完整内容
winwin-cli kb-search search "API" --content

# 组合使用
winwin-cli kb-search search "API" --kb my-docs --json --limit 3
```

## 命令详解

### add - 添加知识库

```bash
winwin-cli kb-search add [PATH] --name [NAME]
```

**参数**：
- `PATH`：文档目录路径（必需）
- `--name`：知识库名称（必需）

**示例**：
```bash
winwin-cli kb-search add ./docs --name project-docs
```

### index - 构建索引

```bash
winwin-cli kb-search index [KB_NAME]
```

**参数**：
- `KB_NAME`：知识库名称（可选，默认所有）

**示例**：
```bash
winwin-cli kb-search index project-docs
```

### search - 搜索知识库

```bash
winwin-cli kb-search search [QUERY] [OPTIONS]
```

**参数**：
- `QUERY`：搜索关键词（可选，默认交互式输入）

**选项**：
- `--kb`, `-k`：指定知识库（默认：所有启用的知识库）
- `--limit`, `-l`：最大结果数（默认：10）
- `--json`, `-j`：JSON 输出
- `--content`, `-c`：返回完整内容

**示例**：
```bash
# 基础搜索
winwin-cli kb-search search "API"

# JSON 输出（AI 推荐）
winwin-cli kb-search search "API" --json --limit 5

# 返回完整内容
winwin-cli kb-search search "API" --json --content
```

### list - 列出知识库

```bash
winwin-cli kb-search list
```

**输出示例**：
```
可用的知识库：
  1. project-docs (已启用)
     路径: /path/to/docs
     文档数: 150
     索引状态: 已构建

  2. research-papers (已禁用)
     路径: /path/to/papers
     文档数: 85
     索引状态: 未构建
```

### remove - 移除知识库

```bash
winwin-cli kb-search remove [KB_NAME]
```

**参数**：
- `KB_NAME`：知识库名称（必需）

**示例**：
```bash
winwin-cli kb-search remove old-docs
```

### enable/disable - 启用/禁用知识库

```bash
winwin-cli kb-search enable [KB_NAME]
winwin-cli kb-search disable [KB_NAME]
```

**参数**：
- `KB_NAME`：知识库名称（必需）

**示例**：
```bash
winwin-cli kb-search enable archive-docs
winwin-cli kb-search disable temp-docs
```

## AI 调用最佳实践

### 搜索并解析 JSON

```python
import subprocess
import json

def search_knowledge(query, kb_name=None, limit=5):
    """搜索知识库并返回结构化结果"""
    cmd = ["winwin-cli", "kb-search", "search", query, "--json", "--limit", str(limit)]

    if kb_name:
        cmd.extend(["--kb", kb_name])

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"搜索失败: {result.stderr}")
        return []

    data = json.loads(result.stdout)
    return data.get("results", [])
```

### 使用完整内容

```python
def search_with_content(query, kb_name):
    """搜索并返回完整文档内容"""
    cmd = ["winwin-cli", "kb-search", "search", query,
           "--kb", kb_name, "--json", "--content", "--limit", "3"]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        data = json.loads(result.stdout)
        for item in data.get("results", []):
            print(f"文件: {item['file']}")
            print(f"内容: {item['content']}")
            print("-" * 50)
```

### 批量添加和索引

```python
def setup_knowledge_bases(kb_config):
    """批量设置知识库"""
    for name, path in kb_config.items():
        # 添加知识库
        subprocess.run(
            ["winwin-cli", "kb-search", "add", path, "--name", name],
            check=True
        )

        # 构建索引
        subprocess.run(
            ["winwin-cli", "kb-search", "index", name],
            check=True
        )

        print(f"✓ 知识库 {name} 设置完成")
```

## JSON 输出格式

### search 命令输出

```json
{
  "query": "API 设计",
  "kb_name": "project-docs",
  "results": [
    {
      "file": "/path/to/docs/api-design.md",
      "score": 0.95,
      "snippet": "API 设计原则...",
      "content": "完整文档内容（使用 --content 时）"
    },
    {
      "file": "/path/to/docs/rest-api.md",
      "score": 0.87,
      "snippet": "RESTful API 规范...",
      "content": "完整文档内容"
    }
  ],
  "total": 2
}
```

### list 命令输出

```json
{
  "knowledge_bases": [
    {
      "name": "project-docs",
      "path": "/path/to/docs",
      "enabled": true,
      "document_count": 150,
      "indexed": true,
      "last_indexed": "2025-02-09T10:30:00"
    }
  ]
}
```

## 工作流程

### 初始化知识库

```bash
# 1. 添加知识库
winwin-cli kb-search add ./docs --name my-docs

# 2. 构建索引
winwin-cli kb-search index my-docs

# 3. 验证状态
winwin-cli kb-search status

# 4. 测试搜索
winwin-cli kb-search search "测试" --limit 1
```

### 更新知识库

```bash
# 1. 添加新文档到目录
# (手动操作)

# 2. 重新构建索引
winwin-cli kb-search index my-docs

# 3. 验证
winwin-cli kb-search status
```

### 多知识库管理

```bash
# 添加多个知识库
winwin-cli kb-search add ./project-docs --name project
winwin-cli kb-search add ./research --name research
winwin-cli kb-search add ./archive --name archive

# 启用/禁用特定知识库
winwin-cli kb-search disable archive

# 搜索所有启用的知识库
winwin-cli kb-search search "API" --json

# 搜索特定知识库
winwin-cli kb-search search "API" --kb project --json
```

## 使用场景

### 场景 1：RAG 系统

构建检索增强生成（RAG）系统：

```python
def rag_answer(question):
    # 1. 搜索相关文档
    results = search_knowledge(question, kb_name="docs", limit=3)

    # 2. 构建上下文
    context = "\n\n".join([r["content"] for r in results])

    # 3. 生成答案
    prompt = f"基于以下文档回答问题：\n\n{context}\n\n问题：{question}"
    # ... 调用 LLM
```

### 场景 2：代码助手

为代码库添加智能搜索：

```bash
# 添加代码文档
winwin-cli kb-search add ./code-docs --name code

# 构建索引
winwin-cli kb-search index code

# 搜索代码示例
winwin-cli kb-search search "如何使用 API" --kb code --json
```

### 场景 3：研究助手

管理研究论文：

```bash
# 添加论文目录
winwin-cli kb-search add ./papers --name papers

# 转换 PDF 为 Markdown（配合 convert）
winwin-cli convert ./papers -o ./papers-md

# 重新索引 Markdown 版本
winwin-cli kb-search remove papers
winwin-cli kb-search add ./papers-md --name papers
winwin-cli kb-search index papers
```

## 性能优化

### 索引优化

```bash
# 定期重建索引
winwin-cli kb-search index --all

# 只启用的知识库参与搜索
winwin-cli kb-search disable large-archive
```

### 搜索优化

```bash
# 限制结果数量
winwin-cli kb-search search "query" --limit 5

# 指定知识库缩小范围
winwin-cli kb-search search "query" --kb specific-kb
```

## 故障排查

### 知识库未索引

```bash
# 查看状态
winwin-cli kb-search status

# 重新构建索引
winwin-cli kb-search index <kb-name>
```

### 搜索无结果

```bash
# 检查知识库是否启用
winwin-cli kb-search list

# 尝试更宽泛的关键词
winwin-cli kb-search search "更宽泛的关键词"

# 检查索引状态
winwin-cli kb-search status
```

### JSON 解析错误

```bash
# 确保 --json 参数正确
winwin-cli kb-search search "query" --json

# 检查返回码
echo $?
```

## 与其他技能集成

### 配合 convert 技能

```bash
# 1. 转换文档为 Markdown
winwin-cli convert ./docs -o ./markdown

# 2. 添加到知识库
winwin-cli kb-search add ./markdown --name my-kb

# 3. 构建索引
winwin-cli kb-search index my-kb
```

### 配合 skills 技能

```bash
# 搜索并安装相关技能
winwin-cli kb-search search "git workflow" --kb skills-docs
winwin-cli skills install git-workflow
```

## 最佳实践

1. **定期重建索引**：文档更新后及时重建索引
2. **使用 JSON 输出**：便于程序化处理
3. **合理设置 limit**：避免返回过多结果
4. **明确指定知识库**：提高搜索准确性和性能
5. **管理知识库状态**：禁用不常用的知识库
