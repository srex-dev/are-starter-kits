from __future__ import annotations

import json
import os
import time
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get("ARE_FOUNDATION_URL", "http://localhost:18085").rstrip("/")
TOKEN = os.environ.get("ARE_TOKEN", "test-token")
CALLER = os.environ.get("ARE_CALLER_AGENT_ID", "demo-operator")
REQ = f"starter-{int(time.time())}"


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
    agent = post(
        "/v1/identity/agents",
        "agent",
        {"agent_type": "starter.release-agent", "owner_id": "starter-owner", "metadata": {"public": True}},
    )["agent"]
    agent_id = agent["agent_id"]
    passport = post(
        "/v1/passports",
        "passport",
        {
            "agent_id": agent_id,
            "passport_type": "standard",
            "requested_scopes": [{"action_class": "model.promote_to_production", "resource_pattern": "model/*"}],
            "ttl_seconds": 3600,
            "issued_by": "starter-owner",
            "reason": "starter kit model promotion check",
        },
    )["passport"]
    passport_id = passport["passport_id"]
    verify = post("/v1/passports:verify", "verify", {"agent_id": agent_id, "passport_id": passport_id})
    scope = post(
        "/v1/enforcement/scope:evaluate",
        "scope",
        {
            "agent_id": agent_id,
            "passport_id": passport_id,
            "action_class": "model.promote_to_production",
            "resource": "model/champion",
        },
    )
    policy = post(
        "/v1/policy/evaluations",
        "policy",
        {
            "decision_id": f"{REQ}-policy",
            "agent_id": agent_id,
            "action_class": "model.promote_to_production",
            "resource": "model/champion",
        },
    )

    summary = {
        "request_id": REQ,
        "agent_id": agent_id,
        "passport_id": passport_id,
        "passport_verified": verify.get("verified"),
        "scope_effect": scope.get("decision", {}).get("effect"),
        "policy_effect": policy.get("decision", {}).get("effect"),
        "executed": False,
        "boundary": "Starter smoke is check-only and public-safe.",
    }
    out_dir = ROOT / "reports" / "starter-smoke"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (out_dir / "public-summary.md").write_text(
        "# Starter Smoke Summary\n\n"
        f"- Agent: `{agent_id}`\n"
        f"- Passport: `{passport_id}`\n"
        f"- Scope: `{summary['scope_effect']}`\n"
        f"- Policy: `{summary['policy_effect']}`\n"
        "- Executed: `false`\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
