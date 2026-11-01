---
name: project-discovery
description: Run a phase-gated discovery-to-delivery workflow for a new software project, producing PRD, MVP scope, a lightweight MVP-focused TRD, UX (user flows and low-fidelity wireframes), design system, database schema, an optional low-level design for the complex parts and an optional stakeholder HLD summary as Markdown files in /docs, with a DECISIONS.md log and requirement traceability. Use this whenever someone wants to plan, scope, spec or kick off an app, product, feature set or side project before coding — even if they only say "help me plan my app", "I have an idea for…", "write a PRD", "what should v1 include", "design the database for my idea" or "where do I start" — and whenever they want to resume or change a project that already has these docs.
---

# Project Discovery (phase-gated)

This skill takes a project from a raw idea to a set of approved planning documents a developer can build from. It exists because most projects go wrong before the first line of code: requirements stay vague, tech choices are made on vibes, v1 quietly grows, and nobody can later say why something was decided. The workflow fixes that with three mechanisms:

1. **Hard phase gates** — each document must be explicitly approved before the next phase starts.
2. **A decision log** — every material choice is recorded in `docs/DECISIONS.md`, whether the developer chose it or accepted (or overrode) a recommendation.
3. **Traceability** — every requirement gets an ID, and everything downstream (components, stories, screens, tables) points back to one. Anything that can't is either justified or cut.

The developer stays accountable: Claude recommends, explains trade-offs and writes the documents, but the developer makes and owns every decision.

## The phases

| # | Phase | Output file | Answers |
|---|-------|-------------|---------|
| 0 | Discovery | `docs/DISCOVERY.md` | What problem, for whom, how big, what constraints |
| 1 | PRD | `docs/PRD.md` | What the product must do and why (requirements with IDs) |
| 2 | MVP Scope | `docs/MVP.md` | What v1 is, what it explicitly is not, how creep is handled |
| 3 | TRD (lightweight) | `docs/TRD.md` | Just enough technical design to build v1: stack, architecture, high-level data model, API contracts, auth, payments, security, key constraints |
| 4 | UX: User Flow & Wireframes | `docs/USER_FLOW.md` | Every screen, every click, every journey, and a low-fidelity wireframe of each key screen |
| 5 | Design System | `docs/DESIGN_SYSTEM.md` | Fonts, colours, spacing, buttons, components |
| 6 | Database Schema | `docs/SCHEMA.md` | Tables, relationships, constraints, permissions |
| 7 | LLD — complex parts *(optional)* | `docs/LLD.md` | How the hardest parts work inside: sequence diagrams, state machines, rules and edge cases, module structure |

On request, at any point after the TRD is approved: `docs/HLD.md` — a stakeholder-facing high-level design summary assembled from approved documents (not a phase, no new decisions).

Running alongside every phase: `docs/DECISIONS.md`, `docs/TRACEABILITY.md` and `docs/STATUS.md` (which doubles as the handoff file).

**Projects without a user interface.** Phases 4 and 5 assume screens. For a pure API, backend service or library, mark both `not applicable` in STATUS.md with a one-line reason (no decision entry needed — it's a fact, not a choice). For a CLI tool, keep Phase 4 but adapt it: commands instead of screens, sample terminal output instead of wireframes; mark Phase 5 `not applicable` unless the CLI has a styled interface.

Templates for every file are in `references/templates.md`. Read the template for a phase just before drafting that phase's document, not all at once up front.

Follow the order above. Each phase builds on approved earlier ones (the TRD shouldn't design for features v1 won't ship; the schema can't be designed before flows show what data the screens need).

**Why MVP comes before the TRD, and why the TRD is lightweight.** The technical design should serve what v1 actually has to do, not the whole PRD wishlist. Designing infrastructure for features that might never ship wastes time and quietly pulls them back into scope. So the TRD in this workflow is deliberately *lightweight*: enough architecture, stack, data model, API contracts, security and constraints to start building v1 with confidence — not a comprehensive design document. It grows later: once building starts, the TRD is expanded and maintained as implementation teaches you things (see "After the gates").

**Skipping is allowed, but never silent.** If the developer wants to jump ahead, say in a sentence or two what the skipped phase would have settled, and offer as options: do a quick version of the skipped phase first (recommended), or skip it. If they've already made the decision clearly ("I've decided, skip it"), don't re-ask — state the main risk in one line and proceed. If they choose to skip, that's their call: log a decision (type `risk-acceptance`, origin `developer`) naming the phase skipped and the specific risks, mark the phase `skipped` in STATUS.md, and in the next document list the assumptions you had to make in place of the skipped work, so they're visible and can be revisited. A skipped phase can be done later; it then goes through its gate like any other.

## Starting or resuming

First look for an existing `docs/` folder (in the working directory, or files the user attached).

- **STATUS.md exists** → read it, DECISIONS.md and the latest approved docs, then summarise in two or three lines where the project stands and continue from the current phase. Don't restart discovery or re-ask settled questions.
- **Some docs but no STATUS.md** → treat them as drafts: read them, reconstruct STATUS.md, and ask the developer to confirm which are actually approved.
- **Nothing exists** → start Phase 0.

If there is no filesystem (a plain chat), produce each document in the conversation instead and keep the same structure; tell the developer once that the files are meant to live in `/docs` in their repo.

## How to ask questions

Ask questions as selectable options, not open text boxes. Use the AskUserQuestion tool when it's available (up to 4 questions per call, 2–4 options each, "Other" is always available automatically). Without it, write numbered options the developer can answer with a letter or number.

- Put the recommended option first and mark it "(Recommended)" — but only when there's a genuine reason to prefer it, and say the reason in the option description.
- Ask only what changes the document. Batch related questions; don't drip-feed one question per turn.
- Never invent an answer for something only the developer knows (users, budget, deadlines, business rules). For technical choices, recommend; for product facts, ask.
- If an answer contradicts an earlier approved decision, point at the decision ID and ask whether to supersede it.

## Standard phase response format

Use the same shape for the main message of every phase, so the developer always knows where they are and what's needed from them. Leave out a heading that would be empty.

- **Current phase** — number and name
- **Objective** — one line
- **What we already know** — the approved context this phase builds on (brief; point at docs and decision IDs rather than repeating them)
- **Questions** — only unanswered ones that matter now, as options
- **Recommendations** — suggested choices with reasons
- **Deliverables** — the documents written or updated
- **Validation** — exit-checklist results, orphans and gaps, and anything not yet verified
- **Decisions required** — gate approval and any open decisions, with IDs
- **Next step** — what happens after approval

If questions must be answered before the deliverable can be written, stop after the Questions (and any Recommendations). Don't draft a document on invented answers just to fill the format.

## Proportionality

Size the documents to the project. A single-user offline to-do app does not need a payments section, an RBAC matrix or twelve components. In Phase 0, classify the project and record the tier in DISCOVERY.md:

- **Small** — one user or a handful, no money, no sensitive data, one platform. Short docs; sections that don't apply say `N/A — <one-line reason>` rather than disappearing (so it's visible they were considered).
- **Medium** — real users, accounts, some integrations or payments.
- **Large** — multiple roles, regulated or sensitive data, money movement, multiple clients/platforms, teams.

Every section in a template is a prompt to consider something, not a quota to fill. Padding a document makes it harder to review and weakens the gate.

### Simplicity guardrails

Prefer the simplest design that meets the approved requirements, and make anything more complex earn its place with a requirement ID. Without a specific reason, don't recommend:

- microservices over a modular monolith
- Kubernetes or self-managed clusters over simpler hosting (a PaaS or a single VM)
- event-driven or queue-based processing where a synchronous call is enough
- more than one database
- self-built authentication infrastructure where a framework's built-in auth or a managed provider fits
- abstraction layers, plugin systems or "future-proofing" for features not in v1

When a complex option is genuinely justified, say which requirement drives it and log the decision. Keep three categories separate in every technical discussion: **MVP requirements** (needed for v1), **production-readiness** (needed before real users depend on it: backups, monitoring, rate limits), and **future enhancements** (Later list).

## Phase gates (hard)

At the end of each phase:

1. Write the document to `docs/`.
2. Run the phase's exit checklist (in `references/templates.md`) against it yourself and fix anything that fails before showing it. Mention any item you deliberately marked N/A.
3. Present a short summary: what the document says in 4–8 bullets, the decisions made in this phase (with IDs), and any open questions.
4. Ask for the gate decision as options: **Approve** / **Request changes** / **Discuss a section first**.

Only an explicit approval passes the gate. "Looks good", "fine" or "ok" said about the document counts; silence, a change of subject, or "let's keep going" with an unresolved open question does not — ask again. On approval:

- Set the document's header status to `Approved` with the date.
- Update STATUS.md (phase → `approved`, next phase → `in progress`).
- Log a gate entry in DECISIONS.md (`type: gate`).

Then start the next phase in the same turn.

**Open questions block the gate.** A document can be approved with an open question only if the developer explicitly accepts it as a known risk; record that acceptance in DECISIONS.md.

### Changing an approved document

Approved docs are not frozen, but changes are deliberate. When something needs to change in an earlier phase:

1. Say which document and which IDs are affected, and which later documents ripple (use TRACEABILITY.md to find them).
2. Get the developer's choice.
3. Log a new decision that supersedes the old one (`supersedes: D-0xx`), never edit history out of DECISIONS.md.
4. Update the affected documents, bump their version, and set them back to `Approved` only after the developer confirms the change.

Treat new feature ideas after Phase 2 as change requests against MVP.md: the default answer is "add to the Later list", unless the developer decides to swap something out of v1. Log either way.

## The decision log

Every material choice goes in `docs/DECISIONS.md` — product choices, technical choices, scope cuts, gate approvals, skipped phases, accepted risks. "Material" means: if someone asked in three months "why is it like this?", the answer would matter. Naming a CSS variable isn't material; choosing PostgreSQL over SQLite is.

Each entry records its **origin** honestly:

- `developer` — the developer chose it without a recommendation, or chose an option Claude didn't recommend.
- `recommendation-accepted` — Claude recommended it and the developer agreed.
- `recommendation-overridden` — Claude recommended X, the developer chose Y. Record both and the developer's reason.

Always record the options considered and the rationale in the developer's terms. When a recommendation is accepted with a bare "ok", write the rationale Claude gave and note it was accepted without further comment — don't invent reasons the developer didn't give. The owner is always the developer: they made the call, even when they took the recommendation.

IDs are sequential and never reused: `D-001`, `D-002`, …

## Traceability

IDs make every later artefact answerable to a requirement:

- PRD: functional requirements `FR-01…`, non-functional `NFR-01…`, user roles `R-…`.
- MVP: user stories `US-…`, each linked to FR IDs; out-of-scope items `OUT-…`.
- TRD: components/services `C-…`, API endpoints `API-…`, entities `E-…`, each listing the US (and FR/NFR) IDs it serves. Anything serving only an out-of-scope item is an orphan.
- UX: screens `S-…` (each with its wireframe), journeys `J-…`, linked to US IDs.
- Design System: components `UI-…`, linked to the screens that use them.
- Schema: tables `T-…`, linked to the FR/US IDs that need the data.
- LLD: designed parts `LLD-…`, each linked to the US IDs and components (`C-…`) it details.

Maintain `docs/TRACEABILITY.md` as a matrix (requirement → downstream IDs), updating it at the end of every phase. Before each gate, check for:

- **Orphans** — a downstream item with no requirement behind it (a table no story needs, a screen no journey reaches, an endpoint nothing calls). Either link it, justify it in DECISIONS.md, or cut it. Orphans are where feature creep hides.
- **Gaps** — an in-scope requirement with nothing downstream covering it yet (expected only for phases not reached).

Report orphans and gaps in the gate summary.

## STATUS.md (status and handoff)

STATUS.md lets anyone — the developer next month, another developer, or a fresh AI session — pick the project up without losing context. Keep it short and current; it points to the other docs rather than repeating them. It holds:

- **Project summary** — two or three lines, plus tier
- **Current phase and next action**
- **Phase table** — status and approval date per phase. Statuses: `not started`, `in progress`, `awaiting input` (waiting on the developer's answers), `awaiting approval`, `approved`, `blocked` (with the reason and what unblocks it), `skipped` (with decision ID), `not applicable` (with reason), and `expanding` (the TRD after the build starts)
- **Approved scope** — one line pointing at MVP.md and its version
- **Stack** — one line once the TRD is approved
- **Key decisions** — the handful of IDs that most shape the project
- **Accepted risks and open questions**
- **Document index** — each doc with its version

Update it whenever a phase changes state. Never mark something approved, or a task done, because it was planned — only when it actually happened.

## Phase notes

Short guidance on what each phase is for; the templates hold the structure.

**0 — Discovery.** Understand the idea before defining anything. If the developer hasn't described it yet, the first message simply asks what they want to build and what problem it solves — no technical questions. Then cover, only where it matters for this project: who uses it and roughly how many; the problem, current workaround and pain points; project type (personal, internal tool, commercial product, other); new build or extending an existing system; platforms (web, mobile, desktop, API, CLI); existing systems and integrations; timeline and budget; the developer's skills and preferred technologies; legal, regulatory, security or data requirements; maturity (prototype / MVP / production); what success looks like. One or two rounds of option questions is usually enough. The deliverable is a discovery summary separating **known facts**, **assumptions**, **constraints** and **open questions**, plus the tier. It's a gate too.

**1 — PRD.** Product-level, no technology. Problem statement, target users and short personas, goals and non-goals, roles, core use cases, functional requirements written as observable behaviour, NFRs, business rules, external integrations and dependencies, data sensitivity, accessibility and compliance needs, explicit exclusions, measurable success criteria, assumptions. Ask the developer about rules and edge cases (what happens on delete, duplicates, expiry); don't guess them.

Challenge vague requirements instead of copying them: if the developer says "it should be fast" or "secure", ask what matters and offer measurable targets as options ("search results in under 1.5 s on 4G"). And separate requirements from solutions — "users are told when their wash finishes" is a requirement; "send a push notification via Firebase" is a solution that belongs in the TRD.

**2 — MVP Scope.** The v1 line, decided before any technical design. In-scope user stories with acceptance criteria, an explicit Out of scope list (with the reason each is out), a Later list, the core assumptions v1 is meant to validate, a Definition of Done, and a thin-slice build order grouped into milestones with dependencies and a rough effort estimate. Before proposing the cut, ask what the first release is for (validation, demonstration, internal adoption or paying customers), whether there's a target date, and how many people will build it — the answers change how small v1 should be. Classify every PRD requirement as Must / Should / Could / Out of scope for v1. Estimates are ranges with their assumptions and the biggest uncertainty stated ("3–5 weeks part-time, assuming photo storage uses a managed service"); never a single confident number. Push for the smallest v1 that tests the core value; if the in-scope list covers most of the PRD, say so and suggest cuts. Sanity-check the size against the Discovery timeline. This document is the creep guard — make it concrete enough to say "no" with. Don't make technology choices here; if a story's feasibility is genuinely uncertain, note it as a risk for the TRD to resolve.

**3 — TRD (lightweight, MVP-scoped).** Design for the in-scope stories only. Before recommending, check you know the inputs that drive the choice — preferred languages and existing skills, hosting or cloud preference, budget, expected scale, availability expectations, data residency, existing infrastructure, and who will maintain it — and ask only for what Discovery didn't already settle. Then offer 2–3 coherent stack options suited to the tier, the developer's skills and the constraints, with trade-offs, and recommend one, following the simplicity guardrails above. Then cover, briefly: architecture, high-level data model (entities and relationships — full schema is Phase 6), API contracts for v1 endpoints, authentication and authorisation, payments (or N/A), integrations, hosting/deployment, security requirements, key technical constraints, and testing approach. For out-of-scope and Later items, don't design them — only note a constraint where a v1 choice would make them expensive later ("one-way door" decisions), in a short Future considerations section. Each significant choice is a decision entry. If a section would run past a page for a Small or Medium project, it's probably more than v1 needs.

**4 — UX: User Flow & Wireframes.** Design the experience before anyone builds an interface. Start by asking what Discovery and the PRD haven't settled: target devices (mobile-first, desktop-first, both), navigation preference, accessibility needs beyond the WCAG AA baseline, existing branding, UI references they like, and desired complexity (minimal and fast vs feature-rich). Then produce:

- **Journey maps** for each primary journey — the user's goal, the steps, and where they might get stuck or drop off
- **Screen inventory** with every screen's purpose and its empty, loading, error and success states
- **Screen-to-screen flows** as Mermaid flowcharts, including every click that changes state
- **Navigation structure**
- **Low-fidelity ASCII wireframes** for each key screen (every screen on a primary journey; a simple dialog can be described in a line). Wireframes show layout, hierarchy and content, not visual style. They live in USER_FLOW.md so they diff cleanly in git and need no tools; the template shows the format.

Validate against the MVP: every in-scope story is reachable through a journey, every screen serves an in-scope story, and nothing on a wireframe belongs to an out-of-scope item.

**5 — Design System.** Tokens (colour with contrast-checked pairs, typography scale, spacing, radii, shadows, breakpoints), component specs with states (default, hover, focus, disabled, error, loading), accessibility rules, light/dark if needed. Derive the component list from the screens and wireframes in USER_FLOW.md rather than a generic kit. If the developer has existing branding, build the tokens from it; otherwise offer 2–3 visual directions as options before writing tokens, informed by the UI references and desired complexity gathered in Phase 4.

**6 — Database Schema.** Tables with columns, types, nullability, defaults, keys, indexes, constraints; relationships with cardinality (Mermaid ER diagram); permissions per role (who can read/create/update/delete which rows — row-level rules where it matters); data retention and deletion behaviour that matches the PRD's business rules; migration and seed approach. Use the database chosen in the TRD and refine its high-level data model; if the schema contradicts the TRD's data model, update the TRD and log it.

**7 — LLD for the complex parts (optional).** The approved docs say *what* v1 does and *which* parts exist; the LLD says *how* the hardest parts work inside, which is where projects most often break. It's optional and selective by design: a full LLD for every component written before any code goes stale fast, and simple CRUD parts don't need one.

After the Schema gate, offer it as options, with the recommendation based on the project:
- **LLD for the complex parts only** — recommended for Medium/Large tiers, or any project with significant domain logic (bookings and overlaps, scheduling, money, multi-step approvals, external callbacks, concurrency)
- **Full LLD for every component** — rarely worth it before building; say why
- **No LLD now; design each slice at build time** — the natural default for Small projects with simple logic

If the developer picks the selective option, propose which parts qualify and why (as a multi-select), using the stories, components and business rules — e.g. "the loan lifecycle: state changes, date-overlap checks and address reveal" rather than "the listings CRUD". For each chosen part, cover: purpose and the stories/components it traces to; module or package structure and the main classes or interfaces with responsibilities; sequence diagrams (Mermaid) for its critical flows, including failure paths; a state machine (Mermaid) where the part has a lifecycle; rules and validation; edge cases, error handling and retries; idempotency and concurrency (what happens on double-submit or two simultaneous requests); and a worked example with realistic sample data. Use the stack chosen in the TRD. If the LLD reveals something the TRD or schema got wrong, use the change process — don't silently diverge. It's gated like any other phase.

Choosing "no LLD" is logged as a decision (origin as usual) and the phase marked `skipped`; that's a normal choice, not a risk, unless the project has complex logic and you recommended otherwise — then say so in the entry.

**HLD summary (on request).** Some readers expect a High Level Design: a team, a client, a manager, an interviewer. In this workflow the lightweight TRD already *is* the high-level design, so don't create a second one that can drift. When the developer wants an HLD — or when offering the LLD, ask once whether one would help (only mention it, don't push it) — assemble `docs/HLD.md` from approved content: overview and goals (PRD), v1 scope (MVP), architecture diagram, components, stack, integrations, deployment and security approach (TRD), key decisions (DECISIONS.md), and data model summary (TRD/Schema). Write it for a reader who hasn't seen the other docs, link to the sources, and mark it `generated from` with the versions it was built from. It introduces no new decisions — if writing it exposes a gap, raise it as a change to the source doc. Regenerate it when the sources change, rather than editing it by hand.

## After the gates

After Phase 6 is approved (and Phase 7, if chosen), give a short close-out: the docs produced, the count of decisions, any accepted risks, and the first build slice from MVP.md as the natural next step. Coding is outside this skill (scaffolding, implementation, testing and deployment are meant for a separate build skill that starts from these approved docs), but the build should follow MVP.md's slices. Make sure STATUS.md reads as a complete handoff before closing out.

When the developer returns during or after the build, the TRD moves into **expand and maintain** mode:

- Record implementation decisions and anything the build taught (a library swapped, a constraint discovered) as decision entries, and update the TRD to match. Use the change process above; these are expected, not failures.
- Newly discovered requirements go through the PRD/MVP first (change request), then into the TRD.
- Once v1 is validated, add the sections that were deliberately left out: scaling, reliability, observability depth, and design for the next features. Bump the TRD's major version and mark the status in STATUS.md as `expanding`.
