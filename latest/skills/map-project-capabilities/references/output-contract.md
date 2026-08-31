# Capability-map output contract

Read this reference only after approved project discovery and capability analysis are complete.

## Required sequence

```text
1. Read-only discovery
2. Capability analysis
3. Complete capability model
4. Semantic compression
5. Fidelity check
```

Do not compress projects independently during discovery. Cross-project dependencies, policy boundaries, contradictions, and unknowns must first coexist in the complete model.

For final synthesis, use Semantic Compression when available. Otherwise remove redundancy without changing meaning: preserve intent, decisions, constraints, dependencies, technical accuracy, contradictions, and uncertainty; do not redesign, resolve ambiguity silently, or invent claims. Allow a longer result when shortening would lose material substance.

## Default chat result

Return one progressive-disclosure map:

1. **Audit objective** — the initiating question in one concise statement.
2. **Project capability cards** — one per relevant project.
3. **Shared capability checklist** — reusable evidence or interface candidates.
4. **Technical-enabler and maturity map** — material APIs, protocols, identities, provenance, freshness, failure semantics, and evidence state.
5. **Project-owned boundaries** — consumer policy and workflow actions that must remain local.
6. **Material contradictions and unknowns** — only those that could change the result.
7. **Evidence references** — enough project-relative locations to trace material findings.
8. **Optional deeper view** — offer expansion only when it would help.

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

## Final fidelity check

Before returning, verify that the compact map retains every material:

- deliverable and dependency;
- maturity distinction and evidence limitation;
- reusable-evidence versus policy/action boundary;
- API, protocol, identity, provenance, freshness, and failure fact;
- contradiction, uncertainty, and unavailable-project limitation;
- project relationship that changes the initiating decision.

Restore anything removed only to make the answer shorter.
