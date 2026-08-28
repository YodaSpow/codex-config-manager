# Doc 15 — Operator Runbook — Mac mini Phase 15 Activation

**Status:** Ready for operator use; Mac mini activation remains unexecuted and unproven
**Authority:** Human-readable activation sequence; not independent authority to alter either machine
**Governing handoff:** [Doc 12 — Mac mini Phase 15 Handoff](12-mac-mini-phase-15-handoff.md)
**SSH contract:** [Doc 14 — GitHub SSH Machine Bootstrap](14-operator-guide-github-ssh-machine-bootstrap.md)
**Canonical operations:** [Doc 10 — Implementation Architecture and Operations](10-implementation-architecture-and-operations.md)
**Mac Studio evidence:** [Doc 11 — Mac Studio Validation Evidence](11-validation-evidence-mac-studio.md)

## Current activation state

- ✅ The Mac Studio publisher and reusable consumer implementation are complete and published.
- ✅ GitHub `origin/main` contains the canonical implementation and current `latest/` snapshot.
- ▶ The operator has reported an empty Mac mini directory intended to become `/Users/spowart/Scripts/codex-config-manager`; this must still be inspected on that machine.
- ⛔ Mac mini SSH, repository access, local environment, consumer deployment and launchd operation remain unproven until this runbook and Doc 12 are executed on the real Mac mini.

Creating or reading this document does not configure the Mac mini. Do not report the two-machine system operational until the Phase 15 evidence required by Doc 12 has been captured and published.

## Purpose

This is the linear operator journey from the already working Mac Studio publisher to a validated Mac mini consumer. It joins the existing documents without replacing them:

```text
Doc 14 = establish and prove machine-local GitHub SSH
Doc 12 = govern the complete Mac mini Phase 15 goal
Doc 15 = tell the operator exactly when, where and how to activate that goal
```

The intended journey is:

```text
Mac Studio freshness gate
        ↓
Mac mini SSH identity and GitHub registration
        ↓
exact-repository access proof
        ↓
clone established origin/main into the Mac mini checkout
        ↓
open that checkout as the local Codex project
        ↓
execute the persistent Doc 12 Phase 15 goal
        ↓
publish public Mac mini evidence and permitted refinements
        ↓
confirm Mac Studio safely fast-forwards the shared history
```

## Human and AI responsibility boundary

The operator remains responsible for:

- choosing the correct GitHub account and email/comment value for a new key;
- entering and retaining any SSH key passphrase privately;
- checking GitHub's published host fingerprint at first contact;
- adding only the public key through the GitHub account UI;
- confirming that SSH names the intended GitHub account;
- selecting the real Mac mini local repository project in Codex;
- approving or rejecting any architectural decision that falls outside Doc 12;
- confirming final human-visible operation.

The local Codex agent may, when explicitly authorised by the operator:

- perform read-only discovery and report existing SSH, path, repository and launchd state;
- create the Mac mini's own SSH key without displaying its private contents;
- merge the selected GitHub host block into an existing SSH config without overwriting unrelated entries;
- run the documented SSH and repository tests;
- clone the canonical repository into a proven-safe destination;
- execute the complete bounded Phase 15 goal from the cloned repository;
- pause at human interaction or architecture gates;
- publish only the public validation evidence and permitted consumer refinements authorised by Doc 12.

Neither the operator nor an AI should manually copy the Mac Studio private SSH key, Mac Studio `config/config.yaml`, runtime receipts, logs or installed LaunchAgent into the Mac mini.

## Stage 1 — Run the final Mac Studio freshness gate

Run this immediately before moving the work to the Mac mini. In the Codex project rooted at the Mac Studio checkout, submit:

```text
Run the read-only pre-handoff freshness reconciliation required by Doc 12.

Confirm that the checkout is clean on main, local HEAD and origin/main agree,
latest/ is current, Docs 10, 12, 14 and 15 match repository and runtime reality,
every remaining activation task genuinely requires the real Mac mini, and no
private or Mac Studio-specific material is entering the handoff.

Do not change anything. Report whether Mac mini Phase 15 is ready to begin and
cite the evidence for every gate.
```

Do not proceed when this check finds a dirty checkout, local/remote disagreement, invalid `latest/`, private material or material documentation drift. Reconcile the finding on the Mac Studio before asking the Mac mini to consume it.

## Stage 2 — Open this runbook on the Mac mini

Before the repository exists locally, this committed document can be read from GitHub:

```text
https://github.com/YodaSpow/codex-config-manager/blob/main/docs/15-operator-runbook-mac-mini-phase-15-activation.md
```

After cloning, use the repository-owned local copy:

```text
/Users/spowart/Scripts/codex-config-manager/docs/15-operator-runbook-mac-mini-phase-15-activation.md
```

Do not manually copy this document into the reported empty repository directory. That would make the destination non-empty and create a detached handoff copy. Cloning `origin/main` brings Docs 10, 12, 14 and 15 onto the Mac mini together in one canonical history.

## Stage 3 — Inspect the intended Mac mini destination

Open Terminal on the Mac mini and inspect the reported directory without changing it:

```bash
cd "/Users/spowart/Scripts" \
&& /usr/bin/printf 'Intended repository directory:\n' \
&& /bin/ls -la "/Users/spowart/Scripts/codex-config-manager" \
&& echo "✅ Command ran successfully"
```

The destination must be an ordinary empty directory and must remain separate from `~/.codex`. Do not run `git init`, create a local README or add another initial commit. If the path is missing, non-empty, already a Git checkout or contains anything unexpected—including Finder metadata—stop and let the Mac mini discovery determine a safe resolution. Do not automatically delete or overwrite its contents.

## Stage 4 — Establish the Mac mini SSH identity

Doc 14 is authoritative if any wording here and the SSH guide differ. The following is the Mac mini-specific route through that guide.

### 4.1 Inspect existing SSH state

```bash
if [ -d "$HOME/.ssh" ]; then /bin/ls -la "$HOME/.ssh"; else /usr/bin/printf 'No existing ~/.ssh directory\n'; fi \
&& echo "✅ Command ran successfully"
```

Finding an existing key does not prove that it belongs to the intended GitHub account or is safe to reuse. Do not inspect, replace or delete private-key contents merely to continue.

### 4.2 Create a dedicated key when required

`YOUR_GITHUB_EMAIL` is a placeholder, not a stored project value. Replace it with the operator-selected GitHub account email or GitHub-provided no-reply address. The proposed key filename is also an operator aid, not machine identity authority.

```bash
/bin/mkdir -p "$HOME/.ssh" \
&& /bin/chmod 700 "$HOME/.ssh" \
&& test ! -e "$HOME/.ssh/id_ed25519_github_mac_mini" \
&& test ! -e "$HOME/.ssh/id_ed25519_github_mac_mini.pub" \
&& /usr/bin/ssh-keygen -t ed25519 -C "YOUR_GITHUB_EMAIL" -f "$HOME/.ssh/id_ed25519_github_mac_mini" \
&& echo "✅ Command ran successfully"
```

The private key is:

```text
~/.ssh/id_ed25519_github_mac_mini
```

The only file that may be registered with GitHub is:

```text
~/.ssh/id_ed25519_github_mac_mini.pub
```

Never copy, paste, publish or commit the private key or its passphrase.

### 4.3 Add the selected key to the Mac mini keychain

For a passphrase-protected key:

```bash
/usr/bin/ssh-add --apple-use-keychain "$HOME/.ssh/id_ed25519_github_mac_mini" \
&& echo "✅ Command ran successfully"
```

Merge—not overwrite—the following block into `~/.ssh/config` when this is the selected GitHub identity:

```sshconfig
Host github.com
  AddKeysToAgent yes
  UseKeychain yes
  IdentityFile ~/.ssh/id_ed25519_github_mac_mini
```

If the file already contains a `github.com` block or multiple GitHub identities, stop and reconcile the selection deliberately. Do not append a conflicting block blindly.

### 4.4 Register only the public key

Copy the public key to the clipboard:

```bash
/usr/bin/pbcopy < "$HOME/.ssh/id_ed25519_github_mac_mini.pub" \
&& echo "✅ Public key copied"
```

Then the operator must:

1. sign in to the intended GitHub account;
2. open **Settings → SSH and GPG keys**;
3. select **New SSH key**;
4. choose **Authentication Key**;
5. use a descriptive title such as `Mac mini — Codex Config Manager`;
6. paste the copied public key and save it.

No repository document or evidence record should contain the full public-key value.

### 4.5 Prove the GitHub account

At first contact, compare the displayed host fingerprint with GitHub's current published fingerprint before accepting it:

```text
ssh -T git@github.com
```

A successful response names the authenticated GitHub account and says that GitHub does not provide shell access. GitHub documents exit status `1` as expected for this test, so do not add a generic success echo. The named account must be the intended account.

### 4.6 Prove non-interactive access to the exact repository

```bash
GIT_SSH_COMMAND='/usr/bin/ssh -o BatchMode=yes' \
/usr/bin/git ls-remote "git@github.com:YodaSpow/codex-config-manager.git" HEAD \
&& echo "✅ Repository SSH access verified"
```

This must return the repository's `HEAD` SHA without requesting a password or passphrase. It proves the user-domain prerequisite only; Doc 12 still requires later proof from the installed launchd context.

## Optional AI-assisted pre-clone bootstrap

The SSH and clone stages can be assisted by a local Codex session on the Mac mini, but they still contain human interaction. Open a local Codex project with `/Users/spowart/Scripts` as its bounded working area and submit:

```text
Assist me with the pre-goal Mac mini bootstrap for Codex Config Manager.

Use the public Doc 15 runbook at:
https://github.com/YodaSpow/codex-config-manager/blob/main/docs/15-operator-runbook-mac-mini-phase-15-activation.md

Treat its cited Doc 14 SSH contract as authoritative. Start read-only: inspect the
reported /Users/spowart/Scripts/codex-config-manager destination, existing SSH
filenames without reading private-key contents, current Git/OpenSSH availability,
and whether the intended destination is genuinely safe for cloning.

Help establish a dedicated Mac mini GitHub SSH identity only after resolving the
operator-selected GitHub email/comment value and any existing github.com SSH config.
Never expose or copy private-key contents. Pause while I register the public key
and confirm GitHub's host fingerprint and authenticated account.

Then prove BatchMode=yes access to
git@github.com:YodaSpow/codex-config-manager.git and clone origin/main into the
intended repository path only if that destination is proven empty and safe.
Do not run git init, create independent history, force, delete unexpected files,
modify ~/.codex, build the project environment or begin Phase 15. Finish by showing
the clone's remote, branch, upstream, HEAD and clean status.
```

This prompt authorises only the bounded pre-clone setup it describes. It is not the Phase 15 implementation goal.

## Stage 5 — Clone the established repository history

Only after the SSH account and exact-repository gates pass, clone `origin/main`. For the reported existing empty directory:

```bash
cd "/Users/spowart/Scripts" \
&& test -d "/Users/spowart/Scripts/codex-config-manager" \
&& test -z "$(/bin/ls -A "/Users/spowart/Scripts/codex-config-manager")" \
&& /usr/bin/git clone \
  "git@github.com:YodaSpow/codex-config-manager.git" \
  "/Users/spowart/Scripts/codex-config-manager" \
&& echo "✅ Repository cloned successfully"
```

The emptiness check deliberately stops the chain if the directory contains anything. Do not bypass it with deletion, force or a separate `git init` history.

Inspect the resulting checkout:

```bash
cd "/Users/spowart/Scripts/codex-config-manager" \
&& /usr/bin/git remote get-url origin \
&& /usr/bin/git branch --show-current \
&& /usr/bin/git status --short --branch \
&& echo "✅ Checkout identity inspected successfully"
```

The required result is the exact SSH remote, `main`, an `origin/main` tracking relationship and a clean checkout. A missing upstream, unexpected remote, dirty state, ahead state or divergence is a stop condition.

## Stage 6 — Open the cloned repository in local Codex

Use the Mac mini's local Codex project surface that can access its filesystem and Terminal. An ordinary web-only ChatGPT conversation cannot build the repository-owned environment, validate the real `~/.codex` boundary or install launchd integration.

Open this exact folder as the project:

```text
/Users/spowart/Scripts/codex-config-manager
```

Before starting the goal, confirm the agent can read the local copies of:

```text
docs/10-implementation-architecture-and-operations.md
docs/12-mac-mini-phase-15-handoff.md
docs/14-operator-guide-github-ssh-machine-bootstrap.md
docs/15-operator-runbook-mac-mini-phase-15-activation.md
```

Do not manually install Mac Studio copies of `AGENTS.md` or user skills as a substitute for Phase 15. The controlled consumer deployment is responsible for reconciling the bounded managed state and proving exclusions.

## Stage 7 — Start the persistent Phase 15 goal

Submit the following in the Codex chat rooted at the cloned Mac mini repository:

```text
/goal

Execute the complete real Mac mini Phase 15 rollout governed by
docs/12-mac-mini-phase-15-handoff.md.

This goal is running on the real Mac mini from its own local clone of
codex-config-manager. Treat Doc 12 as the governing handoff, Doc 10 as the
canonical implementation and operating contract, Doc 14 as the completed SSH
prerequisite, and Doc 15 as the operator activation sequence.

Begin with the bounded read-only Mac mini discovery required by Doc 12. Confirm
the derived MacMini identity, repository and ~/.codex separation, existing
managed and excluded surfaces, compatible Python, Git state, SSH evidence and
existing launchd state before mutation.

Then pursue the complete Phase 15 outcome: construct and validate the
repository-owned development environment and rsync runtime; create truthful
ignored consumer configuration; run the full relevant test suite; validate
latest/; perform the controlled foreground consumer deployment; prove a second
run is a no-op; prove skills/.system/**, .DS_Store and unrelated ~/.codex
content remain unchanged; install and validate only the consumer LaunchAgent;
prove launchd-domain SSH and headless consumer operation; exercise the safe
uninstall/reinstall contract; and create and publish the permitted public Mac
mini validation receipt and any necessary bounded consumer-specific corrections.

The Mac Studio remains the authoring authority. GitHub origin/main remains the
shared published history. The Mac mini is consumer-only and must never run the
publisher, create automatic commits, force-push, rewrite history or redefine
managed scope, deletion rules, latest/, exclusions, repository topology or
public configuration architecture.

Keep the goal active through discovery, construction, testing, foreground
deployment, launchd validation, evidence capture and permitted publication.
Stop for human direction if a Doc 12 stop condition occurs or if completion
would require an architectural change.
```

The `/goal` prompt is the explicit authority for the Mac mini implementation work. Merely opening this document or the repository does not authorise Phase 15.

## Stage 8 — What the Phase 15 agent owns

Within the goal, the Mac mini agent should:

1. derive and prove the expected `MacMini` identity;
2. prove the repository and `~/.codex` are distinct safe roots;
3. inspect managed and excluded surfaces without traversing `.system` as input;
4. discover a compatible external Python in the declared `>=3.12,<3.15` range;
5. build and validate the repository-owned development `.venv` from hashed locks;
6. build and validate `.tools/rsync` from the tracked source contract;
7. create ignored truthful `config/config.yaml` with `role: "consumer"`, `machine.id: MacMini`, absolute Mac mini paths and `consumer.check_interval: 5m`;
8. run the complete relevant tests and repository validation;
9. validate the pulled `latest/` snapshot before touching live Codex state;
10. capture bounded before-state evidence without publishing private details;
11. run one foreground consumer deployment;
12. prove only `AGENTS.md` and dynamic user-managed skills changed;
13. prove `.system/**`, `.DS_Store` and unrelated `~/.codex` content remained unchanged;
14. prove a second foreground run is a no-op;
15. install and validate only `com.yodaspow.codex-config-manager.consumer`;
16. prove the publisher service is absent on the Mac mini;
17. prove launchd-domain SSH, headless polling, logs and single-instance behavior;
18. exercise safe uninstall and reinstall without deleting live or repository state;
19. create a public Mode B Mac mini Phase 15 validation receipt;
20. commit and push only permitted public evidence and necessary bounded consumer refinements.

The agent must not assume the Mac Studio's proven Python path, SSH agent, keychain state, absolute support paths or launchd evidence applies to the Mac mini. Those are real-machine discovery and validation inputs.

## Human interaction gates during the goal

The agent may pause for the operator when:

- a passphrase or macOS security interaction requires the human lane;
- a GitHub account, host fingerprint or key-registration fact requires confirmation;
- an existing Mac mini file, SSH block, LaunchAgent or managed target creates ambiguity;
- foreground deployment is ready but its before-state evidence needs human review;
- the final public evidence is ready for review before publication;
- a Doc 12 stop condition or architecture decision is reached.

A pause at one of these gates is expected and does not mean the goal has failed. After the operator supplies the required confirmation, the same goal should continue rather than starting a competing setup path.

## Stage 9 — Phase 15 completion evidence

The goal is not complete merely because files appeared beneath the Mac mini `~/.codex`. The published validation receipt must record, without secrets:

- Mac mini model identifier, macOS version, Python version and architecture;
- repository and pulled publication SHA;
- rsync build receipt summary and permitted linkage;
- full decisive test result;
- truthful consumer configuration shape without private local values;
- foreground deployment and second-run no-op evidence;
- preservation of `.system/**`, `.DS_Store` and unrelated sentinels;
- installed consumer LaunchAgent and absent publisher evidence;
- launchd-domain SSH and headless consumer proof;
- safe uninstall/reinstall outcome;
- any evidence-driven bounded correction;
- the conclusion on complete Mac Studio → GitHub → Mac mini readiness.

The consumer runtime never creates this commit. It is a human-controlled development contribution made by the authorised Phase 15 goal.

## Stage 10 — Return to the Mac Studio and close the loop

After the Mac mini evidence commit reaches `origin/main`, return to the Mac Studio Codex Config Manager project and request a read-only reconciliation:

```text
Verify the completed Mac mini Phase 15 contribution from the Mac Studio.

Confirm that the published validation receipt and any bounded consumer fixes are
present on origin/main, the Mac Studio checkout has safely fast-forwarded or can
fast-forward without conflict, the worktree is clean, the publisher remains the
only active Mac Studio role, and normal managed-state publication is healthy.

Do not force, rewrite history or modify either machine. Report whether the full
Mac Studio → GitHub → Mac mini pipeline can now be declared operational.
```

The Mac Studio publisher may safely fast-forward a clean behind-only checkout under its existing Git contract. Any ahead/diverged or pending-publication conflict is an operator recovery condition, never permission to force-push.

## Stop conditions

Stop the current stage without inventing a workaround when:

- the final Mac Studio freshness gate has not passed;
- the intended Mac mini repository path is non-empty, unsafe or overlaps `~/.codex`;
- the SSH key belongs to an unknown account or would need to be copied from another machine;
- GitHub reports the wrong authenticated account;
- `BatchMode=yes` cannot read the exact repository;
- the clone is dirty, ahead, diverged or tracks the wrong remote/branch;
- the derived machine identity is not `MacMini` or disagrees with configuration;
- `latest/` is invalid or contains excluded/unexpected content;
- exact Python, dependency, rsync or linkage validation fails;
- `.system`, `.DS_Store` or unrelated content cannot be proven preserved;
- launchd would install or run the publisher on the Mac mini;
- evidence would expose credentials, private configuration or identifying diagnostics;
- completion requires changing authority, managed scope, deletion policy, exclusions, `latest/`, publisher behavior, repository topology or public configuration architecture.

Ordinary Mac mini-specific path, command or compatibility corrections may remain inside the persistent goal only when Doc 12 permits them and the established architecture remains intact.

## Successful steady state

When every gate has passed, the operating system is:

```text
Mac Studio ~/.codex
        ↓ validated publisher ingestion
GitHub origin/main + latest/
        ↓ safe Mac mini consumer fast-forward every 5 minutes
Mac mini ~/.codex bounded managed targets
```

The Mac Studio remains the only authoring and publishing authority. The Mac mini automatically receives the validated global `AGENTS.md` and dynamically discovered user-managed skills, while preserving Codex-managed `.system/**`, `.DS_Store` and every unrelated local Codex surface.
