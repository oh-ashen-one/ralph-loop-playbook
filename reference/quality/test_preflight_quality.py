#!/usr/bin/env python3
"""Red/green tests for the production-quality launch gate."""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from preflight_quality import REQUIRED_EVIDENCE_IDS, STORY_CLASS_PHASES, validate_project


class QualityPreflightTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for directory in ("quality/references", "assets", "scripts/ralph", "tests_staged", "src"):
            (self.root / directory).mkdir(parents=True, exist_ok=True)
        self._write_project()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _asset(self, asset_id: str, role: str, category: str) -> dict[str, object]:
        path = self.root / "assets" / f"{asset_id}.glb"
        path.write_bytes(f"fixture:{asset_id}".encode())
        asset: dict[str, object] = {
            "id": asset_id,
            "role": role,
            "category": category,
            "sourceUrl": "https://example.test/assets",
            "license": "CC0",
            "shipApproved": True,
            "path": str(path.relative_to(self.root)),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "fallback": f"procedural:{role}",
        }
        if category in {"character", "environment", "prop"}:
            asset.update(
                {
                    "targetSizeMeters": [1.0, 1.0, 1.0],
                    "frontAxis": "+Z" if category == "character" else "none",
                    "upAxis": "+Y",
                    "rootMotion": "cancel-horizontal" if category == "character" else "none",
                    "maxTriangles": 15000,
                    "maxTextureMB": 16,
                }
            )
        if category == "animation":
            asset.update(
                {
                    "durationMs": 1000,
                    "upAxis": "+Y",
                    "rootMotion": "in-place",
                    "gaitCycleMs": 500,
                    "contactFrameMs": 500,
                }
            )
        return asset

    def _write_project(self) -> None:
        assets = [
            self._asset("hero", "hero", "character"),
            self._asset("environment", "environment-kit", "environment"),
            self._asset("prop", "primary-interactable", "prop"),
            self._asset("idle", "hero-idle", "animation"),
            self._asset("locomotion", "hero-locomotion", "animation"),
            self._asset("action", "hero-action", "animation"),
            self._asset("hit", "hero-hit", "animation"),
        ]
        assets[0]["clips"] = {
            "idle": "idle",
            "locomotion": "locomotion",
            "primaryAction": "action",
            "hitOrFail": "hit",
        }
        (self.root / "assets/asset-manifest.json").write_text(
            json.dumps({"schemaVersion": 1, "assets": assets}), encoding="utf-8"
        )
        for evidence_id in REQUIRED_EVIDENCE_IDS:
            probe = self.root / "tests_staged" / f"probe-{evidence_id}.sh"
            probe.write_text("#!/bin/bash\nexit 0\n", encoding="utf-8")
        contract = {
            "schemaVersion": 1,
            "projectName": "Fixture Game",
            "dimensions": "3d",
            "productFantasy": "Race a storm skiff through a hand-painted archipelago.",
            "assetManifest": "assets/asset-manifest.json",
            "requiredPhases": [1, 2, 3, 4, 5, 6, 7],
            "humanCheckpoints": [2, 7],
            "requiredStoryClasses": list(STORY_CLASS_PHASES),
            "requiredAssetRoles": ["hero", "environment-kit", "primary-interactable"],
            "requiredCharacterClipRoles": ["idle", "locomotion", "primaryAction", "hitOrFail"],
            "productShell": {
                "coreFlows": ["boot", "menu", "play", "pause", "failure", "restart", "settings"],
                "persistenceContract": "Settings and best results survive a clean relaunch.",
                "loadingFallback": "Loading state remains branded and exposes a recoverable retry.",
                "missingMediaFallback": "Missing media lowers fidelity but never blocks play.",
            },
            "assetIo": {
                "maxConcurrentLoads": 4,
                "retryAttempts": 3,
                "timeoutMs": 10000,
                "backoffPolicy": "exponential with deterministic test jitter disabled",
                "localOnlyAtShip": True,
            },
            "sharedSimulation": [
                {
                    "quantity": "ocean height and normal",
                    "source": "one compiled wave table",
                    "consumers": ["renderer", "boat buoyancy", "AI racing line"],
                }
            ],
            "referenceContract": [
                {
                    "id": "ref-ocean",
                    "source": "https://example.test/reference",
                    "localPath": "quality/references/ocean.png",
                    "sha256": "",
                    "learn": ["layered wave silhouettes and warm horizon separation"],
                    "mustNotCopy": ["characters, logo, course layout, or exact palette"],
                    "evidenceId": "title",
                }
            ],
            "actionBeats": [
                {
                    "id": "boost",
                    "stateResult": "speed rises from 12 to 18 metres per second",
                    "timelineMs": {"anticipation": 80, "contact": 40, "response": 240, "settle": 300},
                    "channels": ["state", "motion", "visual", "audio", "hud", "camera"],
                    "evidenceIds": ["primary-action"],
                }
            ],
            "canonicalEvidence": [
                {
                    "id": evidence_id,
                    "seed": 7,
                    "state": f"deterministic {evidence_id} state",
                    "camera": "canonical-chase",
                    "viewport": [390, 844] if evidence_id == "mobile" else [1280, 720],
                    "assertions": [f"{evidence_id} state is visible and measurable"],
                }
                for evidence_id in sorted(REQUIRED_EVIDENCE_IDS)
            ],
            "performanceTiers": [
                {
                    "id": "target",
                    "device": "desktop WebGL2 baseline",
                    "worstScene": "storm race with four rivals and maximum spray",
                    "durationSeconds": 30,
                    "maxP95FrameMs": 16.7,
                    "maxDrawCalls": 250,
                    "maxActiveObjects": 600,
                    "maxParticles": 1200,
                    "maxPixelRatio": 2,
                    "maxConcurrentAssetLoads": 4,
                    "maxResidentAssetMB": 512,
                    "poolBudgets": {"collectibles": 70, "effects": 32},
                    "preserve": ["controls, hazard silhouette, boost feedback"],
                    "degradeOrder": ["grain", "bloom", "ambient spray"],
                }
            ],
            "inputMatrix": [
                {
                    "device": "touch phone",
                    "viewport": [390, 844],
                    "input": "swipe",
                    "firstAction": "steer into the next lane",
                    "minTargetPx": 44,
                    "probe": "tests_staged/probe-mobile.sh",
                }
            ],
            "debugBridge": {
                "transport": "window.__fixture debug-only bridge",
                "capabilities": [
                    "reset",
                    "start",
                    "stepOrSeek",
                    "input",
                    "setCamera",
                    "setUi",
                    "state",
                    "metrics",
                    "screenshot",
                ],
            },
            "proofBoundary": {
                "buildGate": "npm run build",
                "runtimeGate": "Playwright drives one complete race and restart",
                "targetDevice": "desktop WebGL2 plus 390x844 touch emulation",
                "humanPlaytestRequired": True,
            },
        }
        reference_path = self.root / "quality/references/ocean.png"
        reference_path.write_bytes(b"reference fixture")
        contract["referenceContract"][0]["sha256"] = hashlib.sha256(
            reference_path.read_bytes()
        ).hexdigest()
        (self.root / "quality/contract.json").write_text(json.dumps(contract), encoding="utf-8")
        classes = list(STORY_CLASS_PHASES)
        stories = []
        for index, quality_class in enumerate(classes, start=1):
            test_file = f"tests_staged/test-q{index:02d}.sh"
            (self.root / test_file).write_text("#!/bin/bash\nexit 0\n", encoding="utf-8")
            story: dict[str, object] = {
                "id": f"US-Q{index:02d}",
                "title": f"Implement {quality_class}",
                "description": f"Implement the measured {quality_class} contract in exactly one subsystem.",
                "acceptanceCriteria": ["The manager-owned behavioral test passes."],
                "priority": index,
                "phase": STORY_CLASS_PHASES[quality_class],
                "qualityClass": quality_class,
                "passes": False,
                "managerInterventions": 0,
                "allowedFiles": [f"src/q{index:02d}.ts"],
                "testFile": test_file,
                "verify": f"bash {test_file}",
            }
            if quality_class == "asset-integration":
                story["assetIds"] = ["hero", "environment", "prop"]
            elif quality_class == "feedback-atom":
                story["actionBeatIds"] = ["boost"]
            elif quality_class == "performance-resilience":
                story["performanceTierIds"] = ["target"]
            elif quality_class in {"vertical-slice", "look-lock", "camera-input", "critique-ship"}:
                story["evidenceIds"] = ["traversal", "failure"]
            stories.append(story)
        (self.root / "scripts/ralph/prd.json").write_text(
            json.dumps({"projectName": "Fixture Game", "userStories": stories}), encoding="utf-8"
        )
        brief_sections = (
            "Product fantasy",
            "Product shell",
            "Reference contract",
            "Visual system",
            "Scale and camera",
            "Asset manifest contract",
            "Action beat sheets",
            "Performance and resilience",
            "Canonical evidence set",
            "Honest limitations",
        )
        (self.root / "scripts/ralph/BRIEF.md").write_text(
            "# Fixture Game\n\n" + "\n\n".join(f"## {section}\nSpecific contract." for section in brief_sections),
            encoding="utf-8",
        )
        (self.root / "scripts/ralph/QWEN.md").write_text(
            "# ANTI-SLOP\nNO PRIMITIVE PLACEHOLDERS\nUse ASSET-MANIFEST.md.\n",
            encoding="utf-8",
        )
        (self.root / "quality/QUALITY-LEDGER.md").write_text(
            "# Quality ledger\n\n## Reference lock\nLocked.\n\n## Findings\nNone yet.\n\n## Honest limitations\nNot physically tested.\n",
            encoding="utf-8",
        )

    def assert_valid(self) -> None:
        errors, _ = validate_project(self.root)
        self.assertEqual([], errors, "\n".join(errors))

    def test_complete_contract_passes(self) -> None:
        self.assert_valid()

    def test_asset_hash_mismatch_blocks(self) -> None:
        (self.root / "assets/hero.glb").write_bytes(b"changed")
        errors, _ = validate_project(self.root)
        self.assertTrue(any("sha256 mismatch" in error for error in errors))

    def test_missing_license_approval_blocks(self) -> None:
        path = self.root / "assets/asset-manifest.json"
        manifest = json.loads(path.read_text())
        manifest["assets"][0]["license"] = "TBD"
        manifest["assets"][0]["shipApproved"] = False
        path.write_text(json.dumps(manifest))
        errors, _ = validate_project(self.root)
        self.assertTrue(any("license" in error or "shipApproved" in error for error in errors))

    def test_missing_canonical_state_blocks(self) -> None:
        path = self.root / "quality/contract.json"
        contract = json.loads(path.read_text())
        contract["canonicalEvidence"] = [
            item for item in contract["canonicalEvidence"] if item["id"] != "mobile"
        ]
        path.write_text(json.dumps(contract))
        errors, _ = validate_project(self.root)
        self.assertTrue(any("missing required ids" in error for error in errors))

    def test_story_over_two_files_blocks(self) -> None:
        path = self.root / "scripts/ralph/prd.json"
        prd = json.loads(path.read_text())
        prd["userStories"][0]["allowedFiles"] = ["src/a.ts", "src/b.ts", "src/c.ts"]
        path.write_text(json.dumps(prd))
        errors, _ = validate_project(self.root)
        self.assertTrue(any("maximum is two" in error for error in errors))

    def test_unimplemented_manager_test_blocks(self) -> None:
        path = self.root / "tests_staged/test-q01.sh"
        path.write_text("#!/bin/bash\n# RALPH RED SPEC STUB\nexit 1\n")
        errors, _ = validate_project(self.root)
        self.assertTrue(any("red-spec stub" in error for error in errors))

    def test_missing_debug_bridge_blocks(self) -> None:
        path = self.root / "quality/contract.json"
        contract = json.loads(path.read_text())
        del contract["debugBridge"]
        path.write_text(json.dumps(contract))
        errors, _ = validate_project(self.root)
        self.assertTrue(any("debugBridge" in error for error in errors))

    def test_incomplete_product_shell_blocks(self) -> None:
        path = self.root / "quality/contract.json"
        contract = json.loads(path.read_text())
        contract["productShell"]["coreFlows"].remove("restart")
        path.write_text(json.dumps(contract))
        errors, _ = validate_project(self.root)
        self.assertTrue(any("coreFlows missing" in error for error in errors))

    def test_unmeasured_locomotion_blocks(self) -> None:
        path = self.root / "assets/asset-manifest.json"
        manifest = json.loads(path.read_text())
        locomotion = next(asset for asset in manifest["assets"] if asset["id"] == "locomotion")
        del locomotion["gaitCycleMs"]
        path.write_text(json.dumps(manifest))
        errors, _ = validate_project(self.root)
        self.assertTrue(any("gaitCycleMs" in error for error in errors))

    def test_invalid_pool_budget_blocks(self) -> None:
        path = self.root / "quality/contract.json"
        contract = json.loads(path.read_text())
        contract["performanceTiers"][0]["poolBudgets"]["effects"] = 0
        path.write_text(json.dumps(contract))
        errors, _ = validate_project(self.root)
        self.assertTrue(any("poolBudgets" in error for error in errors))

    def test_unresolved_qwen_engine_template_blocks(self) -> None:
        path = self.root / "scripts/ralph/QWEN.md"
        path.write_text(
            "# ANTI-SLOP\nNO PRIMITIVE PLACEHOLDERS\nUse ASSET-MANIFEST.md.\n## {{ENGINE}} laws\n",
            encoding="utf-8",
        )
        errors, _ = validate_project(self.root)
        self.assertTrue(any("QWEN.md still contains" in error for error in errors))

    def test_reference_drift_blocks(self) -> None:
        (self.root / "quality/references/ocean.png").write_bytes(b"changed reference")
        errors, _ = validate_project(self.root)
        self.assertTrue(any("referenceContract" in error and "sha256 mismatch" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
