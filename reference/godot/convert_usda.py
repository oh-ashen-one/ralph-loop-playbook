# Blender batch: USDA -> GLB. Usage:
#   blender --background --python convert_usda.py -- <out_dir> <file.usda> [more...]
import sys
from pathlib import Path

import bpy

argv = sys.argv[sys.argv.index("--") + 1 :]
out_dir = Path(argv[0])
out_dir.mkdir(parents=True, exist_ok=True)

for src in argv[1:]:
    src_p = Path(src)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    try:
        bpy.ops.wm.usd_import(filepath=str(src_p))
    except Exception as exc:  # noqa: BLE001
        print(f"IMPORT-FAIL {src_p.name}: {exc}")
        continue
    dst = out_dir / (src_p.stem + ".glb")
    try:
        bpy.ops.export_scene.gltf(filepath=str(dst), export_format="GLB")
        print(f"OK {dst.name}")
    except Exception as exc:  # noqa: BLE001
        print(f"EXPORT-FAIL {src_p.name}: {exc}")
