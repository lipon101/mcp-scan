"""Shared helpers for check modules."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".mypy_cache", ".pytest_cache"}
CODE_EXTS = {".py", ".js", ".ts", ".jsx", ".tsx"}
CONFIG_EXTS = {".json", ".yaml", ".yml", ".toml", ".env", ".sh", ".cfg", ".ini", ".txt", ".md"}


def iter_files(root: Path, max_files: int = 3000) -> Iterable[Path]:
    """Yield files under root, skipping VCS/build/dep dirs. Bounded for safety."""
    count = 0
    if not root.is_dir():
        return
    for p in root.rglob("*"):
        if count >= max_files:
            break
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.is_file():
            count += 1
            yield p


def read_text(p: Path, limit: int = 300_000) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")[:limit]
    except Exception:
        return ""


def find_readme(root: Path) -> Optional[Path]:
    for name in ["README.md", "README.MD", "README.markdown", "README.rst", "README.txt", "README"]:
        f = root / name
        if f.exists():
            return f
    return None
