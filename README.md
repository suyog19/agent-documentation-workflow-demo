# Agent Documentation Workflow Demo

A small, reproducible companion demo for an article about how coding agents use repository documentation.

The research motivation comes from *From Agent Behaviour to Agent-Friendly Documentation: An Empirical Study of How Coding Agents Discover, Read, and Write Technical Documentation* (Gao & Chen, 2026): https://arxiv.org/abs/2608.20195

This repository does **not** attempt to reproduce that observational study. It demonstrates one engineering response to the problem it raises:

> A documented engineering rule can exist while code that violates it still appears functionally correct. Where a rule can be checked deterministically, connecting documentation to workflow and executable validation makes compliance observable.

## The pattern

```text
Knowledge                 Routing                 Verification

architecture.md    ->     AGENTS.md       ->     executable check
```

- `docs/architecture.md` contains the authoritative engineering rule.
- `AGENTS.md` tells a coding agent when to consult that documentation and what validation to run.
- `scripts/check_architecture.py` checks the enforceable part of the rule independently of the agent's reasoning.

## The architecture rule

The sample has three conceptual layers:

```text
domain  <-  application  ->  infrastructure
```

The rule is:

> Code under `src/domain/` must not import code from `src/infrastructure/`.

The feature is intentionally simple: completing an order should send one email notification.

## Reproduce the three states

### State 1 — documentation exists, violation still passes feature tests

```bash
git checkout d0dd3073e785c147b1be81f1302a00d02411569a
python -m unittest discover -s tests -v
```

The test passes even though `src/domain/order.py` imports `EmailSender`, violating the documented architecture rule.

### State 2 — the same violation becomes checkable

```bash
git checkout 7d390ab447928b119e1b3285a60d4c6a61e46505
python -m unittest discover -s tests -v
python scripts/check_architecture.py
```

The feature test still passes. The architecture check fails and identifies the prohibited dependency.

### State 3 — compliant implementation and workflow integration

```bash
git checkout main
python -m unittest discover -s tests -v
python scripts/check_architecture.py
```

Both pass. The domain now owns only the state transition, while the application layer coordinates the domain object with the email infrastructure service.

If `make` is available, the same final validation can be run with:

```bash
make validate
```

## Final repository layout

```text
.
├── AGENTS.md
├── Makefile
├── README.md
├── docs/
│   └── architecture.md
├── scripts/
│   └── check_architecture.py
├── src/
│   ├── application/
│   │   └── order_completion.py
│   ├── domain/
│   │   └── order.py
│   └── infrastructure/
│       └── email_sender.py
└── tests/
    └── test_order.py
```

## What the demo establishes — and what it does not

The demo establishes that functional tests alone do not necessarily verify documented architecture constraints, and that an executable check can make one such constraint observable and enforceable.

It does **not** establish that coding agents always ignore traditional documentation, or that `AGENTS.md` guarantees correct behavior. Agent behavior is model- and context-dependent. The point of the repository pattern is to reduce how much assurance depends on discretionary model behavior when an important rule can be checked deterministically.
