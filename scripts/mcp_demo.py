from __future__ import annotations

import json
import os
import time
import urllib.request
from pathlib import Path
from typing import Any

from are_mcp_gateway import AreGatewayConfig, evaluate_tool_call

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get("ARE_FOUNDATION_URL", "http://localhost:18085").rstrip("/")
TOKEN = os.environ.get("ARE_TOKEN", "test-token")
CALLER = os.environ.get("ARE_CALLER_AGENT_ID", "demo-operator")
REQ = f"starter-mcp-{int(time.time())}"


def post(path: str, purpose: str, body: dict[str, Any]) -> dict[str, Any]:
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "X-Request-ID": f"{REQ}-{purpose}",
            "X-ARE-Agent-ID": CALLER,
            "Idempotency-Key": f"{REQ}-{purpose}",
        },
    )
    with urllib.request.urlopen(req, timeout=10) as response:  # noqa: S310 - local dev URL.
        return json.loads(response.read().decode("utf-8") or "{}")


def main() -> None:
    agent_id = post(
        "/v1/identity/agents",
        "agent",
        {"agent_type": "starter.local-agent", "owner_id": "starter-owner", "metadata": {"public": True}},
    )["agent"]["agent_id"]
    passport_id = post(
        "/v1/passports",
        "passport",
        {
            "agent_id": agent_id,
            "passport_type": "standard",
            "requested_scopes": [{"action_class": "file.read", "resource_pattern": "file/*"}],
            "ttl_seconds": 3600,
            "issued_by": "starter-owner",
            "reason": "starter kit MCP file read check",
        },
    )["passport"]["passport_id"]

    config = AreGatewayConfig(
        foundation_url=BASE,
        token=TOKEN,
        agent_id=agent_id,
        passport_id=passport_id,
        map_tool_call=lambda call: {
            "action_type": call["name"],
            "resource": call.get("resource", "file/readme"),
        },
    )
    safe = evaluate_tool_call({"name": "file.read", "resource": "file/readme"}, config)
    unsafe = evaluate_tool_call({"name": "file.delete", "resource": "file/private"}, config)

    summary = {
        "safe_call": {"effect": safe.effect, "enforced_effect": safe.enforced_effect},
        "unsafe_call": {"effect": unsafe.effect, "enforced_effect": unsafe.enforced_effect, "reason": unsafe.reason},
        "executed": False,
        "boundary": "Demo checks tool calls before execution.",
    }
    out_dir = ROOT / "reports" / "mcp-demo"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
