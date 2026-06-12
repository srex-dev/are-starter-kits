from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache" / "repos"


def run(command: list[str], cwd: Path | None = None) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=cwd, check=True)


def checkout(name: str, repo: str, ref: str) -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    target = CACHE / name
    if not target.exists():
        run(["git", "clone", repo, str(target)])
    run(["git", "fetch", "--all", "--tags"], cwd=target)
    run(["git", "checkout", ref], cwd=target)
    return target


def main() -> None:
    refs = json.loads((ROOT / "are.refs.json").read_text(encoding="utf-8"))
    foundation = checkout("are-foundation", refs["are_foundation"]["repo"], refs["are_foundation"]["ref"])
    integrations = checkout(
        "are-agent-integrations",
        refs["are_agent_integrations"]["repo"],
        refs["are_agent_integrations"]["ref"],
    )

    run(["npm", "install"], cwd=integrations)
    run(["python", "-m", "pip", "install", "-e", "python[dev]"], cwd=integrations)

    print("")
    print("Next:")
    print(f"  cd {foundation}")
    print("  make certs && make up")
    print(f"  cd {ROOT}")
    print("  python scripts/smoke.py")


if __name__ == "__main__":
    main()
