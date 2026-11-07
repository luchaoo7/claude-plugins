# Stack Guide — Python (Django, FastAPI, Flask)

Detect via `pyproject.toml`, `requirements*.txt`, `Pipfile`, `manage.py`, `settings.py`,
`FastAPI(` / `Flask(` instantiation. Note the Python version; < 3.9 is end-of-life → flag.

## Cross-framework
- Missing type hints on public functions in a sizeable codebase; `dict` passed everywhere
  instead of dataclasses/Pydantic models.
- `except Exception: pass` / bare `except:` / broad excepts that log and continue.
- Mutable default arguments (`def f(x=[])`).
- Modules > 800 lines (`views.py`, `utils.py`, `services.py`) mixing concerns.
- Duplicated helpers across apps/modules; reimplementation of stdlib (`pathlib`,
  `itertools`, `functools`, `dataclasses`).
- `print` debugging left in; `logging` configured in multiple places.
- Settings/env read ad hoc via `os.environ[...]` across code instead of one settings object.
- Sync blocking calls (`requests`, `time.sleep`, sync DB drivers) inside `async def`
  handlers (FastAPI) → event-loop blocking.

## Security
- `subprocess.*(..., shell=True)` with input, `os.system` (CWE-78).
- f-strings/`%`/`.format` in SQL: `cursor.execute(f"...")`, Django `.raw()` / `.extra()`
  with interpolation, SQLAlchemy `text(f"...")` (CWE-89).
- `pickle.loads`, `yaml.load` without `SafeLoader`, `eval`/`exec` on input (CWE-502, CWE-95).
- `requests.get(..., verify=False)` (CWE-295); user-supplied URLs fetched server-side (CWE-918).
- `random` used for tokens instead of `secrets` (CWE-330).
- Jinja2 `Environment(autoescape=False)`, `|safe`, `Markup()` on user input (CWE-79).
- `send_file`/`open` with user paths (CWE-22).
- Passwords hashed with `hashlib` instead of `passlib`/`argon2`/Django hashers.

## Django
- `DEBUG = True`, `ALLOWED_HOSTS = ['*']`, `SECRET_KEY` hard-coded in settings.
- `@csrf_exempt` on state-changing views; `CORS_ALLOW_ALL_ORIGINS = True`.
- Missing `permission_classes` / object-level permission checks in DRF views (IDOR);
  `DEFAULT_PERMISSION_CLASSES` set to `AllowAny`.
- `ModelSerializer` with `fields = '__all__'` on write endpoints (mass assignment, CWE-915).
- N+1 queries: missing `select_related`/`prefetch_related`; queries in templates/loops.
- Fat views; business logic in `save()` overrides and signals scattered across apps.
- `mark_safe` on user content.

## FastAPI
- Endpoints without auth dependencies; auth logic copied per route instead of a shared
  `Depends`.
- Pydantic models reused for input and DB/output, leaking fields (e.g. `password_hash`).
- `response_model` missing on endpoints returning ORM objects.
- CORS middleware with `allow_origins=["*"]` and `allow_credentials=True`.
- DB sessions created per call instead of a dependency with proper lifecycle.

## Flask
- `app.run(debug=True)` reachable in production; `SECRET_KEY` hard-coded.
- No CSRF protection on forms (Flask-WTF absent) with session auth.
- Blueprints absent in a large app — everything in `app.py`.

## Before/after idioms
- Raw SQL f-string → parameterised query / ORM filter.
- Untyped dict payloads → Pydantic model / dataclass.
- Copy-pasted auth checks → `Depends(get_current_user)` / DRF permission class / decorator.
- N+1 loop → `select_related` / `selectinload`.

## Tools (only if installed)
`ruff check` (read-only), `bandit -r`, `pip-audit -r requirements.txt` (reads files, needs
network), `vulture` for dead code, `radon cc` for complexity, `semgrep --config p/python`.
