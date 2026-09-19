---
name: phase-visibility
description: Create or reconcile an on-demand phase-completion index for a docs-first, multi-phase project, linking durable phases to disposable numbered goal attempts, execution authority, evidence, and next gates. Use when the user asks for phase visibility, a roadmap status table, goal-to-phase tracking, or a clear record of what executed each phase. Do not use for ordinary status summaries, runtime monitoring, AGENTS.md reconciliation, or projects without a meaningful phased plan.
---

# Phase Visibility

**Version:** 1.0 · **Updated:** 19 September 2026

Give a project one durable, at-a-glance view of where its phased initiative
stands, which authority executed or will execute each phase, where the evidence
lives, and what gate comes next.

Use this skill only when the visibility is useful. Do not impose phase tables,
goal folders, or extra documents on every repository.

## Core model

Keep these concerns distinct:

- **Canonical project documentation** owns durable intent, architecture, and
  phase definitions.
- **The phase-completion index** is a slow-changing projection of phase status,
  execution authority, decisive evidence, and next gate.
- **Goal files** are disposable execution attempts. Their numeric identity is
  durable enough to cite, but they do not become the project roadmap.
- **The live checklist or equivalent evidence source** owns detailed current
  work, validation, and operational truth.

A goal completing does not automatically mean its phase completed. A goal may
be partial, superseded, or followed by a residual goal. The index must preserve
that distinction.

## Begin with discovery

Announce why Phase Visibility applies. Then inspect only the project material
needed to locate:

1. the repository's operating instructions;
2. the canonical roadmap, blueprint, plan, or initiative document;
3. the live checklist, status, audit, or evidence authority;
4. existing goal files and their current states; and
5. any decision log that materially governs the phases.

Respect the active operating mode and repository scope. Phase Visibility does
not itself authorise implementation, cross-project inspection, external
actions, protected-file changes, or deletion.

If the project has no meaningful multi-phase initiative, do not manufacture
one merely to use the skill. Explain that the pattern is not yet useful or
limit the work to a review-only proposal.

## Place the index

Prefer the canonical document that already defines the phases. Put the index
near its top, after the document status and before the detailed phase
narrative. Create a separate project document only when no existing canonical
surface is suitable and the user has authorised that documentation change.

Do not put project phases, goal history, or evidence tables in `AGENTS.md`.
Global or repository `AGENTS.md` may contain only a short workflow pointer
when separately approved.

When a concrete pattern would help, read
[`references/worked-example.md`](references/worked-example.md). It shows the
default repository layout, a goal file, and index transitions for dormant,
active, completed, partial, and superseded execution attempts. Adapt it to the
project; do not copy it mechanically.

Use the smallest useful table:

| Phase | Status | Execution authority | Completion evidence or next gate |
|---|---|---|---|
| Phase 1 — Example foundation | ⚪ Planned | Dormant `Goal 01` | Invoke Goal 01. |

Use these states consistently:

- `✅ Completed` — the phase outcome is proven and linked to decisive evidence.
- `🟨 Active` — work is currently executing under the named authority.
- `⚪ Planned` — the phase exists but no implementation is active.
- `⛔ Gated` — the phase cannot start until a named prerequisite or approval.

Add another state only when the project already has a necessary established
vocabulary. Do not use a green tick for documentation intent, a completed goal,
or a successful subtask when the phase outcome itself remains incomplete.

## Record execution authority

Name the actual route that controls or controlled delivery:

- a linked numbered goal such as `Goal 01`;
- an explicitly approved Mode C package;
- a named migration, incident, or other bounded implementation package; or
- `No executable authority yet` when the phase is still conceptual.

The goal number is the stable citation. A descriptive filename suffix is a
navigation aid, not semantic project truth. Prefer links so the operator can
open a goal and decide whether it is current, historical, partial, or
superseded.

When execution changes, preserve meaningful history without letting the cell
become a narrative wall. Examples:

- `Goal 01 — completed; phase evidence accepted`
- `Goal 01 — completed partial; residual work in dormant Goal 02`
- `Goal 01 — superseded before execution; active Goal 02`
- `Approved Mode C package — completed 19-09-2026`

If several attempts need fuller history, keep the current authority concise in
the index and link to the live checklist or a small goal register. Do not make
the phase depend on a deleted link. Retire, archive, replace, or remove a goal
only under the repository's convention and the user's authority; disposable
does not mean erase evidence automatically.

## Reconcile lifecycle transitions

### When a goal is prepared

- Keep the phase `⚪ Planned`.
- Link the dormant goal as its proposed execution authority.
- State the invocation or approval needed to start.

### When execution starts

- Change the phase to `🟨 Active`.
- Name and link the active goal or approved package.
- Point to the live work surface rather than copying task detail into the
  index.

### When an execution attempt finishes

Reconcile the attempt against the phase outcome:

- If all phase gates and evidence pass, mark `✅ Completed`, record the actual
  authority and completion date, and link decisive evidence.
- If useful work landed but the phase remains incomplete, do not mark it
  completed. Record the completed partial attempt and identify the residual
  next authority or gate.
- If the attempt was abandoned or superseded, keep the phase planned or active
  as reality requires and identify the replacement.
- If evidence conflicts, retain the non-completed state and surface the
  conflict rather than choosing the most convenient source.

### When phases change

Update the canonical phase definition first. Then reconcile the index, goal
links, live evidence, and next gate. Do not silently rewrite historical goal
scope to make it appear aligned with a later phase definition.

## Goal-folder behaviour

Use a repository-level `goals/` directory when the user requests goal-backed
execution or the repository has already adopted it. Do not create it merely
because the skill is active.

Default to one Markdown file per goal inside that directory, for example
`goals/01-foundation.md` and `goals/02-residual-work.md`. The numeric prefix is
the stable citation; the descriptive suffix is only a navigation aid. Create a
subdirectory for an individual goal only when it genuinely owns several
supporting artifacts that would otherwise clutter the shared folder.

A goal file should normally state:

- numeric identity and current state;
- invocation contract;
- bounded objective and canonical sources;
- authority activated only on invocation;
- milestones or coherent delivery stages;
- acceptance evidence;
- explicit exclusions and pause points; and
- final handoff requirements.

Goal files start dormant unless the user explicitly invokes them. They may
cite canonical documentation but must not replace it. Later goals may finish,
correct, or supersede earlier attempts without changing the durable phase
identity.

## Avoid a second heartbeat

The index answers only:

- Where are we?
- What delivered or will deliver this phase?
- Where is completion proven?
- What is the next gate?

Keep task lists, logs, test transcripts, operational observations, and detailed
handoff in the project's existing live evidence surface. Link to that evidence
from the index. Update the index only for phase starts, completions, material
reframing, authority replacement, or changed gates.

## Validation and handoff

After changes:

1. prove every created or modified file exists as required by the repository;
2. validate internal links and Markdown structure;
3. confirm there is exactly one phase index in its canonical location;
4. confirm the live heartbeat or checklist was not duplicated;
5. confirm every completed claim has evidence;
6. report whether any goal is dormant, active, partial, superseded, or
   completed; and
7. state the next gate without starting it unless authorised.

When the user wants global `AGENTS.md` awareness, keep the mention short and
point to this skill's purpose. Follow the protected global-guidance review,
backup, version, approval, application, and proof process. Never place this
skill's full workflow in global guidance.
