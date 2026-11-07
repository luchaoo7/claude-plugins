# Project Discovery

A Claude plugin that takes a software project from a raw idea to a set of approved planning documents you can build from — before any code is written. It also works on projects that already have code, documenting what exists and planning new work on top.

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

From your terminal, without starting a session:

```
claude plugin marketplace add luchaoo7/claude-plugins
claude plugin install project-discovery@luchaoo7-plugins
```

Or inside a session:

```
/plugin marketplace add luchaoo7/claude-plugins
/plugin install project-discovery@luchaoo7-plugins
/reload-plugins
```

### Claude desktop app / claude.ai

Add this repository as a plugin marketplace from the plugin settings, or download the plugin folder and upload it.

## Usage

### Starting a project

Open a session in your project's repo and describe what you want to plan. The skill triggers on things like:

- "Help me plan my app"
- "I have an idea for a booking tool for barbers"
- "Write a PRD for…"
- "What should v1 include?"
- "Design the database for my idea"

In Claude Code you can also start it directly with `/project-discovery:plan`.

### Using it on an existing project

There's no separate command. Open a session in the project's repo and run `/project-discovery:plan`, or just say something like "document this codebase" or "plan a new feature for this app". The skill sees the code and switches to existing-project mode on its own. Claude reads the code first, then asks whether you want to document what exists, plan new work on it, or both, unless your message already said which.

- **Same documents, same gates** — but they record the system as it is, and approving one means it's accurate.
- **Claude only writes to `docs/`** — it doesn't change your code, and it won't overwrite existing files in `docs/` it didn't write. It doesn't open secrets or connect to live databases.
- **Clear sources** — statements about the current system are labelled `[code]`, `[inferred]` or `[confirmed]`, and existing choices are logged with `Rationale: unknown` if nobody knows why they were made.
- **Findings, not fixes** — problems the survey turns up, such as dead code or a documented feature that isn't built, are recorded for you to fix later or accept.

### Moving through the phases

Claude asks a few questions, drafts the phase's document in `docs/`, then asks for a gate decision:

- **Approve** — the document is marked approved, the decision is logged and the next phase starts.
- **Request changes** — Claude revises the document and asks again.
- **Discuss a section first** — talk it through before deciding.

Open questions block a gate unless you explicitly accept them as a known risk.

### Skipping a phase

You can ask to skip a phase. Claude explains what it would have settled, then logs the decision and the risks in `docs/DECISIONS.md` and lists the assumptions it had to make in the next document. For projects without a user interface, the flows and design system phases are adapted or marked not applicable.

### Changing an approved document

Ask for the change at any point. Claude handles it as a deliberate change: the affected documents are updated, their version is bumped, and they return to approved only after you confirm.

### Resuming later

Open a session in a repo that already has a `docs/STATUS.md` and ask to continue — it picks up from the current phase without re-asking settled questions.

### After the last gate

You get a short close-out covering the documents produced, the decisions made, any accepted risks and the first build slice from `MVP.md`. Writing the code is outside this plugin.

## Roadmap

- **v0.3** — companion build skill: scaffold, implement, test and deploy from the approved docs, following the MVP's build slices.

## Licence

MIT
