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

## What Runs

- `scripts/smoke.py`: registers a demo actor, issues a scoped passport, verifies
  passport binding, evaluates scope, evaluates policy, and writes a public-safe
  summary under `reports/starter-smoke/`.
- `scripts/mcp_demo.py`: checks one safe MCP-style tool call and one unsafe tool
  call. The unsafe call is denied before execution.
- `starters/`: short recipes for model promotion, filesystem tools, and local
  agent passport patterns.

## Commands

```bash
make up
make smoke
make mcp-demo
make clean
```

The Makefile delegates to scripts; Windows users can run the scripts directly.

## Pinned Refs

Defaults are kept in `are.refs.json`.

- `are-foundation`: pinned to the latest public release tag.
- `are-agent-integrations`: pinned to `main` until the first integration release tag exists.

## Safety Boundary

- No customer action is executed.
- Proof summaries keep `executed=false`.
- No raw payloads, tokens, headers, credentials, signatures, private policy
  bodies, or protected evidence should appear in outputs.
- Full ARE/BYOPolicy handles policy generation, simulation, conflict review,
  promotion gates, Command Center, and rich evidence.
