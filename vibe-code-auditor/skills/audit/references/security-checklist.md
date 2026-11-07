# Security Checklist (language-agnostic)

Category in findings.json: `security`. Always fill `cwe` and, where it applies, `owasp`
(OWASP Top 10 2021 IDs, e.g. `A03:2021-Injection`).

## Method
1. List entry points: HTTP routes, message consumers, CLI args, file uploads, webhooks,
   scheduled jobs.
2. For each, trace untrusted input to sinks: DB queries, shell/process calls, file paths,
   template rendering, HTML output, outbound HTTP, deserialisers, eval/reflection.
3. Check authentication and authorisation on every route — not just presence of a login,
   but that each resource access checks ownership/role (IDOR).
4. Review configuration: CORS, CSRF, cookies, headers, TLS, debug flags, error pages.
5. Search for secrets and review dependency risk.

Confidence: `high` only when the source→sink path is confirmed in code. Pattern matches
without a traced path are `medium` or `low`.

## Checks

| Area | What to look for | CWE |
|---|---|---|
| SQL/NoSQL injection | String-built queries, raw queries with interpolation, `$where`, unvalidated sort/filter fields | CWE-89, CWE-943 |
| Command injection | `exec`, `system`, `subprocess(shell=True)`, `Runtime.exec` with input | CWE-78 |
| XSS | `dangerouslySetInnerHTML`, `innerHTML`, `|safe`, `th:utext`, unescaped templates | CWE-79 |
| Path traversal | User input in file paths without normalisation + base-dir check | CWE-22 |
| SSRF | Server fetches user-supplied URLs without allow-list | CWE-918 |
| Broken access control / IDOR | Resource fetched by ID without owner check; admin routes unguarded; auth only in UI | CWE-639, CWE-862, CWE-285 |
| Broken authentication | Home-grown auth, weak password hashing (MD5/SHA1/unsalted), no rate limiting on login, long-lived tokens, JWT `none`/unchecked signature | CWE-287, CWE-916, CWE-307, CWE-347 |
| Session/cookie | Missing `HttpOnly`/`Secure`/`SameSite`, tokens in localStorage for high-risk apps | CWE-614, CWE-1004 |
| CSRF | Disabled CSRF with cookie auth | CWE-352 |
| CORS | `*` with credentials, reflected Origin | CWE-942 |
| Secrets | Keys, tokens, passwords, private keys in source, config or git history | CWE-798 |
| Insecure deserialisation | `pickle`, `yaml.load`, Java native serialisation, polymorphic Jackson typing | CWE-502 |
| Crypto | Custom crypto, ECB mode, static IVs, `Math.random`/`random` for tokens, disabled TLS verification | CWE-327, CWE-330, CWE-295 |
| Input validation | Missing schema validation on request bodies, mass assignment of entity fields | CWE-20, CWE-915 |
| File upload | No type/size checks, stored under web root, original filename used | CWE-434 |
| Sensitive data exposure | PII/tokens in logs, stack traces returned to clients, verbose errors, debug mode on | CWE-532, CWE-209, CWE-489 |
| Open redirect | Redirect to user-supplied URL | CWE-601 |
| Dependencies | Known-vulnerable versions (from `npm audit`, `pip-audit`, `osv-scanner` if available), abandoned packages, unpinned versions | CWE-1104 |
| Rate limiting / DoS | No limits on auth, expensive endpoints, unbounded uploads or regex (ReDoS) | CWE-770, CWE-1333 |
| AI/LLM features | Prompt injection paths, model output rendered as HTML or executed, API keys in client bundle | CWE-77, CWE-79, CWE-798 |

## Secret search patterns
Search (case-insensitive) for: `api[_-]?key`, `secret`, `password\s*[:=]`, `token\s*[:=]`,
`BEGIN (RSA|EC|OPENSSH) PRIVATE KEY`, `AKIA[0-9A-Z]{16}`, `sk_live_`, `ghp_`, `xox[baprs]-`,
`AIza[0-9A-Za-z_-]{35}`, connection strings with inline credentials. Check whether `.env`
files are committed and whether `.gitignore` covers them. If git is present and the user
approves, `git log -p -S <pattern>` can reveal removed-but-leaked secrets — report them as
"rotate required" even if deleted.

Redact every secret: show type, location and at most the first 4 characters.
