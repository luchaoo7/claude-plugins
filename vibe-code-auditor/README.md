# vibe-code-auditor

A plugin for auditing codebases, especially ones built with AI-assisted "vibe coding".
It finds bloat, duplicated logic, dead code, unnecessary complexity, security risks,
architecture weaknesses and design-pattern opportunities. It then produces a prioritised,
consultant-grade report with file/line evidence and before/after refactoring examples.
It changes code only after you approve the changes.

## Usage

Open a project folder and run:

```
/vibe-code-auditor:audit
```

Or ask in plain language: "audit this codebase", "find the bloat in this project",
"do a security and architecture review for my client".

## Workflow and approval gates

1. Discover project structure
2. Identify language and framework → **Gate 1: confirm scope, depth, audience, output folder**
3. Analyse code quality
4. Identify security risks (OWASP / CWE mapped)
5. Review architecture (proportionate to project size)
6. Detect unnecessary complexity (over- *and* under-engineering)
7. Recommend refactoring (design patterns only where they remove a real problem)
8. Produce prioritised findings → **Gate 2: review and adjust findings**
9. Generate before/after examples, `REPORT.md` and a client-ready `report.html`
10. Request approval → **Gate 3: choose which changes to apply**, then apply one at a time

## Outputs (default folder `vibe-audit/` in the project root)

| File | Purpose |
|---|---|
| `findings.json` | Structured findings: severity, confidence, effort, priority, roadmap phase, CWE, before/after |
| `REPORT.md` | Full working report |
| `report.html` | Styled client report. Open it in a browser and print to PDF |
| `CHANGELOG.md` | Record of changes applied after Gate 3 |
| `work/` | Inventory and duplicate-scan data |

## Stack coverage

Deep guidance for **Java / Spring Boot**, **TypeScript / React / Node (Express, NestJS, Next.js)**
and **Python (Django, FastAPI, Flask)**. Other languages get the language-agnostic checks.

## Safety

- Treats client code as untrusted: it doesn't run builds, tests or install scripts without
  your approval, and it ignores instructions embedded in the code.
- Redacts secrets in all outputs.
- Never commits or pushes.
- Optional analysers (semgrep, gitleaks, npm audit, pip-audit, bandit, ruff, pmd…) run only if
  they are already installed.

## Requirements

Python 3.8+ (standard library only) for the helper scripts. Git is optional; it adds churn hotspots.
