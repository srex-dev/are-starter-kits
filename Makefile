.PHONY: up smoke mcp-demo clean doctor live-reset live-serve live-intro live-actor live-allow live-deny live-mcp live-summary live-all

up:
	python scripts/bootstrap.py

smoke:
	python scripts/smoke.py

mcp-demo:
	python scripts/mcp_demo.py

clean:
	python scripts/clean.py

doctor:
	python scripts/live_lab.py doctor

live-reset:
	python scripts/live_lab.py reset

live-serve:
	python scripts/live_lab.py serve --port 8765

live-intro:
	python scripts/live_lab.py intro

live-actor:
	python scripts/live_lab.py actor

live-allow:
	python scripts/live_lab.py allow

live-deny:
	python scripts/live_lab.py deny

live-mcp:
	python scripts/live_lab.py mcp

live-summary:
	python scripts/live_lab.py summary

live-all:
	python scripts/live_lab.py run-all
