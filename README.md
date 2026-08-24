# Agent Documentation Workflow Demo

A small, reproducible companion demo for an article about how coding agents use repository documentation.

The research motivation comes from *From Agent Behaviour to Agent-Friendly Documentation: An Empirical Study of How Coding Agents Discover, Read, and Write Technical Documentation* (Gao & Chen, 2026): https://arxiv.org/abs/2608.20195

The study observed that coding agents interacted disproportionately with agent-facing artifacts such as instruction files and working notes, while traditional technical documentation represented a much smaller share of documentation activity. It also found no clear pattern in which reading documentation led to explicit validation, and code was often touched before documentation in pull requests that changed both.

This repository does **not** attempt to reproduce those behavioural findings. It demonstrates one engineering response to them:

> Important repository knowledge should not merely exist. For high-value rules, the repository can deliberately route an agent to the right knowledge before implementation, connect that knowledge to validation, and require the resulting evidence to be reported.

## From research observation to engineering response

The demo maps three research observations to three repository mechanisms:

| Research observation | Engineering response in this demo |
| --- | --- |
| Agents spend substantial documentation effort on agent-facing files | Use `AGENTS.md` as a small routing layer for the coding workflow |
| Documentation does not reliably appear before implementation | Tell the agent which authoritative document to read before changing `src/` |
| Reading documentation does not clearly lead to explicit validation | Connect an enforceable architecture rule to a deterministic checker |

The resulting workflow is:

```text
Route  ->  Read  ->  Implement  ->  Validate  ->  Report
```

And the repository separates the responsibilities deliberately:

```text
KNOWLEDGE                 ROUTING                    VERIFICATION

architecture.md    ->     AGENTS.md          ->     executable check
what the rule is          when to consult it        whether it was respected
```

- `docs/architecture.md` is the authoritative engineering knowledge.
- `AGENTS.md` is agent-facing workflow guidance. It points to the authoritative document rather than duplicating its rules.
- `scripts/check_architecture.py` verifies the enforceable part of the rule independently of the agent's reasoning or final explanation.

## The concrete rule used in the demo

The sample has three conceptual layers:

```text
domain  <-  application  ->  infrastructure
```

The documented rule is:

> Code under `src/domain/` must not import code from `src/infrastructure/`.

The feature is intentionally simple: completing an order should send one email notification.

This creates a useful failure case. A developer or coding agent can implement the feature by letting the domain object call the email infrastructure directly. The feature works and its functional test passes, but the implementation violates the documented architecture.

That gap lets the demo show why documentation, routing, and verification are different responsibilities.

## Reproduce the three states

### State 1 — the knowledge exists, but nothing verifies it

```bash
git checkout d0dd3073e785c147b1be81f1302a00d02411569a
python -m unittest discover -s tests -v
```

The architecture document contains the correct rule. The implementation violates it by importing `EmailSender` from the domain layer. The feature test still passes.

This state demonstrates a narrow point: **having the correct technical documentation does not itself create assurance that an implementation respects it.**

### State 2 — the documented rule becomes verifiable

```bash
git checkout 7d390ab447928b119e1b3285a60d4c6a61e46505
python -m unittest discover -s tests -v
python scripts/check_architecture.py
```

The implementation is unchanged. The feature test still passes, but the architecture checker now fails and identifies the prohibited dependency.

The repository has converted one enforceable part of its documentation into objective evidence.

### State 3 — knowledge, routing, and verification are connected

```bash
git checkout main
python -m unittest discover -s tests -v
python scripts/check_architecture.py
```

Both checks pass. The domain now owns only the state transition, while the application layer coordinates the domain object with the email infrastructure service.

The final state also adds `AGENTS.md`, which tells a coding agent to:

1. read `docs/architecture.md` before implementation,
2. identify relevant constraints,
3. inspect the existing code and tests,
4. implement the change,
5. run feature and architecture validation, and
6. report the evidence.

If `make` is available, the final validation can also be run with:

```bash
make validate
```

## Why `AGENTS.md` does not contain the architecture rule

The demo deliberately avoids copying the dependency rule into `AGENTS.md`.

The architecture document remains the source of truth. The agent-facing file acts as a **router**: it tells the agent when that knowledge matters and what workflow should follow from it.

This avoids creating two competing copies of the same technical rule while still giving the coding agent explicit guidance about when to consult the authoritative source.

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

The demo establishes that a repository can contain the correct engineering knowledge while a functionally successful implementation still violates it. It also demonstrates a concrete repository pattern for connecting authoritative documentation to an agent-facing workflow and deterministic validation:

```text
Knowledge  ->  Routing  ->  Verification
```

It does **not** establish that coding agents always ignore traditional documentation, that an agent will never discover `architecture.md` without explicit routing, or that `AGENTS.md` guarantees correct behaviour. Agent behaviour remains model- and context-dependent.

The research paper supplies the empirical evidence about how agents use documentation in practice. This repository demonstrates an engineering response: reduce how much important assurance depends on whether a particular agent happens to discover, remember, interpret, and verify a rule on its own.
