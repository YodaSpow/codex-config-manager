# Codex Config Manager — Architecture & Implementation Blueprint

**Repository:** `codex-config-manager`  
**GitHub:** [YodaSpow/codex-config-manager](https://github.com/YodaSpow/codex-config-manager)  
**Primary local repository path:** `/Users/spowart/Scripts/codex-config-manager`  
**Primary authoring machine:** Mac Studio  
**Initial consumer machine:** Mac mini  
**Platform:** macOS / Apple Silicon  
**Status:** Architecture defined; implementation not yet started

---

## 1. Purpose

`codex-config-manager` is intended to provide a controlled, headless way to publish and distribute a deliberately limited subset of the global Codex configuration between Macs.

The immediate requirement is:

**Mac Studio → GitHub → Mac mini**

The Mac Studio is the primary AI-development and authoring machine. Its live Codex configuration is the authoritative source for the managed assets.

The Mac mini should be able to consume the published state automatically without depending on the Mac Studio being online, mounted, reachable over the network, or sharing files directly.

The project must therefore avoid cross-machine hard links, symlinks, mounted-folder dependencies, or other mechanisms that leave one Mac operationally dependent on another.

GitHub acts as the durable transport and published source between independently functioning machines.

The project is deliberately broader than a simple sync script. The repository should ultimately contain:

1. The managed Codex assets being distributed.
2. The publisher machinery.
3. The consumer machinery.
4. Shared/configuration logic required by both roles.
5. Architecture and implementation documentation.
6. A reusable handoff/onboarding surface for future AI sessions and potentially other machines/users.

The repository should therefore become the complete, living representation of the system rather than merely the transport location for two copied Codex assets.

---

# 2. Core Architecture

The system follows a one-project, two-role model.

The same `codex-config-manager` repository exists on each participating Mac.

Each installation declares its role explicitly through local configuration rather than attempting to infer its identity from hostname, hardware, path, or other environmental characteristics.

The two initial roles are:

| Machine | Role | Primary responsibility |
|---|---|---|
| Mac Studio | `publisher` | Capture the authoritative Codex assets and publish them |
| Mac mini | `consumer` | Retrieve the published state and deploy it into its own Codex environment |

Future machines may also operate as consumers.

The architecture should therefore not assume that there will only ever be one consumer.

---

# 3. Confirmed Local Repository Paths

Both existing Macs use the same user and Scripts layout.

## Mac Studio

```text
/Users/spowart/Scripts/codex-config-manager
```

Current initial structure:

```text
codex-config-manager/
└── docs/
```

## Mac mini

```text
/Users/spowart/Scripts/codex-config-manager
```

Current initial structure:

```text
codex-config-manager/
└── docs/
```

This symmetry is useful but should not become an implicit machine-identification mechanism.

The application should remain configurable rather than assuming that identical paths will exist forever.

---

# 4. GitHub Repository

The canonical remote repository is:

```text
https://github.com/YodaSpow/codex-config-manager
```

The repository is public.

GitHub Pages has also been enabled from the `main` branch, giving the project the ability to develop a public documentation surface later.

GitHub is not merely a temporary relay between the two Macs.

It should ultimately contain the complete reusable project:

- orchestration code;
- publisher implementation;
- consumer implementation;
- shared implementation;
- managed public Codex assets;
- documentation;
- installation guidance;
- handoff guidance.

Machine-specific operational state must remain local.

---

# 5. Authoritative Codex Source

The confirmed global Codex location on the Mac Studio is:

```text
/Users/spowart/.codex
```

The directory currently contains many different Codex-owned surfaces, including:

```text
AGENTS-history
AGENTS.md
archived_sessions
attachments
auth.json
browser
cache
computer-use
config.toml
dictation-history
generated_images
goals_1.sqlite
installation_id
ipc
logs_2.sqlite
logs_2.sqlite-shm
logs_2.sqlite-wal
memories
memories_1.sqlite
models_cache.json
node_repl
operator-notes
pets
plugins
process_manager
queue_1.sqlite
realtime-voice-continuity.json
rules
session_index.jsonl
sessions
shell_snapshots
skills
sqlite
state_5.sqlite
thread-writer-locks
tmp
transcription-history.jsonl
validation-env
vendor_imports
visualizations
```

This inventory establishes an important architectural boundary.

**The project must never treat `/Users/spowart/.codex` as a directory to synchronise wholesale.**

Only two explicitly whitelisted surfaces are managed.

---

# 6. Strict Managed-Asset Whitelist

The only Codex assets in scope are:

```text
/Users/spowart/.codex/AGENTS.md
```

and:

```text
/Users/spowart/.codex/skills/
```

Nothing else inside `.codex` is in scope.

This must be implemented as a **whitelist**, not a blacklist.

The correct rule is:

> If a Codex path has not been explicitly declared as managed, Codex Config Manager must not touch it.

This protects the project from:

- accidentally publishing authentication material;
- copying databases or application state;
- exposing histories, memories, sessions or attachments;
- future additions to `.codex` unexpectedly becoming synchronised;
- application changes upstream expanding the project's scope without explicit approval.

The implementation should therefore identify the two allowed paths positively rather than copying `.codex` and excluding known unwanted files.

---

# 7. `AGENTS.md`

`AGENTS.md` is a single managed file.

On the publisher it originates from:

```text
/Users/spowart/.codex/AGENTS.md
```

It should be copied into the managed repository representation.

On a consumer it should ultimately be deployed to:

```text
/Users/spowart/.codex/AGENTS.md
```

The live Mac Studio copy remains authoritative during normal operation.

The transported global `AGENTS.md` must not be confused with a repository-level `AGENTS.md`.

A future repository-level `AGENTS.md`, if one is ever introduced, would govern the `codex-config-manager` repository itself.

The transported global file therefore requires its own managed repository location rather than occupying the repository root.

The detailed repository topology for that distinction is defined by the repository and operational blueprint.

---

# 8. `skills/` Is a Managed Tree

The Mac Studio currently contains:

```text
/Users/spowart/.codex/skills
```

with the observed structure:

```text
skills/
├── chat-handoff/
│   ├── SKILL.md
│   └── agents/
│       └── openai.yaml
├── operational-modes/
│   ├── SKILL.md
│   └── agents/
│       └── openai.yaml
└── semantic-compression/
    ├── SKILL.md
    └── agents/
        └── openai.yaml
```

This establishes another important implementation principle:

> `skills/` is an opaque recursive tree.

Codex Config Manager should not need to understand what constitutes a skill internally.

It should not assume that a skill consists only of `SKILL.md`, `agents/openai.yaml`, or the structure currently observed.

Instead, everything below the managed `skills/` root must be recursively preserved.

If future skills contain additional directories, files, dependencies, assets or other structures, those should naturally travel with the tree without requiring changes to Codex Config Manager.

The publisher therefore copies the complete managed tree recursively.

The consumer restores the complete managed tree recursively.

The system transports the tree; it does not interpret it.

---

# 9. Mac Studio — Publisher Role

The Mac Studio is the initial lead implementation machine and authoritative authoring environment.

Its live Codex state is the source of truth for:

```text
~/.codex/AGENTS.md
~/.codex/skills/
```

The publisher should operate headlessly.

Conceptually:

```text
Mac Studio live .codex
        │
        │ whitelist capture
        ▼
codex-config-manager managed representation
        │
        │ Git commit/push when changed
        ▼
GitHub
```

The publisher should:

1. Observe or periodically evaluate the two managed source surfaces.
2. Determine whether their effective contents have changed.
3. Copy the current authoritative state into the repository's managed representation.
4. Preserve the complete recursive `skills/` structure.
5. Determine whether the repository now contains a real Git diff.
6. Commit only when a meaningful change exists.
7. Push the new published state to GitHub.
8. Do nothing when there has been no change.

The architecture originally left the exact implementation mechanism open to implementation-time validation.

Subsequent repository planning has refined that expectation: a lightweight trigger should initiate authoritative recursive comparison, with `rsync` used to determine whether a meaningful managed difference actually exists.

The architectural requirement remains:

**Publishing must be headless, deterministic and change-driven.**

---

# 10. Mac mini — Consumer Role

The Mac mini is the first consumer.

Conceptually:

```text
GitHub
   │
   │ fetch/pull
   ▼
local codex-config-manager
   │
   │ deploy whitelist
   ▼
Mac mini ~/.codex
```

The consumer should periodically check the GitHub-backed local repository for a newer published state.

When nothing has changed, it should leave the local Codex environment untouched.

When a new published state exists, it should:

1. Safely update its local repository.
2. Deploy the published `AGENTS.md`.
3. Recursively deploy the complete published `skills/` tree.
4. Touch no other `.codex` surfaces.
5. Record useful operational information in logs.

Once deployed, the Mac mini owns real local files.

It is **not** using files remotely from the Mac Studio.

It therefore continues operating normally if:

- the Mac Studio is switched off;
- the Mac Studio is asleep;
- the Macs cannot see one another over the LAN;
- the Studio repository is unavailable locally;
- a network share is disconnected.

Only GitHub connectivity is required when checking for new versions.

The most recently deployed state remains local and usable regardless.

---

# 11. Why Hard Links Are Not Used

The original question considered hard-linking Codex configuration between the Macs.

That is not suitable.

Hard links do not provide the required cross-machine architecture and introduce filesystem constraints that are fundamentally incompatible with this use case.

More importantly, they would create the wrong dependency model.

The Mac mini should not consume the Mac Studio's live files.

It should consume a **published state**.

That distinction is fundamental.

---

# 12. Why Symlinks Are Not Used

Symlinks could point one local path towards another directory, including potentially a mounted remote filesystem.

They are still undesirable here.

A symlink-based architecture would make the consumer dependent on the target remaining reachable and would blur the separation between:

- authoring;
- publishing;
- transport;
- deployment.

The chosen architecture instead gives every consumer real local files.

This is intentionally closer to software deployment than filesystem sharing.

---

# 13. GitHub as Published State

The intended lifecycle is:

```text
AUTHOR
Mac Studio ~/.codex
        │
        ▼
PUBLISH
Mac Studio codex-config-manager
        │
        ▼
TRANSPORT / SOURCE OF PUBLISHED STATE
GitHub
        │
        ▼
CONSUME
Mac mini codex-config-manager
        │
        ▼
DEPLOY
Mac mini ~/.codex
```

This means the Mac mini depends on the **published state**, not on the Mac Studio itself.

That makes the architecture portable.

A future machine can become another consumer without requiring direct access to the Mac Studio.

---

# 14. One Repository, Two Operational Roles

The project should not become separate publisher and consumer repositories.

There should be one codebase.

A conceptual architecture requires:

```text
codex-config-manager/
├── README.md
├── docs/
├── publisher-capable implementation
├── consumer-capable implementation
├── shared implementation
├── configuration
└── managed published state
```

This is an architectural requirement rather than a frozen physical folder layout.

The more specific repository topology is defined by the repository and operational blueprint.

The important principle is:

> One project, one architecture, multiple explicitly configured roles.

Publisher and consumer remain separate operational workflows even though they belong to the same project.

---

# 15. Managed Assets and Orchestration Both Belong in the Repository

A crucial design distinction emerged during planning.

The repository must not contain only the final copied `skills/` and `AGENTS.md`.

That would capture the payload while losing the most valuable part of the project: the system that publishes and consumes it.

The repository should ultimately contain both:

### Managed state

The published Codex assets:

```text
global AGENTS.md representation
skills/
```

### Orchestration

The implementation responsible for:

- discovering changes;
- copying managed assets;
- validating scope;
- Git operations;
- publisher scheduling;
- consumer polling;
- consumer deployment;
- logging;
- configuration;
- installation;
- recovery;
- future-machine onboarding.

This makes GitHub the living representation of **Codex Config Manager**, not merely a bucket containing copied configuration.

The physical managed-state location must respect the repository `AGENTS.md` namespace boundary defined elsewhere in the project blueprint.

---

# 16. Machine Configuration

Machine role must be explicitly configured.

Do not infer it from:

- hostname;
- hardware model;
- filesystem paths;
- presence of certain files;
- network identity.

A local YAML configuration is preferred.

Conceptually:

```yaml
# Machine identity used for operator visibility and logging.
machine_id: mac-studio

# Valid roles:
#   publisher - capture local managed Codex state and publish it
#   consumer  - retrieve published state and deploy it locally
role: publisher
```

The Mac mini would instead use:

```yaml
# Machine identity used for operator visibility and logging.
machine_id: mac-mini

# Valid roles:
#   publisher - capture local managed Codex state and publish it
#   consumer  - retrieve published state and deploy it locally
role: consumer
```

Comments are deliberately valuable here.

They are not machine-readable authority.

They exist as a **human operator guide**, allowing configuration to be understood and changed without requiring an AI to inspect the source code.

The YAML values remain authoritative.

---

# 17. Local Configuration Should Not Define Public Machine State

The repository should contain:

- configuration defaults;
- example configuration;
- documentation of supported roles;
- code capable of operating in either role.

It should not require the public repository to declare that Nicholas's specific Mac Studio is the publisher or Mac mini is the consumer.

Machine identity is installation state.

The reusable project should instead say:

> This software can operate as a publisher or consumer. The local operator explicitly chooses the role.

This is essential if the project is later used on additional machines or by another person.

The public configuration template must expose the supported configuration contract without exposing private or machine-specific values.

The local configuration file contains the truthful machine-specific implementation of that public contract.

---

# 18. Publisher Must Not Automatically Consume

The Mac Studio may technically contain consumer-capable code because both roles belong to the shared project.

However:

> The authoritative publisher must not automatically consume its own published state.

For the initial deployment:

```text
Mac Studio:
publisher = enabled
consumer  = disabled
```

and:

```text
Mac mini:
publisher = disabled
consumer  = enabled
```

This is an important loop-prevention and data-protection boundary.

The Mac Studio's live `.codex` state is authoritative.

Automatically pulling GitHub state back over that live authoring environment could:

- overwrite newer local work;
- reintroduce stale state;
- create publisher/consumer loops;
- make provenance ambiguous;
- turn recovery behaviour into normal behaviour.

Therefore, normal Studio operation is one-way.

---

# 19. Publisher Recovery Is Manual

There is still value in GitHub acting as a backup/recovery source for the Mac Studio.

If the Studio loses its managed Codex files, the published state may be useful for recovery.

That recovery path should be **explicit and human-triggered**.

It must not run automatically.

The project may eventually expose a safe recovery command or documented procedure, but recovery remains an operator action.

This preserves the principle:

> Authoring flows outward automatically. Recovery flows inward deliberately.

---

# 20. Headless Operation

Normal operation should require no GUI interaction.

Both roles should eventually run silently in the background.

On macOS, `launchd` / LaunchAgents are the intended orchestration surface unless implementation proves a concrete reason to use another mechanism.

The intended experience is:

### Publisher

A skill or `AGENTS.md` changes.

A lightweight trigger causes the publisher to verify the effective managed state recursively.

If the managed state has genuinely changed, the persistent repository representation is updated and the new state is published.

No action is required when nothing changed.

### Consumer

A new published state appears on GitHub.

The consumer discovers it during its next scheduled check.

If the repository has advanced, it updates its local checkout, verifies the managed staged state, determines whether deployment is actually required, and deploys only the managed surfaces.

No action is required when nothing changed.

The detailed launchd topology and execution flow belong in the repository and operational blueprint and, once built, in truthful implementation documentation.

---

# 21. Avoid No-Op Git Noise

Periodic execution must not imply periodic commits.

The publisher should only commit when the managed representation has materially changed.

Likewise, the consumer should not rewrite live Codex files merely because its scheduled job ran.

The desired behaviour is idempotent:

```text
no change → no meaningful action
```

This keeps:

- Git history meaningful;
- logs useful;
- filesystem writes low;
- operational behaviour predictable.

Git is responsible for versioning published state.

It should not be used as a substitute for authoritative recursive managed-file comparison on the publisher.

Likewise, a consumer detecting a newer Git revision does not automatically imply that every managed live file requires rewriting.

---

# 22. Public Repository and Privacy Boundary

The repository is public.

A manual review has already confirmed that the currently intended managed assets are suitable for public publication.

However, privacy review remains an **authoring responsibility**, not something the publisher should attempt to infer automatically.

The system should remain deliberately simple:

> Publish exactly the explicitly managed assets.

It should not attempt semantic inspection or automatic redaction of skill contents.

Before introducing future skills or changes that contain sensitive material, the human author is responsible for determining whether they are appropriate for the public repository.

This should eventually be captured as operator guidance.

Machine-specific configuration must remain outside the public repository wherever it contains truthful local values.

A public example configuration should document the supported shape without publishing private machine details.

---

# 23. Documentation Is Part of the Product

The `docs/` directory is not temporary scaffolding.

Documentation should live with the code and evolve with it.

The repository documentation should eventually cover:

- architecture;
- installation;
- configuration;
- publisher setup;
- consumer setup;
- operations;
- troubleshooting;
- recovery;
- safety boundaries;
- handoff to future AI sessions.

GitHub Pages may provide a public-facing rendering of this documentation.

The repository itself remains the canonical source.

The initial bootstrap documents used to create the project may later be archived once the implementation has produced truthful permanent documentation.

They should not be deleted or silently replaced until the operator is satisfied that the implemented repository documentation fully supersedes them.

---

# 24. AI Handoff Should Become a Repository Feature

A particularly useful future addition is a dedicated handoff document stored inside the repository.

Its purpose is to allow a new AI session to understand the current project without requiring a massive external prompt.

Conceptually, a future user should be able to point an AI at the repository and say:

> Read the project handoff and continue from the current state.

The repository itself should explain:

- what the project is;
- the architecture;
- what has been implemented;
- what remains;
- whether the current machine should be configured as publisher or consumer;
- relevant validation expectations;
- where deeper documentation lives.

This is valuable for the initial Mac Studio → Mac mini handoff, but the principle is deliberately broader than those two machines.

A future AI should not have to reconstruct the project's intent from scripts, Git history or filenames.

The repository should expose enough authoritative documentation for an AI to distinguish:

- architectural invariants;
- current implementation;
- machine-specific configuration;
- publisher-owned responsibilities;
- consumer-owned responsibilities;
- explicitly permitted extension points;
- areas that must not be redesigned casually.

The Mac Studio is responsible for establishing this handoff model during the initial build.

The Mac mini should subsequently receive a repository that already explains its expected consumer role and its implementation boundaries.

The Mac mini may contribute truthful implementation findings from the real consumer environment, but those changes must remain within the established architectural contract unless the architecture is deliberately revisited.

---

# 25. Mac Studio Is the Initial Architecture and Implementation Lead

The Mac Studio is not merely the first publisher.

It is the machine on which the initial complete project structure is established.

The Mac Studio implementation should therefore consider the needs of both roles from the beginning.

It should:

1. Implement and validate the publisher lane against the real Mac Studio.
2. Establish the repository structure required by both publisher and consumer.
3. Establish the public configuration contract.
4. Establish the publisher-specific local configuration.
5. Establish the consumer configuration shape without inventing private Mac mini values that have not yet been validated.
6. Establish separate publisher and consumer orchestration surfaces.
7. Establish shared primitives only where genuine implementation reuse exists.
8. Establish launchd structure for both roles.
9. Establish tests for the publisher.
10. Establish consumer contract tests and simulation where possible.
11. Create the structural consumer lane before handing the repository to the Mac mini.
12. Document what has actually been implemented.
13. Document what remains intentionally deferred to real Mac mini validation.
14. Prepare a bounded consumer handoff.

The Studio therefore builds **for the system**, not merely for itself.

---

# 26. Mac Mini Is a Bounded Consumer Implementation Environment

The Mac mini is not intended to become a second independent architecture authority.

Its role is to consume the project structure produced by the Mac Studio and prove the consumer lane against a real downstream machine.

The Mac mini may legitimately discover realities that the Studio cannot fully prove in simulation, including:

- actual launchd behaviour on the consumer;
- consumer Git-fetch and pull behaviour;
- local deployment behaviour;
- filesystem permissions or environment differences;
- logging requirements;
- consumer-specific installation realities;
- consumer-specific configuration needs;
- deployment verification behaviour.

Those discoveries are valuable.

However, they must not cause the Mac mini implementation to silently redefine:

- source-of-truth direction;
- staging semantics;
- publisher behaviour;
- the global managed-asset allowlist;
- role semantics;
- shared architecture;
- repository topology;
- public configuration contract;
- architectural documentation.

If a real consumer requirement exposes an architectural deficiency, that must be treated as a deliberate architecture change rather than silently solved through consumer-side drift.

---

# 27. Consumer Simulation on the Mac Studio

The Mac Studio should prepare for the Mac mini by testing the consumer contract as far as possible without turning the Studio into an actual consumer.

This is a **simulation and contract-validation lane**, not normal consumer operation.

The Mac Studio should be able to exercise the consumer logic against controlled fixtures or temporary targets.

Conceptually:

```text
known published staged state
        ↓
consumer validation
        ↓
consumer rsync dry-run
        ↓
temporary/fake Codex target
        ↓
verification
```

The consumer simulation must never automatically deploy GitHub state back into the Studio's live authoritative:

```text
/Users/spowart/.codex
```

The purpose is to prove:

- that the consumer implementation can interpret the published repository state;
- that the correct managed assets are selected;
- that recursive `skills/` behaviour works;
- that global `AGENTS.md` is deployed to the correct semantic destination;
- that no unmanaged `.codex` surfaces are touched;
- that no-op behaviour works;
- that the consumer implementation is structurally viable before Mac mini handoff.

This reduces the amount of architectural discovery that must occur later on the Mac mini.

---

# 28. Change Detection Must Not Depend on Parent Directory Timestamps

A specific macOS filesystem consideration applies to the recursive `skills/` tree.

A modification deep within:

```text
~/.codex/skills/<skill>/...
```

cannot be assumed to produce a reliable modification timestamp change on:

```text
~/.codex/skills/
```

The publisher must therefore not use the root `skills/` directory timestamp as authoritative proof that the tree is unchanged.

The intended architecture separates:

1. **Cheap triggering**
2. **Authoritative comparison**

A lightweight mechanism may decide that verification should run.

That trigger does not establish truth.

The authoritative comparison must recursively inspect the managed state.

`rsync` is the expected mechanism for that recursive comparison.

Conceptually:

```text
possible change
      ↓
rsync dry-run
      ↓
real managed difference?
```

If no managed difference exists:

```text
stop
```

If a real managed difference exists:

```text
real rsync
   ↓
validate
   ↓
git diff
   ↓
commit
   ↓
push
```

This principle allows newly added skills, nested files, new directories and future skill structures to participate naturally without being individually enumerated.

---

# 29. Persistent Staged State

The publisher needs a persistent repository-backed representation of the last published managed state.

This state must survive:

- individual publisher executions;
- logouts;
- reboots;
- periods with no changes.

It must not be treated as disposable temporary storage.

The Mac Studio compares:

```text
LIVE AUTHORITATIVE CODEX STATE
            vs
PERSISTENT REPOSITORY STAGED STATE
```

The consumer uses the same published staged state through a different lens.

After Git updates its local repository, the Mac mini compares:

```text
LATEST LOCALLY CHECKED-OUT PUBLISHED STATE
            vs
CURRENT LIVE CONSUMER CODEX STATE
```

The detailed physical repository location of this staged state is defined in the repository and operational blueprint.

The architectural requirement is:

> There is one persistent published representation of the managed payload, versioned by Git and consumed downstream.

There should not be independent publisher and consumer copies of the canonical payload inside the same repository.

---

# 30. rsync Is a Transport Primitive, Not the Source of Truth

`rsync` is expected to play a central role in both operational lanes.

On the publisher:

```text
live Mac Studio .codex
        ↓
rsync
        ↓
persistent staged state
```

On the consumer:

```text
persistent staged state
        ↓
rsync
        ↓
live Mac mini .codex
```

The direction is role-specific.

The source of truth remains role-specific:

### Publisher

```text
Mac Studio live ~/.codex
```

### Consumer

```text
published repository state
```

`rsync` performs comparison and copying.

It does not determine architectural authority.

Publisher rsync must never mutate the live authoritative source.

Consumer rsync must never broaden deployment beyond the explicitly managed surfaces.

Copy semantics are fundamental.

The system is not designed around moving files from one location to another.

---

# 31. Deletion Semantics Must Be Deliberate

A persistent mirror introduces an important implementation question:

What should happen when a managed file or skill is deliberately deleted from the publisher's authoritative live state?

That behaviour must be decided deliberately during implementation.

The project must not accidentally infer destructive behaviour simply from the use of the term `mirror` or from a particular rsync flag.

Before unattended deletion propagation is enabled, implementation must define and document:

- whether deletion is propagated;
- how deletion is detected;
- whether deleted staged files are removed automatically;
- whether Git clearly records the deletion;
- how consumers deploy intentional deletions;
- whether any safety gate or validation is required;
- how accidental deletion can be recovered.

Until that behaviour is explicitly implemented and validated, the architecture should favour preservation over silent destructive assumptions.

---

# 32. Configuration Contract

The reusable public project requires a public configuration contract and private local configuration.

Conceptually:

```text
config/
├── config.example.yaml
└── config.yaml
```

`config.example.yaml` is Git tracked.

It documents:

- valid roles;
- supported paths;
- required configuration keys;
- human-readable comments;
- safe placeholder values;
- publisher and consumer requirements.

`config.yaml` is local machine state.

It contains the truthful values for the current installation and must be excluded from Git.

Every supported private configuration capability must have a safe public representation in the example configuration.

A machine must not silently invent private configuration keys that do not exist in the public contract.

This applies equally to Mac Studio and Mac mini.

If consumer implementation reveals a legitimate new configuration requirement, the public configuration contract must be updated as part of that change.

---

# 33. Separate Publisher and Consumer Executables

Publisher and consumer responsibilities are sufficiently different that they should not be collapsed into one large executable whose behaviour changes entirely through a role switch.

The repository should contain separate operational entry points for:

```text
publisher
consumer
```

They may share common utilities where doing so genuinely reduces duplication without coupling their control flows.

The exact physical structure is defined more specifically by the repository and operational blueprint.

Architecturally:

- publisher execution belongs to the publisher role;
- consumer execution belongs to the consumer role;
- shared primitives may be reused;
- installing one role must not accidentally activate the other.

This reduces the risk that consumer implementation changes unexpectedly alter publisher control flow or vice versa.

---

# 34. launchd Has Separate Role Lanes

Headless operation exists on both sides.

The publisher and consumer therefore require separate launchd responsibilities.

### Publisher launchd

Conceptually:

```text
trigger publisher
      ↓
cheap detection
      ↓
authoritative recursive verification
      ↓
publish only if required
```

### Consumer launchd

Conceptually:

```text
periodic consumer trigger
      ↓
check Git remote
      ↓
update local published state if required
      ↓
verify managed difference
      ↓
deploy only if required
```

The Mac Studio installs or enables only publisher orchestration.

The Mac mini installs or enables only consumer orchestration.

The project repository should nevertheless contain the machinery required for both so the complete system remains public, reproducible and reusable.

---

# 35. Documentation Lifecycle

The bootstrap documentation serves as the initial design authority before implementation exists.

It should guide the first Mac Studio implementation.

Once real implementation exists, the repository should produce permanent documentation reflecting reality rather than continuing indefinitely to treat pre-implementation assumptions as current truth.

The intended documentation lifecycle is:

```text
BOOTSTRAP ARCHITECTURE
        +
BOOTSTRAP REPOSITORY/OPERATIONAL BLUEPRINT
        ↓
MAC STUDIO IMPLEMENTATION
        ↓
TRUTHFUL REPOSITORY DOCUMENTATION
        ↓
MAC MINI HANDOFF
        ↓
CONSUMER VALIDATION / BOUNDED REFINEMENT
        ↓
UPDATED TRUTHFUL REPOSITORY DOCUMENTATION
```

The bootstrap documents should be preserved until the operator is satisfied that their responsibilities have been superseded.

They may then be archived rather than silently deleted.

---

# 36. Relationship to the Repository & Operational Blueprint

This architecture document and the companion repository/operational blueprint are complementary.

This document defines:

- the purpose of the project;
- architectural authority;
- managed-surface scope;
- source-of-truth direction;
- publisher and consumer roles;
- safety invariants;
- headless-operation intent;
- portability requirements;
- anti-loop behaviour;
- documentation and handoff principles.

The repository and operational blueprint defines the more specific current intended shape for:

- repository topology;
- persistent staging location;
- `AGENTS.md` namespace separation;
- publisher executable location;
- consumer executable location;
- shared helper structure;
- local and example configuration;
- launchd layout;
- test and simulation structure;
- Studio ownership boundaries;
- Mini implementation boundaries.

Where this architecture document deliberately leaves a physical implementation choice conceptual and the repository/operational blueprint supplies a more specific implementation-facing refinement, the repository/operational blueprint should guide the implementation provided that it does not violate an invariant in this architecture document.

The documents should therefore be interpreted as layers rather than competing specifications.

---

# 37. Initial Implementation Sequence

The intended high-level implementation order is:

## Phase 1 — Mac Studio bootstrap

1. Read this architecture document fully.
2. Read the repository and operational blueprint fully.
3. Inspect the real Mac Studio environment.
4. Confirm current paths and managed surfaces.
5. Establish the intended repository structure.
6. Establish configuration handling.
7. Establish persistent staged state.
8. Implement publisher comparison and sync.
9. Implement publisher Git behaviour.
10. Implement publisher launchd orchestration.
11. Implement logging and validation.
12. Establish consumer structure and contract.
13. Establish consumer simulation where possible.
14. Produce truthful implementation documentation.
15. Prepare a bounded Mac mini handoff.

## Phase 2 — Mac mini consumer validation

1. Consume the repository produced by the Mac Studio.
2. Read the permanent project documentation and handoff.
3. Configure the machine as a consumer.
4. Validate Git update behaviour.
5. Validate staged-state handling.
6. Validate rsync deployment.
7. Validate consumer launchd behaviour.
8. Confirm no unmanaged `.codex` surfaces are touched.
9. Refine only explicitly bounded consumer implementation areas.
10. Contribute truthful findings back to the canonical repository.

## Phase 3 — Stable reusable project

Once both roles are proven:

- keep the repository canonical;
- keep configuration contracts public;
- keep local configuration private;
- keep architecture stable unless deliberately changed;
- keep implementation documentation truthful;
- support additional consumer machines without redesigning the system.

---

# 38. Core Invariants

The following principles should be considered architectural invariants unless explicitly revisited:

1. The Mac Studio live managed `.codex` state is the initial publisher source of truth.
2. Only global `AGENTS.md` and the complete recursive `skills/` tree are managed.
3. Everything else beneath `.codex` is out of scope.
4. The allowlist must not silently broaden.
5. GitHub transports published state between independent machines.
6. Cross-machine hard links are not used.
7. Cross-machine symlink dependency is not used.
8. Consumers own real local deployed files.
9. Publisher operation is automatic outward.
10. Publisher recovery inward is manual.
11. The publisher must not automatically consume.
12. Publisher and consumer are separate operational workflows.
13. The repository contains the machinery for both roles.
14. Machine role is explicit local configuration.
15. Public configuration describes capability; private configuration contains machine truth.
16. The managed staged state is persistent.
17. `skills/` is recursive and opaque.
18. Deep skill changes must not rely on root-directory modification time.
19. Recursive comparison must establish actual managed differences.
20. No-op runs must not produce unnecessary writes or commits.
21. The transported global `AGENTS.md` must not be confused with repository instructions.
22. The Mac Studio owns the initial architecture and repository bootstrap.
23. The Mac mini validates and refines within bounded consumer responsibilities.
24. Consumer findings must not silently create architectural drift.
25. Documentation is part of the product.
26. The repository should eventually be sufficient for a future AI to understand and continue the project.

---

# 39. Definition of Success

The initial project should eventually reach a state where:

```text
Mac Studio
    │
    │ edit ~/.codex/AGENTS.md or anything beneath ~/.codex/skills/
    ▼
headless publisher detects meaningful managed change
    │
    ▼
persistent staged representation updated
    │
    ▼
Git commit + push
    │
    ▼
GitHub canonical published state
    │
    ▼
Mac mini headless consumer detects newer published state
    │
    ▼
local repository updated
    │
    ▼
managed difference verified
    │
    ▼
AGENTS.md + skills/ deployed locally
    │
    ▼
Mac mini Codex consumes real local files
```

with:

- no dependence on the Mac Studio being online;
- no remote filesystem dependency;
- no hard links;
- no cross-machine symlinks;
- no unmanaged `.codex` content copied;
- no meaningless Git commits;
- no publisher self-consumption loop;
- no consumer architecture drift;
- no private machine configuration published;
- no requirement for a future AI to rediscover the system from scratch.

That is the intended architecture for `codex-config-manager`.

---

# 40. Bootstrap Status

At the time this blueprint is handed to the Mac Studio implementation:

- the architecture has been defined;
- the repository exists;
- the GitHub remote exists;
- the project is public;
- the local repository path is established on both Macs;
- the Mac Studio managed Codex source surfaces have been confirmed;
- the Mac Studio is the initial publisher and architecture owner;
- the Mac mini is the initial downstream consumer;
- implementation has not yet been completed;
- the repository and operational blueprint provides the more specific physical repository design;
- the Mac Studio should read both bootstrap documents completely before beginning implementation.

The first implementation AI should not treat this document as a request to blindly create every conceptual element exactly as written.

It should treat it as the architectural contract.

Where implementation details remain open, they should be resolved carefully against the real environment and the companion repository/operational blueprint.

Where a decision could change an architectural invariant, source-of-truth rule, safety boundary, consumer contract or public configuration contract, the operator should be consulted before that decision is silently made.

The objective of the first Mac Studio implementation is not merely to make synchronisation work once.

It is to establish a coherent, reusable and documented system that the Mac mini — and future consumers — can inherit without redesigning it.