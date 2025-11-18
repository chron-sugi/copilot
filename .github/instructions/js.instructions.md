<priority_legend>
P0=MUST follow; breaking this invalidates the request.
P1=SHOULD follow; deviations need an explicit rationale.
P2=CAN follow; use when helpful but optional.
</priority_legend>

<rules>

## Core Principles — Architecture & Design

J1  [P0] Single responsibility at every level  
  - Each function, module, and feature has one clear purpose.  
  - Split code when a unit has more than one reason to change.

J2  [P0] Functional core, imperative shell  
  - Keep business logic pure and side‑effect free where possible.  
  - Confine I/O (DOM, network, storage, timers, process env) to thin adapter layers.  
  - Pure logic should be easily testable without mocking global state.

J3  [P0] Explicit contracts and runtime validation at boundaries  
  - Define explicit data contracts (types/schemas) for module boundaries and external inputs.  
  - Validate all untrusted data (network, storage, user input, environment) using runtime schemas (e.g., Zod, Valibot, Yup, custom validators).  
  - Reject invalid data early with actionable error messages.

J4  [P0] Dependency inversion and explicit side‑effect dependencies  
  - Pass effectful dependencies (e.g., `fetch`, `storage`, `logger`, `clock`, `random`) into functions instead of importing globals where feasible.  
  - Avoid hidden singletons; make side effects explicit in function signatures.  
  - Prefer small “dependency bags” (`{ fetchFn, logger, now }`) over broad, opaque containers.

J5  [P1] Deterministic, idempotent logic; avoid global mutable state  
  - Prefer deterministic functions (same input → same output).  
  - Make operations idempotent where it improves safety (e.g., applying the same update twice yields same result).  
  - Avoid module‑level mutable state unless it’s clearly a cache or intentional singleton with documented behavior.

J6  [P1] Guard clauses and invariants  
  - Fail fast with guard clauses at the top of functions to reject impossible or invalid states.  
  - Use small assertion helpers to enforce invariants; errors should have clear messages and ideally typed shapes.

J7  [P1] Structured error types and logging  
  - Use domain‑specific error classes (e.g., `HttpError`, `ValidationError`) instead of generic `Error`.  
  - Include `.cause` when rethrowing to preserve original context.  
  - Prefer structured logging (`{ topic, ...fields }`) over interpolated strings.

---

## Naming Conventions — Files, Folders, Symbols

J8  [P0] Consistent naming across the codebase  
  - Folders and files: `kebab-case` (e.g., `user-profile`, `cart.service.ts`).  
  - Components and classes: `PascalCase` (e.g., `CartPanel`, `HttpError`).  
  - Functions, variables, hooks: `camelCase` (hooks start with `use` e.g., `useCart`).  
  - Constants and enums: `SCREAMING_SNAKE_CASE`.  
  - Tests: `[name].test.[jt]s(x)`; mocks: `[name].mock.[jt]s`.

J9  [P1] Export style and barrels  
  - Prefer named exports (`export function parseUser…`) for most modules.  
  - Avoid ambiguous `index.[jt]s` barrels inside features except at clear feature boundaries (e.g., `features/cart/index.ts`).  
  - Keep barrel modules small and explicit; no deep re‑export chains.

J10 [P1] UI naming patterns (React or similar)  
  - Hooks: `useSomething` (`useCart`, `useUserProfile`).  
  - Context providers: `SomethingProvider` (`CartProvider`).  
  - Event handler props: `onX` (e.g., `onSubmit`); handler implementations: `handleX` (e.g., `handleSubmit`).  
  - Styles: files mirror component names (`Button.tsx`, `Button.module.css`, `button.css.ts`, or `button.css`, depending on approach).

---

## Project Layout & Structure

J11 [P0] Feature‑oriented directory structure for front‑end apps  
  - Use a feature‑first layout by default:  
    - `app/` — app shell: routing, root providers, global styles, error boundary.  
    - `features/<feature>/` — self‑contained slices with `components/`, `hooks/`, `api/`, `model/`, `services/`, tests, and styles.  
    - `shared/` — cross‑feature building blocks: `ui/`, `lib/`, `config/`, `types/`, `logger`, etc.  
  - Co‑locate tests and styles next to the code they relate to.

J12 [P1] Example front‑end layout  
  - Typical structure an agent should prefer to create/extend:  
    - `src/app/router/routes.ts` — route definitions.  
    - `src/app/providers/QueryClientProvider.tsx` — global providers.  
    - `src/features/cart/components/CartPanel/CartPanel.tsx` and `.test.tsx`.  
    - `src/features/cart/hooks/useCart.ts` and `.test.ts`.  
    - `src/features/cart/api/get-cart.ts`, `update-cart.ts`.  
    - `src/features/cart/model/cart.types.ts`, `cart.schema.ts`, `cart.selectors.ts`.  
    - `src/features/cart/services/cart.service.ts`.  
    - `src/shared/ui/Button/Button.tsx` and `.test.tsx`.  
    - `src/shared/lib/http/http-client.ts`, `src/shared/logger/logger.ts`.  
    - `src/shared/config/env.ts`.

J13 [P2] Limited, intentional cross‑cutting modules  
  - Use `shared/` only for genuinely cross‑feature concerns; avoid dumping misc utilities here.  
  - When a utility is used by a single feature, keep it under that feature.

---

## Type Safety, Modules & Modern JS (2025‑ready)

J14 [P0] Prefer TypeScript; otherwise enable strong JS type checking  
  - If TypeScript is allowed, write new code in `.ts`/`.tsx`.  
  - If strictly JS, enable `// @ts-check` and use JSDoc for public functions, types, and complex data.  
  - Use runtime validation libraries (e.g., Zod, Valibot) at network and storage boundaries.

J15 [P1] Module system and bundling conventions  
  - Use ESM as the default (`"type": "module"` or `.mjs` where appropriate).  
  - Use top‑level `await` and dynamic `import()` only where supported and justified (e.g., code‑splitting).  
  - Prefer modern bundlers (Vite, Rspack, Turbopack) with strict source maps enabled in dev and staging.

J16 [P1] State and data handling  
  - Keep local UI state inside components (hooks/signals) and separate from server/cache state.  
  - Use a dedicated async data library (e.g., TanStack Query, SWR) for server state.  
  - Wrap `fetch`/HTTP calls with a small client that handles timeouts, retries, backoff, and `AbortController`.  
  - Narrow types at the edges; use richer domain types internally.

J17 [P1] Security and safety on the front‑end  
  - Sanitize any untrusted HTML before injecting into the DOM.  
  - Respect CSP (nonces/hashes) and avoid inline scripts/styles.  
  - Never embed secrets or privileged credentials in front‑end code.  
  - Use strict `postMessage` origins and validate message payloads.

---

## UI, Accessibility & Performance

J18 [P0] Accessible by default  
  - Prefer semantic HTML elements; use ARIA attributes only when necessary and correctly.  
  - Ensure all interactive elements are keyboard accessible and have visible focus states.  
  - Use proper roles, labels, and relationships; prefer accessible queries in tests.

J19 [P1] Styling approach and component API  
  - Use a single primary styling approach per repo (CSS Modules, Tailwind, or vanilla‑extract).  
  - Use design tokens and CSS variables rather than hardcoded values in JS/TS logic.  
  - Keep component props surfaces small and focused; support controlled/uncontrolled patterns and `ref` forwarding when appropriate.

J20 [P1] Performance patterns  
  - Apply route‑ and component‑level code splitting where it meaningfully reduces initial bundle size.  
  - Prefer tree‑shakeable libraries and named exports; avoid unnecessary side effects in modules.  
  - Optimize images (responsive sizes, `loading="lazy"`, modern formats) and configure HTTP caching (ETag/Cache‑Control).  
  - Maintain performance budgets and enforce them in CI for critical bundles where possible.

---

## Testing Strategy & Conventions

J21 [P0] Testing pyramid and scope  
  - Prioritize unit tests for pure functions and selectors (no network/DOM).  
  - Use component tests (e.g., Testing Library) for UI interactions and states; avoid brittle DOM snapshots.  
  - Add contract/adapter tests for HTTP clients, storage, and router adapters (e.g., with MSW).  
  - Use a small number of focused E2E tests (Playwright/Cypress) for critical flows only.  
  - Always run static checks (typecheck, ESLint, formatting) as part of the validation pipeline.

J22 [P1] Testing conventions  
  - Prefer one `describe` block per public function or component.  
  - Use accessible queries first (role, name, label) and `data-testid` only when necessary.  
  - Use property‑based tests for parsers/formatters when they add real value.  
  - Keep mocks local to each test file; avoid heavy global Jest/Vitest setup where not needed.

---

## Debuggability & Observability

J23 [P1] Error handling patterns  
  - Define dedicated error types with additional fields (e.g., `status`) and a `.cause` chain.  
  - Avoid swallowing errors; log and rethrow with context where appropriate.  
  - Use assertions/invariants to detect impossible states early in development.

J24 [P1] Logging and instrumentation  
  - Use a minimal structured logger with log levels (`debug`, `info`, `warn`, `error`).  
  - Include correlation identifiers (user/session/request) in logs where relevant.  
  - Instrument key user journeys and Web Vitals where feasible; connect errors to user‑visible error boundaries.

J25 [P1] Source maps and dev tooling  
  - Enable source maps in all non‑production builds (dev/staging).  
  - Use `displayName` or clear component names to improve debugging experiences in dev tools.

---

## Implementation Style & Coding Guidelines

J26 [P0] Module size and export clarity  
  - Prefer small modules (generally ≤200 lines) focused on a cohesive concern.  
  - Use named exports and keep the public API of a module obvious and documented.  
  - For feature entry points, use `index.ts` to re‑export the feature’s public surface intentionally.

J27 [P1] Function style and complexity  
  - Prefer short functions (~5–25 lines) and composition instead of deeply nested branching.  
  - Use early returns (guard clauses) to simplify control flow.  
  - Avoid “clever” patterns that reduce readability for marginal gains.

J28 [P1] Magic values, configuration, and comments  
  - Avoid magic numbers/strings; extract them into constants, enums, or config.  
  - Co‑locate domain‑specific constants near their primary usage.  
  - Comments should explain *why* something is done; names should explain *what/how*.

J29 [P1] Explicit dependencies over imports of globals  
  - Accept dependencies as parameters where it improves testability, e.g., `{ fetchFn, logger, now = Date.now }`.  
  - Avoid reaching into global singletons (e.g., `window.fetch`, global loggers) in core logic where injection is viable.  
  - Be pragmatic: framework integration code (e.g., React components) can use ambient APIs when that’s idiomatic, but keep business logic injectible.

J30 [P2] File headers and documentation  
  - At the top of complex or central modules, briefly document: purpose, public API, key dependencies, notable side effects.  
  - Keep these headers concise and updated when APIs evolve.

---

## Tooling & Automation

J31 [P0] Baseline tooling for JS/TS repos  
  - Use ESLint (`eslint:recommended`, framework plugins like `eslint-plugin-react`) plus rules for import ordering and unused imports.  
  - Use Prettier as the single source of formatting truth; avoid overlapping formatting rules in ESLint.  
  - Enforce type checking (`tsc --noEmit` or `tsc --allowJs --checkJs`) in CI.

J32 [P1] Tests, hooks, and CI gates  
  - Use Vitest or Jest for unit/component tests, Testing Library for UI, and Playwright/Cypress for E2E.  
  - Use Git hooks (e.g., `lint-staged`) to verify format, lint, typecheck, and tests on changed files.  
  - Configure CI to gate merges on lint, typecheck, tests, and build; apply coverage thresholds for critical modules.

---

## Quick Naming & Structure Cheat Sheet

J33 [P1] Naming recap for common artifacts  
  - Feature folder: `kebab-case` — `features/user-profile`.  
  - Component folder: `PascalCase` — `Button/`.  
  - Component file: `PascalCase` — `Button.tsx`.  
  - Hook: `useCamelCase` — `useUserProfile.ts`.  
  - Utility: `camelCase` — `formatPrice.ts`.  
  - Class: `PascalCase` — `HttpError.ts`.  
  - Test: `name.test.ts(x)` — `CartPanel.test.tsx`.  
  - Mock: `name.mock.ts` — `http-client.mock.ts`.  
  - Styles: mirror component — `Button.module.css`.  
  - Entry/integration: minimal barrels — `features/cart/index.ts`.

---

## TL;DR for JS/TS Agents

J34 [P0] Summary of behavior to optimize for  
  - Use feature‑first structures and consistent naming.  
  - Keep core logic pure, inject effects, and enforce typed + validated contracts.  
  - Write small, named‑export modules with clear responsibilities.  
  - Prefer deterministic, well‑tested code with clean seams for adapters.  
  - Make debugging easy via structured logs, error types, and source maps.  
  - Automate lint/format/type/tests to keep feedback fast and quality high.

</rules>