# Doc 6 — Implementation Discovery — Settled-State Publication Controls

**Status:** All four modes implemented and tested; `after_settle` is active on the Mac Studio. See [Doc 10](10-implementation-architecture-and-operations.md) and [Doc 11](11-validation-evidence-mac-studio.md).
**Scope:** Mac Studio publisher observation, settling, publication eligibility, pause/schedule/throttle controls and human-readable durations  
**Relationship to existing documents:** This record refines the publisher timing and configuration contract and defines the eligibility layer before private candidate construction, root-level `latest/` promotion and Doc 5 managed-state publication.  
**Related documents:** [Doc 3 — Mode C Implementation Plan](03-mode-c-implementation-plan.md) · [Doc 5 — Deterministic Managed-State Publication History](05-implementation-discovery-deterministic-managed-state-publication-history.md) · [Doc 8 — Root-Level Latest Managed Snapshot](08-architecture-reconciliation-root-level-latest-managed-snapshot.md)

## Status

- ✅ `check_interval: 1m` is the preferred Mac Studio publisher observation interval.
- ✅ `settle_period: 5m` is the preferred quiet period after the last observed managed-state change.
- ✅ `publication.mode: after_settle` is the preferred normal operating mode.
- ✅ The coherent publication-mode vocabulary is `after_settle`, `paused`, `scheduled` and `throttled`.
- ✅ Manual publication mode is excluded from the proposed contract.
- ✅ Human-facing durations use whole numbers with lowercase `s`, `m`, `h` or `d` units and are normalized internally.
- ✅ No mode may publish actively changing, invalid or unverified managed state.
- ▶ Exact scheduled-mode edge behaviour and which optional modes enter the first implementation remain bounded pre-Mode-C decisions.
- ⛔ No configuration, runtime state, source fingerprinting, launchd cadence or publication control is implemented by this document.

## Purpose

Codex Config Manager needs to distinguish three questions that were previously collapsed into one scheduled interval:

1. **When should the Mac Studio inspect managed state?**
2. **When is a changed managed state mechanically quiet enough to become eligible?**
3. **What publication policy applies after it becomes eligible?**

The selected model gives each question one configuration surface:

```yaml
publisher:
  check_interval: 1m
  settle_period: 5m

  publication:
    mode: after_settle
```

The first two values establish observation and settling. The publication mode controls what happens only after settlement. This preserves a simple default while making pause, scheduled batching and rolling throttling expressible without pretending they are longer settle periods.

## Authoring and managed-source boundary

Skill development occurs in the separate lowercase `codex-guidance` project. Codex Config Manager is not the skill-authoring environment and must not monitor, interpret or couple itself to that repository.

The Mac Studio's authoritative installed managed state remains:

```text
/Users/spowart/.codex/AGENTS.md
/Users/spowart/.codex/skills/<dynamic user-skill content>
```

Any authoring, validation or promotion process that moves work from `codex-guidance` into the installed `.codex` surfaces is upstream of Codex Config Manager. Settling begins from observed changes in the authoritative managed `.codex` universe, not activity in the authoring repository.

If an authoring change never reaches the authoritative installed state, Codex Config Manager has nothing to publish. This separation prevents the transport project from becoming responsible for skill creation or authoring-repository semantics.

## Existing-plan distinction

Doc 3 presently describes separately configured publisher and consumer intervals initially expressed as `300` seconds, and describes the scheduled interval as a cheap trigger rather than proof of change. That is a five-minute polling interval, not a five-minute quiet-state contract.

Under the preferred Doc 6 model:

- the Mac Studio publisher checks every minute;
- the managed state must then remain unchanged for five continuous minutes;
- the publication mode determines whether an eligible state is published immediately, held, scheduled or throttled;
- the Mac mini consumer remains a separate later lane with its own polling contract.

Doc 3 now incorporates the one-minute check, five-minute settlement and publication-mode eligibility layer. Doc 8 supplies the subsequent private-candidate and root-level `latest/` transition.

## Mechanical settlement, not conceptual completion

A timer cannot prove that a skill is conceptually complete. It can prove only that the managed bytes and topology have remained unchanged for a configured period.

The term **settled** therefore means:

> The complete managed source fingerprint has remained unchanged for the entire configured settle period.

It does not mean:

- the skill is semantically finished;
- the author has approved a release;
- the content has been interpreted or reviewed by AI;
- the authoring repository is clean;
- every external authoring workflow has completed.

Because work is authored separately and reaches `.codex` as installed managed state, five quiet minutes provides a proportionate buffer for multi-file or overlapping updates. Every newly observed managed-state change resets the settle period.

Example:

```text
12:00  first installed managed files change
12:02  final installed managed file changes
12:07  five uninterrupted quiet minutes complete
12:07–12:08  next check confirms eligibility
```

The two-minute update sequence does not consume the quiet allowance. Settlement begins again after the final observed change.

## Timing foundation

The preferred steady-state configuration is:

```yaml
publisher:
  check_interval: 1m
  settle_period: 5m

  publication:
    mode: after_settle
```

### `check_interval`

`check_interval` controls how often the headless Mac Studio publisher wakes and observes the managed source. It is observation granularity, not proof of a change and not a publication deadline.

With `check_interval: 1m`, a five-minute settlement is normally confirmed approximately five to six minutes after the final real change.

### `settle_period`

`settle_period` is a debounce/quiescence duration measured from the most recently observed managed-source fingerprint change.

- A different managed fingerprint resets the settle timer.
- A fingerprint equal to the last published state cancels the pending publication.
- A continuously changing state may remain unsettled indefinitely.
- A settled state is eligible for its configured publication mode; it is not yet permission to bypass validation.

This is distinct from cadence. A one-hour settle period restarts after every new change. A one-hour throttle is measured from the last successful publication and does not become another quiet timer.

## Human-readable duration grammar

Operator-facing YAML uses readable duration strings. The implementation may normalize them to integer seconds only after strict validation.

Supported units are:

```text
s = seconds
m = minutes
h = hours
d = days
```

Valid examples:

```yaml
check_interval: 30s
check_interval: 1m
settle_period: 5m
minimum_interval: 2h
minimum_interval: 1d
```

The initial grammar must:

- accept lowercase `s`, `m`, `h` and `d` only;
- accept whole non-negative numbers only where zero is meaningful;
- require exactly one unit;
- reject unitless numbers;
- reject prose such as `five minutes`;
- reject uppercase or ambiguous units;
- reject decimals and compound forms such as `1.5h` or `1h30m` initially;
- apply field-specific minimum and maximum bounds before normalization;
- detect overflow or unreasonably large values rather than silently clamp them.

`check_interval` must be greater than zero. `minimum_interval` must be greater than zero when throttled mode is selected. A future `settle_period: 0s` may represent disabled settling/immediate eligibility, but that value must not bypass source, candidate, `latest/`, artifact or Git safety.

A duration `1d` means a fixed elapsed duration for throttling. Calendar-day scheduling uses explicit local time and timezone semantics instead; it must not be implemented by treating `1d` as a daily wall-clock schedule.

## Deterministic settled-state observation

Settling must not depend on the parent `skills/` directory modification time. Parent timestamps may fail to reflect arbitrary nested changes and are already unsuitable as authoritative change proof.

The publisher requires a deterministic managed-source fingerprint covering only:

- the managed global `AGENTS.md` when present;
- every dynamically discovered user-skill path and supported entry recursively;
- relative managed path, supported entry type and content identity;
- the same ingestion exclusions and entry semantics used by the authoritative managed-scope contract.

The fingerprint must exclude `.system/**` recursively and ignore `.DS_Store` everywhere. It must not inspect unrelated `.codex` state.

Conceptually, local ignored runtime state retains:

```text
last published source fingerprint
pending source fingerprint
pending first-observed time
pending quiet-since time
configured publication mode
last successful publication time and SHA
mode-specific eligibility state
```

The pending-state record is operational metadata, not managed payload. It must never enter `latest/` or Git.

Before publication, private candidate construction, the authoritative rsync dry-run, real bounded `latest/` reconciliation, snapshot validation and post-sync equivalence checks still apply. If the source changes during ingestion or validation, publication fails safely and the new source state must settle again. Settlement never replaces the existing proof pipeline.

## Shared publication invariant

Every mode is governed by the same invariant:

```text
managed source changed
        ↓
complete fingerprint remains unchanged for settle_period
        ↓
publication-mode eligibility satisfied
        ↓
private candidate + latest/artifact/README/Git validation succeeds
        ↓
Doc 5 deterministic managed-state publication
```

No mode may:

- create/promote a candidate or mutate `latest/` while a source state is merely pending or unsettled;
- publish an unsettled source;
- weaken `.system/**` or `.DS_Store` exclusions;
- bypass candidate/`latest/` equivalence or Git path validation;
- parse or infer managed-content meaning;
- create a no-op commit;
- turn a routine publication into a SemVer release.

`latest/` remains the persistent latest validated repository snapshot until a state is both settled and mode-eligible. This avoids allowing a pause, schedule or throttle to place unpublished authoring state in the tracked canonical snapshot.

## Publication modes

The coherent mode vocabulary is:

```text
after_settle
paused
scheduled
throttled
```

`manual` is intentionally excluded. It would introduce a separate publish command, invocation authority and recovery path without a demonstrated need. Temporary operator control is served by `paused`; automatic normal operation is served by `after_settle`.

Mode-specific keys must be validated conditionally. Missing required keys, unknown modes or keys that conflict with the selected mode must stop before candidate, `latest/`, artifact, README or Git mutation.

## Mode: `after_settle`

Configuration:

```yaml
publisher:
  check_interval: 1m
  settle_period: 5m

  publication:
    mode: after_settle
```

Behaviour:

```text
change detected
      ↓
five uninterrupted quiet minutes
      ↓
publish on the next successful eligibility check
```

This is the default and preferred steady-state mode. “After settle” means no additional cadence delay is imposed after the configured quiet period. Publication still includes every existing environment, role, path, source, candidate, `latest/`, artifact, README and Git validation gate.

## Mode: `paused`

Configuration:

```yaml
publication:
  mode: paused
```

The scheduled publisher continues observing managed state and maintaining non-mutating pending-state metadata, but it must not:

- construct/promote a private candidate;
- mutate `latest/`, artifacts or README;
- stage or commit Git changes;
- push to GitHub.

Read-only status should expose at least:

```text
Publication mode: paused
Pending managed changes: yes
Pending components: AGENTS.md, operational-modes
Settled: yes
```

Changing back to `after_settle` is an intentional resume action. If the current pending fingerprint has already remained quiet for the full settle period, it may become eligible on the next check; the publisher must still revalidate the current source and complete the full publication pipeline. A source change while paused resets settlement normally.

Paused mode does not unload launchd, destroy runtime state, modify managed source or discard pending knowledge. Invalid paused-mode configuration must fail safely rather than accidentally fall back to automatic publication.

## Mode: `scheduled`

Conceptual configuration:

```yaml
publisher:
  check_interval: 1m
  settle_period: 5m

  publication:
    mode: scheduled
    schedule:
      frequency: daily
      local_time: "18:00"
      timezone: local
```

Scheduled mode observes and settles managed state continuously but holds eligible state for a wall-clock boundary.

Example:

```text
14:30  managed state settles
14:30–17:59  remain pending without candidate or latest/ mutation
18:00  scheduled boundary becomes eligible
18:00  validate and publish the latest settled state
```

`local_time` uses a quoted strict 24-hour `HH:MM` value, for example:

```text
06:00
12:30
18:00
23:45
```

The likely daily semantics are:

- at most one successful scheduled managed-state publication per local calendar day;
- publication on the first publisher check at or after the configured local time;
- if the Mac Studio is asleep at the boundary, the first eligible check after wake may satisfy that day's missed boundary;
- unsettled state is never published merely because the scheduled time arrived;
- after that day's successful publication, later changes wait for the next permitted daily boundary.

Before first implementation, the operator must conclusively decide:

- whether an unsettled state at the boundary waits until the next day or publishes later the same day once settled;
- the exact missed-boundary rule across sleep, shutdown and restart;
- whether only daily frequency is supported initially;
- how `timezone: local`, explicit IANA timezones and daylight-saving transitions behave;
- how schedule edits affect an already pending state.

These are real wall-clock policy decisions, not ordinary duration parsing. Scheduled mode must not be claimed as implementation-ready until they are settled and tested.

## Mode: `throttled`

Conceptual configuration:

```yaml
publisher:
  check_interval: 1m
  settle_period: 5m

  publication:
    mode: throttled
    minimum_interval: 1h
```

Throttling means:

> Publish settled changes automatically, while maintaining at least the configured elapsed interval between successful managed-state publications.

Both conditions must be true:

```text
settle period completed
        AND
minimum interval since the last successful publication completed
```

Example where settlement completes first:

```text
10:00  previous publication succeeds
10:10  another managed change begins
10:20  the new state becomes settled
10:20  hold: the one-hour publication interval has not elapsed
11:00  interval completes; publish the latest still-settled state
```

Example where throttling completes first:

```text
10:00  previous publication succeeds
10:55  another managed change begins
11:00  interval completes, but the source remains unsettled
11:05  five quiet minutes complete; publish
```

Throttling is rolling rather than wall-clock scheduled. If a publication succeeds at `11:05`, the next earliest throttled publication is `12:05` for `minimum_interval: 1h`.

While throttled, further managed changes update the pending fingerprint and reset settlement. When both conditions are finally satisfied, only the latest complete settled state is ingested and published. This can prevent bursts of closely spaced GitHub commits while retaining automatic eventual publication.

The interval is measured from the last successful publication, not a failed attempt. If no previous successful managed-state publication exists, the first valid settled state is eligible without an artificial initial throttle delay. Push failure and retry remain governed by the existing pending-publication contract; retrying the same already-created commit must not wait for a new throttle interval.

## Mode comparison

| Mode | After the state settles | Time basis | Typical use |
| --- | --- | --- | --- |
| `after_settle` | Publish on the next eligible check | Last managed-source change | Normal steady state |
| `paused` | Remain pending; never mutate candidate/latest/artifacts/README or Git | Operator-controlled hold | Temporary publication freeze |
| `scheduled` | Wait for a configured wall-clock boundary | Local calendar/timezone | Daily or planned batching |
| `throttled` | Wait until the minimum interval after the last successful publication | Rolling elapsed duration | Prevent closely spaced publication bursts |

## Mode transitions and safe configuration reload

The ignored local `config.yaml` is read and validated through the same role-aware preflight used by scheduled execution. A mode change must not require launchd removal or environment reconstruction.

Safe transition principles are:

- any invalid or unknown mode fails closed before candidate, `latest/`, artifact, README or Git mutation;
- entering `paused` prevents further publication mutation immediately after the validated configuration is observed;
- leaving `paused` never bypasses current fingerprint, settlement or pipeline validation;
- changing a scheduled time or throttle interval recalculates eligibility without rewriting managed source or `latest/`;
- a configuration edit is local operational control and must not itself become canonical managed or Git-staged content;
- an already-created, validated but unpushed Git commit remains a pending-publication recovery case rather than being silently abandoned or rewritten because the mode changed.

The exact precedence between an emergency pause and an already-created unpushed commit requires explicit implementation treatment. The safest likely rule is that `paused` blocks new push attempts until resumed while preserving the exact pending commit and receipt, but this must be reconciled with Doc 5's conservative retry contract before implementation.

## Status and observability

The read-only status surface must make timing and eligibility understandable without exposing managed contents:

```text
Publisher check interval: 1m
Settle period: 5m
Publication mode: throttled
Pending managed changes: yes
Pending components: AGENTS.md, operational-modes
Settled: yes
Throttle remaining: 23m
Last successful publication: <full SHA with short display form>
```

Mode-specific status may include:

- `after_settle`: quiet time elapsed/remaining;
- `paused`: pending and settled state with publication held;
- `scheduled`: next eligible local boundary and missed-boundary status;
- `throttled`: last successful publication and remaining minimum interval.

Logs and receipts remain metadata-only. They may record fingerprints, times, modes, component names and eligibility decisions, but never managed file contents, credentials or unrelated `.codex` state.

## Interaction with Doc 5

Doc 6 controls when a managed source state may enter the mutation/publication pipeline. Doc 5 controls how a validated indexed change becomes a deterministic Git publication.

```text
Doc 6
observe → settle → apply publication mode → become eligible
                                           ↓
private candidate → latest/artifact/README/Git validation
                                           ↓
Doc 5
derive ManagedChangeSet → commit → push → receipt/status identity
```

The Doc 5 component mapping, semantic limit, deterministic ordering, commit grammar, SHA identity, retry safety and release separation remain unchanged. A pause, schedule or throttle must not create alternative commit semantics.

If a push fails after commit creation, Doc 5's exact pending-publication identity takes precedence over detecting and packaging a newer state. New authoring changes may be observed, but they must not rewrite the existing pending commit. Recovery must resolve the known publication safely before a later settled state can form another commit.

## Reconciled impact on Doc 3

Doc 6 has cross-cutting impact but one primary orchestration home. The active Doc 3 reconciliation accounts for the following without restructuring unrelated phases.

| Doc 3 location | Required reconciliation |
| --- | --- |
| Governing reading map | Add Doc 6 as the settled-state timing and publication-control contract |
| Locked architecture | Insert observation, pending settlement and mode eligibility before private candidate and `latest/` mutation |
| Publication/config boundaries | Separate local timing/mode control from managed payload and public content |
| Planned topology | Represent pending fingerprint, mode eligibility and timing state through cohesive runtime-state ownership; avoid speculative modules unless implementation needs them |
| Phase 0 | Hash/read Doc 6 and reconfirm any still-open scheduled-mode decisions before mutation |
| Phase 5 | Replace raw publisher seconds with strict duration strings and mode-specific schema validation; keep consumer timing separate |
| Phase 6 | Reuse the exact managed-scope/exclusion contract to derive the source fingerprint; never rely on parent timestamps |
| Phase 7 | Preserve `latest/` as the canonical snapshot; pending/unsettled/mode-held state must not enter it |
| Phase 8 | Make the publisher a deterministic state machine: observe, track fingerprint, settle, apply mode, then run candidate/latest/artifact/Git orchestration |
| Phase 9 | Enter Doc 5 publication only after Doc 6 eligibility; preserve known pending commits across pause/throttle/schedule changes and retries |
| Phase 10 | No publisher-mode authority for the Mac mini consumer; its polling/deployment contract remains independently configured |
| Phase 11 | Add duration parsing, fingerprint, settlement, mode transition, pause, schedule, throttle, restart, sleep and failure tests |
| Phase 12 | Render the one-minute Mac Studio launchd trigger, validate config reload/status, and prove live settle/mode behaviour without installing the consumer |
| Phase 13 | Document actual timing grammar, mode operations, status, recovery and scheduled semantics from implemented evidence |
| Phase 14 | Audit that held state never mutates candidate/latest/artifacts/README/Git and that configured modes cannot weaken exclusions or publication safety |
| Phase 15 | No source-of-truth change; the Mac mini later validates only the independent consumer lane and published SHA state |
| Implementation-discovery ledger | Add exact duration bounds/parser, fingerprint/receipt design, scheduled edge rules, mode-transition precedence and live sleep/wake evidence |

The primary implementation gate remains the Mac Studio publisher orchestration gate, with Git publication continuing to own commit formation. Tests, launchd proof, permanent documentation and readiness audit provide the later validation layers.

## Completed Doc 3 reconciliation boundary

The operator authorised Doc 3 reconciliation through Doc 8. The completed Mode B workflow is:

1. record current hashes for Docs 3, 5 and 6;
2. create a new byte-identical, dated protected snapshot of the then-current Doc 3 before editing it;
3. prove the new snapshot matches the active pre-edit Doc 3;
4. leave the existing older protected Doc 3 snapshot unchanged as historical drift evidence;
5. reconcile the active Doc 3 surgically at the impact points above;
6. reconcile Docs 5 and 6 only at identified path and publication-boundary contradictions;
7. compare the revised Doc 3 against the immediately preceding protected snapshot and the older pre-Doc-5 baseline;
8. prove all phases, gates, links, governing-document counts and unrelated contracts remain intact;
9. report the exact files and hashes without performing application implementation.

The immediate pre-edit snapshot is the authoritative drift comparison for the next reconciliation. The older pre-Doc-5 snapshot remains useful historical evidence but must not be used to restore text that later operator-approved discoveries intentionally changed.

## Decisions still required before implementation

The following are bounded decisions, not permission to reopen the settled architecture:

1. Whether `scheduled` and `throttled` are required in the first implementation or are schema-reserved for a later release.
2. The exact scheduled-mode behaviour for unsettled state at the daily boundary.
3. Sleep, restart, missed-boundary, timezone and daylight-saving semantics for scheduled mode.
4. Whether explicit timezones are supported initially or only the validated local machine timezone.
5. Field-specific minimum/maximum duration bounds and whether `settle_period: 0s` is supported.
6. Precedence of `paused` over an already-created but unpushed commit.
7. Exact fingerprint representation, atomic state receipt and conservative clock-anomaly handling.

These decisions belong in Mode A/0 discussion or evidence-driven implementation planning before Mode C. They must not be silently guessed by code.

## Current implementation status

- ✅ The preferred `1m` observation, `5m` settlement and `after_settle` steady-state configuration is captured.
- ✅ The `after_settle`, `paused`, `scheduled` and `throttled` vocabulary and distinct timing meanings are captured.
- ✅ The duration grammar, authoring boundary, `latest/` invariant, Doc 5 relationship and Doc 3 impact surface are captured.
- ✅ This record is reconciled into active Docs 3 and 8 using protected pre-edit snapshots and a drift audit.
- ⛔ No application, configuration, runtime state, tests, Git, launchd or Codex managed state has been implemented or modified.
