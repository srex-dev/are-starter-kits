from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

for name in [".cache", "reports"]:
    target = ROOT / name
    if target.exists():
        shutil.rmtree(target)
        print(f"removed {target}")
