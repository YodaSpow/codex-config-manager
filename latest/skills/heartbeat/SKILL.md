---
name: heartbeat
description: Audit and repair a repository's project-context routing when AGENTS.md, a next-steps file, or a growing documentation list gives future agents too much history but too little current authority. Produce a compact current baseline plus task-specific routes while preserving provenance. Do not use for scheduled monitoring, runtime health checks, or ordinary status summaries.
---

# Heartbeat

**Version:** 1.0 · **Updated:** 15 September 2026

## Purpose

Give a mature project a reliable heartbeat: a small, current context package that tells a fresh agent what is true now, what remains permanently important, what work is authorised, and where to look for task-specific detail.

The skill does not compress the whole project into one monolithic document. It routes context deliberately so history remains available without becoming mandatory startup load.

## Core model

Classify project material into five roles:

1. **Durable foundation** — identity, domain invariants, safety and ownership boundaries that remain true across milestones.
2. **Current state** — the latest verified schema, production state, completion report, or equivalent present-tense authority.
3. **Execution authority** — the active goal, approved plan, or explicit operator instruction that permits work. Documentation alone does not activate execution.
4. **Task route** — specialist contracts and reports needed only for a relevant topic such as providers, testing, deployment, artwork, or producers.
5. **Historical evidence** — superseded, completed, rejected, or intermediate material retained for provenance and explanation.

Do not infer that a higher document number is more authoritative. Supersession may be partial. Do not call a document stale merely because it is old; establish its present role from status language, explicit precedence, current implementation, and later references.

## Workflow

### Establish repository reality

Inspect the repository-level agent guidance, documentation index, goal index, active goal, current status or heartbeat document, and implementation surfaces relevant to the request. Use document headings, status blocks, links, and explicit supersession statements to locate likely authorities before reading deeper.

Read enough source material to distinguish current contracts from reports and history. Do not read every numbered document merely because it exists.

### Build the heartbeat

Select the smallest always-read set that lets a fresh agent understand:

- what the project is;
- its canonical domain and irreversible invariants;
- its standing safety boundaries;
- its current goal and activation state;
- its current implementation or production contract; and
- its latest verified material state.

Prefer a short ordered list, usually five to eight items. Include the repository's documentation index when it provides the discovery map. Do not force this count when the project genuinely needs fewer or more.

Then define conditional routes by real task area. Each route should point to the current entry document and tell the agent how to reach supporting or historical evidence. Keep detailed project contracts in canonical documentation; `AGENTS.md` should contain workflow instructions and concise pointers, not copied domain content.

### Preserve authority and provenance

- Keep historical documents intact unless the user separately asks to revise them.
- Preserve explicit precedence and partial supersession.
- Make clear that completed reports prove prior work but do not reactivate it.
- Require the active goal and current implementation to be checked before consequential work.
- Retain project-specific safety and permission boundaries even when shortening the reading map.
- Do not turn discoverability into authority: a linked document does not itself permit external access, mutation, deployment, or live operations.

### Apply only when authorised

For a read-only audit, present the proposed always-read baseline, task routes, items moving to historical-on-demand status, and any unresolved authority conflicts.

When the user asks to apply the correction, update the repository-level guidance and any necessary documentation index. Do not alter global guidance or existing global skills unless the user separately authorises that protected surface and its required change-control process.

Avoid adding another monolithic “current state” document when routing existing authorities is sufficient. Create a new project document only when a genuinely new contract, decision, or durable protocol needs its own home.

## Validation

After an applied correction:

- prove every referenced file exists;
- confirm the always-read set includes current state rather than only project inception;
- confirm specialist subjects remain discoverable through conditional routes;
- confirm historical evidence has not been deleted or silently rewritten;
- confirm the guidance does not imply authority beyond the active goal;
- run whitespace or formatting validation appropriate to the repository; and
- show the exact changed guidance and its recovery or version-control state when required by the governing change-control rules.

The result is successful when a fresh agent can enter the repository with a small accurate baseline, find deeper context on demand, and avoid both legacy drift and indiscriminate context loading.
