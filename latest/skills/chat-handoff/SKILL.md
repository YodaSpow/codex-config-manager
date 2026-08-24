---
name: chat-handoff
description: Create a complete, copyable continuity prompt for moving same-project work into a fresh chat, or bootstrap a fresh chat from one. Use when the user requests a handoff, new-chat bootstrap, repo prompt, or the current chat is too large to continue safely. Preserve active rationale and transitional context without treating the handoff as the canonical project record.
---

# Chat Handoff (Mode H)

**Status:** Approved source — promoted as a global skill  
**Version:** 1.0 · **Updated:** 6 August 2026  
**Source:** [Doc 5 — Chat Handoff Skill Review](/Users/spowart/Scripts/voice-guard/Docs/ChatGPT%20Guidance/DOC_5_CHAT_HANDOFF_SKILL_REVIEW.md)

## Purpose

Preserve continuity when work must move to a new chat before durable Mode B documentation is appropriate. A handoff is a temporary bridge, not a competing project source of truth. Its prompt must carry enough context for safe continuation without claiming unperformed discovery, implementation, validation, or documentation.

Carry the originating chat's active rationale and transitional context, including work not yet fully represented in the repository or durable docs. Use available repository state and cited docs as supporting evidence to verify, extend, or stabilise that context; their absence must not prevent a safe handoff.

> **In plain language:** A new chat does not automatically carry the working context of the previous one. This is an accelerator for continuing the same project in a fresh chat: it makes that reset controlled, not amnesiac, while global safeguards still govern what may be shared or done.

## Use when

Use when the user requests a new or bootstrapped chat, a repo prompt, or the current chat has become too large to continue safely. Do not substitute handoff for a durable record: return to Mode B when a decision, evidence, milestone, or handoff record must persist.

## Generate the handoff prompt

Begin with this exact line:

`Quoted hand-off prompt from previous AI chat for new chat bootstrap:`

This marks the prompt as an AI-to-AI working brief. The receiving chat uses it for orientation, then responds in clear human-facing language rather than echoing internal technical wording. This rationale belongs to the originating chat's skill instructions; include only the provenance line in the generated prompt.

Include:

- current task, intended outcome, scope, and authority;
- originating chat's rationale, decisions, constraints, assumptions, unresolved questions, evidence, completed and remaining work, limitations, and intended next posture or mode;
- a clear note when durable documentation has deliberately not been created or updated;
- project root as a full absolute path;
- relevant and available files or documents, their full absolute paths, why each matters, and any foundation that must not be skipped or silently replaced;
- relevant secondary docs, configuration, code areas, or evidence when available;
- divergence, incompleteness, or verification still needed between handoff context, docs, and repository state; and
- whether the next pass is read-only and all important constraints and boundaries.

Return the entire generated prompt in one fenced code block. Do not split, abbreviate, or place any copyable part outside it. Do not claim bootstrap or discovery has already happened unless it has.

## New-chat bootstrap

When a prompt begins with the exact handoff line, treat it as read-only bootstrap or discovery unless it explicitly says otherwise.

### Actions

- Read `AGENTS.md` first when it exists in the active repository.
- Read supplied handoff or source-of-truth docs by absolute path when available.
- Prioritise a named work area.
- Scrutinise docs against repository code, configuration, tests, and available tools before trusting them.
- Build context as though the new AI has never worked on the repository.

### Boundaries

- Do not edit, install dependencies, restart services, or suggest version-control workflow during a read-only bootstrap unless explicitly requested.
- Do not treat a handoff as a canonical project record.
- Surface material divergence or uncertainty with evidence; do not silently redesign.

## Final check

Before returning, verify that the handoff preserves task, outcome, evidence, decisions, constraints, authority, next posture, and any available reading path needed for safe continuation.
