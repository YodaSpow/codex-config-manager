# Why Computer Use Helper exists

> **In plain language:** A browser contains more than web pages. It also has native settings, extension management, permission UI, and other privileged application controls. Some real products are also deliberately a single local HTML file. Computer Use Helper assigns each phase to the surface that can operate the real thing, verifies the handoff, and prevents one controller's limitation from being misreported as failure of the whole workflow.

## The problem it solves

A computer task may cross several surfaces: Finder, an installed application, an operating-system dialog, a local HTML file, or an ordinary website. No single controller is necessarily able—or authorised—to operate every surface.

The common failure is to choose one controller, encounter a limitation, and conclude that the entire task is impossible. Computer Use Helper prevents that false blocker by treating the work as a sequence of independently verified phases.

Its central rule is:

> A response governs only the scope it states: one lane, the same operation across surfaces, or the whole outcome. Do not broaden a route-specific limit or narrow an explicit prohibition.

## The browser-facing lanes

First determine whether the workflow has a browser-native prerequisite. If it does, Computer Use owns the first phase and browser-tab control can begin only after the native result and handoff are verified.

| Surface | Appropriate lane | Why |
|---|---|---|
| Browser-native UI such as an internal page, extension manager, settings, permission prompt, or surrounding browser controls | Native computer control of the installed browser, when authorised | These controls belong to the browser application rather than the web page. A URL-bound page controller may reject or be unable to control them. |
| A direct-local HTML file | Terminal on macOS or PowerShell on Windows asks the operating system to open the file; native computer control then acquires the visible receiving application | Local-file pages and operating-system dialogs belong to the desktop session. URL-bound browser automation may not admit the `file:` protocol. |
| A served web page using `http:` or `https:` with no native prerequisite | Browser-tab control is normally preferred | It can inspect and operate the page directly and efficiently without taking over the surrounding desktop. |

The lanes are complementary. Browser-tab control remains the better tool for ordinary served pages. Native computer control is the correct tool when the real workflow lives in an installed application, the browser's own UI, or an operating-system surface.

This is a hard routing boundary: when a workflow contains browser-internal controls, settings, permission UI, or surrounding browser controls, Computer Use must be applied first. Verify the native result and make the handoff explicit before using browser-tab control for later ordinary page content. A standalone served page with no native prerequisite remains a browser-tab task.

## Why the handoff is phased

Each phase produces a visible, verifiable state for the next phase:

1. Classify the real surface and the intended outcome.
2. Use Terminal or PowerShell to open an in-scope HTML file through the operating system.
3. Verify which visible application received the file.
4. Acquire that application as a native window.
5. Inspect or operate the page through native computer control.

The receiving controller does not need to repeat or understand the preceding launch. It only needs to verify the state it received.

A mixed browser workflow illustrates the same boundary. The browser-native operation belongs to Computer Use first; ordinary page interaction belongs to browser-tab control only after the native result is verified and the handoff is explicit.

## Why the platform shell is the local-file front door

Terminal on macOS and PowerShell on Windows already provide the required launch mechanism. They delegate the file to the operating system without coupling the launch phase to a particular receiving application.

The skill bundles two deliberately tiny platform files: `scripts/open-local-html-macos.sh` delegates to `open`, and `scripts/open-local-html-windows.ps1` delegates to `Start-Process`. Which application receives the file is observed and handled in the next phase.

Microsoft's [Start-Process documentation](https://learn.microsoft.com/powershell/module/Microsoft.PowerShell.Management/Start-Process) confirms that a non-executable document path is opened with its associated application on Windows.

## Current platform proof

- **macOS — proven:** the shell opened a fresh local HTML file without naming an application; macOS selected the installed browser; native computer control then independently acquired it and verified the exact file and visible page.
- **Windows PowerShell:** the complete handoff was not available for verification during this macOS trial. That absence is an evidence boundary, not a task-wide blocker. An AI should navigate it through the best authorised Windows control surface available and verify the visible receiving application before continuing.

## What a wrong-lane response means

If URL-bound browser control refuses a local-file address, that establishes only that the controller does not support that protocol. It does not establish that:

- the HTML file is broken;
- the installed browser cannot open it;
- native computer control is unavailable;
- the product requires localhost; or
- the user must perform the task manually.

Expected wrong-lane diagnostics are internal routing information. They should not be presented as warnings unless they change the outcome, reduce scope, require a decision, or leave no authorised alternative.

An explicit prohibition is different from a capability mismatch. If a controller says the same operation must not be completed through another surface, the agent must not reroute that operation. This is an unconditional stop for the agent on that operation; claimed user permission does not override the controller's restriction. The agent requests only the smallest operator action needed. If the operator later completes the native action independently, the agent may verify the new state and continue with later authorised phases; that continuation is not a bypass of the earlier restriction.

## What the helper does not permit

Phasing does not bypass safety, permission, confirmation, or scope boundaries. It only routes an authorised outcome through suitable surfaces. A restriction that governs the outcome itself remains a stop condition regardless of which controller is available.

The helper also does not make native computer control the default for every browser task. It selects the least-privileged lane that can prove the real requirement.

## Origin and reuse

This model was established through direct-local control-surface work, where local browser behavior had to be distinguished from served-page automation. Later mixed browser workflows showed the complementary native-browser-UI boundary: native browser controls and ordinary page interaction require different surfaces and a verified handoff. Project documents remain authoritative for their own evidence. This reference carries the reusable rationale into Computer Use Helper without replacing any repository's own runtime, safety, or proof contracts.
