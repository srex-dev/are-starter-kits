.PHONY: up smoke mcp-demo clean

up:
	python scripts/bootstrap.py

smoke:
	python scripts/smoke.py

mcp-demo:
	python scripts/mcp_demo.py

clean:
	python scripts/clean.py
