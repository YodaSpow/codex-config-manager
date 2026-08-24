# Doc 3 — Mode C Implementation Plan — Mac Studio Bootstrap and Mac mini Handoff

**Status:** Final pre-implementation execution plan; implementation is not yet authorised or started  
**Scope:** Complete Mac Studio repository bootstrap, Python implementation, environment construction, publisher validation, consumer simulation, permanent documentation and bounded Mac mini handoff  
**Prepared:** 21 August 2026  
**Implementation authority:** This document defines what a future Mode C must do. It does not itself authorise Mode C, Git mutation, dependency installation, rsync construction, launchd installation, GitHub publication or Codex-state mutation.

## Status

- ✅ The architecture, managed scope, source-of-truth direction, deletion semantics, Python direction, environment ownership, GitHub transport and machine-role boundaries are settled.
- ✅ The pre-implementation Mac Studio repository, managed-source, Python, rsync and Git/GitHub state has been inspected read-only.
- ✅ Every remaining unknown has been classified below as a Mode C implementation discovery, implementation choice, proof gate or explicitly deferred Mac mini validation item.
- ▶ The next action, only after explicit operator authorisation, is to execute this plan in Mode C in its stated order.
- ⛔ No application code, Git repository, dependency environment, repository-owned rsync, staging payload or launchd service is created by this document.

## Purpose

This document gives the first Mode C implementation one repository-owned execution plan with parity to:

- both complete bootstrap documents;
- the managed-skill ingestion discovery;
- the Python and environment-ownership discovery;
- subsequent operator decisions made after those documents;
- verified Mac Studio Git/GitHub discovery;
- all implementation evidence still to be obtained;
- the work that must remain deferred to the real Mac mini.

It is intended to prevent implementation details, open proof obligations or safety conditions from surviving only in chat memory. A future implementation session must be able to read the repository and execute from this document without reconstructing the preceding conversation.

## Governing reading map and precedence

Mode C must read all six documents completely before changing the repository or any external state:

1. [Architecture and Implementation Blueprint](bootstrap/01-codex-config-manager-architecture-and-implementation-blueprint.md) — architectural purpose, authority, direction and invariants.
2. [Repository and Operational Blueprint](bootstrap/02-codex-config-manager-repository-and-operational-blueprint.md) — repository-facing topology, role boundaries, operational flows and validation expectations.
3. [Doc 1 — Managed Skill Ingestion Exclusions](01-implementation-discovery-managed-skill-ingestion-exclusions.md) — `.system/**`, `.DS_Store` and dynamic user-skill discovery.
4. [Doc 2 — Python Runtime and Environment Ownership](02-implementation-discovery-python-runtime-environment-ownership.md) — Python, PyYAML, dependency locking, `.venv`, repository-owned rsync, `.tools`, launchd resolution and environment proofs.
5. [Doc 4 — Deterministic Model-Derived Machine Identity](04-implementation-discovery-deterministic-machine-identity.md) — native model-name identity, normalization, local config ownership and preflight matching.
6. This Doc 3 — the reconciled Mode C sequence, current Mac Studio evidence, proof gates, stop conditions and handoff boundary.

The documents are layers, not competing specifications:

- the architecture blueprint owns architectural invariants;
- the repository blueprint owns the more specific repository and operational shape where it does not violate an invariant;
- Docs 1, 2 and 4 refine implementation contracts using verified repository and machine reality;
- this plan reconciles later operator decisions and verified Git discovery into an executable sequence without replacing the earlier documents.

Where the bootstrap documents describe deletion semantics as undecided, the later operator decision recorded here governs: legitimate managed deletions propagate automatically and remain strictly bounded. Where the bootstrap documents use shell entry points or discuss `yq`, Doc 2 governs: the implementation is Python-first and uses repository-local PyYAML. The bootstrap documents must remain unchanged as historical design inputs until truthful implementation documentation later supersedes them with operator approval.

## Mode A implementation baseline

### Local repository and managed-source state

Read-only inspection on 21 August 2026 established the following baseline:

```text
repo_exists= True
repo_git_directory_exists= False
repo_venv_exists= False
repo_tools_exists= False
repo_pyproject_exists= False
codex_root_exists= True
managed_agents_exists= True
managed_skills_root_exists= True
system_exclusion_root_present= True
dynamic_user_skill_root_count= 3
```

Practical meaning:

- `/Users/spowart/Scripts/codex-config-manager` exists but is not yet a Git working tree;
- the only repository-owned project content currently present is documentation plus unmanaged Finder metadata;
- `.venv`, `.tools`, `pyproject.toml`, application code, tests, config, staging and launchd implementation do not yet exist;
- `/Users/spowart/.codex` exists and its two managed entry surfaces currently exist;
- `skills/.system` exists but is outside the managed universe;
- three current user-skill roots were observed, but their names are deliberately not an implementation contract.

### Python and rsync baseline

The current executable observations are:

```text
python_executable= /opt/homebrew/opt/python@3.14/bin/python3.14
python_version= 3.14.4
/opt/homebrew/bin/rsync
rsync  version 3.4.1  protocol version 32
```

Python 3.14.4 is the initial implementation and validation baseline. It is not a permanent exact public pin. Homebrew rsync 3.4.1 is a modern capability reference only; it is not the project runtime, version ceiling or selected upstream release.

### Git and GitHub baseline

The local directory is not currently a Git repository:

```text
fatal: not a git repository (or any of the parent directories): .git
```

The Mac Studio has an existing machine-local Git identity and an explicit GitHub SSH configuration. A non-interactive authentication check reached GitHub as the intended account:

```text
Hi YodaSpow! You've successfully authenticated, but GitHub does not provide shell access.
ssh_status=1
```

Exit status `1` is GitHub's expected response to a successful SSH authentication request because it does not provide interactive shell access. Authenticated repository access over SSH succeeded:

```text
ref: refs/heads/main	HEAD
fa0e73b4ef1109c1b4614f2372beb6d2f80ffa3a	HEAD
```

The existing remote is public, active and uses `main`:

```text
remote_private=False
remote_default_branch=main
remote_archived=False
remote_disabled=False
```

Its current root contains:

```text
remote_path=README.md type=file
```

Therefore Mode C must reuse the proven machine-local SSH lane unless new evidence invalidates it. It must attach the local directory to the existing remote history, preserve the remote `README.md` and avoid force-pushing or inventing an unrelated root history. GitHub CLI is not required. Push authority and launchd-context SSH access remain implementation proofs because Mode A deliberately performed no write.

## Locked target architecture

```text
Mac Studio — authoritative publisher

/Users/spowart/.codex/
├── AGENTS.md
└── skills/
    ├── .system/             excluded recursively
    ├── .DS_Store            ignored wherever encountered
    └── every current/future user skill, discovered dynamically
            │
            │ Python publisher + exact repository-owned rsync
            ▼
source/staging/
├── AGENTS.md                present only when present in authoritative source
└── skills/                  managed user-skill payload only
            │
            │ path-scoped Git commit and SSH push
            ▼
PUBLIC GITHUB REPOSITORY
            │
            │ consumer fast-forward update
            ▼
Mac mini — bounded consumer

source/staging/
            │
            │ Python consumer + exact repository-owned rsync
            ▼
/Users/spowart/.codex/
├── AGENTS.md
└── skills/                 unrelated content and exclusions preserved
```

The Mac Studio live managed state is authoritative. `source/staging/` is a persistent Git-tracked mirror, never an authoring source on the Mac Studio. GitHub is the canonical shared published repository state. The Mac mini consumes real local files and never depends on a live mount, hard link, symlink to, or network connection with the Mac Studio.

## Final managed-universe contract

The publisher allowlist is exactly:

```text
/Users/spowart/.codex/AGENTS.md
/Users/spowart/.codex/skills/**
```

subject to these exclusions:

```text
/Users/spowart/.codex/skills/.system/**    excluded recursively
.DS_Store                                 excluded globally at every depth
```

All other content beneath `/Users/spowart/.codex` is outside the project. The implementation must positively construct operations from the two allowed surfaces; it must never copy the `.codex` root and subtract known unwanted content.

User-skill discovery is dynamic. Every current and future normal entry beneath `skills/` participates recursively without a hard-coded skill-name list. The contents of each included user skill are opaque to Codex Config Manager.

The exclusion contract applies identically to:

- scheduled or cheap detection;
- recursive dry-run comparison;
- real copying;
- itemized-change interpretation;
- staging validation;
- Git diff, staging and publication;
- consumer staging validation;
- consumer deployment;
- automatic managed deletion;
- no-op detection;
- tests and simulations.

`.system/**` must never become managed staged state. If a manually or externally introduced `.system` path is detected in the staged payload, validation must fail safely and report it; Codex Config Manager must not deploy, publish, clean or delete it.

`.DS_Store` is noise, not managed state. Codex Config Manager must never copy, publish, deploy, compare as meaningful change, deliberately remove or otherwise manage it. The global `.gitignore` protects Git, and rsync exclusions prevent it from entering managed transfers. If Finder independently creates one, the application ignores and preserves it rather than treating cleanup as part of the project.

### Missing-source and deletion distinction

The configured Codex root is the safety anchor:

- if the configured `/Users/spowart/.codex` root is missing, unreadable, inaccessible, outside the accepted containment boundary or affected by an I/O/permission failure, the publisher stops without changing staging or Git;
- if that root exists and is readable, absence of a managed item is authoritative managed state and therefore represents deletion;
- this applies to `AGENTS.md`, user-skill files, user-skill directories and the absence of previously managed user skills;
- the managed `skills/` staging container may remain as structural representation even when it contains no managed user skills.

Tests must distinguish authoritative absence from source-root failure so a transient access problem can never be interpreted as a request to delete the published payload.

## Final deletion contract

Ordinary legitimate managed deletion propagates automatically:

```text
managed item absent from readable authoritative Mac Studio source
        ↓
bounded deletion from source/staging
        ↓
Git records deletion
        ↓
GitHub publishes deletion
        ↓
Mac mini receives deletion in staging
        ↓
bounded deletion from Mac mini managed target
```

There is no per-deletion human approval requirement. Git history provides historical recovery. Deletion must nevertheless be bounded to the managed universe and proven before unattended launchd activation.

The rsync contract may use `--delete` only at the specific managed destination boundary. It must never construct or execute `--delete-excluded`. Excluded `.system/**`, `.DS_Store` and every unrelated `.codex` surface must survive deletion operations untouched.

Publisher recovery from GitHub is not the reverse half of normal publication. Any future Mac Studio restoration remains explicit, human-triggered, separately validated and outside the unattended publisher lane. Consumer rollback is likewise not allowed to emerge accidentally from normal operation.

## Locked execution-environment contract

```text
EXTERNAL / PLATFORM OWNED

macOS
Apple Silicon as the initially validated architecture
compatible Python interpreter
Apple Command Line Tools only when required for controlled build/bootstrap

        ↓

REPOSITORY CONTRACT OWNED

Python support/test policy
direct Python dependency declarations
runtime and development lock generation and consumption
environment creation, validation, receipt and repair
rsync upstream source/version/SHA-256/build contract
rsync complete non-system runtime dependency closure
launchd rendering and deterministic runtime resolution

        ↓

LOCAL GENERATED, REPOSITORY-OWNED ENVIRONMENT

<repo-root>/.venv/
<repo-root>/.tools/rsync/
```

After successful bootstrap, normal operation must continue without Homebrew packages, binaries, libraries or runtime paths other than the permitted compatible external Python interpreter if that interpreter originated from Homebrew.

Python orchestrates; rsync remains authoritative for recursive checksum comparison, copying and bounded deletion. Python must execute exactly `<repo-root>/.tools/rsync/bin/rsync`. Neither application code nor launchd may search `PATH`, invoke unqualified `rsync`, fall back to macOS-native rsync or dynamically resolve Homebrew rsync.

## Locked publication, privacy and machine-ownership boundaries

The public GitHub repository contains the complete reusable project, not only the transported payload. Appropriate tracked content includes:

- persistent `source/staging/` managed state;
- publisher and consumer application code;
- genuine shared primitives;
- the complete safe public configuration template;
- publisher and consumer launchd templates;
- environment and rsync build/reproduction contracts;
- installer and operator tooling;
- tests and public-safe fixtures;
- architecture, discovery, implementation, operations and handoff documentation.

The following remain local and untracked:

- truthful `config/config.yaml` values;
- Git credentials, SSH keys, tokens and authentication material;
- `.venv/` and `.tools/` generated bytes;
- machine runtime state and locks;
- machine logs unless a separately reviewed public artifact is deliberately produced;
- generated/installed LaunchAgent state;
- caches, temporary artifacts and `.DS_Store`.

Codex Config Manager publishes exactly the explicit managed payload. It must not inspect file meaning, redact skill content automatically or infer whether authored content is confidential. Public suitability is a human authoring responsibility before content is introduced into the managed source. The application enforces scope and exclusions; it does not act as a semantic privacy scanner.

The Mac Studio owns the initial repository architecture, publisher implementation, shared contracts, initial consumer implementation, consumer simulation, permanent documentation and bounded handoff. The Mac mini owns truthful real-consumer validation and consumer-specific refinements within that established contract. The Mac mini must not silently redefine publisher behaviour, source-of-truth direction, staging, scope, deletion, public config or shared architecture.

The initial topology is one Mac Studio publisher and one Mac mini consumer, but the public design must support one explicitly configured publisher and one or more independently configured consumers. Current usernames, absolute paths and Apple Silicon observations are truthful validation inputs, not universal identity-detection logic or permanent portability limits.

## Planned repository topology

Mode C should create only paths backed by real implementation responsibilities. The intended final shape is:

```text
codex-config-manager/
├── README.md
├── .gitignore
├── pyproject.toml
├── requirements/
│   ├── runtime.lock
│   └── development.lock
├── config/
│   ├── config.example.yaml
│   └── config.yaml                         local, ignored
├── docs/
│   ├── bootstrap/
│   │   ├── 01-codex-config-manager-architecture-and-implementation-blueprint.md
│   │   └── 02-codex-config-manager-repository-and-operational-blueprint.md
│   ├── 01-implementation-discovery-managed-skill-ingestion-exclusions.md
│   ├── 02-implementation-discovery-python-runtime-environment-ownership.md
│   ├── 03-mode-c-implementation-plan.md
│   ├── 04-implementation-discovery-deterministic-machine-identity.md
│   └── <truthful permanent implementation and operating documents>
├── source/
│   └── staging/
│       ├── AGENTS.md                       when authoritatively present
│       └── skills/
│           └── <dynamic managed user-skill content>
├── src/
│   └── codex_config_manager/
│       ├── __init__.py
│       ├── publisher.py
│       ├── consumer.py
│       ├── config.py
│       ├── managed_scope.py
│       ├── paths.py
│       ├── rsync.py
│       ├── git.py
│       ├── launchd.py
│       ├── locking.py
│       ├── logging.py
│       └── validation.py
├── tooling/
│   └── rsync/                              tracked source/build contract
├── launchd/
│   ├── publisher/
│   │   └── <publisher plist template>
│   └── consumer/
│       └── <consumer plist template>
├── scripts/
│   ├── bootstrap.py
│   ├── install.py
│   ├── uninstall.py
│   ├── status.py
│   └── validate.py
└── tests/
    ├── unit/
    ├── integration/
    ├── simulation/
    └── fixtures/

LOCAL, GENERATED AND IGNORED
├── .venv/
├── .tools/
├── config/config.yaml
├── Python/test/tool caches
└── .DS_Store wherever Finder creates it
```

`source/staging/` is transported state. `src/` is application code. `tooling/rsync/` is the tracked reproducibility contract. `.tools/rsync/` is the generated local runtime. Mode C may consolidate very small modules where that reduces empty abstraction, but it must preserve the ownership boundaries and separately installed publisher and consumer entry points.

## Mode C execution rules

1. Execute phases in order and do not cross a proof gate merely because later work is convenient.
2. Use evidence from the real repository/runtime path, not detached substitutes, when live behaviour is being claimed.
3. Keep implementation decisions within the settled contracts. Do not reopen architecture without material contradictory evidence.
4. Treat every filesystem destination and deletion boundary as hostile until canonicalized, containment-checked and tested.
5. Never inspect, stage, publish or mutate unrelated `.codex` state.
6. Never copy credentials, SSH private keys, tokens or truthful machine configuration into the public repository.
7. Do not activate the Mac mini consumer on the Mac Studio. Consumer tests use isolated temporary paths only.
8. A scheduled job must fail clearly on an invalid environment; it must never repair dependencies over the network opportunistically.
9. Preserve both bootstrap documents verbatim during the initial implementation.
10. Record exact commands and decisive results in permanent documentation when implementation makes them truthful.

## Phase 0 — Reconfirm authority and safety baseline

Before the first mutation, Mode C must:

1. read the six governing documents completely;
2. confirm that the operator's Mode C authorisation covers the proposed repository changes and any external actions planned for that session;
3. inventory the current local tree and verify that no unexpected implementation or user change appeared after this plan;
4. recheck the remote branch, HEAD and repository identity;
5. record hashes for all six governing documents so their preservation can be proven;
6. confirm the managed Codex root and allowlisted entry surfaces without traversing unrelated `.codex` content;
7. identify any existing `.DS_Store` only as ignored noise and leave it untouched;
8. stop if new evidence materially contradicts an architectural invariant or changes the authority required.

**Gate 0:** The implementation inputs remain coherent, the exact actions are authorised and no unsafe external or repository state is present.

## Phase 1 — Reconcile local Git with the existing GitHub history

Mode C must establish one normal Git history rather than overwrite either side:

1. use the existing SSH remote `git@github.com:YodaSpow/codex-config-manager.git` and machine-local authentication unless revalidation proves it unusable;
2. establish the local Git metadata and `main` branch in a way that fetches and preserves the existing remote commit and `README.md`;
3. preserve every existing local documentation file;
4. create the repository-wide `.gitignore` before any broad initial staging, covering at least `.DS_Store`, `.venv/`, `.tools/`, private config, Python bytecode/caches, pytest/tool caches, local runtime state, locks, logs and generated launchd installation state;
5. verify that no `.DS_Store`, local config, credential or generated/private file is staged;
6. make ordinary human/AI development commits for repository construction; do not use the unattended publisher path for implementation commits;
7. prove branch ancestry and upstream tracking;
8. prove SSH push authority with a legitimate authorised development commit without force-pushing;
9. record and test the response to authentication failure, non-fast-forward rejection, branch protection/rules and network failure.

The implementation must not modify global Git identity, SSH configuration or credentials unless separate evidence and authority require it. The Mac Studio's currently working Git setup is an input, not project content.

**Gate 1:** The local directory is a normal `main` working tree tracking the existing `origin/main`; the remote `README.md` and local documents coexist in one ancestry; ignored/private paths are absent from Git; an authorised normal SSH push has succeeded; no force operation was used.

## Phase 2 — Establish the Python project and dependency contract

Mode C must:

1. create `pyproject.toml` as the authoritative project metadata, direct-dependency and console-entry-point surface;
2. establish separate publisher and consumer console commands plus operator commands for install, uninstall, status and validation;
3. use Python 3.14.4 as the first implementation/test input while selecting the public supported range only from actual compatibility evidence;
4. select current compatible PyYAML, pytest and lock-generation tooling deliberately using primary upstream/package evidence;
5. keep PyYAML as a direct runtime dependency and pytest/lock tooling in the development dependency set;
6. use `yaml.safe_load()` followed by explicit type, required-key and semantic validation;
7. implement one coherent resolver/lock workflow—initially the minimal pinned `pip-tools` model from Doc 2 unless implementation evidence proves a simpler equally reproducible mechanism;
8. generate exact hashed `runtime.lock` and `development.lock` closures;
9. make the development lock include the runtime closure plus test/development tools;
10. document the exact command that declares, resolves, reviews, installs and deliberately refreshes each dependency set;
11. prove clean installation from committed locks without resolving new versions during normal bootstrap.

The supported Python declaration and tested-Python record are different facts. A newer compatible interpreter may be validated and adopted later without turning the current patch release into a permanent pin.

**Gate 2:** A clean environment can reproduce the exact runtime and development dependency closures; no project package is imported from global, user, Apple/Xcode or unrelated environments; exact selected versions and hashes are reviewable.

## Phase 3 — Implement `.venv` bootstrap, receipt, validation and repair

The repository must provide a deterministic bootstrap path that can run from a compatible external Python before the project environment exists. It must:

1. create only the bounded `<repo-root>/.venv` destination;
2. install the selected hashed runtime or development lock;
3. install Codex Config Manager without re-resolving dependencies;
4. validate imports and installed console commands;
5. write an atomic local environment receipt containing interpreter path, Python version/cache tag, architecture, environment type, dependency-lock digest, project/source identity and last successful validation;
6. detect missing/broken Python, incompatible major/minor or architecture, changed lock digest, broken imports, missing entry points and receipt mismatch;
7. rebuild only the verified repository-local `.venv` after validating the exact deletion target;
8. leave scheduled operation failed and diagnosable rather than starting an uncontrolled network rebuild;
9. expose an explicit operator repair/update command;
10. prove rebuild from missing, stale and deliberately corrupted test environments.

Compatible patch-level changes should be validated rather than causing gratuitous rebuilds. A broken interpreter link or materially incompatible interpreter must cause deliberate repair.

**Gate 3:** `.venv` creation and bounded repair are deterministic, receipt-backed, isolated and reproducible, and a scheduled command cannot silently mutate dependency state.

## Phase 4 — Select and construct repository-owned rsync

This phase is a deliberate selection event. Mode C must:

1. check the authoritative upstream rsync source at implementation time and identify the latest suitable stable release;
2. select one exact release and record its version, source URL and SHA-256 in the tracked contract;
3. never use macOS-native rsync as runtime, fallback or capability baseline;
4. treat Homebrew rsync 3.4.1 only as observed reference capability;
5. prefer a pinned upstream source build using Apple Command Line Tools as build-only infrastructure;
6. configure the smallest feature set required for local checksum comparison, dry-run, itemized changes, recursive copy and bounded deletion;
7. disable optional libraries and features that are not required;
8. if a non-system runtime library is unavoidable, pin/checksum it, contain it beneath `.tools/rsync/lib`, use loader-relative resolution and include it in recursive validation;
9. install the executable only at `.tools/rsync/bin/rsync`;
10. create `.tools/rsync/build-receipt.json` with source/build/toolchain/architecture information, installed hashes, dependency closure and validation results;
11. use no internal multi-version manager, `current` symlink, runtime version switching or automatic upstream update check;
12. hold the selected build fixed until a later deliberate dependency refresh.

Mode C must determine, from the real source and build evidence:

- the exact first upstream release;
- minimal configure/build flags;
- whether non-system libraries can be eliminated, statically linked or must be bundled;
- loader-relative linkage and any macOS signing consequences;
- the capabilities actually needed for the managed files, including safe metadata and symlink/file-type behaviour.

If complete runtime isolation cannot be achieved using macOS system libraries/frameworks and locally contained `.tools/rsync/lib`, stop and return the evidence. Do not silently widen the runtime boundary.

**Gate 4:** The exact executable is checksummed, arm64-compatible, capability-verified and recursively linked only to permitted macOS or local `.tools/rsync/lib` dependencies. No `/opt/homebrew`, Homebrew Cellar or uncontrolled external runtime path remains.

## Phase 5 — Implement configuration, canonical paths and role enforcement

Mode C must create:

```text
config/config.example.yaml    complete tracked public contract
config/config.yaml            truthful ignored Mac Studio configuration
```

The public template must describe the union of publisher and consumer capabilities with safe examples and concise comments. The local Mac Studio file must declare `publisher` explicitly and use truthful absolute paths. Runtime code must not infer role from hardware, hostname, username or path.

Machine-ID formation and validation must follow [Doc 4 — Deterministic Model-Derived Machine Identity](04-implementation-discovery-deterministic-machine-identity.md): derive the actual human-readable identity mechanically from native macOS `Model Name`, compare it with local `machine.id`, fail safely on mismatch and keep role selection explicit and separate.

The schema must cover, at minimum:

- human-readable machine ID;
- `publisher` or `consumer` role;
- Codex root;
- repository root;
- persistent staging root;
- runtime-state and lock locations;
- log locations;
- separately configured publisher and consumer intervals, initially `300` seconds each;
- any environment/tool path that is legitimately operator-configurable rather than repository-derived.

Every supported private key must have a safe public representation. Credentials remain outside this config unless a later explicit contract requires a local secret reference; Git/SSH credentials remain machine-owned and never enter YAML or the repository.

Path handling must:

- expand operator-facing home notation only at the configuration boundary;
- operate internally on canonical absolute paths;
- reject dangerous roots, traversal and source/destination overlap;
- prove every mutation/deletion target is within its exact allowed boundary;
- resolve repository-owned Python and rsync paths from the repository contract, not interactive `PATH`;
- fail if configured role and invoked command disagree.

Mode C must choose final key names, logging rotation details and runtime-state representation within this contract, then keep loader, public example, tests and permanent docs aligned.

**Gate 5:** Both role configurations validate against one public schema; model-derived and configured machine identity match; the Mac Studio's private config is ignored; invalid identities, types, roles, missing keys and dangerous paths fail before mutation.

## Phase 6 — Implement one reusable managed-scope and rsync contract

The Python implementation must centralize inclusion, exclusion, path mapping, deletion and rsync argument construction so publisher, consumer, validation and tests cannot drift.

Required rsync behaviour:

- exact repository-owned executable path;
- checksum comparison with `--checksum`;
- a mutation-free `--dry-run` first;
- machine-parseable `--itemize-changes`;
- correct recursion and trailing-slash semantics;
- `.system/**` excluded at the skills ingestion boundary;
- `.DS_Store` excluded globally;
- bounded `--delete` for authoritative managed deletion;
- no construction of `--delete-excluded`;
- post-operation validation followed by a second dry-run proving equivalence.

The implementation must define and test supported filesystem entry semantics. Regular files and directories must work recursively. Symlinks, empty directories, special files, modes, timestamps, xattrs and ACLs must be evaluated against Git representability, portability and the actual managed source. Unsupported or unsafe entries must cause a clear conservative failure rather than silent loss, external-target traversal or accidental scope expansion.

Rsync itemization must be parsed as operational metadata. Logs must never dump managed file contents.

**Gate 6:** Publisher and consumer derive their inverse mappings from one tested managed-scope contract; all exclusion/deletion options are identical where required; dry-run is non-mutating; a second dry-run proves no meaningful difference.

## Phase 7 — Establish and validate persistent staging

Only after the environment and scope gates pass may Mode C create the managed payload:

```text
source/staging/
├── AGENTS.md      if present in authoritative state
└── skills/        managed user-skill content only
```

Initial ingestion must originate only from the readable authoritative Mac Studio managed source. It must not manually copy hard-coded current skills. It must not place the transported global `AGENTS.md` at repository root.

Staging validation must prove:

- every managed path maps to an allowed source path;
- no `.system` content is present in the managed payload;
- `.DS_Store` is ignored and untracked rather than cleaned;
- no unrelated `.codex` content entered staging;
- unsupported path/file forms are rejected;
- the staged tree is a truthful managed representation of the source;
- a post-ingestion dry-run is equivalent;
- Git sees only expected public managed content.

**Gate 7:** Persistent staging contains exactly the managed public payload and survives repeated no-op runs without writes or Git noise.

## Phase 8 — Implement the Mac Studio publisher

The publisher owns this control flow:

```text
configured scheduled invocation
        ↓
single-instance lock
        ↓
environment/config/role/path/Git/source preflight
        ↓
checksum rsync dry-run: Mac Studio live source → staging
        ↓
no difference ──► record concise no-op and stop
        ↓
real bounded rsync
        ↓
staging validation + post-sync equivalence dry-run
        ↓
conservative path-scoped Git validation
        ↓
commit source/staging changes only
        ↓
SSH push
        ↓
atomic success state and metadata-only log
```

The scheduled interval is a cheap trigger, not proof of a change. Parent `skills/` modification time must never suppress the authoritative recursive dry-run.

Publisher failures must stop the pipeline in place. Invalid config, missing/unreadable Codex root, invalid environment, unsafe Git state, rsync failure, invalid staging, failed equivalence, commit failure or push failure must prevent later stages and produce a useful non-secret error.

Each run must log operational metadata sufficient to diagnose behaviour: timestamp, configured machine ID and role, operation attempted, change/no-change result, whether dry-run and real rsync ran, Git action/outcome, final success/failure and a concise error classification. Logs must not contain managed file contents, credentials or authentication material.

The publisher must never deploy staging or GitHub state into the Mac Studio live `.codex`. Recovery remains separate and human-triggered.

**Gate 8:** Unit/integration tests and an explicitly authorised controlled Mac Studio validation prove meaningful change, no-op, nested change, new future-style skill and legitimate managed deletion without touching excluded or unrelated state.

## Phase 9 — Implement conservative automated Git publication

Normal development and unattended publication are different lanes.

Normal human/AI development commits may change all appropriate public project files. The unattended publisher may stage and commit only:

```text
source/staging/**
```

It must never use `git add .` or an equivalent broad pathspec. Git logic must:

1. acquire the project execution lock before inspecting or mutating shared repository state;
2. verify expected repository identity, branch and upstream;
3. fetch/compare remote state without deploying it into the Mac Studio live source;
4. reject unexpected staged paths, unrelated worktree changes, detached HEAD, unmerged state and unrecognized divergence;
5. stage the exact `source/staging` pathspec so deletions are represented;
6. inspect every staged path and reject anything outside that prefix;
7. commit only when the staged diff is meaningful;
8. push without force;
9. log commit identity and outcome without credentials or managed content;
10. preserve a successfully created but unpushed commit after network failure;
11. recognize and safely retry only its own validated pending publication rather than creating duplicate commits or rewriting unknown work;
12. stop for operator recovery when ahead/behind/diverged state cannot be proven safe.

Mode C must test branch-rule behaviour, authentication failure, network failure, push rejection, pre-existing dirty work, pre-existing staged work, unrelated changes, deletion-only changes, failed retry and successful retry. The exact pending-publication marker/recognition mechanism is an implementation choice, but it must be deterministic and receipt/test-backed.

**Gate 9:** Automated publication cannot stage unrelated content, cannot force-push, creates no no-op commits, records legitimate deletions and has a proven conservative failure/retry path.

## Phase 10 — Implement the bounded consumer lane

The repository must contain a complete initial consumer implementation even though the real Mac mini is not yet available for validation.

The consumer owns:

```text
configured scheduled invocation
        ↓
single-instance lock
        ↓
environment/config/role/path/repository preflight
        ↓
Git fetch and safe fast-forward determination
        ↓
no newer state ──► record concise no-op and stop
        ↓
safe repository update
        ↓
validate source/staging before live deployment
        ↓
checksum rsync dry-run: staging → consumer live managed targets
        ↓
no managed difference ──► record success and stop
        ↓
real bounded rsync with managed deletions
        ↓
post-deployment validation and equivalence dry-run
```

The consumer must:

- update only through a safe fast-forward policy and stop on dirty/ahead/diverged/ambiguous state;
- validate the staged payload before touching live Codex state;
- deploy only `AGENTS.md` and dynamically discovered managed user-skill content;
- preserve `.system/**`, `.DS_Store` and every unrelated `.codex` surface;
- propagate legitimate deletion within managed targets;
- never commit or republish deployed live state during normal runtime;
- never invoke publisher orchestration;
- preserve the last known usable live state when update or validation fails before deployment.

Any lightweight repository/config contract marker must remain proportionate. Mode C must decide whether it materially prevents incompatible deployment once the real schema exists; implement and test the smallest useful marker if justified, or record why existing validation is sufficient. It must not grow into an elaborate version-management subsystem.

**Gate 10:** Consumer code is structurally complete and can be exercised entirely against isolated paths with no route to the Mac Studio's authoritative live `.codex`.

## Phase 11 — Build the complete test and simulation proof

Tests must use the repository-owned development environment and actual repository-owned rsync where integration behaviour is claimed. The minimum suite must cover:

### Configuration, paths and roles

- PyYAML safe loading;
- generic model-name normalization and exact detected/configured machine-ID matching;
- missing, malformed and mismatched machine identity failing before mutation;
- required keys, types and valid role values;
- public/private schema alignment;
- publisher/consumer interval rendering, including initial `300`-second values;
- canonical absolute paths;
- containment, source/destination overlap and dangerous-target rejection;
- wrong-role command rejection.

### Managed scope and exclusions

- current and future user-skill roots discovered dynamically without a name allowlist;
- arbitrary nested user-skill files/directories preserved;
- root `skills/.system/**` excluded at ingestion;
- manually introduced staged `.system` rejected without deletion;
- `.DS_Store` ignored at repository root, staging, nested skills and consumer targets;
- `.DS_Store` never treated as change and never deliberately removed;
- unrelated `.codex` sentinels unchanged;
- supported/unsupported symlink and filesystem-entry policy;
- no traversal outside approved roots.

### Comparison, copying and deletion

- checksum detection when timestamp and size would otherwise conceal content change;
- mutation-free dry-run;
- truthful parseable itemization;
- correct recursive/trailing-slash mapping;
- new file, nested directory and future-style skill creation;
- file, directory, user-skill and `AGENTS.md` deletion propagation;
- readable-root authoritative absence distinguished from missing/unreadable-root failure;
- bounded deletion preserves exclusions and unrelated content;
- command construction can never contain `--delete-excluded`;
- no-op produces no meaningful write;
- second dry-run proves equivalence.

### Environment and rsync isolation

- runtime and development clean installs from hashes;
- missing/stale/incompatible/corrupt `.venv` detection and bounded repair;
- receipt and lock-digest mismatch;
- exact `.tools/rsync/bin/rsync` resolution;
- executable/library hashes and recursive linkage;
- absence of Homebrew runtime paths;
- required rsync flags/capabilities;
- conceptual Homebrew-removal acceptance test, preserving only the permitted external Python interpreter.

### Git safety

- expected branch/upstream and fast-forward checks;
- path-scoped staging including deletions;
- rejection of staged or dirty unrelated work;
- no-op commit suppression;
- authentication/network/push failure;
- safe pending-publication retry without duplicate commit;
- consumer dirty/ahead/diverged rejection;
- consumer never commits.

### Publisher and consumer orchestration

- step ordering and stop-on-failure at every boundary;
- single-instance and stale-lock behaviour;
- metadata-only logging and atomic runtime-state updates;
- publisher change/no-op/deletion flows;
- consumer remote-no-change, repository-change/live-equivalent and deployment flows;
- no cross-invocation of the opposite role.

### Installer and operator commands

- bootstrap creates or repairs only the repository-owned environment boundaries;
- install validates role/config and installs only the matching launchd lane;
- uninstall unloads/removes only generated launchd integration and preserves live Codex state, staging, config, environments, logs and user data unless a separately explicit bounded removal is authorised;
- status is read-only and reports configured machine/role, environment validity, repository state, installed service state, last known result and useful paths without secrets;
- validate is role-aware and non-mutating, checks config/environment/repository/staging/managed paths and reports exact failures;
- wrong-role, missing-environment and unsafe-path cases fail conservatively for every command.

### Mac Studio consumer simulation

Simulation must create isolated temporary repositories, staging trees and fake Codex roots at runtime. It must prove initial deployment, update, no-op, deletion, invalid staging, unmanaged sentinel preservation and exclusion preservation. Tests may create `.system` and `.DS_Store` conditions inside temporary directories; those artifacts must never become published managed fixtures.

Every simulation must assert that `/Users/spowart/.codex` was not a target. A path guard must make accidental use of the authoritative Mac Studio root impossible, not merely discouraged.

**Gate 11:** The exact repository test command passes with a decisive summary; targeted safety suites pass independently; temporary artifacts are contained and removed; no live Codex or launchd state was touched by simulation.

## Phase 12 — Render, install and validate launchd

Launchd work begins only after deletion, environment, Git and consumer-simulation safety gates pass.

The repository contains both role templates, but the Mac Studio installs only the publisher LaunchAgent. Mode C must:

1. render the plist from validated local config rather than hard-code machine truth;
2. use the configured publisher interval, initially `300` seconds;
3. execute the absolute `<repo-root>/.venv/bin/codex-config-manager-publisher` command;
4. use deterministic repository/config/state/log paths;
5. avoid shell activation, aliases, interactive `PATH`, global packages and unqualified rsync;
6. define a stable label, working directory, stdout/stderr handling and conservative failure behaviour;
7. prevent overlapping publisher instances;
8. create only bounded local application-support, lock, runtime-state and log directories;
9. install/uninstall through explicit operator commands that never delete live Codex assets, staging, config or user data by default;
10. validate the real user LaunchAgent domain, loaded state, schedule, environment resolution, log output, no-op run, meaningful authorised publication and failure reporting;
11. prove non-interactive SSH access from the launchd execution context;
12. leave the consumer LaunchAgent uninstalled on the Mac Studio.

The operator command contract must be completed in this phase:

- `install` prepares bounded local support directories, renders the configured role plist and installs only that role;
- `uninstall` removes only the installed role integration by default and explicitly preserves live managed Codex state, persistent staging, local config, `.venv`, `.tools`, logs and runtime data;
- `status` performs no mutation and presents the configured role, environment/tool validity, Git/remote state, LaunchAgent state, last result and relevant paths;
- `validate` performs a non-mutating role-aware preflight using the same contracts as scheduled execution.

Exact plist label/name, log rotation and launchctl commands must be selected and documented from real macOS behaviour during this phase. A saved plist is not runtime proof.

Any real managed-state canary creation/deletion used to prove the Mac Studio publisher requires explicit authority for that controlled validation. It must be obviously bounded, publicly safe and removed through the normal managed deletion path only after the publication evidence is captured. Existing operator content must never be sacrificed for a test.

**Gate 12:** The installed Mac Studio publisher runs through launchd at the configured interval using only repository-owned runtime paths, performs no-op and authorised-change behaviour correctly, publishes through SSH, logs safely and never activates the consumer.

## Phase 13 — Produce permanent implementation and operating documentation

Documentation must be written from implemented evidence, not by converting this future-tense plan into claims of success. The Mac Studio phase must produce a coherent permanent set covering:

- current architecture and repository topology;
- environment/dependency ownership, selected versions, hashes and refresh workflow;
- installation, bootstrap, repair and uninstall;
- complete configuration contract;
- publisher behaviour, Git safety and launchd operation;
- consumer contract and Mac Studio simulation evidence;
- validation/test commands and expected results;
- logging, status and troubleshooting;
- failure and recovery boundaries;
- public/privacy boundary;
- known Mac mini deferrals;
- bounded Mac mini handoff.

The root `README.md` should become the concise public entry point while preserving the legitimate existing remote history. Bootstrap documents remain preserved. Discovery and plan documents must be marked with truthful lifecycle status once implementation milestones are actually validated; they must not be left implying that future work remains current after it is complete.

**Gate 13:** A new human or AI can distinguish locked architecture, actual implementation, machine-local state, validation evidence and deferred Mac mini work from repository documentation alone.

## Phase 14 — Mac Studio repository-readiness audit and handoff

Before handoff, Mode C must prove:

- one coherent public Git history and clean expected working state;
- complete reusable code, config template, tests, launchd templates, tooling contracts and docs are published;
- only `source/staging/**` is writable by unattended publication;
- persistent staging truthfully represents the current managed Mac Studio state;
- publisher environment, rsync, Git and launchd gates pass;
- consumer simulation gates pass;
- private config, `.venv`, `.tools`, credentials, logs, state, locks, caches and `.DS_Store` are absent from Git;
- the transported global `AGENTS.md` is not at repository root;
- the consumer lane and its extension boundary are documented;
- every proof requiring the real Mac mini is listed explicitly.

The handoff must point to repository documentation rather than duplicate the entire project history. It must state exactly what the Mac mini may refine and what requires architecture-level escalation.

**Gate 14:** The repository satisfies the bootstrap definition of readiness and can be cloned by the Mac mini without requiring it to invent shared architecture or publisher behaviour.

## Phase 15 — Deferred real Mac mini validation

This phase does not occur on the Mac Studio and must remain labelled unproven until performed on the actual Mac mini. The Mac mini must:

1. use its own truthful machine-local Git identity and credential/SSH key; never copy the Mac Studio private key;
2. validate authenticated access and clone/update the canonical repository;
3. provide a compatible external Python and reconstruct `.venv` and `.tools/rsync` from the tracked contracts;
4. create its ignored truthful `consumer` config;
5. validate local paths, permissions, filesystem semantics and staging;
6. install only the consumer LaunchAgent;
7. prove safe fast-forward Git updates and invalid-state failures;
8. prove bounded deployment, no-op and legitimate deletion against the real Mac mini `.codex`;
9. prove `.system/**`, `.DS_Store` and unrelated `.codex` content remain untouched;
10. prove real launchd scheduling, deterministic runtime resolution, logging and failure behaviour;
11. complete the Mac Studio → GitHub → Mac mini end-to-end proof;
12. contribute truthful consumer-specific fixes, tests and documentation to the same canonical repository within the established extension boundary.

A Mac mini discovery that changes source-of-truth direction, managed scope, staging semantics, deletion policy, publisher behaviour, public config architecture, repository topology or safety boundaries is not a local fix. It must be escalated as an explicit architecture decision.

## Complete implementation-discovery ledger

The following are not unanswered architecture questions. They are mandatory Mode C discoveries or proof items and may not be silently omitted:

| Item to establish | Mode C location | Required durable outcome |
| --- | --- | --- |
| Supported Python range | Phases 2–3 | `pyproject.toml`, tested-version record and passing evidence |
| Exact tested Python versions | Phases 2–3 | Exact interpreter/architecture evidence |
| PyYAML, pytest and lock-tool versions | Phase 2 | Reviewed declarations and exact hashed locks |
| Lock generation/consumption/update workflow | Phase 2 | Reproducible commands and permanent dependency docs |
| `.venv` stale/rebuild semantics | Phase 3 | Receipt, bounded repair implementation and tests |
| Latest suitable stable upstream rsync at selection time | Phase 4 | Exact version, upstream source and SHA-256 |
| Minimal rsync feature/build configuration | Phase 4 | Tracked recipe and local build receipt |
| Complete rsync non-system dependency closure | Phase 4 | Local containment or proof that none is required |
| Loader-relative linkage and signing behaviour | Phase 4 | Recursive linkage/signing validation evidence |
| Required metadata, symlink and file-type semantics | Phases 4 and 6 | Conservative implemented policy and tests |
| Final config key names and validation | Phase 5 | Aligned example, loader, private config and tests |
| Exact logging paths, rotation and runtime state | Phases 5, 8 and 12 | Implemented operator contract and live evidence |
| Initial Git history reconciliation | Phase 1 | Existing remote history plus local docs in one ancestry |
| Actual Git push authority | Phases 1 and 9 | Successful authorised SSH push |
| Branch rules, retry and recovery behaviour | Phases 1 and 9 | Tested conservative policy and docs |
| Launchd plist generation/install/runtime | Phase 12 | Real Mac Studio user-agent evidence |
| SSH availability inside launchd context | Phase 12 | Non-interactive publisher push proof |
| Optional lightweight compatibility marker | Phase 10 | Small justified implementation or documented non-need |
| Consumer behaviour on the Mac Studio | Phase 11 | Isolated simulation evidence only |
| Consumer authentication/environment/live deployment | Phase 15 | Deferred real Mac mini evidence |
| Permanent docs and handoff | Phases 13–14 | Repository-owned truthful documentation |

## Stop and escalation conditions

Mode C may resolve ordinary implementation detail within this plan without returning a questionnaire. It must stop and present evidence if:

- the governing documents contain a genuine contradiction not reconciled here;
- current reality would require changing an architectural invariant or operator-approved boundary;
- the configured Codex root or a mutation/deletion target cannot be proven safe;
- rsync cannot meet the complete Homebrew-isolation contract;
- an upstream source or checksum cannot be authenticated sufficiently for the selected contract;
- the existing Git remote/history cannot be reconciled without destructive history rewriting;
- credentials, public-content suitability or required external authority is ambiguous;
- a managed filesystem entry cannot be transported truthfully and safely through both Git and rsync;
- Git is divergent or dirty in a way the conservative policy cannot recognize safely;
- a safety, deletion, isolation, simulation or launchd proof gate fails;
- real Mac mini evidence requires a change outside the bounded consumer extension contract.

These are evidence-triggered escalation conditions, not presently open operator questions.

## Completion definitions

### Mac Studio Mode C complete

The Mac Studio phase is complete only when Gates 0–14 pass, the public repository contains the complete reusable system, the publisher operates headlessly through its repository-owned environment, consumer simulation is safe and comprehensive, and permanent documentation plus the bounded Mac mini handoff are published.

### Whole project complete

The full Mac Studio → GitHub → Mac mini system is complete only after Phase 15 is executed on the real Mac mini, its evidence is contributed back, and permanent documentation reflects the validated behaviour of both machines.

## Final implementation posture

There are no material unanswered architectural questions before Mode C. Exact versions, build flags, config names, logging mechanics, Git failure handling, launchd details and real consumer behaviour remain intentionally evidence-driven, but every one now has an assigned implementation phase, proof gate and failure boundary.

Mode C must implement this established system; it must not reinterpret the absence of current code as permission to redesign it.
