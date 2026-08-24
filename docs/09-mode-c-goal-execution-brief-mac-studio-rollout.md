# Doc 9 — Mode C Goal — Mac Studio Rollout and Mac mini Handoff

**Status:** Goal executed through Doc 3 Gates 0–14; Phase 15 remains deferred. See [Doc 10](10-implementation-architecture-and-operations.md), [Doc 11](11-validation-evidence-mac-studio.md), and [Doc 12](12-mac-mini-phase-15-handoff.md).
**Scope:** Complete the Mac Studio implementation through Doc 3 Gates 0–14, including a production publisher, a complete consumer implementation proven only through isolated Mac Studio simulation, permanent documentation and a bounded Mac mini handoff
**Deferred:** Doc 3 Phase 15 real Mac mini installation, live consumer validation and full Mac Studio → GitHub → Mac mini proof
**Goal record:** This package supplied the authority boundary for the completed Mac Studio rollout. It remains the preserved goal input; Docs 10–12 record outcome, evidence and deferred work.

## Status

- ✅ Docs 1–8 retain their established architecture, discovery and implementation-plan roles.
- ✅ This package subsequently authorized and governed the completed Mac Studio Mode C rollout through Gate 14.
- ✅ All four Doc 6 publication modes are implemented; `after_settle` is the active default.
- ✅ Application code, environment, rsync, configuration, managed snapshot, distribution artifacts, Git publication and the publisher LaunchAgent are implemented and validated in Docs 10–11.
- ⏸ Real Mac mini work remains outside this completed goal and is handed off in Doc 12.
- ℹ The objective and future-tense execution language below are preserved as the approved goal input, not current implementation status.

## Goal objective

Build, validate, document and publish the complete reusable Codex Config Manager system on the Mac Studio through Doc 3 Gates 0–14.

The completed goal must provide:

1. the repository-owned Python project, reproducible `.venv` contract and repository-owned rsync runtime;
2. validated publisher and consumer configuration with deterministic `MacStudio` and `MacMini` identity enforcement;
3. one reusable managed-scope contract with dynamic user-skill discovery and the ingestion-boundary exclusions for `.system/**` and `.DS_Store`;
4. private candidate construction and the root-level canonical `latest/` snapshot;
5. the Mac Studio publisher with all four approved settled-state publication modes;
6. deterministic per-skill ZIPs, `global-agents.zip` and the bounded README download surface derived only from validated `latest/`;
7. conservative Git publication with deterministic component-level commit context, atomic receipts and no force-push or automatic release tags;
8. a complete bounded consumer implementation tested only against isolated paths on the Mac Studio;
9. complete automated, simulation and real Mac Studio launchd evidence;
10. permanent operating and implementation documentation plus a bounded Phase 15 Mac mini handoff.

Completion of this goal means **Mac Studio Mode C complete** under Doc 3. It does not mean the whole two-machine project is complete.

## Governing documents and precedence

Doc 3 remains the canonical phase-and-gate implementation plan. This document is its execution brief: it records current Git reality and closes the publication-control decisions that remained open in Doc 6. It does not rewrite Doc 3 or duplicate its detailed implementation requirements.

Read in this order before mutation:

1. [Doc 3 — Mode C Implementation Plan](03-mode-c-implementation-plan.md)
2. [Doc 1 — Managed Skill Ingestion Exclusions](01-implementation-discovery-managed-skill-ingestion-exclusions.md)
3. [Doc 2 — Python Runtime and Environment Ownership](02-implementation-discovery-python-runtime-environment-ownership.md)
4. [Doc 4 — Deterministic Machine Identity](04-implementation-discovery-deterministic-machine-identity.md)
5. [Doc 5 — Deterministic Managed-State Publication History](05-implementation-discovery-deterministic-managed-state-publication-history.md)
6. [Doc 6 — Settled-State Publication Controls](06-implementation-discovery-settled-state-publication-controls.md)
7. [Doc 7 — Portable Global Guidance and Per-Skill ZIP Distribution](07-implementation-discovery-portable-skills-zip-distribution.md)
8. [Doc 8 — Root-Level Latest Managed Snapshot](08-architecture-reconciliation-root-level-latest-managed-snapshot.md)
9. this Doc 9 execution brief.

If Doc 6 still labels any decision below as open, this later operator-approved record closes that bounded decision. All other architectural authority remains with Docs 1–8 according to Doc 3's existing precedence rules. The two bootstrap documents remain unchanged historical design inputs.

## Current Git baseline

The earlier Git-bootstrap uncertainty is resolved:

```text
branch:         main
HEAD:           6f8c66a3de5d042c9616c22a97434c26e038815c
upstream:       origin/main
upstream HEAD:  6f8c66a3de5d042c9616c22a97434c26e038815c
remote:         git@github.com:YodaSpow/codex-config-manager.git
push method:    normal SSH push
force used:     no
```

Doc 3 Phase 1 must therefore revalidate and preserve this established checkout rather than recreate or reattach it. The successful push satisfies the positive Git-bootstrap proof. Any remaining negative-path tests and implementation-specific Git safety behaviour still belong to the relevant Doc 3 gates.

## Locked first-implementation publication contract

### Publication modes

The first implementation must support all four modes:

| Mode | Locked behaviour |
| --- | --- |
| `after_settle` | Default. Publish on the next eligible check after the managed state has remained quiet for the complete settlement period. |
| `paused` | Continue observing and settling, but freeze candidate, `latest/`, artifacts, README, commit and push mutation. Preserve any exact pending unpushed publication until deliberate resume or recovery. |
| `scheduled` | Publish only at the approved daily wall-clock boundary when the state is already settled and otherwise eligible. |
| `throttled` | Publish settled state automatically only after the minimum interval since the last successful publication has also elapsed. |

`manual` remains excluded.

### Approved operator-facing YAML

The committed example and private configuration must represent the approved defaults and guide in this form, subject only to surrounding schema sections required by Doc 3:

```yaml
publisher:
  check_interval: 1m
  settle_period: 5m
  publication:
    mode: "after_settle"
    schedule:
      frequency: "daily"
      local_time: "18:00"
      timezone: "Europe/London"
    minimum_interval: 1h

# 📖 Publication guide
# 🔄 Modes: "after_settle", "paused", "scheduled", "throttled".
# ⏱️ Durations: whole numbers with s/m/h/d; zero invalid.
# 📏 Limits: check 10s–1h, settle 1m–7d, throttle 1m–30d.
# 🔗 Settle and throttle durations must be >= check_interval.
# 🗓️ Scheduled: missed, unavailable, or unsettled at 18:00 defers to the next day.
```

The inactive mode-specific values may remain configured and validated; only the selected mode gives them runtime authority.

## Seven settled decisions

### 1. Scheduled timezone

Scheduled mode uses the explicit IANA timezone `Europe/London`. Python `zoneinfo` supplies the applicable GMT/BST offset and daylight-saving transition rules. Machine-local timezone guessing is not publication authority.

### 2. Scheduled default boundary

The initial scheduled frequency is daily at `18:00` in `Europe/London`, expressed as a quoted strict 24-hour `HH:MM` value.

### 3. Strict scheduled-window behaviour

The managed state must already be settled at the daily boundary. If the Mac Studio is unavailable or the state is unsettled at `18:00`, that publication opportunity is missed and the pending state waits for the next day's `18:00` boundary. There is no same-evening catch-up.

A push failure after a valid boundary created an exact pending commit is recovery of that same authorised publication, not a new schedule decision; safe retry may continue under the pending-publication contract.

### 4. Throttle default and time basis

`minimum_interval` defaults to `1h` and is measured from the last successful managed-state publication. The first valid settled publication is not artificially delayed when no previous success exists. Failed attempts do not reset the interval, and retry of an already-created exact pending commit does not wait for a new throttle interval.

### 5. Pause precedence and Git reconciliation

`paused` freezes the complete mutation/publication flow, including retries of an already-created but unpushed commit. Observation and settlement may continue without mutating candidate state, `latest/`, derived artifacts, README or Git.

On resume:

- when GitHub is unchanged, retry the exact validated pending commit normally;
- when no local pending commit exists and `origin/main` has advanced safely, fetch and fast-forward before forming a new managed publication;
- tags or GitHub Releases attached to an existing commit do not independently advance `main`;
- a direct GitHub file edit creates a new commit and must be reconciled as remote history;
- when a local pending commit and an independent remote commit overlap, never force-push or discard either history. Stop for explicit recovery, fetch the remote change, then rebuild the authoritative Mac Studio managed state as a new validated commit on top of the remote history.

### 6. Duration grammar, defaults and limits

Durations use one whole number followed by one lowercase unit: `s`, `m`, `h` or `d`. Zero, decimals, uppercase units, unitless values, prose and compound durations are invalid.

| Field | Default | Minimum | Maximum | Additional rule |
| --- | ---: | ---: | ---: | --- |
| `check_interval` | `1m` | `10s` | `1h` | Must be greater than zero. |
| `settle_period` | `5m` | `1m` | `7d` | Must be at least `check_interval`. |
| `minimum_interval` | `1h` | `1m` | `30d` | Throttled mode only; must be at least `check_interval`. |

The normal default remains `publication.mode: "after_settle"`.

### 7. Deterministic fingerprint, atomic state and conservative time

The publisher must derive one deterministic SHA-256 fingerprint from a canonical, sorted manifest of the complete managed source. Each manifest entry represents the relative managed path, validated entry type and file-content identity required by the shared managed-scope contract. `.system/**`, `.DS_Store` and unrelated `.codex` content never participate.

Settlement state is repository-owned local operational metadata in one Git-ignored JSON receipt, not managed payload. The receipt must retain only the current operational memory needed for safe observation, settlement, mode eligibility and publication recovery, including the applicable fingerprints, quiet timing, last successful publication identity and exact pending-publication identity where one exists.

The receipt is self-maintaining and bounded:

- retain one current state file rather than timestamped history;
- write a complete temporary file and atomically replace the current receipt;
- clean or replace only the exact known temporary-write residue after interruption;
- clear obsolete pending fields after successful publication while retaining the last published fingerprint, SHA and timing identity;
- never perform broad cleanup outside the exact repository-owned runtime paths.

Git supplies permanent publication history; the local receipt supplies only current runtime memory.

Use monotonic elapsed time while the Mac Studio remains on the same boot. If the receipt is missing or corrupt, the boot changed, the clock relationship is anomalous, or elapsed quiet time cannot be proven, retain safety by restarting the full settlement period. No clock change may make content settle early or create a duplicate scheduled publication. Scheduled wall-clock decisions remain governed by `Europe/London`.

## Goal execution envelope

The future goal must follow Doc 3's phases and gates without turning this brief into a second implementation plan:

| Goal milestone | Doc 3 authority | Required outcome |
| --- | --- | --- |
| Safety and established Git checkout | Gates 0–1 | Reconfirm scope, current clean checkout, upstream, SSH path and remaining negative Git proofs. |
| Reproducible Python and rsync environment | Gates 2–4 | Build and prove repository-owned dependencies and tooling without Homebrew runtime ownership. |
| Configuration, scope and canonical snapshot | Gates 5–7 | Implement identity, config, exclusions, private candidate and validated `latest/`. |
| Publisher and Git publication | Gates 8–9 | Implement all four modes, Doc 7 derived surfaces, deterministic commits, atomic state and conservative recovery. |
| Consumer implementation and simulation | Gates 10–11 | Complete the consumer but exercise it only through isolated Mac Studio paths. |
| Real Mac Studio operation | Gate 12 | Install and prove only the publisher LaunchAgent through repository-owned runtime paths. |
| Durable operations and handoff | Gates 13–14 | Publish truthful permanent docs and a bounded, executable Mac mini handoff. |

Ordinary evidence-driven implementation details listed in Doc 3 may be resolved within the goal without returning a questionnaire. Architecture, authority, safety and scope boundaries may not be silently changed.

## Explicit authority boundary for the future goal

When the operator separately starts this goal, it may perform the in-scope repository and Mac Studio actions required by Doc 3 Gates 0–14, including repository edits, dependency resolution into repository-owned environments, rsync source retrieval/building under the tracked contract, test execution, normal development commits and pushes, private config creation, publisher LaunchAgent installation and authorised publisher validation.

That authority does not permit:

- modifying or deleting `~/.codex/skills/.system/**` or `.DS_Store` anywhere;
- treating `latest/`, ZIP artifacts or GitHub as an authoring source for the Mac Studio;
- activating the consumer on the Mac Studio;
- installing or validating anything on the real Mac mini;
- copying credentials between machines or publishing private configuration;
- force-pushing, rewriting unknown Git history or creating automatic tags/Releases;
- creating or deleting a live managed Codex canary solely for testing without a separate explicit checkpoint when that mutation becomes necessary.

Existing authoritative Mac Studio managed content may be read and ingested only through the documented bounded contract. Publisher operation must never rewrite the Mac Studio's live source.

## Deferred Mac mini goal

Doc 3 Phase 15 is a separate future goal executed on the real Mac mini after Gates 0–14 complete. Its objective will be to reconstruct the repository-owned environment, establish truthful consumer configuration, install only the consumer LaunchAgent, validate bounded deployment against the real Mac mini `.codex`, and contribute the resulting evidence and permitted consumer refinements back to the same repository.

Until then, the following remain explicitly unproven:

- Mac mini Git authentication and checkout behaviour;
- Mac mini Python, rsync, filesystem and launchd runtime behaviour;
- live Mac mini deployment, no-op and deletion handling;
- preservation of real Mac mini excluded and unrelated `.codex` state;
- the complete Mac Studio → GitHub → Mac mini end-to-end proof.

The Mac mini goal may refine consumer-specific implementation within the established extension boundary. It may not silently reverse authority, redefine managed scope, alter publisher behaviour, replace `latest/`, or weaken exclusions and deletion safety.

## Completion and stopping rules

The Mac Studio goal is complete only when every Doc 3 Gate 0–14 is proven, the publisher runs headlessly through launchd, the complete reusable repository is published, consumer simulation passes, permanent documentation reflects actual behaviour and the Phase 15 handoff is ready.

The goal must stop and report evidence under Doc 3's escalation conditions rather than redesigning around a material contradiction, unsafe path, unprovable dependency, irreconcilable Git state, failed safety gate or required authority outside this envelope.

Budget, elapsed time or implementation difficulty do not redefine completion. Phase 15 remains deferred by scope, not treated as a blocker to Mac Studio goal completion.

## Mode B validation record — 24 August 2026

At creation of this document:

- the working tree was clean before the Doc 9 addition;
- local `main`, `origin/main` and HEAD all resolved to `6f8c66a3de5d042c9616c22a97434c26e038815c`;
- the existing SSH remote was `git@github.com:YodaSpow/codex-config-manager.git`;
- Doc 3 contained Gates 0–14 for Mac Studio completion and Phase 15 for deferred real Mac mini validation;
- the exact approved YAML and all seven operator decisions were transferred from the current discussion into this repository-owned goal package;
- no implementation, dependency installation, Codex mutation, launchd mutation, commit or push occurred.
