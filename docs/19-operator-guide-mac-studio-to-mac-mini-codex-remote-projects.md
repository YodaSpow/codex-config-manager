# Doc 19 — Operator Guide — Mac Studio-to-Mac mini Codex Remote Projects

**Status:** Discovered and documented; SSH remote-project route not yet commissioned
**Machine authority:** Mac Studio-owned operator guide
**Repository workflow:** Root [`AGENTS.md`](../AGENTS.md) and [Doc 16 — Repository Operations — Agent Workflow and Publication Guardrails](16-repository-agent-workflow-and-publication-guardrails.md)
**Cross-machine baseline:** [Doc 17 — Mac mini Report — Phase 15 validation](17-mac-mini-report-phase-15-validation.md)
**Official product reference:** [OpenAI remote connections documentation](https://developers.openai.com/es-419/docs/remote-connections)
**Captured:** 20 September 2026

## Current state

- ✅ The Mac Studio and Mac mini already have a proven GitHub-backed global
  guidance and user-skill synchronization path.
- ✅ The Mac mini has a working local Codex installation and has independently
  used its registered NICLAB MCP connection.
- ✅ The operator has identified the Codex SSH remote-project surface as a
  useful way to work from the Mac Studio against repositories that physically
  remain on the Mac mini.
- ▶ This guide defines the smallest safe commissioning and acceptance path.
- ⛔ The Studio-to-Mini SSH host alias, remote-project connection and remote
  task execution have not yet been proven.
- ⛔ The Mac mini login shell must not be treated as ready until the `codex`
  command is shown to be available there. An earlier ordinary Terminal check
  did not find that command on `PATH`, even though the installed application
  supplied a usable bundled CLI through a separately discovered path.

## Purpose

Use the Mac Studio Codex app as the control surface while Codex works directly
inside a project stored on the Mac mini. The remote task uses the Mac mini's
filesystem and shell; it does not copy the project into a Studio checkout.

This is useful when:

- a repository or its machine-specific runtime belongs on the Mac mini;
- the operator wants one Studio-facing Codex workspace without relocating that
  repository;
- a Mini-hosted task needs the Mini's dependencies, paths or local runtime; or
- the synchronized global guidance and skills should govern work performed on
  either machine while each repository stays on its owning host.

This guide does not make the Mac mini a second NICLAB host, move services from
the Studio, replace the existing configuration synchronization system, or
grant one repository authority over another.

### Concrete operator use case

The operator has a media-automation repository that belongs on the Mac mini
because it maintains a service running there. Today, maintenance requires
opening and operating Codex on the Mini. With a commissioned SSH remote
project, the operator can select that Mini repository from the Studio Codex
app, review and approve the work from the Studio, and still execute against the
real Mini files, dependencies and service environment.

This improves the control surface without moving the repository or pretending
the service runs on the Studio.

## Architecture in plain language

```text
Codex app on Mac Studio
        ↓ authenticated SSH
Mac mini login shell starts Codex App Server
        ↓
Codex reads, runs and writes in the selected Mac mini project folder
```

The Studio provides the visible control surface. The Mini remains the execution
host and owns the remote project's files, shell, dependencies and machine-local
configuration.

This SSH project route is distinct from remotely controlling a complete
ChatGPT desktop host. OpenAI documents both capabilities under remote
connections; this guide concerns selecting a project folder on an SSH host.

## Security and authority boundary

- Use the existing trusted private network and normal SSH security posture.
- Use a trusted machine-specific SSH key and a least-privilege account.
- Do not expose an unauthenticated SSH or Codex listener publicly.
- Do not copy private keys between machines or record their contents here.
- A remote project has the same write consequences as working locally on the
  Mini. Repository instructions, task authority and approval gates still apply.
- The remote connection does not merge the two filesystems, repositories or
  machine roles.
- A remote Mini task does not automatically see Studio-local files or sibling
  Studio repositories. It may use only separately authorised network services,
  mounts or other explicit contracts available from its Mini execution
  environment.
- Synced global guidance and skills are useful prerequisites, not proof that a
  particular remote task discovered or applied them.

## Readiness prerequisites

All of the following must be true before the route is classified **proven
ready**:

1. The Studio has an explicit, resolvable SSH host alias for the Mac mini in
   `~/.ssh/config`. OpenAI documents that explicit aliases are discovered;
   pattern-only entries are ignored.
2. Ordinary SSH from the Studio to that alias succeeds using the intended
   account and trusted key.
3. Codex is installed and authenticated on the Mac mini.
4. The Mac mini's SSH login shell can resolve `codex` on `PATH` without relying
   on an interactive Finder launch or a chat-specific temporary command.
5. The intended project folder exists on the Mac mini and its repository rules
   permit the requested work.
6. The Codex app exposes **Settings → Connections → SSH** for the current
   account and rollout.

The current readiness state is **discovered but unproven**. Items 1, 2, 4 and
the complete remote-project acceptance sequence still require evidence.

## Commissioning sequence

### 1. Establish the explicit Studio-side SSH alias

Use a dedicated explicit host block in the Mac Studio's `~/.ssh/config`.
Resolve the real host address, account and key through the operator's existing
SSH setup; do not guess them from this document.

Example shape only:

```sshconfig
Host mac-mini-codex
  HostName REPLACE_WITH_TRUSTED_LAN_ADDRESS
  User REPLACE_WITH_REMOTE_ACCOUNT
  IdentityFile ~/.ssh/REPLACE_WITH_MACHINE_KEY
```

The alias is an operator convenience, not machine-role authority.

### 2. Prove ordinary SSH before involving Codex

From the Mac Studio, use the resolved alias:

```bash
ssh mac-mini-codex '/usr/bin/true' \
&& echo "✅ Mac mini SSH connection succeeded"
```

An authentication, host-key or network failure stops commissioning. Do not
weaken SSH security or publish another listener merely to continue.

### 3. Prove Codex is available to the Mini login shell

From the Mac Studio:

```bash
ssh mac-mini-codex 'command -v codex && codex --version' \
&& echo "✅ Mac mini login shell can launch Codex"
```

If this fails while the desktop application still works, classify the route
**fixtures incomplete**. Reconcile the supported Codex installation path with
the Mini login shell before adding the host in the app. Do not create an
undocumented wrapper or hard-coded application path merely to bypass the gate.

### 4. Add the SSH host in Codex

On the Mac Studio:

1. Open **Settings → Connections**.
2. Open the **SSH** connection area.
3. Add or enable the explicit Mac mini host alias.
4. Select the intended project folder on the Mac mini.
5. Start with a fresh read-only acceptance task.

The app starts the remote Codex App Server through the Mini's SSH login shell.
The selected folder stays on the Mini.

## Baseline acceptance task

Use a non-sensitive repository whose clean state is already known. Submit this
as the first remote task:

```text
Operate in Mode A only. Prove that this task is executing in the selected
remote project on the Mac mini. Report the resolved project root, current Git
branch and concise Git status. Read the applicable repository instructions and
report their title. Do not edit files, install anything, start services, stage,
commit or push.
```

Acceptance requires:

- the resolved root is the selected Mini project, not a Studio path;
- Git evidence comes from that Mini checkout;
- the applicable repository instructions are discovered;
- no file, index, runtime or remote state changes; and
- the task completes without falling back to a copied local checkout.

This proves the remote-project foundation only. It does not prove every skill,
MCP server, credential, browser capability or project-specific runtime.

## Optional environment acceptance

After baseline acceptance, test only the remote capabilities a real Mini task
will depend on. For the current shared setup, a useful read-only follow-up is:

1. confirm the synchronized global guidance version visible to the remote task;
2. confirm a known synchronized user skill is discoverable; and
3. invoke one harmless NICLAB read-only allocation query through the Mini's
   durable MCP registration.

Record each result separately. A successful SSH project task must not be used
to infer that every remote integration is present.

## Failure classification

| Evidence | State | Meaning |
| --- | --- | --- |
| SSH alias or authentication unresolved | Assessment incomplete | The Studio cannot yet establish the remote host contract |
| SSH works but Mini login shell cannot resolve Codex | Fixtures incomplete | The desktop install exists, but the documented SSH launch route is not ready |
| Codex connection opens but selected project evidence is wrong | Unavailable or disproven | Stop; the task is not operating in the intended Mini project |
| Baseline task passes without mutation | Proven ready | Remote project access is safe to use for suitably authorised work |
| Optional skill or MCP check fails | Dependency-scoped incomplete | Remote project access may still be ready; only that dependent capability remains unresolved |

## Operator outcome

Once the baseline passes, the operator can open Mini-owned projects from the
Studio and work against their real host environment without relocating them.
The Mini remains a separate execution boundary, and normal repository,
approval and machine-role rules continue to apply.

Until that proof exists, this document is a commissioning guide rather than a
claim that remote projects are operational.
