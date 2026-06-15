# ARE Starter Kits

Clone this repo when you want to see ARE Foundation work in minutes:

```text
start foundation -> register agent -> issue passport -> check MCP-style tool calls -> see proof basics
```

This is a public-safe template repo. It does not include Command Center,
BYOPolicy, governance-strata internals, private proof packets, or commercial
ARE evidence surfaces.

## Quick Start

Windows:

```powershell
.\scripts\bootstrap.ps1
python .\scripts\smoke.py
python .\scripts\mcp_demo.py
```

macOS/Linux:

```bash
./scripts/bootstrap.sh
python scripts/smoke.py
python scripts/mcp_demo.py
```

If you already have ARE Foundation running at `http://localhost:18085`, you can
skip bootstrap and run the smoke scripts directly.

## Live Lab

The Nigel live lab is a command-driven demo for talks and design-partner
walkthroughs. It runs commands in the terminal while a browser dashboard updates
side by side.

Prep:

```powershell
python scripts\live_lab.py doctor
python scripts\live_lab.py reset
python scripts\live_lab.py serve --port 8765
```

Open:

```powershell
start http://127.0.0.1:8765/demo/live-lab.html
```

Run the live beats:

```powershell
python scripts\live_lab.py intro
python scripts\live_lab.py actor
python scripts\live_lab.py allow
python scripts\live_lab.py deny
python scripts\live_lab.py mcp
python scripts\live_lab.py summary
```

Presenter docs:

- [Live lab prerequisites](docs/live-lab-prereqs.md)
- [Nigel 15-minute script](docs/nigel-15-minute-script.md)

## What Runs

- `scripts/smoke.py`: registers a demo actor, issues a scoped passport, verifies
  passport binding, evaluates scope, evaluates policy, and writes a public-safe
  summary under `reports/starter-smoke/`.
- `scripts/mcp_demo.py`: checks one safe MCP-style tool call and one unsafe tool
  call. The unsafe call is denied before execution.
- `scripts/live_lab.py`: drives the side-by-side terminal and browser demo,
  including Nigel, passport issuance, allowed and denied model checks, MCP tool
  checks, and a public-safe proof summary under `reports/live-lab/`.
- `starters/`: short recipes for model promotion, filesystem tools, and local
  agent passport patterns.

## Commands

```bash
make up
make smoke
make mcp-demo
make doctor
make live-serve
make live-intro
make live-actor
make live-allow
make live-deny
make live-mcp
make live-summary
make clean
```

The Makefile delegates to scripts; Windows users can run the scripts directly.

## Pinned Refs

Defaults are kept in `are.refs.json`.

- `are-foundation`: pinned to the latest public release tag.
- `are-agent-integrations`: pinned to the first public alpha release tag.

## Safety Boundary

- No customer action is executed.
- Proof summaries keep `executed=false`.
- No raw payloads, tokens, headers, credentials, signatures, private policy
  bodies, or protected evidence should appear in outputs.
- Full ARE/BYOPolicy handles policy generation, simulation, conflict review,
  promotion gates, Command Center, and rich evidence.
