---
name: map-project-capabilities
description: Map what selected projects genuinely deliver and require, then identify reusable capabilities, technical enablers, and project-owned boundaries for the initiating project. Use for explicitly requested read-only cross-project capability or deliverability discovery; do not use for implementation, unrestricted filesystem scanning, or automatic documentation changes.
---

# Map Project Capabilities

Map an operator-approved project landscape from the viewpoint of the project where the skill was invoked. Establish observable deliverables and requirements, then distinguish reusable evidence from project-owned policy and workflow actions.

## Required workflow

1. Establish the audit question. If the user already supplied a clear objective, adopt it. Otherwise ask: **What are you trying to learn or unlock for the current project?**
2. Resolve the initiating project and suggest exactly its parent as the candidate project-group root. Use `scripts/discover_project_group.py suggest` when helpful. Show both paths and obtain confirmation or replacement **before** enumerating or inspecting siblings.
3. Support a confirmed root, an allowlist, exact project paths, or multiple custom locations. Show the final project list before inspection. Path approval grants read-only audit scope only.
4. Before inspecting any selected project, announce exactly:

```text
This is a read-only cross-project audit.
No repository files will be changed.
The capability map will be returned in chat.
```

5. Read [references/audit-contract.md](references/audit-contract.md) completely, then perform the approved read-only discovery and build the complete capability model.
6. Read [references/output-contract.md](references/output-contract.md) completely only after discovery and analysis are complete, then synthesize the final map.
7. Return the capability map in chat. Stop without writing reports or implementing discovered candidates.

## Non-negotiable boundaries

- Never treat an inferred path as inspection authority. Suggestion must not enumerate siblings.
- Reject automatic enumeration of filesystem roots, drive roots, the user's home directory, or another plainly over-broad location; ask for a narrower root or exact paths.
- Never edit projects, install dependencies, alter configuration, operate services, run migrations, mutate APIs or databases, publish artifacts, or change Git state.
- Do not inspect secret files, private infrastructure, unrelated external paths, or live services by default.
- Documentation establishes intent and navigation; source establishes implementation; relevant tests establish tested behavior; only authorised operator/runtime evidence establishes live behavior.
- Classify maturity as `live-proven`, `tested`, `implemented`, `partial`, `documented`, `deferred`, or `unknown`.
- Complete evidence discovery and capability analysis before compression. Preserve every material decision, dependency, constraint, contradiction, technical enabler, and unknown.
- Default to chat output. A persistent report requires a separate explicit request and a documentation posture.

## Companion skills

Use Operational Modes in Mode A when available. If it is unavailable, this skill's read-only boundary still applies in full.

Use Semantic Compression only for final synthesis after the complete capability model exists. If it is unavailable, apply the lossless compression and fidelity rules in the output contract directly.
