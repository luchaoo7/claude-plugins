# Design Patterns — When They Help, When They Hurt

Category in findings.json: `design-pattern`.

Recommend a pattern only when **all** are true:
1. A concrete, cited problem exists (duplication, rigid branching, untestable coupling).
2. The pattern removes that problem with less total code or clearly lower change cost.
3. The team/project size can carry the abstraction.

Otherwise prefer: extract function, inline, delete, consolidate module, introduce a plain
data type, or move logic to where its data lives.

## Patterns worth suggesting (with the triggering smell)

| Smell in the code | Pattern | Notes |
|---|---|---|
| Large `if/else`/`switch` on a type or mode, repeated in several places | Strategy (or a map of functions) | In TS/Python a dict/map of functions is often enough — no classes needed |
| Same third-party API called directly from many files | Adapter / Gateway | One module owns the integration; enables mocking and provider swap |
| Complex object construction duplicated with many optional params | Builder or factory function | Prefer named/keyword args or object literals first |
| Many components/services need the same cross-cutting behaviour (auth, logging, retries) | Decorator / middleware / interceptor / HOC / hook | Use the framework's native mechanism (Spring AOP/filters, Express middleware, React hooks, Python decorators) |
| Data access logic mixed into controllers/components | Repository / data-access module | Don't add if the ORM already acts as one and logic is thin |
| Multi-step workflows with copy-pasted skeletons | Template method or a pipeline of functions | Functions composition usually beats inheritance |
| Objects that react to domain events across modules | Observer / domain events | Only if more than one consumer exists today |
| Global mutable singletons used for configuration | Dependency injection / explicit config object | Spring/NestJS/FastAPI `Depends` already provide DI |
| Entity state transitions scattered with flag checks | State machine | Worth it when transitions have rules and bugs exist around them |
| Business rules duplicated between frontend and backend | Shared schema (e.g. Zod/OpenAPI/JSON Schema) | Single source of validation truth |

## Anti-patterns to flag (often introduced by AI tools)
- **Pattern for its own sake** — Factory producing one class; Strategy with one strategy;
  Abstract base + one subclass; Interface + one `Impl` with no test or extension need.
- **Service locator / global registries** hiding dependencies.
- **Deep inheritance hierarchies** where composition would do.
- **Generic repository over an ORM** that already offers the same API.
- **Event bus in a single-process small app** making control flow untraceable.

When removing a pattern is the recommendation, say so plainly: deleting an unneeded
abstraction is a valid, often high-value refactoring.
