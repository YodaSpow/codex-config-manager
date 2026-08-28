# Doc 14 — Operator Guide — GitHub SSH Machine Bootstrap

**Status:** Ready for human-controlled use; no machine has been configured by this document
**Scope:** Public-safe setup and validation of machine-local GitHub SSH authentication on macOS and Windows
**Project use:** [Doc 12 — Mac mini Phase 15 Handoff](12-mac-mini-phase-15-handoff.md) uses this guide as its pre-goal Git-access prerequisite
**Verified against:** Current official GitHub documentation on 28 August 2026

## Purpose

This guide explains how to give one local machine its own SSH identity for GitHub. It is suitable for preparing a Mac, including the deferred Mac mini, or a permitted Windows PC before cloning a Git repository over SSH.

In plain language:

```text
local private key                    stays on this machine
        ↕ proves identity
matching public key                  is registered with GitHub
        ↓ authorises
Git operations over SSH              clone, fetch and permitted push
```

SSH avoids entering a GitHub username or access token for each Git operation. It does not grant permissions by itself: repository access still follows the GitHub account or repository credential to which the public key is attached.

## Security and authority boundary

- Create a separate machine-local key. Never copy a private key from another Mac or PC.
- Never paste, commit, publish, email or upload the private key. A private key normally has no `.pub` suffix.
- Only the matching `.pub` file is added to GitHub.
- Do not overwrite an existing key merely because a default filename already exists.
- Use a meaningful machine-specific filename and GitHub title so the key can later be identified and revoked.
- A lost, retired or untrusted machine requires removal of its key from GitHub.
- Workplace machines remain subject to organizational policy. Do not bypass network, software-installation or account restrictions.
- This guide does not copy credentials, inspect private-key contents, change repository history or prove that a particular machine has completed setup.

The examples use an SSH authentication key attached to the operator's GitHub account. This is the straightforward choice when the machine may later create an explicitly permitted development commit. A narrowly read-only consumer credential is a separate least-privilege design decision and must not be substituted silently where the governing handoff expects permitted evidence contributions.

## Where SSH material normally lives

| Platform | User SSH directory | Typical private key | Matching public key |
| --- | --- | --- | --- |
| macOS | `~/.ssh/` | `~/.ssh/id_ed25519_github_MACHINE` | `~/.ssh/id_ed25519_github_MACHINE.pub` |
| Windows | `%USERPROFILE%\.ssh\` | `%USERPROFILE%\.ssh\id_ed25519_github_MACHINE` | `%USERPROFILE%\.ssh\id_ed25519_github_MACHINE.pub` |

`MACHINE` is a placeholder. Replace it with a short machine label before running a generation command. For example, a Mac mini could use `id_ed25519_github_mac_mini`. The filename is not an identity authority; it is an operator aid.

## Prerequisites

Before creating a key, establish:

1. the GitHub account that should authorize this machine;
2. the repository and whether the machine needs read-only or permitted write access;
3. that Git and OpenSSH are available;
4. that the operator can open GitHub **Settings → SSH and GPG keys**;
5. that local and organizational policy permits SSH access to GitHub.

For Codex Config Manager, the established transport identity is:

```text
git@github.com:YodaSpow/codex-config-manager.git
```

The Mac Studio already has a separately proven SSH path. That fact does not authenticate the Mac mini or any Windows PC.

## Step 1 — Check before creating anything

GitHub recommends checking for existing keys before generating another one.

On macOS Terminal or Git Bash:

```bash
if [ -d "$HOME/.ssh" ]; then /bin/ls -la "$HOME/.ssh"; else /usr/bin/printf 'No existing ~/.ssh directory\n'; fi \
&& echo "✅ Command ran successfully"
```

On Windows PowerShell:

```powershell
if (Test-Path "$env:USERPROFILE\.ssh") { Get-ChildItem -Force "$env:USERPROFILE\.ssh" } else { Write-Output "No existing .ssh directory" }
if ($?) { Write-Output "✅ Command ran successfully" }
```

Look for matching private/public pairs such as `id_ed25519` and `id_ed25519.pub`. Finding a key does not prove that it belongs to the intended account or should be reused. If ownership or purpose is uncertain, stop and make a deliberate operator decision rather than inspecting or replacing the private key.

## Step 2 — Generate a machine-specific Ed25519 key

Replace `YOUR_GITHUB_EMAIL` and `MACHINE` first. GitHub recommends Ed25519 on current systems and a secure passphrase for additional protection.

On macOS Terminal or Git Bash:

```bash
/bin/mkdir -p "$HOME/.ssh" \
&& /bin/chmod 700 "$HOME/.ssh" \
&& test ! -e "$HOME/.ssh/id_ed25519_github_MACHINE" \
&& test ! -e "$HOME/.ssh/id_ed25519_github_MACHINE.pub" \
&& /usr/bin/ssh-keygen -t ed25519 -C "YOUR_GITHUB_EMAIL" -f "$HOME/.ssh/id_ed25519_github_MACHINE" \
&& echo "✅ Command ran successfully"
```

On Windows PowerShell using system OpenSSH:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.ssh" | Out-Null
$KeyPath = "$env:USERPROFILE\.ssh\id_ed25519_github_MACHINE"
if ((Test-Path $KeyPath) -or (Test-Path "$KeyPath.pub")) { throw "Refusing to overwrite an existing SSH key" }
ssh-keygen -t ed25519 -C "YOUR_GITHUB_EMAIL" -f $KeyPath
if ($?) { Write-Output "✅ Command ran successfully" }
```

The command prompts for a passphrase and confirmation. It must not overwrite an existing file. Legacy systems that cannot generate Ed25519 keys should follow GitHub's current fallback guidance rather than inventing another key type.

## Step 3 — Make the key available to the SSH agent

### macOS

Use Apple's system `ssh-add`, not a Homebrew or MacPorts replacement. For a passphrase-protected key:

```bash
/usr/bin/ssh-add --apple-use-keychain "$HOME/.ssh/id_ed25519_github_MACHINE" \
&& echo "✅ Command ran successfully"
```

Merge—not overwrite—the following host block into `~/.ssh/config`, changing the key filename to match:

```sshconfig
Host github.com
  AddKeysToAgent yes
  UseKeychain yes
  IdentityFile ~/.ssh/id_ed25519_github_MACHINE
```

If the key has no passphrase, GitHub says to omit `UseKeychain` and run ordinary `ssh-add` without `--apple-use-keychain`. A passphrase-free key is easier for unattended use but carries greater risk if its private file is exposed; that trade-off must be deliberate.

### Windows PowerShell

In an elevated PowerShell window, enable and start the Windows OpenSSH agent:

```powershell
Get-Service -Name ssh-agent | Set-Service -StartupType Manual
Start-Service ssh-agent
if ($?) { Write-Output "✅ Command ran successfully" }
```

Then, in a normal non-elevated PowerShell window:

```powershell
ssh-add "$env:USERPROFILE\.ssh\id_ed25519_github_MACHINE"
if ($?) { Write-Output "✅ Command ran successfully" }
```

Git for Windows can use a bundled SSH client that cannot communicate with the Windows system agent. If Git prompts despite a working Windows agent, follow GitHub's documented client-alignment troubleshooting. One documented option is:

```powershell
git config --global core.sshCommand "C:/Windows/System32/OpenSSH/ssh.exe"
if ($?) { Write-Output "✅ Command ran successfully" }
```

That command changes global Git behavior and should be used only when the conflict is present and system OpenSSH is the selected client.

## Step 4 — Add only the public key to GitHub

Copy the `.pub` file—not the private file—to the clipboard.

On macOS:

```bash
/usr/bin/pbcopy < "$HOME/.ssh/id_ed25519_github_MACHINE.pub" \
&& echo "✅ Public key copied"
```

On Windows PowerShell:

```powershell
Get-Content "$env:USERPROFILE\.ssh\id_ed25519_github_MACHINE.pub" | Set-Clipboard
if ($?) { Write-Output "✅ Public key copied" }
```

Then in GitHub:

1. Open **Settings**.
2. Select **SSH and GPG keys**.
3. Select **New SSH key**.
4. Choose **Authentication Key**.
5. Give it a descriptive machine-specific title.
6. Paste the public key and add it.

The public key may identify the machine descriptively, but the document and repository must never record its full value as project configuration or evidence.

## Step 5 — Validate GitHub identity safely

On first contact, SSH may ask whether the GitHub host is trusted. Compare the displayed fingerprint with GitHub's current published fingerprints before accepting it. Do not accept an unexpected fingerprint merely to make the command continue.

Run on macOS Terminal, Windows PowerShell or Git Bash:

```text
ssh -T git@github.com
```

Successful GitHub authentication returns a message naming the authenticated GitHub account and explaining that GitHub does not provide shell access. GitHub documents exit status `1` as expected for this test, so a generic success echo must not be used to judge it.

The account named in the response must be the intended account. `Permission denied (publickey)` means the authentication gate has not passed.

## Step 6 — Prove access to the exact repository

Authentication to GitHub is not the same as authorization for a repository. Prove the exact repository without cloning or changing it:

On macOS:

```bash
GIT_SSH_COMMAND='/usr/bin/ssh -o BatchMode=yes' \
/usr/bin/git ls-remote "git@github.com:YodaSpow/codex-config-manager.git" HEAD \
&& echo "✅ Repository SSH access verified"
```

On Windows PowerShell:

```powershell
$env:GIT_SSH_COMMAND = "C:/Windows/System32/OpenSSH/ssh.exe -o BatchMode=yes"
git ls-remote "git@github.com:YodaSpow/codex-config-manager.git" HEAD
if ($?) { Write-Output "✅ Repository SSH access verified" }
Remove-Item Env:GIT_SSH_COMMAND
```

`BatchMode=yes` refuses interactive password or passphrase prompts. Passing this check demonstrates that the current user environment can reach and read the repository non-interactively. It does not prove launchd, Windows Task Scheduler or another service context.

Write access should not be tested by creating noise, force-pushing, or rewriting history. Prove permitted write access only through a legitimate bounded development commit when its governing task reaches that stage.

## Step 7 — Clone into a deliberate local path

Choose a destination that does not exist or contain unrelated files. Do not clone the repository into the live `.codex` directory.

Generic form:

```text
git clone "git@github.com:OWNER/REPOSITORY.git" "/absolute/path/to/local/repository"
```

Codex Config Manager on a Mac using this repository's local convention:

```bash
/usr/bin/git clone \
  "git@github.com:YodaSpow/codex-config-manager.git" \
  "$HOME/Scripts/codex-config-manager" \
&& echo "✅ Repository cloned successfully"
```

If that destination already exists, do not run clone over it. Inspect whether it is the intended repository and whether it can safely fast-forward under the governing project contract.

After cloning:

```bash
cd "$HOME/Scripts/codex-config-manager" \
&& /usr/bin/git remote get-url origin \
&& /usr/bin/git branch --show-current \
&& /usr/bin/git status --short --branch \
&& echo "✅ Checkout identity inspected successfully"
```

For Windows, use the same SSH URL with an approved local destination and the Git/SSH client selected earlier. Do not reuse the macOS path literally.

## Automation and headless contexts

An interactive terminal result does not prove that a scheduled process can use the same key. Agents and services may have different environment variables, agent sockets, keychain access or user identities.

For Codex Config Manager:

- the pre-goal Mac mini gate requires the account test and exact-repository `BatchMode=yes` test above;
- Phase 15 repeats repository authentication in the real Mac mini runtime context;
- consumer LaunchAgent installation is allowed only after foreground validation;
- launchd-domain SSH access must be proven after the real consumer plist and user-domain context exist;
- the consumer runtime may fetch and fast-forward but never commits or republishes;
- a human-controlled Phase 15 goal may later create one permitted public evidence/refinement commit under Doc 12's development boundary.

A passphrase prompt, missing agent socket or locked keychain in headless execution is a failed automation gate even when interactive SSH works.

## Troubleshooting boundaries

| Symptom | Likely boundary | Safe next check |
| --- | --- | --- |
| `Permission denied (publickey)` | Key not loaded, public key not registered, wrong account or wrong identity selected | Recheck agent membership, GitHub key title/account and selected `IdentityFile` |
| Host authenticity warning | First contact or missing `known_hosts` entry | Compare the displayed fingerprint with GitHub's published fingerprints before accepting |
| Connection timeout | Network, firewall, proxy, policy or endpoint availability | Confirm organizational policy and use GitHub's official connectivity troubleshooting; do not bypass controls |
| Interactive SSH works but `BatchMode=yes` fails | Passphrase/agent/keychain dependency | Fix non-interactive key availability before scheduled use |
| Windows Git still prompts | Git for Windows and Windows OpenSSH agent mismatch | Align Git with the intended SSH client using GitHub's documented guidance |
| Clone succeeds but consumer later refuses | Repository cleanliness, branch, upstream, config identity or runtime contract | Continue with the repository's role-aware validation; do not weaken Git safety |

Verbose SSH diagnostics can reveal usernames, paths and public-key fingerprints. Review and redact diagnostic output before placing it in public evidence.

## Machine-bootstrap acceptance record

A machine is ready to begin a repository-specific setup goal only when the operator can record:

```text
machine:                   identified without publishing private details
private key:               machine-local and not copied
GitHub account response:   expected account confirmed
host fingerprint:          checked against GitHub documentation
repository ls-remote:      succeeded with BatchMode=yes
repository destination:    safe and distinct from live managed data
private material in Git:   none
```

This record contains results and identifiers only. It must not include the private key, passphrase, full public key, authentication-agent data or credential-bearing diagnostics.

## Official references

- [GitHub — Connecting to GitHub with SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [GitHub — Checking for existing SSH keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/checking-for-existing-ssh-keys)
- [GitHub — Generating a new SSH key and adding it to the ssh-agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
- [GitHub — Adding a new SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
- [GitHub — Testing your SSH connection](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/testing-your-ssh-connection)
- [GitHub — GitHub's SSH key fingerprints](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints)
- [GitHub — Cloning a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)

## Documentation-only validation — 28 August 2026

At creation:

- the Mac Studio checkout used the established `git@github.com:YodaSpow/codex-config-manager.git` remote and was clean on `main`;
- Doc 11 recorded successful Mac Studio user-domain and launchd-domain SSH evidence;
- Docs 3, 9, 10 and 12 still identified real Mac mini Git authentication as unproven Phase 15 work;
- current GitHub documentation was checked for macOS, Windows, account-key registration, host verification, connection testing and SSH cloning behavior;
- no SSH directory, key, agent, GitHub setting, repository remote, configuration, launchd state or other machine credential was created, read, changed or deleted by this document.
