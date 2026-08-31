# Capability-map output contract

Read this reference only after approved project discovery and capability analysis are complete.

## Required sequence

```text
1. Approved-root census and second scope confirmation
2. Shallow capability census of every selected project
3. Relevance-led deep inspection
4. Complete capability model
5. Semantic compression
6. Fidelity and coverage check
```

Do not compress projects independently during discovery. Cross-project dependencies, policy boundaries, contradictions, and unknowns must first coexist in the complete model.

For final synthesis, use Semantic Compression when available. Otherwise remove redundancy without changing meaning: preserve intent, decisions, constraints, dependencies, technical accuracy, contradictions, and uncertainty; do not redesign, resolve ambiguity silently, or invent claims. Allow a longer result when shortening would lose material substance.

## Default chat result

Return one progressive-disclosure map:

1. **Audit objective** — the initiating question in one concise statement.
2. **Scope census** — all immediate entries, their classifications, and the operator-approved inspection set.
3. **Project capability cards** — one per directly relevant project.
4. **Shared capability checklist** — reusable evidence or interface candidates.
5. **Technical-enabler and maturity map** — material APIs, protocols, identities, provenance, freshness, failure semantics, and evidence state.
6. **Project-owned boundaries** — consumer policy and workflow actions that must remain local.
7. **Adjacent and future capability signals** — concise signals retained from shallowly inspected projects outside the direct shortlist.
8. **Material contradictions and unknowns** — only those that could change the result.
9. **Evidence references** — enough project-relative locations to trace material findings.
10. **Coverage ledger** — every census entry and approved project, with inspection depth or exclusion/unavailability reason.
11. **Optional deeper view** — offer expansion only when it would help.

Do not ask where to save the result and do not create a report by default. Persistence is a separate explicit documentation request.

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

Use a concise entry rather than a full card when shallow evidence is material but not directly relevant enough for deep inspection:

```text
Project: <name>
Signal: <reusable pattern, evidence source, integration, identity, or future consumer>
Why it may matter: <connection to the initiating horizon>
Evidence state: <maturity and limitation>
```

## Coverage ledger

Account for all scope, not merely positive findings:

```text
Entry: <project or immediate-child label>
Classification: <recognised, unclassified, non-directory, symlink, unavailable, or operator-excluded>
Inspection: <deep, shallow, not inspected, or unavailable>
Reason: <brief evidence-based explanation>
```

Every approved project must be `deep` or `shallow`. Every other census entry must carry an explicit exclusion, unavailability, or operator decision. Redact sensitive-looking non-directory names where revealing them is unnecessary.

## Final fidelity check

Before returning, verify that the compact map retains every material:

- deliverable and dependency;
- maturity distinction and evidence limitation;
- reusable-evidence versus policy/action boundary;
- API, protocol, identity, provenance, freshness, and failure fact;
- contradiction, uncertainty, and unavailable-project limitation;
- project relationship that changes the initiating decision.
- adjacent or future-facing signal supported by shallow evidence;
- census entry, inspection depth, exclusion, and unavailability accounted for in the coverage ledger.

Restore anything removed only to make the answer shorter.
