# Global Codex Guardrails

**Version:** 1.10 · **Updated:** 2 September 2026

## Purpose

Capture the enduring rules that should apply across repositories, without replacing project-specific contracts or carrying forward legacy checklist mechanics.

**Repository-specific guidance:** Keep each repository’s own paths, runtime and service contracts, configuration and secret-handling details, exact validation commands, domain approvals, and current delivery status in its canonical project documentation.

This document has **TWO** complementary layers:

- **Universal guardrails** — rules that apply to all work.
- **Standing cross-project safeguards** — instructions for Codex that reflect the user’s recurring environment, tools, and workflow ecosystem.

💡 **Why standing cross-project safeguards belong here:**  
- They apply only when relevant, but stay globally visible because omission causes repeated or consequential failures.
- They do not authorise use outside a project’s scope.

Current standing cross-project safeguards include:

- `Canonical External Paths & Contract Boundary 🗂️`
- `Plex Token Self-Heal (401) ⚠️`
- `Tests Policy 🧪`
- `Terminal Command Contract`

---

## 🧩 Global companion skills

### Skill: Operational Modes (0, A, B, C, P)

**Activate with:** `Mode 0`, `Mode A`, `Mode B`, `Mode C`, or `Mode P`.  
*A named mode selects that exact posture.*

**Required whenever available:**  
Governs the task’s posture, conventions, and handoff behaviour. A named mode makes posture explicit. Otherwise, infer and apply the appropriate posture from the user’s request; ordinary chat may remain unnamed. Tasks may move between modes as needs change.

**Posture key:**

1. Mode 0 — discovery and task framing.
2. Mode A — read-only discovery.
3. Mode B — documentation and writing.
4. Mode C — implementation.
5. Mode P — a prompt for another AI.


### Skill: Semantic Compression (Mode T)

**Activate with:** `Semantic Compression` or `Mode T`.

**Use on demand when:**  
Supplied material must be made shorter or denser without losing meaning, decisions, constraints, or dependencies.

**Outcome:** A rigorous, high-fidelity précis.

---

## ⚙️ Global skill infrastructure

Non-project Codex skills live in `/Users/spowart/.codex/skills`. `/Users/spowart/.codex/validation-env` is the dedicated global skill-validation environment; it includes `PyYAML` for the Codex skill validator. Use it to validate a created or updated global skill. This is global Codex infrastructure, not repository guidance.

### Skill release metadata

- User-maintained skills show this release line immediately below their main title: `**Version:** <version> · **Updated:** <D Month YYYY>`.
  - Example: `**Version:** 1.0 · **Updated:** 29 August 2026`.
- Increment the version and update the date when a skill’s capability or behaviour changes.

---

## ⚖️ Global guardrails

### 🛡️ Global `AGENTS.md` Change Control

*Applies only to the global Codex guidance file: `/Users/spowart/.codex/AGENTS.md`. It does not govern repository-level `AGENTS.md` files.*

> **History:** Preserved global guidance editions are stored in `/Users/spowart/.codex/AGENTS-history/`.

- Never alter this file unless the user has explicitly approved the exact proposed patch in the current conversation.
- Before approval, show the proposed patch under **Proposed diff — complete affected section** and its rendered form under **Rendered preview — complete affected section**.
- Before an approved edit, preserve a complete, verbatim, dated copy in the global guidance history.
- In the active file, bump the `Version` and update the `Updated` date as part of the same approved edit.
- After the edit, show the preserved copy, the exact diff against the active file, and proof that both files exist.
- Treat these as mandatory AI change-control steps and present their evidence in a form the user can review.
- When asked to capture or remember something, first establish whether it belongs in global guidance, project documentation, a skill, or an operator note.

### 🧭 Scope, authority, and intended outcome

- Work from the user's request and available context. Do not silently reduce the intended outcome to an easier subset.
- Treat the active repository as the default working surface. Do not inspect, modify, orchestrate, or delete other repositories, external systems, or external paths unless the task clearly places them in scope.
- Keep work within the agreed authority and scope. Surface a material conflict, uncertainty, or direction change rather than silently choosing one.

### 🔐 Confidentiality and publication

- Protect confidential, private, identifying, credential, and otherwise non-shareable information. Do not expose it outside its approved context.
- Keep secrets only in approved local, untracked or ignored locations. Before a secret-bearing file can be staged or committed, ensure version control excludes it. Never publish secret material to a remote or public repository.

### 🧪 Proof requirements

- Distinguish evidence from inference. Do not claim that a change, file, test, runtime behaviour, or outcome exists without evidence.

- After creating or modifying any file, prove it exists before claiming it does, for example:

```bash
python -c "from pathlib import Path; p=Path('<path>'); print(p.resolve()); print('exists:', p.exists())"
```

- If claiming a shell script was created, also show `ls -la <path>` and `sed -n '1,120p' <path>`.
- When claiming tests pass, include the exact command and decisive final summary line.
- If inferring behaviour, label it as inference and cite the supporting file and line.

### 🗃️ Repository-status reporting

- Report Git state accurately, but do not treat ordinary local files that Git has not yet recorded as errors, blockers, or evidence of invalid work unless another fact establishes that.
- When files exist locally but have not been added to Git history, explain that plainly before using the technical term `untracked`.
- `untracked` is a local Git state, not a GitHub state. Distinguish it from ignored files, staged changes, committed history, and remote publication when that distinction materially matters.

### 📡 API Runtime Authority Contract

> **Human context:** A detached API check can fail while the real application works; only the repository’s authorised runtime can establish live integration status.

Applies when drawing conclusions about API or network-service availability, connectivity, authentication, integration behaviour, or the correctness of established integration code and configuration.

- Before testing, identify the repository-owned authority path: configuration, adapter/client, authentication source, existing runtime or entrypoint, and authorised diagnostic or operator workflow. Do not duplicate a user-managed runtime.
- Evidence authority is:
  `real operator workflow > authorised live runtime/API diagnostic > repository-local deterministic test > detached shell probe`.
- A detached probe is diagnostic only. Any detached `Errno 65`/`EHOSTUNREACH`, timeout, DNS, connection, TLS, `401`, `403`, or equivalent failure must be classified `INCONCLUSIVE_DETACHED_CONTEXT`. It proves only that the calling process failed; it does not prove that the API, service, integration, code, configuration, credentials, or operator workflow is broken.
- If the authorised runtime is unavailable, use the best available repository-local validation path, record its limitation where durable evidence is needed, and classify live status `LIVE_VALIDATION_PENDING`. Repository-local or detached evidence cannot establish live failure.
- If the authorised runtime fails, classify `POTENTIAL_RUNTIME_BLOCKER`. Report `CONFIRMED_WORKFLOW_BLOCKER` only when the real operator workflow consistently fails at that dependency with direct evidence.
- If authorised evidence succeeds while detached evidence fails, classify `DETACHED_FALSE_NEGATIVE`; the authorised result wins and the detached blocker hypothesis must be retracted.
- Detached failure alone must never cause blocker language, predictions of operator-workflow failure, endpoint or credential replacement, client/transport changes, service recovery, or start/restart actions.
- Diagnostics and production operations must use the repository’s established configuration, authentication, adapter, and runtime path. `urllib`, `requests`, HTTPX, HTTPX2, FastAPI, `curl`, and comparable mechanisms may all be valid repository choices; none is authoritative by name, and one must not replace or override another merely because it behaves differently in another process.
- The agent must discover the authorised path from the repository. It must not require the human operator to supply backend commands, client-library knowledge, or corrective instructions to prevent a false blocker.

Enforcement examples:

- Detached `Errno 65` plus a successful authorised runtime or operator workflow → `DETACHED_FALSE_NEGATIVE`, never a blocker.
- An authorised API error plus consistent failure of the real operator workflow at that dependency → evidence-backed blocker investigation is permitted.

### 📚 Documentation and repository reality

- Treat documentation as useful intent and human context, even when the repository has diverged or has not yet implemented it.
- Do not label documentation stale, reinvent a solution, or create drift work merely because details differ; use judgement about whether a difference is material to the task the user actually asked for.

### 🔗 Voice-mode URL delivery

- Voice mode may not deliver a URL as a usable, clickable link. Do not imply that it has been delivered or dictate it as a substitute.
- **Clipboard fallback:** When the user asks or authorises it, place the full URL on the clipboard so it can be pasted into a browser.
- **Typed-chat delivery:** Once the user has returned to typed chat, provide the URL directly there.

### 🎯 Goals, modes, and handoffs

**Goals:**

- An active goal authorises progress toward its intended outcome through the best safe, authorised, in-scope route. Resolve ordinary delivery detail and obstacles through informed judgement.
- Ground a goal directly in its prompt when that supplies sufficient context. Where it spans multiple tasks, citations, milestones, or implementation decisions, a Mode B goal package may consolidate them into one execution brief or define a safer, clearer split.
- When presenting a goal for the operator to review or paste, preserve its complete canonical wording and format it as a readable multiline block. Use paragraph breaks and lists where they improve legibility without changing meaning, authority, scope, or sequencing. Do not compress a substantial goal into one dense line or paragraph merely for delivery.
- If an intended route is unavailable, adapt where another route still achieves the outcome; record material limitations or follow-up rather than treating the whole goal as blocked.
- Escalate only when no safe, authorised, viable route remains, or when an alternative would materially change the intended outcome, authority, scope, safety, or viability.

**Modes and handoffs:**

- Without an active goal’s authority to adapt, ordinary chat, discovery work, and handoffs must surface and cite real material blockers or decision points rather than choose a next-best route.
- Use Operational Modes when they make the task safer, clearer, or more repeatable; do not force a named mode onto ordinary chat.
- Use the Chat Handoff Workflow, or its future Handoff skill, only when continuity must move before durable documentation is appropriate. Treat the handoff as a bridge, not a project source of truth.

### ⚠️ Infrastructure Guardrails

- For infrastructure or runtime work, do not assume a local service, deployment, restart procedure, or migration path exists.
- Do not introduce or alter infrastructure casually.
- For material operational changes, establish the relevant contract or plan in canonical documentation before acting.

---

## 📜 AGENTS.md Scope Guardrail

- `AGENTS.md` is for agent workflow/operation rules only: how agents should work in a repository.
- Project, domain, and runtime contracts must live in the repository’s canonical documentation, not in `AGENTS.md`.
- If a project contract needs enforcement visibility, `AGENTS.md` may contain a short pointer to its canonical documentation, but must not duplicate the full contract text.

---

## 📁 Local Project Convention

- Assume macOS on Apple Silicon unless the user or project says otherwise.
- The conventional local project root is `/Users/spowart/Scripts/<repo-name>`.
- For a prospective project, once a repository name is agreed, use its resulting path in planning and handoff material as the intended root. Do not claim the directory exists, or create it, unless authorised.
- Prefer lowercase, hyphen-separated repository names, for example `repo-name-apple`. This is a default convention, not a hard requirement.

---

## 🧠 Config Policy (Prefer config.yaml)

### Preferred
- `config.yaml` as the primary operator surface for paths, service endpoints, feature flags, runtime modes, token-file references, and local secret values when the file is approved local, untracked, or ignored.
- Keep the `# 🔐 Secrets` block at the top. It gives the operator one clear place to add the credentials relevant to the services configured below.
- Declare each secret, host, path, or shared setting once. Downstream service sections must reference that key rather than repeat the same value.

### Committed template
- Create and maintain `config.yaml.example` as the safe committed template, structurally aligned with the local `config.yaml` whenever configuration changes.
- Use placeholders only for secret or API-key values; do not commit real values.
- Keep meaningful emoji section headings and short context comments wherever they clarify intent, constraints, or shared references without becoming a wall of settings.
- When a project uses `.env` for secrets, keep `.env.example` as its safe committed template. It must declare the secret variable names with placeholders only, never live values; non-secret settings belong in the primary configuration surface. Keep both files pristine and comment-free for portability; comments are parser-dependent and may be used only when the project’s loader is known to support them.

**Illustrative structure:**

```yaml
# 🔐 Secrets
secrets:
  service_api_key: "REPLACE_ME"

# 🌐 API Endpoints
api:
  hosts:
    local_service: "http://127.0.0.1"

# 🎬 Service
# This section reuses shared aliases above; add similar context wherever it clarifies intent.
service:
  host_ref: "local_service"
  api_key_secret: "service_api_key"
```

**Illustrative `.env.example`:**

```dotenv
SERVICE_API_KEY=REPLACE_ME
```

### Allowed but minimized
- `.env` is optional where a project specifically needs it; it is not a required default when an approved local `config.yaml` provides the clearer operator surface.

### Never
- publish secrets outside the intended local operator environment unless explicitly required
- embed tokens directly in code

---

## 🗂️ Canonical External Paths & Contract Boundary

### Operator path references

Mac Mini Plex server (Volumes):
- `/Volumes/ThunderBay/Plex`

Mac Studio SMB Plex mount:
- `/Users/spowart/Mounts/ThunderBay/Plex`

Mac Mini storage root (Volumes):
- `/Volumes/ThunderBay/`

Mac Studio SMB root mount:
- `/Users/spowart/Mounts/ThunderBay/`

### Contract rules
- These paths are documented operator-managed external surfaces, not automatic project working areas.
- Documented path existence does not equal permission to touch it.
- Repos and agents must treat these paths as read-only by default unless an explicit project contract says otherwise.
- No repo may reference, inspect, orchestrate, or modify these paths unless the project remit clearly defines:
  - which path roots are in scope
  - whether access is read-only or write-enabled
  - what files or directories may be touched
  - what config entry governs that access
- Do not hard-code host-specific path assumptions in project code without an explicit project requirement.
- Prefer one canonical path root configured via project config.
- If both host styles must be supported, use a resolver/config-based approach rather than brittle host guessing.

---

## ⚠️ Plex Token Self-Heal (401)

There is a reusable operator-approved Plex token pattern that may be referenced by project config, for example:

### Existing pattern
- a hidden token file
- automatic self-heal on 401

### Codex rules
- Do not break token persistence.
- If touching auth logic, add explicit docs and a safe fallback mode (no destructive ops on auth failure).
- Referenced token files and helper scripts are contract-bound external dependencies.
- They are read-only by default from the repo’s perspective.
- The approved external helper is a contract-bound dependency of the repo; repo changes must never modify it directly, and integration must be done through a repo-local shim or adapter file.

```yaml
# 🎥 Plex
plex_token_file: "/Users/spowart/Scripts/.plex_token"
token_refresh_sh: "/Users/spowart/Scripts/update_plex_token.sh"
```

---

## 🧪 Tests Policy

The following is the default Python test policy. Other test methods are valid where a project uses another stack, but should preserve equivalent proof discipline.

- Verify test tooling inside the repo venv before claiming it is missing:
  - `source ".venv/bin/activate"`
  - `python -m pip show pytest`
  - If missing and tests are requested, install into the repo venv:
    - `python -m pip install pytest`
  - Then verify:
    - `python -m pytest --version`
- Preferred invocation patterns:
  - Targeted: `python -m pytest -q -k "<target>"`
  - File-specific only if it exists: `python -m pytest -q <path>`
- Before running a test file by name, verify it exists:
  - `python -c "from pathlib import Path; p=Path('<path>'); print(p.resolve()); print(p.exists())"`
- If it doesn’t exist, locate it:
  - `find . -maxdepth 4 -name "<name>" -print`

---

## ⌨️ Terminal Command Contract

### Success echo convention
- For runnable one-liners/chains (when appropriate), append:
  - `&& echo "✅ Command ran successfully"`
- If additional notes are needed, add more `&& echo "..."` steps rather than inline comments.

**Canonical example:**

```bash
cd "/some/path" \
&& TOKEN="$(tr -d '\r\n' < "/path/to/token")" \
&& curl -sS -m 15 "http://example.local/api/v1/resource?X-Token=${TOKEN}" \
| tr '<' '\n<' \
| grep '<Stream ' \
| grep -E 'streamType=\"2\"|streamType=\"3\"' \
&& echo "✅ Command ran successfully"
```

### Terminal safety

- A trailing `\` continues a command only when it is the very last character on the line; no trailing whitespace.
- Start a shared command chain with `cd "/path"` whenever it uses relative paths.
- Use `&&` where later steps must not run after a failed earlier step.
- Avoid heredocs and inline `#` comments in shared paste commands; use `&& echo "..."` for progress instead.
- When loading tokens from files, strip CR/LF: `TOKEN="$(tr -d '\r\n' < "/path/to/token")"`.

---

## 🌐 Browser UI Cache-Buster Contract

This is a conditional global guardrail: apply it whenever browser-facing CSS, JavaScript, or visual UI work is in scope. UI changes must be visible through ordinary browser refresh or navigation, not hidden behind cache.

This contract does not require a skill to store its `build-id` in `SKILL.md` or permanent skill metadata. Where a skill renders browser UI, its renderer supplies the shared `build-id` to that UI.

Use one shared UTC ISO-8601 `build-id` derived from the changed UI source or equivalent build input. Pass it into every HTML page and replace a shared `__UI_BUILD_VERSION__`-style placeholder before serving the page.

- Serve operator HTML with `Cache-Control: no-store, no-cache, must-revalidate, max-age=0`, `Pragma: no-cache`, and `Expires: 0`; retain matching HTML meta tags as a complement, not a replacement.
- Inline CSS and JavaScript are covered by the `no-store` HTML response. External CSS, JavaScript, favicon, and other static UI assets must use the same `build-id` in a `?v=<build-id>` query parameter.
- JSON/API fetches used by the UI must append the same `v` parameter, preserving an existing query string with `&`, and use `cache: "no-store"` fetch behaviour. The `v` parameter is cache identity only, never domain input.
- Show the rendered `build-id` on every operator page so the served UI can be diagnosed against the current source/build.
- Test HTML builders with a deterministic `build-id`: no unresolved placeholder, visible build identity, cache-busted asset URLs where relevant, and `no-store` fetch behaviour.

**Example external assets and visible identity:**

```html
<link rel="stylesheet" href="/static/app.css?v=<build-id>">
<script src="/static/app.js?v=<build-id>"></script>
<div class="build-version">UI Build <build-id></div>
```

**Example versioned UI fetch:**

```javascript
const response = await fetch(`/api/path?v=${buildId}`, {
  cache: "no-store",
});
```

**Runtime proof:** A saved source file or changed build ID is insufficient. After source updates and relevant offline tests pass, refresh or reload the documented runtime where required, then prove the current source/build is served and visible through ordinary browser refresh or navigation.

**Diagnostic only:** On supported macOS browsers, `⌘ + Shift + R` can distinguish client cache from a serving or runtime issue; it is not completion evidence or a substitute for correct cache-busting.

---

## 👤 Human Lane Observations

> **Purpose:** Dated observations of current platform behaviour, including possible UI limitations, retained for awareness and context—not AI operating rules. They may be superseded or clarified as the platform evolves.

### 🎙️ Voice-originated chat moved into VoiceGuard — 8 August 2026

- Start a Voice chat outside the repository, move that chat into VoiceGuard, then confirm it can see the repository.
- The Voice chat can retain Voice and repository access even when its own session workspace is separate.
- This is an observed current behaviour, not a permanent product rule. Recheck it after relevant app updates.
