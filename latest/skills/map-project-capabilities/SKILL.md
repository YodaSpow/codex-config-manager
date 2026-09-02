---
name: map-project-capabilities
description: Map what selected projects genuinely deliver and require, then identify reusable capabilities, technical enablers, and project-owned boundaries for the initiating project. Use for explicitly requested read-only cross-project capability or deliverability discovery; do not use for implementation, unrestricted filesystem scanning, or automatic documentation changes.
---

# Map Project Capabilities

**Version:** 1.0 · **Updated:** 31 August 2026

Map an operator-approved project landscape from the viewpoint of the project where the skill was invoked. Establish observable deliverables and requirements, then distinguish reusable evidence from project-owned policy and workflow actions.

## Required workflow

1. Read [references/audit-contract.md](references/audit-contract.md) completely. Establish the audit question. If the user already supplied a clear objective, adopt it. Otherwise ask: **What are you trying to learn or unlock for the current project?**
2. Resolve the initiating project and suggest exactly its parent as the candidate project-group root. Use `scripts/discover_project_group.py suggest` when helpful. Show both paths and obtain confirmation or replacement **before** enumerating or inspecting siblings. Make clear that this first approval authorises a content-free immediate-child census only.
3. After root approval, run `scripts/discover_project_group.py enumerate`. Present every readable immediate directory as a project-folder candidate, grouped into recognised and unclassified folders. Present loose root files, symlinks, and unavailable paths separately; loose files are not project folders and do not inflate project counts.
4. Without an operator allowlist, propose **all readable project-folder candidates** for inspection. If narrowing is proposed or requested, list every selected folder and every not-selected folder one per row, reconcile the counts, and state the coverage consequence. Optional review of loose root tools requires separate approval.
5. Obtain a **second explicit confirmation** for the exact folder-inspection set. Root approval permits enumeration only; this approval permits read-only content inspection of the named folders. An operator may add, remove, or promote any folder candidate.
6. Before inspecting any selected folder, announce exactly:

```text
This is a read-only cross-project audit.
No repository files will be changed.
The capability map will be returned in chat.
```

7. Perform a shallow capability census of **every approved folder**, then deepen only where evidence is directly relevant to the audit question. Do not infer irrelevance from a folder name. Build the complete capability model before compression.
8. Read [references/output-contract.md](references/output-contract.md) completely only after discovery and analysis are complete. Synthesize the status-first map, including early coverage limitations, adjacent and future signals, and a complete folder ledger.
9. Return the capability map in chat. End with the singular new-document offer defined by the output contract, then stop without writing or implementing. The audit itself never creates a file.
10. If the operator immediately accepts that singular offer in a later turn, leave the read-only audit posture and use Mode B to create one **new canonical project document** in the initiating repository. Use the completed audit as the source context; do not require the operator to restate it, merge into an existing document, or begin implementation. If the offer is no longer the active conversational choice or the document destination is materially ambiguous, briefly restate or resolve the intended target before writing.

## Non-negotiable boundaries

- Never treat an inferred path as inspection authority. Suggestion must not enumerate siblings.
- Never treat root approval as content-inspection authority. Account for every immediate entry before the second approval.
- Reject automatic enumeration of filesystem roots, drive roots, the user's home directory, or another plainly over-broad location; ask for a narrower root or exact paths.
- Filesystem type determines folder versus file. A filename extension may subtype a loose file, but must never determine whether an entry is a project-folder candidate.
- Do not silently hide unclassified folders, create a name-based shortlist, or dismiss a project by name. Recognition markers describe evidence; they do not determine relevance.
- Keep the initiating project visually and numerically distinct from sibling comparison projects.
- Never edit projects, install dependencies, alter configuration, operate services, run migrations, mutate APIs or databases, publish artifacts, or change Git state.
- Do not inspect secret files, private infrastructure, unrelated external paths, or live services by default.
- Documentation establishes intent and navigation; source establishes implementation; relevant tests establish tested behavior; only authorised operator/runtime evidence establishes live behavior.
- Classify maturity as `live-proven`, `tested`, `implemented`, `partial`, `documented`, `deferred`, or `unknown`.
- Complete evidence discovery and capability analysis before compression. Preserve every material decision, dependency, constraint, contradiction, technical enabler, and unknown.
- Account for every folder candidate and every approved project in the final ledger, including why anything was excluded, unavailable, or not deepened. Account for loose items separately.
- Keep reusable skill text, generated fixtures, and examples project-neutral. Do not embed personal repository names, personal absolute paths, secret-looking names, or private evidence as reusable examples.
- In generated shell commands, never repurpose shell- or environment-special names such as `PATH`, `path`, `HOME`, `home`, `CDPATH`, `IFS`, `PWD`, `OLDPWD`, `status`, or `CODEX_HOME`; use task-specific variable names.
- Default to chat output. Offering a documentation handoff does not authorise it. Only the operator's acceptance authorises the later Mode B creation of one new initiating-project document; Mode C always requires a separate explicit request.

## Companion skills

Use Operational Modes in Mode A when available. If it is unavailable, this skill's read-only boundary still applies in full.

Use Semantic Compression only for final synthesis after the complete capability model exists. If it is unavailable, apply the lossless compression and fidelity rules in the output contract directly.
