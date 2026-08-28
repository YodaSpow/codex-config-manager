# Doc 17 — Mac mini Report — Phase 15 validation

**Status:** Open — Mac mini validation complete; awaiting Mac Studio reconciliation
**Machine lane:** Real Mac mini consumer
**Governing handoff:** [Doc 12 — Mac mini Phase 15 Handoff](12-mac-mini-phase-15-handoff.md)
**Activation runbook:** [Doc 15 — Operator Runbook — Mac mini Phase 15 Activation](15-operator-runbook-mac-mini-phase-15-activation.md)
**Repository workflow:** Root [`AGENTS.md`](../AGENTS.md) and [Doc 16 — Agent Workflow and Publication Guardrails](16-repository-agent-workflow-and-publication-guardrails.md)

## Scope and conclusion

The real Mac mini completed the bounded Phase 15 consumer rollout at repository
commit `28562eef78a4637e065106caf511a43fab602f72`.

The repository-owned development environment, rsync runtime, consumer
configuration, foreground deployment, exclusion preservation, no-op behavior,
consumer LaunchAgent, launchd-domain repository access, automatic polling,
single-instance behavior and uninstall/reinstall contract all passed.

The Mac mini consumer is operational. The complete two-machine system remains
open pending the required Mac Studio reconciliation and a response commit that
references this report.

## Platform and repository evidence

- Hardware: Mac mini (`Macmini9,1`), model-derived identity `MacMini`.
- Operating system: macOS 14.7.1 on `arm64`.
- Python: repository-owned development environment using CPython 3.13.3 on
  `arm64`, within the declared `>=3.12,<3.15` range.
- Repository: clean `main` tracking `origin/main` through the exact SSH remote.
- Pulled publication SHA:
  `28562eef78a4637e065106caf511a43fab602f72`.
- User-domain SSH authentication identified the expected GitHub account, and
  `BatchMode=yes` access to the exact repository succeeded before Phase 15.

## Environment and rsync evidence

- The development `.venv` was constructed from the committed hashed
  development lock and passed its repository receipt, import and entry-point
  validation.
- The tracked rsync contract downloaded and verified the pinned upstream source
  before building repository-owned rsync 3.5.0.
- The resulting executable is arm64, matches its build receipt, supplies every
  required option and links only to permitted macOS system libraries. No
  Homebrew or other external package-manager runtime linkage was present.

## Consumer configuration and validation

The ignored private configuration was formed and validated with this public
shape:

```yaml
machine:
  id: MacMini
role: consumer
consumer:
  check_interval: 5m
git:
  remote: origin
  branch: main
  url: git@github.com:YodaSpow/codex-config-manager.git
```

All repository, Codex, runtime-state, lock and log paths are absolute,
machine-local and non-overlapping. Their private local values are not recorded
in this report.

The complete tracked test suite passed: `97 passed`. Environment validation,
repository hygiene validation and role-aware runtime validation also passed.

The pulled `latest/` snapshot and portable distribution validated with managed
fingerprint:

```text
9bfea4c3cfa1a7307d54b98170171110bd19df507995b3cb314287ca466ce678
```

The validated dynamic user-skill set was:

```text
chat-handoff
operational-modes
semantic-compression
```

## Foreground deployment and preservation evidence

The pre-deployment dry run identified changes only to global `AGENTS.md` and
the three validated dynamic user skills above.

The first foreground consumer run completed at the pulled SHA with no
repository update and deployed the managed change. Independent before/after
evidence then proved:

- live managed state exactly equalled validated `latest/`;
- `skills/.system/**` content and executable identity were unchanged;
- every observed `.DS_Store` was unchanged;
- unrelated `~/.codex` metadata was unchanged;
- the repository remained clean at the pulled SHA;
- no publisher path was invoked.

A second foreground run reported no repository update and no deployment. The
same managed, excluded and unrelated evidence remained unchanged, proving the
required no-op behavior.

## LaunchAgent and headless evidence

- Installed label: `com.yodaspow.codex-config-manager.consumer`.
- Program: repository-owned consumer entry point with the ignored consumer
  configuration.
- Working directory: the canonical repository checkout.
- Interval: 300 seconds with `RunAtLoad` enabled.
- The installed plist is a regular user-owned file with mode `0600`.
- The publisher plist and publisher launchd service were absent throughout.
- RunAtLoad completed a headless no-op consumer run with exit status 0.
- Because every consumer invocation performs the safe SSH fetch before
  deployment, that successful launchd run proved repository access from the
  actual launchd user domain.
- A later invocation occurred automatically on the configured interval and
  completed another headless no-op at the same SHA.
- Metadata-only rotating application logging and separate launchd stdout/stderr
  logging were present and operational.
- With the consumer lock deliberately held, launchd refused an overlapping run
  and logged the bounded single-instance error. After lock release, a clean
  recovery run completed with exit status 0.

## Uninstall and reinstall evidence

The consumer LaunchAgent was safely uninstalled and then reinstalled.

Uninstall removed only the consumer plist and loaded service. It preserved live
Codex state, `latest/`, the repository and HEAD, ignored configuration,
development environment, repository-owned rsync, runtime-state and lock roots,
and logs.

Reinstall restored the same consumer contract, completed a successful RunAtLoad
no-op and preserved the same live, repository, configuration, environment and
rsync evidence. Publisher state remained absent.

## Corrections and blockers

No consumer implementation correction or governing-document proposal was
required during this rollout.

The remaining case condition is the cross-machine closeout required by Docs 12,
15 and 16. It is not a Mac mini runtime blocker.

## Requested Mac Studio response

The Mac Studio should safely fast-forward a clean checkout to the commit
containing this report, then verify:

1. this Mac mini evidence is present on `origin/main`;
2. the Mac Studio publisher remains the only active Mac Studio role;
3. managed-state publication remains healthy;
4. the shared history is clean and aligned; and
5. no Mac mini report content is edited or closed by the Mac Studio.

The Mac Studio should publish any response through its owned documentation,
implementation or a normal Git commit that references Doc 17. After the Mac
mini safely receives and validates that response, the Mac mini will either
close this report and record the response commit SHA or keep the case open with
continuing evidence.
