# winwin-cli

<div align="center">

**专为 AI 设计的 CLI 封装工具集**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

[功能特性](#功能特性) • [快速开始](#快速开始) • [使用文档](#使用文档) • [开发指南](#开发)

</div>

## 📖 简介

winwin-cli 是一套专为 AI 使用设计的命令行工具集，提供知识库检索、文档转换、技能管理等实用功能。

**设计理念：**
- 🤖 **AI 优先** - 所有命令支持 JSON 输出，便于 AI 调用和解析
- 🎯 **简单易用** - 清晰的命令结构，简洁的参数设计
- 🔧 **可扩展** - 模块化架构，易于添加新功能
- 📦 **零依赖安装** - 使用 `uvx` 无需安装即可运行

## ✨ 功能特性

### 🔍 kb-search - 知识库检索工具

基于 BM25 算法的全文检索系统，快速搜索你的文档。

- 支持 30+ 种文档格式（PDF、Office、Markdown、HTML 等）
- 中文分词支持（jieba）
- 多知识库管理
- 自动文档索引和更新
- JSON 输出，便于 AI 解析

### 🔄 convert - 文档转换工具

将各种格式的文档转换为 Markdown 或纯文本。

- 支持的格式：PDF、Word、PowerPoint、Excel、图片（OCR）、音频、视频等
- 批量转换目录
- 保留目录结构
- 转换进度显示

### 🛠️ skills - 技能管理命令

从 GitHub 仓库为 Claude Code 等 AI 工具安装和管理技能。

- **从 GitHub 仓库安装** - 支持从远程仓库下载技能
- **多种安装方式** - 支持完整 URL、简写形式、交互式选择
- **多平台支持** - Claude Code、OpenCode
- **自动解析元数据** - 从 SKILL.md 提取技能信息
- **自定义仓库** - 支持指定自定义技能仓库

## 🚀 快速开始

### 安装

**方式一：使用 uvx（推荐，无需安装）**

```bash
# 直接运行，无需安装
uvx winwin-cli --help

# 查看特定命令
uvx winwin-cli kb-search --help
```

**方式二：使用 uv 安装**

```bash
# 安装 uv（如果未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装 winwin-cli
uv pip install winwin-cli

# 验证安装
winwin-cli --help
```

**方式三：从源码安装**

```bash
# 克隆仓库
git clone https://github.com/your-username/winwin-cli.git
cd winwin-cli

# 安装依赖
uv sync

# 激活虚拟环境
source .venv/bin/activate

# 运行命令
winwin-cli --help
```

### 基础使用

**知识库检索：**

```bash
# 添加文档到知识库
winwin-cli kb-search add my-kb ./docs

# 搜索文档
winwin-cli kb-search search my-kb "如何使用 Python"

# 列出所有知识库
winwin-cli kb-search list

# 索引知识库
winwin-cli kb-search index my-kb
```

**文档转换：**

```bash
# 转换单个文件
winwin-cli convert document.docx

# 转换目录
winwin-cli convert ./docs

# 指定输出目录
winwin-cli convert ./docs -o ./markdown

# 只转换特定格式
winwin-cli convert ./docs --ext .pdf --ext .docx
```

**技能管理：**

```bash
# 列出所有可用技能（从默认 GitHub 仓库）
winwin-cli skills list

# 查看技能详情
winwin-cli skills info skill-name

# 交互式选择并安装技能
winwin-cli skills install

# 使用简写形式安装
winwin-cli skills install skill-name

# 指定仓库安装
winwin-cli skills install owner/repo/skill-name

# 使用完整 GitHub URL
winwin-cli skills install https://github.com/owner/repo/tree/main/skill-name

# JSON 格式输出（AI 调用）
winwin-cli skills list --json
```

## 📚 使用文档

### kb-search 详细用法

```bash
# 添加知识库
winwin-cli kb-search add my-kb ./docs --desc "我的文档"

# 添加并立即索引
winwin-cli kb-search add my-kb ./docs --init

# 搜索（JSON 输出）
winwin-cli kb-search search my-kb "查询词" --json

# 更新索引
winwin-cli kb-search index my-kb

# 查看知识库状态
winwin-cli kb-search status my-kb

# 启用/禁用知识库
winwin-cli kb-search enable my-kb
winwin-cli kb-search disable my-kb

# 删除知识库
winwin-cli kb-search remove my-kb

# 搜索所有启用的知识库
winwin-cli kb-search search "查询词"

# 限制结果数量
winwin-cli kb-search search my-kb "查询词" --limit 5
```

### skills 详细用法

**配置默认技能仓库：**

```bash
# 通过环境变量设置默认仓库
export WINWIN_SKILLS_REPO="heibaibufen/winwin-skills"

# 或在命令中临时指定
winwin-cli skills list --repo owner/custom-skills
```

**列出技能：**

```bash
# 从默认仓库列出所有技能
winwin-cli skills list

# 指定分支
winwin-cli skills list --branch develop

# 指定仓库
winwin-cli skills list --repo owner/custom-skills

# JSON 格式输出
winwin-cli skills list --json
```

**查看技能信息：**

```bash
# 使用技能名称（默认仓库）
winwin-cli skills info skill-name

# 指定仓库
winwin-cli skills info skill-name --repo owner/custom-skills

# 指定分支
winwin-cli skills info skill-name --branch feature-branch
```

**安装技能：**

```bash
# 方式 1: 交互式选择
winwin-cli skills install

# 方式 2: 使用技能名称（默认仓库）
winwin-cli skills install skill-name

# 方式 3: 指定仓库和技能
winwin-cli skills install owner/repo/skill-name

# 方式 4: 使用完整 GitHub URL
winwin-cli skills install https://github.com/owner/repo/tree/main/skill-name

# 指定安装路径
winwin-cli skills install skill-name /path/to/project

# 指定平台
winwin-cli skills install skill-name --platform claude-code

# 指定分支
winwin-cli skills install skill-name --branch develop

# 覆盖默认仓库
winwin-cli skills install skill-name --repo owner/custom-repo

# 完整示例
winwin-cli skills install my-skill ./my-project --platform claude-code --branch dev
```

**技能格式要求：**

技能仓库支持按分类组织，结构如下：

```
owner/skills-repo/
├── category1/          # 分类目录（如：heibai、xurui）
│   ├── skill-a/       # 具体技能目录
│   │   └── SKILL.md   # 必需：技能定义文件
│   └── skill-b/
│       └── SKILL.md
├── category2/
│   └── skill-c/
│       └── SKILL.md
└── README.md
```

每个技能目录需要包含：
- `SKILL.md` - 技能定义文件，包含 YAML 前置元数据
- 可选的子目录（scripts、references、assets 等）

示例 SKILL.md：

```markdown
---
name: my-skill
description: 我的技能描述
version: 1.0.0
author: Your Name
---

# 技能使用说明

...
```

## 🏗️ 项目结构

```
winwin-cli/
├── src/winwin_cli/       # 源代码
│   ├── cli.py           # 主入口
│   ├── convert/         # 文档转换模块
│   │   ├── __init__.py
│   │   └── cli.py       # convert 命令
│   ├── skills/          # 技能管理模块
│   │   ├── __init__.py
│   │   └── cli.py       # skills 命令（从 GitHub 仓库安装）
│   └── kb_search/       # 知识库检索模块
│       ├── cli.py       # kb-search 命令组
│       ├── config.py    # 配置管理
│       ├── indexer.py   # 文档索引
│       ├── search.py    # 搜索引擎
│       ├── models.py    # 数据模型
│       ├── markitdown.py # 文档转换
│       └── commands/    # 子命令实现
│           ├── add.py
│           ├── remove.py
│           ├── index.py
│           ├── search.py
│           ├── list.py
│           ├── enable.py
│           ├── disable.py
│           ├── status.py
│           └── info.py
├── tests/               # 测试文件
│   ├── test_convert.py
│   ├── test_kb_search_*.py
│   └── test_skills.py
├── docs/                # 文档
├── pyproject.toml       # 项目配置
├── CLAUDE.md           # Claude Code 开发指南
└── README.md           # 本文件
```

## 🔧 开发指南

### 环境设置

```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 克隆仓库
git clone https://github.com/your-username/winwin-cli.git
cd winwin-cli

# 安装依赖
uv sync

# 激活虚拟环境
source .venv/bin/activate
```

### 运行测试

```bash
# 运行所有测试
uv pytest

# 运行特定测试文件
uv pytest tests/test_skills.py

# 显示详细输出
uv pytest -v

# 显示测试覆盖率
uv pytest --cov=winwin_cli
```

### 构建和发布

```bash
# 构建分发包
uv build

# 发布到 PyPI（需要凭据）
uv publish

# 或使用 twine
pip install twine
twine upload dist/*
```

### 代码风格

项目遵循以下代码规范：
- 使用 Click 进行 CLI 开发
- 遵循 PEP 8 代码风格
- 使用类型注解（Type Hints）
- 编写完整的文档字符串
- 保持测试覆盖率 > 80%

### 添加新命令

1. 创建新模块目录：`src/winwin_cli/my_command/`
2. 创建 `cli.py` 实现命令
3. 创建 `__init__.py` 导出命令
4. 在 `src/winwin_cli/cli.py` 中注册命令
5. 编写测试 `tests/test_my_command.py`

## 🤝 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m '✨ feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

**提交规范：**

使用约定式提交格式（Conventional Commits）：
- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `style:` 代码格式
- `refactor:` 重构
- `test:` 测试相关
- `chore:` 构建过程或辅助工具

## 📝 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 🔗 相关资源

- [知识库配置示例](knowledge-bases.yaml)
- [Claude Code 开发指南](CLAUDE.md)
- [默认技能仓库](https://github.com/heibaibufen/winwin-skills)
- [项目 Issue](https://github.com/your-username/winwin-cli/issues)

## 💡 使用场景

### 为 AI Agent 提供知识库

```bash
# 添加项目文档
winwin-cli kb-search add project-docs ./docs --init

# AI 可以快速查询
winwin-cli kb-search search project-docs "如何配置 API" --json
```

### 批量文档转换

```bash
# 转换所有 Office 文档为 Markdown
winwin-cli convert ./documents --ext .docx --ext .pptx --ext .xlsx
```

### 统一开发工作流

```bash
# 为团队项目安装标准技能
winwin-cli skills install vega-lite-charts ./team-project --platform claude-code
winwin-cli skills install winwin-cli ./team-project --platform claude-code
```

---

<div align="center">

**用 ❤️ 构建，专为 AI 设计**

[🔝 回到顶部](#winwin-cli)

</div>
