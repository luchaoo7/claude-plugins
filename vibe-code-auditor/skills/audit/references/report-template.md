# REPORT.md Template

Write for the audience chosen at Gate 1. For `client`, lead with business impact and keep
jargon out of the executive summary; technical detail lives in the findings section.
For `developer`, be terse and code-first. For `both`, keep the executive summary plain and
the rest technical.

Paraphrase, don't pad. Every claim traces to a finding ID.

```markdown
# Code Audit Report — <Project>
Prepared for <Client> by <Consultant> · <Date> · Audit depth: <depth>

## 1. Executive summary
<2–4 sentences: overall state, the most serious risk, the headline recommendation.>

**Overall health:** <one line>  
**Immediate actions:** <1–3 bullets with finding IDs>

## 2. Scope and method
- Codebase: <stacks, LOC, files>
- In scope / out of scope
- Method: static review against code-quality, security (OWASP/CWE), architecture and
  design-pattern checklists; tools used (list only those actually run)
- Limitations: <e.g. no runtime testing, config outside repo not reviewed>

## 3. Health scorecard
| Area | Grade | Key driver |
|---|---|---|

## 4. Findings summary
Counts by severity × category table, then the top 10 by priority:
| ID | Title | Severity | Effort | Location |

## 5. Architecture assessment
As-is description (optional Mermaid diagram), weaknesses, recommended target and moves.

## 6. Refactoring themes
For each theme: problem, linked finding IDs, proposed approach, before/after excerpt.

## 7. Prioritised remediation roadmap
### Immediate (critical)
### Quick wins
### Short term
### Strategic
Each line: ID — action — effort.

## 8. Detailed findings
Grouped by category, ordered by priority. For each:
### VCA-001 · <Title>
**Severity:** critical · **Confidence:** high · **Effort:** S · **CWE:** CWE-89  
**Location:** `path/File.java:42-47` (`findByName`)

**What:** …  
**Why it matters:** …  
**Recommendation:** …

<before code block> <after code block>

## 9. Positive observations
What the codebase does well (keep it honest and specific).

## Appendix
- Tool output summaries
- Glossary (for client audience)
```
