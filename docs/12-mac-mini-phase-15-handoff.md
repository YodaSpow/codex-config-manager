# Doc 12 — Mac mini Phase 15 Handoff

**Status:** Ready after the Mac mini SSH prerequisite and final Mac Studio freshness reconciliation
**Authority:** This document is a handoff, not authorization to operate on the Mac mini
**Prerequisite:** Mac Studio Gates 0–14 are complete; `origin/main` contains the reusable implementation and current `latest/`
**Identity contract:** [Doc 4 — Deterministic Model-Derived Machine Identity](04-implementation-discovery-deterministic-machine-identity.md)
**Canonical operations:** [Doc 10 — Implementation Architecture and Operations](10-implementation-architecture-and-operations.md)
**SSH bootstrap:** [Doc 14 — GitHub SSH Machine Bootstrap](14-operator-guide-github-ssh-machine-bootstrap.md)
**Repository workflow:** Root [`AGENTS.md`](../AGENTS.md) and [Doc 16 — Agent Workflow and Publication Guardrails](16-repository-agent-workflow-and-publication-guardrails.md)

## Objective

On the real Mac mini, establish the repository-owned environment, create truthful consumer configuration, validate the pulled snapshot, deploy only the bounded managed targets, install only the consumer LaunchAgent, and contribute permitted evidence/refinements back to this repository.

Completion of this later goal proves the full Mac Studio → GitHub → Mac mini system. It must not redefine the already validated authority, scope, `latest/`, publisher or exclusion contracts.

## Locked boundaries

The Mac mini work must preserve:

- Mac Studio `~/.codex` as the authoring authority;
- GitHub `origin/main` as the canonical shared published history;
- `latest/` as the only unpacked consumer payload;
- dynamic immediate user-skill discovery;
- complete exclusion/preservation of `skills/.system/**`;
- global `.DS_Store` ignore/preservation;
- bounded managed deletion for `AGENTS.md` and user skills only;
- explicit consumer role and model-derived `MacMini` identity;
- safe fast-forward-only repository updates;
- exact repository-owned `.venv` and `.tools/rsync` runtime paths;
- publisher absence on the Mac mini;
- root `AGENTS.md` as read-only guidance on the Mac mini, with any proposed
  correction returned to the Mac Studio rather than applied locally;
- ordinary and governing documents as Mac Studio-owned, with the Mac mini
  writing real evidence, blockers and proposals only to its reserved report at
  `docs/17-mac-mini-report-phase-15-validation.md`;
- no force push, automatic tag or automatic GitHub Release.

Do not copy SSH credentials, private Mac Studio configuration, runtime receipts, logs or LaunchAgent files between machines. Reconstruct machine-local state from tracked contracts.

## Pre-handoff freshness reconciliation on the Mac Studio

Immediately before the Mac mini work begins, run a read-only Mode A reconciliation on the Mac Studio. Confirm:

1. the checkout is clean, on `main`, tracks `origin/main`, and local/remote SHA agree;
2. root `AGENTS.md` and Docs 4, 10, 12, 14, 15 and 16 still match the current identity, code, public config, tests, repository topology, Git transport and repository-workflow contracts;
3. later documentation has not changed the consumer scope, exclusion rules, evidence requirements or extension boundary;
4. `latest/` is the current validated publisher output;
5. every remaining task genuinely requires the real Mac mini;
6. no private Mac Studio material has entered the handoff.

If that pass finds material drift, reconcile this handoff through Mode B before starting the Mac mini goal. Do not ask the Mac mini to infer which competing instruction is current.

## Mac mini SSH prerequisite before the goal

The Mac Studio SSH setup does not transfer to the Mac mini. Before the Phase 15 goal starts, use Doc 14 on the Mac mini to create or deliberately select a machine-local key and prove:

```text
ssh -T git@github.com                                  expected GitHub account identified
git ls-remote over SSH with BatchMode=yes              exact repository readable non-interactively
repository destination                                 safe and separate from ~/.codex
private key origin                                     created or selected on the Mac mini, never copied
```

Do not record the private key, passphrase, full public key or credential-bearing diagnostic output. Failure of either connection test leaves Phase 15 not ready; it is not permission to switch transport, weaken validation or copy the Mac Studio key.

This prerequisite proves the interactive user environment and non-interactive repository read path. The later Phase 15 goal must still prove SSH from the actual launchd user domain after the consumer runtime context exists.

## Goal and local-project execution model

Run Phase 15 as one persistent goal on the real Mac mini, governed by this document. Use a local Codex project rooted at the Mac mini's own repository clone because environment construction, filesystem validation, live `.codex` deployment and launchd operation occur on that machine.

Root `AGENTS.md` and Doc 16 govern repository-agent workflow and Git authority during that goal. The Mac mini must not originate edits to root `AGENTS.md`; a clean safe fast-forward may receive the Mac Studio-authored version from `origin/main`. Any proposed root-instruction or ordinary/governing-document correction must be recorded in the reserved Mac mini Phase 15 report for Mac Studio review. `latest/AGENTS.md` remains managed payload for deployment to `~/.codex/AGENTS.md`; it is not a repository instruction file.

Do not combine a Mac Studio folder and Mac mini folder as competing source roots, and do not treat source-folder priority or a remote project as cross-machine synchronization. GitHub `origin/main` is the shared history; each machine has its own local checkout and machine-local state.

The goal remains active through bounded discovery, environment construction, foreground deployment, tactical correction, retesting, launchd validation, evidence capture and permitted contribution. It may correct a Mac mini-specific command, path, local config value or implementation defect when the correction preserves this specification. It must stop for an architecture decision before changing authority, managed scope, exclusion/deletion policy, `latest/`, publisher behavior, repository topology or public configuration architecture.

## Required discovery before mutation

Run a bounded Mode A pass on the real Mac mini and record:

1. native Model Name and derived identity (`MacMini` expected);
2. intended repository root and its non-overlap with the Mac mini Codex root;
3. readable Mac mini `~/.codex`, `AGENTS.md`, `skills/`, `.system` presence and unrelated sentinel surfaces without traversing `.system`;
4. current Python candidate, version and architecture;
5. the already established Doc 14 user-domain SSH evidence and, when its real runtime context exists, SSH access from the launchd domain;
6. existing clone/branch/upstream state, or the safe destination for a new clone;
7. existing publisher/consumer LaunchAgent state;
8. any filesystem, permission or path fact that differs from the Mac Studio evidence.
9. root `AGENTS.md` and Doc 16 are readable, and the agent distinguishes them from the managed payload at `latest/AGENTS.md`.

Stop if the intended Codex root is unreadable, overlaps the repository, contains unsupported managed entries, or the machine/config identity cannot agree.

## Repository and environment setup

Clone or safe-fast-forward the existing repository over SSH. Do not create unrelated history and do not force.

Build the repository-owned development environment with a compatible external Python:

```bash
cd "/Users/spowart/Scripts/codex-config-manager" \
&& /absolute/path/to/python3 scripts/bootstrap.py --environment development \
&& echo "✅ Command ran successfully"
```

Build `.tools/rsync` from the tracked source contract:

```bash
cd "/Users/spowart/Scripts/codex-config-manager" \
&& /absolute/path/to/python3 tooling/rsync/build.py \
&& echo "✅ Command ran successfully"
```

Validate the executable hash, version, architecture, required options and complete linkage. Runtime linkage must remain limited to permitted macOS libraries or repository-contained `.tools/rsync/lib`; no Homebrew rsync runtime is allowed.

## Consumer configuration

Create ignored `config/config.yaml` from the public example and set truthful Mac mini values:

```yaml
contract_version: 1

machine:
  id: MacMini

role: "consumer"
```

Set absolute Mac mini paths for:

- `paths.codex_root`;
- `paths.repo_root`;
- runtime state, locks and logs.

Keep the tracked Git identity exactly aligned with this repository. Publisher settings remain in the union schema but do not authorize publisher behaviour under consumer role. Keep `consumer.check_interval: 5m` initially.

Validate before any live deployment:

```bash
cd "/Users/spowart/Scripts/codex-config-manager" \
&& .venv/bin/codex-config-manager-validate --config config/config.yaml \
&& echo "✅ Command ran successfully"
```

## Controlled live consumer validation

Before the first live consumer run, capture evidence for:

- current Git SHA;
- validated `latest/` fingerprint and skill membership;
- live Mac mini managed fingerprint;
- `.system` sentinel identity without using it as managed input;
- `.DS_Store` observations without mutation;
- unrelated `.codex` sentinel identity.

Run one foreground consumer invocation:

```bash
cd "/Users/spowart/Scripts/codex-config-manager" \
&& .venv/bin/codex-config-manager-consumer --config config/config.yaml \
&& echo "✅ Command ran successfully"
```

Prove:

1. only `AGENTS.md` and dynamic user-skill targets changed;
2. live managed content equals validated `latest/`;
3. `.system/**`, `.DS_Store` and unrelated sentinels are unchanged;
4. a second run is a no-op;
5. consumer runtime created no commit and did not invoke publisher code;
6. checkout HEAD equals the pulled published SHA.

Any real deletion proof must use a separately authorized, bounded managed change originating on the Mac Studio and flowing through normal publication. Never sacrifice existing operator content for a test.

## Launchd activation

Only after foreground deployment and exclusion proofs pass:

```bash
cd "/Users/spowart/Scripts/codex-config-manager" \
&& .venv/bin/codex-config-manager-install --config config/config.yaml \
&& echo "✅ Command ran successfully"
```

Validate:

- label `com.yodaspow.codex-config-manager.consumer`;
- exact `.venv/bin/codex-config-manager-consumer` program path;
- 300-second interval;
- correct repository working directory and log paths;
- loaded `gui/<uid>` state;
- headless no-op output;
- launchd-domain SSH authentication;
- publisher plist/service absent on the Mac mini;
- single-instance behavior and conservative failure logging.

Exercise uninstall and reinstall, proving that uninstall preserves live Codex state, repository state, `latest/`, config, environment, rsync, runtime state and logs.

## Evidence to contribute back

Create `docs/17-mac-mini-report-phase-15-validation.md` with the title `Doc 17 — Mac mini Report — Phase 15 validation` when either every Phase 15 operation requiring a clean, not-ahead checkout has completed or a material blocker has safely stopped those operations. This is the first case file in the Mac mini's persistent report namespace: consolidate proven results, status, bounded consumer corrections and a clearly separated proposed-Mac-Studio-follow-up section without rewriting root `AGENTS.md` or ordinary/governing documents. A blocked report must identify the stop point and required response without claiming completion. Do not use it as a continuously dirty runtime notebook.

Apply Doc 16's public-content and Git publication gate, then create a normal development commit containing only the report and any separately authorised consumer refinements and push through the established SSH path. This bounded agent-driven delivery needs human intervention only if the gate finds sensitive content, uncertain ownership or unsafe Git state. Do not commit private config, machine credentials, key material, identifying raw logs or private runtime receipts. The consumer runtime itself never authors the report, commits or republishes.

Record:

- Mac mini model identifier, macOS, Python and architecture;
- rsync build receipt summary and linkage;
- clean test results on the Mac mini;
- first foreground consumer result and no-op proof;
- before/after exclusion and unrelated-sentinel proof;
- installed consumer LaunchAgent evidence;
- full pulled publication SHA;
- any evidence-driven Mac mini-specific correction;
- final full-system readiness conclusion.

After the report reaches GitHub, the Mac Studio safely receives it, publishes any required response through its own documentation, implementation or a Git commit referencing the report, and never edits or closes the Mac mini's case file. The Mac mini then safely fast-forwards and validates that response. If it resolves the condition, the Mac mini closes its own report and records the response commit SHA; otherwise the report remains active with continuing evidence. A closed report is immutable and any later challenge, regression or recurrence requires a new numbered Mac mini report. Only after successful evidence is reconciled may the Mac Studio update governing documentation to say the complete two-machine system is operational.

## Stop conditions

Stop without deployment or redesign if:

- Git history is dirty, ahead, diverged or cannot safely fast-forward;
- machine identity or role mismatches;
- `latest/` is invalid or contains excluded/unexpected state;
- exact rsync/environment validation fails;
- consumer target overlaps the repository or another unsafe root;
- `.system`, `.DS_Store` or unrelated content cannot be proven preserved;
- launchd would install the publisher lane;
- credentials or private machine data would need publication;
- the Doc 14 SSH prerequisite is absent, identifies the wrong account, or cannot read the exact repository with `BatchMode=yes`;
- an alternative would materially change authority or architecture.
