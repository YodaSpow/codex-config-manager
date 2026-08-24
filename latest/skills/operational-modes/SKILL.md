---
name: operational-modes
description: Set and apply the appropriate operating posture for a task through Operational Modes 0, A, B, C, and P. Use whenever the Operational Modes skill is available, including when a user names a mode or when discovery, documentation, implementation, or a prompt for another AI needs its defined workflow and boundaries.
---

# Operational Modes (0/A/B/C/P)

**Version:** 1.0 · **Updated:** 6 August 2026

## Purpose

Operational Modes are a shared language for directing how Codex works on a task. They describe the current kind of work being requested; they do not replace the task goal.

They make complex work repeatable by separating exploration, inspection, decision capture, and implementation, so each is handled with the right boundary and evidence.

- **Goal** is the intended outcome or milestone.
- **Mode** is the current way of working toward that goal.
- **Validation** is the evidence that confirms a milestone or goal is complete.

Modes are building blocks, not a compulsory sequence. A goal can use one mode when that work is the intended outcome, move through several modes, or repeat a mode; use the modes that serve the job.

### How to Use Modes Proportionately

Modes are an escalation path, not permanent ceremony. Use them when uncertainty, consequential change, handoff, or several decisions make structure worthwhile. Retain the structure that continues to make the work safe and repeatable.

A task may be completed through ordinary chat without a named mode. Codex may infer the appropriate posture from the user’s natural language request; named modes make that posture explicit.

## Intended use

Use a mode name naturally at the start of a request to set the working posture. A task can move between modes as its needs change.

The modes are:

1. Mode 0 — discovery and task framing.
2. Mode A — read-only discovery.
3. Mode B — documentation and writing.
4. Mode C — implementation.
5. Mode P — a prompt for another AI.

## Scope Boundary

Operational Modes define task posture. Standing rules for repository and external scope, secrets, proof or test policy, environment conventions, and temporary handoff mechanics belong in applicable global or project guidance, or in a dedicated workflow skill.

## Decision Framework

Use this comparison when a task has materially different viable approaches. It makes trade-offs explicit rather than assuming that the most established pattern is automatically the best fit.

Mode 0 uses it to make exploratory routes tangible. Mode A uses it to turn read-only evidence into options and recommendations for discussion. Mode B records the conclusion and selected approach. Mode C applies that decision; it does not make the decision or reopen it unless the task or evidence materially changes.

For each viable option, compare:

**Option** · **What runs** · **Reliability** · **Setup effort** · **Maintenance** · **Best use**

---

## Mode 0 — Discovery and Task Framing

Mode 0 is the deliberate innovation mode. Use it for a difficult, unusual, or apparently impossible problem where a conventional approach may prematurely choose the path of least resistance and discard valuable possibilities.

Do not use Mode 0 merely because a task is complicated. Well-documented work that follows established patterns should use the normal mode flow. Use Mode 0 when the task needs unfamiliar tools, systems, or assumptions connected in a way that conventional guidance may reject before it has been properly explored.

Mode 0 is not a feasibility gate and not merely a plan. It permits blue-sky thinking: difficult, unconventional, undocumented, or currently impractical ideas remain open for exploration rather than being ruled out prematurely. Some exploration may prove unproductive; that is acceptable when it creates useful knowledge or opens a route conventional discovery would not pursue.

Mode 0 can frame how a possibility might become achievable: the route worth investigating, the assumptions that must hold, and the research, tests, prototypes, or validation that would be needed next. It does not claim that route is already proven or ready to implement.

### Purpose

Pioneer a solution space before implementation: read what is relevant, reason freely, and investigate routes that may be non-standard or initially unattractive, without changing the repository.

### Codex will

- Clarify the request, constraints, assumptions, dependencies, and material decisions.
- Read relevant repository files, documentation, and supplied material.
- Explore creative or unconventional solution paths.
- Propose an execution plan or workflow.
- Evaluate options, trade-offs, risks, and alternative strategies.
- Create architecture sketches, task lists, option or decision matrices, and practical comparisons when useful.
- Identify what should be discovered or validated next.
- Recommend the next mode: A, B, or C.

### Codex will not

- Run commands.
- Create or edit files.

### Typical outputs

- A task plan or workflow.
- An option, decision, or practical comparison matrix.
- An architecture proposal.
- A risk assessment.
- A recommended next mode.

### Transition

- Mode 0 → Mode A for read-only discovery.
- Mode 0 → Mode B for documentation.
- Mode 0 → Mode C for implementation.

---

## Mode A — Read-only Discovery

Use Mode A to establish the current reality of a project, system, document set, or implementation. It is the normal evidence-gathering mode: read what exists, understand it accurately, and surface findings, options, and recommendations without changing anything.

### Purpose

Ground a decision or next step in the actual repository, documentation, configuration, tests, and runtime evidence available to the task.

### Codex will

- Read supplied material and relevant repository content.
- Inspect code, documentation, configuration, tests, and existing conventions.
- Use read-only discovery tools such as `rg`, `find`, `ls`, `cat`, `sed -n`, `head`, `tail`, and `python -c` for printing only.
- Report the current state, observations, gaps, risks, evidence, and important unknowns.
- Use the Decision Framework when there are materially different options, turning the evidence into recommendations for discussion.
- Recommend the appropriate next mode.

### Codex will not

- Edit files.
- Install dependencies.
- Start, restart, or alter services.

### Typical outputs

- An evidence-backed current-state report.
- A diagnosis or discovery summary.
- An option comparison and recommendation.
- A clear next-step recommendation: Mode 0, B, or C.

### Transition

- Mode A → Mode 0 when an unconventional or underexplored route needs wider investigation.
- Mode A → Mode B when findings or decisions need to be captured as documentation.
- Mode A → Mode C when the user has made or authorised a clear implementation decision.

---

## Mode B — Documentation and Decision Capture

Mode B produces documentation only. It turns the current working truth — established evidence, discussion, decisions, goals, and available validation results — into clear documentation for the people and AI working in the current chat, and for people or AI continuing later in a new chat.

### Purpose

Mode B has three roles: document the work, make evidence legible, and make operational documents durable beyond the current chat — without changing the implementation itself.

### Core rules — always

- Create or update project documentation as Markdown.
- Preserve project facts and distinguish evidence from inference.
- When including evidence or proof, capture the relevant result verbatim in a fenced Markdown code block. Truncate only when necessary, without changing the meaning of the evidence.
- Precede a fenced evidence block with a concise, descriptive heading or sentence that identifies what was checked, how it was checked, and why the captured result matters. Use the context-appropriate level of detail.
- Write for both people and future AI: explain the practical meaning clearly while retaining the decisions, constraints, evidence, and technical detail needed to act on it.
- Capture the knowledge requested for the scenario; a focused document does not require a full historical record.
- Number every Mode B document, including one-offs, in one global `Doc N` sequence; never use decimals such as `Doc 101.1`. Use `Doc N — Family — Semantic title`; related documents retain the family label but receive the next global number.
- Use the repository’s existing documentation location.

### Codex will not

- Change application code.
- Change runtime configuration or infrastructure.
- Treat documentation as proof that an implementation exists.

### Typical outputs

- A settled implementation plan.
- A decision record or option comparison.
- A brief, operating guide, runbook, checklist, or handoff.
- Documentation that identifies the current state and any remaining work.
- A durable capture of the current chat and project context for Mode C or a future chat.

### Operational documents — when the document is a milestone, decision, plan, or handoff

- Consolidate Mode A findings, relevant chat discussion, agreed goals, available validation evidence, and the implementation plan; record the selected approach, conclusion, and any Decision Framework used.
- Make the current decision and handoff state understandable without relying on chat history. Capture the relevant working context so a new chat can proceed from the documentation rather than this conversation’s memory.
- When implementation state matters, begin with a concise status block. Use `✅` for implemented or locked work, `▶` for the next decision or action, and `⛔` for work that is not implemented or not authorised; include any relevant live-proven, planned, blocked, or deferred state. Where a status line comes from one specific document, prefix it with its `Doc N` reference; do not force a single-document citation onto cross-document work.
- Cite material evidence or proof. Identify related, revised, superseded, or dependent documents with dates or status where useful, creating a reading map for future people and AI while keeping current state unambiguous.
- Preserve useful history without leaving the current state ambiguous.

### Lifecycle maintenance — when operational-document context is in scope

- Use new documents to resolve drift between earlier plans and current implementation.
- When documentation and implementation diverge, record the documented intended state and the observed repository state with their evidence. Do not assume either is wrong; mark the divergence as a human decision required to align the code, revise the document, or investigate further.
- Choose whether to update an existing document, create a new current canonical document, or mark an older document historical, archived, superseded, or reference-only. Prefer a scoped new canonical document over a large confusing rewrite when it makes current truth more reliable.
- Retain useful history, but mark non-current documents clearly and point to the current source of truth when in scope. After an implemented and validated milestone, update related in-scope documents with the achieved state and implementation date where known, and cite current evidence; do not leave future-tense plans looking current or turn the document into a running execution transcript.

---

## Mode C — Implementation

Mode C applies an agreed decision or goal through repository changes.

### Purpose

Implement the requested work within its agreed scope, then validate and report what actually happened.

### Entry rule

Proceed only when the user explicitly requests implementation changes.

### Codex will

- Use the relevant current-chat context, project documentation, or agreed goal as needed to implement accurately; documentation is not a prerequisite.
- Make the requested changes within the agreed scope and existing project conventions.
- Validate implementation in proportion to its risk and report the evidence, following any applicable project or global test policy.
- State what changed, what was validated, and any remaining limitation or follow-up.

### Codex will not

- Reopen settled decisions or substitute a different implementation approach without a material reason and appropriate clarification.
- Expand into unrelated repositories, external systems, or unapproved actions.

### Typical outputs

- Implemented repository changes.
- Actual validation evidence.
- A concise implementation and remaining-work report.

### Completion and handback

- At completion, give the current chat a concise human-readable status summary: `✅` implemented or locked work, `▶` the next decision or action, and `⛔` work that remains unimplemented or not authorised; include any relevant blocked or deferred state. Where a status line comes from one specific document, prefix it with that `Doc N` reference; do not force a single-document citation onto cross-document work.
- Return to Mode B when an in-scope plan, milestone, handoff, or operational document needs the implementation result, validation evidence, or current status captured.

---

## Mode P — Prompt for Another AI

Mode P creates a structured, copy-paste-ready prompt for another AI tool or platform.

### Purpose

Move a task, context, or brief safely into another AI while retaining the information it needs and removing confidential or sensitive detail.

### Codex will

- Redact confidential detail, internal names, credentials, private URLs, commercially sensitive targets, personal information, private preferences, sensitive subject matter, and other non-shareable context.
- Replace redacted material with neutral, representative wording or placeholders that preserve the task intent without exposing the person, project, content, or wider work context.
- Structure the prompt with clear context, task, constraints, and requested output format.
- Identify anything the receiving AI still needs but cannot be included, such as a file, screenshot, or URL.
- List all redactions at the end for human review before the prompt is sent.

### Redaction rules

- Replace internal colleague names with role titles.
- Remove internal system URLs and credentials.
- Remove commercially sensitive targets or KPIs.
- Replace project-specific, brand-specific, sensitive, or otherwise non-shareable terminology with neutral equivalents or placeholders where necessary.
- When whether material is shareable is unclear, flag it and ask the user before including it.

### Typical triggers

- Use another AI to turn a process document into an infographic outline.
- Use another AI to build a UI component from a CSS specification.
- Request layout or design help while keeping project context generic.
- Explain a process without internal names or sensitive details.
