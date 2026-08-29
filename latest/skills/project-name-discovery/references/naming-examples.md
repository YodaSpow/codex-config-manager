# Naming Examples

## Purpose of This Reference

This file demonstrates what a strong Project Name Discovery run looks like.

It is not a list of names to reuse.

The goal is to show how project distillation, cultural exploration, user reaction, negative evidence, and independent semantic reinforcement can converge on a durable name.

---

## Worked Example — Canonical Media Capability Layer

### Project Distillation

The project is a canonical media capability layer.

It resolves media identity and metadata through TMDB, determines media type, establishes canonical external identifiers, and queries downstream systems such as Sonarr and Radarr for availability.

Its enduring responsibility is broader than any provider:

> Resolve what something is, establish the identifiers that make it understandable across systems, and use those identifiers to unlock authoritative information from multiple independent sources.

### Capability Verbs

- resolve
- identify
- reveal
- retrieve
- connect
- route
- unlock
- reconcile

---

## Discovery Field

### The Matrix — `keymaker`

The Keymaker creates keys that provide access to otherwise inaccessible parts of the Matrix.

This aligned unusually well with the project's architecture because canonical identifiers act as keys into different downstream systems.

### The Matrix — `architect`

The Architect understands the Matrix at a system level and represents a role defined by understanding and governing a larger environment.

Strong role-token energy, but it implies design and control more than lookup, access, or resolution.

### The Matrix — `matrix`

The Matrix is the underlying system connecting and representing an entire reality.

Extremely strong cultural recognition and excellent visual identity, but broader than the project's specific responsibility.

### Harry Potter — `accio`

The Summoning Charm means, functionally, "bring the requested thing here."

A strong action token because it is repeated across the franchise, highly recognizable to people familiar with the films, and can stand independently as a single word.

Its function maps best to retrieval.

### Harry Potter — `lumos`

A frequently used spell that illuminates what could not previously be seen.

Strong cultural landing and a good metaphor for revealing truth or state.

### Harry Potter — `pensieve`

An object used to retrieve and explore stored memories in context.

Conceptually relevant to knowledge retrieval, but less frequently referenced and therefore weaker as a cultural token for this user.

### Star Trek — `tricorder`

A device used to identify, analyze, and report what is present.

Excellent functional alignment with lookup and inspection.

Strong artifact token, but personal cultural recognition may vary.

### Alien — `mother`

MU/TH/UR, usually called Mother, is the Nostromo's central computer.

It is queried for authoritative information about the ship and its environment.

Strong system-identity candidate when the project behaves like a central source of domain truth.

### Total Recall — `recall`

The word has a strong film association while also carrying an ordinary meaning related to information retrieval and memory.

Very clean as a project name, though the film association is less functionally specific than Keymaker.

### Stargate — `stargate`

One gateway provides access to many destinations.

Very strong functional analogy for a shared access layer, though the name points more to the gateway itself than to identity resolution.

### Marvel — `jarvis`

JARVIS acts as an intelligent interface over many underlying systems and information sources.

Excellent cultural and architectural alignment for an AI or delegated intelligence project.

For this project it was rejected because the service itself was not intended to be an AI.

### Marvel / Interstellar — `tesseract`

A culturally powerful token with multiple prominent fictional associations.

The user's immediate reaction was Marvel, demonstrating strong cultural landing.

However, the term did not fit the desired project identity well enough and its cross-franchise ambiguity weakened clarity.

### Tron — `grid`

The Grid is the interconnected digital environment in Tron.

The concept is strong, but the culturally meaningful form is "The Grid," not `grid`.

This became useful negative evidence for the independence test: a strong one-word project token should ideally stand alone without requiring an article or phrase.

### Terminator — `skynet`

Enormously recognizable and visually strong.

It also represents a system spanning many connected resources.

Rejected because its dominant cultural meaning carries strongly negative autonomous-AI associations.

---

## What the User Reactions Revealed

The user's responses were not incidental. They exposed the real naming criteria.

Important reactions included:

- Frequently repeated words land harder than obscure but semantically perfect references.
- A candidate should ideally stand alone as a single word.
- Visual identity matters in addition to semantic alignment.
- Personal recognition matters more than abstract cultural popularity.
- A name can be culturally excellent but still belong to the wrong project category.
- A candidate becomes especially powerful when several independent meanings reinforce it naturally.

Examples:

- `pensieve` was relevant but too vague and infrequent.
- `accio` landed strongly because it was memorable, frequently used, and independent.
- `jarvis` was excellent but felt like the name of an AI system rather than this MCP.
- `grid` depended too heavily on "The Grid."
- `tesseract` triggered immediate Marvel recognition, proving the cultural-token method even though it was not selected.
- `keymaker` became stronger with every comparison.

---

## Why Keymaker Became the Leading Candidate

Keymaker was not selected because it sounded cool.

Multiple independent signals converged:

1. **Cultural recognition**  
   The Keymaker is a recognizable role from The Matrix.

2. **Functional alignment**  
   The Keymaker creates and uses keys that unlock otherwise inaccessible parts of a larger system.

3. **Existing architectural metaphor**  
   Before the candidate emerged, the architecture had already been described as:

   > one brain, many doors

4. **API terminology**  
   APIs independently use keys as access mechanisms.

5. **Canonical identity**  
   The project's canonical identifiers behave like keys that unlock downstream provider-specific systems.

6. **Provider independence**  
   The name describes the project's enduring responsibility rather than TMDB, Sonarr, Radarr, Seer, MCP, REST, or any other implementation detail.

7. **Repo identity**  
   `keymaker` is concise, lowercase-friendly, visually clean, and memorable.

The most important lesson is not "Keymaker is a good name."

The reusable lesson is:

> A candidate becomes unusually strong when cultural, functional, architectural, linguistic, and visual signals converge independently rather than being retrofitted after selection.

---

## Naming Lane Classification

| Lane | Example |
|---|---|
| Functional metaphor | `keystone` |
| Action token | `accio` |
| Role token | `keymaker` |
| System identity | `matrix` |
| Artifact | `tricorder` |
| Intelligence identity | `jarvis` |
| Cultural shorthand | `recall` |

No lane is inherently superior.

The project context and user reaction determine which lane best expresses the project's identity.

---

## Example Survivor Board

At one point the strongest exploration board looked like:

`keymaker` · `accio` · `architect` · `tricorder` · `mother` · `recall`

The process deliberately did not stop as soon as Keymaker became strong.

That prevented premature convergence and made the eventual preference more trustworthy.
