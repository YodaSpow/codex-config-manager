---
name: capability-readiness
description: Establish and prove the foundational capabilities a new project or proposed goal assumes before dependent execution begins. Use during project inception, architecture or goal planning, or when future work depends on unproven APIs, services, credentials, runtimes, storage, or network routes. Also use on demand to discover and commission likely foundations before a goal exists. Do not use for mature capabilities already proven by current repository evidence, full feature testing, ordinary implementation, or runtime monitoring.
---

# Capability Readiness

**Version:** 1.0 · **Updated:** 19 September 2026

Prevent planned work from silently treating intended infrastructure as working
infrastructure. Pull forward the enabling foundations that later work will
need, prove their baseline availability through the project's authorised path,
and leave reusable evidence. Do not pull forward the later features themselves.

Capability Readiness answers: **Does the house, its required utilities, and a
safe way to test them actually exist?** Later goals decide what to build and do
inside it.

## Automatic assumption gate

Apply this skill without requiring its exact name when either condition is met:

- a new or infancy-stage project is selecting external capabilities; or
- a proposed goal assumes an API, service, account, credential, runtime,
  storage surface, network route, or other technical enabler that current
  repository evidence has not already proven.

Do not impose readiness work merely because a project uses technology. Reuse
current proof for mature foundations. The gate concerns consequential external
or operational assumptions whose absence would prevent later work from even
starting.

This skill has two entry routes:

1. **Goal-led readiness** — inspect the proposed goal, identify its unproven
   enabling assumptions, and make their readiness explicit before dependent
   execution is treated as viable.
2. **Discovery-led readiness** — before a goal exists, use read-only discovery
   to identify likely foundations, authoritative references, configuration
   requirements, human gates, and the smallest useful connectivity proofs.

Readiness does not itself authorise repository changes, secret provision,
external mutations, service starts, installs, or infrastructure changes. Use
the applicable operating mode and obtain the authority required for each
action.

## Distinguish foundations from features

Pull forward only what is needed to establish that a dependency can be used:

- the intended repository structure and ownership boundary;
- the canonical configuration surface and safe secret reference;
- authoritative API or service documentation;
- the supported endpoint, authentication method, and connection route;
- human-supplied accounts, keys, or approvals when required;
- a small, safe, repeatable connectivity checker; and
- sanitized evidence of the baseline result and its limits.

Stop after the smallest representative proof that the utility turns on. This
may be an authenticated health, status, discovery, version, or similarly
harmless request and an expected response such as HTTP 200. Do not use a fixed
status code when the provider's documented success contract differs.

Do not pull forward business operations, mutations, complete endpoint
coverage, schemas, pagination, performance, resilience, or feature acceptance.
Those belong to the goal or later implementation package that needs them.

## Discover the real dependency contract

Begin with the repository's instructions, conventions, current configuration,
adapters or clients, and existing readiness evidence. Do not invent a second
runtime or configuration path.

For an external API or service, use this evidence order:

1. official current documentation, OpenAPI or Swagger specification, or
   provider-owned reference;
2. the provider's registered routes and implementation source when official
   documentation is absent, materially incomplete, or demonstrably lagging;
3. the project's established client, adapter, authentication, and runtime
   path; and
4. a minimal connectivity proof through that authorised project path.

Link to authoritative references rather than copying whole external manuals
into the repository. If source exposes a useful route missing from the
published contract, label the discrepancy explicitly. Source evidence can
establish an implementation route; it does not prove a deployed runtime until
authorised live evidence confirms it.

When a concrete pattern would help, read
[`references/worked-example.md`](references/worked-example.md). Adapt it to the
repository; do not copy its filenames, stack, or response contract
mechanically.

## Establish the readiness fixtures

Prefer existing project conventions. For a new project without an established
shape, create only the minimum coherent fixtures authorised for the task:

- the required repository directories;
- a `tools/` area for safe, re-runnable readiness checks;
- the project's real local configuration surface;
- a structurally aligned committed example configuration; and
- an approved ignored or otherwise protected location for secrets and
  generated evidence.

Under the preferred YAML convention, the real local `config.yaml` is the
operator surface and `config.yaml.example` is its committed placeholder-only
counterpart. Keep them structurally aligned. If the repository already has a
different canonical configuration contract, preserve it instead of forcing
YAML.

Before asking the operator to supply a secret:

1. create or verify the intended real configuration or secret location;
2. prove version control excludes secret-bearing material;
3. place only a placeholder in the committed example;
4. tell the operator exactly which prepared local field or file needs the
   value; and
5. never request that the secret be pasted into chat.

After the operator confirms provision, verify presence or configuration shape
without printing the value.

## Prove baseline connectivity

The readiness checker should:

- use the repository's canonical config, authentication, adapter, and runtime
  path wherever one exists;
- perform one harmless request sufficient to prove baseline connectivity;
- fail safely and explain missing configuration, authentication, transport,
  or response-contract problems;
- be safe to rerun and avoid external mutations;
- never print credentials or sensitive response bodies; and
- emit concise sanitized evidence that can be understood later.

Follow the applicable API runtime authority contract. A detached shell request
may help bootstrap diagnosis, but it must not overrule the established runtime
or be promoted into authoritative integration proof when it uses a different
path.

Useful evidence records:

- dependency and intended purpose;
- authoritative reference link;
- checked route or operation;
- configuration completeness without secret values;
- authentication and baseline response outcome;
- evidence time and execution context; and
- explicit limits: what this check did **not** prove.

Prefer executable, re-runnable evidence over a large new prose document. The
checker, its configuration contract, authoritative links, and sanitized result
should let a later agent establish readiness without reconstructing the chat.
Use an existing project heartbeat or evidence surface when one exists; do not
create a second status system merely for this skill.

## Integrate readiness with goals

While designing a goal:

1. list the external or operational capabilities the outcome assumes;
2. locate current repository-owned proof for each assumption;
3. classify each as proven, human-gated, discovered but unproven, or absent;
4. reuse proven capabilities without repeating commissioning;
5. move unproven foundations into an explicit prerequisite, initial milestone,
   or separate enabling goal according to their independence and human gates;
   and
6. do not describe the dependent outcome as executable until its required
   foundations are proven or visibly gated.

Do not turn every goal into a large preparatory programme. A small missing
fixture can be the first milestone. Use a separate readiness goal when several
dependencies, credentials, human approvals, or independent proof boundaries
would otherwise obscure the main outcome.

The result is not "the future feature works." It is "the project now has the
authoritative plans, safe connection fixtures, provisioned prerequisites, and
baseline evidence needed to attempt that feature honestly."

## Completion and handoff

Readiness is complete only when the required foundation has current evidence,
or is explicitly recorded as human-gated or unavailable. Report:

- what foundation was established;
- the authoritative reference and project-owned path;
- the baseline proof and its limits;
- any human-supplied prerequisite still outstanding;
- which proposed goals are now enabled or still gated; and
- any source-versus-documentation discrepancy.

Never convert documentation, a placeholder, a successful detached request, or
an unverified credential claim into proof that a capability is ready.

If global `AGENTS.md` awareness is requested, keep the mention short: make the
assumption gate permanently discoverable and leave this skill to own the full
workflow. Follow protected global-guidance review, recovery, version, approval,
application, and proof requirements before changing that file.
