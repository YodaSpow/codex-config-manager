# Doc 7 — Implementation Discovery — Portable Global Guidance and Per-Skill ZIP Distribution

**Status:** Operator-approved distribution contract; ChatGPT one-skill ZIP wrapper proven through the real web uploader; repository integration remains unimplemented  
**Scope:** Derived `global-agents.zip`, dynamically generated per-skill ZIPs, bounded README download reconciliation, deterministic packaging, Git publication and human transfer  
**Relationship to existing documents:** This record defines a derived public download surface alongside canonical unpacked staging. It does not replace Docs 3, 5 or 6, change the Mac Studio or Mac mini authority model, or authorise implementation.  
**Related documents:** [Doc 1 — Managed-Skill Ingestion Exclusions](01-implementation-discovery-managed-skill-ingestion-exclusions.md) · [Doc 3 — Mode C Implementation Plan](03-mode-c-implementation-plan.md) · [Doc 5 — Deterministic Managed-State Publication History](05-implementation-discovery-deterministic-managed-state-publication-history.md) · [Doc 6 — Settled-State Publication Controls](06-implementation-discovery-settled-state-publication-controls.md)

## Status

- ✅ Canonical `source/staging/` remains the unpacked repository representation used by the Mac Studio publisher and Mac mini consumer.
- ✅ The portable distribution boundary is `upload-ready/`; it is derived from successfully settled and validated staging and is never an independent source of truth.
- ✅ The aggregate `NIC-codex-skills.zip` proposal is rejected. There is no ZIP-of-ZIPs and no single aggregate skills archive.
- ✅ ChatGPT web has accepted a ZIP containing exactly one wrapped skill directory and created the corresponding skill under **Created by me**.
- ✅ Each top-level staged user-skill directory maps dynamically to one stable ZIP with the same basename under `upload-ready/skills/`.
- ✅ The global `AGENTS.md` remains canonically named `AGENTS.md` and is separately packaged as `upload-ready/global-agents.zip`.
- ✅ The root README provides a view link to canonical staged `AGENTS.md`, a download link to `global-agents.zip`, and one dynamically reconciled download entry per current skill ZIP.
- ✅ Skill additions, updates and deletions must reconcile staging, ZIP artifacts and README membership as one coherent publication state.
- ✅ `.system/**`, `.DS_Store`, macOS archive metadata and unrelated `.codex` content never enter staging or any portable artifact.
- ▶ The exact GitHub direct-download URL form must be tested after the remote repository identity and default branch exist; visible README labels and repository artifact paths are already locked.
- ▶ Re-upload/update behaviour for an existing ChatGPT-created skill remains unverified and does not block the packaging layout.
- ▶ Docs 3 and 5 require a later protected Mode B reconciliation before their unattended Git allowlists can include `upload-ready/` and the bounded README section.
- ⛔ No ZIP, `upload-ready/` directory, README, code, configuration, Git state, launchd state, ChatGPT automation or Codex managed state has been created or modified by this document.

## Purpose

The core project direction remains:

```text
Mac Studio authoritative ~/.codex managed state
        ↓
settled and validated source/staging state
        ↓
GitHub canonical published repository
        ↓
Mac mini bounded consumer
```

The additional distribution lane makes the same published state easy for a person to inspect and download without introducing marketplace/plugin infrastructure or changing the machine-to-machine consumer:

```text
canonical unpacked staging
        ↓
deterministic portable artifacts
        ↓
README view/download surface
        ↓
human-controlled download and transfer
```

The intended external use includes uploading individual skills into a separate ChatGPT account operating under a different account, network and administrative boundary. Codex Config Manager does not authenticate to, automate or manage that account. The transfer remains a deliberate human action.

## Canonical and derived authority

The complete authority rule is:

```text
source/staging/AGENTS.md
        → upload-ready/global-agents.zip

source/staging/skills/<skill-name>/
        → upload-ready/skills/<skill-name>.zip

validated artifact membership
        → bounded README download entries
```

`source/staging/` is canonical. `upload-ready/` and the README download list are deterministic projections of that canonical state.

Portable artifacts and README entries must never:

- become authoring sources;
- determine which managed files or skills exist;
- repair or repopulate staging;
- preserve a skill absent from canonical staging;
- conceal a mismatch with the same commit's staged source;
- be deployed by the Mac mini consumer;
- introduce renamed or semantically edited copies of managed content.

If staging, artifacts and README membership disagree, publication must fail. The publisher repairs derived state only by rebuilding it from validated staging; it never changes staging to match an artifact or README entry.

## Verified ChatGPT ZIP evidence

### Operator test — 24 August 2026

The operator tested `semantic-compression.zip` through the real ChatGPT web **Upload a skill** surface. The supplied UI evidence showed:

```text
Upload a skill
Drag and drop a .zip/.skill file or SKILL.md to upload
semantic-compression.zip
```

The upload was accepted, and ChatGPT displayed the resulting skill under:

```text
Created by me
Semantic Compression (Mode T)
Compress without losing meaning
```

The operator's source evidence was:

```text
/Users/spowart/Scripts/codex-guidance/TEST
.: 
chat-handoff.zip       semantic-compression
operational-modes.zip semantic-compression.zip

./semantic-compression:
SKILL.md  agents

./semantic-compression/agents:
openai.yaml
```

The operator confirmed that the accepted archive used the wrapped-directory form:

```text
semantic-compression.zip
└── semantic-compression/
    ├── SKILL.md
    └── agents/
        └── openai.yaml
```

This proves the required packaging form for the tested ChatGPT web surface: one ZIP represents one skill, and that ZIP contains the named skill directory as its single top-level wrapper. It also proves acceptance of recursively packaged supporting content in the tested skill.

The test does not yet prove whether re-uploading a later archive updates, duplicates or rejects an existing **Created by me** skill. The UI also showed a separately **Installed** copy of Semantic Compression, so the upload created a distinct user-owned entry rather than replacing that installed copy.

### Supporting official evidence

The OpenAI Skills API documents creation of one skill from a directory upload or a single ZIP file:

```text
Skill files to upload (directory upload) or a single zip file.
```

Source: [OpenAI API Reference — Create a new skill](https://developers.openai.com/api/reference/go/resources/skills/methods/create).

The operator's real web test is the decisive evidence for this project's archive layout. The API reference remains supporting context rather than a substitute for that test.

## Locked repository surfaces

The planned topology is:

```text
codex-config-manager/
├── source/
│   └── staging/
│       ├── AGENTS.md
│       └── skills/
│           ├── chat-handoff/
│           ├── operational-modes/
│           ├── semantic-compression/
│           └── <future user-skill>/
├── upload-ready/
│   ├── global-agents.zip
│   └── skills/
│       ├── chat-handoff.zip
│       ├── operational-modes.zip
│       ├── semantic-compression.zip
│       └── <future-user-skill>.zip
└── README.md
```

The three named skills are the currently observed examples, not an allowlist. The implementation must discover all eligible immediate child directories beneath `source/staging/skills/` dynamically.

There must be no active artifacts such as:

```text
NIC-codex-skills.zip
skills.zip
skills-of-zips.zip
chat-handoff-v2.zip
operational-modes-2026-08-24.zip
semantic-compression-003.zip
```

Stable paths represent current state; Git history represents historical state.

## Global `AGENTS.md` portable contract

The source remains exactly:

```text
source/staging/AGENTS.md
```

Its portable artifact is:

```text
upload-ready/global-agents.zip
└── AGENTS.md
```

The archive name communicates that this is the global Codex guidance package. The file inside must remain exactly `AGENTS.md`; it must not be renamed to `global.md`, `global-agents.md`, `globalagents.md.md` or another distribution-oriented filename.

The archive contains `AGENTS.md` directly at its root. It must not add an unnecessary wrapper:

```text
global-agents.zip
└── global-agents/
    └── AGENTS.md
```

This preserves the installation target:

```text
~/.codex/AGENTS.md
```

The ZIP is a download convenience only. It does not authorise Codex Config Manager to modify the live global file during publishing or to deploy it anywhere other than through the separately governed Mac mini consumer contract.

If canonical staged `AGENTS.md` is absent, `global-agents.zip` and its README download entry must be absent. The README view entry must not point knowingly to a nonexistent staged file.

## Per-skill portable contract

For every eligible top-level directory:

```text
source/staging/skills/<skill-name>/
```

the publisher derives exactly:

```text
upload-ready/skills/<skill-name>.zip
└── <skill-name>/
    ├── SKILL.md
    └── <all other eligible skill content recursively>
```

The artifact basename and wrapper directory must match the staged parent-directory name exactly. The publisher must not infer names from `SKILL.md` display metadata, convert names to titles, apply a branding prefix or hard-code the currently observed skills.

The one-to-one membership invariant is:

```text
set(source/staging/skills/<eligible immediate child directory names>)
    = set(upload-ready/skills/<ZIP basenames>)
    = set(README skill download identities)
```

Every ZIP contains one and only one top-level skill wrapper. There is no aggregate archive and no nesting of ZIP files inside another ZIP.

## Exclusion boundary

Doc 1 remains authoritative: exclusions happen at ingestion, before managed staging exists.

Therefore neither artifact builder receives:

- `skills/.system/**` recursively;
- `.DS_Store` anywhere.

Portable packaging additionally rejects:

- `__MACOSX/` metadata;
- AppleDouble `._*` entries;
- Finder attributes or unrelated extended metadata;
- absolute paths or `..` traversal members;
- duplicate or case-colliding archive members;
- repository files, docs, config, receipts, logs or Git metadata;
- unrelated `.codex` content;
- temporary build files or prior ZIP artifacts.

Codex Config Manager must never remove, clean or mutate excluded live `.system/**` or `.DS_Store` content. Artifact validation confirms only that excluded material is absent from managed outputs.

## README distribution surface

The root README must provide two distinct human lanes:

- **View** canonical unpacked global guidance through GitHub's Markdown file view.
- **Download** current portable artifacts from `upload-ready/`.

The intended surface is:

```markdown
## Global AGENTS.md

The global `AGENTS.md` contains guidance intended for the user’s global
Codex environment.

- [View the current global - AGENTS.md](source/staging/AGENTS.md)
- [Download the current global - AGENTS.md](upload-ready/global-agents.zip)

## Skills

Each download contains one complete user-managed skill.

- [Download chat-handoff](upload-ready/skills/chat-handoff.zip)
- [Download operational-modes](upload-ready/skills/operational-modes.zip)
- [Download semantic-compression](upload-ready/skills/semantic-compression.zip)
```

The visible global-guidance labels deliberately use `global - AGENTS.md`, while the canonical filename remains `AGENTS.md` and the artifact remains `global-agents.zip`.

On GitHub, the relative `.md` link opens the normal Markdown file page, which provides rendered preview and raw/source access. The ZIP download links may require GitHub's direct raw/download URL form to produce immediate browser download rather than first opening a repository file page. Their final URL form must be tested after the remote owner, repository name and default branch are known; this does not change the locked visible labels or artifact paths.

### Bounded README reconciliation

The application must own only a clearly bounded generated download section, not overwrite or regenerate the entire human-authored README. The eventual implementation should use unambiguous managed-section boundaries or an equivalently safe structural mechanism.

The bounded section follows canonical artifact reality:

| Canonical change | Artifact effect | README effect |
| --- | --- | --- |
| `AGENTS.md` added | Create `global-agents.zip` | Add view and download entries |
| `AGENTS.md` updated | Replace `global-agents.zip` | No link change |
| `AGENTS.md` removed | Remove `global-agents.zip` | Remove view and download entries |
| Skill added | Create `<skill-name>.zip` | Add one skill download entry |
| Skill updated | Replace `<skill-name>.zip` | No link change |
| Skill removed | Remove `<skill-name>.zip` | Remove its download entry |
| No canonical change | No artifact change | No README change |

Skill entries must be generated from the validated dynamic skill set in stable lexicographic order. README membership is never an input for deciding what to retain or delete.

## Deterministic ZIP contract

The same canonical staged input and packaging-contract version must produce byte-identical ZIP bytes. Otherwise a no-op publisher run could create meaningless binary Git churn.

Mode C must establish and test:

- stable lexicographic member ordering;
- stable UTF-8 filename and `/` path handling;
- one chosen compression method and level;
- normalized ZIP timestamps valid for the format;
- normalized safe permission/external-attribute representation;
- explicit directory-entry treatment;
- no absolute or traversal paths;
- no duplicate or case-colliding names;
- no host-specific owner, group, source path or macOS metadata;
- explicit supported symlink behaviour;
- bounded file count, member size, total uncompressed size and compression ratio;
- a tracked packaging-contract version so intentional future byte changes are distinguishable from nondeterminism.

Each artifact must be built in a private temporary location, validated completely and atomically replace only its corresponding active path after success. A failure must preserve the previous coherent published repository state and prevent a commit claiming the newer canonical state.

## Artifact validation

Before Git staging, validation must prove:

1. `global-agents.zip` contains exactly one root member named `AGENTS.md` whose bytes equal `source/staging/AGENTS.md`.
2. Every skill ZIP basename equals one eligible staged skill-directory name.
3. Every skill ZIP contains exactly one matching wrapper directory and the complete eligible staged subtree beneath it.
4. No expected ZIP is missing, and no stale or unexpected managed ZIP remains.
5. README view/download membership equals the validated artifact set.
6. Excluded and unsafe members are absent.
7. Rebuilding unchanged input produces byte-identical archives.
8. Atomic replacement occurs only after every relevant check succeeds.

Validation must list members without unsafe extraction, reject invalid paths, and—where equivalence requires extraction—use an isolated temporary directory and traversal-safe implementation. Successfully opening an archive is not sufficient proof.

## Settled update and atomic publication flow

Doc 6 eligibility remains upstream. No staging, ZIP or README mutation occurs for merely observed, unsettled, paused, scheduled-held or throttled-held source state.

```text
managed source settles
        ↓
Doc 6 publication mode becomes eligible
        ↓
bounded rsync updates source/staging
        ↓
canonical staging validation succeeds
        ↓
derive expected global and per-skill artifact set
        ↓
build changed/new artifacts in private temporary state
        ↓
reconcile bounded stale artifact deletions
        ↓
reconcile bounded README download membership
        ↓
validate canonical ↔ artifacts ↔ README equivalence
        ↓
atomically publish the coherent working-tree result
        ↓
stage exact canonical, artifact and README pathspecs
        ↓
derive Doc 5 ManagedChangeSet from canonical staged paths
        ↓
commit and push one coherent repository state
```

The commit must never contain only part of a required projection. A known already-created but unpushed commit retains its exact matching artifacts and README during Doc 5 retry; they must not be rebuilt from newer live source state.

## Addition, replacement and deletion semantics

Artifact reconciliation is desired-state reconciliation over manager-owned paths, not broad filesystem deletion.

- A newly staged skill creates exactly one corresponding ZIP and README entry.
- A changed staged skill atomically replaces its same stable ZIP; no numbered or timestamped copy remains.
- A removed staged skill removes only its corresponding managed ZIP and README entry.
- A changed `AGENTS.md` atomically replaces `global-agents.zip` without changing its README path.
- A removed `AGENTS.md` removes only `global-agents.zip` and its two bounded README entries.
- A no-op canonical state must leave artifact bytes and README bytes unchanged.

Deletion must be calculated from the validated before/after canonical managed set and constrained to known manager-owned artifact paths. It must not use `--delete-excluded`, derive deletions from excluded content, recursively clear `upload-ready/`, or touch an unexpected file merely because it occupies that directory.

## Git publication boundary

The existing unattended contract permits only:

```text
source/staging/**
```

The planned distribution lane requires a later explicit allowlist reconciliation conceptually covering:

```text
source/staging/**
upload-ready/global-agents.zip
upload-ready/skills/<validated dynamic skill ZIP set>
README.md                     bounded generated download section only
```

Dynamic ZIP membership is acceptable only because every allowed artifact must correspond one-to-one with a validated top-level staged skill. It is not permission for:

```text
git add .
git add upload-ready/**
unbounded README rewriting
```

The application must reject unexpected Git paths or unrelated working-tree changes rather than staging them. Docs 3 and 5 must be reconciled before Mode C because this changes the paths the unattended publisher may mutate and commit.

## Doc 5 semantic publication interaction

Artifacts and README links are consequences of canonical managed changes, not independent semantic components. Doc 5 summaries should continue to describe:

```text
AGENTS.md updated
chat-handoff added
operational-modes updated
retired-skill removed
```

They should not add routine noise such as:

```text
global-agents.zip updated
README download list updated
operational-modes.zip updated
```

The `ManagedChangeSet` remains derived from canonical staged before/after trees. A derived-only difference during an otherwise canonical no-op is a deterministic-build defect, stale-artifact repair requiring explicit handling, or an authorised packaging-contract migration—not an ordinary managed-content publication.

## Mac mini boundary

The Mac mini consumer continues to validate and deploy only:

```text
source/staging/AGENTS.md
source/staging/skills/<dynamic user-skill content>
```

It ignores `upload-ready/` and the README during normal deployment. It must never deploy ZIP files, unzip or execute download artifacts, use them as deletion authority, or change the Mac Studio source-of-truth direction.

## Separate ChatGPT account boundary

Repository publication does not imply that a separate ChatGPT account or workspace:

- enables member-created skills;
- permits the operator's upload;
- accepts confidential or workplace-controlled content;
- treats re-upload as an update;
- synchronizes skills across web, desktop or other surfaces;
- authorizes automated installation.

The operator must review public skill contents under the receiving environment's policy. Codex Config Manager stores no work-account credentials and performs no cross-account API or browser automation under this contract.

## Public and repository-size boundary

Portable packaging increases download convenience and practical exposure. Before publication:

- every packaged file must already be suitable for the public canonical repository;
- no credentials, tokens, private URLs or workplace-confidential material may be present;
- archive metadata must not disclose local usernames, ownership, source paths or live timestamps;
- README wording must not imply endorsement or workplace suitability merely because an artifact is public.

Stable active filenames prevent directory clutter but do not eliminate Git history cost. Each changed compressed artifact may create another binary blob. Mode C must therefore measure initial and representative changed artifact sizes, Git object growth, clone/fetch impact and applicable GitHub constraints. Per-skill ZIPs limit churn to the changed skill rather than rebuilding one aggregate archive for every skill edit.

## Required tests before implementation completion

Tests must cover at least:

- the proven wrapper-directory ZIP shape;
- dynamic discovery with current and future skill names;
- exact basename/wrapper matching;
- nested supporting files;
- `global-agents.zip` root layout and byte equivalence;
- skill and `AGENTS.md` add/update/remove transitions;
- zero managed skills and absent `AGENTS.md`;
- `.system/**`, `.DS_Store`, `__MACOSX/` and `._*` exclusion;
- traversal, duplicates, case collisions, unsupported entries and archive bombs;
- deterministic no-op rebuild byte equality;
- interrupted build and atomic-replacement recovery;
- bounded README updates that preserve human-authored content;
- README membership equality and stable ordering;
- exact Git path allowlisting and unrelated-change refusal;
- commit/push retry retaining the same canonical/artifact/README state;
- Mac mini ignoring all distribution artifacts;
- real GitHub Markdown preview and direct ZIP download behaviour after the remote exists;
- representative repository-growth measurements.

Re-upload behaviour in ChatGPT is useful follow-up discovery but is not required to prove repository packaging correctness.

## Impact assessment for existing documents

### Doc 3

A protected future reconciliation must:

| Doc 3 junction | Required impact |
| --- | --- |
| Governing reading map | Add Doc 7 as the portable-distribution contract |
| Locked topology | Add `upload-ready/global-agents.zip`, dynamic per-skill ZIPs and bounded README projection |
| Publication allowlist | Permit only validated derived artifacts and the bounded README surface |
| Publisher phases | Build artifacts only after eligible canonical staging succeeds; validate and commit all projections atomically |
| Consumer phases | Explicitly ignore distribution artifacts on the Mac mini |
| Test gates | Add deterministic packaging, equivalence, lifecycle, README and GitHub behaviour tests |
| Documentation gate | Explain global view/download and individual skill-download surfaces |

### Doc 5

Doc 5 must preserve canonical paths as semantic authority while allowing exact derived artifacts and bounded README changes in the same commit. Push retry must retain the identical artifact set associated with the existing commit SHA.

### Doc 6

Doc 6 remains the eligibility layer. `paused`, scheduled-held and throttled-held state performs detection/reporting only and must not mutate staging, artifacts or README.

## Remaining decisions and implementation discoveries

Only bounded implementation details remain:

1. Exact direct-download URL form after the GitHub owner, repository name and default branch exist.
2. Exact bounded README-section mechanism.
3. ZIP timestamp, compression, permission, directory-entry and supported symlink rules.
4. Archive file-count, size and compression-ratio limits.
5. Packaging-contract versioning and intentional migration behaviour.
6. Exact Git pathspec validation for the dynamic but staging-derived skill ZIP set.
7. Repository-growth acceptance after representative binary updates.
8. ChatGPT re-upload/update behaviour as non-blocking external lifecycle discovery.

The core artifact identities, wrapper structures, README labels, canonical/derived relationship and add/update/remove behaviour are no longer open questions.

## Safe reconciliation path

Before implementation, a separately authorised protected Mode B pass should:

1. capture hashes of Docs 3, 5, 6 and this revised Doc 7;
2. create byte-identical dated snapshots only for documents that will be edited;
3. reconcile the exact authority, topology, allowlist, phase, gate, test and documentation junctions;
4. compare every revised document with its immediate pre-edit snapshot;
5. verify unrelated contracts and prior protected snapshots remain unchanged;
6. perform no application, Git, ZIP, README or external-account implementation unless Mode C is separately authorised.

## Current implementation status

- ✅ The real ChatGPT test proves the one-skill ZIP wrapper layout used by this contract.
- ✅ The aggregate ZIP proposal is replaced by one stable ZIP per dynamically discovered staged user skill.
- ✅ Global guidance is represented as `global-agents.zip` containing the unchanged canonical `AGENTS.md` at archive root.
- ✅ README global labels, canonical view path, portable download path and dynamic skill list behaviour are locked.
- ✅ Canonical authority, exclusions, deterministic packaging, atomic publication, bounded deletion, Git semantics and Mac mini separation are captured.
- ▶ Docs 3 and 5 require protected reconciliation before implementation; Doc 6 remains upstream eligibility authority.
- ▶ Direct GitHub ZIP download behaviour must be validated after the remote exists.
- ⛔ No repository implementation, ZIP artifact, README, configuration, Git state, launchd state, ChatGPT automation or Codex managed state has been created or modified.
