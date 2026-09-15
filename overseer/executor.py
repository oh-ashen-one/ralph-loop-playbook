#!/usr/bin/env python3
"""executor.py <project_root> [--dry-run] — validate manager actions against the
caps and apply them. Reads a JSON array on stdin. Never authors code."""
import json, subprocess, sys, time, os

ROOT = sys.argv[1]
DRY = "--dry-run" in sys.argv
NAME = os.path.basename(ROOT.rstrip("/"))
RALPH = os.path.join(ROOT, "scripts", "ralph")
PRD = os.path.join(RALPH, "prd.json")
LOG = os.path.expanduser(os.environ.get("RALPH_MANAGER_LOG", "~/ralph-overseer/overseer-log.jsonl"))
MAX_INTERVENTIONS = 2

def sh(cmd, **kw):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, **kw)

def log(entry):
    entry["ts"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    entry["project"] = NAME
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

def page(reason):
    """Page the human through a pluggable hook. RALPH_MANAGER_PAGER is any
    executable that takes the message as its single argument (chat webhook,
    push service, email CLI...). Unset: the page goes to stdout and the log."""
    msg = f"[ralph-overseer] {NAME}: {reason}"
    pager = os.environ.get("RALPH_MANAGER_PAGER", "")
    if DRY or not pager:
        print(f"{'DRY: ' if DRY else ''}page_human: {msg}")
    else:
        subprocess.run([pager, msg], capture_output=True, text=True)
    log({"type": "page_human", "reason": reason})

def load_prd():
    with open(PRD) as f:
        return json.load(f)

def save_prd(prd):
    tmp = PRD + ".tmp"
    with open(tmp, "w") as f:
        json.dump(prd, f, indent=2)
    os.replace(tmp, PRD)

def interventions(prd, sid):
    for s in prd.get("userStories", []):
        if s.get("id") == sid:
            return s, s.get("managerInterventions", 0)
    return None, None

def main():
    try:
        actions = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        log({"type": "rejected", "reason": f"manager emitted non-JSON: {e}"})
        page("manager reply was not valid JSON; no actions applied")
        return
    if not isinstance(actions, list):
        log({"type": "rejected", "reason": "manager reply not a JSON array"})
        return
    if not actions:
        log({"type": "checkin", "verdict": "healthy"})
        print("no actions (healthy)")
        return

    for a in actions:
        if not isinstance(a, dict) or "action" not in a:
            log({"type": "rejected", "action": a})
            continue
        act = a["action"]

        if act == "page_human":
            page(a.get("reason", "no reason given"))

        elif act in ("edit_story", "unblock"):
            sid = a.get("id", "")
            prd = load_prd()
            story, n = interventions(prd, sid)
            if story is None:
                log({"type": "rejected", "action": a, "reason": "no such story"})
                continue
            if n >= MAX_INTERVENTIONS:
                page(f"story {sid} hit the {MAX_INTERVENTIONS}-intervention cap — needs restructure, refusing to nurse")
                log({"type": "cap_refusal", "action": a})
                continue
            if act == "edit_story":
                app = a.get("append", "").strip()
                if not app:
                    log({"type": "rejected", "action": a, "reason": "empty append"})
                    continue
                story["description"] = story.get("description", "") + "\n\nMANAGER: " + app
            else:
                story["blocked"] = False
                story["blocked_reason"] = ""
            story["managerInterventions"] = n + 1
            if not DRY:
                save_prd(prd)
            log({"type": act, "id": sid, "detail": a, "dry": DRY})
            print(f"{'DRY: ' if DRY else ''}applied {act} on {sid} (intervention {n+1}/{MAX_INTERVENTIONS})")

        elif act == "kill_iteration":
            loops = sh(f"pgrep -f 'run_loop.sh {NAME}'").stdout.strip()
            iters = sh("pgrep -f qwen_iteration.py").stdout.strip().splitlines()
            if not loops:
                log({"type": "rejected", "action": a, "reason": "no run_loop for this project"})
            elif len([p for p in iters if p]) != 1:
                page(f"kill_iteration requested but {len(iters)} qwen_iteration processes box-wide — refusing to guess")
                log({"type": "rejected", "action": a, "reason": "ambiguous iteration count"})
            else:
                if not DRY:
                    sh("pkill -TERM -f qwen_iteration.py")
                log({"type": "kill_iteration", "dry": DRY})
                print(f"{'DRY: ' if DRY else ''}killed in-flight iteration (supervisor respawns)")

        elif act == "relaunch_loop":
            alive = sh(f"pgrep -f 'run_loop.sh {NAME}'").stdout.strip()
            if alive:
                log({"type": "rejected", "action": a, "reason": "loop already alive"})
            else:
                cmd = (f'cd {ROOT} && QWEN_SSH="" nohup caffeinate -s bash '
                       f'scripts/ralph/run_loop.sh {NAME} 200 >> /tmp/ralph-{NAME}.log 2>&1 &')
                if not DRY:
                    sh(cmd)
                log({"type": "relaunch_loop", "dry": DRY})
                print(f"{'DRY: ' if DRY else ''}relaunched loop for {NAME}")

        else:
            log({"type": "rejected", "action": a, "reason": "unknown action"})

if __name__ == "__main__":
    main()
