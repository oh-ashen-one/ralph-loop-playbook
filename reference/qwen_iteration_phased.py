#!/usr/bin/env python3
"""One Ralph iteration against a local OpenAI-compatible model server.
Fresh context. Memory via prd/progress/git.
Phase-gated variant: only stories in the current PHASE file are eligible.

Exit codes (the supervisor routes on these):
  0  normal iteration done
  42 current phase complete (or all stories passed) — park until a human bumps PHASE
  43 no eligible story: everything remaining is blocked or dependency-starved
  44 repeated format failure (3+ consecutive iterations, zero FILE/PATCH blocks)
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import threading
import traceback
import time
from datetime import datetime, timezone
from pathlib import Path

FILE_RE = re.compile(
    r"###\s*FILE:\s*[`']?([^\s`']+)[`']?\s*\n```(?:[\w.+-]*)\n(.*?)```",
    re.S,
)
FILE_RE_ALT = re.compile(
    r"###\s*FILE:\s*[`']?([^\s`']+)[`']?\s*\n(.*?)(?=\n###\s*(?:FILE:|END FILE)|\Z)",
    re.S,
)

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent.parent  # repo root: prd/progress/QWEN/BRIEF live here
PRD_PATH = ROOT_DIR / "prd.json"
PROGRESS_PATH = ROOT_DIR / "progress.txt"
LAST_VERIFY = SCRIPT_DIR / "LAST_VERIFY.txt"
QWEN_MD = ROOT_DIR / "QWEN.md"
BRIEF_PATH = ROOT_DIR / "BRIEF.md"
PHASE_PATH = ROOT_DIR / "PHASE"
TRAJECTORY_PATH = SCRIPT_DIR / "trajectory.jsonl"
ALLOWED_FILES: set = set()
PROTECT: dict = {}

QWEN_SSH = os.environ.get("QWEN_SSH", "")  # loop runs ON the inference box
QWEN_API = os.environ.get("QWEN_API", "http://127.0.0.1:1234/v1/chat/completions")
QWEN_MODEL = os.environ.get("QWEN_MODEL", "ralph-local")

# xhigh thinking on one story can exceed 30 minutes. That is NORMAL — budget
# for it. Killing a long think amputates the reply and looks like model stupidity.
CHAT_TIMEOUT_S = 5400

BLOCK_AFTER = 5  # consecutive failures on one story -> blocked:true, move on
TWOPASS_AFTER = 3  # consecutive failures -> architect two-pass (plan, then emit)
FORMAT_FAIL_EXIT = 3  # consecutive zero-block iterations -> exit 44

# Output markers that mean FAIL even when the verify command exits 0.
# Godot exits 0 on script parse errors, GUT exits 0 with failing tests and
# silently skips unparseable test files — never trust the exit code alone.
VERIFY_FAIL_MARKERS = re.compile(
    r"SCRIPT ERROR|Parse Error|Failed to load script|Failed loading resource"
    r"|[1-9][0-9]* failing tests"
)

SKIP_DIR_NAMES = {
    ".git",
    "node_modules",
    ".next",
    "dist",
    "build",
    "DerivedData",
    "archive",
    ".turbo",
    "coverage",
    "__pycache__",
    ".godot",
    "shots",
    "assets",   # manager-staged binaries: never model-written, never snapshotted
    "addons",   # vendored addons: read via docs, not snapshot
}
SKIP_COMMIT_PATHS = [
    "node_modules",
    ".next",
    "DerivedData",
    "dist",
    "build",
    "coverage",
    "__pycache__",
    "scripts/ralph/__pycache__",
    "scripts/ralph/LAST_REPLY.md",
    "scripts/ralph/LAST_THINKING.md",
    "scripts/ralph/LAST_VERIFY.txt",
    "scripts/ralph/LAST_PLAN.md",
    "scripts/ralph/trajectory.jsonl",
]
SOURCE_SUFFIXES = {
    ".gd",
    ".gdshader",
    ".tscn",
    ".tres",
    ".json",
    ".md",
    ".cfg",
}


def repo_root() -> Path:
    out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True)
    return Path(out.strip())


def load_prd() -> dict:
    return json.loads(PRD_PATH.read_text())


def current_phase() -> str:
    try:
        return PHASE_PATH.read_text().strip()
    except OSError:
        return "0"


def next_story(prd: dict) -> dict | None:
    """Lowest-priority eligible story in the CURRENT phase only (checkpoint
    gating). Eligible = unpassed, not blocked, blockedBy ids all pass."""
    phase = current_phase()
    stories = prd.get("userStories", [])
    passed = {s.get("id") for s in stories if s.get("passes")}
    eligible = [
        s
        for s in stories
        if not s.get("passes")
        and str(s.get("phase", "0")) == phase
        and not s.get("blocked")
        and all(b in passed for b in s.get("blockedBy") or [])
    ]
    if not eligible:
        return None
    return sorted(eligible, key=lambda s: s.get("priority", 999))[0]


def phase_complete(prd: dict) -> bool:
    """True when every story in the current phase passes but later phases remain."""
    phase = current_phase()
    stories = [
        s for s in prd.get("userStories", []) if str(s.get("phase", "0")) == phase
    ]
    return bool(stories) and all(s.get("passes") for s in stories) and not all_passed(prd)


def all_passed(prd: dict) -> bool:
    stories = prd.get("userStories") or []
    return bool(stories) and all(s.get("passes") for s in stories)


def load_trajectory() -> list[dict]:
    if not TRAJECTORY_PATH.exists():
        return []
    events: list[dict] = []
    for line in TRAJECTORY_PATH.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


def norm_hash(text: str) -> str | None:
    norm = re.sub(r"\s+", " ", text).strip()
    if not norm:
        return None
    return hashlib.sha1(norm.encode()).hexdigest()


def consecutive_failures(story_id: str) -> int:
    """Trailing verify_ok==False events for this story in the trajectory.
    Infra crashes (verify_ok null) break the streak — they are not model failures."""
    n = 0
    for ev in reversed(load_trajectory()):
        if ev.get("story_id") != story_id:
            continue
        if ev.get("verify_ok") is False:
            n += 1
        else:
            break
    return n


def format_failure_streak(events: list[dict]) -> int:
    n = 0
    for ev in reversed(events):
        if ev.get("patch_or_file") == "none":
            n += 1
        else:
            break
    return n


def mark_blocked(story_id: str) -> None:
    """5 consecutive failures: the loop cannot pass this story. Flag it, record
    the verify tail for the human, and move on to the next eligible story."""
    fresh = load_prd()
    tail = LAST_VERIFY.read_text(errors="replace")[-500:] if LAST_VERIFY.exists() else ""
    for s in fresh.get("userStories") or []:
        if s.get("id") == story_id:
            s["blocked"] = True
            s["blocked_reason"] = tail
    PRD_PATH.write_text(json.dumps(fresh, indent=2) + "\n")
    print(f"  story {story_id} BLOCKED after {BLOCK_AFTER} consecutive failures", flush=True)


def _consume_sse(stream, content_parts: list[str], think_parts: list[str]) -> None:
    n = 0
    for raw_line in stream:
        line = raw_line.decode("utf-8", errors="replace").strip()
        if not line.startswith("data:"):
            continue
        data = line[5:].strip()
        if data == "[DONE]":
            break
        try:
            chunk = json.loads(data)
        except json.JSONDecodeError:
            continue
        choices = chunk.get("choices") or [{}]
        delta = (choices[0] or {}).get("delta") or {}
        if delta.get("content"):
            content_parts.append(delta["content"])
        if delta.get("reasoning_content"):
            think_parts.append(delta["reasoning_content"])
        n += 1
        if n % 25 == 0:
            # Observability only — files are written once, after the stream
            # completes. Mid-stream writes land half-generated files on disk.
            (SCRIPT_DIR / "LAST_REPLY.md").write_text("".join(content_parts))
            (SCRIPT_DIR / "LAST_THINKING.md").write_text("".join(think_parts))


def chat(user: str) -> tuple[str, str]:
    """One chat completion. Returns (visible_reply, thinking).
    Thinking ON (xhigh) per the max-power defaults: thinking off = garbage
    (the 2026-08 three-day bug). No assistant prefill. Reasoning streams into
    reasoning_content; visible content carries the ### FILE/PATCH blocks."""
    payload = {
        "model": QWEN_MODEL,
        "messages": [
            {"role": "system", "content": QWEN_MD.read_text()},
            {"role": "user", "content": user},
        ],
        "temperature": 1.0,
        "top_p": 0.95,
        "top_k": 20,
        "max_tokens": 65536,
        "stream": True,
        "enable_thinking": True,
        "reasoning_effort": "xhigh",
        "chat_template_kwargs": {
            "enable_thinking": True,
            "preserve_thinking": True,
        },
    }
    body = json.dumps(payload)
    content_parts: list[str] = []
    think_parts: list[str] = []
    if QWEN_SSH:
        remote = (
            f"curl -sS -N -m {CHAT_TIMEOUT_S} {QWEN_API} "
            f"-H 'Content-Type: application/json' -d @-"
        )
        proc = subprocess.Popen(
            ["ssh", QWEN_SSH, remote],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
        assert proc.stdin and proc.stdout

        def _kill() -> None:
            try:
                os.killpg(proc.pid, 9)
            except OSError:
                proc.kill()

        timer = threading.Timer(CHAT_TIMEOUT_S + 10, _kill)
        timer.daemon = True
        timer.start()
        try:
            proc.stdin.write(body.encode())
            proc.stdin.close()
            _consume_sse(proc.stdout, content_parts, think_parts)
            proc.wait(timeout=20)
        except Exception:
            _kill()
            raise
        finally:
            timer.cancel()
            if proc.poll() is None:
                _kill()
    else:
        import urllib.request

        req = urllib.request.Request(
            QWEN_API,
            data=body.encode(),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=CHAT_TIMEOUT_S) as resp:
            _consume_sse(resp, content_parts, think_parts)
    content = "".join(content_parts)
    think = "".join(think_parts)
    (SCRIPT_DIR / "LAST_REPLY.md").write_text(content)
    if think:
        (SCRIPT_DIR / "LAST_THINKING.md").write_text(think)
    # If LMS still hid the files in reasoning, take them from there.
    if not has_file_blocks(content) and think and has_file_blocks(think):
        content = think
    return content, think


def architect_two_pass(user: str, fails: int) -> tuple[str, str]:
    """Story has failed 3+ times in a row: separate diagnosis from emission.
    Call A produces a plan only (no FILE/PATCH blocks, short). Call B gets the
    plan prepended to the normal prompt and must emit only blocks."""
    print(f"  architect two-pass ({fails} consecutive failures)", flush=True)
    plan_prompt = (
        user
        + f"\n\nARCHITECT PASS — this story has failed {fails} consecutive times. "
        "Do NOT emit ### FILE or ### PATCH blocks. Diagnose the root cause from "
        "LAST_VERIFY.TXT and reply with a short numbered fix plan: exact file, "
        "exact symbol/line, exact change. Under 40 lines.\n"
    )
    plan, think_a = chat(plan_prompt)
    (SCRIPT_DIR / "LAST_PLAN.md").write_text(plan)
    build_prompt = (
        "ARCHITECT PLAN (follow it exactly):\n"
        + plan
        + "\n\n"
        + user
        + "\n\nEmit ONLY ### FILE / ### PATCH blocks implementing the plan. "
        "No prose, no restating the plan.\n"
    )
    reply, think_b = chat(build_prompt)
    return reply, think_a + "\n" + think_b


def has_file_blocks(text: str) -> bool:
    return bool(text and re.search(r"###\s*(?:FILE|PATCH):\s*\S+", text))


def safe_rel(path: str) -> str | None:
    rel = path.strip().strip("`").strip("'").strip('"')
    if rel.startswith("./"):
        rel = rel[2:]
    # Only slashes — never lstrip(".") or the set "./" (that turns .gitignore into gitignore).
    rel = rel.lstrip("/")
    if rel == "gitignore":
        rel = ".gitignore"
    if not rel or rel in {"path", "relative/path", "relative/path.ext", "relative/path.tsx"}:
        return None
    parts = Path(rel).parts
    # FAILURES #63 (resolved): rel like "." survives the `not rel` check but
    # yields parts == () — parts[0] then IndexErrors and kills the iteration.
    if not parts or ".." in parts:
        return None
    if parts[0] in SKIP_DIR_NAMES:
        return None
    # Write fence: the model may ONLY write inside game/, and never into
    # manager-staged game/assets/ or vendored game/addons/.
    if parts[0] != "game":
        print(f"  skip {rel}: outside game/ write fence", flush=True)
        return None
    if len(parts) > 1 and parts[1] in {"assets", "addons"}:
        print(f"  skip {rel}: protected harness/asset path", flush=True)
        return None
    return rel


HEADER_RE = re.compile(r"###\s*FILE:\s*[`']?([^\s`']+)[`']?[^\n]*\n")
MARKER_LINE_RE = re.compile(r"(?m)^###\s*(?:END FILE|FILE:)\b")
PLANNING_HEAD = re.compile(
    r"^(Complete file\.?|Copy existing|Full rewrite|Let me |I'll |I will |Now let |Wait[, ]|Hmm[, ])",
    re.I,
)


def _looks_like_planning(body: str) -> bool:
    head = body.lstrip()
    if PLANNING_HEAD.match(head) or head.startswith("### "):
        return True
    return False


def _clean_file_body(body: str) -> str:
    body = body.replace("\r\n", "\n")
    body = re.sub(r"^```[\w.+-]*\n", "", body)
    # Headers win: never let a missing closer swallow the next file.
    body = re.split(r"\n###\s*(?:END FILE|FILE:)\b", body, maxsplit=1)[0]
    body = re.sub(r"(?m)^###\s*(?:END FILE|FILE:).*\n?", "", body)
    body = re.sub(r"\n```[ \t]*\Z", "\n", body)
    return body if body.endswith("\n") else body + "\n"


def parse_file_blocks(text: str) -> list[tuple[str, str]]:
    """Split on ### FILE: headers. A forgotten ``` must not eat the next file."""
    matches = list(HEADER_RE.finditer(text))
    pairs: list[tuple[str, str]] = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        pairs.append((m.group(1), text[m.end() : end]))
    return pairs


def strip_leaked_markers(root: Path) -> list[str]:
    """Truncate any source file that still contains Ralph ### FILE / END FILE lines."""
    cleaned: list[str] = []
    for p in root.rglob("*"):
        rel_parts = p.relative_to(root).parts
        if any(part in SKIP_DIR_NAMES or part == "scripts" for part in rel_parts):
            continue
        if not p.is_file() or p.suffix.lower() not in SOURCE_SUFFIXES:
            continue
        text = p.read_text(errors="replace")
        hit = MARKER_LINE_RE.search(text)
        if not hit:
            continue
        p.write_text(text[: hit.start()].rstrip() + "\n")
        cleaned.append(p.relative_to(root).as_posix())
        print(f"  stripped Ralph markers from {cleaned[-1]}", flush=True)
    return cleaned


def _block_complete(raw: str) -> bool:
    return bool(re.search(r"###\s*END FILE", raw) or re.search(r"\n```[ \t]*\Z", raw.strip()))


PATCH_RE = re.compile(
    r"###\s*PATCH:\s*[`']?([^\s`']+)[`']?[^\n]*\n(?:```[\w.+-]*\n)?<{4,}\n(.*?)\n={4,}\n(.*?)\n>{4,}",
    re.S,
)


def apply_patches(text: str, dest: Path) -> list[str]:
    """### PATCH: path / <<<< old / ==== new / >>>> — exact-match replace.
    Lets a story fix one line in a 400-line file without re-emitting it
    (whole-file emission truncates past ~180 lines)."""
    patched: list[str] = []
    for path, old, new in PATCH_RE.findall(text):
        rel = safe_rel(path)
        if not rel:
            continue
        if rel.startswith(("tools/", "scripts/")):
            print(f"  skip patch {rel}: harness path is write-protected", flush=True)
            continue
        if ALLOWED_FILES and rel not in ALLOWED_FILES:
            print(f"  skip patch {rel}: not in story allowedFiles", flush=True)
            continue
        fp = dest / rel
        if not fp.is_file():
            print(f"  skip patch {rel}: no such file", flush=True)
            continue
        src = fp.read_text(errors="replace")
        if old not in src:
            print(f"  skip patch {rel}: search text not found ({len(old)}B)", flush=True)
            continue
        if src.count(old) > 1:
            print(f"  skip patch {rel}: search text matches {src.count(old)}x, not unique", flush=True)
            continue
        result = src.replace(old, new, 1)
        req = PROTECT.get(rel)
        if req:
            missing = [m for m in req if m not in result]
            if missing:
                print(f"  skip patch {rel}: result drops protected symbols {missing}", flush=True)
                continue
        fp.write_text(result)
        patched.append(rel)
        print(f"  patched {rel} ({len(old)}B -> {len(new)}B)", flush=True)
    return patched


def write_files(text: str, dest: Path) -> list[str]:
    written: list[str] = []
    pairs = parse_file_blocks(text)
    if not pairs:
        pairs = list(FILE_RE.findall(text)) or list(FILE_RE_ALT.findall(text))
    last_idx = len(pairs) - 1
    for i, (path, content) in enumerate(pairs):
        if i == last_idx and not _block_complete(content):
            print(f"  skip incomplete last file {path}", flush=True)
            continue
        rel = safe_rel(path)
        if not rel:
            continue
        if ALLOWED_FILES and rel not in ALLOWED_FILES:
            print(f"  skip {rel}: not in story allowedFiles", flush=True)
            continue
        req = PROTECT.get(rel)
        if req:
            missing = [m for m in req if m not in content]
            if missing:
                print(f"  skip {rel}: write drops protected symbols {missing}", flush=True)
                continue
        body = _clean_file_body(content)
        if not body.strip() or body.lstrip().startswith("### FILE:"):
            continue
        if _looks_like_planning(body):
            print(f"  skip {rel}: planning prose, not source", flush=True)
            continue
        if rel.endswith(".css") and body.count("{") != body.count("}"):
            print(f"  skip unbalanced css {rel}", flush=True)
            continue
        fp = dest / rel
        if rel.endswith(".css") and fp.exists() and len(body) < int(fp.stat().st_size * 0.85):
            print(f"  skip shorter css {rel} ({len(body)} < {fp.stat().st_size})", flush=True)
            continue
        if rel.endswith("globals.css") and fp.exists():
            old = fp.read_text(errors="replace")
            if old.count("{") == old.count("}") and old.count("{") > 0:
                last = LAST_VERIFY.read_text() if LAST_VERIFY.exists() else ""
                css_broken = "globals.css" in last and any(
                    s in last for s in ("Unknown word", "PostCSSSyntaxError", "Syntax error:")
                )
                if not css_broken:
                    print(
                        f"  skip valid existing css {rel}: LAST_VERIFY is not a CSS syntax error",
                        flush=True,
                    )
                    continue
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(body)
        written.append(rel)
        print(f"  wrote {rel} ({len(body)} bytes)", flush=True)
    strip_leaked_markers(dest)
    return written


def run_verify(cmd: str, cwd: Path) -> tuple[bool, str]:
    print(f"  VERIFY: {cmd}", flush=True)
    env = os.environ.copy()
    env.setdefault("CI", "true")
    try:
        p = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=900,
            env=env,
        )
        out = (p.stdout or "") + (p.stderr or "")
        ok = p.returncode == 0
        # Godot/GUT exit 0 even on parse errors, skipped test files, and
        # failing tests — the exit code alone is NOT a gate (FAILURES #52).
        if ok and VERIFY_FAIL_MARKERS.search(out):
            out += ("\nVERIFY: exit code was 0 but failure markers found in "
                    "output — treating as FAIL.")
            ok = False
    except subprocess.TimeoutExpired as exc:
        out = (exc.stdout or "") + (exc.stderr or "") + "\nVERIFY timed out after 900s"
        ok = False
    print(out[-4000:] if len(out) > 4000 else out)
    return ok, out


def extract_verify_cmd(story: dict) -> str:
    cmd = str(story["verify"]) if story.get("verify") else "true"
    strip = "python3 scripts/ralph/strip_markers.py"
    if "strip_markers.py" not in cmd:
        return f"{strip} && {cmd}"
    return cmd


def live_story(story: dict) -> dict:
    """Re-read PRD so a watchdog can enrich verify while this process is in chat()."""
    try:
        fresh = load_prd()
    except Exception:
        return story
    for item in fresh.get("userStories") or []:
        if item.get("id") == story.get("id"):
            return item
    return story


def ensure_gitignore(root: Path) -> None:
    gi = root / ".gitignore"
    needed = [
        "node_modules/",
        ".next/",
        "dist/",
        "build/",
        "DerivedData/",
        ".DS_Store",
        "coverage/",
        "*.tsbuildinfo",
        "scripts/ralph/LAST_REPLY.md",
        "scripts/ralph/LAST_THINKING.md",
        "scripts/ralph/LAST_VERIFY.txt",
        "scripts/ralph/LAST_PLAN.md",
        "scripts/ralph/trajectory.jsonl",
        "__pycache__/",
        "*.pyc",
    ]
    existing = gi.read_text() if gi.exists() else ""
    missing = [line for line in needed if line not in existing]
    if missing:
        extra = ("\n" if existing and not existing.endswith("\n") else "") + "\n".join(missing) + "\n"
        gi.write_text(existing + extra)


def commit(root: Path, story: dict) -> None:
    ensure_gitignore(root)
    stray = root / "gitignore"
    if stray.exists() and (root / ".gitignore").exists():
        stray.unlink()
    subprocess.run(
        ["git", "rm", "-r", "--cached", "--ignore-unmatch", *SKIP_COMMIT_PATHS],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    subprocess.run(["git", "add", "-A"], cwd=root, check=False)
    subprocess.run(
        ["git", "reset", "-q", "--", *SKIP_COMMIT_PATHS],
        cwd=root,
        check=False,
    )
    msg = f"feat: [{story['id']}] {story['title']}"
    subprocess.run(["git", "commit", "-m", msg], cwd=root, check=False)


def append_progress(story: dict, written: list[str], verify_ok: bool, note: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    block = (
        f"\n## {ts} - {story['id']}\n"
        f"- verify_ok: {verify_ok}\n"
        f"- files: {', '.join(written) or '(none)'}\n"
        f"- {note}\n---\n"
    )
    with PROGRESS_PATH.open("a") as f:
        f.write(block)


def tree_snapshot(root: Path) -> str:
    lines: list[str] = []
    for p in sorted(root.rglob("*")):
        if any(part in SKIP_DIR_NAMES or part == "scripts" for part in p.relative_to(root).parts):
            continue
        if p.is_file():
            rel = p.relative_to(root).as_posix()
            lines.append(f"{rel} ({p.stat().st_size} bytes)")
    return "\n".join(lines[:200]) or "(empty project)"


def file_snapshot(root: Path) -> str:
    last = LAST_VERIFY.read_text() if LAST_VERIFY.exists() else ""
    files: list[Path] = []
    for p in sorted(root.rglob("*")):
        rel_parts = p.relative_to(root).parts
        if any(part in SKIP_DIR_NAMES or part == "scripts" for part in rel_parts):
            continue
        if not p.is_file() or p.suffix.lower() not in SOURCE_SUFFIXES:
            continue
        if p.name in {"package-lock.json", "pnpm-lock.yaml"}:
            continue
        files.append(p)
    # Files named in LAST_VERIFY first so a CSS/TS error is shown in full.
    def _prio(p: Path) -> tuple[int, str]:
        rel = p.relative_to(root).as_posix()
        if rel in ALLOWED_FILES:
            return (0, rel)  # story files always first, always in full
        return (1 if rel in last else 2, rel)

    chunks: list[str] = []
    total = 0
    omitted: list[str] = []
    for p in sorted(files, key=_prio):
        rel = p.relative_to(root).as_posix()
        if p.stat().st_size > 80_000:
            omitted.append(f"{rel} ({p.stat().st_size} bytes, too large)")
            continue
        text = p.read_text(errors="replace")
        if total + len(text) > 55_000:
            omitted.append(f"{rel} ({p.stat().st_size} bytes)")
            continue
        chunks.append(f"===== {rel} =====\n{text}")
        total += len(text)
    if omitted:
        chunks.append(
            "===== OMITTED (complete on disk — do not rewrite from memory) =====\n"
            + "\n".join(omitted)
        )
    return "\n\n".join(chunks) or "(no source files yet)"


def build_user_prompt(root: Path, story: dict, prd: dict) -> str:
    progress = PROGRESS_PATH.read_text() if PROGRESS_PATH.exists() else ""
    last = LAST_VERIFY.read_text() if LAST_VERIFY.exists() else "(none)"
    brief = BRIEF_PATH.read_text() if BRIEF_PATH.exists() else "(none)"
    verify = extract_verify_cmd(story)
    # Prefix pinning: static parts first (rules, brief, story), volatile tails
    # (progress, LAST_VERIFY) last — LM Studio's prompt cache hits on the prefix.
    return (
        "You are implementing ONE Ralph story. Emit complete ### FILE blocks — "
        "UNLESS the story mandates a ### PATCH block, in which case emit exactly that:\n"
        "### PATCH: relative/path\n<<<<\n(exact current text)\n====\n(replacement)\n>>>>\n"
        "If you emit neither FILE nor PATCH blocks the iteration is a hard fail.\n\n"
        f"PROJECT ROOT: {root}\n\n"
        f"CURRENT STORY:\n{json.dumps(story, indent=2)}\n\n"
        f"AUTHORITATIVE VERIFY (copy this exact line at the end):\nVERIFY: {verify}\n\n"
        f"PROJECT BRIEF:\n{brief}\n\n"
        f"FULL PRD:\n{json.dumps(prd, indent=2)}\n\n"
        f"PROJECT TREE:\n{tree_snapshot(root)}\n\n"
        f"EXISTING SOURCE (edit these; do not start over):\n{file_snapshot(root)}\n\n"
        f"PROGRESS.TXT (tail):\n{progress[-6000:]}\n\n"
        f"LAST_VERIFY.TXT:\n{last[-5000:]}\n\n"
        "Start your reply with ### FILE: (or ### PATCH: when the story mandates a patch).\n"
        "Close each ``` fence before ### END FILE. Never put ### FILE: or ### END FILE inside a file body.\n"
        "Do not rewrite a file unless this story or LAST_VERIFY requires it. Never emit a truncated CSS/TSX file.\n"
        "If a snapshot says OMITTED or you cannot finish a file, omit it — the on-disk copy stays.\n"
        "Do not draft ### FILE blocks in reasoning. Visible reply is the only write path.\n"
    )


def ping() -> int:
    """Prove endpoint + model mapping: expect a fast literal PONG."""
    reply, _ = chat("Reply with exactly: PONG. Nothing else.")
    print(reply.strip()[:200])
    return 0 if "PONG" in reply.upper() else 1


def _record_failure(story: dict) -> None:
    """Count this iteration against the story; block it at BLOCK_AFTER in a row."""
    if consecutive_failures(story["id"]) + 1 >= BLOCK_AFTER:
        mark_blocked(story["id"])


def _run(event: dict) -> int:
    root = repo_root()
    ensure_gitignore(root)
    prd = load_prd()
    if all_passed(prd):
        print("<promise>COMPLETE</promise>")
        return 42
    story = next_story(prd)
    if story is None:
        if phase_complete(prd):
            print(f"PHASE-COMPLETE phase={current_phase()}")
            return 42
        print(
            "no eligible story in current phase: blocked or dependency-starved",
            flush=True,
        )
        return 43
    global ALLOWED_FILES
    ALLOWED_FILES = set(story.get("allowedFiles") or [])
    global PROTECT
    PROTECT = story.get("protect") or {}
    event["story_id"] = story.get("id")

    user = build_user_prompt(root, story, prd)
    print(f"Story {story['id']}: {story['title']}", flush=True)
    fails = consecutive_failures(story["id"])
    try:
        if fails >= TWOPASS_AFTER:
            reply, think = architect_two_pass(user, fails)
        else:
            reply, think = chat(user)
    except Exception as exc:
        print(f"Qwen API failed: {exc}", flush=True)
        LAST_VERIFY.write_text(str(exc))
        return 1

    event["reply_bytes"] = len(reply.encode())
    event["think_bytes"] = len(think.encode())
    event["emission_hash"] = norm_hash(reply)
    (SCRIPT_DIR / "LAST_REPLY.md").write_text(reply)
    patched = apply_patches(reply, root)
    written = write_files(reply, root)
    if not patched and not written:
        print("  no FILE/PATCH blocks — retrying once with a stricter prompt", flush=True)
        try:
            retry, think2 = chat(
                user
                + "\n\nCRITICAL: your previous reply had ZERO ### FILE/PATCH blocks. "
                "Reply with ONLY the block format the story mandates.\n"
            )
            (SCRIPT_DIR / "LAST_REPLY.md").write_text(retry)
            patched = apply_patches(retry, root)
            written = write_files(retry, root)
            reply = retry
            event["reply_bytes"] = len(reply.encode())
            event["think_bytes"] += len(think2.encode())
            event["emission_hash"] = norm_hash(reply)
        except Exception as exc:
            print(f"Qwen retry failed: {exc}", flush=True)

    event["files_written"] = patched + written
    if patched and written:
        event["patch_or_file"] = "patch+file"
    elif patched:
        event["patch_or_file"] = "patch"
    elif written:
        event["patch_or_file"] = "file"

    if not patched and not written:
        LAST_VERIFY.write_text("no ### FILE/PATCH blocks in model output\n" + reply[-2000:])
        append_progress(story, [], False, "no files emitted")
        event["verify_ok"] = False
        _record_failure(story)
        return 0

    cmd = extract_verify_cmd(live_story(story))
    ok, out = run_verify(cmd, root)
    if ok and prd.get("regressionVerify"):
        # Story gate is green; the whole project must stay green too before
        # the pass is banked and committed.
        rok, rout = run_verify(str(prd["regressionVerify"]), root)
        if not rok:
            ok = False
            out = "STORY VERIFY PASSED but regressionVerify FAILED:\n" + rout
    LAST_VERIFY.write_text(out[-12000:])
    event["verify_ok"] = ok
    event["verify_hash"] = norm_hash(out[-2000:])
    if ok:
        fresh = load_prd()
        for s in fresh["userStories"]:
            if s["id"] == story["id"]:
                s["passes"] = True
        PRD_PATH.write_text(json.dumps(fresh, indent=2) + "\n")
        commit(root, story)
        append_progress(story, event["files_written"], True, "checks passed")
        if all_passed(fresh):
            print("<promise>COMPLETE</promise>")
    else:
        append_progress(
            story,
            event["files_written"],
            False,
            "checks FAILED — next iteration must fix LAST_VERIFY.txt",
        )
        _record_failure(story)
    return 0


def main() -> int:
    if "--ping" in sys.argv:
        return ping()
    t0 = time.time()
    events = load_trajectory()
    event: dict = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "story_id": None,
        "iteration": len(events) + 1,
        "files_written": [],
        "patch_or_file": "none",
        "verify_ok": None,
        "exit_status": 1,
        "duration_s": 0.0,
        "reply_bytes": 0,
        "think_bytes": 0,
        "emission_hash": None,
        "verify_hash": None,
    }
    code = 1
    try:
        code = _run(event)
    except Exception as exc:
        print(f"iteration crashed: {exc}", flush=True)
        traceback.print_exc()
        code = 1
    finally:
        # The trajectory is the postmortem record — log even on crash.
        event["exit_status"] = code
        event["duration_s"] = round(time.time() - t0, 1)
        try:
            with TRAJECTORY_PATH.open("a") as f:
                f.write(json.dumps(event) + "\n")
        except OSError as exc:
            print(f"trajectory write failed: {exc}", flush=True)
    if code == 0 and format_failure_streak(events + [event]) >= FORMAT_FAIL_EXIT:
        print(
            f"{FORMAT_FAIL_EXIT}+ consecutive iterations with zero FILE/PATCH blocks",
            flush=True,
        )
        return 44
    return code


if __name__ == "__main__":
    sys.exit(main())
