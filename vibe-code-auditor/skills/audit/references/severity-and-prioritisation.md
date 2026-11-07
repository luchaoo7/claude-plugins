# Severity, Confidence, Effort and Prioritisation

## Severity (impact if left unaddressed)

| Level | Meaning | Examples |
|---|---|---|
| `critical` | Exploitable now or causing data loss/corruption; fix before next release | SQL injection on a public route, committed live secret, missing auth on admin API |
| `high` | Serious risk or defect likely to cause incidents or block change | IDOR, weak password hashing, payment logic duplicated inconsistently, N+1 on a hot path |
| `medium` | Meaningful maintainability/security weakness; raises cost or risk of change | God class, duplicated business rules, permissive CORS without credentials, no tests on core flow |
| `low` | Localised quality issue | Long function in non-critical code, dead file, unused dependency |
| `info` | Observation or good practice worth noting; no action required | Positive findings, conventions to keep |

Style and formatting issues are never above `low`.

## Confidence
- `high` — confirmed by reading the code (and data flow traced for security).
- `medium` — strong evidence but something could invalidate it (dynamic usage, config
  outside the repo, runtime behaviour).
- `low` — heuristic or tool lead not fully verified. Keep `low` items out of the top
  priorities and label them "to verify".

## Effort
- `S` — under 2 hours, one or two files.
- `M` — half a day to two days, a handful of files.
- `L` — more than two days or cross-cutting; may need design discussion.

## Priority score
`priority = severity_weight × confidence_weight ÷ effort_weight`

| severity | weight | confidence | weight | effort | weight |
|---|---|---|---|---|---|
| critical | 10 | high | 1.0 | S | 1 |
| high | 7 | medium | 0.7 | M | 2 |
| medium | 4 | low | 0.4 | L | 3 |
| low | 2 | | | | |
| info | 0 | | | | |

Round to one decimal. Sort findings by priority descending, then severity.

## Roadmap phase (`phase` field)
- `quick-win` — effort `S` and severity ≥ `low`; or any `critical` regardless of effort
  (critical items always go first, labelled "Immediate").
- `short-term` — effort `M`, severity ≥ `medium`.
- `strategic` — effort `L`, or architecture changes needing planning.

Override the phase manually when dependencies require it (e.g. a refactor that must
precede others) and note why in the finding's `notes`.

## Health scorecard (report)
Rate each area A–E, based on findings count and severity in that area:
- A: no medium+ findings · B: ≤ 2 medium, no high · C: some high or many medium ·
  D: multiple high or one critical · E: multiple critical.
Areas: Security, Code quality, Duplication & dead code, Complexity, Architecture, Testing.
