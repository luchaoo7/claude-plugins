# findings.json Schema

`render_report.py` reads this file. Keep it valid JSON (UTF-8).

```json
{
  "meta": {
    "project": "Acme Portal",
    "client": "Acme Ltd",            
    "consultant": "Bestman",
    "date": "2026-11-07",
    "audience": "client",              
    "depth": "standard",
    "scope": "Backend (Spring Boot) and web frontend (React). Excluded: generated OpenAPI client, node_modules.",
    "stacks": ["Java 17 / Spring Boot 3.2", "TypeScript / React 18 / Vite"],
    "loc": 48210,
    "files": 612,
    "executive_summary": "2–4 sentences in plain language.",
    "architecture_summary": "As-is architecture in a short paragraph.",
    "scorecard": {"Security": "D", "Code quality": "C", "Duplication & dead code": "C", "Complexity": "B", "Architecture": "C", "Testing": "D"},
    "themes": [
      {"title": "Consolidate API clients", "summary": "Three HTTP clients do the same job.", "finding_ids": ["VCA-004", "VCA-011"]}
    ],
    "limitations": ["Runtime behaviour not observed; no tests were executed."]
  },
  "findings": [
    {
      "id": "VCA-001",
      "title": "SQL query built from request parameter",
      "category": "security",
      "severity": "critical",
      "confidence": "high",
      "effort": "S",
      "priority": 10.0,
      "phase": "quick-win",
      "location": {"file": "src/main/java/com/acme/user/UserRepositoryImpl.java", "start_line": 42, "end_line": 47, "symbol": "findByName"},
      "additional_locations": [],
      "description": "What is wrong, factually.",
      "why_it_matters": "Impact in business and technical terms.",
      "recommendation": "Concrete fix.",
      "before": "exact code from the file (secrets redacted)",
      "after": "proposed code",
      "language": "java",
      "cwe": "CWE-89",
      "owasp": "A03:2021-Injection",
      "references": ["https://cwe.mitre.org/data/definitions/89.html"],
      "status": "open",
      "notes": ""
    }
  ]
}
```

## Field rules
- `id`: `VCA-` + 3-digit sequence, stable across revisions.
- `category`: one of `security`, `architecture`, `design-pattern`, `duplication`,
  `dead-code`, `bloat`, `complexity`, `maintainability`, `testing`, `performance`.
- `severity`: `critical|high|medium|low|info`. `confidence`: `high|medium|low`.
  `effort`: `S|M|L`. `phase`: `quick-win|short-term|strategic`.
- `status`: `open|approved|applied|declined|wont-fix`.
- `location.file` is relative to the project root; lines are 1-based and inclusive.
- `before`/`after` are optional for low/info findings; required for critical/high.
- `additional_locations`: list of `{file, start_line, end_line}` for duplicates etc.
- `audience`: `developer|client|both`.
- Unknown optional fields may be omitted; the renderer tolerates missing values.
