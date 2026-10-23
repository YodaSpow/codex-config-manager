---
name: computer-use-helper
description: Route multi-surface desktop tasks through explicit, independently authorised phases when no single controller can complete the whole workflow. Use when Terminal, Finder, an application, browser control, or another surface must hand a proven result to the next surface, especially when a route-level refusal risks being mistaken for task-wide impossibility. Do not use to evade an outcome-wide safety, permission, or scope restriction.
---

# Computer Use Helper

**Version:** 1.16 · **Updated:** 23 October 2026

## Purpose

Choose the control lane that matches the real surface, then hand verified state between authorised phases:

> **Axiom — Real AI work must operate the real product surface.** When a project deliberately requires standalone local HTML rather than localhost, Computer Use Helper makes AI operation and validation viable without changing that architecture merely to suit an automation controller.

**Read-before-routing rule:** Read this complete `SKILL.md` before choosing any route. Do not stop at the first plausible route; classify the full thread and task remit, every required surface, all prerequisites, and every handoff first.

Before choosing a route, identify whether the workflow has any native browser or application UI prerequisite. If it does, use Computer Use first and hand off only after that state is verified; otherwise choose the applicable local-file or served-page route.

- **Route 1 — Browser-native UI prerequisite (internal pages, settings, extension management, permission UI, or surrounding browser controls)**

  - ❌ Never send the browser's own privileged interface to browser-tab control.
  - ✅ **Computer Use goes first**: apply authorised native computer control to the native phase, verify its result and make the handoff explicit, then use browser-tab control only for a later ordinary web-content phase.

- **Route 2 — Standalone local HTML (`file:`)**

  - ❌ Browser-tab control does not admit the local-file route.
  - ✅ Use **Computer Use**: Terminal or PowerShell opens the file, the operating system chooses the receiving application, and native control acquires that visible application.

- **Route 3 — Served page (`http:` or `https:`, including localhost) with no native prerequisite**

  - ✅ Use **browser-tab control**.
  - Native Computer Use is not normally needed.

A response governs only the scope it states: one lane, the same operation across surfaces, or the whole outcome. Do not broaden a route-specific limitation into a task-wide blocker, narrow an explicit cross-surface prohibition into permission to reroute, or change the product architecture merely to suit a controller.

Read [Why Computer Use Helper exists](references/why-computer-use-helper-exists.md) when the human rationale, the distinction between control lanes, or the reason for a phased handoff needs to be explained.

## Core model

Treat the work as a sequence of independently completed phases:

1. Define the intended outcome, split native browser controls from page content, and name the observable result each phase must produce.
2. Assign each phase to a surface that is authorised and capable of performing that exact operation.
3. Complete the phase and verify its result on that surface.
4. Hand only the proven result or state to the next surface.
5. Acquire that result on the next surface, verify the phase boundary, and continue.

The receiving surface does not need to reproduce or know the mechanics of the preceding phase. It starts from the established state.

## Hard surface-routing contract

- Route selection **must** follow a complete read of this skill and a whole-task surface map; no individual route may be selected in isolation from later prerequisites or handoffs.
- Browser-internal pages, extension controls, settings, permission prompts, and surrounding browser controls **must** be classified as native application UI before any controller is invoked.
- When a workflow includes a browser-native prerequisite, authorised native computer control **must be the first controller used**. Apply and verify that phase, then state the handoff before invoking browser-tab control.
- Browser-native UI **must not** be sent to browser-tab control. Browser-tab control may follow only for later ordinary `http:` or `https:` page content after the native phase has produced and proved the required state.
- A standalone ordinary `http:` or `https:` page with no native prerequisite remains a browser-tab task; this contract does not make Computer Use the default for unrelated web work.
- An explicit denial that prohibits performing the same operation through another surface is an unconditional stop for the agent on that operation. Do not bypass it with native control, wrappers, indirection, another controller, or claimed user permission. A later action completed independently by the operator may establish a new starting state.

## Platform operating lanes

### macOS — proven

1. Run `scripts/open-local-html-macos.sh "<absolute-html-path>"`, which delegates directly to macOS `open`.
2. Let macOS choose the application associated with the HTML file.
3. Discover the visible receiving application independently.
4. Acquire that application through native computer control.
5. Verify the exact local file and visible page content before continuing.

This lane was proven on 10 October 2026: the shell opened a fresh local HTML file without naming an application, macOS selected the installed browser, and native computer control independently acquired it and verified the intended file and page content.

### Windows PowerShell

1. Run `scripts/open-local-html-windows.ps1 -Path "<absolute-html-path>"`, which delegates directly to PowerShell `Start-Process`.
2. Let Windows choose the application associated with the HTML file.
3. Discover the visible receiving application and exact window independently.
4. Acquire that window through native computer control.
5. Verify the exact local file and visible page content before continuing.

Microsoft documents that `Start-Process` accepts a document path and, for a non-executable file, starts the application associated with that file. The complete Windows handoff was not available for verification during this macOS trial. That evidence gap is not a task-wide blocker: an AI should use the best authorised Windows control surface available, adapt the launch phase when necessary, and verify the visible receiving application before continuing.

## Routing rules

- Prefer the real operator-session surface for user-facing actions: for example, visible Terminal or Finder for launching a local file, then native computer control for the application that opens it.
- Treat a browser's internal pages, extension manager, settings, permission prompts, and surrounding browser controls as native application UI rather than ordinary web content. Apply native computer control first for that phase when authorised; make the verified handoff explicit before using browser-tab control for a later `http:` or `https:` page phase.
- Choose the receiving control surface before handoff. If acquiring an already-open result would require giving a restricted controller the same blocked protocol or operation, that controller is still the wrong surface.
- Use repository-owned launchers, entrypoints, and operator workflows when they exist. A detached backend command is diagnostic unless the applicable project contract makes it authoritative.
- Read a controller rejection narrowly. Record which surface, operation, and protocol or capability failed.
- After a route-local capability failure that does not prohibit an alternate route, reconsider the task decomposition and select another independently authorised surface for the unmet phase.
- Do not feed the rejected operation back into the same controller through wrappers, indirection, or disguised equivalents.
- If a controller expressly prohibits completing the same operation through another surface, do not switch surfaces for that operation. Stop it and request only the smallest required operator action. If the operator later establishes the required state independently, verify that state and continue only with separately authorised later phases; do not describe this as the agent having bypassed the prohibition.
- Do not use a handoff to evade a restriction that clearly governs the outcome itself, crosses the user's authority, or requires new permission.
- Declare a blocker only after the safe, authorised surfaces relevant to that phase have been checked and no viable route remains.

## Canonical local-file handoff

When a browser controller cannot navigate directly to a local file but the product workflow is direct-local:

1. For a browser-page workflow, accept `.html` and `.htm` artifacts only by default. Refuse other file types unless the user explicitly requests that exact type and its native application is part of the intended outcome.
2. Use the applicable platform operating lane above. This phase does not select or control the receiving application.
3. Verify which visible application received the file.
4. Acquire that application as a native application or visible window, using application identity and visible state rather than the local-file URL.
5. Verify the intended HTML page is open in the receiving application.
6. Perform inspection and interaction from that established state.

If the receiving application is a browser, do not bind the page through a browser API that requires the `file:` URL, even if the page is already open; that still re-enters the restricted route. The URL-bound browser controller is not asked to navigate to or acquire the local file and does not need the launch history. The handoff object is the visible native application window containing the open page.

## Browser-native UI to web-content handoff

When one workflow contains both browser-native UI and an ordinary page, Computer Use is the mandatory first phase:

1. Separate the native operation from later page interaction before choosing a controller.
2. Apply authorised native computer control first to the browser's own UI.
3. Verify the native operation's visible result before leaving that surface.
4. State the proven handoff, then acquire the ordinary `http:` or `https:` page through browser-tab control and verify that it reflects the new state.

Do not send the native phase to browser-tab control merely because both phases appear in the same browser. If browser-tab control has already rejected the native operation and expressly prohibited an alternate control route, step 2 is no longer authorised for the agent in that attempt. Stop the operation. A later operator-completed action may supply a new proven starting state for steps 3 and 4, but it does not retroactively authorise the rejected reroute.

## Failure classification

- **Route unavailable:** One surface cannot perform one phase. Re-route that phase only if an authorised alternative exists and no rule or explicit response prohibits the switch.
- **Operation restricted:** A rule or explicit controller response prohibits performing the same operation through another surface. Stop that operation; do not treat the restriction as permission to try a different controller.
- **Handoff incomplete:** The preceding phase did not produce or prove the state required by the next phase. Repair that phase before continuing.
- **Outcome restricted:** A safety, permission, or scope rule applies to the intended outcome across surfaces. Stop rather than re-route.
- **Confirmed blocker:** No safe, authorised, viable surface can complete the required phase.

## User-facing semantics

- Treat a known wrong-lane response as internal routing information, not an error, warning, or degraded outcome.
- Lead with the available working route and its observed result. For example: native computer control is available and operating the direct-local page; URL-bound browser control is not used for local files.
- Suppress controller diagnostics that do not require user action and do not change the requested outcome.
- Surface a route limitation only when it changes scope, reduces the result, requires a user decision, or leaves no authorised handoff.
- Surface an explicit cross-surface prohibition when it stops the operation or requires operator action, while keeping unrelated later phases scoped separately.
- Avoid broad statements such as "browser control failed" when the evidence concerns only one protocol or controller. Name the boundary precisely when it materially matters.

## Completion evidence

Report the phase chain in terms of observable outcomes, not controller internals. For example: native computer control completed and verified the browser-native phase; the handoff was established; browser-tab control then acquired the ordinary page and verified the updated state. Mention an unavailable lane only if it affected the delivered result or requires action.
