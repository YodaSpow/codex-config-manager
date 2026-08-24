# Doc 5 — Implementation Discovery — Deterministic Managed-State Publication History

**Status:** Operator-approved publication-history contract; not yet implemented  
**Scope:** Headless GitHub visibility, managed-state commit semantics and deliberate project releases  
**Relationship to existing documents:** Standalone implementation discovery. Its eventual placement references in implementation and permanent operating documentation are deferred; no existing document is changed by this record.

## Status

- ✅ Codex Config Manager remains headless; no custom web UI is required for the initial system.
- ✅ GitHub is the selected human-facing visibility surface for published managed state, exact diffs, project documentation and deliberate releases.
- ✅ Routine managed-state publications and Codex Config Manager software releases are two different histories with different identities.
- ✅ Managed-state commit context is derived deterministically at the `AGENTS.md` and top-level user-skill component boundary, without AI interpretation.
- ✅ Git commit SHAs identify exact managed-state publications; automatic version tags are not created for them.
- ✅ Semantic-version tags and GitHub Releases are reserved for deliberate, evidence-gated Codex Config Manager milestones.
- ▶ Mode C must implement and test the deterministic publication summary when the publisher is built.
- ⛔ This document does not initialise Git, create tags or releases, alter GitHub, change existing documentation or implement any application behaviour.

## Purpose

Codex Config Manager is intended to operate robustly without an application portal. Its primary job is to preserve and transport the managed Codex state: the global `AGENTS.md` and dynamically discovered user-created skills. The public GitHub repository also provides a useful human lane: it can expose the orchestration and documentation, show the managed components that are publicly shareable, and provide an exact history of what the Mac Studio published.

A raw sequence of automatic commits would provide forensic diffs but weak immediate context. Conversely, interpreting the meaning of changed prose or skill instructions would require AI judgement and make an otherwise deterministic publisher non-deterministic. The selected middle layer is therefore component-level publication meaning:

- report that `AGENTS.md` was added, updated or removed;
- report that a named top-level user skill was added, updated or removed;
- retain Git's exact nested file diff for deeper inspection;
- never claim what the changed content means.

This gives every legitimate automated publication a concise and truthful reason while keeping the runtime fully headless.

## Three intended outcomes

The repository serves three related outcomes:

1. **Managed-state preservation:** capture the Mac Studio's managed Codex state in a validated, persistent and versioned repository representation.
2. **Machine-to-machine orchestration:** provide the later Mac mini consumer with the canonical published state through GitHub, without requiring a live connection to the Mac Studio.
3. **Public visibility:** provide a shareable view of the user's Codex orchestration, `AGENTS.md`, user skills and project documentation.

The first two outcomes govern correctness. Public visibility is valuable, but it must not broaden managed scope, weaken exclusions or turn presentation concerns into runtime authority.

## Headless visibility model

No bespoke website or local web portal is required for the initial implementation. The visibility surfaces are:

| Surface | Purpose |
| --- | --- |
| GitHub commit history | Chronological managed-state publication timeline and normal project-development history |
| GitHub commit detail and comparisons | Exact file-level and line-level forensic evidence |
| Deterministic managed-state commit messages | Immediate component-level explanation of an unattended publication |
| Repository documentation | Architecture, implementation contracts, operating guidance and human context |
| GitHub tags and Releases | Deliberate Codex Config Manager software milestones |
| CLI `status` and `validate` | Local role, health, last publication identity and validation evidence |
| GitHub Pages, if adopted later | Optional rendering of public documentation only; not runtime control |

This model avoids introducing another service that would need to be hosted, secured, updated, diagnosed and kept synchronized with the repository.

## Three distinct Git activities

The repository must distinguish these activities explicitly.

### 1. Managed-state publication

The unattended Mac Studio publisher may stage and commit only validated changes beneath:

```text
source/staging/**
```

Each successful non-no-op publication receives a deterministic component summary and is identified immutably by its Git commit SHA.

### 2. Project-development commit

Normal authorised human or AI work may change application code, tests, documentation and other appropriate public repository files. Such commits are not managed-state publications and are not constrained to the publisher's generated message format.

The Mac mini may later contribute authorised consumer documentation or implementation refinements through this project-development lane. That possibility does not give the Mac mini authority to act as the unattended managed-state publisher or redefine the Mac Studio source-of-truth direction.

### 3. Codex Config Manager release

A release represents a deliberate milestone in the manager's code, contracts or proven operating capability. It uses a human-approved semantic-version tag and, where useful, a GitHub Release. A routine `AGENTS.md` or user-skill update is not a software release.

## Two histories, two identities

| History | Meaning | Identity |
| --- | --- | --- |
| Managed-state publication history | The Mac Studio's managed Codex configuration changed | Full Git commit SHA; short SHA for display |
| Codex Config Manager release history | The project reached an approved implementation or compatibility milestone | Deliberate SemVer tag such as `v0.1.0` |

Automatic `v1`, `v2`, `v3` tags must not be created for routine managed-state publications. That would conflate configuration snapshots with software releases, create tag noise and obscure the meaning of a real project milestone.

The Git commit graph already provides ordered, immutable managed-state versions. The CLI may expose a short SHA for human readability, but stored receipts and machine comparisons should retain the full SHA.

## Deterministic derivation point

The component summary is derived from the validated Git index immediately before commit:

```text
checksum-aware rsync dry-run
        ↓
controlled staging update
        ↓
staging validation and post-sync equivalence
        ↓
stage the exact source/staging pathspec
        ↓
reject every indexed path outside source/staging
        ↓
inspect the staged before/after trees
        ↓
derive the component-level publication summary
        ↓
commit and push
```

The rsync comparison determines whether the managed filesystem representation differs and controls the bounded copy. The staged Git difference is the stronger source for publication context because it describes exactly what the proposed commit will publish, including legitimate deletions.

The summary must be generated only after staging validation and exact path-scoped Git staging. It must never be generated from unrestricted worktree changes.

## Semantic component boundary

The component mapping is fixed by managed topology:

| Staged path | Human-facing component |
| --- | --- |
| `source/staging/AGENTS.md` | `AGENTS.md` |
| `source/staging/skills/<skill-name>/**` | `<skill-name>` |

For skills, `<skill-name>` is the immediate child directory beneath `source/staging/skills/`. That directory is the semantic skill identity. Repeated internal filenames such as `SKILL.md`, references, scripts or assets are implementation detail and do not belong in the concise publication summary.

Nested paths still participate in exact comparison and Git's forensic diff. They are collapsed only for the human-facing component summary.

The mapping remains dynamic. It must not contain an allowlist of currently known user-skill names; a future user-created skill automatically obtains its identity from its top-level directory name.

## Exclusion boundary

Only content that has already passed the managed ingestion and staging contracts may participate in summary generation.

- `skills/.system/**` is outside managed state and must never appear as a component.
- `.DS_Store` is ignored noise and must never appear as a component or meaningful change.
- An unexpected path or forbidden staged path is a validation failure, not an item to describe and publish.

Summary generation is not a late exclusion mechanism. Excluded content must never enter the managed staged payload or Git index in the first place.

## Component action classification

The publisher must compare each component's presence in the published parent tree with its presence in the proposed index tree.

### `AGENTS.md`

- absent before, present after → **added**
- present before and after with a staged difference → **updated**
- present before, absent after → **removed**

### User-skill root

- top-level skill root absent before, present after → **added**
- top-level skill root present before and after with any nested difference → **updated**
- top-level skill root present before, absent after → **removed**

Classification must be based on component presence before and after, not merely on individual file status. Adding a new reference or script inside an existing skill updates that skill; it does not add a new skill.

Potential renames are conservatively represented as one removal and one addition unless a separate, explicit rename contract is approved later. The implementation should disable or avoid relying on Git's heuristic rename interpretation when deriving this summary.

## Deterministic ordering and message formation

Given the same staged before/after trees, the publisher must produce byte-for-byte equivalent semantic content.

Ordering is:

1. `AGENTS.md`, when changed;
2. user skills sorted by skill name;
3. within structured action groups: `added`, `updated`, then `removed`.

The subject uses the `managed-state:` prefix so managed publications remain recognizable among normal project-development commits. It may name a small number of components directly and must fall back to a stable component count when listing names would exceed the implementation's fixed subject-length rule. The body always carries the complete structured component list.

Example with two directly named component changes:

```text
managed-state: update AGENTS.md and operational-modes

AGENTS.md:
  updated

skills:
  updated:
    - operational-modes

publisher: MacStudio
```

Example with one changed skill:

```text
managed-state: update operational-modes

skills:
  updated:
    - operational-modes

publisher: MacStudio
```

Example when a concise subject cannot list every component:

```text
managed-state: publish 6 component changes

AGENTS.md:
  updated

skills:
  added:
    - new-user-skill
  updated:
    - operational-modes
    - semantic-compression
  removed:
    - retired-skill
    - superseded-skill

publisher: MacStudio
```

Mode C must select and test one fixed subject-length threshold and exact pluralization rules. These formatting mechanics must not alter the component mapping or action classifications defined here.

The `publisher` value is the validated configured machine identity used for that publisher run. In the initial architecture this is `MacStudio`. It is attribution, not permission: identity and role preflight must already have succeeded before the publication workflow reaches Git mutation.

## Deliberate semantic limit

The deterministic layer may truthfully state:

> `operational-modes` was updated.

It must not infer:

> The validation policy in Operational Modes became stricter.

The second statement requires understanding the changed content. Content interpretation by an AI, language model, keyword classifier or generated prose service is outside the unattended publication path. Git retains the exact nested diff for a human or AI to inspect separately when deeper meaning is required.

This limit is a feature: it makes automatic messages repeatable, auditable, private by construction and independent of external inference services.

## No-op and failure behaviour

- No meaningful validated staged difference means no commit, no push and no publication message.
- Summary generation failure means no commit and no push.
- An unknown managed topology, malformed path, forbidden component, unexpected indexed path or inconsistent before/after tree means safe failure.
- A commit failure or push failure must preserve sufficient non-secret local evidence for deterministic retry; it must not manufacture a second semantic event for the same staged state.
- A successful retry of the same pending publication must reproduce the same component summary.
- Legitimate deletion-only publications must receive a truthful summary and must not be suppressed as no-ops.

## Status and receipt visibility

The local read-only status surface should eventually report at least:

```text
Published state: 8f34c2a
Published by: MacStudio
Components changed: AGENTS.md, operational-modes
```

The short SHA is for display. Repository and runtime receipts should preserve the full commit SHA, publication result, timestamp, validated machine identity and deterministic component summary needed to diagnose or retry safely.

The Mac mini consumer can use the published commit SHA to establish which exact managed state it has validated or deployed. Consumer deployment does not generate a new managed-state publication commit merely because it consumed an existing one.

## Release policy

Codex Config Manager releases are deliberate rather than inferred. Automation may verify predetermined evidence gates and assemble known facts, but it must not decide that a change deserves a major, minor or patch version.

The initial milestone shape is:

```text
v0.1.0  Repository and reproducible environments established
v0.2.0  Mac Studio publisher validated
v0.3.0  Consumer simulation validated
v1.0.0  Mac Studio → Mac mini operation validated end to end
```

A tag or GitHub Release may be created only after the corresponding milestone has actually been implemented, validated and explicitly approved for release. Documentation intent alone is not release evidence.

The read-only remote tag query on 21 August 2026 established the pre-implementation baseline:

```text
remote_tag_ref_count=0
```

After `v1.0.0`:

- patch versions represent compatible fixes;
- minor versions represent backward-compatible capability additions;
- major versions represent breaking public contract or compatibility changes.

Release notes may use deterministic commit categories as evidence, but the release description should explain the project milestone rather than reproduce every managed-state publication.

## GitHub as the public portal

GitHub provides the initial public visibility needed by this project:

- the current managed `AGENTS.md` and user skills are directly browsable;
- component-oriented commit subjects make the timeline legible;
- exact diffs preserve the detail behind each signal;
- tags and Releases distinguish software milestones from configuration movement;
- repository documentation explains the orchestration and safety model;
- the repository can be shared as a public representation of the user's Codex setup.

GitHub Pages may later render selected documentation more accessibly, but it is not necessary for publisher or consumer operation and must never become a control plane.

## Deferred future representation lanes

A future project phase may explore a Claude-oriented representation of the public skills or instructions. Possible routes include derived guidance, explicit Claude variants or conversion instructions based on the canonical public Codex representation.

That work is intentionally deferred until the Codex-first repository, Mac Studio publisher and Mac mini consumer are operational and proven. This document does not define a Claude format, add another managed source, make cross-platform conversion automatic or authorise a second publisher. Any future representation must preserve a clear canonical source and must not destabilize the initial Codex managed-state contract.

## Mode C requirements

Mode C must:

- preserve the separate managed-publication, project-development and project-release lanes;
- stage the exact `source/staging/**` pathspec and prove no other indexed path can enter an unattended commit;
- derive publication context from the validated staged before/after trees;
- map `AGENTS.md` and dynamic top-level user-skill roots exactly as defined here;
- classify component addition, update and removal from component presence, including deletion-only changes;
- collapse nested skill paths to the top-level skill name for the message while retaining exact Git diffs;
- reject forbidden, malformed or unexpected paths rather than summarize them;
- produce deterministic ordering, subject formation, body formatting and publisher attribution;
- ensure no-op runs create no commit or message;
- ensure retry behaviour reproduces the same summary for the same pending state;
- store and expose the full publication SHA in receipts while using a short SHA only for human display;
- expose the last publication SHA, publisher identity and component summary through read-only status output;
- test initial addition, `AGENTS.md` update/removal, skill addition/update/removal, nested-file addition, multiple components, deletion-only publication, apparent rename, exclusions, malformed paths, no-op, failure and retry;
- keep SemVer tag and GitHub Release creation outside unattended managed-state publication;
- document the final implemented message grammar, receipt fields, status output and release procedure from real validation evidence.

## Current implementation status

- ✅ The purpose, semantic boundary, component mapping, history separation and headless visibility model are operator-approved.
- ✅ The GitHub remote was observed with no existing tags during the read-only discovery that preceded this record.
- ▶ Future Mode C must implement the deterministic publication summary and prove it against repository-local tests and real staged-state behaviour.
- ▶ Placement citations from the implementation plan and eventual permanent operating documentation remain a later documentation action; this record currently stands independently.
- ⛔ No publisher, semantic commit generator, status receipt, tag, GitHub Release or custom UI is established by this document.
