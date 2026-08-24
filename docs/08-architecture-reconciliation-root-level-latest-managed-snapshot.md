# Doc 8 — Architecture Reconciliation — Root-Level Latest Managed Snapshot

**Status:** Architecture implemented and validated through root-level `latest/`; retained as the reconciliation record. See [Doc 10](10-implementation-architecture-and-operations.md) and [Doc 11](11-validation-evidence-mac-studio.md).
**Decision date:** 24 August 2026  
**Scope:** Replace the planned tracked `source/staging/` path with root-level `latest/`, preserve the Mac Studio authority direction, define private candidate handling, derive `upload-ready/` from `latest/`, and reconcile active documentation  
**Historical boundary:** The two documents under `docs/bootstrap/` remain unchanged historical inputs. This document and the reconciled active Docs 1–7 govern the implementation path.  
**Related documents:** [Doc 1 — Managed-Skill Ingestion Exclusions](01-implementation-discovery-managed-skill-ingestion-exclusions.md) · [Doc 2 — Python Runtime and Environment Ownership](02-implementation-discovery-python-runtime-environment-ownership.md) · [Doc 3 — Mode C Implementation Plan](03-mode-c-implementation-plan.md) · [Doc 5 — Deterministic Publication History](05-implementation-discovery-deterministic-managed-state-publication-history.md) · [Doc 6 — Settled-State Publication Controls](06-implementation-discovery-settled-state-publication-controls.md) · [Doc 7 — Portable Distribution](07-implementation-discovery-portable-skills-zip-distribution.md)

## Status

- ✅ Root-level `latest/` replaces every planned active use of the tracked `source/staging/` repository payload.
- ✅ There is no second persistent staging mirror.
- ✅ The managed portion of the Mac Studio live `~/.codex` remains the sole authoring authority.
- ✅ `latest/` is the canonical unpacked repository snapshot and is never an authoring source on the Mac Studio.
- ✅ Private temporary candidate construction remains available as implementation machinery but is not a tracked or persistent mirror.
- ✅ `upload-ready/` is derived only from the validated `latest/` snapshot.
- ✅ The Mac mini validates and consumes `latest/`; it ignores `upload-ready/` during normal deployment.
- ✅ The repository-facing name now communicates that the content is current and consumable rather than unfinished.
- ✅ Git history remains the record of earlier snapshots; no timestamped or numbered `latest` directories are created.
- ✅ Docs 1, 2, 3, 5, 6 and 7 are the affected active records. Doc 4 is unaffected.
- ✅ Byte-identical pre-reconciliation snapshots of every affected active document are preserved under `docs/history/`.
- ▶ Mode C must implement and prove the phases and gates in this document together with the reconciled Doc 3 plan.
- ⛔ This Mode B reconciliation does not create `latest/`, migrate files, initialise Git, build Python code, generate ZIPs, alter configuration, install launchd or touch live Codex state.

## Decision and rationale

The previously planned name `source/staging/` was technically meaningful from the publisher's internal perspective but misleading at the public repository boundary. On GitHub, “staging” implies incomplete or not-yet-ready content. The tracked payload is intended to be the current validated representation available for inspection and Mac mini consumption.

The locked topology is therefore:

```text
Mac Studio authoritative managed ~/.codex state
        ↓
private temporary candidate and validation
        ↓
latest/                              canonical unpacked repository snapshot
├── AGENTS.md
└── skills/
    └── <dynamic user-skill directories>
        ↓
upload-ready/                        derived human-download artifacts
├── global-agents.zip
└── skills/
    └── <dynamic per-skill ZIPs>
```

The path change is semantic as well as cosmetic:

- `latest/` describes the role of the tracked content to repository readers and consumers.
- Private candidate construction describes the internal pre-validation operation.
- Git index staging remains ordinary Git terminology and is not renamed.
- “Settled source,” “candidate,” “latest snapshot,” “Git-staged diff” and “published commit” remain distinct states.

## Rejected dual-mirror model

The project must not implement:

```text
source/staging/
        ↓
latest/
        ↓
upload-ready/
```

Two persistent payload mirrors would add another synchronization boundary, duplicate deletion semantics and create uncertainty about which tree the Mac mini consumes. Only `latest/` is tracked canonical managed payload.

Temporary candidate state is permitted only as bounded implementation machinery. It must be:

- created in a private repository-local ignored runtime area or secure system temporary directory selected by the implementation contract;
- unique to one attempted publication transaction;
- inaccessible as a public or consumer source;
- validated before it can replace `latest/`;
- safely disposable after success or failure;
- incapable of surviving as a second authoritative mirror;
- excluded from Git, managed-change summaries and download generation.

## Meaning of `latest/` at each boundary

### Mac Studio working tree

`latest/` is the most recent validated managed snapshot prepared for repository publication. It may temporarily be ahead of GitHub while a commit or push is pending, but Doc 5 retry state must preserve the exact snapshot associated with that pending commit.

It is never read back into the Mac Studio live `~/.codex` during ordinary publishing. Recovery from repository state is a separate human-authorised operation.

### GitHub

Within each visible commit, `latest/` is the latest successfully committed snapshot for that commit and branch. The repository default branch exposes the most recently pushed successful snapshot. Git history supplies earlier states.

### Mac mini

After a safe Git update, `latest/` is the candidate repository snapshot the Mac mini validates before bounded deployment. A failed validation leaves live Mac mini managed state unchanged.

### Human download lane

`upload-ready/` is a deterministic projection of the same commit's `latest/`. It cannot be newer, older or independently authored. The README view link targets `latest/AGENTS.md`; download links target the matching `upload-ready/` artifacts.

## Locked repository topology

```text
codex-config-manager/
├── latest/
│   ├── AGENTS.md                         present only when authoritative source contains it
│   └── skills/
│       └── <dynamic managed user skills>
├── upload-ready/
│   ├── global-agents.zip
│   └── skills/
│       └── <dynamic skill-name>.zip
├── src/
├── tests/
├── tooling/
├── docs/
├── config.yaml.example
├── pyproject.toml
└── README.md
```

There is no tracked `source/` container merely to hold the managed snapshot. If later implementation finds a separate `source/` purpose, that is a new architecture decision and cannot silently recreate `source/staging/`.

## Authority and exclusions

The source direction remains one-way:

```text
Mac Studio managed ~/.codex
        → private candidate
        → latest/
        → GitHub
        → Mac mini
```

Doc 1's ingestion boundary is unchanged in substance:

- `~/.codex/skills/.system/**` never enters the private candidate or `latest/`;
- `.DS_Store` never enters the private candidate, `latest/`, `upload-ready/` or Git;
- future top-level user-skill directories remain dynamically discovered;
- excluded live content is never cleaned, modified or deleted;
- deletion logic never uses `--delete-excluded`.

The primary contract is now stated as:

> Excluded content never enters the managed candidate or canonical `latest/` snapshot.

## Snapshot transition contract

The publisher must distinguish five states:

```text
1. observed live source state
2. settled and mode-eligible source state
3. private validated candidate
4. validated canonical latest/ working-tree snapshot
5. committed and pushed published snapshot
```

No state may be silently treated as another:

- Detection and settlement do not mutate the private candidate or `latest/`.
- Candidate validation must complete before `latest/` mutation.
- `latest/` and derived artifacts must be reconciled as one working-tree transaction.
- Git path validation and commit must complete before a state is considered locally published.
- Push success must complete before GitHub is reported current.
- Push retry preserves the exact existing commit and corresponding `latest/`, artifacts and README state.

## Derived distribution contract

Doc 7 remains authoritative for portable artifacts, with these reconciled source paths:

```text
latest/AGENTS.md
        → upload-ready/global-agents.zip

latest/skills/<skill-name>/
        → upload-ready/skills/<skill-name>.zip
```

The root README surface becomes:

```markdown
- [View the current global - AGENTS.md](latest/AGENTS.md)
- [Download the current global - AGENTS.md](upload-ready/global-agents.zip)
```

Skill download entries continue to mirror the dynamic immediate child-directory set under `latest/skills/`.

## Git publication boundary

The canonical managed allowlist changes from the historical planned path to:

```text
latest/**
upload-ready/global-agents.zip
upload-ready/skills/<validated dynamic ZIP set>
README.md                              bounded generated download section only
```

Git index staging remains a later operation over these exact validated paths. The publisher must never generalise this to `git add .`, `git add -A` without path constraints, or an unvalidated `upload-ready/**` wildcard.

The semantic `ManagedChangeSet` remains derived from canonical `latest/` before/after component state, not from ZIP bytes, README churn, temporary candidates or unrestricted working-tree changes.

## Mode C implementation plan

Mode C must execute this plan only when separately authorised. Each gate is blocking; failure leaves the prior coherent published state intact or enters the exact Doc 5 retry state.

### Phase 1 — Establish governing paths and terminology

1. Define one repository-root resolver for `latest/`.
2. Remove all implementation assumptions about `source/staging/`.
3. Define separately named private candidate and Git-index concepts so “staging” cannot become ambiguous.
4. Ensure config exposes operator choices only; locked repository paths should remain code/document contracts unless a genuine deployment need requires configuration.

**Gate 1:** Repository code and templates contain no active `source/staging/` path, and every `latest/` reference resolves beneath the repository root.

### Phase 2 — Build private candidate state

1. Observe and settle the authoritative managed Mac Studio source under Doc 6.
2. Create a fresh private candidate location for one transaction.
3. Ingest `AGENTS.md` if present and dynamically discovered user-skill directories.
4. Apply Doc 1 exclusions at ingestion.
5. Detect source mutation during candidate creation and fail safely.

**Gate 2:** Candidate contents are a complete, bounded representation of the settled managed source; `.system/**` and `.DS_Store` are absent without being mutated live.

### Phase 3 — Validate candidate before canonical mutation

1. Validate containment, entry types, symlink policy, case collisions and structural invariants.
2. Confirm `skills/` contains only eligible dynamic immediate child directories.
3. Run checksum equivalence against the settled source under identical exclusions.
4. Prove no repository, runtime or excluded metadata entered the candidate.

**Gate 3:** Invalid or unstable candidate state cannot modify `latest/`, Git index, artifacts or README.

### Phase 4 — Reconcile root-level `latest/`

1. Calculate the exact managed before/after transition.
2. Apply additions, updates and bounded deletions to `latest/` using the repository-owned rsync contract or an equivalently proven mechanism.
3. Never use `--delete-excluded`.
4. Validate post-reconciliation equivalence between the candidate and `latest/`.
5. Preserve unrelated repository paths and reject unexpected content inside the managed boundary.

**Gate 4:** `latest/` exactly represents the validated candidate, repeated no-op runs produce no writes, and no second persistent mirror exists.

### Phase 5 — Derive portable artifacts and README

1. Build deterministic `global-agents.zip` from `latest/AGENTS.md` when present.
2. Build one deterministic wrapped ZIP per dynamic directory under `latest/skills/`.
3. Reconcile artifact additions, stable replacements and bounded deletions.
4. Reconcile only the managed README view/download section.
5. Validate `latest/` ↔ artifacts ↔ README membership and content equivalence.

**Gate 5:** No artifact or README state can be independently authored, stale, missing or ahead of `latest/`.

### Phase 6 — Git validation, commit and retry

1. Validate branch, remote, authentication, divergence and pre-existing worktree/index state.
2. Stage exact approved `latest/`, artifact and bounded README paths including deletions.
3. Reject every indexed path outside the approved transaction.
4. Derive one deterministic semantic change set from canonical managed components.
5. Commit once and push once under Doc 5.
6. Preserve the exact commit and its matching files for deterministic retry after push failure.

**Gate 6:** The proposed commit contains one coherent canonical and derived state, and GitHub success is never claimed before push confirmation.

### Phase 7 — Mac mini consumption

1. Update the Mac mini repository through the approved Git route.
2. Validate `latest/` before touching live managed targets.
3. Compare and deploy only `latest/AGENTS.md` and `latest/skills/` managed content.
4. Ignore `upload-ready/`, README and private publisher runtime state.
5. Verify live post-deployment equivalence and preserve unmanaged/excluded content.

**Gate 7:** The Mac mini consumes only validated `latest/`; failure leaves its prior live managed state intact.

### Phase 8 — Automated tests

Tests must cover:

- absence of any active `source/staging/` implementation path;
- root containment for `latest/` and private candidates;
- initial population, update, deletion and repeated no-op;
- source mutation during candidate creation;
- candidate failure before `latest/` mutation;
- `.system/**`, `.DS_Store` and `--delete-excluded` safeguards;
- future user-skill discovery without an allowlist;
- atomic `latest/` and derived-state equivalence;
- unrelated worktree and Git-index rejection;
- push failure and exact retry preservation;
- Mac mini validation and deployment from `latest/` only;
- README view path and portable download membership;
- repository-level search proving no unintended active staging-path contract remains.

**Gate 8:** Targeted and full repository test suites pass through the repository-owned Python environment with decisive summaries captured.

### Phase 9 — Real end-to-end verification

On the Mac Studio, prove:

1. no-op source produces no candidate promotion, artifact churn, commit or push;
2. a controlled managed change settles, reaches `latest/`, derives matching downloads, commits and pushes;
3. excluded live content remains untouched and absent from Git;
4. status and receipt surfaces distinguish pending, locally committed, pushed and failed states.

On the Mac mini, prove:

1. the pushed commit is fetched through the approved route;
2. `latest/` validates before deployment;
3. additions, updates and bounded deletions apply correctly;
4. excluded and unmanaged sentinels remain unchanged;
5. `upload-ready/` is ignored.

**Gate 9:** Both machines prove the complete authority direction without a persistent staging mirror or live cross-machine dependency.

### Phase 10 — Documentation and release audit

1. Update operational documentation from planned to implemented state using real evidence.
2. Confirm README links against the real GitHub remote and default branch.
3. Record exact runtime, test, launchd and recovery commands.
4. Audit code, config, tests, templates and active docs for obsolete path terminology.
5. Retain bootstrap and pre-reconciliation history without presenting it as current authority.

**Gate 10:** A new operator or AI can identify authority, current paths, validation commands and recovery boundaries without relying on chat history.

## Documentation reconciliation executed by this Mode B pass

The active documentation impact is intentionally bounded:

| Document | Reconciliation |
| --- | --- |
| Doc 1 | Rename managed ingestion destination and primary exclusion invariant to `latest/` |
| Doc 2 | Reconcile Python topology, entry-point responsibilities and implementation order |
| Doc 3 | Replace tracked staging topology and phases with private candidate → root `latest/` semantics |
| Doc 4 | No change; machine identity is independent of repository payload naming |
| Doc 5 | Reconcile canonical path allowlist and semantic change-set inputs while retaining Git-index staging terminology |
| Doc 6 | Preserve settlement semantics while replacing mutation of persistent staging with promotion to `latest/` |
| Doc 7 | Derive ZIPs and README view links from `latest/` rather than `source/staging/` |
| Bootstrap Docs 1–2 | No change; historical namespace retained |

Protected pre-reconciliation snapshots use:

```text
docs/history/<active-document-stem>-pre-doc-08-reconciliation-2026-08-24.md
```

They must remain byte-identical to the active sources captured before this pass and must never be bulk-rewritten during terminology audits.

## Documentation validation gates

The Mode B reconciliation is complete only when all checks pass:

1. Every affected pre-reconciliation snapshot exists and matches its recorded source hash.
2. Doc 4 and both bootstrap documents retain their pre-pass hashes.
3. Active Docs 1, 2, 3, 5, 6, 7 and 8 agree on root-level `latest/`.
4. No active document retains `source/staging/` as current architecture.
5. Any remaining word “staging” in active docs refers clearly to Git-index staging, historical language or private candidate discussion—not a persistent repository mirror.
6. `latest/` is never described as Mac Studio authoring authority.
7. `upload-ready/` is always derived from validated `latest/` and ignored by the Mac mini consumer.
8. Doc 1 exclusions remain ingestion-boundary rules and future user skills remain dynamic.
9. Doc 5 retry and semantic-summary contracts remain intact.
10. No application, README, Git, configuration, launchd or live Codex state changed.

## Mode B reconciliation validation — 24 August 2026

The protected snapshots were created before active edits and then compared with their recorded pre-edit hashes:

| Protected snapshot | SHA-256 | Match |
| --- | --- | --- |
| Doc 1 pre-Doc-8 | `2146529d3bc8d9487bceaf191d68d6a4f4f97e71c08bb7706665d03fc1ecf006` | byte-identical |
| Doc 2 pre-Doc-8 | `f50bf21c4bb33670ed1004856e47653d5c398243cbf2d63be6e6380fbd1bbe2e` | byte-identical |
| Doc 3 pre-Doc-8 | `2f89be10a976c2fb5686bec9ce756c2608aa7bf0105a21d53e6590952c01c55f` | byte-identical |
| Doc 5 pre-Doc-8 | `54124e41d6b8509461ba324086b3b3460b0dcb806f2fd9d79a0361a574356243` | byte-identical |
| Doc 6 pre-Doc-8 | `ca5c987ef8e93a9914d9bf4c613aff9c19d1f31bcbd9bb9d8bbb8fc4e4a487bb` | byte-identical |
| Doc 7 pre-Doc-8 | `2fa61a7ba7482bf430d4d1e18e2a75c49c1f05bfe8cd570110a7ba318b3965f7` | byte-identical |

The reconciled active documents produced:

| Active document | Post-reconciliation SHA-256 |
| --- | --- |
| Doc 1 | `21429af9dc59abfb3a846448da028e8d29633c56fdfbeb455fde06545a485220` |
| Doc 2 | `a2d31543688c6dbd5553b7946781fdf02dfe23ff37253df6d4af1d22e09fc401` |
| Doc 3 | `bbf9766b7e346fea6cb45c66842651b7d9a0ab5cb3ca11b078105d01017cff79` |
| Doc 4 — intentionally unchanged | `0eeca5ef99363a65673e0dcbabe0fbe971c8858c034c8bd40cd35b0db91ee38a` |
| Doc 5 | `0c873346e850240964bb1422806c9c7bad4e6a57a6cd2e5bcb8b1a41c7172f92` |
| Doc 6 | `de855da02631b6c84c7ce3ad959c97920411303faaf983b2430458d3e1895722` |
| Doc 7 | `787abc8ad3a4487b8c927cb192249395e6a68ae3030064c96af6d4966ada885a` |

The two untouched bootstrap documents retained these hashes:

```text
bootstrap/01  f01e7235408d3fc0dd1edbad3814f7ea25114b318165f6e47b1d7b8b1558dd8e
bootstrap/02  55d45fda1e2b03b061851f477f12918a2cb147fa88af3717bf0fe9b51ab8241d
```

The completed structural and terminology audit reported:

```text
obsolete current source/staging path hits in active Docs 1–7: 0
obsolete persistent-staging contract hits in active Docs 1–7: 0
stale future-reconciliation status hits in active Docs 1–8: 0
broken internal documentation links in active Docs 1–8: 0
active documents with unbalanced fenced-code markers: 0
active documents without exactly one H1 heading: 0
protected pre-Doc-8 snapshot hash mismatches: 0
```

Remaining “staging” or “staged” language was inspected individually. Outside Doc 8's explicit historical/rejected-path discussion, it now refers to Git-index staging, staged Git differences or the historical path replacement—not a second persistent repository mirror.

## Current implementation status

- ✅ The `latest/` architecture decision and rationale are locked.
- ✅ The dual persistent-mirror model is explicitly rejected.
- ✅ Private candidate, canonical snapshot, Git-index and published states are distinct.
- ✅ The complete Mode C implementation and verification path is defined.
- ✅ The affected active documents are reconciled, their protected snapshots remain intact, and cross-document validation is recorded.
- ▶ Mode C remains separately gated and unauthorised.
- ⛔ No repository implementation or runtime state exists merely because this document defines it.
