# Read-only audit contract

Read this reference completely before inspecting approved projects.

## Initiator and objective

The current project is the initiator and supplies the viewpoint, not authority over neighboring projects. Tie discovery to one accepted audit question. Use whichever lens fits:

- **Outward:** What reusable capability should the initiator provide?
- **Inward:** Which selected projects already solve or expose part of the initiator's problem?
- **Landscape:** Where do selected projects overlap, duplicate capability, or remain correctly separated?

The question narrows the output, not the integrity of relevant discovery. Follow dependencies far enough to understand every material deliverable.

## Scope resolution and confirmation

1. Resolve the current project, preferring version-control metadata and using conservative project markers only when needed.
2. Suggest exactly one parent directory as the candidate group root. Do not enumerate its contents during suggestion.
3. Show the current project and candidate root. Ask the operator to use it, replace it, or provide exact paths. This first approval authorises enumeration only.
4. After approval, enumerate every immediate entry under each approved root without opening project contents. Support an allowlist, several approved roots, or exact projects in unrelated locations.
5. Classify every immediate entry as `recognised project`, `unclassified directory`, `excluded non-directory`, `excluded symlink`, or `unavailable`. Recognition may use a Git directory, Git worktree file, or conservative project marker. It is not a relevance judgement.
6. Show the complete census and propose the actual project-inspection list. An allowlist filters selection, not census visibility. The operator may promote an unclassified directory or exclude a recognised project.
7. Obtain a second explicit confirmation before reading any selected project's contents.

Do not follow directory symlinks into other trees by default. Reject filesystem or drive roots and the user's home directory for automatic enumeration. Ask the operator to narrow any plainly over-broad mounted or workspace root.

If a selected path is missing or unreadable, record it as not inspected, explain the limitation briefly, and continue where meaningful. Never infer capability from an unread project.

During the census, inspect directory structure and permitted marker existence only. Do not open documentation, manifests, source, configuration, or other content. Do not suppress ordinary-looking or unfamiliar directories by name. Sensitive-looking non-directory names may be redacted while preserving their count and exclusion reason.

## Mandatory operator signal

Before inspection, say exactly:

```text
This is a read-only cross-project audit.
No repository files will be changed.
The capability map will be returned in chat.
```

## Prohibited actions

Do not create, edit, rename, move, or delete files; run write-producing formatters or generators; install or upgrade dependencies; alter environments, configuration, or secrets; start, stop, restart, or reload services; run migrations; mutate databases or APIs; send messages; publish artifacts; change remotes; initialise or modify Git state; repair audited projects; or create persistent reports.

Use only read-only search and inspection. Live API/runtime checks are excluded unless separately authorised under the project's own runtime contract. A detached probe never creates live truth.

## Discovery breadth and exclusions

Cast a wide net for deliverables relevant to the audit question:

- enduring purpose and observable outcomes;
- required inputs and external capabilities;
- APIs, protocols, stable identifiers, and mapping boundaries;
- owned decisions and workflow actions;
- maturity, tests, and attributable operational evidence;
- deferred capability, contradictions, and material unknowns;
- relationships with other approved projects.

First perform a shallow capability census of every approved project. Establish its apparent purpose, primary documentation and manifests, implementation languages or entrypoints, visible integration surfaces, evidence-bearing tests, maturity clues, and possible relevance. Do not compress or dismiss it during this pass.

Then deepen projects whose evidence is directly relevant to the audit question. Start with applicable agent guidance, root documentation and maps, canonical architecture or contract documents, manifests, safe configuration templates, and status ledgers. Then inspect relevant source, schemas, entrypoints, adapters, configuration loaders, and tests.

Retain adjacent or future-facing signals from the shallow census even when they do not justify a full capability card. A currently out-of-scope project can still expose a reusable integration pattern, identifier, evidence source, workflow boundary, or future consumer. Name-based filtering is never sufficient evidence of irrelevance.

Avoid `.git` internals, dependency trees, caches, generated outputs, binary/media/data bulk, logs, secret-bearing local configuration, tokens, credentials, and unrelated external paths. Safe committed templates may establish configuration shape without exposing values.

## Evidence authority and maturity

Keep intended and observed state separate:

| State | Evidence meaning |
|---|---|
| `live-proven` | Current or cited authorised operator/runtime evidence demonstrates the capability under identified conditions |
| `tested` | Relevant tests exercise the claimed behavior; live operation is not established |
| `implemented` | Current source contains the capability without sufficient test or live evidence |
| `partial` | Necessary machinery exists, but the observable capability is incomplete or materially bounded |
| `documented` | Canonical documentation describes it, but implementation evidence was not found or inspected |
| `deferred` | The project explicitly preserves it for later work and does not claim it exists now |
| `unknown` | Available evidence cannot establish the capability or its absence confidently |

These are evidence states, not quality rankings. When documentation and implementation differ, retain documented intent and observed implementation separately. Surface drift only when it changes the map; do not call either side broken or repair it.

## Capability analysis

For each relevant deliverable establish:

1. observable outcome;
2. required evidence, input, or dependency;
3. enabling API, protocol, identifier, data source, or local mechanism;
4. evidence-backed maturity;
5. whether another project can reuse the evidence without inheriting product policy;
6. decisions that must remain with the consumer;
7. mutations or operations that must remain with the workflow owner;
8. freshness, granularity, ambiguity, and failure states;
9. overlap with another approved project;
10. whether sharing removes real duplication or merely adds a dependency.

Classify each candidate as `reusable evidence`, `consumer policy`, `workflow action`, `shared capability candidate`, `project-local capability`, or `unclear`. Evidence supply never grants decision authority.

## Technical enablers and privacy

Retain concise material facts about service or component, API/protocol/file interface, read or mutation direction, stable identity, source of truth, authentication category, result granularity, provenance, freshness, uncertainty, failure behavior, maturity, and canonical evidence location.

Never expose credential values, private authenticated URLs, hostnames or addresses, signed links, internal account identifiers, user-specific absolute paths, secret filenames without need, or unrelated raw payloads. Prefer service classes, endpoint families, identifier types, protocol direction, auth categories, safe templates, environment-variable names without values, and project-relative evidence references.

A shared-interface candidate should answer a concrete question, expose reusable evidence rather than consumer policy, preserve identity/provenance/freshness/uncertainty, support bounded permissions, avoid silent mutation, and remove genuine duplicated integration work. Do not implement or automatically document a candidate.

## Coverage accountability

Maintain enough structured audit state to account for:

- every immediate census entry and its classification;
- every project approved for inspection;
- whether each approved project was inspected shallowly or deeply;
- every operator exclusion, unavailable path, and unreadable project;
- the evidence-based reason a project was not deepened;
- adjacent or future-facing signals retained from shallow inspection.

The final ledger is evidence of coverage, not a claim that every project deserved equal depth.
