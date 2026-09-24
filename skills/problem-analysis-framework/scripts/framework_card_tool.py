"""框架卡工具：生成空白模板、校验字段完整性、渲染为 Markdown 卡片。

只依赖标准库。解析的是受限 YAML 子集（顶层 `key: value` 与 `- item` 列表），
选择自实现解析器而非引入 PyYAML，是为了让本脚本在任意环境零安装即可运行。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# (字段键, 中文标签, 是否必填)，顺序即渲染顺序
CARD_SCHEMA = (
    ("name", "框架名", True),
    ("source", "来源", True),
    ("one_line_definition", "一句话定义", True),
    ("when_to_use", "适用场景", True),
    ("when_not_to_use", "不适用场景", True),
    ("goal", "目标", True),
    ("inputs", "输入", True),
    ("outputs", "输出", True),
    ("steps", "核心步骤", True),
    ("decision_rules", "判断规则", True),
    ("question_checklist", "提问清单", True),
    ("common_tools", "常用工具", False),
    ("common_mistakes", "常见错误", True),
    ("quality_checks", "检查清单", True),
    ("positive_example", "正例", True),
    ("negative_example", "反例", True),
    ("source_location", "原文位置", False),
)


def is_ignorable_line(stripped_line: str) -> bool:
    if not stripped_line:
        return True
    return stripped_line.startswith("#")


def append_list_item(card_fields: dict, list_key: str, list_item: str) -> None:
    if list_key is None:
        return
    if not isinstance(card_fields.get(list_key), list):
        card_fields[list_key] = []
    card_fields[list_key].append(list_item)


def parse_card_fields(raw_text: str) -> dict:
    card_fields: dict = {}
    current_list_key = None
    for raw_line in raw_text.splitlines():
        stripped_line = raw_line.strip()
        if is_ignorable_line(stripped_line=stripped_line):
            continue
        if stripped_line.startswith("- "):
            append_list_item(
                card_fields=card_fields,
                list_key=current_list_key,
                list_item=stripped_line[2:].strip(),
            )
            continue
        if ":" not in stripped_line:
            continue
        field_key, _, field_value = stripped_line.partition(":")
        field_key = field_key.strip()
        field_value = field_value.strip()
        if field_value:
            card_fields[field_key] = field_value
            current_list_key = None
            continue
        card_fields[field_key] = []
        current_list_key = field_key
    return card_fields


def is_field_populated(field_value) -> bool:
    if field_value is None:
        return False
    if isinstance(field_value, str):
        return bool(field_value.strip())
    if isinstance(field_value, (list, tuple, dict, set)):
        return len(field_value) > 0
    return True


def find_missing_fields(card_fields: dict) -> list:
    missing_labels = []
    for field_key, field_label, is_required in CARD_SCHEMA:
        if not is_required:
            continue
        if is_field_populated(field_value=card_fields.get(field_key)):
            continue
        missing_labels.append(field_label)
    return missing_labels


def read_text(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8")


def validate_card_file(card_path: Path) -> bool:
    card_fields = parse_card_fields(raw_text=read_text(file_path=card_path))
    missing_labels = find_missing_fields(card_fields=card_fields)
    if not missing_labels:
        print(f"[通过] {card_path}")
        return True
    joined_labels = "、".join(missing_labels)
    print(f"[失败] {card_path} 缺少或为空的字段：{joined_labels}")
    return False


def render_field_lines(field_label: str, field_value) -> list:
    if not is_field_populated(field_value=field_value):
        return []
    if isinstance(field_value, str):
        return [f"**{field_label}**：{field_value}", ""]
    item_lines = [f"- {list_item}" for list_item in field_value]
    return [f"**{field_label}**：", *item_lines, ""]


def render_card_to_markdown(card_fields: dict) -> str:
    card_name = card_fields.get("name", "未命名框架")
    output_lines = [f"# 框架卡：{card_name}", ""]
    for field_key, field_label, _ in CARD_SCHEMA:
        field_lines = render_field_lines(
            field_label=field_label,
            field_value=card_fields.get(field_key),
        )
        output_lines.extend(field_lines)
    return "\n".join(output_lines) + "\n"


def build_scaffold_template(card_name: str) -> str:
    template_lines = [f"name: {card_name}"]
    for field_key, field_label, _ in CARD_SCHEMA:
        if field_key == "name":
            continue
        template_lines.append(f"# {field_label}")
        template_lines.append(f"{field_key}:")
    return "\n".join(template_lines) + "\n"


def run_scaffold(command_arguments: argparse.Namespace) -> int:
    template_text = build_scaffold_template(card_name=command_arguments.card_name)
    output_path = Path(command_arguments.output)
    output_path.write_text(template_text, encoding="utf-8")
    print(f"[完成] 已生成框架卡模板：{output_path}")
    return 0


def run_validate(command_arguments: argparse.Namespace) -> int:
    target_path = Path(command_arguments.card_path)
    if target_path.is_dir():
        card_paths = sorted(target_path.glob("*.yaml"))
    else:
        card_paths = [target_path]
    if not card_paths:
        print(f"[失败] 未找到框架卡：{target_path}")
        return 1
    validation_results = []
    for card_path in card_paths:
        validation_results.append(validate_card_file(card_path=card_path))
    if all(validation_results):
        return 0
    return 1


def run_render(command_arguments: argparse.Namespace) -> int:
    card_path = Path(command_arguments.card_path)
    card_fields = parse_card_fields(raw_text=read_text(file_path=card_path))
    markdown_text = render_card_to_markdown(card_fields=card_fields)
    if command_arguments.output:
        output_path = Path(command_arguments.output)
        output_path.write_text(markdown_text, encoding="utf-8")
        print(f"[完成] 已渲染框架卡：{output_path}")
        return 0
    print(markdown_text)
    return 0


def run_command(arguments: argparse.Namespace) -> int:
    if arguments.command == "scaffold":
        return run_scaffold(command_arguments=arguments)
    if arguments.command == "validate":
        return run_validate(command_arguments=arguments)
    if arguments.command == "render":
        return run_render(command_arguments=arguments)
    print(f"[失败] 未知命令：{arguments.command}")
    return 2


def build_argument_parser() -> argparse.ArgumentParser:
    argument_parser = argparse.ArgumentParser(description="框架卡生成、校验与渲染工具")
    subparsers = argument_parser.add_subparsers(dest="command", required=True)

    scaffold_parser = subparsers.add_parser("scaffold", help="生成空白框架卡模板")
    scaffold_parser.add_argument("--card-name", required=True, help="框架名，snake_case")
    scaffold_parser.add_argument("--output", required=True, help="模板输出路径")

    validate_parser = subparsers.add_parser("validate", help="校验框架卡字段完整性")
    validate_parser.add_argument("--card-path", required=True, help="卡文件或卡所在目录")

    render_parser = subparsers.add_parser("render", help="渲染框架卡为 Markdown")
    render_parser.add_argument("--card-path", required=True, help="卡文件路径")
    render_parser.add_argument("--output", default="", help="Markdown 输出路径，缺省打印到标准输出")
    return argument_parser


def main() -> None:
    argument_parser = build_argument_parser()
    arguments = argument_parser.parse_args()
    exit_code = run_command(arguments=arguments)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
