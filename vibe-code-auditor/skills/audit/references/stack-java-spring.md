# Stack Guide — Java / Spring Boot

Detect via `pom.xml` / `build.gradle(.kts)`, `@SpringBootApplication`, `application.yml|properties`.
Note the Java and Spring Boot versions; Boot 2.x is end of OSS support — flag as `medium`
(maintainability) with an upgrade path to 3.x (Jakarta namespace migration).

## Architecture & layering
- Controllers containing business logic or calling repositories directly → `architecture`.
- `@Service` classes that only forward to repositories (anaemic layer) — recommend
  deleting the layer or giving it real responsibilities; don't add more.
- JPA entities returned from controllers / accepted as `@RequestBody` → mass assignment
  (CWE-915) and leaky persistence. Recommend DTOs/records + mapping.
- Interface + single `*Impl` for every service with no second implementation or test
  need → `complexity` (phantom abstraction). Spring proxies don't require interfaces.
- Package-by-layer sprawl vs package-by-feature: note inconsistency, recommend one.
- Circular bean dependencies, field injection (`@Autowired` on fields) → prefer
  constructor injection (`final` fields, Lombok `@RequiredArgsConstructor` or records).
- Multiple `@ControllerAdvice`s or try/catch in every controller → centralise.

## JPA / data access
- N+1: `@OneToMany`/`@ManyToOne` lazy collections accessed in loops or serialised by
  Jackson; missing `JOIN FETCH`/`@EntityGraph`.
- `FetchType.EAGER` everywhere; `CascadeType.ALL` on many-to-many.
- `findAll()` without pagination on large tables.
- `@Transactional` on private methods or self-invoked methods (proxy bypass), or on
  controllers; missing `readOnly = true` on read paths.
- `spring.jpa.hibernate.ddl-auto=update|create` in production config instead of
  Flyway/Liquibase.
- `open-in-view` left enabled (default true) — note as `low`/`medium`.

## Security (Spring Security)
- `csrf().disable()` / `csrf(AbstractHttpConfigurer::disable)` with cookie/session auth.
- `permitAll()` on broad matchers (`/**`, `/api/**`); ordering mistakes in matchers.
- Method security missing for ownership checks (`@PreAuthorize`) → IDOR.
- `@CrossOrigin("*")` or `allowedOrigins("*")` with `allowCredentials(true)`.
- String-concatenated JPQL/native queries, `createNativeQuery(... + param)`,
  `JdbcTemplate` with concatenation → CWE-89.
- Passwords encoded with anything other than `BCryptPasswordEncoder`/Argon2/`DelegatingPasswordEncoder`.
- JWT libraries with signature not verified, secrets hard-coded in `application.yml`.
- Actuator endpoints exposed (`management.endpoints.web.exposure.include=*`) without auth.
- Jackson default typing / `@JsonTypeInfo(use = Id.CLASS)` → CWE-502.
- `ObjectInputStream` on untrusted data; XML parsers without XXE protection (CWE-611).
- Stack traces in responses (`server.error.include-stacktrace=always`).
- Secrets in `application*.yml` committed; prefer env vars / vault.

## Code quality
- Lombok overuse (`@Data` on entities → broken equals/hashCode, lazy loading in toString).
- Checked exceptions swallowed: `catch (Exception e) { e.printStackTrace(); }`.
- `Optional.get()` without check; returning `null` collections.
- Static utility classes duplicating Apache Commons/Guava/JDK functionality.
- Use records for DTOs (Java 16+), switch expressions, `var` where it helps readability.
- `System.out.println` logging; string concatenation in log calls.

## Before/after idioms
- Field injection → constructor injection.
- Entity in API → `record UserResponse(...)` + mapper.
- Native query concatenation → named parameters / Spring Data derived queries.
- Try/catch per controller → `@RestControllerAdvice` with `ProblemDetail` (Boot 3).

## Tools (only if installed)
`mvn -q dependency:tree` (read-only), OWASP `dependency-check`, `spotbugs` + FindSecBugs,
`pmd`, `semgrep --config p/java`. Do not run the build or tests without approval.
