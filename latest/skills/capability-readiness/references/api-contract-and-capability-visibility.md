# API contract and capability visibility

Use when an in-scope API-backed outcome needs a clearer provider capability
view or an explicit project dependency contract. This includes already
reachable services: reuse established connectivity proof. Do not inventory
every API merely because it exists, reopen a settled contract without a
material reason, or turn discovery into exhaustive endpoint testing.

## Look outward: what does the provider expose?

Start with the project's configured client/runtime and intended outcome.
Inspect only authorised provider references, schemas, registered routes and
source needed to understand the relevant surface.

- **Service identity and version:** surface the installed/deployed service
  version or build from current authoritative evidence. Separately identify
  the API version, contract revision and relevant compatibility constraints.
  A service's release number, an API path such as `/v2`, and an OpenAPI format
  version are different facts. Mark unknowns rather than deriving one from
  another or treating the latest public docs as the deployed contract.
- **Authority:** link the official version-matched docs and schema when
  available. Where docs lag, identify provider-owned registered routes and
  implementation source with their revision. Label documented support,
  source-backed exposure and deployed availability separately; explain any
  material mismatch instead of silently choosing a contract.
- **Reach and authentication:** describe the configured endpoint/route,
  project adapter/runtime, auth scheme and relevant permission tier using
  existing configuration references. Withhold secret values and scrub tokens,
  credential-bearing URLs or sensitive identifying details from evidence.
- **Capability areas:** give a compact map of the major relevant areas, such
  as discovery, lookup, search, bulk operations or events, with authoritative
  links. Show what the project actually uses from inspected clients/call
  sites; distinguish that from planned use or provider availability.
- **Adjacent options:** identify a small number of exposed capabilities only
  if they might simplify the proposed outcome or avoid rebuilding something
  the provider already offers. Explain the relevance, compatibility and proof
  limits. An option is not an adoption decision, implementation task or licence
  to call a mutating endpoint.

Use the best available evidence for each fact. A checked version response
proves that response in its stated context; it does not prove every capability
listed in the provider's schema. Do not probe every area to fill a table.

## Look inward: what exactly does this project rely on?

Retain one concise declaration in the established canonical project
documentation when writing is authorised; update or link the existing owner
instead of creating a second status system. A chat-only explanation is not a
durable selected contract. Under read-only authority, return the proposed
declaration, its intended canonical home and any decision still needed.

Capture the useful dependency contract, proportionate to the problem:

- service identity and observed version/build, with observation time/context;
- selected API/contract version and authoritative docs/schema/source reference;
  when unversioned, say so and anchor the relied-on revision with an available
  release, commit or schema digest rather than inventing a version;
- configured reach and auth method through safe configuration/client references;
- operations and response fields or semantics the project actually relies on,
  plus relevant compatibility constraints; link the full provider schema rather
  than copying it;
- current use versus selected future use, relevant adjacent options still only
  under consideration, and the decision or uncertainty behind the selection;
- evidence for each material reliance: documented, source-backed, or checked
  live through the authorised project path, with explicit gaps and limits.

Keep the declaration as canonical project truth about the selected dependency,
not a claim that the provider must behave as expected. Update it when the
project changes that selection or new authoritative evidence materially
changes the dependency. This does not establish monitoring or an automatic
upgrade policy.

## Keep proof and authority bounded

A representative harmless live check can prove a relevant reliance where the
task authorises it; use the existing runtime/client and safe operation. Reuse
current evidence where it already answers the question. Describe the exact
operation and observed result, not general API compatibility. Documented
availability is useful without live proof, provided it remains labelled.

Baseline readiness, selected contract and feature acceptance remain different
claims. Record unresolved version/schema discrepancies or unavailable
representative checks without inventing a failure or revoking unrelated
proven foundations. Follow the applicable runtime-authority contract when a
detached diagnostic differs from the project's authorised path.

## Compact illustration

An invented catalogue service is reachable through the project's existing
adapter. The outcome is to reduce repeated item-by-item lookups.

The discovery reports service build `4.7`, selected API `v2`, a provider schema
at a pinned revision, configured adapter/auth method without values, and a
short map of lookup, search and batch retrieval. Source inspection shows the
project currently uses only lookup. The documented batch route may reduce
round trips; it remains an option until selected and proved for that use.

The canonical dependency entry records the current lookup contract, its
authoritative schema and the existing harmless status proof. It labels batch
retrieval as documented but untested, with implementation and performance
proof outside this discovery. No real service version, capability or runtime
result is asserted by this illustration.
