# ARE Live Lab Prerequisites

This is the prep checklist for the 15-minute ARE/Nigel live lab.

The goal is simple:

```text
terminal command -> browser proof view updates -> explain what ARE just governed
```

Use this for rehearsal, the prep meeting, and the live room. The demo is public-safe:
no customer action executes, no raw payloads are shown, and no secrets should appear
on screen.

## Screen Layout

Recommended layout for a live room:

- Left side: browser at `http://127.0.0.1:8765/demo/live-lab.html`
- Right side: Windows Terminal or PowerShell
- Optional: slides behind those two windows for the opening and closing

Terminal setup:

- Font size: large enough for the back row
- Theme: high contrast dark
- Window width: at least 90 columns
- Keep only this repo open in the terminal

Browser setup:

- Open the live lab dashboard
- Zoom to 100% or 110%
- Keep the page visible while each command runs

## Local Prereqs

You need these installed before the demo:

- Python 3.11+
- Git
- Docker Desktop
- Node.js and npm
- ARE Foundation available at `http://localhost:18085`
- Python package `are_mcp_gateway` available in the current environment

Run the preflight:

```powershell
cd C:\Users\jonat\are-starter-kits
python scripts\live_lab.py doctor
```

If `ARE Foundation` is not reachable, start ARE Foundation first from the
foundation repo or helper command. The starter kit intentionally does not expose
Cloudflare, Command Center, databases, Grafana, Jaeger, or private proof folders.

## Bootstrap

Fresh starter-kit setup:

```powershell
cd C:\Users\jonat\are-starter-kits
.\scripts\bootstrap.ps1
python scripts\live_lab.py doctor
```

Reset the live lab state:

```powershell
python scripts\live_lab.py reset
```

Start the dashboard server in one terminal:

```powershell
python scripts\live_lab.py serve --port 8765
```

Open the browser:

```powershell
start http://127.0.0.1:8765/demo/live-lab.html
```

Use a second terminal for the commands in the script.

## Live Commands

Run these in order during the live lab:

```powershell
python scripts\live_lab.py intro
python scripts\live_lab.py actor
python scripts\live_lab.py allow
python scripts\live_lab.py deny
python scripts\live_lab.py mcp
python scripts\live_lab.py summary
```

One-shot rehearsal:

```powershell
python scripts\live_lab.py run-all
```

## Make Targets

The Makefile exposes the same flow:

```powershell
make live-reset
make live-intro
make live-actor
make live-allow
make live-deny
make live-mcp
make live-summary
```

## Fallback Plan

If the live stack misbehaves:

1. Keep the browser dashboard open.
2. Run:

   ```powershell
   python scripts\live_lab.py reset
   python scripts\live_lab.py intro
   ```

3. Tell the story from the dashboard and switch to the full ARE screenshots or
   Command Center preview.

Do not debug Docker live unless the room is explicitly a lab room. The point is
governed action flow, not watching dependency therapy happen in real time.

## Safety Rules

- Do not paste API keys, bearer tokens, headers, credentials, signatures, raw
  prompts, raw tool arguments, raw policy bodies, or protected evidence.
- Use fake model names and fake file resources only.
- Keep the phrase `executed=false` visible.
- Say "check-only" when explaining model promotion.
- Say "Foundation" for the OSS S0/S1 repo.
- Say "full ARE" for Command Center, BYOPolicy, HITL, ledger/evidence depth,
  visual proof, recovery, and governance-strata.
