# Why Computer Use Helper exists

> **In plain language:** Most browser work assumes the page is hosted. Some real products are deliberately a single local HTML file and must stay that way. Browser-tab control cannot operate that local-file route, but the product is not broken. Computer Use Helper lets the operating system open the file, then lets AI take over the application that appears. That keeps AI working on the real product instead of replacing it with localhost merely to make automation easier.

## The problem it solves

A computer task may cross several surfaces: Finder, an installed application, an operating-system dialog, a local HTML file, or an ordinary website. No single controller is necessarily able—or authorised—to operate every surface.

The common failure is to choose one controller, encounter a limitation, and conclude that the entire task is impossible. Computer Use Helper prevents that false blocker by treating the work as a sequence of independently verified phases.

Its central rule is:

> A limitation belongs to the control lane that produced it unless a governing rule clearly applies to the whole outcome.

## The two browser-facing lanes

| Surface | Appropriate lane | Why |
|---|---|---|
| A direct-local HTML file | Terminal on macOS or PowerShell on Windows asks the operating system to open the file; native computer control then acquires the visible receiving application | Local-file pages and operating-system dialogs belong to the desktop session. URL-bound browser automation may not admit the `file:` protocol. |
| A served web page using `http:` or `https:` | Browser-tab control is normally preferred | It can inspect and operate the page directly and efficiently without taking over the surrounding desktop. |

The lanes are complementary. Browser-tab control remains the better tool for ordinary served pages. Native computer control is the correct tool when the real workflow lives in an installed application or crosses into operating-system UI.

## Why the handoff is phased

Each phase produces a visible, verifiable state for the next phase:

1. Classify the real surface and the intended outcome.
2. Use Terminal or PowerShell to open an in-scope HTML file through the operating system.
3. Verify which visible application received the file.
4. Acquire that application as a native window.
5. Inspect or operate the page through native computer control.

The receiving controller does not need to repeat or understand the preceding launch. It only needs to verify the state it received.

## Why the platform shell is the local-file front door

Terminal on macOS and PowerShell on Windows already provide the required launch mechanism. They delegate the file to the operating system without coupling the launch phase to a particular receiving application.

The skill bundles two deliberately tiny platform files: `scripts/open-local-html-macos.sh` delegates to `open`, and `scripts/open-local-html-windows.ps1` delegates to `Start-Process`. Which application receives the file is observed and handled in the next phase.

Microsoft's [Start-Process documentation](https://learn.microsoft.com/powershell/module/Microsoft.PowerShell.Management/Start-Process) confirms that a non-executable document path is opened with its associated application on Windows.

## Current platform proof

- **macOS — proven:** the shell opened a fresh local HTML file without naming an application; macOS selected Chrome; native computer control then independently acquired Chrome and verified the exact file and visible page.
- **Windows PowerShell:** the complete handoff was not available for verification during this macOS trial. That absence is an evidence boundary, not a task-wide blocker. An AI should navigate it through the best authorised Windows control surface available and verify the visible receiving application before continuing.

## What a wrong-lane response means

If URL-bound browser control refuses a local-file address, that establishes only that the controller does not support that protocol. It does not establish that:

- the HTML file is broken;
- Chrome cannot open it;
- native computer control is unavailable;
- the product requires localhost; or
- the user must perform the task manually.

Expected wrong-lane diagnostics are internal routing information. They should not be presented as warnings unless they change the outcome, reduce scope, require a decision, or leave no authorised alternative.

## What the helper does not permit

Phasing does not bypass safety, permission, confirmation, or scope boundaries. It only routes an authorised outcome through suitable surfaces. A restriction that governs the outcome itself remains a stop condition regardless of which controller is available.

The helper also does not make native computer control the default for every browser task. It selects the least-privileged lane that can prove the real requirement.

## Origin and reuse

This model was established in Readlane's control-surface routing work, where direct-local browser behaviour had to be distinguished from served-page automation. Readlane's Doc Nineteen remains the project authority for that product and its evidence. This reference carries the reusable human rationale into Computer Use Helper without replacing any repository's own runtime, safety, or proof contracts.
