# Agent Documentation Workflow Demo

A small, reproducible experiment showing the difference between **having useful documentation** and **wiring that documentation into a coding agent's workflow and validation path**.

The repository supports an article about an emerging engineering problem: coding agents can work in well-documented repositories without necessarily consulting the right documentation at the right stage or turning documented constraints into explicit checks.

## Experiment question

Given the same feature request and the same architecture documentation, what changes when the repository also:

1. routes the agent to the relevant documentation before implementation,
2. requires a deterministic architecture check, and
3. asks the agent to report the evidence it produced?

This is a demonstration of an engineering pattern, **not a scientific replication or proof of agent behaviour**. Coding-agent outputs are stochastic, and results can vary by model, agent, repository state, and run.

## Repository variants

The experiment uses two branches created from the same baseline:

- `case-a-docs-only` — the architecture rule exists in `docs/architecture.md`, but no agent-facing workflow tells the agent when to consult it and no deterministic architecture check enforces it.
- `case-b-workflow-integrated` — the same architecture documentation is retained, while `AGENTS.md` routes the agent to it and `make check-architecture` verifies the key dependency rule.

The feature request is identical in both cases: `experiment/TASK.md`.

## The architecture rule

The demo has three conceptual layers:

```text
domain  <-  application  ->  infrastructure
```

The important rule is simple:

> Code under `src/domain/` must not import code from `src/infrastructure/`.

The domain should remain independent of delivery mechanisms such as email. Application code may coordinate the domain with infrastructure services.

## The feature request

The baseline contains an `Order` domain object and an existing `EmailSender` infrastructure service. The task asks the coding agent to send an email when an order is completed.

A locally convenient implementation can put the email dependency directly inside `Order.complete()`. That works functionally, but violates the documented architecture boundary. A compliant implementation keeps the domain independent and performs the coordination outside the domain layer.

## Running the experiment

Use a fresh checkout or reset to the branch head before every run.

### Case A — documentation only

```bash
git switch case-a-docs-only
python -m unittest discover -s tests -v
```

Give your coding agent only the task in `experiment/TASK.md` and let it work normally.

Record whether the agent:

- read `docs/architecture.md` before its first code change,
- introduced a `domain -> infrastructure` dependency,
- ran any architecture-specific validation,
- reported which documentation and checks influenced completion.

### Case B — workflow-integrated documentation

```bash
git switch case-b-workflow-integrated
make validate
```

Give the same agent the same task in `experiment/TASK.md`. In this branch, the repository itself tells the agent when to consult the architecture document and which checks form part of completion.

Record the same observations.

## Suggested run matrix

For a more useful comparison, run each case several times using:

- the same coding agent and model,
- the same task wording,
- the same starting branch head,
- the same permissions and tool access,
- a fresh context for every run.

A simple results table is sufficient:

| Observation | Docs only | Workflow-integrated |
| --- | ---: | ---: |
| Read architecture before coding |  |  |
| Architecture check executed |  |  |
| Boundary violation introduced |  |  |
| Validation evidence reported |  |  |

Do not interpret a small number of runs as statistically significant evidence. The purpose is to make the workflow mechanism visible and reproducible.

## What this demo is intended to show

The demo separates three concerns that are often collapsed into 'good documentation':

- **Knowledge** — `docs/architecture.md` describes the engineering rule and its rationale.
- **Routing** — `AGENTS.md` tells the agent when that knowledge matters.
- **Verification** — an executable check determines whether the implementation respects the rule.

The intended engineering lesson is straightforward: important repository knowledge becomes more reliable for autonomous work when the workflow deliberately activates it and, where possible, converts it into observable checks.
