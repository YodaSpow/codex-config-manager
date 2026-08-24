# Doc 2 — Implementation Discovery — Python Runtime and Environment Ownership

**Status:** Implemented and validated on the Mac Studio; retained as the environment discovery record. See [Doc 10](10-implementation-architecture-and-operations.md) and [Doc 11](11-validation-evidence-mac-studio.md).
**Scope:** Python application shape, dependency ownership, repository-local execution environment, rsync runtime isolation, launchd resolution, validation and rebuild boundaries  
**Relationship to bootstrap documents:** This record refines the physical implementation proposed by the bootstrap architecture and repository blueprint. It preserves their architectural contracts and does not modify or replace either bootstrap document.  
**Related discovery:** [Doc 1 — Implementation Discovery — Managed Skill Ingestion Exclusions](01-implementation-discovery-managed-skill-ingestion-exclusions.md) · [Doc 8 — Root-Level Latest Managed Snapshot](08-architecture-reconciliation-root-level-latest-managed-snapshot.md)

## Status

- ✅ Python is the operator-selected implementation language.
- ✅ PyYAML in a repository-local virtual environment is the approved YAML direction.
- ✅ The repository owns the reproducible Python dependency and rsync tool contracts.
- ✅ Normal runtime must be isolated from Homebrew except for the permitted external Python interpreter.
- ✅ macOS-native rsync is prohibited; Homebrew rsync is a reference baseline only.
- ✅ The latest suitable stable upstream rsync is preferred at a deliberate selection event, after which the exact validated release is held stable.
- ▶ Mode C must implement and prove this contract.
- ⛔ No Python project, virtual environment, dependency lock, local rsync runtime or launchd integration is established by this document.

## Purpose

The bootstrap documents established the system architecture before the real repository and Mac Studio runtime could be fully inspected. Repository-grounded discovery and subsequent operator decisions have now resolved the application language and execution-environment ownership model.

This document makes those decisions durable. It defines the implementation surface that Mode C should build while retaining the existing architecture:

```text
Mac Studio live managed Codex state
        ↓
Python publisher orchestration
        ↓
repository-owned rsync
        ↓
root-level latest/
        ↓
GitHub
        ↓
consumer repository latest/
        ↓
Python consumer orchestration
        ↓
repository-owned rsync
        ↓
consumer live managed Codex state
```

## Relationship to the bootstrap implementation shape

The bootstrap documents' separate `publisher.sh` and `consumer.sh` workflows expressed a role-separation requirement, not a permanent commitment to shell as the application language.

The reconciled implementation uses separate Python workflows:

```text
publisher.py
consumer.py
```

installed as separate console entry points. This retains:

- one project with two roles;
- separate publisher and consumer orchestration;
- shared primitives without mixed control flow;
- Studio-only publisher activation;
- Mini-only consumer activation;
- the existing persistent managed-snapshot and source-of-truth model, reconciled by Doc 8 to root-level `latest/`.

Shell must not carry substantive application logic. If any shell surface proves necessary for bootstrap compatibility, it must remain a minimal, deterministic launcher rather than a second implementation layer.

## Verified Mac Studio environment

The following facts were established through read-only inspection on 21 August 2026.

### Primary Python

The active `python3` is Homebrew Python 3.14.4, PyYAML is absent from that interpreter, and Homebrew marks the installation as externally managed. This proves that project packages must not be installed into its global package area.

```text
executable= /opt/homebrew/opt/python@3.14/bin/python3.14
version= 3.14.4 (main, Apr  7 2026, 13:13:20) [Clang 17.0.0 (clang-1700.6.4.2)]
prefix= /opt/homebrew/opt/python@3.14/Frameworks/Python.framework/Versions/3.14
base_prefix= /opt/homebrew/opt/python@3.14/Frameworks/Python.framework/Versions/3.14
stdlib= /opt/homebrew/opt/python@3.14/Frameworks/Python.framework/Versions/3.14/lib/python3.14
purelib= /opt/homebrew/lib/python3.14/site-packages
yaml_spec= None
externally_managed_exists= True
pip 26.0.1 from /opt/homebrew/lib/python3.14/site-packages/pip (python 3.14)
WARNING: Package(s) not found: PyYAML
```

### Unrelated Apple/Xcode Python package state

Apple/Xcode Python 3.9 can see a user-level PyYAML 6.0.2 installation required by another tool. It is unrelated global/user state and must not be consumed or changed by Codex Config Manager.

```text
executable= /Applications/Xcode.app/Contents/Developer/usr/bin/python3
version= 3.9.6 (default, Apr 30 2025, 02:07:17)  [Clang 17.0.0 (clang-1700.0.13.5)]
Name: PyYAML
Version: 6.0.2
Location: /Users/spowart/Library/Python/3.9/lib/python/site-packages
Required-by: ultralytics
```

### Repository Python state

No Python project or local environment existed during discovery.

```text
.venv exists= False
pyproject.toml exists= False
requirements.txt exists= False
requirements-dev.txt exists= False
Pipfile exists= False
poetry.lock exists= False
uv.lock exists= False
```

### Installed rsync reference

The observed Homebrew rsync is modern enough to demonstrate the expected capability class, but it is not self-contained and therefore cannot be copied into the project as the runtime tool.

```text
rsync  version 3.4.1  protocol version 32
Capabilities:
    64-bit files, 64-bit inums, 64-bit timestamps, 64-bit long ints,
    socketpairs, symlinks, symtimes, hardlinks, hardlink-specials,
    hardlink-symlinks, IPv6, atimes, batchfiles, inplace, append, ACLs,
    xattrs, optional secluded-args, iconv, no prealloc, stop-at, crtimes,
    file-flags
Checksum list:
    xxh128 xxh3 xxh64 (xxhash) md5 md4 sha1 none
Compress list:
    zstd lz4 zlibx zlib none
```

Its dynamic linkage proves that copying only `/opt/homebrew/bin/rsync` would retain Homebrew runtime dependencies:

```text
/opt/homebrew/opt/popt/lib/libpopt.0.dylib
/opt/homebrew/opt/lz4/lib/liblz4.1.dylib
/opt/homebrew/opt/zstd/lib/libzstd.1.dylib
/opt/homebrew/opt/xxhash/lib/libxxhash.0.dylib
/opt/homebrew/opt/openssl@3/lib/libcrypto.3.dylib
```

The installed Homebrew version was `3.4.1`; Homebrew metadata already described a newer stable formula version during inspection. This reinforces the distinction between an observed reference version and the project's deliberate upstream selection policy.

## Core execution-environment ownership

The acceptance principle is:

> After successful bootstrap, Homebrew can disappear and Codex Config Manager must continue to work. The sole permitted Homebrew-originating runtime exception is the compatible external Python interpreter itself.

The ownership layers are:

```text
EXTERNAL / PLATFORM OWNED

macOS
Apple Silicon as the currently validated architecture
compatible Python interpreter

OPTIONAL EXTERNAL BUILD / BOOTSTRAP TOOLING

Apple Command Line Tools and compiler toolchain

        ↓

REPOSITORY CONTRACT OWNED

Python compatibility policy
tested Python records
direct dependency declarations
runtime and development lock workflow
environment creation, validation and rebuild logic
rsync selection, source, version and SHA-256 contract
rsync build configuration and dependency closure
rsync integrity, linkage and functional validation
launchd environment resolution

        ↓

LOCAL REPOSITORY-OWNED GENERATED ENVIRONMENT

<repo-root>/.venv/
<repo-root>/.tools/
```

Git owns the recipe, policy, hashes, validation rules and rebuild process. The generated environment bytes remain local and ignored.

## Proposed Python-first repository topology

This is the intended structural lens for implementation. Directories should be created only when backed by real responsibilities; Mode C may consolidate very small modules without changing their ownership boundaries.

```text
codex-config-manager/
├── README.md
├── .gitignore
├── pyproject.toml
├── requirements/
│   ├── runtime.lock
│   └── development.lock
│
├── config/
│   ├── config.example.yaml
│   └── config.yaml                         # local and ignored
│
├── docs/
│   ├── bootstrap/
│   │   ├── 01-codex-config-manager-architecture-and-implementation-blueprint.md
│   │   └── 02-codex-config-manager-repository-and-operational-blueprint.md
│   ├── 01-implementation-discovery-managed-skill-ingestion-exclusions.md
│   ├── 02-implementation-discovery-python-runtime-environment-ownership.md
│   └── <subsequent active discovery and implementation documents>
│
├── latest/                                      # canonical transported snapshot
│   ├── AGENTS.md
│   └── skills/
│       └── <dynamically discovered user skills>
│
├── upload-ready/                                # deterministic human downloads
│   ├── global-agents.zip
│   └── skills/
│       └── <dynamic per-skill ZIPs>
│
├── src/                                         # Python application code
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
│
├── launchd/
│   ├── publisher/
│   │   └── <publisher plist template>
│   └── consumer/
│       └── <consumer plist template>
│
├── scripts/
│   ├── install.py
│   ├── uninstall.py
│   ├── status.py
│   └── validate.py
│
└── tests/
    ├── unit/
    │   ├── test_config.py
    │   ├── test_managed_scope.py
    │   ├── test_paths.py
    │   ├── test_rsync.py
    │   └── test_git.py
    ├── integration/
    │   ├── test_publisher.py
    │   └── test_consumer.py
    ├── simulation/
    │   ├── test_consumer_deployment.py
    │   ├── test_deletion_propagation.py
    │   └── test_excluded_content_protection.py
    └── fixtures/
        ├── publisher-source/
        ├── latest-state/
        └── consumer-target/
```

`latest/` and `src/` have deliberately different meanings:

```text
latest/             persistent Git-tracked managed snapshot
src/                Python implementation that transports and validates it
```

## Python application boundaries

The proposed modules own the following concerns:

| Module | Responsibility |
| --- | --- |
| `publisher.py` | Studio preflight, live-to-private-candidate comparison, `latest/` promotion, artifact/README projection, validation and scoped publication orchestration |
| `consumer.py` | Git update, `latest/` validation, latest-to-live comparison, deployment and verification orchestration |
| `config.py` | PyYAML loading, required-key checks, type validation and role-aware configuration |
| `managed_scope.py` | One reusable inclusion, exclusion and deletion boundary contract |
| `paths.py` | Canonical path resolution, containment and dangerous-target rejection |
| `rsync.py` | Exact local-tool resolution, argument construction, dry-run parsing and equivalence checks |
| `git.py` | Conservative Git inspection, path-scoped staging, commit and fetch/update primitives |
| `launchd.py` | Role-specific plist rendering, configured scheduling and deterministic paths |
| `locking.py` | Single-instance execution and stale-lock handling |
| `logging.py` | Metadata-focused operational logs without managed-file contents |
| `validation.py` | Environment, private-candidate, `latest/`, deployment and post-operation proofs shared where genuinely common |

Publisher and consumer own their control flows. Shared modules provide primitives and contracts rather than blending the two roles.

## Python command surface

`pyproject.toml` should install separate console commands conceptually equivalent to:

```text
codex-config-manager-publisher
codex-config-manager-consumer
codex-config-manager-install
codex-config-manager-uninstall
codex-config-manager-status
codex-config-manager-validate
```

The exact public names may be refined during implementation, but publisher and consumer must remain separately invocable and separately installable through launchd.

## Python compatibility policy

The project must distinguish three facts:

### Supported Python

The compatibility range accepted by the public project and declared in `pyproject.toml`. The exact range must be selected only after implementation tests; it must not be inferred from one machine's patch version.

### Tested Python

Exact interpreter versions against which the application, environment lifecycle and tests have actually passed. Tested versions are evidence, not the entire compatibility policy.

### Current Studio observation

Homebrew Python 3.14.4. It is the currently available implementation input, not a permanent exact public requirement.

Compatible patch upgrades should normally validate without unnecessary rebuilds. A broken interpreter link, incompatible major/minor, architecture mismatch, changed dependency contract or failed import/entry-point validation makes `.venv` stale.

## Python dependency-management workflow

One coherent workflow must own declaration, resolution, installation and deliberate updates.

### Authoritative declarations

`pyproject.toml` is authoritative for:

- project metadata;
- supported Python range;
- direct runtime dependencies;
- a development/test dependency extra or group;
- installed console entry points.

PyYAML is a direct runtime dependency. pytest and the chosen lock-generation tooling belong to development/test dependencies.

### Resolution and locking

The proposed minimal workflow uses a pinned `pip-tools` process:

```text
pyproject.toml direct dependencies
        ↓
pinned pip-tools resolver
        ↓
requirements/runtime.lock
requirements/development.lock
```

Both lock files must contain exact resolved closures and hashes. The runtime lock contains only operational requirements; the development lock contains the runtime closure plus pytest and declared development tooling.

The exact `pip-tools` version must itself be declared by the development dependency contract. It must not remain an undocumented command assumed to exist globally.

### Environment installation

Normal bootstrap consumes committed locks and must not resolve new versions:

```text
select compatible external Python
        ↓
create <repo-root>/.venv
        ↓
install exact hashed runtime or development lock
        ↓
install Codex Config Manager from the repository without re-resolving dependencies
        ↓
validate imports, commands and environment receipt
```

The Studio development environment installs the development closure. A future minimal consumer may install only the runtime closure.

### Deliberate dependency updates

An update is an explicit development operation:

```text
edit direct dependency policy
        ↓
resolve with the recorded lock tool
        ↓
regenerate both locks
        ↓
review dependency and hash changes
        ↓
rebuild a clean test environment
        ↓
run validation and tests
        ↓
commit the updated contract
```

Runtime must never update packages opportunistically.

## PyYAML contract

PyYAML is approved because the application is Python and YAML is the established public/private configuration format.

It must:

- exist only inside `.venv` for this project;
- never be taken from global, user, Apple/Xcode or unrelated environments;
- be installed from the tracked runtime dependency contract;
- be loaded with `yaml.safe_load()`;
- be followed by explicit required-key and type validation.

`yq` is not a Codex Config Manager runtime dependency. Its presence on the Studio is unrelated local tooling.

## pytest contract

pytest belongs to the development/test closure and must be installed in the repository-owned environment. It supports unit, integration and isolated consumer simulation tests.

A minimal consumer runtime need not carry pytest unless that installation is expected to perform the full validation suite. The Studio development environment should contain both runtime and development dependencies.

## Virtual-environment ownership and receipt

The actual `.venv` is local, generated and Git-ignored. The repository owns its complete reproducible recipe.

An environment receipt should record at least:

- selected interpreter path;
- Python version and implementation/cache tag;
- architecture;
- dependency-lock digest;
- installed project version or source identity;
- environment type: runtime or development;
- last successful validation.

The environment is stale or invalid when, for example:

- `.venv/bin/python` or an installed console entry point is missing or broken;
- the interpreter is outside the supported range;
- Python major/minor or architecture is incompatible;
- the relevant dependency-lock digest changed;
- required imports fail;
- installed console commands fail validation;
- the application/environment receipt no longer matches the repository contract.

### Rebuild policy

A tracked repair operation must be able to:

```text
detect stale or incompatible .venv
        ↓
remove only the bounded local .venv environment
        ↓
recreate it with a compatible external Python
        ↓
install the tracked dependency closure
        ↓
install the repository application
        ↓
validate imports and console commands
        ↓
run appropriate validation/tests
        ↓
write a successful environment receipt
        ↓
resume operation
```

The operator must never have to reconstruct historical package state manually.

Scheduled publisher/consumer execution should fail clearly on an invalid environment rather than silently performing an uncontrolled network rebuild. Repair or upgrade is a deliberate environment-management operation.

## rsync authority remains unchanged

Python orchestrates rsync; it does not replace it. rsync remains authoritative for recursive filesystem comparison, copy and bounded deletion.

The approved behaviour remains:

- `--checksum` for content-based comparison;
- `--dry-run` before mutation;
- `--itemize-changes` for machine-parseable differences;
- correct recursive and trailing-slash semantics;
- bounded `--delete` for legitimate managed deletion propagation;
- never `--delete-excluded`;
- `.system/**` excluded at ingestion;
- `.DS_Store` excluded globally;
- a second dry-run proving post-sync equivalence.

The same managed-scope contract must govern cheap detection, comparison, copying, validation, Git publication, consumer deployment, deletion and tests. Doc 1 owns the detailed ingestion exclusions.

## Final rsync source and version-selection contract

### macOS-native rsync

The macOS-provided native/system rsync must never be used. It is not an acceptable fallback, compatibility alternative or capability baseline.

### Homebrew rsync

The observed Homebrew rsync 3.4.1 is a capability/reference baseline only. It is:

- not the runtime source;
- not a permanent version pin;
- not a maximum permitted version;
- not a reason to downgrade or cap the project.

### Upstream selection

At initial tool selection or a deliberate future dependency refresh, prefer the latest suitable stable upstream rsync available at that decision point:

```text
latest suitable stable upstream release
        ↓
select exact release
        ↓
record version, source and SHA-256
        ↓
build/acquire in a controlled environment
        ↓
validate runtime isolation and required behaviour
        ↓
install as the fixed repository-owned rsync
```

"Latest" is a selection policy, not a runtime update policy. Once selected, the exact recorded, checksummed and validated build remains fixed until a deliberate dependency refresh. Publisher and consumer must never check continuously for rsync releases or upgrade automatically.

The exact first release cannot be recorded until the deliberate Mode C selection event verifies what is then upstream stable and suitable.

## Repository-owned rsync environment

The generated local layout should remain simple:

```text
<repo-root>/.tools/
└── rsync/
    ├── bin/
    │   └── rsync
    ├── lib/
    │   └── <any required non-system runtime libraries>
    └── build-receipt.json
```

There is no internal multi-version manager, `current` symlink, active-version file, runtime version switching or permanent rollback subsystem. A deliberate upgrade builds and validates a candidate in controlled temporary state, replaces the local rsync environment, records the new receipt and revalidates the project.

Python must execute exactly:

```text
<repo-root>/.tools/rsync/bin/rsync
```

It must never invoke an unqualified executable name or search `PATH`.

## rsync acquisition and build

The preferred acquisition is a pinned upstream source release rather than a copied Homebrew binary:

```text
select suitable stable upstream source
        ↓
record source URL and SHA-256 in Git
        ↓
download source during deliberate bootstrap/build
        ↓
verify SHA-256 before extraction/build
        ↓
build with accepted Apple bootstrap tooling
        ↓
install complete runtime beneath .tools/rsync
        ↓
validate linkage, integrity and behaviour
```

Apple Command Line Tools may be required to compile rsync and any unavoidable local supporting library. They are an external build/bootstrap dependency only and must not be required during normal publisher or consumer execution after `.tools/rsync` is valid.

Homebrew may assist an explicitly designed bootstrap step, but the preferred model does not use it for rsync acquisition. Homebrew must never remain part of the resulting rsync runtime dependency closure.

## rsync dependency closure

The source build should use the smallest feature set that satisfies project requirements. Optional dependencies such as OpenSSL acceleration, xxhash, LZ4 and Zstandard should be disabled when the required local comparison/copy behaviour does not need them.

If a required non-system library cannot be eliminated or statically linked, it must be:

- selected through a pinned, checksummed contract;
- built or acquired during controlled bootstrap;
- installed under `.tools/rsync/lib`;
- resolved through a local loader-relative path;
- recorded and hashed in `build-receipt.json`;
- included in recursive linkage and functional validation.

The complete runtime dependency graph may resolve only to macOS system frameworks/libraries or locally contained `.tools/rsync/lib` files. No Homebrew path or arbitrary external library is permitted.

## rsync build receipt

`build-receipt.json` should record enough truth to inspect and reproduce the local runtime, including as appropriate:

- exact rsync version;
- upstream source location;
- source SHA-256;
- build configuration and feature choices;
- build platform and architecture;
- compiler/toolchain identity;
- installed executable path and hash;
- local non-system library paths and hashes;
- dynamic-linkage validation result;
- required capability result;
- functional validation result;
- build/validation timestamp.

The receipt is generated local environment state and normally remains ignored. The source/version/hash/build policy that produces it is Git-tracked.

## rsync integrity, isolation and functional validation

Validation must prove:

- the executable resolves beneath `<repo-root>/.tools/rsync/bin`;
- its architecture is supported;
- its exact version and protocol meet the selected contract;
- its executable hash matches the receipt;
- every locally bundled library hash matches the receipt;
- required capabilities and flags exist;
- recursive dynamic linkage points only to macOS system libraries/frameworks or `.tools/rsync/lib`;
- no `/opt/homebrew`, Homebrew Cellar or other uncontrolled runtime path appears;
- checksum comparison detects content changes, including timestamp/size edge cases;
- dry-run produces no mutation;
- itemized output is parseable and truthful;
- no-op comparison produces no meaningful action;
- bounded deletion removes legitimate managed content;
- `.system/**` remains protected;
- `.DS_Store` remains protected;
- `--delete-excluded` is never constructed;
- a post-sync dry-run proves equivalence.

The environment must also pass the conceptual Homebrew-removal acceptance test:

```text
bootstrap completed successfully
        ↓
Homebrew rsync and its libraries unavailable
        ↓
project-local .venv remains functional
        +
project-local rsync and local non-system libraries remain functional
        ↓
publisher/consumer operations continue normally
```

The permitted exception is the compatible Python interpreter itself if it originated from Homebrew. Removing that interpreter naturally prevents Python execution.

## Configuration contract

The established public/private model remains:

```text
config/config.example.yaml     tracked complete public contract
config/config.yaml             ignored truthful machine configuration
```

The public template must describe the union of publisher and consumer capabilities. Any supported private key must have a safe public representation.

Initial scheduling remains configuration-owned:

```yaml
schedule:
  publisher_interval_seconds: 300
  consumer_interval_seconds: 300
```

The values are separate and may diverge later. The applicable role value is rendered into local launchd installation state; `300` is not an architectural constant embedded in application logic.

## Deterministic launchd runtime

The role-specific LaunchAgent must execute an absolute repository-local console command:

```text
<repo-root>/.venv/bin/codex-config-manager-publisher
```

or:

```text
<repo-root>/.venv/bin/codex-config-manager-consumer
```

The Python application then resolves:

```text
<repo-root>/.tools/rsync/bin/rsync
<repo-root>/config/config.yaml
<configured runtime-state path>
<configured log path>
```

Launchd and application execution must not depend on:

- shell activation;
- interactive `PATH`;
- shell aliases;
- global or user Python packages;
- Apple/Xcode Python packages;
- arbitrary rsync resolution;
- Homebrew runtime packages other than the permitted Python interpreter.

The Mac Studio installs only the publisher LaunchAgent. The Mac Mini installs only the consumer LaunchAgent. Both role templates remain public repository content.

## Local generated state

The expected local-only surfaces are:

```text
<repo-root>/
├── .venv/
├── .tools/
└── config/
    └── config.yaml

~/Library/Application Support/codex-config-manager/
├── locks/
└── runtime-state/

~/Library/Logs/codex-config-manager/
├── publisher.log
└── consumer.log

~/Library/LaunchAgents/
└── <generated role-specific plist>
```

These are local installation truth, not public repository state.

## Git-tracked and Git-ignored environment surfaces

### Git-tracked contract

- `pyproject.toml`;
- runtime and development dependency locks;
- supported and tested Python policy;
- environment bootstrap, validation and repair logic;
- rsync selection/source/version/SHA-256 contract;
- rsync build and acquisition recipe;
- rsync capability and linkage rules;
- application code and console entry points;
- launchd templates;
- public configuration template;
- tests and suitable public fixtures;
- dependency, environment and operational documentation.

### Git-ignored generated/private state

- `.venv/`;
- `.tools/`;
- Python bytecode and caches;
- pytest and tool caches;
- `config/config.yaml`;
- runtime state and locks;
- logs;
- generated LaunchAgent installation state;
- `.DS_Store` everywhere.

The repository tracks the complete reusable system, not only `latest/`. Automated publisher commits remain more narrowly bounded than public project contents.

## Automated Git publication boundary

Normal human/AI development commits may update all appropriate public implementation, test, launchd, configuration-template and documentation surfaces.

The unattended publisher may stage and commit only:

```text
latest/**
upload-ready/global-agents.zip
upload-ready/skills/<validated dynamic skill ZIP set>
README.md                              bounded generated download section only
```

It must never use `git add .`, sweep unrelated development work into a managed-state commit or confuse the automated publication boundary with the wider public repository boundary.

Preflight and post-sync Git validation must stop on unsafe, divergent or ambiguous state and verify every staged path before commit.

## Test and simulation coverage

The Studio development environment should use pytest to prove:

- supported Python and environment-receipt validation;
- runtime versus development dependency installation;
- configuration safe loading, required keys and types;
- configured-role enforcement;
- canonical path containment and dangerous-target rejection;
- dynamic current and future user-skill discovery;
- `.system/**` ingestion exclusion and preservation;
- `.DS_Store` global exclusion and preservation;
- checksum-based comparison;
- dry-run and itemized-output handling;
- no-op behaviour;
- automatic bounded managed deletion;
- protected excluded content during deletion;
- post-sync equivalence;
- exact repository-local rsync resolution;
- rsync hash, linkage, capability and Homebrew-isolation checks;
- conservative Git path restrictions and unsafe-state rejection;
- publisher orchestration;
- consumer deployment into temporary targets;
- unmanaged sentinel preservation;
- launchd template rendering with configured role intervals.

Tests should create `.system` and `.DS_Store` conditions inside temporary directories at runtime rather than publishing real excluded content as managed fixtures.

Studio consumer simulation must never target the Studio's authoritative live `~/.codex`.

## Machine ownership and validation boundary

### Mac Studio

The Studio remains responsible for:

- initial architecture and repository bootstrap;
- Python project establishment;
- environment-contract implementation;
- publisher implementation and real validation;
- repository-local rsync build and isolation proof;
- public configuration contract;
- both launchd templates and publisher installation;
- consumer implementation contract and isolated simulation;
- permanent documentation as implementation becomes truthful;
- bounded Mac Mini handoff.

### Mac Mini

The Mini remains responsible for:

- creating its local consumer `.venv` and `.tools` from the tracked contract;
- real Git/authentication validation;
- real consumer launchd installation;
- real local deployment and filesystem validation;
- bounded consumer-specific refinements;
- contributing truthful findings to the same canonical repository.

It must not independently redefine publisher behaviour, shared architecture, `latest/` snapshot semantics, managed scope or environment ownership.

## Implementation sequence implied by this discovery

When Mode C is explicitly authorised, a safe high-level sequence is:

1. Establish Git and the minimal tracked Python project structure.
2. Define the supported Python policy, direct dependencies and exact lock workflow.
3. Implement bounded environment bootstrap, receipt, validation and repair.
4. Select the then-latest suitable stable upstream rsync release and record its exact source/hash contract.
5. Build the simple local `.tools/rsync` runtime with complete non-system dependency isolation.
6. Prove rsync integrity, linkage, required capabilities and filesystem safety behaviour.
7. Implement shared Python contracts, then separate publisher and consumer orchestration.
8. Establish the public/private configuration model and local Studio publisher configuration.
9. Establish private candidate construction and root-level `latest/` using the Doc 1 ingestion boundary and Doc 8 promotion contract.
10. Implement and validate conservative automated Git publication.
11. Build unit, integration and Studio consumer-simulation tests.
12. Render, install and validate only the Studio publisher LaunchAgent after deletion and environment safety tests pass.
13. Create permanent implementation/operations/dependency documentation from actual evidence.
14. Produce the bounded Mac Mini handoff.

This sequence is directional, not proof that any stage currently exists.

## Remaining implementation proofs

No unresolved operator-policy decision remains in this discovery. Mode C must still establish evidence for:

- the supported Python range;
- exact tested Python versions;
- exact PyYAML, pytest and lock-tool versions;
- the first selected latest suitable stable upstream rsync release;
- the minimal rsync build configuration;
- whether required non-system rsync libraries can be eliminated, statically linked or must be bundled locally;
- correct macOS loader-relative linkage and code-signing behaviour where applicable;
- environment rebuild and Homebrew-removal acceptance tests;
- real launchd behaviour on the Studio;
- real consumer behaviour later on the Mini.

If rsync cannot satisfy the agreed runtime boundary using only macOS system libraries and locally contained `.tools/rsync/lib` dependencies, implementation must stop and return the evidence for operator review rather than silently expanding the runtime boundary.

## Current implementation status

- ✅ The Python direction, dependency ownership and rsync environment contracts are operator-approved and durably recorded here.
- ✅ The bootstrap architecture and Doc 1 managed-scope discovery remain in force.
- ▶ The next authorised phase is Mode C implementation against this combined contract.
- ⛔ No code, dependency state, `.venv`, `.tools`, `latest/` payload, Git bootstrap or launchd service is created by this document.
