# Doc 4 — Implementation Discovery — Deterministic Model-Derived Machine Identity

**Status:** Operator-approved identity contract; verified on the Mac Studio and Mac mini; not yet implemented  
**Scope:** Human-readable machine identity, `config.yaml` ownership and role-aware preflight  
**Relationship to existing documents:** This record refines the machine-ID portion of Doc 3 Phase 5. It does not change explicit role selection or infer publisher/consumer authority from hardware.  
**Related plan:** [Doc 3 — Mode C Implementation Plan — Mac Studio Bootstrap and Mac mini Handoff](03-mode-c-implementation-plan.md)

## Status

- ✅ macOS `Model Name` is the selected native source for the project machine identity.
- ✅ One generic normalization rule derives `MacStudio` and `MacMini` without a model-name lookup table.
- ✅ The command has been executed successfully on both real machines.
- ✅ `machine.id` and `role` remain separate configuration facts.
- ▶ Mode C must implement this identity derivation, config formation, validation and tests.
- ⛔ This document does not create or modify either machine's configuration.

## Purpose

The repository and its documentation distinguish Mac Studio publisher work from Mac mini consumer work. That distinction must not depend only on an AI interpreting prose, an editable hostname or a hard-coded script branch.

Codex Config Manager therefore needs a deterministic, human-readable machine identity that:

- originates from a native macOS hardware-family fact;
- produces the same result every time on the same product family;
- is independent of Computer Name, Local Hostname and Unix hostname;
- can be placed directly into the ignored local `config.yaml`;
- can be recomputed during preflight and compared with configuration;
- does not itself assign the publisher or consumer role.

## Terminology

macOS does not expose a native field literally named `machine.id`. `machine.id` is a Codex Config Manager configuration field.

Its selected native source is the macOS hardware product-family value exposed as `Model Name`:

```text
Mac Studio
Mac mini
```

The project converts that source into:

```text
MacStudio
MacMini
```

This is a model-derived orchestration identity. It is not a PID, hostname, serial number, platform UUID, credential identity or globally unique hardware fingerprint.

## Why `Model Name` is the source

The observed macOS identity surfaces have different meanings:

| Surface | Suitability for `machine.id` |
| --- | --- |
| `Model Name` | Selected: stable, human-readable hardware product family |
| `Model Identifier` | Technical model revision; not the intended human lane |
| Computer Name | Human-readable but editable and personally named |
| Local Hostname | Bonjour/network identity; editable and naming-dependent |
| Unix hostname | Operational network/shell state; may differ or contain legacy naming |
| Platform UUID | Unique but opaque and unnecessarily fingerprint-like for this requirement |
| Serial number | Sensitive and unnecessary |
| PID | Process identity that changes between executions; unusable for machine identity |

The Mac Studio and Mac mini hostnames differ from their hardware-family names. Model-derived identity therefore avoids allowing local naming choices or historical hostname errors to control orchestration identity.

## Canonical normalization rule

The normalization is mechanical and contains no Mac Studio/Mac mini lookup table:

1. Read the non-empty native `Model Name`.
2. Split it on whitespace.
3. Preserve the first word exactly.
4. For every subsequent word, uppercase its first character and preserve the remainder.
5. Concatenate the words without separators.
6. Fail if no model name or no derived value is available.

Examples:

```text
Mac Studio  → MacStudio
Mac mini    → MacMini
MacBook Pro → MacBookPro
iMac        → iMac
```

The implementation must not return a fabricated `Unknown` identity and continue. Identity derivation failure is a preflight failure.

## Canonical human verification command

This read-only Terminal command prints only the derived machine identity:

```bash
/usr/sbin/system_profiler SPHardwareDataType \
| /usr/bin/awk -F': ' '/Model Name:/{n=split($2,w,/[[:space:]]+/); id=w[1]; for(i=2;i<=n;i++) id=id toupper(substr(w[i],1,1)) substr(w[i],2); print id; found=1; exit} END{if(!found) exit 1}'
```

This command is the human verification surface. The Python application should implement the same normalization natively rather than invoke an embedded shell pipeline.

## Verified two-machine evidence

The operator ran the canonical command on the real Mac mini on 21 August 2026. Its decisive output was:

```text
MacMini
```

The operator ran the same command on the real Mac Studio on 21 August 2026. Its decisive output was:

```text
MacStudio
```

The same generic command therefore produced the intended identity on both sides of the initial topology without hostname input or hard-coded model matching.

Read-only Mac Studio inspection also confirmed that structured `system_profiler` output supplies both `machine_name` and `machine_model`, with `machine_name` equal to `Mac Studio`:

```text
structured_machine_name_key_present= True
structured_machine_model_key_present= True
structured_machine_name_matches_expected= True
```

Mode C should prefer structured `system_profiler` output for Python parsing where it proves reliable, while preserving the exact `Model Name` semantics and normalization verified by the human command.

## Configuration ownership contract

The ignored Mac Studio configuration contains:

```yaml
machine:
  id: MacStudio

role: publisher
```

The ignored Mac mini configuration contains:

```yaml
machine:
  id: MacMini

role: consumer
```

`config/config.example.yaml` must show the safe public shape and explain that `machine.id` is derived from the native model name during local configuration formation.

The installer/configuration workflow may display or populate the derived value, but the resulting truthful value lives in local ignored `config.yaml`. It must not be published as machine-specific repository state.

## Runtime identity and role preflight

Before publisher or consumer mutation, Git publication, deployment or launchd activation, the application must:

```text
read native Model Name
        ↓
derive actual machine ID
        ↓
load configured machine.id
        ↓
exact match?
   ├── NO  ──► fail safely before mutation
   └── YES
        ↓
validate separately configured role
        ↓
invoke only that role's workflow
```

Examples:

```text
actual=MacStudio  configured=MacStudio  role=publisher  → identity accepted
actual=MacMini    configured=MacMini    role=consumer   → identity accepted
actual=MacMini    configured=MacStudio  role=publisher  → stop: identity mismatch
```

Hardware family does not assign authority. A detected `MacStudio` must not automatically become a publisher, and a detected `MacMini` must not automatically become a consumer. The configured role remains explicit and authoritative after identity match.

This preserves the existing architecture while preventing a truthful configuration for one hardware family from being used silently on the other.

## Documentation and human-lane use

The identity should be visible through installation, status and validation output so a human or AI can establish its current lane before following role-specific instructions. Conceptually:

```text
Detected machine ID:   MacMini
Configured machine ID: MacMini
Configured role:       consumer
Relevant lane:         Mac mini consumer documentation and handoff
```

The repository remains shared. Both machines still need the common architecture, configuration and safety contracts. Machine identity and configured role determine which operational lane is installed and which role-specific documentation applies; they do not hide or delete the other lane's public documentation.

## Reusability boundary

`MacStudio` and `MacMini` identify hardware product families, not globally unique physical machines. Two machines with the same model name derive the same value.

That is sufficient for the current one-Mac-Studio/one-Mac-mini topology and for preventing cross-family config mistakes. The implementation must not treat the value as a secret, credential or globally unique database key.

If the project later needs to distinguish multiple consumers of the same hardware family, a separate explicit instance label may be added through the public configuration contract. That future distinction must not replace or weaken the deterministic model-derived identity defined here.

## Mode C requirements

Mode C must:

- implement model-name retrieval with an absolute macOS tool path and safe subprocess handling;
- prefer structured output where validated rather than parse localized presentation text blindly;
- implement the normalization in Python with no hardware-model lookup table;
- validate non-empty, well-formed results;
- form or present the truthful local `machine.id` during configuration setup;
- compare detected and configured identity before mutation;
- keep role validation separate;
- expose identity and role through read-only status/validation output;
- test Mac Studio, Mac mini, multiword model, single-word model, missing output, malformed output and mismatch cases;
- ensure launchd uses the same preflight;
- document the implemented config formation and failure behaviour from real evidence.

## Current implementation status

- ✅ The identity source, normalization, Mac Studio result and Mac mini result are verified and durably recorded.
- ✅ The separation between derived machine identity and explicit role is locked.
- ▶ Doc 3 Phase 5 must implement and validate this contract.
- ⛔ No config, Python logic, installer, launchd service or runtime behaviour is established by this document.
