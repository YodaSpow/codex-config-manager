---
name: capability-readiness
description: Establish and prove the foundational capabilities a project or proposed goal assumes before dependent execution begins. Use during project inception, architecture or goal planning, when future work depends on unproven APIs, services, credentials, runtimes, storage, or network routes, or when a deferred foundation becomes timely later in the project lifecycle. Also use on demand to discover and commission likely foundations before a goal exists. Do not use for mature capabilities already proven by current repository evidence, full feature testing, ordinary implementation, or runtime monitoring.
---

# Capability Readiness

**Version:** 1.1 · **Updated:** 19 September 2026

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
  repository evidence has not already proven; or
- a previously deferred foundation becomes necessary for upcoming work.

Do not impose readiness work merely because a project uses technology. Reuse
current proof for mature foundations. The gate concerns consequential external
or operational assumptions whose absence would prevent later work from even
starting.

This skill remains available at three points in the project lifecycle:

1. **Inception discovery** — before a goal exists, use read-only discovery
   to identify likely foundations, authoritative references, configuration
   requirements, human gates, and the smallest useful connectivity proofs.
2. **Goal preflight** — inspect the proposed goal, identify its unproven
   enabling assumptions, and make their readiness explicit before dependent
   execution is treated as viable.
3. **Lifecycle re-entry** — resume the same readiness workflow when a
   deliberately deferred dependency becomes timely. Reuse established
   fixtures and evidence instead of rebuilding them.

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

Determine from authoritative provider guidance and the intended project use
whether authentication is **required**, **preferred**, or **not needed**. Do
not invent credential ceremony. When authenticated use is preferred because
the intended workload needs its quotas, control, or reliability, treat the key
as part of that workload's readiness even if a limited anonymous route exists.

Keep these two human states distinct:

- **Awaiting operator input** — the protected destination and checker are ready
  and the operator can supply the credential now.
- **Deferred by decision** — the operator has intentionally postponed the
  credential or approval until a named future dependency gate.

Neither state means unavailable or failed. A deferred item must re-enter the
readiness workflow before the first milestone that depends on it.

Before asking the operator to supply a secret:

1. create or verify the intended real configuration or secret location;
2. prove version control excludes secret-bearing material;
3. place only a placeholder in the committed example;
4. tell the operator exactly which prepared local field or file needs the
   value;
5. provide a clickable file link in Codex, and open the prepared file when
   useful or requested, so the operator does not have to discover a buried
   filesystem path;
6. never request that the secret be pasted into chat; and
7. pause the dependent readiness check while leaving unrelated work available.

After the operator confirms provision, resume the same readiness workflow,
verify presence or configuration shape without printing the value, and run the
prepared baseline check. Do not require the operator to restate earlier context
or manually reconstruct the next step.

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
6. gate only the work that actually depends on the unresolved foundation.

Independent preparation or goal work may continue when it does not rely on
that foundation. Do not describe a dependent milestone or final outcome as
executable until its required foundations are proven. A missing dependency
must never become an implied project-wide blocker merely because readiness
identified it.

Do not turn every goal into a large preparatory programme. A small missing
fixture can be the first milestone. Use a separate readiness goal when several
dependencies, credentials, human approvals, or independent proof boundaries
would otherwise obscure the main outcome.

The result is not "the future feature works." It is "the project now has the
authoritative plans, safe connection fixtures, provisioned prerequisites, and
baseline evidence needed to attempt that feature honestly."

## Completion and handoff

Use precise states and never blur an assessed dependency with a ready one:

- **Discovered** — the dependency and authoritative route are known, but its
  project fixtures or baseline evidence are not complete.
- **Fixtures prepared** — configuration, secret destination, checker, and
  references exist, but the baseline proof has not completed.
- **Awaiting operator input** — the next protected human action is prepared and
  available now.
- **Deferred by decision** — the human action or commissioning is intentionally
  postponed until a named future gate.
- **Proven ready** — the required foundation has current baseline evidence
  through the authorised project path.
- **Unavailable or disproven** — current evidence shows that the intended route
  cannot provide the assumed foundation and needs reconsideration.
- **Assessment incomplete** — material discovery or evidence is still missing,
  so no stronger classification is justified.

Only **proven ready** unlocks dependent execution. Every other state leaves
that dependency's readiness incomplete without automatically blocking
unrelated project work. Report:

- what foundation was established;
- the authoritative reference and project-owned path;
- the baseline proof and its limits;
- any human-supplied prerequisite still outstanding;
- whether the current state is awaiting action now or deferred to a named gate;
- which proposed goals are now enabled or still gated; and
- any source-versus-documentation discrepancy.

Never convert documentation, a placeholder, a successful detached request, or
an unverified credential claim into proof that a capability is ready.

If global `AGENTS.md` awareness is requested, keep the mention short: make the
assumption gate permanently discoverable and leave this skill to own the full
workflow. Follow protected global-guidance review, recovery, version, approval,
application, and proof requirements before changing that file.
