# codex-config-manager

Codex Config Manager is a headless, deterministic publisher/consumer pipeline for one bounded global Codex configuration: `AGENTS.md` plus dynamically discovered user-managed skills. The Mac Studio is the authoring authority; GitHub carries the validated `latest/` snapshot; the Mac mini consumer is implemented but remains pending real-machine rollout.

The Mac Studio publisher is operational. It checks once per minute, waits for five quiet minutes, then publishes through a path-scoped Git transaction. `skills/.system/**`, `.DS_Store`, and unrelated `.codex` content are never managed.

## Documentation

- [Implementation architecture and operations](docs/10-implementation-architecture-and-operations.md)
- [Mac Studio validation evidence](docs/11-validation-evidence-mac-studio.md)
- [Deferred Mac mini Phase 15 handoff](docs/12-mac-mini-phase-15-handoff.md)
- [Historical implementation plan](docs/03-mode-c-implementation-plan.md)

<!-- BEGIN CODEX CONFIG MANAGER DOWNLOADS -->
## Global AGENTS.md

The global `AGENTS.md` contains guidance intended for the user’s global Codex environment.

- [View the current global - AGENTS.md](latest/AGENTS.md)
- [Download the current global - AGENTS.md](https://raw.githubusercontent.com/YodaSpow/codex-config-manager/main/upload-ready/global-agents.zip)

## Skills

Each download contains one complete user-managed skill.

- [Download chat-handoff](https://raw.githubusercontent.com/YodaSpow/codex-config-manager/main/upload-ready/skills/chat-handoff.zip)
- [Download operational-modes](https://raw.githubusercontent.com/YodaSpow/codex-config-manager/main/upload-ready/skills/operational-modes.zip)
- [Download project-name-discovery](https://raw.githubusercontent.com/YodaSpow/codex-config-manager/main/upload-ready/skills/project-name-discovery.zip)
- [Download semantic-compression](https://raw.githubusercontent.com/YodaSpow/codex-config-manager/main/upload-ready/skills/semantic-compression.zip)
<!-- END CODEX CONFIG MANAGER DOWNLOADS -->
