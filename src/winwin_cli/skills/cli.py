"""Skills CLI command - Manage and install skills."""

import os
import sys
import subprocess
import tempfile
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
import click
import yaml
import requests
from pathlib import Path
from typing import Optional, List, Tuple


@click.group()
def skills():
    """技能管理命令 - 安装和管理 Claude Code 技能"""
    pass


@skills.command()
@click.argument("skill_spec", required=False)
@click.argument("path", required=False, type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option(
    "--platform",
    type=click.Choice(["claude-code", "opencode"], case_sensitive=False),
    help="目标平台",
)
@click.option(
    "--branch", "ref",
    default="main",
    help="Git 分支或标签（默认: main）",
)
@click.option(
    "--repo",
    help="覆盖默认的 GitHub 仓库（格式: owner/repo）",
)
def install(skill_spec: Optional[str], path: Optional[str], platform: Optional[str], ref: str, repo: Optional[str]):
    """从 GitHub 仓库安装技能到指定位置

    用法：
        winwin-cli skills install                           # 从配置列表交互式选择
        winwin-cli skills install skill-name                # 使用简写名称（在所有分类中查找）
        winwin-cli skills install category/skill-name       # 使用完整路径
        winwin-cli skills install owner/repo/category/skill-name
        winwin-cli skills install https://github.com/...    # 使用完整 GitHub URL
        winwin-cli skills install skill-name --repo owner/custom-repo
        winwin-cli skills install skill-name --branch dev
    """
    try:
        # 确定安装路径（path 参数或当前目录）
        install_path = Path(path) if path else Path.cwd()

        # 如果没有指定技能，显示列表供选择
        if not skill_spec:
            skill_spec = _interactive_select_skill(repo)
            if not skill_spec:
                click.echo("未选择技能", err=True)
                sys.exit(1)

        # 如果只输入了技能名称（没有 /），尝试在所有分类中查找
        if skill_spec and "/" not in skill_spec and not skill_spec.startswith("https://"):
            resolved_spec = _find_skill_by_name(skill_spec, ref, repo)
            if resolved_spec:
                click.echo(f"找到技能: {resolved_spec}")
                skill_spec = resolved_spec
            else:
                click.echo(f"警告: 未找到技能 '{skill_spec}'，尝试直接下载...", err=True)

        # 解析技能规格并下载
        skill_temp_dir = _resolve_and_download_skill(skill_spec, ref, repo)
        if not skill_temp_dir:
            sys.exit(1)

        try:
            # 获取技能名称
            skill_name = _get_skill_name(skill_temp_dir)

            # 解析技能元数据
            skill_file = skill_temp_dir / "SKILL.md"
            if not skill_file.exists():
                click.echo(f"错误: 技能文件不存在: SKILL.md", err=True)
                sys.exit(1)

            skill_metadata = _parse_skill_metadata(skill_file)

            # 如果没有指定平台，交互式选择
            if not platform:
                click.echo("\n选择目标平台：")
                click.echo("  1. claude-code")
                click.echo("  2. opencode")

                platform_choice = click.prompt("\n选择平台（输入序号）", type=int)
                platform = "claude-code" if platform_choice == 1 else "opencode"

            # 执行安装
            _install_skill(skill_temp_dir, skill_name, install_path, platform, skill_metadata)

            click.echo(f"\n✅ 技能 '{skill_name}' 安装成功！")
            click.echo(f"   平台: {platform}")
            click.echo(f"   路径: {install_path}")

        finally:
            # 清理临时目录
            if skill_temp_dir and skill_temp_dir.exists():
                shutil.rmtree(skill_temp_dir, ignore_errors=True)

    except Exception as e:
        click.echo(f"错误: {e}", err=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


@skills.command("list")
@click.option(
    "--json", "output_json",
    is_flag=True,
    help="以 JSON 格式输出（用于 AI 调用）",
)
@click.option(
    "--repo",
    help="指定 GitHub 仓库（格式: owner/repo）",
)
@click.option(
    "--branch", "ref",
    default="main",
    help="Git 分支或标签（默认: main）",
)
def list_cmd(output_json: bool, repo: Optional[str], ref: str):
    """列出所有可用的技能（从 GitHub 仓库）"""
    try:
        # 获取配置的默认仓库
        default_repo = repo or _get_default_skills_repo()

        click.echo(f"正在从 GitHub 仓库获取技能列表: {default_repo} (branch: {ref})...")

        # 从 GitHub API 获取技能列表
        available_skills = _list_github_skills(default_repo, ref)

        if not available_skills:
            click.echo("未找到可用技能")
            return

        if output_json:
            import json
            click.echo(json.dumps(available_skills, ensure_ascii=False, indent=2))
        else:
            if not available_skills:
                click.echo("未找到可用技能")
            else:
                click.echo(f"\n找到 {len(available_skills)} 个技能：\n")
                for skill in available_skills:
                    category = skill.get("category", "")
                    skill_name = skill['name']
                    if category:
                        click.echo(f"📦 {skill_name} (分类: {category})")
                        click.echo(f"   安装: winwin-cli skills install {category}/{skill_name}")
                    else:
                        click.echo(f"📦 {skill_name}")
                        click.echo(f"   安装: winwin-cli skills install {skill_name}")
                    click.echo(f"   描述: {skill.get('description', '无描述')}")
                    click.echo(f"   版本: {skill.get('version', 'N/A')}")
                    click.echo(f"   作者: {skill.get('author', 'N/A')}")
                    click.echo()

    except Exception as e:
        click.echo(f"错误: {e}", err=True)
        sys.exit(1)


@skills.command()
@click.argument("skill_spec")
@click.option(
    "--repo",
    help="指定 GitHub 仓库（格式: owner/repo）",
)
@click.option(
    "--branch", "ref",
    default="main",
    help="Git 分支或标签（默认: main）",
)
def info(skill_spec: str, repo: Optional[str], ref: str):
    """显示技能详细信息（从 GitHub 仓库）

    技能规格格式:
    - category/skill-name (使用默认仓库)
    - owner/repo/category/skill-name
    - skill-name (在所有分类中查找)
    """
    try:
        # 如果只输入了技能名称（没有 /），尝试在所有分类中查找
        if "/" not in skill_spec:
            skill_spec = _find_skill_by_name(skill_spec, ref, repo)
            if not skill_spec:
                click.echo(f"错误: 未找到技能 '{skill_spec}'", err=True)
                click.echo(f"提示: 使用 'winwin-cli skills list' 查看所有可用技能", err=True)
                sys.exit(1)

        # 下载技能到临时目录
        skill_temp_dir = _resolve_and_download_skill(skill_spec, ref, repo)
        if not skill_temp_dir:
            sys.exit(1)

        try:
            skill_name = _get_skill_name(skill_temp_dir)
            skill_file = skill_temp_dir / "SKILL.md"

            if not skill_file.exists():
                click.echo(f"错误: 技能文件不存在: SKILL.md", err=True)
                sys.exit(1)

            # 解析技能元数据
            metadata = _parse_skill_metadata(skill_file)

            # 显示信息
            click.echo(f"\n📦 技能: {metadata.get('name', skill_name)}")
            click.echo(f"{'='*50}")
            click.echo(f"描述: {metadata.get('description', '无描述')}")
            click.echo(f"版本: {metadata.get('version', 'N/A')}")
            click.echo(f"作者: {metadata.get('author', 'N/A')}")

            # 显示支持的文件
            click.echo(f"\n包含的文件:")
            for item in sorted(skill_temp_dir.rglob("*")):
                if item.is_file():
                    rel_path = item.relative_to(skill_temp_dir)
                    click.echo(f"  - {rel_path}")

            click.echo()

        finally:
            # 清理临时目录
            if skill_temp_dir and skill_temp_dir.exists():
                shutil.rmtree(skill_temp_dir, ignore_errors=True)

    except Exception as e:
        click.echo(f"错误: {e}", err=True)
        sys.exit(1)


def _find_skill_by_name(skill_name: str, ref: str, repo_override: Optional[str]) -> Optional[str]:
    """在所有分类中查找指定名称的技能

    返回完整的技能规格 (如: category/skill-name)
    """
    try:
        default_repo = repo_override or _get_default_skills_repo()
        all_skills = _list_github_skills(default_repo, ref)

        # 查找匹配的技能
        for skill in all_skills:
            if skill.get("name") == skill_name:
                category = skill.get("category", "")
                if category:
                    return f"{default_repo}/{category}/{skill_name}"
                else:
                    return f"{default_repo}/{skill_name}"

        # 如果没有找到精确匹配，尝试模糊匹配
        for skill in all_skills:
            if skill_name.lower() in skill.get("name", "").lower():
                category = skill.get("category", "")
                if category:
                    return f"{default_repo}/{category}/{skill['name']}"
                else:
                    return f"{default_repo}/{skill['name']}"

        return None

    except Exception as e:
        click.echo(f"查找技能失败: {e}", err=True)
        return None


def _get_default_skills_repo() -> str:
    """获取默认的技能仓库"""
    # 可以从环境变量或配置文件读取
    # 例如: export WINWIN_SKILLS_REPO="owner/skills-repo"
    return os.environ.get("WINWIN_SKILLS_REPO", "heibaibufen/winwin-skills")


def _interactive_select_skill(repo_override: Optional[str]) -> Optional[str]:
    """交互式选择技能"""
    try:
        default_repo = repo_override or _get_default_skills_repo()
        click.echo(f"正在从仓库获取技能列表: {default_repo}")

        available_skills = _list_github_skills(default_repo, "main")

        if not available_skills:
            click.echo("未找到可用技能", err=True)
            return None

        click.echo("\n可用的技能：")
        for idx, skill in enumerate(available_skills, 1):
            click.echo(f"  {idx}. {skill['name']} - {skill.get('description', '无描述')}")

        # 让用户选择
        choice = click.prompt("\n选择要安装的技能（输入序号）", type=int)
        if choice < 1 or choice > len(available_skills):
            click.echo("无效的选择", err=True)
            return None

        skill_name = available_skills[choice - 1]["name"]
        category = available_skills[choice - 1].get("category", "")
        click.echo(f"\n已选择: {skill_name}")

        # 构建技能规格（包含分类）
        if category:
            return f"{default_repo}/{category}/{skill_name}"
        else:
            return f"{default_repo}/{skill_name}"

    except Exception as e:
        click.echo(f"获取技能列表失败: {e}", err=True)
        return None


def _resolve_and_download_skill(skill_spec: str, ref: str, repo_override: Optional[str]) -> Optional[Path]:
    """解析技能规格并下载到临时目录

    支持的格式:
    - https://github.com/owner/repo/tree/main/category/skill-name
    - https://github.com/owner/repo/tree/branch/category/skill-name
    - owner/repo/category/skill-name
    - owner/repo/skill-name
    - skill-name (使用默认仓库)
    """
    temp_dir = None

    try:
        # 解析 GitHub URL
        if skill_spec.startswith("https://github.com/"):
            # 从 URL 解析
            parts = skill_spec.replace("https://github.com/", "").split("/tree/")
            repo_path = parts[0]

            if len(parts) > 1:
                ref = parts[1].split("/")[0]  # 获取分支名
                skill_name = "/".join(parts[1].split("/")[1:])  # 获取技能路径
            else:
                skill_name = repo_path.split("/")[-1]
                repo_path = "/".join(repo_path.split("/")[:-1])

            owner, repo = repo_path.split("/")
            skill_path = skill_name

        elif "/" in skill_spec:
            # owner/repo/skill-name 或 owner/repo 格式
            parts = skill_spec.split("/")
            if len(parts) >= 3:
                owner, repo = parts[0], parts[1]
                skill_path = "/".join(parts[2:])
            else:
                # 使用提供的 repo 或默认仓库
                if repo_override:
                    owner, repo = repo_override.split("/")
                    skill_path = skill_spec
                else:
                    default_repo = _get_default_skills_repo()
                    owner, repo = default_repo.split("/")
                    skill_path = skill_spec
        else:
            # 仅技能名称，使用默认仓库
            default_repo = repo_override or _get_default_skills_repo()
            owner, repo = default_repo.split("/")
            skill_path = skill_spec

        click.echo(f"正在下载技能: {owner}/{repo}/{skill_path} (ref: {ref})")

        # 下载技能
        temp_dir = _download_skill_from_github(owner, repo, skill_path, ref)
        return temp_dir

    except Exception as e:
        click.echo(f"下载技能失败: {e}", err=True)
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)
        return None


def _download_skill_from_github(owner: str, repo: str, skill_path: str, ref: str = "main") -> Optional[Path]:
    """从 GitHub 下载技能目录到临时目录（使用并发下载加速）

    使用 GitHub API 获取目录内容并使用并发下载
    """
    temp_dir = Path(tempfile.mkdtemp(prefix="winwin_skill_"))

    try:
        # 首先收集所有需要下载的文件
        files_to_download = []

        def _collect_files(api_url: str, local_dir: Path):
            """递归收集所有文件"""
            response = requests.get(api_url, params={"ref": ref}, timeout=30)
            response.raise_for_status()

            items = response.json()

            if not isinstance(items, list):
                items = [items]

            for item in items:
                if item.get("type") == "file":
                    download_url = item.get("download_url")
                    if download_url:
                        file_path = local_dir / item["name"]
                        files_to_download.append((download_url, file_path, item.get("path", item["name"])))

                elif item.get("type") == "dir":
                    sub_dir = local_dir / item["name"]
                    _collect_files(item["url"], sub_dir)

        # 收集所有文件
        api_base = f"https://api.github.com/repos/{owner}/{repo}/contents/{skill_path}"
        click.echo(f"正在分析技能目录结构...")
        _collect_files(api_base, temp_dir)

        if not files_to_download:
            click.echo(f"错误: 未找到任何文件", err=True)
            shutil.rmtree(temp_dir, ignore_errors=True)
            return None

        # 使用并发下载
        click.echo(f"正在下载 {len(files_to_download)} 个文件...")

        def _download_file(args: Tuple[str, Path, str]) -> Tuple[bool, str]:
            """下载单个文件"""
            download_url, file_path, display_path = args
            try:
                response = requests.get(download_url, timeout=30)
                response.raise_for_status()

                file_path.parent.mkdir(parents=True, exist_ok=True)

                with open(file_path, "wb") as f:
                    f.write(response.content)

                return (True, display_path)
            except Exception as e:
                return (False, f"{display_path}: {e}")

        # 使用线程池并发下载（最多 10 个并发）
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(_download_file, args): args for args in files_to_download}

            completed = 0
            failed = 0

            for future in as_completed(futures):
                completed += 1
                success, result = future.result()

                if success:
                    # 每下载 10% 显示一次进度
                    if completed % max(1, len(files_to_download) // 10) == 0 or completed == len(files_to_download):
                        click.echo(f"  进度: {completed}/{len(files_to_download)} 文件已完成")
                else:
                    failed += 1
                    click.echo(f"  ✗ 下载失败: {result}", err=True)

        if failed > 0:
            click.echo(f"警告: {failed} 个文件下载失败", err=True)

        # 验证 SKILL.md 是否存在
        skill_md = temp_dir / "SKILL.md"
        if not skill_md.exists():
            click.echo(f"警告: 下载的目录中未找到 SKILL.md", err=True)

        return temp_dir

    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        click.echo(f"从 GitHub 下载失败: {e}", err=True)
        return None


def _get_skill_name(skill_dir: Path) -> str:
    """从 SKILL.md 或目录名获取技能名称"""
    skill_file = skill_dir / "SKILL.md"

    if skill_file.exists():
        metadata = _parse_skill_metadata(skill_file)
        if metadata.get("name"):
            return metadata["name"]

    # 如果元数据中没有名称，使用目录名
    return skill_dir.name


def _list_github_skills(repo: str, ref: str = "main") -> List[dict]:
    """从 GitHub 仓库列出所有技能

    扫描仓库根目录的分类子目录，在每个分类下查找包含 SKILL.md 的技能目录
    结构: repo/category/skill-name/
    """
    try:
        owner, repo_name = repo.split("/")

        # 获取仓库根目录内容
        api_url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/"
        response = requests.get(api_url, params={"ref": ref}, timeout=30)
        response.raise_for_status()

        categories = response.json()

        # 检查返回的数据格式
        if not isinstance(categories, list):
            click.echo(f"警告: GitHub API 返回了意外的数据格式", err=True)
            if isinstance(categories, dict):
                # 可能是错误信息
                if "message" in categories:
                    click.echo(f"错误信息: {categories.get('message')}", err=True)
                if "documentation_url" in categories:
                    click.echo(f"文档: {categories.get('documentation_url')}", err=True)
            return []

        skills = []

        # 遍历每个分类目录
        for category in categories:
            if not isinstance(category, dict):
                continue

            if category.get("type") == "dir":
                category_name = category["name"]
                category_url = f"{api_url}{category_name}"

                try:
                    # 获取分类目录下的内容
                    cat_response = requests.get(category_url, params={"ref": ref}, timeout=30)
                    cat_response.raise_for_status()
                    items = cat_response.json()

                    if not isinstance(items, list):
                        continue

                    # 在分类目录下查找技能
                    for item in items:
                        if not isinstance(item, dict):
                            continue

                        if item.get("type") == "dir":
                            # 检查是否包含 SKILL.md
                            skill_api_url = f"{category_url}/{item['name']}"
                            try:
                                skill_response = requests.get(skill_api_url, params={"ref": ref}, timeout=30)
                                skill_response.raise_for_status()
                                skill_items = skill_response.json()

                                if isinstance(skill_items, list) and any(i.get("name") == "SKILL.md" for i in skill_items if isinstance(i, dict)):
                                    # 下载 SKILL.md 获取元数据
                                    skill_md_url = f"{skill_api_url}/SKILL.md"
                                    md_response = requests.get(skill_md_url, params={"ref": ref}, timeout=30)

                                    metadata = {}
                                    if md_response.status_code == 200:
                                        try:
                                            md_content = md_response.json()
                                            if isinstance(md_content, dict) and md_content.get("encoding") == "base64":
                                                import base64
                                                content = base64.b64decode(md_content["content"]).decode("utf-8")
                                                # 解析 YAML 前置元数据
                                                metadata = _parse_skill_metadata_from_content(content)
                                        except Exception as e:
                                            click.echo(f"警告: 解析 {category_name}/{item['name']} 的元数据失败: {e}", err=True)

                                    skills.append({
                                        "name": metadata.get("name", item["name"]),
                                        "description": metadata.get("description", "无描述"),
                                        "version": metadata.get("version", "N/A"),
                                        "author": metadata.get("author", "N/A"),
                                        "category": category_name,
                                        "path": f"{repo}/{category_name}/{item['name']}",
                                    })

                            except requests.exceptions.RequestException as e:
                                click.echo(f"警告: 获取技能 {category_name}/{item['name']} 信息失败: {e}", err=True)
                                continue

                except requests.exceptions.RequestException as e:
                    click.echo(f"警告: 获取分类 {category_name} 的内容失败: {e}", err=True)
                    continue

        return sorted(skills, key=lambda x: (x.get("category", ""), x["name"]))

    except requests.exceptions.RequestException as e:
        click.echo(f"从 GitHub 获取技能列表失败: {e}", err=True)
        return []
    except Exception as e:
        click.echo(f"从 GitHub 获取技能列表失败: {e}", err=True)
        import traceback
        traceback.print_exc()
        return []


def _parse_skill_metadata_from_content(content: str) -> dict:
    """从 SKILL.md 内容解析 YAML 前置元数据"""
    try:
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                yaml_content = parts[1]
                return yaml.safe_load(yaml_content) or {}

        return {}
    except Exception as e:
        return {}


def _parse_skill_metadata(skill_file: Path) -> dict:
    """解析 SKILL.md 文件中的 YAML 前置元数据"""
    try:
        with open(skill_file, "r", encoding="utf-8") as f:
            content = f.read()

        # 提取 YAML 前置元数据（在 --- 之间）
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                yaml_content = parts[1]
                return yaml.safe_load(yaml_content) or {}

        return {}
    except Exception as e:
        click.echo(f"警告: 无法解析技能元数据: {e}", err=True)
        return {}


def _install_skill(skill_path: Path, skill_name: str, install_path: Path, platform: str, metadata: dict):
    """执行技能安装"""
    if platform == "claude-code":
        _install_for_claude_code(skill_path, skill_name, install_path, metadata)
    elif platform == "opencode":
        _install_for_opencode(skill_path, skill_name, install_path, metadata)
    else:
        click.echo(f"错误: 不支持的平台: {platform}", err=True)
        sys.exit(1)


def _install_for_claude_code(skill_path: Path, skill_name: str, install_path: Path, metadata: dict):
    """安装到 Claude Code"""
    import shutil

    # 创建 .claude/skills 目录结构
    claude_skills_dir = install_path / ".claude" / "skills"
    claude_skills_dir.mkdir(parents=True, exist_ok=True)

    # 复制整个技能目录
    dest_skill_dir = claude_skills_dir / skill_name
    if dest_skill_dir.exists():
        shutil.rmtree(dest_skill_dir)

    shutil.copytree(skill_path, dest_skill_dir)
    click.echo(f"✓ 已复制技能目录到: {dest_skill_dir}")

    # 不再需要单独执行 install.sh，因为整个目录已经复制了
    # 保留这个逻辑以向后兼容
    install_script = skill_path / "scripts" / "install.sh"
    if install_script.exists():
        click.echo(f"✓ 检测到安装脚本（已随目录复制）")
        # 不执行脚本，因为整个目录已经复制完成
        # 如果需要执行，可以取消下面的注释
        # subprocess.run(["bash", str(install_script), str(skill_path)], cwd=install_path, check=True)


def _install_for_opencode(skill_path: Path, skill_name: str, install_path: Path, metadata: dict):
    """安装到 OpenCode（待实现）"""
    import shutil

    click.echo(f"警告: OpenCode 平台支持尚未完全实现", err=True)
    click.echo(f"提示: 复制技能文件，但可能需要手动配置", err=True)

    # 创建示例目录结构
    opencode_skills_dir = install_path / ".opencode" / "skills"
    opencode_skills_dir.mkdir(parents=True, exist_ok=True)

    # 复制整个技能目录
    dest_skill_dir = opencode_skills_dir / skill_name
    if dest_skill_dir.exists():
        shutil.rmtree(dest_skill_dir)

    shutil.copytree(skill_path, dest_skill_dir)

    click.echo(f"✓ 已复制技能目录到: {dest_skill_dir}")
    click.echo(f"  (平台适配需要进一步配置)")


__all__ = ["skills"]
