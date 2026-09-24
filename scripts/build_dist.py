"""校验技能目录并打包为 dist/<技能名>.zip。

仓库自带打包脚本而不是调用 IDE 内置工具，是为了让贡献者只装 Python 就能复现
发布产物——开源仓库的使用者未必使用同一个 IDE。
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = PROJECT_ROOT / "skills"
DIST_ROOT = PROJECT_ROOT / "dist"
SKILL_FILE_NAME = "SKILL.md"
HYPHEN_CASE_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
IGNORED_DIRECTORY_NAMES = frozenset({"__pycache__"})


def read_frontmatter_field(frontmatter_text: str, field_key: str) -> str:
    field_pattern = re.compile(rf"^{field_key}:\s*(.+)$", re.MULTILINE)
    field_match = field_pattern.search(frontmatter_text)
    if field_match is None:
        return ""
    return field_match.group(1).strip()


def collect_skill_problems(skill_directory: Path) -> list[str]:
    skill_file_path = skill_directory / SKILL_FILE_NAME
    if not skill_file_path.exists():
        return [f"{skill_directory.name}: 缺少 {SKILL_FILE_NAME}"]

    frontmatter_match = FRONTMATTER_PATTERN.match(skill_file_path.read_text(encoding="utf-8"))
    if frontmatter_match is None:
        return [f"{skill_directory.name}: 缺少 YAML frontmatter"]

    frontmatter_text = frontmatter_match.group(1)
    declared_name = read_frontmatter_field(frontmatter_text=frontmatter_text, field_key="name")
    declared_description = read_frontmatter_field(
        frontmatter_text=frontmatter_text,
        field_key="description",
    )

    skill_problems = []
    if declared_name != skill_directory.name:
        skill_problems.append(f"{skill_directory.name}: name 为 {declared_name or '空'}，必须与目录名一致")
    elif not HYPHEN_CASE_PATTERN.match(declared_name):
        skill_problems.append(f"{declared_name}: name 只能使用小写字母、数字与单个连字符")
    if not declared_description:
        skill_problems.append(f"{skill_directory.name}: description 不能为空")
    if "<" in declared_description or ">" in declared_description:
        skill_problems.append(f"{skill_directory.name}: description 不能包含尖括号")
    return skill_problems


def collect_skill_directories() -> list[Path]:
    if not SKILLS_ROOT.is_dir():
        return []
    return sorted(skill_path for skill_path in SKILLS_ROOT.iterdir() if skill_path.is_dir())


def collect_all_problems(skill_directories: list[Path]) -> list[str]:
    all_problems = []
    for skill_directory in skill_directories:
        all_problems.extend(collect_skill_problems(skill_directory=skill_directory))
    return all_problems


def is_packable_file(file_path: Path) -> bool:
    if not file_path.is_file():
        return False
    return not IGNORED_DIRECTORY_NAMES.intersection(file_path.parts)


def write_skill_archive(skill_directory: Path) -> Path:
    DIST_ROOT.mkdir(parents=True, exist_ok=True)
    archive_path = DIST_ROOT / f"{skill_directory.name}.zip"
    if archive_path.exists():
        archive_path.unlink()  # 复用旧压缩包会让上一次的条目残留，必须重建

    packable_file_paths = sorted(
        file_path for file_path in skill_directory.rglob("*") if is_packable_file(file_path=file_path)
    )
    with zipfile.ZipFile(file=archive_path, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file_path in packable_file_paths:
            archive.write(
                filename=file_path,
                arcname=Path(skill_directory.name) / file_path.relative_to(skill_directory),
            )
    return archive_path


def run(command_arguments: argparse.Namespace) -> int:
    skill_directories = collect_skill_directories()
    if not skill_directories:
        print(f"[失败] 未找到技能目录：{SKILLS_ROOT}")
        return 1

    all_problems = collect_all_problems(skill_directories=skill_directories)
    if all_problems:
        for problem in all_problems:
            print(f"[失败] {problem}")
        return 1

    if command_arguments.check_only:
        print(f"[通过] {len(skill_directories)} 个技能校验通过")
        return 0

    for skill_directory in skill_directories:
        archive_path = write_skill_archive(skill_directory=skill_directory)
        print(f"[完成] 已打包 {archive_path.relative_to(PROJECT_ROOT)}")
    return 0


def build_argument_parser() -> argparse.ArgumentParser:
    argument_parser = argparse.ArgumentParser(description="校验并打包技能目录")
    argument_parser.add_argument(
        "--check",
        dest="check_only",
        action="store_true",
        help="只校验格式，不生成 zip",
    )
    return argument_parser


def main() -> None:
    argument_parser = build_argument_parser()
    command_arguments = argument_parser.parse_args()
    exit_code = run(command_arguments=command_arguments)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
