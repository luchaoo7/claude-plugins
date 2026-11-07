# Architecture Review

Category in findings.json: `architecture`.

## 1. Describe what exists (as-is)
Write 5–10 lines for the report covering:
- Deployable units and runtime (monolith, SPA + API, serverless functions, workers).
- Layers/modules actually present and how they depend on each other.
- Data stores, external services, auth provider, background jobs.
- Main request flow for one representative feature, file by file.

Optionally include a Mermaid diagram (`graph LR`) in REPORT.md.

## 2. Size the need (proportionality)
Classify the project before judging it:

| Profile | Typical shape | Appropriate architecture |
|---|---|---|
| Prototype / MVP, 1–3 devs | < 20k LOC, one domain | Modular monolith, simple layering, one DB |
| Growing product, small team | 20k–150k LOC, several domains | Modular monolith with explicit module boundaries; extract only hot spots |
| Multi-team / high scale | > 150k LOC, independent release needs | Service boundaries justified by team or scaling needs |

Recommendations must fit the profile. Recommending more architecture than the profile
needs is a defect in the audit.

## 3. Assess against these questions
1. **Separation of concerns** — is business logic separate from transport (controllers,
   route handlers, React components) and from persistence?
2. **Dependency direction** — do inner layers depend on outer ones (domain importing web
   framework types, utilities importing features)? Any circular imports between modules?
3. **Cohesion** — are files grouped by feature/domain or scattered by technical type with
   features spread across many folders? Either can work; inconsistency is the problem.
4. **Boundaries to the outside** — are external APIs, payment providers, LLM calls, email
   etc. wrapped behind one module each, or called directly from many places?
5. **Data model integrity** — single source of truth for entities and validation? DTOs vs
   entities? Shared types between frontend and backend?
6. **Configuration** — one config mechanism, environment-driven, validated at startup?
7. **Error handling strategy** — consistent, centralised (exception handler, error
   boundary, middleware) or ad hoc everywhere?
8. **State management (frontend)** — one approach, or several competing (context + Redux +
   Zustand + prop drilling)?
9. **Testability** — can core logic be tested without the framework, DB or network?
10. **Operational readiness** — logging, health checks, migrations, secrets handling, CI.

## 4. Common weaknesses to name explicitly
- God module/class/component (`AppService`, `utils`, a 2,000-line `App.tsx`).
- Fat controllers / fat components carrying business rules.
- Anaemic layering: service layer that only forwards to repositories.
- Leaky persistence: ORM entities returned straight from APIs.
- Distributed monolith: "microservices" sharing one DB and deployed together.
- Scattered integration: the same third-party API called from many files.
- Config sprawl: env vars read in dozens of places with different defaults.

## 5. Target architecture
Recommend the nearest sensible target, expressed as a small number of moves
("introduce a `billing` module that owns all Stripe calls"), each linked to findings.
Avoid rewrite recommendations unless the codebase is genuinely unsalvageable; if you do
recommend one, justify it with cited evidence and a strangler-style migration path.
