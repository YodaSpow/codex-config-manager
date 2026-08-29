# Doc 18 — Architecture Discovery — GitHub-Backed Cross-Machine Report Notification

**Status:** Discovery and recommended future contract — notification watcher not implemented
**Machine authority:** Mac Studio-owned architecture record
**Repository workflow:** Root [`AGENTS.md`](../AGENTS.md) and [Doc 16 — Repository Operations — Agent Workflow and Publication Guardrails](16-repository-agent-workflow-and-publication-guardrails.md)
**Proven case:** [Doc 17 — Mac mini Report — Phase 15 validation](17-mac-mini-report-phase-15-validation.md)
**Captured:** 29 August 2026

## Current state

- ✅ GitHub `origin/main` is already the durable cross-machine transport and
  shared history.
- ✅ The Mac Studio publisher and Mac mini consumer provide automatic managed
  state synchronization without an active Codex chat.
- ✅ Doc 16 already defines the Mac mini report, Mac Studio response and Mac
  mini closure lifecycle.
- ✅ Doc 17 proved that lifecycle through a real Mac mini report, Mac Studio
  response commit and Mac mini closure commit.
- ✅ A closed Mac mini report is immutable, and the Mac Studio never edits or
  closes it.
- ▶ This document defines a stable candidate model for detecting and presenting
  report work without the human carrying SHAs or technical evidence between
  machine chats.
- ⛔ No report watcher, notification service, new LaunchAgent, runtime receipt,
  automatic AI invocation or service-authored report exists yet.
- ⛔ This document does not authorise implementation, change the existing
  publisher or consumer, or introduce a publicly reachable endpoint.

## Purpose

The complete Mac Studio to Mac mini rollout exposed one small coordination gap.
The machines already exchange repository state through GitHub, but a dormant
Codex chat is not awakened merely because a report commit arrives.

During Phase 15, the operator supplied that missing notification manually:

```text
Mac mini agent publishes report
        ↓
operator tells the Mac Studio chat
        ↓
Mac Studio validates and publishes a response
        ↓
operator resumes the Mac mini chat
        ↓
Mac mini validates the response and closes its report
```

This was a useful bootstrap and acceptance ceremony, not a defect in managed
state synchronization. The future opportunity is narrower: remove the need for
the operator to transport the notification while retaining the human decision
and evidence-validation gates.

## Teachable architecture: agent, MCP, service and orchestrator

The discovery began while distinguishing several concepts that are easily
conflated.

| Concept | Role in plain language | Relevance here |
| --- | --- | --- |
| Agent | A goal-directed worker that reasons and selects actions | The Mac mini and Mac Studio Codex sessions perform bounded diagnosis, validation and documentation work |
| MCP server | A standardized provider of tools, resources or prompts for AI hosts | Not required merely to notice a Git commit or display a pending report |
| Service | Deterministic background automation | The publisher, consumer and a possible future report watcher belong here |
| Orchestrator | Selects or wakes the participant that should act next | A future agent-dispatch layer could do this, but it is not required for initial notification |
| Human | Supplies authority and judgment where automation must not decide | Still required for sensitive, ambiguous or architectural responses |

The missing bridge does not initially require an MCP server or another
autonomous agent. GitHub already carries the durable message. A deterministic,
outbound-only polling service can identify when human or Mac Studio agent
attention is required.

MCP may become relevant only if several AI applications later need a standard
tool such as `list_pending_machine_reports`. It would still not wake a dormant
agent by itself; an AI host or orchestrator would remain responsible for
invocation.

## The three implemented lanes

### Lane 1 — Managed data

```text
Mac Studio ~/.codex
        ↓ validated publisher
GitHub origin/main + latest/
        ↓ validated consumer
Mac mini ~/.codex
```

This lane is automatic. It publishes and deploys only the bounded global
`AGENTS.md` and dynamically discovered user-managed skills, while excluding and
preserving `skills/.system/**` and `.DS_Store`.

### Lane 2 — Repository development

```text
authorised Mac Studio documentation or implementation
        ↓ normal exact-path development commit
GitHub origin/main
        ↓ consumer safe fast-forward
Mac mini repository checkout
```

The Mac mini receives the complete repository history. Ordinary documents
therefore arrive in its checkout automatically, but they are not deployed into
`~/.codex` and do not awaken or inject themselves into a dormant Codex chat.

### Lane 3 — Exception and coordination

```text
Mac mini agent-owned report
        ↓ normal exact-path development commit
GitHub origin/main
        ↓ Mac Studio reconciliation
Mac Studio-owned response commit
        ↓ Mac mini validation
Mac mini-owned report closure
```

This lane is intentionally agent-driven. It is used when real Mac mini work,
evidence, a blocker or a proposal requires cross-machine review. The consumer
runtime itself never authors a report, commit or response.

The current gap is notification inside Lane 3, not transport or authority.

## Proven Phase 15 signal chain

The actual repository history proves that commits and the report together
already contain the required coordination information:

```text
20248413728567d3eade8eb3ccfdf92c08d13838
docs: add Mac mini Phase 15 validation report

ff981089c726d75e2ac57e81ed6d459129d669f3
docs: acknowledge Doc 17 Mac mini validation

9eb38290cdf081bbc961793eeaf2747eef23e8c7
docs: close Mac mini Phase 15 report
```

The report commit supplied the case and evidence. The Mac Studio response
commit supplied the acknowledgement and reconciliation result without editing
the report. The closure commit supplied Mac mini validation and final state.

The durable signal model is therefore:

```text
Git commit                  notification signal and exact repository position
Mac mini report             authoritative case payload and Mac mini-owned status
Mac Studio response commit  authoritative Mac Studio acknowledgement or answer
Mac mini closure commit     authoritative completion of that case
```

The SHA is not the meaning by itself. It is the stable identity that binds each
signal to exact repository content.

## Why not add a committed feed file

A second repository log, queue or report index initially appears attractive,
but it would duplicate truth already present in Git history and report files.
It would also create new ownership and synchronization questions:

- which machine edits the feed;
- whether both machines can safely append to it;
- whether the feed or the report wins when they disagree;
- how feed updates avoid generating further feed events;
- how closed entries are removed without rewriting another machine's record;
- whether a stale index could hide a real report commit.

The recommended first design therefore has no committed feed. GitHub history is
the feed, and the report namespace identifies relevant payloads.

GitHub's official commits API exposes ordered commits and permits path-based
filtering. Its repository-events API is optimized for conditional polling but
is explicitly not a real-time surface and may be delayed. These APIs are valid
research alternatives, but the existing SSH Git transport already provides the
repository facts required by this project:

- [GitHub REST API — Commits](https://docs.github.com/en/rest/commits/commits)
- [GitHub REST API — Events](https://docs.github.com/en/rest/activity/events)

## Recommended future watcher

The smallest useful future component is a separate Mac Studio report watcher.
It should remain independent of the managed-state publisher and use only
outbound access to the established GitHub repository.

Conceptually:

```text
local last-inspected SHA
        ↓
observe current origin/main
        ↓
inspect every new commit in the bounded range
        ↓
filter changed paths matching
docs/<doc-number>-mac-mini-report-<semantic-topic>.md
        ↓
read the report at the relevant commit
        ↓
derive explicit coordination state
        ↓
record bounded local receipt and notify when action is required
```

The watcher must inspect every new commit since its cursor. It must not merely
look for the highest numbered report, because an earlier active report may have
received a later update or closure.

### Network boundary

The recommended watcher opens no inbound port and exposes neither Mac to the
local network or public internet. It initiates outbound repository access using
the already approved Git transport.

GitHub webhooks can deliver events to an external HTTP server, but that would
require a reachable receiver and additional infrastructure. It is deliberately
outside the recommended design:

- [GitHub Webhooks](https://docs.github.com/en/webhooks)

### Separation from existing services

The watcher must not be folded casually into the publisher or consumer:

- the publisher owns managed-state ingestion, settlement and publication;
- the consumer owns safe fast-forward and bounded `latest/` deployment;
- the watcher would own observation, classification and notification only.

Any future implementation must coordinate Git access with existing repository
locks so a watcher fetch cannot race publisher or development operations. A
read-only notification task must never broaden the publisher allowlist or
become permission to merge, commit or push.

## Explicit coordination states

The future watcher should not present a vague inference. It should calculate a
small, named state from authoritative repository facts.

| Coordination state | Required evidence | Meaning |
| --- | --- | --- |
| `pending_studio_review` | Mac mini report is `Open` or `Blocked`, and no qualifying Mac Studio response follows its current report commit | Mac Studio attention is required |
| `pending_mini_validation` | A qualifying Mac Studio response references the current report commit, while the report remains open | Mac Studio has answered; the Mac mini must validate the response |
| `closed` | The Mac mini report is `Closed` and records the validated Mac Studio response commit | No action remains for that case |
| `invalid_or_ambiguous` | Ownership, status, ancestry, reference or content does not satisfy the contract | Notify as a safe failure; do not guess or advance the cursor past unresolved evidence |

These are watcher presentation states, not additional report statuses and not
new repository authority.

### Report status vocabulary

The report itself remains Mac mini-owned. The proven lifecycle requires:

```text
Open      active case that may require Mac Studio review
Blocked   active case that cannot continue without an external response
Closed    response validated by the Mac mini; report is now immutable
```

Doc 16 currently also permits `Resolved`, but the implemented Phase 15 case did
not establish a distinct meaning for it. A future contract must either define
exactly how `Resolved` differs from `Closed` and the watcher states above, or
remove it from the watcher-supported initial vocabulary. The watcher must not
invent that meaning during implementation.

## Local receipt and self-cleaning state

Notification progress belongs in the Mac Studio's configured, ignored runtime
state—not in tracked documentation or managed payload.

A representative conceptual receipt is:

```yaml
contract_version: 1
last_inspected_sha: "<full-commit-sha>"
pending_reports:
  - path: "docs/<number>-mac-mini-report-<semantic-topic>.md"
    report_commit: "<full-commit-sha>"
    status: "pending_studio_review"
    last_notified_commit: "<full-commit-sha>"
```

The exact schema and path are deferred. The durable rules are:

- retain the full inspected SHA as the bounded cursor;
- retain only active pending report entries and minimal notification deduplication;
- remove a pending entry after its authoritative report becomes `Closed`;
- do not delete or alter the tracked report when removing local receipt state;
- do not retain an unbounded event history, because Git already supplies it;
- write receipts atomically;
- validate ancestry before advancing the cursor;
- treat missing, malformed or incompatible local state conservatively;
- keep the receipt ignored and free of credentials or unnecessary private data.

Self-cleaning means closed pending entries disappear from local runtime state.
It does not mean deleting reports, commits, logs belonging to another contract,
or `.DS_Store`.

## Human-readable visibility

The first implementation should offer two complementary local surfaces:

1. a Mac Studio notification when a report first enters a state requiring Mac
   Studio attention;
2. a read-only status command that can show all currently pending cases.

Representative output:

```text
Mac mini report awaiting Mac Studio review
Report: Doc 18 — <semantic title>
Commit: abc1234
Status: Open
Coordination: pending_studio_review
```

The status command may show closed cases only when explicitly requested from
Git history. The default view should remain a concise pending-work surface.

A repository agent on the Mac Studio could later be instructed to consult this
status at task entry. That would make the pending report visible whenever a new
Mac Studio Codex task begins, but it would still not awaken a dormant chat.

## Authority retained after notification

The watcher only answers:

> Has the Mac mini published a new or changed report that requires attention?

It must not:

- accept evidence automatically;
- decide that a reported condition is architecturally acceptable;
- edit or close a Mac mini report;
- generate a Mac Studio response commit;
- invoke a dormant Codex chat;
- start a goal or grant implementation authority;
- mutate `latest/`, `upload-ready/`, README or live Codex state;
- run publisher or consumer behavior;
- force, rewrite history or bypass dirty/ahead/diverged Git gates;
- expose a public callback, listener or webhook receiver.

After notification, the Mac Studio agent performs the existing Doc 16
reconciliation. The human remains responsible for any material choice. The
technical evidence stays in GitHub, so the human need only initiate or approve
the decision—not copy the report or SHA between machines.

## Dormant-agent boundary

Automatic repository synchronization and automatic AI interpretation are
different capabilities.

When a Mac Studio-authored document reaches the Mac mini:

- the consumer can fast-forward the complete repository;
- the document becomes locally available in the Mac mini checkout;
- only validated `latest/` managed content is deployed into `~/.codex`;
- an inactive Codex chat remains inactive;
- a future Mac mini agent can discover the document at task entry under root
  `AGENTS.md` and Doc 16.

Similarly, a Mac Studio watcher can make the operating environment aware of a
pending report, but an agent becomes aware only when a supported task or chat
is started. Automatic agent dispatch is a separate, more powerful future
orchestration decision.

## Options considered

| Option | What runs | Reliability | Setup and maintenance | Best use | Current conclusion |
| --- | --- | --- | --- | --- | --- |
| Human carries the notification | Operator copies completion/blocker text between chats | Proven but easy to forget and unnecessarily manual | No implementation; continued human ceremony | Bootstrap and rare one-off recovery | Retain as fallback, not preferred steady state |
| Outbound Git report poller | Separate local service inspects new commits and report paths | Uses existing durable history and transport | Small bounded implementation plus local receipt and notification | Current two-machine topology | Recommended first future implementation |
| GitHub REST polling | Local service queries commit or event endpoints | Viable, but adds API-version/rate-limit behavior and events may lag | Additional HTTP/API validation; optional authentication for non-public use | Environments without a suitable Git checkout | Research fallback |
| Repository webhook | GitHub sends push events to a receiver | Timely delivery | Requires reachable listener, validation and delivery recovery | Existing hosted integration infrastructure | Rejected for this topology |
| Autonomous agent dispatcher | Event starts or resumes the correct AI worker | Could remove the remaining initiation step | Larger authority, product-integration and safety surface | Mature high-volume exception workflow | Defer until notification-only use proves a need |
| MCP report server | AI hosts query standardized report tools/resources | Useful only with multiple AI consumers | New server and host integration | Cross-application reuse | Not justified by the current notification problem |

## Deferred service-generated reports

A later operational service might detect a consumer failure without an active
Mac mini Codex agent. Allowing that service to author and push a Mac mini report
would materially expand authority, credential handling and Git mutation.

That possibility is explicitly deferred. It would require a separate contract
covering:

- which deterministic failures qualify;
- how evidence is sanitized;
- which process holds Git credentials;
- how report numbering and collisions are prevented;
- how clean-worktree and exact-path publication gates are retained;
- how repeated failures are deduplicated;
- how a service-authored report differs from agent evidence;
- how recovery avoids report storms.

The notification watcher described here consumes already authorised reports. It
does not create them.

## Entry criteria for Mode C

Before implementing a report watcher, a Mode B implementation contract must
settle:

1. the supported report status vocabulary, including the fate of `Resolved`;
2. the exact qualifying relationship between report, response and closure commits;
3. the configured local runtime-state and log paths;
4. the receipt schema, migration and corruption behavior;
5. the polling interval and notification deduplication rules;
6. the shared Git-lock interaction with publisher and development work;
7. whether observation uses the local Git transport, GitHub commits API or a bounded fallback;
8. the read-only status and macOS notification surfaces;
9. restart, missed-interval, remote-rewrite and unreachable-GitHub behavior;
10. tests for multiple commits, multiple active reports, updates to earlier report numbers, closure cleanup and ambiguous histories;
11. installation, uninstall and proof requirements for any separate LaunchAgent;
12. the exact root `AGENTS.md` pointer, if task-entry report awareness is approved.

Implementation must prove that the watcher neither exposes an inbound network
surface nor mutates report content, repository history, managed state or live
Codex state.

## Relationship to existing documents

- [Doc 5](05-implementation-discovery-deterministic-managed-state-publication-history.md)
  remains authoritative for managed-state commit semantics; report commits must
  never impersonate `managed-state:` history.
- [Doc 10](10-implementation-architecture-and-operations.md) remains
  authoritative for the implemented publisher, consumer, configuration and
  runtime paths.
- [Doc 12](12-mac-mini-phase-15-handoff.md) and
  [Doc 15](15-operator-runbook-mac-mini-phase-15-activation.md) preserve the
  Phase 15 activation and evidence journey. Their post-activation status
  reconciliation is separate from this discovery.
- [Doc 16](16-repository-agent-workflow-and-publication-guardrails.md) remains
  authoritative for machine ownership, report publication, Mac Studio response
  and Mac mini closure.
- [Doc 17](17-mac-mini-report-phase-15-validation.md) remains the immutable,
  closed Mac mini-owned proof that the lifecycle works.

This document does not supersede those contracts. It captures the missing
notification layer and the evidence required before that layer can be safely
implemented.

<!-- End of document -->
