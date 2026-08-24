# Doc 1 — Implementation Discovery — Managed Skill Ingestion Exclusions

**Status:** Implemented and validated; retained as the discovery record for the exclusion contract. See [Doc 10](10-implementation-architecture-and-operations.md).
**Scope:** Managed-skill ingestion and transport boundaries  
**Relationship to bootstrap documents:** This record refines the managed-skills contract. It does not replace or modify either bootstrap document.  
**Architecture reconciliation:** [Doc 8 — Root-Level Latest Managed Snapshot](08-architecture-reconciliation-root-level-latest-managed-snapshot.md) replaces the historical planned staging path with root-level `latest/`.

## Verified rule

Codex Config Manager manages the global `AGENTS.md` file and dynamically discovered user-created skills, subject to two mandatory exclusions at the ingestion boundary.

### Codex-managed system skills

`~/.codex/skills/.system/**` is out of scope. This subtree contains Codex-managed system skills and must:

- never enter `latest/`;
- never be copied by publisher rsync;
- never be published to GitHub;
- never be deployed by a consumer;
- never be modified or deleted by Codex Config Manager.

The exclusion occurs at ingestion. Codex Config Manager must not copy the subtree into a private candidate or `latest/` and filter it later. Consequently, `latest/skills/` contains only managed user-skill content.

### Finder metadata

`.DS_Store` is globally ignored project noise wherever it appears. It must:

- never enter a managed candidate or `latest/`;
- never be copied as managed content;
- never be published;
- never be deployed;
- never be treated as a meaningful change;
- never be deliberately removed or otherwise managed by Codex Config Manager.

The eventual repository-wide `.gitignore` must prevent `.DS_Store` from entering Git without attempting to clean up or mutate existing `.DS_Store` files.

## Dynamic user-skill discovery

User-created skill names must not be hard-coded. All current and future user-created content directly beneath `~/.codex/skills/` participates automatically and recursively, except for the exclusions above.

```text
~/.codex/skills/
├── .system/                 EXCLUDED recursively
├── .DS_Store                EXCLUDED
├── current-user-skill/      INCLUDED recursively
└── future-user-skill/       INCLUDED automatically and recursively
```

## Consistency requirement

The same exclusion contract must apply to:

- cheap detection;
- rsync dry-run;
- real rsync;
- candidate and `latest/` validation;
- tests;
- Git publication;
- consumer validation;
- consumer deployment;
- deletion handling.

Deletion logic must never use `--delete-excluded`. This is a secondary defensive safeguard; the primary contract is that excluded content never enters the managed candidate or canonical `latest/` snapshot.

## Current implementation status

- ✅ The ingestion exclusions and dynamic user-skill discovery rule are verified and locked by operator direction.
- ▶ Future implementation must apply this contract consistently across publisher candidate construction, `latest/`, Git, consumer, tests, portable artifacts and deletion handling.
- ⛔ No implementation is established by this document.
