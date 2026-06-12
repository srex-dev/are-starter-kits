# Model Promotion Starter

Use this when your first governed workflow is:

```text
release agent -> model.promote_to_production -> model/champion
```

Checks:

- actor is registered
- passport has `model.promote_to_production` over `model/*`
- scope allows `model/champion`
- policy denies experimental resources
- no model is promoted by the starter kit
