# State 2 — The Same Violation Becomes Checkable

The implementation is intentionally unchanged from State 1, so the feature test still passes:

```bash
python -m unittest discover -s tests -v
```

This commit adds a deterministic architecture check:

```bash
python scripts/check_architecture.py
```

Expected result:

```text
Architecture check failed:
  - src/domain/order.py:3 imports src.infrastructure.email_sender

Rule: src/domain must not import src/infrastructure.
```

The important change is not better documentation. The documented rule is the same. The repository now has an executable mechanism that can determine whether the implementation respects that rule.

The next commit fixes the implementation and wires the documentation and validation into an agent-facing workflow.
