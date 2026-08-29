---
name: project-name-discovery
description: Discover durable, memorable names for software projects, repositories, apps, services, agents, utilities, or technical components by distilling their enduring responsibility and exploring multiple naming abstractions. Use when naming or renaming a durable project identity; do not use for marketing copy, legal trademark clearance, or domain availability unless explicitly requested.
---

# Project Name Discovery

## Purpose

Discover durable, memorable project names by distilling a project's essential responsibility and exploring multiple naming abstractions rather than generating literal or generic names.

The goal is not to produce "cool names." The goal is to find a compact project identity that:

- fits what the project fundamentally does,
- survives implementation changes,
- lands clearly in the user's mind,
- works naturally as a project or repo name,
- and can gain strength from cultural, functional, metaphorical, or linguistic associations.

## When to Use

Use this skill when naming or renaming:

- software projects,
- repositories,
- apps,
- services,
- agents,
- utilities,
- internal tools,
- technical components,
- or other durable project identities.

Do not use it for product marketing copy, company naming, legal trademark clearance, or domain-name availability unless explicitly requested.

## Core Principle

Do not begin by inventing names.

Begin by understanding the project.

A strong name should emerge from the project's enduring responsibility, not from its current stack, implementation language, provider names, or temporary architecture.

## Phase 1 — Project Distillation

Summarize the project in plain language.

Extract:

1. The problem it solves.
2. The responsibility it owns.
3. The actions it performs.
4. The relationships it mediates.
5. The parts likely to remain true even if the implementation changes.

Then rewrite the project as a short capability statement.

Example shape:

> Resolve what something is, establish the identifiers that make it understandable across systems, and use those identifiers to unlock authoritative information from multiple sources.

Avoid provider-heavy descriptions unless the provider itself is part of the project's lasting identity.

## Phase 2 — Capability Extraction

Extract verbs and conceptual actions from the distilled project.

Examples:

- resolve
- identify
- reveal
- retrieve
- unlock
- connect
- route
- reconcile
- translate
- guide
- detect
- map
- observe
- verify
- bridge

These capabilities become search directions, not candidate names by themselves.

## Phase 3 — Explore Multiple Naming Lanes

Do not assume a single naming method will win.

Explore across multiple lanes:

### Functional Metaphor

A real-world concept whose behavior resembles the project.

Examples:
- keystone
- beacon
- compass
- loom

### Action Token

A word, command, incantation, or phrase whose meaning is "do this."

Examples:
- accio
- lumos

### Role Token

A person, title, or role whose responsibility resembles the project.

Examples:
- keymaker
- architect
- watcher

### System Identity

A named system that represents the whole operating environment or capability.

Examples:
- matrix
- skynet
- mother

### Artifact

An object whose fictional or real function resembles the project.

Examples:
- tricorder
- pensieve
- tesseract

### Intelligence Identity

A named intelligence or assistant that operates across capabilities.

Examples:
- hal
- jarvis

Use this lane only when the project itself behaves like an intelligence or delegated operator.

### Cultural Shorthand

A token that has escaped its original source and gained independent cultural meaning.

Examples:
- flux
- recall
- multipass

### Other Lanes

If another naming abstraction becomes relevant, add it rather than forcing candidates into the existing categories.

## Phase 4 — Cultural Token Discovery

When cultural naming is appropriate, search for terms from well-known film, TV, literature, games, mythology, or other shared cultural sources.

Prefer tokens that:

- are repeated enough to be memorable,
- can stand independently as a word,
- trigger recognition without requiring a full quote,
- have a functional or conceptual relationship to the project,
- look clean as a project or repo name,
- and remain understandable even after the implementation changes.

Recognition matters, but objective fame is not enough. Personal recognition for the user is a first-class signal.

A candidate can be culturally strong and still be wrong for the project.

## Phase 5 — Produce a Broad Discovery Field

Do not prematurely converge.

Generate a wide enough field to expose different semantic directions. Twenty to forty candidates can be appropriate when the territory is rich.

For each candidate, use this structure:

- **Source — `candidate`**  
  Short explanation of what the token means in its source and why it may or may not align with the project.

Do not present only winners. Include useful near-misses and explain why they are weaker.

Negative evidence helps reveal the naming criteria.

## Phase 6 — Treat User Reactions as Discovery Signals

The user's spontaneous reactions are valuable evidence.

Capture signals such as:

- immediate recognition,
- emotional resonance,
- "I know exactly what that means,"
- weak or absent recognition,
- visual dislike,
- unwanted baggage,
- wrong functional association,
- strong cultural association but poor project fit,
- needing an article or extra word to work,
- or a surprising secondary interpretation.

Do not treat these reactions as noise.

Examples of useful signals:

- "I immediately thought Marvel when I saw Tesseract."
- "Grid only works as The Grid."
- "Jarvis is great, but it feels like an AI name rather than this project."
- "Keymaker keeps getting stronger the more we compare it."

## Phase 7 — Run a Second Exploration Pass

Use the reaction signals to explore adjacent cultural and conceptual territory.

Do not simply generate synonyms or variants of the current favorite.

A strong candidate becomes an anchor for comparison, not a reason to stop discovery.

## Phase 8 — Evaluate Survivors

Evaluate promising candidates qualitatively across independent dimensions.

### Functional Alignment

Does the concept actually behave like the project?

### Cultural Landing

Does the token spontaneously evoke its source, function, or cultural meaning?

### Personal Recognition

Does it land for the user specifically?

### Visual Identity

Does the word look and sound like a durable project name?

### Independence

Can the token stand alone?

Prefer:
- `keymaker`

Be cautious with tokens whose meaning depends on an article or phrase:
- "The Grid" rather than `grid`

### Longevity

Does the name represent the enduring responsibility rather than the current implementation?

### Semantic Baggage

Does it carry unwanted meanings, negative associations, or a conflicting primary interpretation?

### Accidental Reinforcement

Does the candidate gain strength from multiple independent associations that were not artificially engineered?

This is a particularly strong signal.

Example:

- a role in a film opens many doors,
- the project had already been described as "one brain, many doors,"
- APIs independently use keys,
- canonical identifiers behave like keys into downstream systems.

When several independent signals converge naturally, the candidate is stronger than one supported only by a clever explanation.

## Phase 9 — Build a Survivor Board

When useful, finish an exploration pass with a compact survivor board.

Example:

`candidate-one` · `candidate-two` · `candidate-three`

Do not declare a winner unless:

- the user asks to converge,
- the evidence is unusually strong,
- or the naming process has clearly reached decision stage.

## Anti-Patterns

Do not default to literal compound names such as:

- media-hub
- data-core
- project-manager
- unified-service
- smart-tool

Do not assume metaphor is always best.

Do not assume cultural naming is always best.

Do not choose a word merely because it sounds impressive.

Do not invent a functional justification after selecting a cool-sounding name.

Do not overfit to the current technology stack.

Do not encode provider names into the project identity unless the project is intentionally provider-specific.

Do not prematurely narrow after the first strong candidate.

Do not confuse cultural popularity with personal recognition.

Do not force one-word naming when the project genuinely requires something else, but prefer concise independent tokens when possible.

Do not repeatedly reuse examples from this skill as candidate defaults.

## Output Contract

A full run should generally contain:

1. **Project distillation**  
   A concise explanation of the enduring responsibility.

2. **Capability verbs**  
   The conceptual actions implied by the project.

3. **Discovery field**  
   A broad candidate set with source, token, and explanation.

4. **Reaction interpretation**  
   What the user's responses reveal about the naming criteria.

5. **Second-pass exploration**  
   New candidates based on the discovered criteria.

6. **Survivor board**  
   The strongest remaining candidates without forced convergence.

7. **Decision rationale**  
   Only when the user is ready to choose.

## Repo Naming Normalization

When the final name will be used as a repo:

- prefer lowercase,
- preserve the semantic identity of the chosen name,
- use hyphens only when the name genuinely contains multiple words,
- avoid implementation suffixes unless required,
- and do not dilute a strong project name with unnecessary descriptors.

Examples:

- `keymaker`
- `project-name-discovery`
- `deep-thought` only if the phrase genuinely requires two words

## Validation

A successful run should not merely produce names.

It should make the user feel that the surviving names are understandable consequences of the project's identity.

The strongest outcome is when the user independently notices the same alignment the skill identified.

See `references/naming-examples.md` for a worked example of the method.
