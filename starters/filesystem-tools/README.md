# Filesystem Tools Starter

Use this when your first governed workflow is local tool access.

Default pattern:

- allow: `file.read` over `file/*`
- deny: `file.delete` unless explicitly scoped and allowed by policy
- never send raw file contents to ARE Foundation
