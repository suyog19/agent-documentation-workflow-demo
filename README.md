# State 1 — The Rule Exists, but Nothing Enforces It

This commit intentionally contains an architecture violation.

The repository documents a simple rule in `docs/architecture.md`:

> Code under `src/domain/` must not import code from `src/infrastructure/`.

The implementation violates that rule by letting the domain object depend directly on `EmailSender`.

Run the feature test:

```bash
python -m unittest discover -s tests -v
```

It passes.

That is the point of this state: **functional tests can pass even when the implementation violates a documented engineering constraint.**

The next commit adds a deterministic architecture check without changing the violating implementation.
