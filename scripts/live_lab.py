from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports" / "live-lab"
STATE_PATH = REPORT_DIR / "state.json"
BASE = os.environ.get("ARE_FOUNDATION_URL", "http://localhost:18085").rstrip("/")
TOKEN = os.environ.get("ARE_TOKEN", "test-token")
CALLER = os.environ.get("ARE_CALLER_AGENT_ID", "demo-operator")

GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[36m"
RED = "\033[31m"
BOLD = "\033[1m"
RESET = "\033[0m"
DIM = "\033[2m"


@dataclass
class Step:
    id: str
    label: str
    command: str
    status: str = "waiting"
    headline: str = ""
    detail: str = ""
    outcome: str = ""


@dataclass
class LabState:
    title: str = "Govern Nigel. Govern agents."
    subtitle: str = "Actor, authority, scope, policy, proof before action."
    active_step: str = "reset"
    generated_at: str = ""
    facts: dict[str, Any] = field(default_factory=dict)
    events: list[dict[str, str]] = field(default_factory=list)
    steps: list[Step] = field(default_factory=list)


STEPS = [
    Step("intro", "Meet Nigel", "python scripts/live_lab.py intro"),
    Step("actor", "Register actor + issue passport", "python scripts/live_lab.py actor"),
    Step("allow", "Allowed model check", "python scripts/live_lab.py allow"),
    Step("deny", "Denied risky model check", "python scripts/live_lab.py deny"),
    Step("mcp", "Govern MCP tool calls", "python scripts/live_lab.py mcp"),
    Step("summary", "Proof summary", "python scripts/live_lab.py summary"),
]


def main() -> None:
    parser = argparse.ArgumentParser(description="ARE live lab command driver.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    sub.add_parser("reset")
    sub.add_parser("serve").add_argument("--port", type=int, default=8765)
    for command in ["intro", "actor", "allow", "deny", "mcp", "summary", "run-all"]:
        sub.add_parser(command)
    args = parser.parse_args()

    if args.command == "doctor":
        doctor()
    elif args.command == "reset":
        reset_state()
    elif args.command == "serve":
        serve(args.port)
    elif args.command == "run-all":
        reset_state()
        intro()
        actor()
        allow()
        deny()
        mcp()
        summary()
    else:
        globals()[args.command]()


def doctor() -> None:
    rows = []
    rows.append(("Python", sys.version.split()[0], "ok"))
    rows.append(("Git", which_version("git", ["git", "--version"]), "ok" if shutil.which("git") else "missing"))
    rows.append(("Docker", which_version("docker", ["docker", "--version"]), "ok" if shutil.which("docker") else "missing"))
    rows.append(("Node", which_version("node", ["node", "--version"]), "ok" if shutil.which("node") else "missing"))
    rows.append(("npm", which_version("npm", ["npm", "--version"]), "ok" if shutil.which("npm") else "missing"))
    rows.append(("ARE Foundation", BASE, "ok" if foundation_reachable() else "not reachable"))
    try:
        import are_mcp_gateway  # noqa: F401

        rows.append(("are_mcp_gateway", "python import", "ok"))
    except Exception:
        rows.append(("are_mcp_gateway", "python import", "missing"))

    print_panel("PRE-FLIGHT", "Run this before the room is watching.")
    for name, value, status in rows:
        color = GREEN if status == "ok" else YELLOW
        print(f"{color}{status.upper():<13}{RESET} {name:<18} {value}")
    print()
    print(f"{BOLD}Recommended prep commands{RESET}")
    print("  python scripts/live_lab.py reset")
    print("  python scripts/live_lab.py serve --port 8765")
    print("  start http://127.0.0.1:8765/demo/live-lab.html")
    print("  python scripts/live_lab.py intro")


def reset_state() -> None:
    state = LabState(
        active_step="reset",
        generated_at=now(),
        facts={"executed": False, "boundary": "Public-safe live lab. No customer action executes."},
        steps=[Step(**asdict(step)) for step in STEPS],
    )
    write_state(state)
    print_panel("RESET", "Live lab state reset. Browser dashboard is ready.")


def serve(port: int) -> None:
    os.chdir(ROOT)
    print_panel("SERVE", f"Open http://127.0.0.1:{port}/demo/live-lab.html")
    ThreadingHTTPServer(("127.0.0.1", port), SimpleHTTPRequestHandler).serve_forever()


def intro() -> None:
    state = load_state()
    update_step(
        state,
        "intro",
        "done",
        "Nigel is not malicious. Nigel is helpful.",
        "Nigel represents the normal person, local agent, or workflow that wants to do useful things with tools.",
        "The risk is not intent. The risk is ungoverned action.",
    )
    add_event(state, "Nigel enters", "A non-threatening actor wants to use tools. Governance begins before action.", "info")
    write_state(state)
    print_panel(
        "MEET NIGEL",
        "Nigel has attended one AI webinar and is now ready to modernize the operating model.",
    )
    print_kv("Point", "Intent is not governance.")
    print_kv("Translation", "Agents are Nigel at machine speed.")


def actor() -> None:
    state = load_state()
    req = request_prefix("nigel")
    update_step(state, "actor", "running", "Registering Nigel and issuing scoped authority.", "", "")
    write_state(state)

    agent = post(
        "/v1/identity/agents",
        f"{req}-agent",
        {
            "agent_type": "nigel.local-agent",
            "owner_id": "nigel-office",
            "metadata": {"public": True, "demo": "live-lab"},
        },
    )["agent"]
    passport = post(
        "/v1/passports",
        f"{req}-passport",
        {
            "agent_id": agent["agent_id"],
            "passport_type": "standard",
            "requested_scopes": [
                {"action_class": "model.promote_to_production", "resource_pattern": "model/*"},
                {"action_class": "file.read", "resource_pattern": "file/*"},
            ],
            "ttl_seconds": 3600,
            "issued_by": "nigel-office",
            "reason": "live lab local governance",
        },
    )["passport"]
    verify = post(
        "/v1/passports:verify",
        f"{req}-verify",
        {"agent_id": agent["agent_id"], "passport_id": passport["passport_id"]},
    )

    state.facts.update(
        {
            "agent_id": agent["agent_id"],
            "agent_type": agent["agent_type"],
            "passport_id": passport["passport_id"],
            "passport_verified": verify.get("verified"),
            "scopes": ["model.promote_to_production:model/*", "file.read:file/*"],
            "executed": False,
        }
    )
    update_step(
        state,
        "actor",
        "done",
        "Nigel now has a scoped passport.",
        "Authority is explicit, limited, and attributable.",
        "Actor registered. Passport issued. Passport verified. Nothing executed.",
    )
    add_event(state, "Authority issued", "Nigel can request model promotion checks and file reads, not arbitrary actions.", "good")
    write_state(state)
    print_panel("ACTOR + PASSPORT", "Nigel gets authority, not blind trust.")
    print_kv("Agent", agent["agent_id"])
    print_kv("Passport", passport["passport_id"])
    print_kv("Verified", str(verify.get("verified")))
    print_kv("Executed", "false")


def allow() -> None:
    state = load_state()
    agent_id, passport_id = require_actor(state)
    req = request_prefix("allow")
    update_step(state, "allow", "running", "Checking governed model promotion.", "", "")
    write_state(state)

    scope = post(
        "/v1/enforcement/scope:evaluate",
        f"{req}-scope",
        {
            "agent_id": agent_id,
            "passport_id": passport_id,
            "action_class": "model.promote_to_production",
            "resource": "model/champion",
        },
    )
    policy = post(
        "/v1/policy/evaluations",
        f"{req}-policy",
        {
            "decision_id": f"{req}-policy",
            "agent_id": agent_id,
            "action_class": "model.promote_to_production",
            "resource": "model/champion",
        },
    )
    state.facts["allow_case"] = {
        "action": "model.promote_to_production",
        "resource": "model/champion",
        "scope": scope.get("decision", {}).get("effect"),
        "policy": policy.get("decision", {}).get("effect"),
        "reason": policy.get("decision", {}).get("reason"),
    }
    update_step(
        state,
        "allow",
        "done",
        "Champion model check allowed.",
        "Scope matched and policy allowed the governed model resource.",
        "This is proof before action, not the action itself.",
    )
    add_event(state, "Allowed check", "model/champion passed scope and policy.", "good")
    write_state(state)
    print_panel("ALLOW CASE", "Nigel asks about the champion model. Reasonable. Still checked.")
    print_decision("Scope", scope.get("decision", {}))
    print_decision("Policy", policy.get("decision", {}))
    print_kv("Executed", "false")


def deny() -> None:
    state = load_state()
    agent_id, passport_id = require_actor(state)
    req = request_prefix("deny")
    update_step(state, "deny", "running", "Checking risky model promotion.", "", "")
    write_state(state)

    scope = post(
        "/v1/enforcement/scope:evaluate",
        f"{req}-scope",
        {
            "agent_id": agent_id,
            "passport_id": passport_id,
            "action_class": "model.promote_to_production",
            "resource": "model/experimental-candidate",
        },
    )
    policy = post(
        "/v1/policy/evaluations",
        f"{req}-policy",
        {
            "decision_id": f"{req}-policy",
            "agent_id": agent_id,
            "action_class": "model.promote_to_production",
            "resource": "model/experimental-candidate",
        },
    )
    state.facts["deny_case"] = {
        "action": "model.promote_to_production",
        "resource": "model/experimental-candidate",
        "scope": scope.get("decision", {}).get("effect"),
        "policy": policy.get("decision", {}).get("effect"),
        "reason": policy.get("decision", {}).get("reason"),
    }
    update_step(
        state,
        "deny",
        "done",
        "Experimental model denied.",
        "Scope can be broad while policy still blocks the specific risky resource.",
        "Nigel does not get to promote experimental because it sounds exciting.",
    )
    add_event(state, "Denied check", "model/experimental-candidate was blocked by policy before execution.", "warn")
    write_state(state)
    print_panel("DENY CASE", "Nigel sees 'experimental' and mistakes it for 'visionary'. Policy disagrees.")
    print_decision("Scope", scope.get("decision", {}))
    print_decision("Policy", policy.get("decision", {}))
    print_kv("Executed", "false")


def mcp() -> None:
    state = load_state()
    agent_id, passport_id = require_actor(state)
    update_step(state, "mcp", "running", "Wrapping MCP-style tool calls.", "", "")
    write_state(state)
    try:
        from are_mcp_gateway import AreGatewayConfig, evaluate_tool_call
    except Exception as exc:
        raise SystemExit("are_mcp_gateway is not installed. Run: python scripts/bootstrap.py") from exc

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
    state.facts["mcp_case"] = {
        "safe_tool": {"tool": "file.read", "effect": safe.effect, "enforced_effect": safe.enforced_effect},
        "unsafe_tool": {
            "tool": "file.delete",
            "effect": unsafe.effect,
            "enforced_effect": unsafe.enforced_effect,
            "reason": unsafe.reason,
        },
        "executed": False,
    }
    update_step(
        state,
        "mcp",
        "done",
        "MCP tool boundary governed.",
        "file.read is allowed. file.delete is denied before the tool executes.",
        "This is the OSS beachhead: govern your MCP tool calls.",
    )
    add_event(state, "MCP governed", "Safe tool allowed; unsafe tool denied before execution.", "good")
    write_state(state)
    print_panel("MCP TOOL CALLS", "An agent tool call is Nigel with an API key and no lunch break.")
    print_kv("Safe tool", f"file.read -> {safe.effect}")
    print_kv("Unsafe tool", f"file.delete -> {unsafe.effect}")
    print_kv("Executed", "false")


def summary() -> None:
    state = load_state()
    update_step(
        state,
        "summary",
        "done",
        "Proof returned.",
        "Actor, passport, scope, policy, and MCP denial are visible without exposing payloads.",
        "OSS foundation proves the first gate; full ARE adds BYOPolicy, HITL, Command Center, evidence depth, and recovery.",
    )
    add_event(state, "Proof summary", "Public-safe proof packet written locally.", "info")
    write_state(state)
    summary_path = REPORT_DIR / "public-summary.md"
    summary_path.write_text(render_public_summary(state), encoding="utf-8")
    print_panel("SUMMARY", "Nigel is the story. Agents are the scale problem. ARE is the action boundary.")
    print_kv("Summary", str(summary_path))
    print_kv("Executed", "false")


def post(path: str, idem: str, body: dict[str, Any]) -> dict[str, Any]:
    request_id = idem
    request = urllib.request.Request(
        BASE + path,
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "X-Request-ID": request_id,
            "X-ARE-Agent-ID": CALLER,
            "Idempotency-Key": idem,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:  # noqa: S310 - local dev URL.
            return json.loads(response.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"{path} failed: {exc.code} {body_text}") from exc


def foundation_reachable() -> bool:
    try:
        request = urllib.request.Request(
            BASE + "/v1/platform/health",
            headers={"Authorization": f"Bearer {TOKEN}", "X-Request-ID": "live-lab-doctor", "X-ARE-Agent-ID": CALLER},
        )
        with urllib.request.urlopen(request, timeout=3):  # noqa: S310 - local dev URL.
            return True
    except Exception:
        return False


def require_actor(state: LabState) -> tuple[str, str]:
    agent_id = state.facts.get("agent_id")
    passport_id = state.facts.get("passport_id")
    if not agent_id or not passport_id:
        raise SystemExit("Run actor first: python scripts/live_lab.py actor")
    return str(agent_id), str(passport_id)


def load_state() -> LabState:
    if not STATE_PATH.exists():
        reset_state()
    data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return LabState(
        title=data.get("title", "Govern Nigel. Govern agents."),
        subtitle=data.get("subtitle", ""),
        active_step=data.get("active_step", "reset"),
        generated_at=data.get("generated_at", ""),
        facts=data.get("facts", {}),
        events=data.get("events", []),
        steps=[Step(**step) for step in data.get("steps", [])],
    )


def write_state(state: LabState) -> None:
    state.generated_at = now()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(
        json.dumps(
            {
                "title": state.title,
                "subtitle": state.subtitle,
                "active_step": state.active_step,
                "generated_at": state.generated_at,
                "facts": state.facts,
                "events": state.events[-12:],
                "steps": [asdict(step) for step in state.steps],
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def update_step(state: LabState, step_id: str, status: str, headline: str, detail: str, outcome: str) -> None:
    state.active_step = step_id
    for step in state.steps:
        if step.id == step_id:
            step.status = status
            step.headline = headline
            step.detail = detail
            step.outcome = outcome
            return


def add_event(state: LabState, label: str, summary_text: str, tone: str) -> None:
    state.events.append({"time": time.strftime("%H:%M:%S"), "label": label, "summary": summary_text, "tone": tone})


def render_public_summary(state: LabState) -> str:
    facts = state.facts
    lines = [
        "# ARE Live Lab Public Summary",
        "",
        f"- Agent: `{facts.get('agent_id', 'not-set')}`",
        f"- Passport: `{facts.get('passport_id', 'not-set')}`",
        f"- Passport verified: `{facts.get('passport_verified', 'unknown')}`",
        f"- Allow case: `{facts.get('allow_case', {}).get('policy', 'unknown')}`",
        f"- Deny case: `{facts.get('deny_case', {}).get('policy', 'unknown')}`",
        f"- MCP safe tool: `{facts.get('mcp_case', {}).get('safe_tool', {}).get('effect', 'unknown')}`",
        f"- MCP unsafe tool: `{facts.get('mcp_case', {}).get('unsafe_tool', {}).get('effect', 'unknown')}`",
        "- Executed: `false`",
        "",
        "Boundary: public-safe local lab. No customer action executed.",
    ]
    return "\n".join(lines) + "\n"


def print_panel(title: str, message: str) -> None:
    width = 76
    print()
    print(f"{BLUE}+{'-' * (width - 2)}+{RESET}")
    print(f"{BLUE}|{RESET} {BOLD}{title:<{width - 4}}{RESET} {BLUE}|{RESET}")
    print(f"{BLUE}|{RESET} {message:<{width - 4}} {BLUE}|{RESET}")
    print(f"{BLUE}+{'-' * (width - 2)}+{RESET}")


def print_kv(key: str, value: str) -> None:
    print(f"{YELLOW}{key:<14}{RESET} {value}")


def print_decision(label: str, decision: dict[str, Any]) -> None:
    effect = str(decision.get("effect", "UNKNOWN"))
    color = GREEN if effect == "ALLOW" else RED if effect == "DENY" else YELLOW
    print(f"{YELLOW}{label:<14}{RESET} {color}{effect:<8}{RESET} {decision.get('reason', '')}")


def which_version(name: str, command: list[str]) -> str:
    if not shutil.which(name):
        return "not found"
    try:
        return subprocess.check_output(command, text=True, stderr=subprocess.STDOUT, timeout=5).strip().splitlines()[0]
    except Exception:
        return "found"


def request_prefix(label: str) -> str:
    return f"live-lab-{label}-{int(time.time() * 1000)}"


def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


if __name__ == "__main__":
    main()
