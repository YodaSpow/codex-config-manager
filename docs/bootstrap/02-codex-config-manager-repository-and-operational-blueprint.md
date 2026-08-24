# Codex Config Manager — Repository & Operational Blueprint

**Status:** Pre-implementation blueprint  
**Repository:** `codex-config-manager`  
**Primary bootstrap machine:** Mac Studio  
**Initial downstream consumer:** Mac Mini  
**Purpose:** Define the repository structure, ownership boundaries, configuration model, staging topology, implementation responsibilities, testing expectations, and controlled Mac Studio → Mac Mini handoff before implementation begins.

---

# Problem Statement 🎯

`codex-config-manager` must do more than transport a global Codex `AGENTS.md` file and the global Codex `skills/` tree between machines.

The repository must eventually contain the **complete reusable machinery that performs that transport**.

The project therefore has two related but distinct operational lanes:

- **Publisher:** initially the Mac Studio.
- **Consumer:** initially the Mac Mini.
- Both implementations live in the same Git repository.
- They are separate executable workflows.
- They share common utilities where appropriate.
- They operate against the same persistent staged payload.
- Each machine activates only its assigned role.
- Machine-specific configuration remains local and is never committed.
- The Mac Studio bootstraps the complete repository structure before the Mac Mini implementation begins.
- The Mac Mini may refine its explicitly bounded consumer implementation, but it must not independently redefine the architecture or publisher contract.

The objective is to prevent two AIs working on two Macs from gradually producing two incompatible implementations.

The repository itself becomes the canonical contract between them.

---

# Key Paths and Repository 🔗

## Repository

GitHub repository:

```text
https://github.com/YodaSpow/codex-config-manager
```

Local repository path on both machines:

```text
/Users/spowart/Scripts/codex-config-manager
```

## Mac Studio Codex root

```text
/Users/spowart/.codex
```

The only managed global Codex surfaces are:

```text
/Users/spowart/.codex/AGENTS.md
/Users/spowart/.codex/skills/
```

Everything else beneath `.codex` is outside the project boundary.

The publisher must therefore use an **allowlist**, not a blacklist.

Conceptually:

```text
IN SCOPE
├── ~/.codex/AGENTS.md
└── ~/.codex/skills/**

OUT OF SCOPE
└── ~/.codex/everything-else
```

The `skills/` tree is recursive and opaque.

The implementation must preserve all files, directories, nested directories, and future additions beneath `skills/` without requiring them to be individually enumerated.

---

# Core Architectural Boundary 🧱

The project has three different kinds of state.

## 1. Live Codex state

This is the actual state consumed by Codex on a machine.

```text
~/.codex/
├── AGENTS.md
└── skills/
```

On the Mac Studio this is the **publisher source of truth**.

On the Mac Mini this is the **consumer deployment target**.

---

## 2. Persistent staged state

The repository contains one persistent staged representation:

```text
source/staging/
├── AGENTS.md
└── skills/
```

This directory is Git tracked.

It is **not temporary storage**.

It persists between executions and across restarts.

Its semantic role depends upon the machine:

| Machine | Meaning of `source/staging/` |
| --- | --- |
| Mac Studio | Persistent published mirror of the managed live Codex state |
| Mac Mini | Persistent locally checked-out representation of the published GitHub state |

There must not be separate publisher and consumer copies of this payload.

There is one canonical staged payload.

---

## 3. Orchestration machinery

The repository also contains the code required to move and validate that staged state.

Publisher and consumer orchestration remain separate because their responsibilities and directions are fundamentally different.

Shared primitives may be reused.

---

# Critical `AGENTS.md` Namespace Rule ⚠️

The transported global Codex `AGENTS.md` must **never** be placed at the repository root.

A repository-level:

```text
codex-config-manager/AGENTS.md
```

would have a different semantic meaning: it could become Codex instructions governing the `codex-config-manager` repository itself.

The transported global file must therefore live at:

```text
codex-config-manager/source/staging/AGENTS.md
```

This preserves the repository root namespace for a legitimate future repository-specific `AGENTS.md` if one is ever required.

The distinction is:

```text
Repository instructions, if ever required:
codex-config-manager/AGENTS.md

Transported global Codex instructions:
codex-config-manager/source/staging/AGENTS.md
```

These must never be conflated.

---

# Target Repository Blueprint 🗂️

The Mac Studio implementation should establish the repository shape before the Mac Mini is asked to implement its consumer role.

The initial target structure is:

```text
codex-config-manager/
├── README.md
├── .gitignore
│
├── docs/
│   ├── architecture.md
│   ├── blueprint.md
│   └── implementation.md
│
├── source/
│   ├── staging/
│   │   ├── AGENTS.md
│   │   └── skills/
│   │       └── ...
│   │
│   ├── publisher/
│   │   ├── publisher.sh
│   │   └── ...
│   │
│   ├── consumer/
│   │   ├── consumer.sh
│   │   └── ...
│   │
│   └── shared/
│       ├── rsync.sh
│       ├── logging.sh
│       ├── config.sh
│       └── ...
│
├── config/
│   ├── config.example.yaml
│   └── config.yaml
│
├── launchd/
│   ├── publisher/
│   │   └── ...
│   └── consumer/
│       └── ...
│
├── scripts/
│   ├── install
│   ├── uninstall
│   ├── status
│   └── validate
│
└── tests/
    ├── publisher/
    ├── consumer/
    ├── simulation/
    └── fixtures/
```

This is a **structural contract**, not a requirement to create empty directories or artificial abstraction.

If implementation proves that a proposed subdirectory serves no useful purpose, the Mac Studio may simplify it while preserving the architectural boundaries defined by this blueprint.

For example, the project should not create:

```text
publisher/detect/
publisher/sync/
publisher/validate/
publisher/publish/
```

merely because those are conceptual stages.

Those responsibilities can initially reside within `publisher.sh` and shared helpers.

Directories should be introduced when actual implementation complexity warrants them.

---

# Same Repository, Different Roles 🧠

Both Macs have the same repository structure.

They do **not** have identical operational behaviour.

## Side-by-side model

| Concern | Mac Studio | Mac Mini |
| --- | --- | --- |
| Role | Publisher | Consumer |
| Repo path | `/Users/spowart/Scripts/codex-config-manager` | `/Users/spowart/Scripts/codex-config-manager` |
| Codex path | `/Users/spowart/.codex` | `/Users/spowart/.codex` |
| Staging path | `source/staging/` | `source/staging/` |
| Staging meaning | Last published mirror | Latest pulled published state |
| rsync direction | `.codex` → staging | staging → `.codex` |
| Git behaviour | Commit + push | Fetch + pull |
| Main executable | `publisher.sh` | `consumer.sh` |
| launchd lane | Publisher | Consumer |
| Architecture authority | Yes | No |
| Consumer refinement | Defines initial contract | Bounded implementation/validation |

Graphically:

```text
MAC STUDIO                                  MAC MINI
PUBLISHER                                   CONSUMER

~/.codex/                                   ~/.codex/
├── AGENTS.md                               ├── AGENTS.md
└── skills/                                 └── skills/
     │                                           ▲
     │ rsync                                     │ rsync
     ▼                                           │
source/staging/                             source/staging/
├── AGENTS.md                               ├── AGENTS.md
└── skills/                                 └── skills/
     │                                           ▲
     │ git push                                  │ git pull
     └──────────────► GitHub ────────────────────┘
```

---

# Publisher Boundary — Mac Studio 🧱

The Mac Studio is the initial **architecture owner and bootstrap implementation environment**.

Its live Codex state is authoritative:

```text
/Users/spowart/.codex/AGENTS.md
/Users/spowart/.codex/skills/
```

The publisher must never treat:

```text
source/staging/
```

as the authoring source.

Staging is a persistent mirror.

The fundamental direction is always:

```text
LIVE CODEX
    ↓
PERSISTENT STAGING
    ↓
GIT
    ↓
GITHUB
```

Never:

```text
STAGING
    ↓
LIVE CODEX
```

during normal publisher operation.

Automatic consumer behaviour must remain disabled on the Mac Studio.

Recovery from GitHub on the Studio is a separate, explicit, human-triggered operation if it is ever implemented.

---

# Mac Studio Publisher Pipeline 🧰

The publisher needs two levels of change detection.

## Cheap trigger

A lightweight mechanism determines that something **may** have changed.

This trigger must not depend upon the modification timestamp of the parent `skills/` directory.

Deep modifications inside:

```text
skills/<skill>/...
```

cannot be assumed to propagate reliable modification information to the root `skills/` directory.

The trigger therefore only initiates verification.

It does not determine truth.

## Authoritative recursive comparison

`rsync` performs the authoritative recursive comparison.

Conceptually:

```text
possible change
      ↓
rsync dry-run
      ↓
actual managed difference?
```

If no managed difference exists:

```text
STOP
```

If a difference exists:

```text
real rsync
   ↓
validate staging
   ↓
git diff
   ↓
commit
   ↓
push
```

The complete conceptual publisher flow is:

```text
launchd / lightweight trigger
        ↓
possible managed change
        ↓
rsync dry-run
~/.codex → source/staging
        ↓
difference?
   ├── NO ──► stop
   │
   └── YES
        ↓
real rsync
        ↓
source/staging updated
        ↓
validate
        ↓
git diff
        ↓
meaningful Git change?
   ├── NO ──► stop
   │
   └── YES
        ↓
commit
        ↓
push GitHub
        ↓
record success
```

---

# Publisher rsync Contract ⚠️

Publisher rsync is **copy-oriented**.

The live `.codex` source must never be moved, rewritten, reorganised, or otherwise mutated by the publishing operation.

The managed source is:

```text
~/.codex/AGENTS.md
~/.codex/skills/
```

The destination is:

```text
source/staging/AGENTS.md
source/staging/skills/
```

The implementation must preserve:

- directory hierarchy;
- nested skill directories;
- existing files;
- newly discovered files;
- newly discovered directories;
- legitimate updates to existing managed files.

The implementation must determine deliberate deletion semantics during build and document them before enabling unattended operation.

Deletion behaviour must **not** be assumed merely from the word "mirror."

No implementation may broaden rsync from the allowlisted surfaces to the entire `.codex` directory.

---

# Consumer Boundary — Mac Mini 🧱

The Mac Mini is initially a **consumer**.

Its normal direction is:

```text
GITHUB
   ↓
LOCAL REPOSITORY
   ↓
source/staging/
   ↓
LIVE CODEX
```

It must not independently redesign:

- repository topology;
- publisher behaviour;
- shared contracts;
- staging semantics;
- role semantics;
- configuration schema;
- architecture documentation.

Its purpose during phase two is to prove that the consumer contract established by the Studio works against a real consumer machine.

The Mini may discover implementation realities that were impossible to prove on the Studio.

Those discoveries may result in changes to the repository, but only within explicitly defined consumer extension boundaries or through a deliberate architecture change reviewed against the canonical contract.

---

# Mac Mini Consumer Pipeline 🧰

The consumer has a different change-detection problem from the publisher.

Git already provides the first comparison:

```text
LOCAL REPOSITORY REVISION
        vs
REMOTE REPOSITORY REVISION
```

The normal flow should therefore resemble:

```text
launchd trigger
      ↓
git fetch
      ↓
remote published state newer?
   ├── NO ──► stop
   │
   └── YES
        ↓
git pull
        ↓
validate source/staging
        ↓
rsync dry-run
source/staging → ~/.codex
        ↓
managed Codex state differs?
   ├── NO ──► record success / stop
   │
   └── YES
        ↓
real rsync
        ↓
verify deployed state
        ↓
record success
```

Git determines whether the published repository has advanced.

rsync determines whether the managed live Codex state needs deployment.

These are separate checks.

---

# Separate Publisher and Consumer Executables 🧠

Publisher and consumer must **not** be collapsed into one large role-switching executable merely because they share some primitives.

The intended model is:

```text
source/publisher/publisher.sh
source/consumer/consumer.sh
```

with shared functionality underneath:

```text
source/shared/
├── rsync.sh
├── logging.sh
└── config.sh
```

This preserves clear operational ownership.

Publisher code can evolve without accidentally altering consumer control flow, and consumer implementation work can remain bounded without rewriting publisher orchestration.

Role selection determines which executable and launchd service are installed or activated.

---

# Configuration Contract 🧠

Configuration has two surfaces.

## Public configuration template

Tracked by Git:

```text
config/config.example.yaml
```

This is part of the public project contract.

It must document **both publisher and consumer configuration requirements**.

It must contain safe placeholders rather than personal machine information.

Example conceptual structure:

```yaml
# Human-readable machine identifier.
# Examples: mac-studio, mac-mini, workstation-01
machine:
  id: example-machine

# Valid roles:
#   publisher
#   consumer
role: publisher

paths:
  # Local user home directory.
  home: /Users/<username>

  # Codex runtime root.
  codex_root: /Users/<username>/.codex

  # Local codex-config-manager repository.
  repo_root: /Users/<username>/Scripts/codex-config-manager

  # Persistent managed staging state.
  staging_root: /Users/<username>/Scripts/codex-config-manager/source/staging
```

The exact final keys are implementation decisions, but the template must describe the complete supported contract.

---

# Local `config.yaml` Boundary ⚠️

Each machine has:

```text
config/config.yaml
```

This file must be excluded through `.gitignore`.

For example:

```text
config/
├── config.example.yaml    Git tracked
└── config.yaml            local only
```

The local configuration contains truthful machine-specific values.

Mac Studio example conceptually:

```yaml
machine:
  id: mac-studio

role: publisher

paths:
  home: /Users/spowart
  codex_root: /Users/spowart/.codex
  repo_root: /Users/spowart/Scripts/codex-config-manager
  staging_root: /Users/spowart/Scripts/codex-config-manager/source/staging
```

Mac Mini conceptually:

```yaml
machine:
  id: mac-mini

role: consumer

paths:
  home: /Users/spowart
  codex_root: /Users/spowart/.codex
  repo_root: /Users/spowart/Scripts/codex-config-manager
  staging_root: /Users/spowart/Scripts/codex-config-manager/source/staging
```

These examples describe the current machines only.

The implementation should avoid unnecessarily hard-coding `spowart` into application logic.

Where practical, paths should be derived from configuration or safe operating-system information so the public project remains reusable by other users.

---

# Configuration Boundary Rule ⚠️

`config.example.yaml` and `config.yaml` must remain structurally aligned.

If the Mac Mini implementation discovers that a new consumer setting is required, it must not quietly add a private key only to its local `config.yaml`.

The required sequence is:

```text
consumer discovers legitimate configuration requirement
        ↓
determine whether requirement fits existing architecture
        ↓
update public config contract
        ↓
update config.example.yaml
        ↓
update configuration loader / validation
        ↓
set truthful local value in Mini config.yaml
```

Therefore:

> Every supported private configuration capability must have a safe public representation in `config.example.yaml`.

The example file exposes the **shape and meaning** of configuration.

The local file exposes the **truthful machine-specific values**.

---

# launchd Blueprint 🧰

Both roles require headless operation.

The repository should therefore contain both launchd implementations:

```text
launchd/
├── publisher/
│   └── ...
└── consumer/
    └── ...
```

The Mac Studio installs only the publisher service.

The Mac Mini installs only the consumer service.

## Publisher launchd responsibility

Conceptually:

```text
trigger publisher
      ↓
cheap detection
      ↓
rsync verification
      ↓
publish only when required
```

## Consumer launchd responsibility

Conceptually:

```text
periodically trigger consumer
      ↓
Git remote check
      ↓
pull when required
      ↓
rsync deployment when required
```

The exact plist names, cadence, environment setup, log paths, and failure behaviour must be established during implementation and subsequently documented in `implementation.md`.

---

# Mac Studio as Initial Builder 🧱

The Mac Studio has a larger responsibility than merely implementing `publisher.sh`.

Phase one must establish the **whole project shape**.

The Studio AI should:

1. Read the canonical architecture document.
2. Read this blueprint.
3. Inspect the real Mac Studio environment.
4. Confirm the live Codex paths and allowlisted surfaces.
5. Confirm the repository location and Git state.
6. Establish the agreed repository topology.
7. Establish `source/staging/` as the persistent managed payload.
8. Establish publisher, consumer and shared implementation surfaces.
9. Establish public and private configuration handling.
10. Establish `.gitignore` protection for local-only state.
11. Establish the publisher launchd lane.
12. Establish the consumer launchd lane structurally, even if real consumer validation is deferred.
13. Implement the publisher workflow against the real Mac Studio.
14. Build consumer simulation and contract tests where reasonably possible.
15. Document what is implemented versus what remains deferred.
16. Prepare the Mac Mini to inherit an already-defined project rather than inventing one independently.

The Mac Studio is therefore the **initial architecture owner, repository bootstrapper and publisher implementation environment**.

Its responsibility extends beyond getting the publisher working.

It must prepare the complete project for downstream adoption.

---

# Mac Studio Ownership Boundary 🧱

The Mac Studio owns the initial canonical shape of:

- repository topology;
- staging semantics;
- publisher architecture;
- consumer contract;
- shared implementation boundaries;
- configuration schema;
- launchd structure;
- testing structure;
- documentation structure;
- public project behaviour.

The Studio may refine the proposed physical folder structure during implementation if real implementation evidence shows that a different arrangement is simpler or safer.

However, structural refinement must preserve the architectural contracts.

For example, it may decide that:

```text
source/shared/rsync.sh
```

does not justify its own file and should initially be implemented differently.

That is acceptable.

It may **not** decide that:

```text
source/staging/
```

is unnecessary and place the transported global `AGENTS.md` at repository root.

That would violate an established architectural boundary.

The distinction is:

> Implementation shape may evolve. Architectural meaning must remain stable unless deliberately changed.

---

# Mac Mini Handoff Boundary 📤

The Mac Mini must not receive only a repository clone and a vague instruction to "make the consumer work."

The Studio must prepare a bounded handoff.

The handoff should explain:

- the current architecture;
- the repository topology;
- the consumer executable;
- the persistent staging model;
- the intended Git flow;
- the intended rsync direction;
- the config contract;
- the expected local `config.yaml`;
- consumer launchd expectations;
- what has already been simulated;
- what has not yet been proven;
- what the Mini is allowed to refine;
- what the Mini must not redefine;
- required validation and reporting.

The Mac Mini should therefore start from:

```text
ESTABLISHED REPOSITORY
        +
ESTABLISHED CONSUMER CONTRACT
        +
HANDOFF
```

rather than:

```text
ARCHITECTURAL IDEA
        ↓
MAC MINI INVENTS IMPLEMENTATION
```

This is the primary mechanism for preventing publisher/consumer drift.

---

# Mac Mini Consumer Extension Boundary 🧠

The Mac Mini may need to change repository code during the real consumer build.

That is expected.

The goal is not to make the Mini read-only.

The goal is to constrain **where and why** it changes things.

Examples of legitimate consumer refinements include:

- correcting consumer-specific launchd behaviour;
- adjusting consumer installation logic;
- fixing Git-fetch or pull behaviour;
- adding consumer-specific validation;
- improving consumer logging;
- accounting for a real macOS consumer environment difference;
- adding a legitimate consumer configuration requirement;
- improving deployment verification;
- correcting assumptions exposed only by real consumer testing.

These changes should primarily remain within:

```text
source/consumer/
launchd/consumer/
tests/consumer/
tests/simulation/
scripts/
docs/
```

and shared code where the change is genuinely shared.

Changes to:

```text
source/publisher/
launchd/publisher/
source/staging/ semantics
configuration schema
architecture
```

require stronger justification because those areas are not consumer-owned by default.

The Mini must not solve a local problem by silently breaking the producer contract.

---

# Consumer Discoveries and Architecture Escalation ⚠️

Real consumer implementation may reveal that the Studio's original assumptions were incomplete.

That is not failure.

The required response is to classify the discovery.

## Consumer-local implementation issue

If the issue can be solved entirely within the established consumer contract:

```text
implement
      ↓
test
      ↓
document
      ↓
commit
```

## Shared implementation issue

If both roles legitimately require the change:

```text
identify shared requirement
      ↓
update shared implementation
      ↓
validate publisher remains unchanged
      ↓
validate consumer
      ↓
document
```

## Architectural issue

If the discovery would alter:

- role semantics;
- staging semantics;
- source-of-truth direction;
- managed asset scope;
- publisher behaviour;
- public configuration contract;
- repository topology;
- deletion behaviour;
- safety boundaries;

the Mini should stop treating it as a local fix.

It should be raised as an architecture-level change.

That creates a deliberate decision point rather than silent drift.

---

# Consumer Simulation on the Mac Studio 🧪

The Mac Studio should test as much of the consumer contract as possible before handing the project downstream.

This does **not** mean configuring the Studio as a consumer.

The Studio's real live `.codex` remains authoritative and must never be overwritten by normal consumer logic.

Instead, tests should use controlled fixtures or temporary destinations.

Conceptually:

```text
tests/
├── simulation/
└── fixtures/
```

A consumer simulation could resemble:

```text
known source/staging fixture
        ↓
consumer validation
        ↓
rsync dry-run
        ↓
temporary fake ~/.codex
        ↓
deployment
        ↓
verification
```

The test should prove, where possible:

- correct source path;
- correct destination mapping;
- recursive skill transfer;
- new files are included;
- new directories are included;
- unrelated `.codex` paths are untouched;
- `AGENTS.md` is placed correctly;
- no-op deployment behaves correctly;
- missing or invalid staging state fails safely;
- consumer code does not accidentally invoke publisher behaviour.

Simulation does not replace real Mini testing.

It narrows what the Mini has to discover.

---

# Persistent Staging Contract 🗂️

`source/staging/` is central to both roles.

Its physical structure is:

```text
source/staging/
├── AGENTS.md
└── skills/
    └── ...
```

It persists indefinitely.

It is Git tracked.

It is never deleted merely because a publisher or consumer execution completes.

It should not be treated like:

```text
/tmp/
cache/
build/
```

Its meaning is role-specific.

## Publisher meaning

```text
last staged/published representation
of the authoritative managed Mac Studio Codex state
```

## Consumer meaning

```text
latest locally checked-out representation
of the GitHub-published managed state
```

The same Git-tracked files provide continuity across both machines.

---

# Staging Direction Contract ⚠️

On the Mac Studio:

```text
~/.codex
   ↓
source/staging
```

On the Mac Mini:

```text
source/staging
   ↓
~/.codex
```

These directions must never be accidentally reversed during normal operation.

The publisher must never use staging as an automatic restore source.

The consumer must never publish its deployed `.codex` back into staging.

This maintains one-way provenance:

```text
AUTHOR
Mac Studio ~/.codex
        ↓
PUBLISHER STAGING
        ↓
GITHUB
        ↓
CONSUMER STAGING
        ↓
Mac Mini ~/.codex
```

---

# Git Ownership Contract 🧱

Git has different responsibilities on each role.

## Publisher

The publisher is allowed to create canonical published repository changes.

Conceptually:

```text
rsync updates source/staging
        ↓
git diff
        ↓
meaningful change?
        ↓
commit
        ↓
push
```

## Consumer

The consumer normally retrieves published repository changes.

Conceptually:

```text
git fetch
        ↓
remote advanced?
        ↓
git pull
```

The normal consumer runtime should not automatically commit local deployed state back into the repository.

Consumer **development work** may of course produce Git commits when improving consumer implementation, documentation or tests.

That is different from the runtime consumer pipeline.

---

# Git Safety Boundary ⚠️

Automated publisher Git behaviour must be conservative.

The publisher should not blindly commit arbitrary repository changes simply because `git status` is dirty.

A dirty repository may contain:

- human documentation edits;
- implementation work;
- uncommitted scripts;
- local debugging changes;
- unrelated project modifications.

The implementation must distinguish managed automated publication changes from unrelated development work.

Before enabling unattended commit/push behaviour, the Mac Studio implementation must define and document a safe policy for:

- detecting unrelated dirty worktree state;
- deciding when automated publication should stop rather than commit;
- restricting automated commits to intended managed changes where practical;
- ensuring local development work is never accidentally swept into an automated sync commit.

This is an implementation-critical safety requirement.

---

# rsync Copy-Only Principle ⚠️

The architecture is copy-oriented.

Publisher:

```text
SOURCE
live Mac Studio Codex

COPY TO

DESTINATION
persistent staging
```

Consumer:

```text
SOURCE
persistent staging

COPY TO

DESTINATION
live Mac Mini Codex
```

Neither workflow should be conceptualised as moving files.

The source remains in place after successful operation.

The destination remains in place between operations.

This persistence is fundamental to comparison and idempotency.

---

# Deletion Semantics Must Be Explicit ⚠️

The blueprint intentionally does not silently define deletion behaviour.

A key implementation question is:

> If something is deliberately deleted from `~/.codex/skills/` on the publisher, should that deletion propagate through staging, GitHub and consumers?

That decision has consequences.

Potentially:

```text
publisher deletion
      ↓
staging deletion
      ↓
Git deletion
      ↓
consumer deletion
```

could be correct.

It could also be destructive if triggered accidentally.

Before unattended deletion propagation is enabled, the Studio implementation must explicitly define:

- publisher deletion detection;
- staging deletion behaviour;
- Git representation;
- consumer deletion behaviour;
- safeguards;
- validation;
- rollback expectations.

Do not enable destructive rsync flags merely because `source/staging/` is described as a mirror.

---

# No-Op Behaviour 🧪

Both workflows must be idempotent.

## Publisher

```text
no effective managed difference
        ↓
no staging mutation
        ↓
no Git commit
        ↓
no push
```

## Consumer

```text
no newer Git state
        ↓
stop
```

or:

```text
newer Git state
        ↓
staging updated
        ↓
live Codex already equivalent
        ↓
no deployment rewrite
```

Periodic scheduling must not create meaningless filesystem churn or Git history.

---

# Validation Boundaries 🧪

Validation should exist at several points.

## Publisher preflight

Confirm:

- correct role;
- valid local config;
- repository exists;
- Codex root exists;
- `AGENTS.md` source exists;
- `skills/` source exists;
- staging destination is valid;
- Git repository is in an acceptable state.

## Publisher post-sync validation

Confirm:

- staged `AGENTS.md` exists;
- staged `skills/` exists;
- recursive structure is intact;
- nothing outside staging was unexpectedly changed;
- Git diff is limited to intended publication effects.

## Consumer preflight

Confirm:

- correct role;
- valid local config;
- repository exists;
- staging exists;
- expected staged assets exist;
- Codex target path is valid.

## Consumer post-deployment validation

Confirm:

- target `AGENTS.md` matches staging;
- target `skills/` reflects staging according to defined semantics;
- no unrelated `.codex` locations were modified;
- deployment completed successfully.

---

# Logging Blueprint 🧰

Both workflows should generate useful operational logs.

Logs should make it clear:

- which machine executed;
- configured role;
- timestamp;
- operation attempted;
- whether change was detected;
- whether rsync dry-run found differences;
- whether real rsync executed;
- Git action taken;
- success/failure;
- meaningful error information.

Logs must not contain sensitive contents from managed files unless explicitly required for debugging.

The log should favour metadata and operational outcomes over file content.

The final log path and rotation behaviour should be determined during implementation.

---

# Shared Utility Boundary 🧠

`source/shared/` should contain functionality that is genuinely common to both workflows.

Likely candidates include:

```text
source/shared/
├── config.sh
├── logging.sh
└── rsync.sh
```

These names are provisional.

Shared code should not become a dumping ground for role-specific logic.

A useful rule is:

> Shared utilities provide primitives. Publisher and consumer scripts own orchestration.

For example:

```text
shared rsync helper
```

may provide safe options and dry-run handling.

But:

```text
publisher decision to commit
```

belongs in publisher orchestration.

And:

```text
consumer decision to git pull
```

belongs in consumer orchestration.

---

# Installer and Operator Scripts 🧰

The initial structural blueprint reserves:

```text
scripts/
├── install
├── uninstall
├── status
└── validate
```

The final names may change.

Their intended purpose is to give the project a human-operable surface without requiring the operator to understand internal file locations or launchd commands.

Potential responsibilities:

## install

- validate config;
- determine configured role;
- install the correct launchd service;
- prepare required local directories;
- avoid installing the opposite role.

## uninstall

- disable/remove installed launchd integration;
- preserve user data and staged state unless explicitly requested otherwise;
- avoid deleting live Codex assets.

## status

- report configured role;
- report service state;
- show last known operational result;
- surface useful paths.

## validate

- perform role-aware preflight checks;
- validate config;
- validate repository structure;
- validate required managed paths;
- avoid modifying live state.

Implementation should keep these tools simple until real operational needs justify additional complexity.

---

# Public Repository Boundary ⚠️

The GitHub repository is public.

Git-tracked content must therefore be suitable for public exposure.

Expected public content includes:

- source code;
- publisher implementation;
- consumer implementation;
- shared implementation;
- `source/staging/AGENTS.md`;
- `source/staging/skills/**`;
- `config.example.yaml`;
- launchd templates or configuration;
- tests;
- documentation;
- public handoff material.

Expected local-only content includes:

- `config/config.yaml`;
- machine-specific secrets;
- credentials;
- authentication material;
- private machine state;
- logs where not deliberately included;
- temporary test artifacts;
- runtime-only state.

The project must never publish the whole `.codex` directory.

---

# Public Config and Private Config 🧠

The public repository must allow another person or future machine to understand the configuration contract without seeing the current operator's private values.

That means:

```text
config.example.yaml
```

must be complete enough that an AI or human can understand all supported options.

Local:

```text
config.yaml
```

provides real values.

The public example should therefore not be a token minimal file that omits consumer settings.

It should represent the union of supported publisher and consumer capabilities.

Comments should explain:

- purpose;
- expected format;
- valid values;
- publisher relevance;
- consumer relevance;
- safe examples.

This makes the config template part of the project's public documentation.

---

# Machine Identity Is Human-Controlled 🧠

The application should not guess:

```text
I am on a Mac Studio, therefore I am publisher.
```

Nor:

```text
hostname contains Mini, therefore I am consumer.
```

Instead:

```yaml
machine:
  id: mac-studio

role: publisher
```

or:

```yaml
machine:
  id: mac-mini

role: consumer
```

The identity is semantically meaningful for:

- logs;
- status;
- troubleshooting;
- human clarity.

The configured role determines operational behaviour.

---

# Publisher Must Never Auto-Consume ⚠️

Even though consumer code exists in the same repository on the Mac Studio, it must not be activated automatically.

Normal Studio operation is:

```text
LIVE CODEX
    ↓
PUBLISH
```

not:

```text
LIVE CODEX
    ↓
PUBLISH
    ↓
PULL
    ↓
OVERWRITE LIVE CODEX
```

That would introduce circular authority.

Recovery may eventually be supported, but it must be separately invoked and explicitly human-authorised.

---

# Mac Studio Consumer Simulation Is Not Consumer Mode ⚠️

The Studio may execute consumer code in:

- tests;
- fixtures;
- dry runs;
- isolated temporary directories;
- simulation environments.

That does not change its configured role.

Simulation must never result in automatic deployment into:

```text
/Users/spowart/.codex
```

on the authoritative publisher.

The publisher's live managed Codex state remains protected.

---

# Documentation Structure 📦

The eventual repository should contain permanent project documentation.

A conceptual final structure is:

```text
docs/
├── architecture.md
├── blueprint.md
├── implementation.md
├── publisher.md
├── consumer.md
├── configuration.md
├── operations.md
├── recovery.md
└── handoff.md
```

This is not a requirement to create every file immediately.

The Mac Studio should build documentation as implementation becomes truthful.

The purpose of the initial bootstrap documents is to guide creation of that reality.

They should not permanently substitute for implementation documentation.

---

# Bootstrap Documentation Lifecycle 📤

The initial bootstrap source lives under:

```text
docs/bootstrap/
```

The current handoff documents are:

```text
01-codex-config-manager-architecture-and-implementation-blueprint.md
02-codex-config-manager-repository-and-operational-blueprint.md
```

These documents should be read fully before implementation begins.

During initial construction, they serve as the pre-implementation authority.

Once the repository has:

- real code;
- real folder structure;
- real configuration;
- real launchd behaviour;
- real validation;
- real operational documentation;

the Studio may create canonical permanent docs that supersede bootstrap assumptions.

The bootstrap documents should not be silently deleted.

Once superseded, they may be archived with operator approval.

---

# Document Precedence 🧠

The architecture document and this blueprint overlap intentionally.

They are not competing specifications.

The architecture document defines:

- system purpose;
- managed scope;
- source-of-truth rules;
- publisher/consumer roles;
- core safety principles;
- high-level lifecycle;
- architectural invariants.

This repository and operational blueprint defines:

- current intended repository topology;
- staging location;
- namespace handling;
- executable separation;
- config structure;
- launchd topology;
- testing expectations;
- ownership boundaries;
- handoff behaviour.

Where the architecture document provides a broad conceptual implementation and this blueprint provides a more specific repository-facing refinement, this blueprint governs the implementation detail **provided it does not violate an architectural invariant**.

If a genuine conflict is discovered, the implementing AI must not silently choose one.

It should raise the issue for operator review.

---

# Mac Studio Initial Implementation Sequence 🧰

The Studio should not begin by blindly generating every folder from the tree diagram.

The recommended sequence is:

## Stage 1 — Read and inspect

1. Read the architecture bootstrap fully.
2. Read this blueprint fully.
3. Inspect the current repository.
4. Inspect the actual managed Mac Studio Codex surfaces.
5. Inspect Git status and remote configuration.
6. Confirm what already exists.
7. Identify assumptions requiring validation.

## Stage 2 — Establish project skeleton

Create the minimum meaningful structure for:

```text
source/staging/
source/publisher/
source/consumer/
source/shared/
config/
launchd/
scripts/
tests/
docs/
```

Avoid empty abstraction for its own sake.

## Stage 3 — Configuration

Implement:

```text
config/config.example.yaml
config/config.yaml
```

with:

- public contract;
- private truthful values;
- `.gitignore` protection;
- validation.

## Stage 4 — Staging

Establish:

```text
source/staging/AGENTS.md
source/staging/skills/
```

from the Mac Studio's authoritative managed state.

Ensure the global `AGENTS.md` never lands at repository root.

## Stage 5 — Publisher implementation

Implement and validate:

```text
source/publisher/publisher.sh
```

including:

- role validation;
- cheap triggering;
- rsync dry-run;
- real sync when needed;
- staging validation;
- safe Git diff handling;
- safe commit behaviour;
- safe push behaviour;
- logs.

## Stage 6 — Publisher launchd

Implement and validate:

```text
launchd/publisher/
```

including:

- correct execution environment;
- safe cadence/trigger;
- log paths;
- failure handling.

## Stage 7 — Consumer skeleton

Establish:

```text
source/consumer/consumer.sh
launchd/consumer/
tests/consumer/
```

to the extent possible without pretending the real Mac Mini environment has been validated.

## Stage 8 — Consumer simulation

Use controlled fixtures and temporary targets to prove the consumer contract without deploying into the Studio's live `.codex`.

## Stage 9 — Documentation

Create truthful documentation of:

- repository structure;
- publisher implementation;
- config;
- launchd;
- staging;
- tests;
- known deferred consumer work.

## Stage 10 — Mac Mini handoff

Prepare the repository so the Mac Mini can begin from an established state.

---

# Mac Mini Initial Adoption Sequence 🧰

The Mac Mini should begin from the repository created by the Mac Studio.

Its sequence should resemble:

## Stage 1 — Read

1. Read canonical project documentation.
2. Read the Mac Mini handoff.
3. Inspect current repository state.
4. Inspect local `.codex`.
5. Confirm that the machine is intended to be a consumer.

## Stage 2 — Local configuration

Create:

```text
config/config.yaml
```

with:

```yaml
role: consumer
```

and truthful Mini paths.

Do not modify `config.example.yaml` unless a legitimate new public contract requirement is discovered.

## Stage 3 — Consumer validation

Validate:

- Git repository;
- remote;
- staging;
- managed source files;
- local Codex destination;
- consumer script assumptions.

## Stage 4 — Consumer implementation refinement

Complete or correct consumer-specific implementation only where real Mini evidence requires it.

## Stage 5 — launchd

Install and validate only the consumer service.

## Stage 6 — End-to-end proof

Prove:

```text
Studio source
   ↓
Studio staging
   ↓
GitHub
   ↓
Mini staging
   ↓
Mini live Codex
```

## Stage 7 — Contribute findings

Update:

- consumer code;
- tests;
- docs;
- public config contract if legitimately required.

Do not redesign publisher architecture casually.

---

# Consumer Handoff Content 📤

The Studio-generated handoff should eventually tell the Mini AI:

- what the repository is;
- which role to use;
- which docs to read;
- what paths are expected;
- which files are local-only;
- which Git branch/state is canonical;
- what is already implemented;
- what has been simulated;
- what remains unproven;
- which files the Mini may legitimately change;
- which architectural surfaces require escalation;
- how to validate success;
- how to report any discrepancy.

The handoff should be concise enough to use practically but grounded in repository documentation.

The repository should carry the deep context.

The handoff should point to that context rather than duplicate the entire project history.

---

# Drift Prevention Contract ⚠️

The project must treat drift as a first-class design risk.

Potential drift sources include:

- Mac Studio changing publisher assumptions without updating consumer expectations;
- Mac Mini independently changing shared code;
- private config keys appearing only on one machine;
- launchd behaviour diverging;
- staging semantics changing;
- documentation no longer matching code;
- consumer fixes altering publisher behaviour;
- GitHub no longer reflecting actual implementation.

The prevention model is:

```text
ONE CANONICAL REPOSITORY
        +
PUBLIC CONFIG CONTRACT
        +
EXPLICIT ROLE BOUNDARIES
        +
TESTS
        +
TRUTHFUL DOCUMENTATION
        +
BOUNDED HANDOFF
```

The repo is the boss.

Neither physical Mac is allowed to maintain a secret incompatible version of the project.

---

# Contract Versioning 🧠

The first implementation may benefit from a lightweight project or contract version marker.

The exact mechanism should be decided during implementation.

Its purpose would be to let a consumer determine whether its expected architecture/config contract is compatible with the repository it has pulled.

Conceptually:

```text
consumer expects contract X
        vs
repo declares contract X
```

If incompatible:

```text
STOP
        ↓
report mismatch
```

rather than blindly deploying.

This should remain lightweight.

Do not introduce elaborate schema/version infrastructure unless implementation demonstrates a real need.

---

# Repository-Specific `AGENTS.md` Future Option 🧠

The repository root remains intentionally available for a future:

```text
AGENTS.md
```

that governs AI behaviour **inside this repository**.

If one is introduced later, it must clearly refer to:

```text
codex-config-manager
```

and not represent the global Codex file being transported.

The global managed file remains:

```text
source/staging/AGENTS.md
```

This namespace separation is permanent.

---

# README Responsibility 📦

The root `README.md` should eventually provide a concise public-facing explanation of:

- what Codex Config Manager does;
- publisher and consumer roles;
- what is synchronised;
- what is deliberately excluded;
- basic architecture;
- installation entry points;
- configuration;
- documentation links;
- safety model.

It should not attempt to replace the deeper architecture or operational documentation.

GitHub Pages may later provide a richer documentation surface.

---

# Public Reusability 🧠

Although the initial machines are:

```text
Mac Studio
Mac Mini
```

and both currently use:

```text
/Users/spowart
```

the repository should not be unnecessarily tied to that account or hardware.

The project should be reusable conceptually as:

```text
publisher machine
        ↓
GitHub
        ↓
one or more consumer machines
```

The current paths are real implementation inputs.

They are not universal architectural requirements.

Configuration should provide the portability boundary.

---

# Safety Invariants ⚠️

The repository implementation should preserve the following invariants:

1. Only global `AGENTS.md` and `skills/**` are managed.
2. The whole `.codex` tree is never synced.
3. The transported global `AGENTS.md` is never placed at repository root.
4. Staging is persistent.
5. Staging is Git tracked.
6. There is only one canonical staged payload.
7. Publisher and consumer executables are separate.
8. Shared code contains primitives, not mixed orchestration.
9. The Mac Studio is publisher by explicit local config.
10. The Mac Mini is consumer by explicit local config.
11. Publisher operation is `.codex → staging → GitHub`.
12. Consumer operation is `GitHub → staging → .codex`.
13. Publisher never auto-consumes.
14. Consumer never republishes its live `.codex` as normal runtime behaviour.
15. rsync is copy-oriented.
16. Deep skill changes are discovered recursively.
17. Parent `skills/` timestamps are not treated as authoritative.
18. No-op operations produce no meaningful mutation.
19. `config.yaml` remains local.
20. `config.example.yaml` remains the public config contract.
21. Consumer config changes must remain aligned with the public contract.
22. Only the assigned launchd lane is installed on a machine.
23. Consumer simulation on Studio never targets Studio's live `.codex`.
24. Mac Mini changes remain bounded unless architecture is deliberately revisited.
25. GitHub remains the canonical shared repository state.
26. Documentation must evolve with implementation.
27. The project should remain reusable beyond the initial two machines.

---

# Validation Milestones 🧪

The implementation should not be considered complete because scripts merely execute without errors.

## Publisher milestone

Prove:

```text
edit managed Studio source
        ↓
trigger
        ↓
rsync detects real difference
        ↓
staging updated
        ↓
Git records intended change
        ↓
GitHub receives it
```

and:

```text
no managed change
        ↓
no commit
```

## Consumer simulation milestone

On the Studio, prove against a safe temporary target:

```text
known staging state
        ↓
consumer
        ↓
correct target state
```

without touching authoritative Studio live state.

## Real consumer milestone

On the Mac Mini, prove:

```text
new GitHub published state
        ↓
git fetch/pull
        ↓
source/staging updated
        ↓
rsync detects live difference
        ↓
Mini ~/.codex updated
```

and:

```text
no newer state
        ↓
no deployment
```

## Safety milestone

Prove that unrelated `.codex` files remain unchanged.

---

# Failure Behaviour ⚠️

Unattended operation must fail conservatively.

Examples:

## Publisher

If:

- config invalid;
- source missing;
- repo missing;
- staging invalid;
- Git state unsafe;
- rsync fails;
- validation fails;
- push fails;

the publisher should stop and log the failure.

It should not continue to later stages blindly.

## Consumer

If:

- config invalid;
- repository update fails;
- staging invalid;
- validation fails;
- rsync fails;
- target path invalid;

the consumer should stop and preserve the last known usable local Codex state wherever possible.

A partially validated upstream state must not be deployed merely because a scheduled job ran.

---

# Recovery Boundary ⚠️

Publisher recovery remains separate from normal publishing.

If implemented later, a recovery workflow may allow the Mac Studio to restore managed assets from a known GitHub state.

That action must be:

- explicit;
- human-triggered;
- validated;
- clearly logged.

It must never be wired into normal publisher launchd behaviour.

Similarly, consumer rollback may eventually be supported through Git history, but should be designed deliberately rather than emerging accidentally.

---

# Definition of Repository Readiness 📦

The repository is ready for Mac Mini handoff when the Mac Studio has established:

- a coherent repository tree;
- persistent staging;
- correct global `AGENTS.md` namespace handling;
- working publisher script;
- working publisher launchd;
- safe Git publishing;
- public config template;
- private Studio config;
- consumer script structure;
- consumer launchd structure;
- shared helper structure where justified;
- consumer simulation;
- validation tests;
- implementation documentation;
- consumer handoff documentation;
- known limitations;
- explicit unresolved Mini-only validation items.

The Mini should not receive a half-defined repository whose architecture still depends upon the Mini inventing missing fundamentals.

---

# Definition of Consumer Readiness 📦

The Mac Mini is considered operational when:

- the canonical repository is present;
- local consumer config exists;
- consumer role is confirmed;
- Git remote updates function;
- staging is correctly populated;
- consumer rsync works;
- live `.codex/AGENTS.md` is correctly deployed;
- the full recursive `skills/` tree is correctly deployed;
- unrelated `.codex` content is untouched;
- launchd runs the consumer reliably;
- no-op checks behave correctly;
- logs provide useful evidence;
- consumer-specific refinements are committed back appropriately;
- documentation reflects what was learned.

---

# End-to-End Target State 📦

The finished system should look conceptually like this:

```text
MAC STUDIO
Publisher

/Users/spowart/.codex/
├── AGENTS.md
└── skills/
      │
      │ rsync dry-run / rsync
      ▼
/Users/spowart/Scripts/codex-config-manager/
└── source/
    └── staging/
        ├── AGENTS.md
        └── skills/
              │
              │ Git commit / push
              ▼

           GITHUB
YodaSpow/codex-config-manager

              │
              │ Git fetch / pull
              ▼

MAC MINI
Consumer

/Users/spowart/Scripts/codex-config-manager/
└── source/
    └── staging/
        ├── AGENTS.md
        └── skills/
              │
              │ rsync dry-run / rsync
              ▼
/Users/spowart/.codex/
├── AGENTS.md
└── skills/
```

The Git repository also carries the implementation machinery surrounding that payload:

```text
source/publisher/
source/consumer/
source/shared/
config/
launchd/
scripts/
tests/
docs/
```

Therefore the repository contains both:

```text
THE STATE BEING TRANSPORTED
```

and:

```text
THE SYSTEM THAT TRANSPORTS IT
```

That distinction is one of the core reasons this project exists.

---

# Mac Studio Bootstrap Handoff 📤

The Mac Studio AI should receive both bootstrap documents:

```text
/Users/spowart/Scripts/codex-config-manager/docs/bootstrap/
├── 01-codex-config-manager-architecture-and-implementation-blueprint.md
└── 02-codex-config-manager-repository-and-operational-blueprint.md
```

It must read both completely before implementing.

The documents are complementary.

The Mac Studio AI should then:

1. inspect reality;
2. reconcile the blueprint with the actual environment;
3. report any material ambiguity;
4. establish the repository structure;
5. implement the publisher;
6. prepare the consumer contract;
7. simulate the consumer where possible;
8. create truthful permanent project documentation;
9. prepare the Mac Mini handoff;
10. preserve architectural boundaries throughout.

The first task is not blind code generation.

The first task is:

```text
READ
  ↓
INSPECT
  ↓
UNDERSTAND
  ↓
RECONCILE
  ↓
PLAN
  ↓
IMPLEMENT
```

If a material question affects:

- architecture;
- staging;
- source-of-truth direction;
- deletion semantics;
- config exposure;
- Git safety;
- rsync behaviour;
- launchd behaviour;
- consumer boundaries;

the Studio AI should ask the operator rather than silently inventing a new contract.

---

# Final Blueprint Principle 🧱

The Mac Studio digs the first side of the tunnel.

But it also establishes the reference line, dimensions, interfaces and endpoint that the Mac Mini is expected to meet.

The Mac Mini is allowed to discover the realities of its side.

It is not allowed to dig in an unrelated direction.

The canonical repository is the shared survey.

The architecture is the contract.

The staging state is the payload.

The publisher and consumer are separate operational lanes.

The public config defines the supported machine contract.

Local config supplies each machine's private truth.

The Mac Studio establishes the system.

The Mac Mini validates and completes its bounded consumer implementation.

Both contribute back to one canonical repository.

That is the intended repository and operational blueprint for `codex-config-manager`.