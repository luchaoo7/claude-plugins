# Stack Guide — TypeScript / React / Node (Express, NestJS, Next.js)

Detect via `package.json` dependencies, `tsconfig.json`, `next.config.*`, `vite.config.*`.
Check `tsconfig` for `"strict": true`; its absence is a `medium` maintainability finding
in TS projects of meaningful size.

## React / frontend
- God components (> 300 lines, many `useState`, mixed data fetching + business logic +
  rendering) → extract custom hooks and presentational components.
- `useEffect` misuse: deriving state in effects, missing/incorrect dependency arrays,
  fetch-in-effect without cancellation/race handling, effects that should be event handlers.
- Duplicated fetch logic across components instead of one API module or a data library
  already in the project (React Query/SWR). Don't introduce a new library if fetch
  consolidation suffices.
- Competing state management (Context + Redux + Zustand + prop drilling).
- Prop drilling > 3 levels for the same value.
- Keys from array index on dynamic lists; inline object/func props causing rerenders
  only when a measured or obvious hot path.
- Copies of the same UI component with small differences (Button, ButtonNew, PrimaryBtn).
- `any`/`as any`/`// @ts-ignore` density — count and report hotspots.
- Duplicated type definitions for the same API entity; recommend a shared types/schema
  module (Zod or generated OpenAPI types).

## Next.js specifics
- Secrets referenced in client components or `NEXT_PUBLIC_*` vars holding secrets.
- Server actions / route handlers without auth checks or input validation.
- `getServerSideProps`/server components fetching per request what could be cached —
  only when evident.
- Mixed `pages/` and `app/` routers without a migration plan.

## Node / Express / NestJS backend
- Route handlers containing business logic and DB queries inline → service module.
- Missing request validation (zod/joi/class-validator) on bodies, params and queries.
- Error handling: async handlers without try/catch or error middleware (Express 4),
  unhandled promise rejections, `catch (e) {}`.
- `cors()` with no options in production, or `origin: true` with `credentials: true`.
- Missing `helmet`, rate limiting on auth routes, body size limits.
- `child_process.exec` with interpolated input (CWE-78); `eval`/`new Function`.
- SQL via template literals in `pg`/`mysql2`/Prisma `$queryRawUnsafe` (CWE-89);
  Mongo queries accepting raw objects from `req.body` (operator injection, CWE-943).
- JWT: `jwt.decode` used instead of `jwt.verify`; algorithms not pinned; secret in code.
- Passwords hashed with `crypto.createHash('sha256')` instead of bcrypt/argon2.
- `fs` paths built from user input (CWE-22); `res.redirect(req.query.url)` (CWE-601).
- Secrets in `.env` committed; `process.env` read throughout code instead of one
  validated config module.
- Prototype pollution via deep-merge of user input (CWE-1321).

## Dependencies & bloat
- Multiple libraries for the same job (axios + node-fetch + ky; moment + dayjs; lodash +
  underscore). Unused dependencies: search for each package name in imports.
- `devDependencies` vs `dependencies` misplacement; huge bundles from whole-library imports.
- `npm audit --omit=dev --json` (or pnpm/yarn equivalent) only if a lockfile exists and the
  tool is available — it reads the lockfile and does not execute project code.

## Before/after idioms
- Effect-derived state → computed value / `useMemo`.
- Repeated fetch + loading/error state → one `useXxx` hook or the existing data library.
- Inline handler logic → service function with validated input (zod schema).
- Scattered `process.env` → `config.ts` parsed once with a schema.

## Tools (only if installed and already configured)
`eslint` (project config), `tsc --noEmit` (needs approval: it's safe but slow),
`semgrep --config p/typescript p/react p/nodejs`, `knip` or `depcheck` for unused files/deps.
