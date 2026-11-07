# Code Quality Checklist

Use these categories (they map to the `category` field in findings.json).

## Complexity thresholds (guides, not laws)

| Metric | Watch | Report |
|---|---|---|
| Function length | > 50 lines | > 100 lines |
| File length | > 400 lines | > 800 lines |
| Nesting depth | 4 | ≥ 5 |
| Parameters | 5 | ≥ 7 |
| Cyclomatic complexity (approx. branches) | 10 | ≥ 15 |
| Class/component responsibilities | 3 | ≥ 4 unrelated concerns |

Adjust for context: a generated file, a migration, or a long-but-flat config mapping is
not a complexity problem. Report the reason, not just the number.

## `duplication`
- Copy-pasted blocks across files (use `find_duplicates.py`, then confirm by reading).
- Near-duplicates: same logic with renamed variables or slightly different literals.
- Parallel implementations of the same concern: two HTTP clients, three date helpers,
  several validation approaches, duplicated DTO/type definitions front and back.
- Repeated magic values that should be one constant or config entry.

## `dead-code`
- Exported functions/classes with no references (search for the symbol across the repo,
  including dynamic usage: reflection, string-based routing, DI containers, templates).
- Unreachable branches, always-true/false flags, commented-out code blocks.
- Unused dependencies in manifests (search imports for each package).
- Orphaned files: components, pages, endpoints, migrations, assets not referenced anywhere.
- Mark confidence `medium` when dynamic dispatch could hide usage.

## `bloat`
- Code that re-implements the standard library or an existing dependency.
- Multiple libraries for one job (axios + fetch wrapper + got; moment + date-fns + dayjs).
- Excessive defensive checks for impossible states; redundant null checks after validation.
- Over-verbose comments restating code; boilerplate docstrings on trivial functions.
- Giant utility files ("utils.ts", "helpers.py") mixing unrelated concerns.

## `complexity`
- Long functions, deep nesting, boolean-flag parameters that switch behaviour.
- Over-engineering: interfaces with one implementation and no test seam need, abstract
  base classes with one subclass, factories/builders for trivial objects, event buses in
  small apps, wrapper layers that only delegate, configurable "frameworks" used once.

## `maintainability`
- Inconsistent naming, structure or patterns across modules (a strong AI-tool signature).
- Swallowed exceptions / empty catch blocks / `except: pass` / `.catch(() => {})`.
- Mixed responsibilities (I/O + business logic + formatting in one function).
- Hidden global state, mutable singletons, implicit coupling via shared mutable objects.
- Missing or misleading types (`any`, untyped dicts passed everywhere, raw `Object`).
- Hard-coded environment specifics (URLs, ports, file paths, feature flags).

## `testing`
- Critical paths (auth, payments, data writes) with no tests.
- Tests that assert nothing meaningful, snapshot-everything tests, tests mocking the unit
  under test, disabled/skipped tests.
- Test-to-source ratio from inventory as a signal only.

## `performance` (only when evident from code)
- N+1 queries, queries in loops, unbounded result sets, missing pagination.
- Repeated expensive computation in render paths/loops; missing memoisation where obvious.
- Synchronous blocking I/O on request threads / event loop.

## AI-generated code smells

Typical signatures of vibe-coded projects. Each is a lead; confirm before reporting.

1. **Parallel reinvention** — the same helper written several times in different files
   because each prompt session started fresh.
2. **Style drift** — different error-handling, naming, state-management or folder
   conventions between features built at different times.
3. **Phantom abstractions** — layers, interfaces or "services" generated for completeness
   but with one caller.
4. **Placeholder residue** — `TODO: implement`, mock data, `example.com`, hard-coded test
   users, fake API keys, stubbed functions that return constants in production paths.
5. **Hallucinated or unused dependencies** — packages in the manifest never imported,
   or imports of APIs that do not exist in the installed version.
6. **Over-commenting and narrative comments** — "// Now we loop through the users".
7. **Defensive noise** — try/catch around everything, logging and re-throwing at every
   layer, fallback values that hide failures.
8. **Generated-but-abandoned files** — v2/v3/`-new`/`-old`/`copy` files, unused pages.
9. **Security shortcuts** — disabled CSRF, `cors("*")`, `verify=False`, auth checks only
   in the frontend, secrets in `.env` committed to git.
10. **Inconsistent data models** — the same entity shaped differently across API, DB and UI.
