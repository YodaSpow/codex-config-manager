# Capability-map output contract

Read this reference only after approved folder discovery and capability analysis are complete.

## Required sequence

```text
1. Approved-root census and explicit folder-inspection confirmation
2. Shallow capability census of every selected folder
3. Relevance-led deep inspection
4. Complete capability model
5. Semantic compression
6. Fidelity and coverage check
```

Do not compress projects independently during discovery. Cross-project dependencies, policy boundaries, contradictions, and unknowns must first coexist in the complete model.

For final synthesis, use Semantic Compression when available. Otherwise remove redundancy without changing meaning: preserve intent, decisions, constraints, dependencies, technical accuracy, contradictions, and uncertainty; do not redesign, resolve ambiguity silently, or invent claims. Allow a longer result when shortening would lose material substance.

## Human-readable signal grammar

Use stable signals only where they add meaning:

- `✅` — established, approved, completed, or evidence-backed;
- `▶` — decision, candidate set, next action, or proposed scope;
- `⚠️` — limitation, uncertainty, contradiction, or coverage consequence;
- `⛔` — outside scope, not authorised, not inspected, or deliberately excluded.

Use these on semantic headings or compact status lines, not on every bullet. Keep names one per row when the operator may need to verify or change them. Prefer explicit labels and reconciled counts over arithmetic the reader must infer.

## Default chat result

Return one progressive-disclosure map in this order:

1. **✅ Audit status** — read-only completion state, initiating project, inspected-folder count, and any incomplete authority or availability.
2. **Audit objective** — the initiating question in one concise statement.
3. **Main conclusions** — the most decision-relevant capability findings.
4. **⚠️ Coverage limitations** — immediately after conclusions; state exclusions, unavailable paths, shallow-only boundaries, and evidence gaps that could change interpretation.
5. **Shared capability checklist** — reusable evidence or interface candidates.
6. **Technical-enabler and maturity map** — material APIs, protocols, identities, provenance, freshness, failure semantics, and evidence state.
7. **Project-owned boundaries** — consumer policy and workflow actions that must remain local.
8. **Project capability cards** — deep evidence for directly relevant projects.
9. **Adjacent and future capability signals** — one project per entry, retained from shallowly inspected projects outside the direct shortlist.
10. **Material contradictions and unknowns** — only those that could change the result.
11. **Evidence references** — enough project-relative locations to trace material findings.
12. **Complete folder coverage ledger** — every folder candidate and its inspection or exclusion state.
13. **Optional loose-tool signals** — only when separately authorised; never mix them into project-folder counts.
14. **▶ Optional deeper view** — offer expansion only when it would help.
15. **▶ Available next step — capture this audit** — always end with the singular, bounded new-document handoff below.

Do not ask where to save the audit result and do not create a report during the audit. The final handoff offers a later Mode B action; it does not execute it.

## Audit status block

```text
✅ Audit status

Initiating project: <name>
Approved project folders: <count>
Deeply inspected: <count>
Shallowly inspected: <count>
Not inspected: <count>
Unavailable: <count>
Loose root review: <not authorised, authorised, or not applicable>
```

The initiating project is a viewpoint and may also appear in the approved folder set. Keep it visually distinct from the sibling-comparison count so totals remain unambiguous.

## Project capability card

```text
Project: <name>

Core purpose:
<one sentence>

Relevant deliverables:
- <observable outcome>

Requires:
- <evidence or external capability>

Retains locally:
- <consumer policy or workflow action>

Technical enablers:
- <API, protocol, identity, or component fact>

Maturity:
<state with material qualification>

Relevance:
<one sentence tied to the audit objective>
```

## Shared capability checklist

```text
Capability: <semantic name>

Answers:
- <concrete question>

Required evidence:
- <input and provenance>

Known consumers:
- <approved project or count>

Shared contract:
- <what can be normalized safely>

Must remain outside:
- <consumer policy or workflow action>

Technical enablers:
- <relevant API, protocol, or identity>

Maturity:
<evidence state with qualification>

Fit:
<strong candidate, project-local, or needs evidence>
```

## Shared-service mapping fields

When the initiator is considering a shared service or MCP, retain: candidate surface, question answered, backing enablers, normalized identity/state/provenance/uncertainty, known consumers, excluded consumer-owned decisions, maturity, and unresolved identity/freshness/permission/failure gaps. Do not assume the initiator is an MCP.

## Contradictions, unknowns, and evidence

Preserve a contradiction when it changes capability meaning, maturity, reuse suitability, or an authority boundary. Preserve an unknown when resolving it could change the recommendation. Do not inflate harmless historical wording differences.

Use project-relative references where possible. Distinguish documentation, source, test, and attributable runtime evidence. Never label a capability `live-proven` from source or tests alone.

## Adjacent and future capability signal

Use a concise entry rather than a full card when shallow evidence is material but not directly relevant enough for deep inspection. Keep one project per entry so provenance and operator review remain clear:

```text
Project: <name>
Signal: <reusable pattern, evidence source, integration, identity, or future consumer>
Why it may matter: <connection to the initiating horizon>
Evidence state: <maturity and limitation>
```

Never combine several project names into an opaque bundle.

## Complete folder coverage ledger

Account for project folders separately from loose files:

```text
Folder: <project-folder label>
Classification: <recognised Git, recognised marker, or unclassified folder candidate>
Selection: <selected or not selected>
Inspection: <deep, shallow, not inspected, or unavailable>
Reason: <brief evidence-based explanation>
```

Every approved folder must be `deep` or `shallow`. Every other readable folder candidate must carry an explicit operator exclusion or not-selected decision. Missing or unreadable folders must be `unavailable`. Symlinks remain separately recorded as not followed.

Show and verify:

```text
total readable folder candidates = selected folders + not-selected folders
selected folders = deeply inspected folders + shallowly inspected folders
```

## Optional loose-tool ledger

Include only when loose-item review was separately authorised:

```text
Loose item: <safe label or redacted label>
Classification: <standalone script/executable, document/data, archive, system metadata, sensitive redacted, or other>
Inspection: <shallow, not inspected, unavailable, or redacted>
Reason: <brief scope or evidence explanation>
```

Loose items must never be counted as projects or folded into project capability-card totals.

## Final new-document handoff

End the rendered capability map with this semantic shape:

```text
## ▶ Available next step — capture this audit

This audit is complete and remains chat-only.

If you accept its direction, I can capture the complete audit as the next new
canonical Mode B project document. That document will preserve the material
analysis, evidence, recommendations, limitations, boundaries, and unresolved
decisions from this result. It will not be merged into an existing document,
and no implementation will begin.

Reply “Yes, create the new document” or say how you want the handoff changed.
```

Adapt the prose naturally where needed, but preserve every guarantee. Keep the handoff:

- **singular** — one primary documentation action, not several competing next steps;
- **context-aware** — use the completed audit rather than asking the operator to repeat it;
- **explicitly new** — say `new canonical Mode B project document`;
- **non-blending** — say an existing document will not be changed by default;
- **non-implementing** — say implementation will not begin;
- **concise** — do not repeat the capability map inside the offer;
- **actionable** — provide one minimal affirmative reply;
- **adjustable** — permit the operator to request another documentation treatment.

An optional deeper evidence view may appear earlier, but this documentation offer is the final rendered block.

### Accepted handoff document

If the operator accepts the immediately preceding singular offer, the next turn is Mode B rather than part of the audit. Create one new Markdown document in the initiating project's canonical documentation location and follow its established document-numbering convention. If either is materially ambiguous, show the intended target before writing.

The document is a durable semantic synthesis, not a transcript or recommendation-only summary. Preserve every material:

- status, audit objective, approved scope, and coverage depth;
- conclusion, limitation, accepted direction, and recommendation;
- shared capability candidate and technical enabler;
- maturity state, evidence limitation, and project-owned boundary;
- directly relevant evidence and adjacent or future signal;
- contradiction, unknown, and unresolved design choice;
- sequencing decision and valid future Mode C plan or goal;
- statement of what remains unimplemented.

Documentation does not elevate maturity. Do not rerun discovery merely to recreate facts already established by the accepted audit. Do not merge, append to, rewrite, or supersede an existing document unless the operator explicitly requests that different outcome. Stop after Mode B validation; Mode C requires another explicit request.

Silence, decline, a deeper-view request, or a non-accepting response creates no file. Treat an immediate `yes` or `go ahead` as acceptance only while this singular offer remains the active conversational choice; otherwise briefly restate the intended action.

## Final fidelity check

Before returning, verify that the compact map retains every material:

- deliverable and dependency;
- maturity distinction and evidence limitation;
- reusable-evidence versus policy/action boundary;
- API, protocol, identity, provenance, freshness, and failure fact;
- contradiction, uncertainty, and unavailable-project limitation;
- project relationship that changes the initiating decision;
- adjacent or future-facing signal supported by shallow evidence;
- readable folder candidate, inspection depth, operator exclusion, and unavailability;
- loose-item state, but only when separately authorised;
- count equation and initiator/comparison distinction.
- final handoff clarity: new document, complete audit context, no merge, and no implementation.

Restore anything removed only to make the answer shorter.
