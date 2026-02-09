---
name: winwin-cli-skills
description: "⚡ 技能管理优先工具 - 安装和管理 Claude Code 技能。当用户需要列出技能、安装技能、查看技能信息时优先使用 winwin-cli skills。"
version: 1.0.0
priority: 1
---

# winwin-cli skills - 技能管理工具

Claude Code 技能包管理工具，支持技能的安装、列表和查看。

## 核心特性

- **技能安装**：一键安装技能到项目
- **多平台支持**：支持 Claude Code 和 OpenCode 平台
- **技能发现**：列出所有可用技能
- **AI 友好**：非交互式安装，适合自动化

## 子命令列表

| 命令 | 说明 | AI 友好 |
|------|------|---------|
| `list` | 列出所有可用技能 | ✅（支持 JSON） |
| `info` | 显示技能详细信息 | ✅ |
| `install` | 安装技能到项目 | ✅ |

## 常用命令

### 列出技能

```bash
# 列出所有技能（人类友好格式）
winwin-cli skills list

# JSON 格式输出（AI 推荐）
winwin-cli skills list --json
```

### 查看技能详情

```bash
winwin-cli skills info <skill-name>
```

### 安装技能

```bash
# 安装到当前目录
winwin-cli skills install <skill-name>

# 安装到指定目录
winwin-cli skills install <skill-name> /path/to/project

# 指定平台
winwin-cli skills install <skill-name> --platform claude-code
```

## 命令详解

### list - 列出技能

```bash
winwin-cli skills list [--json]
```

**选项**：
- `--json`：以 JSON 格式输出（AI 推荐）

**示例**：
```bash
# 人类可读格式
winwin-cli skills list

# JSON 格式
winwin-cli skills list --json
```

**输出示例（人类可读）**：
```
找到 3 个技能：

📦 git-workflow
   描述: Git 工作流管理技能
   版本: 1.0.0
   作者: Your Name
   路径: /path/to/skills/git-workflow

📦 code-review
   描述: 代码审查助手
   版本: 2.1.0
   作者: Another Author
   路径: /path/to/skills/code-review
```

**输出示例（JSON）**：
```json
[
  {
    "name": "git-workflow",
    "description": "Git 工作流管理技能",
    "version": "1.0.0",
    "author": "Your Name",
    "path": "/path/to/skills/git-workflow"
  },
  {
    "name": "code-review",
    "description": "代码审查助手",
    "version": "2.1.0",
    "author": "Another Author",
    "path": "/path/to/skills/code-review"
  }
]
```

### info - 查看技能详情

```bash
winwin-cli skills info <skill-name>
```

**参数**：
- `skill-name`：技能名称（必需）

**示例**：
```bash
winwin-cli skills info git-workflow
```

**输出示例**：
```
📦 技能: git-workflow
==================================================
描述: Git 工作流管理技能
版本: 1.0.0
作者: Your Name
路径: /path/to/skills/git-workflow

包含的文件:
  - SKILL.md
  - examples.json
  - scripts/install.sh
```

### install - 安装技能

```bash
winwin-cli skills install [skill-name] [path] [OPTIONS]
```

**参数**：
- `skill-name`：技能名称（可选，不提供则交互式选择）
- `path`：安装路径（可选，默认当前目录）

**选项**：
- `--platform`：目标平台（claude-code 或 opencode）

**AI 调用建议**：
- **始终提供 skill-name**：避免交互式选择
- **使用 `--platform`**：明确目标平台

**示例**：
```bash
# AI 推荐：明确指定所有参数
winwin-cli skills install git-workflow /path/to/project --platform claude-code

# 安装到当前目录
winwin-cli skills install git-workflow --platform claude-code

# 交互式选择（不推荐 AI 使用）
winwin-cli skills install
```

## AI 调用最佳实践

### 批量安装技能

```python
import subprocess

def install_skills(skill_names, project_path, platform="claude-code"):
    """批量安装技能"""
    for skill_name in skill_names:
        cmd = [
            "winwin-cli", "skills", "install",
            skill_name, project_path,
            "--platform", platform
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"✓ {skill_name} 安装成功")
        else:
            print(f"✗ {skill_name} 安装失败: {result.stderr}")

# 使用示例
skills_to_install = ["git-workflow", "code-review", "test-helper"]
install_skills(skills_to_install, "/path/to/project")
```

### 列出并选择技能

```python
import subprocess
import json

def get_available_skills():
    """获取可用技能列表"""
    result = subprocess.run(
        ["winwin-cli", "skills", "list", "--json"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return json.loads(result.stdout)
    return []

def find_skill(keyword):
    """根据关键词查找技能"""
    skills = get_available_skills()
    matches = [
        s for s in skills
        if keyword.lower() in s["name"].lower() or
           keyword.lower() in s.get("description", "").lower()
    ]
    return matches

# 使用示例
matches = find_skill("git")
for skill in matches:
    print(f"{skill['name']}: {skill['description']}")
```

### 安装前检查

```python
def install_with_check(skill_name, project_path):
    """安装前检查技能是否存在"""

    # 1. 列出所有技能
    skills = get_available_skills()
    skill_names = [s["name"] for s in skills]

    # 2. 检查技能是否存在
    if skill_name not in skill_names:
        print(f"错误: 技能 '{skill_name}' 不存在")
        print(f"可用技能: {', '.join(skill_names)}")
        return False

    # 3. 安装技能
    cmd = [
        "winwin-cli", "skills", "install",
        skill_name, project_path,
        "--platform", "claude-code"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✓ 技能 '{skill_name}' 安装成功")
        return True
    else:
        print(f"✗ 安装失败: {result.stderr}")
        return False
```

## 安装位置

### Claude Code 平台

技能安装到：`<project-path>/.claude/plugins/skills/`

```bash
# 安装后目录结构
project/
└── .claude/
    └── plugins/
        └── skills/
            └── git-workflow.md
```

### OpenCode 平台

技能安装到：`<project-path>/.opencode/skills/`

```bash
# 安装后目录结构
project/
└── .opencode/
    └── skills/
        └── git-workflow.md
```

## 技能目录结构

一个完整的技能应包含：

```
skill-name/
├── SKILL.md              # 技能主文件（必需）
├── examples.json         # 使用示例（推荐）
├── README.md             # 详细说明（可选）
└── scripts/              # 安装脚本（可选）
    └── install.sh        # 安装时执行
```

### SKILL.md 格式

```markdown
---
name: skill-name
description: "技能描述"
version: 1.0.0
author: "作者名称"
---

# 技能标题

技能详细说明...

## 触发场景
...

## 使用方法
...
```

## 使用场景

### 场景 1：项目初始化

为新项目安装标准技能集：

```bash
# 安装 Git 工作流技能
winwin-cli skills install git-workflow --platform claude-code

# 安装代码审查技能
winwin-cli skills install code-review --platform claude-code

# 安装测试技能
winwin-cli skills install test-helper --platform claude-code
```

### 场景 2：技能发现

查找并安装相关技能：

```bash
# 1. 列出所有技能
winwin-cli skills list --json > skills.json

# 2. 查看感兴趣的技能
winwin-cli skills info git-workflow

# 3. 安装技能
winwin-cli skills install git-workflow --platform claude-code
```

### 场景 3：自动化配置

在项目脚本中自动安装技能：

```python
#!/usr/bin/env python3
"""项目配置脚本"""

import subprocess

REQUIRED_SKILLS = [
    "git-workflow",
    "code-review",
    "documentation-helper"
]

def setup_project_skills():
    """安装项目所需技能"""
    project_path = "/path/to/project"

    for skill in REQUIRED_SKILLS:
        subprocess.run(
            ["winwin-cli", "skills", "install", skill,
             project_path, "--platform", "claude-code"],
            check=True
        )
        print(f"✓ 已安装技能: {skill}")

if __name__ == "__main__":
    setup_project_skills()
```

## 故障排查

### 技能目录不存在

```bash
# 检查技能源目录
ls -la /path/to/winwin-cli/skills

# 确认技能名称
winwin-cli skills list
```

### 安装失败

```bash
# 检查目标目录权限
ls -la /path/to/project

# 检查磁盘空间
df -h

# 尝试安装到当前目录
cd /tmp
winwin-cli skills install git-workflow --platform claude-code
```

### 技能未生效

```bash
# 检查安装位置
ls -la /path/to/project/.claude/plugins/skills/

# 确认技能文件存在
cat /path/to/project/.claude/plugins/skills/git-workflow.md

# 重启 Claude Code 使其生效
```

## 技能开发

### 创建新技能

1. **创建技能目录**：
```bash
mkdir -p /path/to/winwin-cli/skills/my-skill
```

2. **创建 SKILL.md**：
```markdown
---
name: my-skill
description: "我的自定义技能"
version: 1.0.0
---

# 我的技能

技能描述...
```

3. **添加示例**：
```json
{
  "example": {
    "description": "使用示例",
    "command": "命令示例"
  }
}
```

4. **测试技能**：
```bash
# 列出技能
winwin-cli skills list

# 查看详情
winwin-cli skills info my-skill

# 安装测试
winwin-cli skills install my-skill --platform claude-code
```

## 最佳实践

1. **明确技能名称**：AI 调用时始终提供完整技能名称
2. **指定平台**：使用 `--platform` 避免歧义
3. **检查安装**：安装后验证技能文件存在
4. **版本管理**：在 SKILL.md 中维护版本号
5. **文档完整**：提供清晰的使用说明和示例

## 与其他工具集成

### 配合 kb-search

```bash
# 1. 搜索技能文档
winwin-cli kb-search search "git workflow" --kb skills-docs

# 2. 安装相关技能
winwin-cli skills install git-workflow --platform claude-code
```

### 配合项目管理

```bash
# 在项目 Makefile 中
.PHONY: install-skills
install-skills:
	winwin-cli skills install git-workflow --platform claude-code
	winwin-cli skills install code-review --platform claude-code
```
