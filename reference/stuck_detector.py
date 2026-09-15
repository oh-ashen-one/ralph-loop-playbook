#!/usr/bin/env python3
"""Classify ruts from a Ralph trajectory log. Stdlib only, no LLM calls.

Usage: stuck_detector.py [trajectory.jsonl]   (default: scripts/ralph/trajectory.jsonl)

Prints one JSON verdict: {"stuck": bool, "pattern": str|null, "suggestion": str}.
Patterns (checked over the last WINDOW events, first match wins):
  identical_emission  — same emission_hash 3+ times: the model emits the same
                        reply forever; the story (or its snapshot) is lying
  no_file_blocks      — 4+ consecutive zero-file iterations: format failure
  verify_oscillation  — verify_ok alternates pass/fail for 3+ cycles:
                        fix A breaks B, classic missing-regression-gate rut
  repeated_failure    — same story fails 3+ times with identical verify output:
                        the model is not reading the error, or cannot fix it
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

WINDOW = 20


def load(path: Path) -> list[dict]:
    if not path.exists():
        return []
    events: list[dict] = []
    for line in path.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


def emit(stuck: bool, pattern: str | None, suggestion: str) -> None:
    print(json.dumps({"stuck": stuck, "pattern": pattern, "suggestion": suggestion}))


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("scripts/ralph/trajectory.jsonl")
    events = load(path)
    if not events:
        emit(False, None, "no trajectory yet — nothing to classify")
        return 0
    window = events[-WINDOW:]

    # (a) identical emission 3+ times in the window
    hashes = [e["emission_hash"] for e in window if e.get("emission_hash")]
    if any(hashes.count(h) >= 3 for h in set(hashes)):
        emit(
            True,
            "identical_emission",
            "same reply emitted 3+ times — rewrite the story surgically (exact "
            "file/line/error), shrink the emission to one file, and check the "
            "story is not lying about the state of the tree",
        )
        return 0

    # (b) 4+ consecutive trailing zero-file iterations
    zero_files = 0
    for e in reversed(window):
        if e.get("patch_or_file") == "none":
            zero_files += 1
        else:
            break
    if zero_files >= 4:
        emit(
            True,
            "no_file_blocks",
            "4+ iterations with zero FILE/PATCH blocks — read LAST_REPLY.md; "
            "shrink the story to EXACTLY ONE file and re-state the block format "
            "in the story text",
        )
        return 0

    # (c) verify_ok alternating pass/fail for 3+ cycles at the tail
    seq = [bool(e["verify_ok"]) for e in window if e.get("verify_ok") is not None]
    if len(seq) >= 6 and all(seq[-i] != seq[-i - 1] for i in range(1, 6)):
        emit(
            True,
            "verify_oscillation",
            "pass/fail alternating 3+ cycles — fixing A breaks B: add a "
            "regressionVerify (or protect the sibling file) so the two stories "
            "stop fighting",
        )
        return 0

    # (d) same story failing 3+ times with identical verify output
    streak = 0
    last_key = None
    for e in reversed(window):
        if e.get("verify_ok") is not False:
            break
        key = (e.get("story_id"), e.get("verify_hash"))
        if e.get("verify_hash") is None:
            break
        if last_key is None or key == last_key:
            streak += 1
            last_key = key
        else:
            break
    if streak >= 3:
        emit(
            True,
            "repeated_failure",
            f"story {last_key[0]} failing with identical verify output {streak}x "
            "— paste the exact error into the story; if the architect two-pass "
            "already ran, curate (delete dead files, git restore clobbered work)",
        )
        return 0

    emit(False, None, "no rut pattern in the last %d events" % len(window))
    return 0


if __name__ == "__main__":
    sys.exit(main())
