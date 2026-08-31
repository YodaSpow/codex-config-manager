---
name: map-project-capabilities
description: Map what selected projects genuinely deliver and require, then identify reusable capabilities, technical enablers, and project-owned boundaries for the initiating project. Use for explicitly requested read-only cross-project capability or deliverability discovery; do not use for implementation, unrestricted filesystem scanning, or automatic documentation changes.
---

# Map Project Capabilities

Map an operator-approved project landscape from the viewpoint of the project where the skill was invoked. Establish observable deliverables and requirements, then distinguish reusable evidence from project-owned policy and workflow actions.

## Required workflow

1. Establish the audit question. If the user already supplied a clear objective, adopt it. Otherwise ask: **What are you trying to learn or unlock for the current project?**
2. Resolve the initiating project and suggest exactly its parent as the candidate project-group root. Use `scripts/discover_project_group.py suggest` when helpful. Show both paths and obtain confirmation or replacement **before** enumerating or inspecting siblings.
3. After root approval, run a complete immediate-child census with `scripts/discover_project_group.py enumerate`. Show recognised projects, unclassified directories, excluded non-directories, excluded symlinks, and unavailable paths. Do not infer irrelevance from a name. Support an allowlist, exact project paths, or multiple custom locations.
4. Propose the actual content-inspection list from that census and obtain a **second explicit confirmation**. Root approval permits enumeration only; project-list approval permits read-only content inspection. An operator may promote an unclassified directory or exclude a recognised project.
5. Before inspecting any selected project, announce exactly:

```text
This is a read-only cross-project audit.
No repository files will be changed.
The capability map will be returned in chat.
```

6. Read [references/audit-contract.md](references/audit-contract.md) completely. Perform a shallow capability census of **every approved project**, then deepen only where the evidence is directly relevant to the audit question. Build the complete capability model before compression.
7. Read [references/output-contract.md](references/output-contract.md) completely only after discovery and analysis are complete, then synthesize the final map, including adjacent and future capability signals plus a coverage ledger.
8. Return the capability map in chat. Stop without writing reports or implementing discovered candidates.

## Non-negotiable boundaries

- Never treat an inferred path as inspection authority. Suggestion must not enumerate siblings.
- Never treat root approval as content-inspection authority. Every immediate entry must be accounted for before the second approval.
- Reject automatic enumeration of filesystem roots, drive roots, the user's home directory, or another plainly over-broad location; ask for a narrower root or exact paths.
- Do not silently hide unclassified directories or dismiss projects by name. Recognition markers support classification; they do not determine relevance.
- Never edit projects, install dependencies, alter configuration, operate services, run migrations, mutate APIs or databases, publish artifacts, or change Git state.
- Do not inspect secret files, private infrastructure, unrelated external paths, or live services by default.
- Documentation establishes intent and navigation; source establishes implementation; relevant tests establish tested behavior; only authorised operator/runtime evidence establishes live behavior.
- Classify maturity as `live-proven`, `tested`, `implemented`, `partial`, `documented`, `deferred`, or `unknown`.
- Complete evidence discovery and capability analysis before compression. Preserve every material decision, dependency, constraint, contradiction, technical enabler, and unknown.
- Account for every census entry and every approved project in the final coverage ledger, including why anything was excluded, unavailable, or not deepened.
- Default to chat output. A persistent report requires a separate explicit request and a documentation posture.

## Companion skills

Use Operational Modes in Mode A when available. If it is unavailable, this skill's read-only boundary still applies in full.

Use Semantic Compression only for final synthesis after the complete capability model exists. If it is unavailable, apply the lossless compression and fidelity rules in the output contract directly.
