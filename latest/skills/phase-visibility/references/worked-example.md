# Phase Visibility — Worked Example

Read this reference when creating or reconciling a project's first phase index
or goal-backed execution layer. Adapt names, phases, evidence locations, and
authority to the repository. Do not treat the example as a fixed template.

## Default repository shape

```text
project/
├── docs/
│   ├── initiative-blueprint.md
│   └── live-checklist.md
└── goals/
    ├── 01-foundation.md
    └── 02-residual-work.md
```

Use one Markdown file per goal by default. A per-goal subdirectory is justified
only when the goal owns several supporting files.

The goal's numeric prefix is its stable citation. The filename suffix helps a
human navigate but does not make the goal the durable project definition.

## Phase-completion index

Place the index near the top of the canonical blueprint:

```markdown
## Phase completion index

This index records initiative-level completion, delivery authority, and the
next gate. The live checklist remains the detailed evidence authority.

| Phase | Status | Execution authority | Completion evidence or next gate |
|---|---|---|---|
| Phase 1 — Shared foundation | ⚪ Planned | Dormant [Goal 01](../goals/01-foundation.md) | Invoke Goal 01. |
| Phase 2 — Operator workflow | ⛔ Gated | No executable authority yet | Complete Phase 1, then define Goal 02. |
| Phase 3 — Promotion | ⚪ Planned | No executable authority yet | Requires the approved Phase 2 workflow. |
```

This is a visibility projection, not a task tracker. Detailed work, commands,
tests, and operational status stay in the live checklist.

## Goal-file example

```markdown
# Goal 01 — Phase 1 Foundation

## Status

⚪ Planned and dormant.

This goal starts only when the operator explicitly invokes Goal 01.

## Objective

Deliver and prove the bounded Phase 1 outcome defined in the canonical
initiative blueprint.

## Canonical sources

1. `docs/initiative-blueprint.md`
2. `docs/live-checklist.md`

## Authority activated by invocation

Invocation authorises only the repository discovery, implementation,
validation, runtime reconciliation, and documentation required for this goal.
It does not authorise unrelated repositories, external systems, destructive
actions, or later phases.

## Milestones

1. Reconcile current reality.
2. Implement the smallest coherent package.
3. Validate the outcome and regressions.
4. Reconcile canonical documentation and evidence.

## Acceptance criteria

- The complete Phase 1 outcome is proven.
- Decisive evidence is recorded in the live checklist.
- The phase index names Goal 01 as the actual execution authority.

## Explicit exclusions

- Phase 2 implementation.
- Unrelated cleanup.
- Protected or external changes without their own approval.

## Completion output

Report the implemented outcome, evidence, residual work, repository state, and
next gate without starting it.
```

The real goal should replace generic wording with the project's actual scope,
constraints, acceptance gates, and authority.

## Lifecycle examples

### Dormant goal prepared

```markdown
| Phase 1 — Shared foundation | ⚪ Planned | Dormant [Goal 01](../goals/01-foundation.md) | Invoke Goal 01. |
```

### Goal actively executing

```markdown
| Phase 1 — Shared foundation | 🟨 Active | Active [Goal 01](../goals/01-foundation.md) | Follow current evidence in the live checklist. |
```

### Goal completes the phase

```markdown
| Phase 1 — Shared foundation | ✅ Completed | [Goal 01](../goals/01-foundation.md), completed 19-09-2026 | [Completion evidence](live-checklist.md#phase-1-completion). |
```

### Goal completes but leaves residual phase work

Goal completion alone does not make the phase green:

```markdown
| Phase 1 — Shared foundation | ⚪ Planned | [Goal 01](../goals/01-foundation.md) completed partial; residual work in dormant [Goal 02](../goals/02-residual-work.md) | Invoke Goal 02 after reviewing the residual scope. |
```

Use `🟨 Active` instead when Goal 02 or another approved package is already
executing.

### Goal superseded before execution

```markdown
| Phase 1 — Shared foundation | ⚪ Planned | [Goal 01](../goals/01-foundation.md) superseded; dormant [Goal 02](../goals/02-residual-work.md) is current | Invoke Goal 02. |
```

Preserve enough linked history to explain what happened. Do not keep an
obsolete goal as the current authority merely because it has the lower number.

## Reconciliation test

Before handing off, a reader should be able to answer in one glance:

1. Which phase is current?
2. Is it planned, active, completed, or gated?
3. Which numbered goal or approved package owns the work now?
4. Which earlier attempt was partial or superseded?
5. Where is completion proven?
6. What must happen next?

If those answers require reading every goal or reconstructing chat history,
the index is not yet doing its job.
