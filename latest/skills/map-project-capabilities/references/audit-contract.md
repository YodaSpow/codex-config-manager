# Read-only audit contract

Read this reference completely before resolving or inspecting the project landscape.

## Initiator and objective

The current project is the initiator and supplies the viewpoint, not authority over neighboring projects. Tie discovery to one accepted audit question. Use whichever lens fits:

- **Outward:** What reusable capability should the initiator provide?
- **Inward:** Which selected projects already solve or expose part of the initiator's problem?
- **Landscape:** Where do selected projects overlap, duplicate capability, or remain correctly separated?

The question narrows the final interpretation, not the integrity of the folder census or shallow discovery. Follow dependencies far enough to understand every material deliverable.

## First checkpoint: approve the census root

1. Resolve the current project, preferring version-control metadata and using conservative project markers only when needed.
2. Suggest exactly one parent directory as the candidate project-group root. Do not enumerate its contents during suggestion.
3. Show the initiating project and proposed root separately. Ask:

```text
▶ Census approval

Initiating project: <path>
Proposed project-group root: <path>

Approving this root authorises a content-free census of its immediate children only.
It does not authorise reading any sibling project contents.

Do you approve this census root, or would you like to replace it or provide exact paths?
```

Reject filesystem or drive roots, the user's home directory, or another plainly over-broad location for automatic enumeration. Ask the operator to narrow it or provide exact project paths.

## Folder-first census

After root approval, enumerate every immediate entry without opening project contents. Classify by filesystem type first.

### Project-folder candidates

- `recognised-git-project-folder` — readable directory with a Git directory or Git worktree file;
- `recognised-marker-project-folder` — readable directory with a conservative project marker;
- `unclassified-project-folder-candidate` — every other readable immediate directory.

Every readable immediate directory remains a project-folder candidate. Recognition is evidence about shape, not relevance or permission to omit it.

### Loose root items

Non-directory entries never inflate project-folder counts. Classify them separately as:

- `standalone-script-or-executable`;
- `document-or-data`;
- `archive`;
- `system-metadata`;
- `sensitive-name-redacted`;
- `other-loose-file`.

Filesystem type determines folder versus file. Extensions may subtype a loose file only. Sensitive-looking loose names may be redacted while preserving count and classification. Do not open loose-item contents during the census.

### Other census outcomes

- `excluded-symlink` — never followed by default;
- `unavailable` — missing, unreadable, or otherwise not safely selectable.

During the census, inspect only entry type, access state, Git-marker existence, conservative project-marker existence, safe file metadata, and loose-file name/suffix where needed for classification. Do not open documentation, manifests, source, configuration, archives, scripts, or other content.

## Inclusive default and narrowing

Without an operator allowlist, the proposed inspection set is **all readable project-folder candidates**: recognised plus unclassified. Never silently shortlist by folder name, domain resemblance, apparent relevance, or marker strength.

When the operator supplies or requests a narrower set:

1. preserve the complete census;
2. list every selected folder one per row;
3. list every not-selected readable folder one per row;
4. show missing or unavailable requested paths separately;
5. reconcile `total folder candidates = selected + not selected`;
6. state that excluded folders will not contribute deliverables, adjacent signals, contradictions, or unknowns;
7. obtain explicit approval for that consequence.

Loose root items are outside the folder audit by default. Offer a separate optional loose-tool review only where useful; approval of project folders does not authorise reading loose files.

## Second checkpoint: approve folder inspection

Present the census with stable, scannable sections:

```text
✅ Census complete

Initiating project: <name>
Readable project-folder candidates: <count>
Loose root items: <count>
Symlinks not followed: <count>
Unavailable paths: <count>

▶ Proposed folder inspection

Selected folders (<count>):
- <one folder per row>

Not selected (<count>):
- <one folder per row, or "None">

⚠️ Coverage consequence
<state the consequence whenever any readable folder is not selected>

Approving this list authorises read-only content inspection of the selected folders only.
It does not authorise inspecting loose root files, changing repositories, or operating services.

Do you approve this exact folder-inspection set, or would you like to add or remove folders?
```

Keep the initiating project distinct from sibling comparison counts. Avoid totals whose meaning requires the operator to reconstruct arithmetic across sections.

## Mandatory operator signal

After the second approval and before any content inspection, say exactly:

```text
This is a read-only cross-project audit.
No repository files will be changed.
The capability map will be returned in chat.
```

## Prohibited actions

Do not create, edit, rename, move, or delete files; run write-producing formatters or generators; install or upgrade dependencies; alter environments, configuration, or secrets; start, stop, restart, or reload services; run migrations; mutate databases or APIs; send messages; publish artifacts; change remotes; initialise or modify Git state; repair audited projects; or create persistent reports.

Use only read-only search and inspection. Live API/runtime checks are excluded unless separately authorised under the project's own runtime contract. A detached probe never creates live truth.

Generated shell commands must use task-specific variable names. Never assign to `PATH`, `path`, `HOME`, `home`, `CDPATH`, `IFS`, `PWD`, `OLDPWD`, `status`, `CODEX_HOME`, or other shell/environment control variables.

## Discovery breadth and exclusions

First perform a shallow capability census of every approved folder. Establish apparent purpose, primary guidance and documentation, manifests, implementation languages or entrypoints, visible integration surfaces, evidence-bearing tests, maturity clues, and possible relevance. Do not compress or dismiss a folder during this pass.

Then deepen folders whose evidence is directly relevant to the audit question. Start with applicable agent guidance, root documentation and maps, canonical architecture or contract documents, manifests, safe configuration templates, and status ledgers. Then inspect relevant source, schemas, entrypoints, adapters, configuration loaders, and tests.

Retain adjacent or future-facing signals from every shallow inspection even when they do not justify a full capability card. A currently out-of-scope project can expose a reusable integration pattern, identifier, evidence source, workflow boundary, or future consumer. Name-based filtering is never sufficient evidence of irrelevance.

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

Reusable skill instructions, examples, fixtures, and generated artifacts must remain project-neutral. Never embed personal repository names or personal absolute paths as demonstrations.

A shared-interface candidate should answer a concrete question, expose reusable evidence rather than consumer policy, preserve identity/provenance/freshness/uncertainty, support bounded permissions, avoid silent mutation, and remove genuine duplicated integration work. Do not implement or automatically document a candidate.

## Coverage accountability

Maintain enough structured state to account for:

- every immediate entry and its filesystem-first classification;
- every readable project-folder candidate;
- every folder approved for inspection;
- whether each approved folder was inspected shallowly or deeply;
- every operator exclusion, unavailable path, unreadable folder, and unfollowed symlink;
- every loose root item and whether optional review was separately authorised;
- the evidence-based reason a folder was not deepened;
- adjacent or future-facing signals retained from shallow inspection.

The final ledger proves coverage, not equal depth. Its folder counts must reconcile independently from loose-item counts.
