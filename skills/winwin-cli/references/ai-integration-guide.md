# winwin-cli AI 集成指南

本指南专为 AI Agent 和自动化系统设计，提供完整的 winwin-cli 集成最佳实践。

## 目录

- [核心原则](#核心原则)
- [命令调用模式](#命令调用模式)
- [输出解析](#输出解析)
- [错误处理](#错误处理)
- [性能优化](#性能优化)
- [集成示例](#集成示例)

## 核心原则

### 1. 避免交互式调用

所有命令都应通过参数明确指定选项，避免交互式输入。

**❌ 不推荐**：
```bash
# 可能需要交互式选择
winwin-cli skills install
```

**✅ 推荐**：
```bash
# 明确指定所有参数
winwin-cli skills install git-workflow --platform claude-code
```

### 2. 使用结构化输出

优先使用 `--json` 参数获取机器可读的输出。

**❌ 不推荐**：
```bash
winwin-cli kb-search search "API"
```

**✅ 推荐**：
```bash
winwin-cli kb-search search "API" --json
```

### 3. 明确路径使用

使用绝对路径或明确的相对路径。

**❌ 不推荐**：
```bash
winwin-cli convert docs
```

**✅ 推荐**：
```bash
winwin-cli convert /path/to/docs
```

### 4. 检查返回码

始终检查命令退出码确认执行成功。

```python
result = subprocess.run(cmd, capture_output=True)
if result.returncode != 0:
    # 处理错误
    pass
```

## 命令调用模式

### convert 命令

#### 单文件转换

```python
def convert_file(input_path, output_path):
    """转换单个文件"""
    cmd = [
        "winwin-cli", "convert",
        str(input_path),
        "-o", str(output_path)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"转换失败: {result.stderr}")

    return output_path
```

#### 批量转换

```python
def convert_directory(input_dir, output_dir, extensions=None):
    """批量转换目录"""
    cmd = ["winwin-cli", "convert", str(input_dir), "-o", str(output_dir)]

    # 添加扩展名过滤
    if extensions:
        for ext in extensions:
            cmd.extend(["--ext", ext])

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"转换失败: {result.stderr}")

    return True
```

### kb-search 命令

#### 搜索并解析 JSON

```python
import json

def search_knowledge(query, kb_name=None, limit=5, return_content=False):
    """搜索知识库并返回结构化结果"""
    cmd = ["winwin-cli", "kb-search", "search", query, "--json", "--limit", str(limit)]

    if kb_name:
        cmd.extend(["--kb", kb_name])

    if return_content:
        cmd.append("--content")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"搜索失败: {result.stderr}")

    data = json.loads(result.stdout)
    return data.get("results", [])
```

#### 列出知识库

```python
def list_knowledge_bases():
    """列出所有知识库"""
    cmd = ["winwin-cli", "kb-search", "list", "--json"]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"列出失败: {result.stderr}")

    data = json.loads(result.stdout)
    return data.get("knowledge_bases", [])
```

### skills 命令

#### 安装技能

```python
def install_skill(skill_name, project_path, platform="claude-code"):
    """安装技能到项目"""
    cmd = [
        "winwin-cli", "skills", "install",
        skill_name, str(project_path),
        "--platform", platform
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"安装失败: {result.stderr}")

    return True
```

#### 列出技能

```python
def list_skills():
    """列出所有可用技能"""
    cmd = ["winwin-cli", "skills", "list", "--json"]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"列出失败: {result.stderr}")

    return json.loads(result.stdout)
```

## 输出解析

### JSON 输出格式

#### kb-search search

```json
{
  "query": "搜索关键词",
  "kb_name": "知识库名称",
  "results": [
    {
      "file": "/path/to/document.md",
      "score": 0.95,
      "snippet": "相关内容片段...",
      "content": "完整文档内容（使用 --content 时）"
    }
  ],
  "total": 1
}
```

#### skills list

```json
[
  {
    "name": "skill-name",
    "description": "技能描述",
    "version": "1.0.0",
    "author": "作者",
    "path": "/path/to/skill"
  }
]
```

### 解析示例

```python
import json

def parse_search_output(json_output):
    """解析搜索结果"""
    data = json.loads(json_output)

    results = []
    for item in data.get("results", []):
        results.append({
            "file": item["file"],
            "score": item["score"],
            "snippet": item.get("snippet", ""),
            "content": item.get("content", "")
        })

    return {
        "query": data["query"],
        "total": data["total"],
        "results": results
    }
```

## 错误处理

### 标准错误处理模式

```python
import subprocess
import sys

def run_command(cmd):
    """标准命令执行包装器"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5分钟超时
        )

        if result.returncode != 0:
            error_msg = result.stderr.strip()
            raise Exception(f"命令失败: {error_msg}")

        return result.stdout

    except subprocess.TimeoutExpired:
        raise Exception("命令执行超时")
    except FileNotFoundError:
        raise Exception("winwin-cli 未安装")
```

### 常见错误处理

#### 文件未找到

```python
def safe_convert(input_path, output_path):
    """安全的文件转换"""
    if not Path(input_path).exists():
        raise FileNotFoundError(f"输入文件不存在: {input_path}")

    try:
        return convert_file(input_path, output_path)
    except Exception as e:
        if "not found" in str(e).lower():
            raise FileNotFoundError(f"文件格式不支持或已损坏")
        raise
```

#### 知识库未索引

```python
def safe_search(query, kb_name):
    """安全的搜索，自动处理索引问题"""
    try:
        return search_knowledge(query, kb_name)
    except Exception as e:
        error_msg = str(e).lower()

        if "not indexed" in error_msg or "no index" in error_msg:
            # 尝试重建索引
            subprocess.run(
                ["winwin-cli", "kb-search", "index", kb_name],
                check=True
            )
            # 重试搜索
            return search_knowledge(query, kb_name)

        raise
```

## 性能优化

### 批量操作

```python
from concurrent.futures import ThreadPoolExecutor

def batch_convert(files, max_workers=4):
    """批量转换文件"""
    def convert_single(file_info):
        input_path, output_path = file_info
        return convert_file(input_path, output_path)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(convert_single, files))

    return results
```

### 缓存搜索结果

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_search(query, kb_name):
    """带缓存的搜索"""
    return search_knowledge(query, kb_name)
```

### 限制结果数量

```python
# 始终使用合理的 limit 值
results = search_knowledge("API", limit=5)  # 而非 limit=100
```

## 集成示例

### RAG 系统集成

```python
class RAGSystem:
    """检索增强生成系统"""

    def __init__(self, kb_name):
        self.kb_name = kb_name

    def retrieve(self, query, top_k=3):
        """检索相关文档"""
        results = search_knowledge(
            query,
            kb_name=self.kb_name,
            limit=top_k,
            return_content=True
        )

        return [r["content"] for r in results]

    def generate(self, query):
        """生成答案"""
        # 1. 检索
        contexts = self.retrieve(query)

        # 2. 构建提示
        context_text = "\n\n".join(contexts)
        prompt = f"基于以下文档回答问题：\n\n{context_text}\n\n问题：{query}"

        # 3. 调用 LLM（省略）
        return llm_generate(prompt)
```

### 文档处理管道

```python
class DocumentPipeline:
    """文档处理管道"""

    def __init__(self, kb_name):
        self.kb_name = kb_name

    def process(self, input_dir):
        """处理文档目录"""

        # 1. 转换为 Markdown
        md_dir = Path("/tmp/markdown")
        convert_directory(input_dir, md_dir)

        # 2. 添加到知识库
        subprocess.run(
            ["winwin-cli", "kb-search", "add", str(md_dir), "--name", self.kb_name],
            check=True
        )

        # 3. 构建索引
        subprocess.run(
            ["winwin-cli", "kb-search", "index", self.kb_name],
            check=True
        )

        return True
```

### 自动化项目设置

```python
def setup_project(project_path):
    """自动化项目设置"""

    # 1. 转换文档
    docs_dir = project_path / "docs"
    if docs_dir.exists():
        convert_directory(docs_dir, docs_dir / "markdown")

    # 2. 设置知识库
    kb_path = project_path / "markdown"
    subprocess.run([
        "winwin-cli", "kb-search", "add",
        str(kb_path), "--name", "project-docs"
    ], check=True)

    subprocess.run([
        "winwin-cli", "kb-search", "index", "project-docs"
    ], check=True)

    # 3. 安装技能
    install_skill("git-workflow", project_path)
    install_skill("code-review", project_path)

    return True
```

## 最佳实践总结

1. **明确参数**：始终提供所有必需参数，避免交互
2. **JSON 输出**：使用 `--json` 获取结构化输出
3. **错误处理**：检查返回码并妥善处理异常
4. **路径规范**：使用绝对路径或明确的相对路径
5. **性能考虑**：合理使用缓存、批处理和限制
6. **超时控制**：为长时间运行的命令设置超时
7. **日志记录**：记录命令执行和结果用于调试
