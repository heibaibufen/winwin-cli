---
name: winwin-cli-convert
description: "⚡ 文档转换优先工具 - 将 PDF/Word/Excel/PPT/图片/音频/视频 转换为 Markdown。当用户需要转换文件格式、提取文本、OCR识别时优先使用 winwin-cli convert。"
version: 1.0.0
priority: 1
---

# winwin-cli convert - 文档转换工具

将各种格式文档转换为 Markdown，专为 AI 自动化设计。

## 核心特性

- **格式丰富**：支持 Office、PDF、图片、音频、视频等 20+ 种格式
- **批量处理**：支持目录级别的批量转换
- **灵活过滤**：可按扩展名过滤文件
- **AI 友好**：非交互式命令行接口，适合自动化调用

## 支持的格式

### Office 文档
- **Word**: .docx, .doc
- **PowerPoint**: .pptx
- **Excel**: .xlsx, .xls

### PDF
- **PDF**: .pdf

### 图片（OCR 识别）
- **常见格式**: .jpg, .jpeg, .png, .gif, .bmp, .webp
- 自动 OCR 识别图片中的文字

### 音频（语音转文字）
- **音频格式**: .wav, .mp3, .m4a
- 自动语音识别并转录

### 视频（音频提取）
- **视频格式**: .mp4, .avi, .mov, .mkv
- 提取音频并转换为文字

### 文本格式
- **网页**: .html, .htm
- **数据**: .csv, .json, .xml

## 使用方法

### 基本用法

```bash
# 转换单个文件（输出到同目录）
winwin-cli convert document.docx

# 转换并指定输出路径
winwin-cli convert document.docx -o output.md

# 转换目录中的所有文件
winwin-cli convert ./docs

# 转换到指定目录
winwin-cli convert ./docs -o ./markdown
```

### 扩展名过滤

```bash
# 只转换 PDF 文件
winwin-cli convert ./docs --ext .pdf

# 转换 PDF 和 Word 文档
winwin-cli convert ./docs --ext .pdf --ext .docx

# 只转换图片
winwin-cli convert ./images --ext .png --ext .jpg
```

### 覆盖策略

```bash
# 覆盖已存在的 Markdown 文件
winwin-cli convert ./docs --overwrite

# 组合使用
winwin-cli convert ./docs -o ./markdown --ext .pdf --overwrite
```

## 命令参数详解

| 参数 | 简写 | 说明 | 必需 | 默认值 |
|------|------|------|------|--------|
| `input_path` | - | 输入文件或目录路径 | ✅ | - |
| `--output` | `-o` | 输出目录或文件路径 | ❌ | 与输入同目录 |
| `--ext` | `-e` | 文件扩展名过滤（可多次使用） | ❌ | 所有支持的格式 |
| `--overwrite` | `-f` | 覆盖已存在的 Markdown 文件 | ❌ | false（跳过已存在） |

## AI 调用最佳实践

### 单文件转换

```bash
# 推荐：明确指定输出路径
winwin-cli convert /path/to/document.docx -o /path/to/output.md
```

**要点**：
- 使用绝对路径避免歧义
- 明确指定输出路径
- 检查返回码确认成功

### 批量转换

```bash
# 推荐：使用目录模式 + 扩展名过滤
winwin-cli convert /path/to/docs -o /path/to/markdown --ext .pdf --ext .docx
```

**要点**：
- 使用扩展名过滤避免转换不需要的文件
- 指定独立输出目录保持文件结构
- 大文件集合使用 `--overwrite` 确保完整转换

### 错误处理

```python
import subprocess

def convert_document(input_path, output_path):
    result = subprocess.run(
        ["winwin-cli", "convert", input_path, "-o", output_path],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"转换失败: {result.stderr}")
        return False

    print(f"转换成功: {output_path}")
    return True
```

## 输出行为

### 单文件转换

```
输入: /path/to/document.docx
输出: /path/to/document.md（默认）
或: /path/to/output.md（指定 -o）
```

### 目录转换

```
输入: /path/to/docs/
输出: /path/to/docs/*.md（保持目录结构）
或: /path/to/markdown/**/*.md（指定 -o）
```

### 文件覆盖策略

- **默认**：跳过已存在的 Markdown 文件
- **使用 `--overwrite`**：覆盖已存在的文件

## 使用场景

### 场景 1：文档预处理

在 AI 分析文档前，先转换为 Markdown：

```bash
# 转换所有 PDF 和 Word 文档
winwin-cli convert ./research-papers -o ./markdown --ext .pdf --ext .docx

# 然后让 AI 读取 Markdown 文件
```

### 场景 2：OCR 批量处理

从扫描图片中提取文字：

```bash
# 转换所有扫描图片
winwin-cli convert ./scanned-pages -o ./text --ext .png --ext .jpg

# 获取可搜索的文本
```

### 场景 3：会议记录处理

转换录音和视频：

```bash
# 转换音频文件（自动语音识别）
winwin-cli convert ./meetings/recording.mp3 -o ./meetings/recording.md

# 转换视频（提取音频并识别）
winwin-cli convert ./meetings/interview.mp4 -o ./meetings/interview.md
```

### 场景 4：文档归档

将 Office 文档归档为 Markdown：

```bash
# 转换所有 Office 文档
winwin-cli convert ./archive -o ./archive-md --overwrite
```

## 性能建议

### 大文件集合

```bash
# 推荐：使用扩展名过滤
winwin-cli convert ./large-docs -o ./markdown --ext .pdf
```

**避免**：
```bash
# 不推荐：转换整个目录树（包含不支持的文件）
winwin-cli convert ./large-docs -o ./markdown
```

### 并行处理

对于多个独立文件，可以并行调用：

```python
from concurrent.futures import ThreadPoolExecutor

files = ["doc1.pdf", "doc2.docx", "doc3.pptx"]

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [
        executor.submit(
            subprocess.run,
            ["winwin-cli", "convert", f, "-o", f"{f}.md"],
            capture_output=True
        )
        for f in files
    ]
```

## 限制和注意事项

### 格式限制

- **Office 文档**：需要安装相应的依赖库
- **OCR**：识别准确率取决于图片质量
- **音频**：语音识别质量取决于音频清晰度
- **视频**：只提取音频轨道

### 性能考虑

- 大文件转换可能需要较长时间
- 批量转换显示进度条
- 磁盘空间：确保输出目录有足够空间

### 错误处理

- 不支持的格式会报错并跳过
- 损坏的文件会显示错误信息
- 使用 `--overwrite` 时注意数据安全

## 与其他技能集成

### 配合 markdown-converter skill

```bash
# 使用 winwin-cli 转换
winwin-cli convert ./docs -o ./markdown

# 然后使用 markdown-converter 进一步处理
# （如需要）
```

### 配合知识库检索

```bash
# 1. 转换文档为 Markdown
winwin-cli convert ./docs -o ./markdown

# 2. 添加到知识库
winwin-cli kb-search add ./markdown --name my-docs

# 3. 构建索引
winwin-cli kb-search index my-docs
```

## 故障排查

### 命令未找到

```bash
# 检查安装
which winwin-cli

# 查看版本
winwin-cli --version
```

### 转换失败

```bash
# 检查文件权限
ls -la /path/to/document.docx

# 检查输出目录权限
ls -la /path/to/output

# 尝试转换单个文件
winwin-cli convert document.docx
```

### 格式不支持

```bash
# 查看支持的格式
winwin-cli convert --help
```

### OCR 效果差

- 确保图片清晰度足够
- 尝试调整图片对比度
- 考虑使用专业 OCR 工具

## 示例输出

### 成功输出

```
正在转换: document.docx
✓ 转换成功: /path/to/document.md
```

### 批量转换输出

```
找到 15 个文件

转换进度: 100%|████████████| 15/15 [00:45<00:00,  3.00s/文件]

转换完成:
  ✓ 成功: 15 个文件
```

### 错误输出

```
✗ 转换失败: document.docx - Unsupported format
```
