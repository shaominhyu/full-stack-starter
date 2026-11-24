"""Check whether local evidence cited by project context entries has changed."""

import hashlib
import re
from collections.abc import Iterator
from pathlib import Path
from urllib.parse import unquote

SOURCE_LINE = re.compile(r"-\s+\[[^\]]+\]\((.+)\)\s+<!--\s*sha256:([0-9a-f]{64})\s*-->")
SOURCE_MARKER = re.compile(
    r"<!--\s*(?:sha[-_ ]?\d+|[\w-]+:\s*[0-9a-f]{64}\s*-->)", re.IGNORECASE
)
FENCE = re.compile(r"(`{3,}|~{3,})(.*)")


def source_lines(markdown: str) -> Iterator[tuple[int, str]]:
    """Yield annotated links, including malformed ones, outside code fences."""
    fence = ""
    for number, raw_line in enumerate(markdown.splitlines(), start=1):
        line = raw_line.strip()
        if fence:
            if line.startswith(fence) and not line.strip(fence[0]):
                fence = ""
            continue
        match = FENCE.fullmatch(line)
        if match:
            fence = match[1]
            continue
        if SOURCE_MARKER.search(line):
            yield number, line


def check_source(page: Path, line: str, project: Path) -> tuple[int, str]:
    match = SOURCE_LINE.fullmatch(line)
    if not match:
        return 2, f"核对标记格式错误：{line}"

    reference, expected = match.groups()
    destination = reference.removeprefix("<").removesuffix(">")
    filename = unquote(destination.split("#", 1)[0])
    if (
        not filename
        or Path(filename).is_absolute()
        or re.match(r"^[\w+.-]+:", filename)
    ):
        return 2, f"来源须使用相对文件路径：{reference}"

    try:
        source = (page.parent / filename).resolve()
        if not source.is_relative_to(project):
            return 2, f"核对来源超出项目目录：{reference}"
        if not source.is_file():
            return 1, f"来源缺失或已不是文件：{reference}"
        digest = hashlib.sha256()
        with source.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
    except (OSError, RuntimeError, ValueError) as error:
        return 2, f"无法读取来源 {reference}：{error}"

    if digest.hexdigest() != expected:
        return 1, f"来源内容已变，请复核条目：{reference}"
    return 0, ""


def check(context: Path) -> int:
    project = context.parent.resolve()
    count = 0
    exit_code = 0
    for folder in ("guides", "questions"):
        for page in sorted((context / folder).rglob("*.md")):
            name = page.relative_to(context)
            try:
                if not page.resolve().is_relative_to(project):
                    print(f"{name} 条目超出项目目录。")
                    exit_code = 2
                    continue
                markdown = page.read_text(encoding="utf-8")
            except (OSError, RuntimeError, UnicodeError) as error:
                print(f"{name} 无法读取条目：{error}")
                exit_code = 2
                continue
            for number, line in source_lines(markdown):
                count += 1
                status, message = check_source(page, line, project)
                if status:
                    print(f"{name}:{number} {message}")
                    exit_code = max(exit_code, status)
    print(f"已检查 {count} 条本地来源引用。")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(check(Path(__file__).resolve().parent))
