from __future__ import annotations

import re
import subprocess
from pathlib import Path
from urllib.parse import unquote

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"(!?)\[[^\]]*]\(([^)]+)\)")
EXTERNAL_SCHEMES = ("http://", "https://", "mailto:")
IMAGE_SUFFIXES = {".gif", ".jpeg", ".jpg", ".png", ".svg", ".webp"}


def _tracked_markdown_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "*.md"],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
    )
    return [PROJECT_ROOT / item.decode() for item in result.stdout.split(b"\0") if item]


def _local_destination(raw_destination: str) -> str | None:
    destination = raw_destination.strip()
    if destination.startswith("<") and destination.endswith(">"):
        destination = destination[1:-1]
    else:
        destination = destination.split(maxsplit=1)[0]
    if destination.startswith(EXTERNAL_SCHEMES) or destination.startswith("#"):
        return None
    return unquote(destination.split("#", maxsplit=1)[0])


def test_tracked_markdown_links_and_images_have_local_targets() -> None:
    checked_links = 0
    checked_images = 0
    for markdown_path in _tracked_markdown_files():
        content = markdown_path.read_text(encoding="utf-8")
        for image_marker, raw_destination in MARKDOWN_LINK.findall(content):
            destination = _local_destination(raw_destination)
            if not destination:
                continue
            target = (markdown_path.parent / destination).resolve()
            assert target.exists(), f"{markdown_path.relative_to(PROJECT_ROOT)} -> {destination}"
            checked_links += 1
            if image_marker:
                assert target.is_file()
                assert target.suffix.lower() in IMAGE_SUFFIXES
                checked_images += 1

    assert checked_links >= 50
    assert checked_images >= 8
