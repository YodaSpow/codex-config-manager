# Capability Readiness — Worked Example

Read this reference when establishing readiness for a new project's external
API dependency or when deciding how readiness should gate a proposed goal.
Adapt it to the repository's established conventions and the provider's actual
contract.

## Example scenario

A new project intends to use a remote catalogue API in a later import goal.
The plan names the API, but the repository has no configuration surface,
credentials, client path, connectivity checker, or retained proof.

The later import operation is **not** part of readiness. The enabling question
is whether the project can safely authenticate and reach the API through its
intended path.

## Minimal repository shape

```text
project/
├── config.yaml.example       # committed, placeholder-only structure
├── config.yaml               # local operator surface, excluded from Git
├── tools/
│   └── check_catalog_api.py  # safe, re-runnable baseline checker
└── evidence/
    └── capability-readiness/ # sanitized results if this is the approved evidence location
```

Do not create this exact layout when the repository already has a canonical
configuration, tools, diagnostics, or evidence convention. Extend the owned
path instead.

## Configuration relationship

Committed example:

```yaml
# 🔐 Secrets
secrets:
  catalogue_api_key: "REPLACE_ME"

# 🌐 API Endpoints
api:
  catalogue_base_url: "https://provider.example/api"

# 📦 Catalogue
catalogue:
  api_key_secret: "catalogue_api_key"
  base_url_ref: "catalogue_base_url"
```

The real local configuration has the same structure. The operator places the
real value only in that protected local file after the agent proves that Git
excludes it. The checker confirms presence without printing the value.

## Discovery evidence

Record or link the smallest useful authoritative set:

- official API reference or current OpenAPI/Swagger URL;
- documented authentication method;
- documented harmless readiness operation; and
- implementation-source citation only when the published contract is missing
  or materially contradicted.

If source reveals an undocumented route, state:

- what the published documentation says or omits;
- which registered route and implementation establish source availability;
- that deployed availability remains unproven until authorised live evidence;
  and
- why this route is being considered.

## Checker boundary

The readiness checker may:

1. load the canonical project configuration;
2. validate that required non-secret settings and secret references exist;
3. authenticate through the intended client or adapter;
4. call one documented, harmless status, version, discovery, or equivalent
   route; and
5. write a sanitized result.

It must not perform the future import, enumerate every endpoint, mutate remote
state, log the key, or claim complete API compatibility.

## Sanitized evidence example

```text
Capability: remote catalogue API
Reference: official API specification
Project path: canonical catalogue client using local project configuration
Configuration: required fields present; secret value withheld
Baseline operation: authenticated service-status request
Outcome: success under the provider's documented response contract
Proven: configuration, authentication, transport, and baseline service response
Not proven: catalogue import, pagination, mutation, rate limits, or resilience
```

Do not require this exact text format. Preserve its distinction between what
was proved and what remains for downstream work.

## Goal integration

Before readiness:

```markdown
Goal viability: gated. The catalogue API is an intended dependency with no
repository-owned connectivity evidence.
```

After readiness:

```markdown
Goal viability: foundation proven. The later import goal may rely on the
canonical catalogue configuration and checker evidence; import behaviour
itself remains untested and in scope for that goal.
```

If the operator has not yet supplied the key:

```markdown
Goal viability: human-gated. Configuration and checker fixtures are ready;
baseline connectivity awaits the API key in the prepared local secret field.
```

The readiness state should be visible wherever the project already records
goal prerequisites or evidence. Do not create a duplicate heartbeat solely to
host these lines.
