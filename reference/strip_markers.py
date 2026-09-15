#!/usr/bin/env python3
"""Re-apply LAST_REPLY with the header-split parser and strip leaked Ralph markers.

Used as a verify prefix so a live qwen_iteration.py (old in-memory parser)
cannot leave ### END FILE in .tsx. Harness only — does not invent app UI.
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from qwen_iteration import repo_root, strip_leaked_markers, write_files  # noqa: E402


def main() -> int:
    root = repo_root()
    last = SCRIPT_DIR / "LAST_REPLY.md"
    if last.exists():
        text = last.read_text(errors="replace")
        if text.strip():
            write_files(text, root)
    strip_leaked_markers(root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
