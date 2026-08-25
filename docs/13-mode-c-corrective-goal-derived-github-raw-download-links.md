# Doc 13 — Mode C Corrective Goal — Derived GitHub Raw Download Links

**Status:** Corrective implementation complete locally; Git publication and live README acceptance pending
**Decision date:** 25 August 2026
**Scope:** Reject the live-failing same-origin `?raw=1` README ZIP-link approach and replace it with absolute `raw.githubusercontent.com` URLs derived from validated Git repository identity and configured branch
**Related documents:** [Doc 7 — Portable Global Guidance and Per-Skill ZIP Distribution](07-implementation-discovery-portable-skills-zip-distribution.md) · [Doc 8 — Root-Level Latest Managed Snapshot](08-architecture-reconciliation-root-level-latest-managed-snapshot.md) · [Doc 10 — Implementation Architecture and Operations](10-implementation-architecture-and-operations.md) · [Doc 11 — Mac Studio Validation Evidence](11-validation-evidence-mac-studio.md)

## Status

- ✅ The ordinary relative `latest/AGENTS.md` link is proven useful and remains the required GitHub rendered-preview lane.
- ✅ The ZIP artifacts themselves remain valid, deterministic and correctly placed under `upload-ready/`.
- ❌ Relative ZIP links with `?raw=1` are rejected as the final README download contract: an external navigation can download successfully, but an operator click from GitHub's rendered README produced GitHub's **Error loading page** state.
- ✅ GitHub's repository Contents API exposes the corresponding absolute `raw.githubusercontent.com` URL as the file's `download_url`.
- ✅ The repository already has a validated Git remote identity and configured branch from which the public raw URL can be derived without adding a second operator-maintained repository identity.
- ✅ The authorised corrective goal implements the derived absolute raw-link contract through explicit validated-identity propagation, focused tests, bounded README output and current-document reconciliation.
- ▶ Git publication and the blocking live README click acceptance remain pending.
- ✅ Configuration, ZIP artifacts, launchd, consumer behavior and Codex-managed state remain unchanged.

## Purpose

The first direct-download correction added `?raw=1` to repository-relative ZIP targets. Command-line HTTP validation proved that GitHub's server redirects those targets to raw ZIP content, and an externally opened test link downloaded successfully. That evidence did not prove the distinct user path of clicking the same-origin link from inside GitHub's rendered README.

The operator subsequently performed that missing test. GitHub remained on the repository `/blob/` URL and rendered an **Error loading page** state instead of completing the ZIP download. The correction therefore improved one navigation context while regressing the actual repository-front-page interaction it was intended to serve.

This record makes that failed approach durable, rejects it as the final contract, and defines the bounded replacement and its stricter completion evidence.

## Current verified baseline

The repository and remote identity were rechecked on 25 August 2026 before this document was created:

```text
local HEAD:   1f41f3d5424db84565be2ee0d2961072d502888f
origin/main:  1f41f3d5424db84565be2ee0d2961072d502888f
remote URL:   git@github.com:YodaSpow/codex-config-manager.git
branch state: ## main...origin/main
```

The current configured Git contract already declares:

```yaml
git:
  remote: "origin"
  branch: "main"
  url: "git@github.com:YodaSpow/codex-config-manager.git"
```

The existing Git validation compares the actual selected remote URL with `git.url` when that value is configured and rejects a mismatch before publication. The corrective implementation must reuse that validated identity rather than introduce a second independently maintained owner or repository setting.

## Failure evidence and rejected approach

### Rendered README target

GitHub's live rendered repository page turns the current relative skill ZIP target into this same-origin link:

```html
href="/YodaSpow/codex-config-manager/blob/main/upload-ready/skills/chat-handoff.zip?raw=1"
```

### Server transport succeeds outside the failing page interaction

Following that URL as a normal HTTP request produces a valid redirect chain:

```text
HTTP/2 302
content-type: text/html; charset=utf-8
location: https://github.com/YodaSpow/codex-config-manager/raw/refs/heads/main/upload-ready/skills/chat-handoff.zip

HTTP/2 302
content-type: text/html; charset=utf-8
location: https://raw.githubusercontent.com/YodaSpow/codex-config-manager/refs/heads/main/upload-ready/skills/chat-handoff.zip

HTTP/2 200
content-type: application/zip
```

This proves the server transport, not the rendered-README click path.

### Live in-GitHub failure

The operator clicked the skill download from inside the rendered GitHub README. The browser remained at:

```text
https://github.com/YodaSpow/codex-config-manager/blob/main/upload-ready/skills/chat-handoff.zip?raw=1
```

GitHub displayed:

```text
Error loading page
An unexpected error occurred. Try reloading the page.
```

The strongest evidence-backed inference is that GitHub's client-side repository navigation intercepts the same-origin `/blob/` link and fails when the navigation resolves toward binary content. The exact internal GitHub implementation is not relied upon as contract; the observed failure is sufficient to reject this route.

### GitHub's canonical file download surface

The live GitHub Contents API reports separate HTML and download identities for the same artifact:

```text
html_url: https://github.com/YodaSpow/codex-config-manager/blob/main/upload-ready/skills/chat-handoff.zip
download_url: https://raw.githubusercontent.com/YodaSpow/codex-config-manager/main/upload-ready/skills/chat-handoff.zip
size: 2641
```

GitHub documents relative README links as repository navigation and exposes `raw.githubusercontent.com` as a file's `download_url` through its Contents API:

- <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes>
- <https://docs.github.com/en/rest/repos/contents>

### Rejected final contract

The following must not remain the generated ZIP-link form:

```markdown
[Download chat-handoff](upload-ready/skills/chat-handoff.zip?raw=1)
```

The failure does not invalidate the ZIP artifact, `upload-ready/`, the bounded README generator, or the ordinary Markdown view link. It invalidates only the same-origin query-based direct-download route and the earlier completion claim based solely on redirect headers.

## Locked corrective decision

Every README ZIP target must become an absolute GitHub raw-file URL derived from validated Git identity and the configured branch.

For the current repository the generated shapes are:

```text
https://raw.githubusercontent.com/YodaSpow/codex-config-manager/main/upload-ready/global-agents.zip
https://raw.githubusercontent.com/YodaSpow/codex-config-manager/main/upload-ready/skills/<encoded-skill-name>.zip
```

The global Markdown view lane remains:

```text
latest/AGENTS.md
```

The semantic separation is:

| README action | Target class | Required behavior |
| --- | --- | --- |
| View global `AGENTS.md` | Ordinary repository-relative Markdown path | Open GitHub's rendered file page |
| Download global ZIP | Derived absolute GitHub raw URL | Return the current `application/zip` payload |
| Download a skill ZIP | Derived absolute GitHub raw URL | Return that current skill's `application/zip` payload |

No GitHub Release, tag, GitHub Pages site, API call during README rendering, ZIP duplication, or second download index is introduced.

## Repository identity derivation contract

### Authority inputs

The URL builder must consume only:

1. the remote URL returned by the existing validated repository-status path;
2. `config.git.url` as the expected identity when configured;
3. `config.git.branch` as the selected publication branch;
4. the already validated relative artifact path.

It must not derive public identity from README content, the live GitHub page, ZIP contents, a hard-coded project owner/repository pair, browser state, or an unvalidated environment variable.

### Supported GitHub transport identities

The implementation must explicitly support and test the canonical forms relevant to this project:

```text
git@github.com:<owner>/<repository>.git
ssh://git@github.com/<owner>/<repository>.git
https://github.com/<owner>/<repository>.git
https://github.com/<owner>/<repository>
```

Normalization may remove the one terminal `.git` suffix. It must not silently rewrite additional path segments or guess at malformed identities.

### Rejection rules

Fail before README or artifact mutation when the selected identity cannot be converted unambiguously and safely. Reject at least:

- non-GitHub hosts;
- missing owner or repository components;
- extra path components;
- `.` or `..` path components;
- empty or whitespace-bearing identity components;
- URL queries or fragments;
- embedded HTTPS credentials, tokens or passwords;
- unexpected SSH users or ports unless separately proven and deliberately supported;
- control characters or encoded forms that could change URL structure;
- a configured branch that cannot be represented safely in the raw URL path.

The public URL must never expose credentials or reuse the Git transport syntax directly.

### Generated raw base

After strict normalization, the derived base is conceptually:

```text
https://raw.githubusercontent.com/<owner>/<repository>/<configured-branch>/
```

`raw.githubusercontent.com` is intentionally fixed as GitHub's raw-content host. The project-specific owner, repository and branch are derived values. Dynamic artifact paths are appended only after their existing validation and deterministic percent-encoding.

## Corrected bounded README contract

The generator must produce the equivalent of:

```markdown
## Global AGENTS.md

The global `AGENTS.md` contains guidance intended for the user’s global Codex environment.

- [View the current global - AGENTS.md](latest/AGENTS.md)
- [Download the current global - AGENTS.md](https://raw.githubusercontent.com/<derived-owner>/<derived-repository>/<configured-branch>/upload-ready/global-agents.zip)

## Skills

Each download contains one complete user-managed skill.

- [Download <skill-name>](https://raw.githubusercontent.com/<derived-owner>/<derived-repository>/<configured-branch>/upload-ready/skills/<encoded-skill-name>.zip)
```

The generator must continue to:

- own only the content between the existing README markers;
- discover skills dynamically from validated canonical state;
- sort skill membership deterministically;
- add and remove exactly one link with each skill addition or deletion;
- preserve human-authored content outside its markers;
- produce identical bytes for identical inputs;
- omit the global view and ZIP entries together when canonical `AGENTS.md` is absent.

The application must not hard-code the three currently published skill names.

## Mode C execution goal

### Phase 1 — Mode A preflight

Before mutation:

1. confirm the index is clean and the worktree contains no pre-existing change other than this authorised Mode B Doc 13 addition; if Doc 13 has already been committed separately, require a fully clean worktree;
2. confirm local `main`, `origin/main`, configured branch and validated remote identity;
3. identify every current code, test, README and current-document reference to `?raw=1`;
4. confirm the existing ordinary `latest/AGENTS.md` preview route;
5. confirm historical documents and excluded content are outside the mutation set;
6. preserve the failure evidence in this document as the corrective baseline.

### Phase 2 — URL resolver and propagation

Implement one strict GitHub raw-base resolver at the narrowest reusable layer. Pass its derived result into bounded README rendering through explicit data flow. Do not make the artifact renderer discover Git state implicitly or invoke GitHub over the network.

Remove `?raw=1` from:

- the global ZIP link;
- every dynamic skill ZIP link;
- tests that encode the rejected contract;
- the current root README output;
- current Docs 7, 8 and 10 descriptions and examples.

Do not change the view link, ZIP builder, ZIP validator, artifact membership, canonical `latest/`, managed-state fingerprints, semantic change detection, commit summaries, consumer behavior or launchd operation.

### Phase 3 — automated tests

Add or update focused tests proving:

1. canonical GitHub SCP-style SSH parsing;
2. canonical `ssh://` GitHub parsing;
3. canonical GitHub HTTPS parsing with and without terminal `.git`;
4. rejection of malformed, unsupported, credential-bearing, query-bearing, fragment-bearing, traversal-bearing and structurally ambiguous identities;
5. different test owner/repository/branch inputs produce correspondingly different URLs, proving project identity is not embedded as a constant;
6. the global ZIP target is absolute and uses the derived raw base;
7. every dynamic skill ZIP target uses the same derived raw base;
8. no generated ZIP link contains `/blob/` or `?raw=1`;
9. unusual valid skill names retain deterministic URL encoding;
10. `latest/AGENTS.md` remains ordinary, relative and unchanged;
11. reconciliation remains bounded, idempotent, deterministic and deletion-aware;
12. affected publisher orchestration supplies validated identity explicitly and retains its existing safe no-op and mutation behavior.

Run the focused URL, artifact/README and publisher tests before the complete suite.

### Phase 4 — Mode B reconciliation

Surgically update current Docs 7, 8 and 10 during the corrective implementation:

- **Doc 7:** mark `?raw=1` rejected by live in-GitHub evidence; establish derived absolute raw URLs as the current distribution contract; keep the ordinary preview lane distinct.
- **Doc 8:** replace the global ZIP example and state that all dynamic skill ZIPs use the same derived raw base; leave the `latest/AGENTS.md` route unchanged.
- **Doc 10:** describe the implemented resolver, validated identity input and live behavior; remove the superseded query-based claim.

Do not modify bootstrap documents, `docs/history/`, unrelated plans, or create another numbered document for the same correction.

After implementation and proof, update this Doc 13 status from planned to implemented and record the commit and decisive validation evidence without turning it into a chronological execution transcript.

### Phase 5 — local validation and scope audit

Required local proof:

```text
focused URL resolver tests
focused artifact/README tests
affected publisher integration tests
complete repository test suite
Python compilation or established equivalent
README generator-equivalence check
git diff --check
```

The final diff audit must prove:

- only intended application code, tests, root README, Docs 7, 8, 10 and this Doc 13 changed;
- no ZIP bytes or artifact membership changed;
- no local/private configuration changed;
- no launchd, consumer, settlement, managed-state, Git safety or unrelated behavior changed;
- no historical document changed;
- `.DS_Store` and `skills/.system/**` remain excluded, untracked and unmodified.

### Phase 6 — Git publication

Stage only the audited paths, validate the staged result, create one bounded corrective commit and push normally to `origin/main` over the established SSH path.

Do not force-push, rewrite history, create a tag, create a Release, or use an unrestricted Git add.

### Phase 7 — live acceptance

HTTP proof must confirm for the global ZIP and every currently generated skill ZIP:

- the README target is an absolute `https://raw.githubusercontent.com/...` URL;
- no target first enters GitHub's `/blob/` route;
- the final response is HTTP 200;
- `Content-Type` is `application/zip`;
- remote `main` resolves to the published corrective commit.

The ordinary global guidance link must still open GitHub's rendered Markdown file page.

Interactive proof is a blocking acceptance gate:

1. open the live repository root README on GitHub;
2. click the global ZIP link from inside that rendered README;
3. click at least one skill ZIP link from inside that rendered README;
4. confirm both initiate ZIP downloads without opening a blob page or GitHub error state;
5. click the global `AGENTS.md` view link and confirm the rendered Markdown preview remains intact.

Use a controllable browser when available. If no browser session is available, command-line headers do not substitute for this gate. Stop short of goal completion and request the operator's live click results.

## Completion matrix

| Requirement | Required evidence |
| --- | --- |
| Rejected approach removed | No current generated ZIP target contains `?raw=1` or `/blob/` |
| Identity is derived | Resolver tests vary owner, repository and branch inputs |
| Input is authoritative | Resolver receives validated remote identity and configured branch through explicit flow |
| Global download | Live README target is absolute raw URL and downloads `global-agents.zip` |
| Dynamic skill downloads | Every current skill has one matching absolute raw ZIP target |
| View lane preserved | `latest/AGENTS.md` still opens GitHub's rendered Markdown page |
| Reconciliation preserved | Bounded, deterministic, idempotent and deletion tests pass |
| Documentation aligned | Docs 7, 8, 10 and 13 agree on implemented behavior |
| Publication safe | Audited commit pushed normally; local and remote SHA match |
| Real interaction proven | Live GitHub README clicks download global and skill ZIPs without an error page |
| Exclusions preserved | `.system/**` and `.DS_Store` remain outside all managed and changed state |

The goal is complete only when every row is proven. HTTP transport evidence without the live README interaction is incomplete.

## Implementation evidence — 25 August 2026

The local corrective implementation now:

- strictly parses canonical GitHub SCP-style SSH, `ssh://` and HTTPS remote forms;
- derives owner and repository from the remote identity already returned by Git validation and uses the configured branch;
- rejects unsupported hosts, credentials, ports, queries, fragments, traversal, control characters and ambiguous components before projection mutation;
- passes the derived raw base explicitly into bounded README reconciliation;
- preserves the ordinary relative `latest/AGENTS.md` preview link;
- generates absolute raw URLs for the global ZIP and every dynamically discovered skill ZIP;
- leaves all current ZIP bytes unchanged.

Decisive local validation:

```text
focused corrective tests: 31 passed
complete repository suite: 97 passed
Python compilation: passed
README generator equivalence: true
git diff --check: passed
ZIP bytes versus HEAD: identical for all four current artifacts
```

The corrective commit identifier and live GitHub acceptance evidence will be recorded here only after normal publication and successful interaction through the rendered root README.

## Explicit authority boundary

When separately started as a goal, this document authorises only the repository code, tests, bounded README, current Docs 7, 8, 10 and this Doc 13 changes required for the correction, followed by targeted validation, a normal bounded commit and push, and live read-only GitHub validation.

It does not authorise:

- modifying or deleting `~/.codex/skills/.system/**` or `.DS_Store`;
- editing global `/Users/spowart/.codex/AGENTS.md`;
- changing local/private configuration values;
- changing ZIP contents or rebuilding unrelated managed state solely for this correction;
- changing launchd installation or runtime settings;
- activating or modifying the Mac mini consumer;
- creating Releases, tags, GitHub Pages or new distribution machinery;
- force-pushing or rewriting Git history;
- changing the Mac Studio authority direction or managed-scope contract.

## Mode B creation validation — 25 August 2026

At creation:

- Doc 6 already existed and was preserved; this new document correctly took the next global number, Doc 13;
- the worktree was clean before the Doc 13 addition;
- local `main`, `origin/main` and HEAD matched at `1f41f3d5424db84565be2ee0d2961072d502888f`;
- the established remote was `git@github.com:YodaSpow/codex-config-manager.git`;
- the failed live README behavior, working redirect chain and GitHub API `download_url` were reconciled into one corrective goal package;
- no application code, test, README, existing document, configuration, ZIP artifact, launchd state, Codex-managed state, commit or remote state was changed by this Mode B creation.
