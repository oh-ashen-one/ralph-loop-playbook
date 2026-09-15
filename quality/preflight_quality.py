#!/usr/bin/env python3
"""Hard pre-launch gate for Ralph game quality contracts.

This validates the manager-owned production plan before Qwen receives a story.
It deliberately checks structure and evidence contracts, not whether the game
already looks good. Runtime verifies and the mandatory critique phase judge the
implementation later.

Usage:
    python3 scripts/ralph/quality/preflight_quality.py --root <project-root>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_EVIDENCE_IDS = {
    "title",
    "traversal",
    "primary-action",
    "failure",
    "mobile",
    "worst-performance",
}
REQUIRED_ACTION_CHANNELS = {"state", "motion", "visual", "audio", "hud"}
REQUIRED_STORY_CLASSES = {
    "vertical-slice",
    "look-lock",
    "asset-integration",
    "feedback-atom",
    "camera-input",
    "performance-resilience",
    "critique-ship",
}
STORY_CLASS_PHASES = {
    "vertical-slice": 1,
    "look-lock": 2,
    "asset-integration": 3,
    "feedback-atom": 4,
    "camera-input": 5,
    "performance-resilience": 6,
    "critique-ship": 7,
}
THREE_D_CATEGORIES = {"character", "environment", "model", "prop", "vehicle"}
AXES = {"+X", "-X", "+Y", "-Y", "+Z", "-Z", "none"}
ROOT_MOTION_POLICIES = {
    "none",
    "in-place",
    "consume",
    "cancel-horizontal",
    "cancel-all",
}
# NOTE: the angle-bracket form must match placeholders like <name> / <path>,
# NOT ordinary prose containing comparisons ("z_index < 0 ... (r+g > 1.2)").
# Requiring a letter/underscore/slash immediately after "<" and no spaces keeps
# real specs legal — a bare `<[^>]+>` rejected every description that used two
# comparison operators (FAILURES #78).
PLACEHOLDER_RE = re.compile(
    r"(?:FILL_ME|\bTBD\b|\bTODO\b|\bREPLACE_ME\b|\(path\)|\(url\)|<[A-Za-z_/][^<>\s]*>)",
    re.IGNORECASE,
)
FILE_PLACEHOLDER_RE = re.compile(
    r"(?:FILL_ME|\bTBD\b|\bTODO\b|\bREPLACE_ME\b|\(path\)|\(url\))",
    re.IGNORECASE,
)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def read_json(path: Path, errors: list[str]) -> Any:
    if not path.is_file():
        errors.append(f"missing {path}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot parse {path}: {exc}")
        return None


def is_filled_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and not PLACEHOLDER_RE.search(value)


def require_text(owner: dict[str, Any], key: str, label: str, errors: list[str]) -> str | None:
    value = owner.get(key)
    if not is_filled_text(value):
        errors.append(f"{label}.{key} must be specific and contain no placeholder text")
        return None
    return str(value)


def require_string_list(
    owner: dict[str, Any], key: str, label: str, errors: list[str], minimum: int = 1
) -> list[str]:
    value = owner.get(key)
    if not isinstance(value, list) or len(value) < minimum:
        errors.append(f"{label}.{key} must contain at least {minimum} item(s)")
        return []
    result: list[str] = []
    for index, item in enumerate(value):
        if not is_filled_text(item):
            errors.append(f"{label}.{key}[{index}] is empty or placeholder text")
        else:
            result.append(str(item))
    return result


def safe_project_path(root: Path, raw: Any, label: str, errors: list[str]) -> Path | None:
    if not is_filled_text(raw):
        errors.append(f"{label} must be a filled project-relative path")
        return None
    rel = Path(str(raw))
    if rel.is_absolute() or ".." in rel.parts:
        errors.append(f"{label} must stay inside the project: {raw}")
        return None
    resolved = (root / rel).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        errors.append(f"{label} escapes the project: {raw}")
        return None
    return resolved


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_reference_contract(root: Path, contract: dict[str, Any], errors: list[str]) -> None:
    references = contract.get("referenceContract")
    if not isinstance(references, list) or not references:
        errors.append("contract.referenceContract must contain at least one decomposed reference")
        return
    seen: set[str] = set()
    for index, reference in enumerate(references):
        label = f"contract.referenceContract[{index}]"
        if not isinstance(reference, dict):
            errors.append(f"{label} must be an object")
            continue
        ref_id = require_text(reference, "id", label, errors)
        if ref_id:
            if ref_id in seen:
                errors.append(f"duplicate reference id: {ref_id}")
            seen.add(ref_id)
        require_text(reference, "source", label, errors)
        local = safe_project_path(root, reference.get("localPath"), f"{label}.localPath", errors)
        expected_hash = reference.get("sha256")
        if not isinstance(expected_hash, str) or not SHA256_RE.fullmatch(expected_hash):
            errors.append(f"{label}.sha256 must pin the local reference with lowercase SHA-256")
        if local:
            if not local.is_file():
                errors.append(f"{label}.localPath does not exist: {local}")
            elif isinstance(expected_hash, str) and SHA256_RE.fullmatch(expected_hash):
                actual_hash = file_sha256(local)
                if actual_hash != expected_hash:
                    errors.append(f"{label}.sha256 mismatch: expected {expected_hash}, got {actual_hash}")
        require_string_list(reference, "learn", label, errors)
        require_string_list(reference, "mustNotCopy", label, errors)
        evidence_id = require_text(reference, "evidenceId", label, errors)
        if evidence_id and evidence_id not in REQUIRED_EVIDENCE_IDS:
            errors.append(f"{label}.evidenceId must name a canonical evidence id")


def validate_action_beats(contract: dict[str, Any], errors: list[str]) -> set[str]:
    beats = contract.get("actionBeats")
    if not isinstance(beats, list) or not beats:
        errors.append("contract.actionBeats must contain at least one complete feedback atom")
        return set()
    ids: set[str] = set()
    for index, beat in enumerate(beats):
        label = f"contract.actionBeats[{index}]"
        if not isinstance(beat, dict):
            errors.append(f"{label} must be an object")
            continue
        beat_id = require_text(beat, "id", label, errors)
        if beat_id:
            if beat_id in ids:
                errors.append(f"duplicate action beat id: {beat_id}")
            ids.add(beat_id)
        require_text(beat, "stateResult", label, errors)
        timeline = beat.get("timelineMs")
        if not isinstance(timeline, dict):
            errors.append(f"{label}.timelineMs must name anticipation/contact/response/settle")
        else:
            values: list[float] = []
            for phase in ("anticipation", "contact", "response", "settle"):
                value = timeline.get(phase)
                if not isinstance(value, (int, float)) or value < 0:
                    errors.append(f"{label}.timelineMs.{phase} must be a non-negative number")
                else:
                    values.append(float(value))
            if values and sum(values) <= 0:
                errors.append(f"{label}.timelineMs cannot be all zero")
        channels = set(require_string_list(beat, "channels", label, errors))
        missing = REQUIRED_ACTION_CHANNELS - channels
        if missing:
            errors.append(f"{label}.channels missing {sorted(missing)}")
        require_string_list(beat, "evidenceIds", label, errors)
    return ids


def validate_evidence(contract: dict[str, Any], errors: list[str]) -> set[str]:
    evidence = contract.get("canonicalEvidence")
    if not isinstance(evidence, list):
        errors.append("contract.canonicalEvidence must be a list")
        return set()
    ids: set[str] = set()
    for index, item in enumerate(evidence):
        label = f"contract.canonicalEvidence[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label} must be an object")
            continue
        evidence_id = require_text(item, "id", label, errors)
        if evidence_id:
            if evidence_id in ids:
                errors.append(f"duplicate canonical evidence id: {evidence_id}")
            ids.add(evidence_id)
        if not isinstance(item.get("seed"), int):
            errors.append(f"{label}.seed must be an integer")
        require_text(item, "state", label, errors)
        require_text(item, "camera", label, errors)
        viewport = item.get("viewport")
        if (
            not isinstance(viewport, list)
            or len(viewport) != 2
            or any(not isinstance(v, int) or v <= 0 for v in viewport)
        ):
            errors.append(f"{label}.viewport must be [positive width, positive height]")
        require_string_list(item, "assertions", label, errors)
    missing = REQUIRED_EVIDENCE_IDS - ids
    if missing:
        errors.append(f"contract.canonicalEvidence missing required ids: {sorted(missing)}")
    return ids


def validate_performance(contract: dict[str, Any], errors: list[str]) -> set[str]:
    tiers = contract.get("performanceTiers")
    if not isinstance(tiers, list) or not tiers:
        errors.append("contract.performanceTiers must contain a measured target tier")
        return set()
    ids: set[str] = set()
    numeric_budgets = (
        "durationSeconds",
        "maxP95FrameMs",
        "maxDrawCalls",
        "maxActiveObjects",
        "maxParticles",
        "maxPixelRatio",
        "maxConcurrentAssetLoads",
        "maxResidentAssetMB",
    )
    for index, tier in enumerate(tiers):
        label = f"contract.performanceTiers[{index}]"
        if not isinstance(tier, dict):
            errors.append(f"{label} must be an object")
            continue
        tier_id = require_text(tier, "id", label, errors)
        if tier_id:
            if tier_id in ids:
                errors.append(f"duplicate performance tier id: {tier_id}")
            ids.add(tier_id)
        require_text(tier, "device", label, errors)
        require_text(tier, "worstScene", label, errors)
        for key in numeric_budgets:
            value = tier.get(key)
            if not isinstance(value, (int, float)) or value <= 0:
                errors.append(f"{label}.{key} must be a positive number")
        require_string_list(tier, "preserve", label, errors)
        require_string_list(tier, "degradeOrder", label, errors)
        pools = tier.get("poolBudgets")
        if not isinstance(pools, dict) or not pools:
            errors.append(f"{label}.poolBudgets must name repeated-object capacity")
        else:
            for pool_name, capacity in pools.items():
                if not is_filled_text(pool_name) or not isinstance(capacity, int) or capacity <= 0:
                    errors.append(f"{label}.poolBudgets entries need a name and positive integer")
    return ids


def validate_input_matrix(root: Path, contract: dict[str, Any], errors: list[str]) -> None:
    matrix = contract.get("inputMatrix")
    if not isinstance(matrix, list) or not matrix:
        errors.append("contract.inputMatrix must cover at least one real input target")
        return
    for index, target in enumerate(matrix):
        label = f"contract.inputMatrix[{index}]"
        if not isinstance(target, dict):
            errors.append(f"{label} must be an object")
            continue
        require_text(target, "device", label, errors)
        require_text(target, "input", label, errors)
        require_text(target, "firstAction", label, errors)
        viewport = target.get("viewport")
        if (
            not isinstance(viewport, list)
            or len(viewport) != 2
            or any(not isinstance(v, int) or v <= 0 for v in viewport)
        ):
            errors.append(f"{label}.viewport must be [positive width, positive height]")
        min_target = target.get("minTargetPx")
        if not isinstance(min_target, (int, float)) or min_target <= 0:
            errors.append(f"{label}.minTargetPx must be positive")
        probe = safe_project_path(root, target.get("probe"), f"{label}.probe", errors)
        if probe and not probe.is_file():
            errors.append(f"{label}.probe does not exist: {probe}")


def validate_contract(root: Path, contract: Any, errors: list[str]) -> dict[str, Any] | None:
    if not isinstance(contract, dict):
        errors.append("quality/contract.json must contain an object")
        return None
    require_text(contract, "projectName", "contract", errors)
    require_text(contract, "productFantasy", "contract", errors)
    dimensions = contract.get("dimensions")
    if dimensions not in {"2d", "3d"}:
        errors.append("contract.dimensions must be '2d' or '3d'")
    phases = contract.get("requiredPhases")
    if phases != [1, 2, 3, 4, 5, 6, 7]:
        errors.append("contract.requiredPhases must be [1,2,3,4,5,6,7]")
    if contract.get("humanCheckpoints") != [2, 7]:
        errors.append("contract.humanCheckpoints must be [2,7] (look lock and ship proof)")
    required_classes = set(require_string_list(contract, "requiredStoryClasses", "contract", errors))
    if required_classes != REQUIRED_STORY_CLASSES:
        errors.append(
            "contract.requiredStoryClasses must contain exactly "
            f"{sorted(REQUIRED_STORY_CLASSES)}"
        )
    require_string_list(contract, "requiredAssetRoles", "contract", errors, minimum=3)
    require_string_list(contract, "requiredCharacterClipRoles", "contract", errors)
    require_text(contract, "assetManifest", "contract", errors)
    product_shell = contract.get("productShell")
    required_flows = {"boot", "menu", "play", "pause", "failure", "restart", "settings"}
    if not isinstance(product_shell, dict):
        errors.append("contract.productShell must define the complete player-facing flow")
    else:
        flows = set(require_string_list(product_shell, "coreFlows", "contract.productShell", errors))
        missing_flows = required_flows - flows
        if missing_flows:
            errors.append(f"contract.productShell.coreFlows missing {sorted(missing_flows)}")
        require_text(product_shell, "persistenceContract", "contract.productShell", errors)
        require_text(product_shell, "loadingFallback", "contract.productShell", errors)
        require_text(product_shell, "missingMediaFallback", "contract.productShell", errors)
    asset_io = contract.get("assetIo")
    if not isinstance(asset_io, dict):
        errors.append("contract.assetIo must bound loading, retries and shipping locality")
    else:
        for key in ("maxConcurrentLoads", "retryAttempts", "timeoutMs"):
            value = asset_io.get(key)
            if not isinstance(value, int) or value <= 0:
                errors.append(f"contract.assetIo.{key} must be a positive integer")
        require_text(asset_io, "backoffPolicy", "contract.assetIo", errors)
        if asset_io.get("localOnlyAtShip") is not True:
            errors.append("contract.assetIo.localOnlyAtShip must be true")
    shared = contract.get("sharedSimulation")
    if not isinstance(shared, list) or not shared:
        errors.append("contract.sharedSimulation must name rendering/gameplay truths that cannot drift")
    else:
        for index, item in enumerate(shared):
            label = f"contract.sharedSimulation[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{label} must be an object")
                continue
            require_text(item, "quantity", label, errors)
            require_text(item, "source", label, errors)
            require_string_list(item, "consumers", label, errors, minimum=2)
    validate_reference_contract(root, contract, errors)
    validate_action_beats(contract, errors)
    evidence_ids = validate_evidence(contract, errors)
    for index, beat in enumerate(contract.get("actionBeats", [])):
        if not isinstance(beat, dict):
            continue
        unknown = set(beat.get("evidenceIds", [])) - evidence_ids
        if unknown:
            errors.append(
                f"contract.actionBeats[{index}].evidenceIds references unknown evidence: {sorted(unknown)}"
            )
    validate_performance(contract, errors)
    validate_input_matrix(root, contract, errors)
    bridge = contract.get("debugBridge")
    required_capabilities = {
        "reset",
        "start",
        "stepOrSeek",
        "input",
        "setCamera",
        "setUi",
        "state",
        "metrics",
        "screenshot",
    }
    if not isinstance(bridge, dict):
        errors.append("contract.debugBridge must define deterministic QA transport/capabilities")
    else:
        require_text(bridge, "transport", "contract.debugBridge", errors)
        capabilities = set(
            require_string_list(bridge, "capabilities", "contract.debugBridge", errors)
        )
        if capabilities != required_capabilities:
            errors.append(
                "contract.debugBridge.capabilities must contain exactly "
                f"{sorted(required_capabilities)}"
            )
    proof = contract.get("proofBoundary")
    if not isinstance(proof, dict):
        errors.append("contract.proofBoundary must distinguish build/runtime/device/human proof")
    else:
        require_text(proof, "buildGate", "contract.proofBoundary", errors)
        require_text(proof, "runtimeGate", "contract.proofBoundary", errors)
        require_text(proof, "targetDevice", "contract.proofBoundary", errors)
        if proof.get("humanPlaytestRequired") is not True:
            errors.append("contract.proofBoundary.humanPlaytestRequired must be true")
    return contract


def validate_asset_manifest(
    root: Path, contract: dict[str, Any], manifest: Any, errors: list[str]
) -> set[str]:
    if not isinstance(manifest, dict) or not isinstance(manifest.get("assets"), list):
        errors.append("asset manifest must contain an assets list")
        return set()
    assets = manifest["assets"]
    if len(assets) < 3:
        errors.append("asset manifest must contain at least three real shipping assets")
    ids: set[str] = set()
    roles: set[str] = set()
    by_id: dict[str, dict[str, Any]] = {}
    for index, asset in enumerate(assets):
        label = f"assetManifest.assets[{index}]"
        if not isinstance(asset, dict):
            errors.append(f"{label} must be an object")
            continue
        asset_id = require_text(asset, "id", label, errors)
        if asset_id:
            if asset_id in ids:
                errors.append(f"duplicate asset id: {asset_id}")
            ids.add(asset_id)
            by_id[asset_id] = asset
        role = require_text(asset, "role", label, errors)
        if role:
            roles.add(role)
        category = require_text(asset, "category", label, errors)
        source = require_text(asset, "sourceUrl", label, errors)
        if source and not (source.startswith("https://") or source.startswith("authored://")):
            errors.append(f"{label}.sourceUrl must start with https:// or authored://")
        require_text(asset, "license", label, errors)
        if asset.get("shipApproved") is not True:
            errors.append(f"{label}.shipApproved must be true after manager license review")
        require_text(asset, "fallback", label, errors)
        path = safe_project_path(root, asset.get("path"), f"{label}.path", errors)
        expected_hash = asset.get("sha256")
        if not isinstance(expected_hash, str) or not SHA256_RE.fullmatch(expected_hash):
            errors.append(f"{label}.sha256 must be a 64-character lowercase digest")
        if path:
            if not path.is_file():
                errors.append(f"{label}.path does not exist: {path}")
            elif isinstance(expected_hash, str) and SHA256_RE.fullmatch(expected_hash):
                actual_hash = file_sha256(path)
                if actual_hash != expected_hash:
                    errors.append(
                        f"{label}.sha256 mismatch for {path}: expected {expected_hash}, got {actual_hash}"
                    )
        if contract.get("dimensions") == "3d" and category in THREE_D_CATEGORIES:
            size = asset.get("targetSizeMeters")
            if (
                not isinstance(size, list)
                or len(size) != 3
                or any(not isinstance(v, (int, float)) or v <= 0 for v in size)
            ):
                errors.append(f"{label}.targetSizeMeters must contain three positive values")
            if asset.get("frontAxis") not in AXES:
                errors.append(f"{label}.frontAxis must be one of {sorted(AXES)}")
            if asset.get("upAxis") not in AXES - {"none"}:
                errors.append(f"{label}.upAxis must be a real axis")
            if asset.get("rootMotion") not in ROOT_MOTION_POLICIES:
                errors.append(
                    f"{label}.rootMotion must be one of {sorted(ROOT_MOTION_POLICIES)}"
                )
            for budget_key in ("maxTriangles", "maxTextureMB"):
                budget = asset.get(budget_key)
                if not isinstance(budget, (int, float)) or budget <= 0:
                    errors.append(f"{label}.{budget_key} must be a positive budget")
        if category == "animation":
            if contract.get("dimensions") == "3d":
                if asset.get("upAxis") not in AXES - {"none"}:
                    errors.append(f"{label}.upAxis must be a real axis")
                if asset.get("rootMotion") not in ROOT_MOTION_POLICIES:
                    errors.append(
                        f"{label}.rootMotion must be one of {sorted(ROOT_MOTION_POLICIES)}"
                    )
            duration = asset.get("durationMs")
            if not isinstance(duration, (int, float)) or duration <= 0:
                errors.append(f"{label}.durationMs must be positive")
        if category == "audio":
            for key in ("durationMs", "maxFileMB"):
                value = asset.get(key)
                if not isinstance(value, (int, float)) or value <= 0:
                    errors.append(f"{label}.{key} must be positive")
            for key in ("lufs", "peakDb"):
                if not isinstance(asset.get(key), (int, float)):
                    errors.append(f"{label}.{key} must be measured")
            if not isinstance(asset.get("loop"), bool):
                errors.append(f"{label}.loop must be boolean")
    required_roles = set(contract.get("requiredAssetRoles", []))
    missing_roles = required_roles - roles
    if missing_roles:
        errors.append(f"asset manifest missing required roles: {sorted(missing_roles)}")
    clip_roles = set(contract.get("requiredCharacterClipRoles", []))
    characters = [asset for asset in assets if isinstance(asset, dict) and asset.get("category") == "character"]
    if not characters:
        errors.append("asset manifest needs at least one character asset")
    for character in characters:
        clips = character.get("clips")
        label = f"character asset {character.get('id', '?')}"
        if not isinstance(clips, dict):
            errors.append(f"{label}.clips must map semantic roles to animation asset ids")
            continue
        missing_clips = clip_roles - set(clips)
        if missing_clips:
            errors.append(f"{label}.clips missing roles: {sorted(missing_clips)}")
        for role, clip_id in clips.items():
            if not is_filled_text(role) or not is_filled_text(clip_id):
                errors.append(f"{label}.clips contains an empty/placeholder role or id")
            elif clip_id not in by_id:
                errors.append(f"{label}.clips.{role} references unknown asset id {clip_id}")
            elif by_id[clip_id].get("category") != "animation":
                errors.append(f"{label}.clips.{role} must reference an animation asset")
            else:
                clip = by_id[clip_id]
                duration = clip.get("durationMs")
                if role == "locomotion":
                    gait = clip.get("gaitCycleMs")
                    if not isinstance(gait, (int, float)) or gait <= 0:
                        errors.append(f"{label}.clips.{role} needs measured gaitCycleMs")
                if role in {"primaryAction", "hitOrFail"}:
                    contact = clip.get("contactFrameMs")
                    if (
                        not isinstance(contact, (int, float))
                        or contact < 0
                        or not isinstance(duration, (int, float))
                        or contact > duration
                    ):
                        errors.append(
                            f"{label}.clips.{role} needs contactFrameMs within durationMs"
                        )
    return ids


def validate_prd(
    root: Path,
    contract: dict[str, Any],
    prd: Any,
    asset_ids: set[str],
    errors: list[str],
) -> None:
    if not isinstance(prd, dict) or not isinstance(prd.get("userStories"), list):
        errors.append("scripts/ralph/prd.json must contain userStories")
        return
    stories = prd["userStories"]
    if not stories:
        errors.append("prd.userStories is empty — author the seven quality phases before launch")
        return
    beat_ids = {
        beat.get("id") for beat in contract.get("actionBeats", []) if isinstance(beat, dict)
    }
    evidence_ids = {
        item.get("id") for item in contract.get("canonicalEvidence", []) if isinstance(item, dict)
    }
    tier_ids = {
        tier.get("id") for tier in contract.get("performanceTiers", []) if isinstance(tier, dict)
    }
    story_ids: set[str] = set()
    story_classes: set[str] = set()
    for index, story in enumerate(stories):
        label = f"prd.userStories[{index}]"
        if not isinstance(story, dict):
            errors.append(f"{label} must be an object")
            continue
        story_id = require_text(story, "id", label, errors)
        if story_id:
            if story_id in story_ids:
                errors.append(f"duplicate story id: {story_id}")
            story_ids.add(story_id)
        require_text(story, "title", label, errors)
        require_text(story, "description", label, errors)
        require_string_list(story, "acceptanceCriteria", label, errors)
        require_text(story, "verify", label, errors)
        if not isinstance(story.get("passes"), bool):
            errors.append(f"{label}.passes must be boolean")
        if not isinstance(story.get("managerInterventions"), int):
            errors.append(f"{label}.managerInterventions must be an integer")
        allowed = story.get("allowedFiles")
        if not isinstance(allowed, list) or not allowed:
            errors.append(f"{label}.allowedFiles must contain one or two source files")
            allowed = []
        elif len(allowed) > 2:
            errors.append(f"{label}.allowedFiles has {len(allowed)} files; maximum is two")
        for file_index, allowed_file in enumerate(allowed):
            safe_project_path(root, allowed_file, f"{label}.allowedFiles[{file_index}]", errors)
        test_raw = story.get("testFile")
        test_path = safe_project_path(root, test_raw, f"{label}.testFile", errors)
        if test_path:
            if "tests_staged" not in test_path.parts:
                errors.append(f"{label}.testFile must live under tests_staged/")
            if not test_path.is_file():
                errors.append(f"{label}.testFile does not exist: {test_path}")
            else:
                body = test_path.read_text(encoding="utf-8", errors="replace")
                if "RALPH RED SPEC STUB" in body or FILE_PLACEHOLDER_RE.search(body):
                    errors.append(f"{label}.testFile is still an unimplemented red-spec stub")
            if str(test_raw) in allowed:
                errors.append(f"{label}.testFile must be excluded from allowedFiles")
            verify = story.get("verify")
            if isinstance(verify, str) and str(test_raw) not in verify:
                errors.append(f"{label}.verify must stage/reference its manager-owned testFile")
        quality_class = story.get("qualityClass")
        if quality_class not in REQUIRED_STORY_CLASSES:
            errors.append(f"{label}.qualityClass must be one of {sorted(REQUIRED_STORY_CLASSES)}")
            continue
        story_classes.add(quality_class)
        expected_phase = STORY_CLASS_PHASES[quality_class]
        if story.get("phase") != expected_phase:
            errors.append(f"{label}.phase must be {expected_phase} for {quality_class}")
        if quality_class == "asset-integration":
            refs = set(require_string_list(story, "assetIds", label, errors))
            unknown = refs - asset_ids
            if unknown:
                errors.append(f"{label}.assetIds references unknown assets: {sorted(unknown)}")
        if quality_class == "feedback-atom":
            refs = set(require_string_list(story, "actionBeatIds", label, errors))
            unknown = refs - beat_ids
            if unknown:
                errors.append(f"{label}.actionBeatIds references unknown beats: {sorted(unknown)}")
        if quality_class in {"vertical-slice", "look-lock", "camera-input", "critique-ship"}:
            refs = set(require_string_list(story, "evidenceIds", label, errors))
            unknown = refs - evidence_ids
            if unknown:
                errors.append(f"{label}.evidenceIds references unknown evidence: {sorted(unknown)}")
        if quality_class == "performance-resilience":
            refs = set(require_string_list(story, "performanceTierIds", label, errors))
            unknown = refs - tier_ids
            if unknown:
                errors.append(
                    f"{label}.performanceTierIds references unknown tiers: {sorted(unknown)}"
                )
    missing_classes = REQUIRED_STORY_CLASSES - story_classes
    if missing_classes:
        errors.append(f"prd.userStories missing quality classes: {sorted(missing_classes)}")


def validate_support_files(root: Path, errors: list[str]) -> None:
    brief = root / "scripts/ralph/BRIEF.md"
    qwen = root / "scripts/ralph/QWEN.md"
    ledger = root / "quality/QUALITY-LEDGER.md"
    required_brief_sections = (
        "## Product fantasy",
        "## Product shell",
        "## Reference contract",
        "## Visual system",
        "## Scale and camera",
        "## Asset manifest contract",
        "## Action beat sheets",
        "## Performance and resilience",
        "## Canonical evidence set",
        "## Honest limitations",
    )
    if not brief.is_file():
        errors.append(f"missing {brief}")
    else:
        body = brief.read_text(encoding="utf-8", errors="replace")
        if FILE_PLACEHOLDER_RE.search(body):
            errors.append("BRIEF.md still contains placeholder text")
        for section in required_brief_sections:
            if section not in body:
                errors.append(f"BRIEF.md missing required section: {section}")
    if not qwen.is_file():
        errors.append(f"missing {qwen}")
    else:
        body = qwen.read_text(encoding="utf-8", errors="replace")
        if "{{" in body or "}}" in body or FILE_PLACEHOLDER_RE.search(body):
            errors.append("QWEN.md still contains unresolved template/placeholder text")
        for guard in ("NO PRIMITIVE PLACEHOLDERS", "ASSET-MANIFEST.md", "ANTI-SLOP"):
            if guard not in body:
                errors.append(f"QWEN.md lost mandatory guard: {guard}")
    if not ledger.is_file():
        errors.append(f"missing {ledger}")
    else:
        body = ledger.read_text(encoding="utf-8", errors="replace")
        if FILE_PLACEHOLDER_RE.search(body):
            errors.append("QUALITY-LEDGER.md still contains placeholder text")
        for section in ("## Reference lock", "## Findings", "## Honest limitations"):
            if section not in body:
                errors.append(f"QUALITY-LEDGER.md missing required section: {section}")


def validate_project(root: Path) -> tuple[list[str], list[str]]:
    root = root.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    contract_raw = read_json(root / "quality/contract.json", errors)
    contract = validate_contract(root, contract_raw, errors)
    if contract is None:
        return errors, warnings
    manifest_path = safe_project_path(
        root, contract.get("assetManifest"), "contract.assetManifest", errors
    )
    manifest_raw = read_json(manifest_path, errors) if manifest_path else None
    asset_ids = validate_asset_manifest(root, contract, manifest_raw, errors)
    prd = read_json(root / "scripts/ralph/prd.json", errors)
    validate_prd(root, contract, prd, asset_ids, errors)
    validate_support_files(root, errors)
    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="project root")
    parser.add_argument(
        "--max-errors",
        type=int,
        default=0,
        help="print at most this many errors (0 prints all)",
    )
    args = parser.parse_args(argv)
    errors, warnings = validate_project(args.root)
    for warning in warnings:
        print(f"preflight_quality: WARNING: {warning}")
    if errors:
        print(f"preflight_quality: BLOCKED ({len(errors)} issue(s))")
        shown = errors if args.max_errors <= 0 else errors[: args.max_errors]
        for error in shown:
            print(f"  - {error}")
        if len(shown) < len(errors):
            print(f"  ... {len(errors) - len(shown)} more; run without --max-errors for all")
        return 1
    print("preflight_quality: OK — production contract is complete and machine-checkable")
    return 0


if __name__ == "__main__":
    sys.exit(main())
