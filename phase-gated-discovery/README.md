# Phase-Gated Discovery

A Claude plugin that takes a software project from a raw idea to a set of approved planning documents you can build from — before any code is written.

Most projects go wrong early: vague requirements, tech choices made on vibes, a v1 that quietly grows, and nobody able to say later why something was decided. This plugin fixes that with three mechanisms:

1. **Hard phase gates** — each document must be explicitly approved before the next phase starts.
2. **A decision log** — every material choice is recorded in `docs/DECISIONS.md`, including whether you chose it, accepted a recommendation, or overrode one.
3. **Traceability** — every requirement gets an ID, and everything downstream (stories, components, screens, tables) points back to one. Anything that can't is justified or cut.

Claude recommends and writes; you decide and own every decision.

## What it produces

All output is Markdown in your repo's `docs/` folder:

| # | Phase | File |
|---|-------|------|
| 0 | Discovery | `DISCOVERY.md` |
| 1 | Product requirements | `PRD.md` |
| 2 | MVP scope | `MVP.md` |
| 3 | Technical requirements (lightweight, MVP-scoped) | `TRD.md` |
| 4 | User flows and ASCII wireframes | `USER_FLOW.md` |
| 5 | Design system | `DESIGN_SYSTEM.md` |
| 6 | Database schema | `SCHEMA.md` |
| 7 | Low-level design for complex parts *(optional)* | `LLD.md` |
| – | Stakeholder high-level design *(on request)* | `HLD.md` |

Maintained throughout: `DECISIONS.md`, `TRACEABILITY.md` and `STATUS.md` (a handoff file so any person or AI session can resume).

Documents are sized to the project (Small / Medium / Large tier), and simplicity guardrails stop over-engineering — no microservices or Kubernetes without a requirement that needs them.

## Installation

### Claude Code

```
/plugin marketplace add luchaoo7/claude-plugins
/plugin install phase-gated-discovery@luchaoo7-plugins
```

### Claude desktop app / claude.ai

Add this repository as a plugin marketplace from the plugin settings, or download the plugin folder and upload it.

## Usage

Just describe what you want to plan. The skill triggers on things like:

- "Help me plan my app"
- "I have an idea for a booking tool for barbers"
- "Write a PRD for…"
- "What should v1 include?"
- "Design the database for my idea"

To resume, open a session in a repo that already has a `docs/STATUS.md` and ask to continue — it picks up from the current phase without re-asking settled questions.

## Roadmap

- **v0.2** — companion build skill: scaffold, implement, test and deploy from the approved docs, following the MVP's build slices.

## Licence

MIT
