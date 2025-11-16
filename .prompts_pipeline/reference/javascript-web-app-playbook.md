# JavaScript Web Application Development Playbook (2025)

A comprehensive guide for LLM agents acting as senior JavaScript architects/front-end engineers. Focuses on **clarity, testability, debuggability, and maintainability**—standardizing naming and structure for consistent, production-ready code.

---

## 1) Core qualities the agent should optimize for

**Design & organization**

* **Single responsibility** at every level (function, module, feature).
* **Functional core, imperative shell**: business logic is pure and testable; I/O, DOM, and network are isolated in thin adapters.
* **Explicit data contracts** between modules (types/schemas), with **runtime validation** on all external boundaries.
* **Dependency inversion**: pass side-effectful dependencies (e.g., `fetch`, storage, logger, clock) into functions; avoid hidden singletons.

**Implementation**

* **Small modules** (generally ≤200 lines) with **named exports**. Default exports only for framework requirements (Next.js pages, etc.).
* **Deterministic, idempotent logic** where possible; avoid global mutable state.
* **Guard clauses** and **invariants** (fail fast with actionable error messages).

**Testability**

* **Pure functions first**; thin adapters make seams for tests.
* **Contract tests** for adapters; **unit tests** for pure logic; **component tests** for UI; **few, focused E2E tests** for critical flows.

**Debuggability**

* **Structured logging** (not string soup), **error types with `.cause`**, and **source maps** in dev/staging (evaluate for production).
* **Feature flags** and **traceable configuration** (environment & build-time).
* **Descriptive names** > comments; when comments exist, they explain *why*, not *what*.

**Maintainability**

* **Consistent naming & layout** (see §3–4).
* **Strong static checks** (TypeScript or `// @ts-check` + JSDoc in JS).
* **Automated quality gates** (lint, format, typecheck, tests) on every change.

---

## 2) Naming conventions (folders, files, classes, symbols)

**General**

* **Folders & files**: `kebab-case`
* **Components & classes**: `PascalCase`
* **Functions, variables, hooks**: `camelCase` (`useSomething` for hooks)
* **Constants & enums**: `SCREAMING_SNAKE_CASE`
* **Tests**: `[name].test.[jt]s(x)`; **mocks**: `[name].mock.[jt]s`

**Do / Don't**

* ✅ Prefer **named exports**: `export function parseUser…`
* ⚠️ Default exports only when required by framework (Next.js pages, etc.)
* ❌ Avoid ambiguous `index.js` barrels except at feature boundaries.
* ✅ Prefix React hooks with `use…`; context providers with `SomethingProvider`.
* ✅ Event handlers: `onX`, handler fns: `handleX`.
* ✅ CSS modules/Tailwind files mirror component names: `Button.module.css`, `button.css.ts`, or `button.css` (depending on approach).

**Examples**


---

## 3) Project layout patterns (front-end)

**Feature-oriented (recommended)**

* `app/` – app shell: routing, root providers, global styles, error boundary
* `features/<feature>/` – self-contained slices with `components/`, `hooks/`, `api/`, `model/`, `services/`, tests, and styles
* `shared/` – cross-feature building blocks: `ui/`, `lib/`, `config/`, `types/`

**Why this helps an LLM**: the folder conveys intent; co-location reduces cross-file hops; limited barrels keep import paths stable and explicit.

---

## 4) Modern techniques & tools (2025-ready, JS-first)

**Type safety (even in JS)**

* If TypeScript is allowed, **use TypeScript** with strict mode:

  ```json
  {
    "compilerOptions": {
      "strict": true,
      "noUncheckedIndexedAccess": true,
      "noImplicitOverride": true,
      "exactOptionalPropertyTypes": true,
      "verbatimModuleSyntax": true
    }
  }
  ```

* If strictly JS, enable `// @ts-check` and **JSDoc types** for functions, plus **runtime validation**:

  ```js
  // @ts-check
  import { userSchema } from './user.schema.js';

  /**
   * @typedef {{ id: string, name: string }} User
   * @param {string} id
   * @param {{ fetchFn?: typeof fetch }} [deps]
   * @returns {Promise<User>}
   */
  export async function getUser(id, deps = {}) {
    const fetchFn = deps.fetchFn ?? fetch;
    const res = await fetchFn(`/api/users/${id}`);
    const data = await res.json();
    // validate with schema (e.g., zod/valibot) before returning
    return userSchema.parse(data);
  }
  ```

**Modules & bundling**

* **ESM everywhere**, **top-level `await`** where supported, **dynamic `import()`** for code-splitting.
* Use **Vite** (or Rspack/Turbopack) for dev/build; strict **source maps** in dev & staging.
* **Configure tree-shaking** properly:

  ```json
  // package.json
  {
    "sideEffects": false,
    // OR list specific files with side effects:
    "sideEffects": ["*.css", "./src/polyfills.js"]
  }
  ```

**State & data**

* **Local UI state** by component (React hooks or framework's signals).
* **Server state** with a cache/async library (TanStack Query/SWR); keep it **separate** from local UI state.
* **Schemas** (zod/valibot) at network boundaries; narrow types at the edges, rich types inside.
* Prefer **fetch wrappers** with timeouts, retries, backoff, and **abort** (AbortController).

**UI**

* **Accessible by default** (semantic HTML, ARIA where required, visible focus, test with axe-core/jest-axe).
* **Styles**: CSS Modules, Tailwind, or vanilla-extract—**one approach per repo**; use **design tokens** and **CSS variables**; embrace **container queries**, **cascade layers** (`@layer`), and native **CSS nesting**.
* **Component API**: small props surface, controlled/uncontrolled patterns, forward refs when appropriate.

**Performance**

* **Route- and component-level code splitting** with Suspense boundaries, prefetch critical routes.
* **Tree-shakeable packages & named exports** (requires `sideEffects: false` in package.json).
* **Image optimization** (responsive images, `loading="lazy"`, modern formats like WebP/AVIF; use tools like next/image or @unpic/react).
* **HTTP caching** (ETag/Cache-Control), **performance budgets** in CI.
* **Resource hints**: `<link rel="preload">`, `<link rel="prefetch">`, `<link rel="preconnect">`.
* **Dependency size awareness**: Check bundlephobia.com; prefer smaller/tree-shakeable alternatives:

  ```js
  // ❌ Large bundle impact
  import _ from 'lodash';  // 70KB
  import moment from 'moment';  // 290KB!

  // ✅ Tree-shakeable or smaller alternatives
  import { debounce } from 'lodash-es';  // ~2KB
  import { formatDistance } from 'date-fns';  // 2-5KB
  ```

* **Re-render optimization gotchas**:

  ```tsx
  // ❌ DON'T memoize unless profiled
  const doubled = useMemo(() => count * 2, [count]);  // Overhead > benefit

  // ✅ DO memoize expensive operations (>16ms)
  const filtered = useMemo(
    () => largeList.filter(item => item.score > threshold),
    [largeList, threshold]
  );

  // ✅ React.memo with custom comparison
  const MemoizedChild = React.memo(Child, (prev, next) => {
    // Only re-render if specific props changed
    return prev.id === next.id && prev.status === next.status;
  });

  // ⚠️ useCallback is only useful with React.memo or deps array
  const handleClick = useCallback(() => {
    doSomething(value);
  }, [value]);  // Only if handleClick is passed to memoized component
  ```

* **Virtual scrolling** for large lists (>100 items):

  ```tsx
  import { useVirtualizer } from '@tanstack/react-virtual';

  function LargeList({ items }) {
    const parentRef = useRef(null);
    const virtualizer = useVirtualizer({
      count: items.length,
      getScrollElement: () => parentRef.current,
      estimateSize: () => 50,  // Estimated row height
    });

    return (
      <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
        <div style={{ height: `${virtualizer.getTotalSize()}px` }}>
          {virtualizer.getVirtualItems().map(virtualRow => (
            <div key={virtualRow.index} style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              transform: `translateY(${virtualRow.start}px)`,
            }}>
              {items[virtualRow.index].name}
            </div>
          ))}
        </div>
      </div>
    );
  }
  ```

* **Request waterfall prevention**:

  ```tsx
  // ❌ BAD: Sequential waterfalls
  const user = await getUser();
  const posts = await getPosts(user.id);  // Waits for user
  const comments = await getComments(posts[0].id);  // Waits for posts

  // ✅ GOOD: Parallel when possible
  const [user, categories] = await Promise.all([
    getUser(),
    getCategories()  // Independent, fetch in parallel
  ]);

  // ✅ With React: Use Suspense boundaries to parallelize
  <Suspense fallback={<Loading />}>
    <UserProfile />  {/* Fetches user */}
    <RecommendedPosts />  {/* Fetches recommendations in parallel */}
  </Suspense>

  // ✅ Prefetch on hover/focus
  <Link
    to="/profile"
    onMouseEnter={() => queryClient.prefetchQuery(['user'], getUser)}
  >
    Profile
  </Link>
  ```

* **CSS-in-JS performance**: Runtime CSS-in-JS (styled-components, Emotion) has measurable cost. **Prefer build-time solutions** for performance-critical apps:

  ```tsx
  // ⚠️ Runtime CSS-in-JS: slower (styles injected during render)
  import styled from 'styled-components';
  const Button = styled.button`color: blue;`;

  // ✅ Build-time CSS-in-JS: faster (styles extracted at build)
  import { style } from '@vanilla-extract/css';
  export const button = style({ color: 'blue' });

  // ✅ Or CSS Modules
  import styles from './Button.module.css';
  ```

**Security**

* **XSS prevention**: Sanitize user-generated HTML with DOMPurify:

  ```tsx
  import DOMPurify from 'dompurify';

  function UnsafeHTML({ html }: { html: string }) {
    // ❌ NEVER do this without sanitization
    // <div dangerouslySetInnerHTML={{ __html: html }} />

    // ✅ Always sanitize
    const clean = DOMPurify.sanitize(html, {
      ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
      ALLOWED_ATTR: ['href'],
    });
    return <div dangerouslySetInnerHTML={{ __html: clean }} />;
  }
  ```

* **postMessage origin validation**: Use strict equality, not `startsWith`:

  ```ts
  // ❌ DANGEROUS: Can be bypassed
  window.addEventListener('message', (event) => {
    if (event.origin.startsWith('https://trusted.com')) {
      // Attacker could use https://trusted.com.evil.com
    }
  });

  // ✅ SAFE: Strict equality
  window.addEventListener('message', (event) => {
    if (event.origin !== 'https://trusted.com') return;
    handleMessage(event.data);
  });
  ```

* **CSRF protection**: For server-rendered apps with sessions:

  ```tsx
  // Include CSRF token in forms
  <form method="POST" action="/api/update">
    <input type="hidden" name="_csrf" value={csrfToken} />
  </form>

  // Or in fetch headers
  fetch('/api/update', {
    method: 'POST',
    headers: {
      'X-CSRF-Token': getCsrfToken(),
    },
  });
  ```

* **CSP** with nonces/hashes; **no secrets in front-end**.
* **CORS configuration**: Explicit origin whitelist, credentials handling.
* **Subresource Integrity (SRI)** for third-party scripts:

  ```html
  <script src="https://cdn.example.com/lib.js"
          integrity="sha384-..."
          crossorigin="anonymous"></script>
  ```

* **Security audits**: Regular `npm audit`, use Dependabot/Snyk for dependency scanning.

**Observability**

* Minimal **structured logger** with levels; **user/session correlation id**.
* Instrument **Web Vitals** (CLS, LCP, FID/INP); use RUM tools (Vercel Analytics, Sentry Performance).
* Surface errors with **Error Boundaries** and add `.cause` to errors you rethrow.
* **Breadcrumbs** for debugging: track user actions before errors.

**Browser Support**

* Define support matrix with **Browserslist** in package.json:

  ```json
  {
    "browserslist": [
      "defaults",
      "not IE 11",
      "maintained node versions"
    ]
  }
  ```

* Use **feature detection** (`@supports` in CSS, conditional checks in JS).
* Polyfill strategy: core-js, polyfill.io, or framework-specific solutions.

---

## 5) Modern React patterns (2025)

**Server Components (RSC)**

* Use Server Components by default for data fetching and heavy computation.
* Client Components (`'use client'`) only when needed: interactivity, browser APIs, hooks.
* Server Actions for mutations; avoid client-side API routes when possible.

**Suspense & Streaming**

* Wrap async components with `<Suspense>` boundaries:

  ```tsx
  <Suspense fallback={<LoadingSkeleton />}>
    <AsyncDataComponent />
  </Suspense>
  ```

* Use streaming SSR for faster Time to First Byte (TTFB).

**Concurrent Features**

* **useTransition**: Mark non-urgent updates to keep UI responsive:

  ```tsx
  const [isPending, startTransition] = useTransition();

  function handleChange(value) {
    startTransition(() => {
      setSearchQuery(value); // Non-urgent update
    });
  }
  ```

* **useDeferredValue**: Defer expensive re-renders:

  ```tsx
  const deferredQuery = useDeferredValue(searchQuery);
  ```

* **use() hook** (React 19): Read promises/context in render:

  ```tsx
  function UserProfile({ userPromise }) {
    const user = use(userPromise);
    return <div>{user.name}</div>;
  }
  ```

**SSR/Hydration Best Practices**

* Avoid hydration mismatches:

  ```tsx
  // ❌ Will mismatch
  <div>{Math.random()}</div>
  <div>{new Date().toISOString()}</div>
  <div>{typeof window !== 'undefined' && <ClientOnly />}</div>

  // ✅ Use suppressHydrationWarning for intentional mismatches
  <time suppressHydrationWarning>{new Date().toISOString()}</time>

  // ✅ Or use useEffect for client-only content
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  if (!mounted) return null;
  ```

---

## 6) Testing strategy (fast to slow)

1. **Unit** (most): pure functions & selectors; **no** network/DOM.
2. **Component tests**: interactions via Testing Library; no brittle DOM snapshots.
3. **Contract/adapter tests**: http client, storage, router adapters (with mock server like MSW).
4. **E2E** (few): Playwright/Cypress for critical flows.
5. **Static**: typecheck + ESLint + Prettier. Gate merges on these.

**Conventions**

* One `describe` block per public function/component.
* Use **data-testids** sparingly; prefer accessible roles/labels first (test via Testing Library queries).
* Property-based tests for parsers/formatters where valuable.
* Keep mocks local to tests; avoid global jest/setup pollution.
* **Mock at boundaries**, not internal modules:

  ```ts
  // ✅ Mock at network boundary
  import { setupServer } from 'msw/node';
  const server = setupServer(
    http.get('/api/cart', () => HttpResponse.json({ items: [] }))
  );

  // ❌ Don't over-mock internals
  jest.mock('../../utils/formatPrice');
  jest.mock('../../api/getCart');
  jest.mock('../../hooks/useUser');
  // You're testing mocks, not real integration!
  ```

**Accessibility testing**

* Integrate **axe-core** in component tests:

  ```ts
  import { axe, toHaveNoViolations } from 'jest-axe';
  expect.extend(toHaveNoViolations);

  test('should have no a11y violations', async () => {
    const { container } = render(<MyComponent />);
    expect(await axe(container)).toHaveNoViolations();
  });
  ```

**Visual regression testing**

* Use Chromatic, Percy, or Playwright screenshots for critical UI.

**Performance testing**

* Lighthouse CI in pipeline; assert on Core Web Vitals thresholds.

**Flaky test prevention**

```ts
// ❌ DON'T: Use arbitrary timeouts
test('loads data', async () => {
  render(<Component />);
  await new Promise(resolve => setTimeout(resolve, 1000));  // Brittle!
  expect(screen.getByText('Loaded')).toBeInTheDocument();
});

// ✅ DO: Wait for specific conditions
test('loads data', async () => {
  render(<Component />);
  await waitFor(() => {
    expect(screen.getByText('Loaded')).toBeInTheDocument();
  });
});

// ✅ DO: Use Testing Library queries that wait
test('loads data', async () => {
  render(<Component />);
  expect(await screen.findByText('Loaded')).toBeInTheDocument();  // Waits automatically
});

// ✅ DO: Test user-visible behavior, not implementation
// ❌ Bad: expect(mockFn).toHaveBeenCalledTimes(1);
// ✅ Good: expect(screen.getByText('Success')).toBeInTheDocument();
```

**Test data factories**

```ts
// shared/test-utils/builders.ts
import { faker } from '@faker-js/faker';

export const buildUser = (overrides: Partial<User> = {}): User => ({
  id: faker.string.uuid(),
  name: faker.person.fullName(),
  email: faker.internet.email(),
  createdAt: faker.date.past(),
  ...overrides,
});

export const buildCart = (overrides: Partial<Cart> = {}): Cart => ({
  id: faker.string.uuid(),
  items: [],
  total: 0,
  ...overrides,
});

// Usage in tests
test('displays user name correctly', () => {
  const user = buildUser({ name: 'John Doe' });
  render(<UserProfile user={user} />);
  expect(screen.getByText('John Doe')).toBeInTheDocument();
});

test('handles empty cart', () => {
  const cart = buildCart({ items: [] });
  render(<CartSummary cart={cart} />);
  expect(screen.getByText('Your cart is empty')).toBeInTheDocument();
});
```

---

## 7) Debuggability patterns

**Error categorization & handling**

Different error types require different handling strategies:

```ts
// User-facing errors: show to user, don't retry
export class DomainError extends Error {
  constructor(message: string, public readonly userMessage: string, cause?: unknown) {
    super(message);
    this.name = 'DomainError';
    if (cause) this.cause = cause;
  }
}

// Technical errors: log & retry with backoff
export class TechnicalError extends Error {
  constructor(message: string, public readonly retryable: boolean = true, cause?: unknown) {
    super(message);
    this.name = 'TechnicalError';
    if (cause) this.cause = cause;
  }
}

// Fatal errors: circuit breaker, alert on-call
export class FatalError extends Error {
  constructor(message: string, cause?: unknown) {
    super(message);
    this.name = 'FatalError';
    if (cause) this.cause = cause;
  }
}

// HTTP-specific errors
export class HttpError extends TechnicalError {
  constructor(message: string, public readonly status: number, cause?: unknown) {
    super(message, status >= 500, cause); // 5xx are retryable
    this.name = 'HttpError';
  }
}
```

**Unhandled error handlers**

```ts
// Catch unhandled promise rejections
window.addEventListener('unhandledrejection', (event) => {
  logger.error({
    reason: event.reason,
    promise: event.promise,
  }, 'Unhandled promise rejection');

  // Prevent default browser behavior
  event.preventDefault();
});

// Catch global errors
window.addEventListener('error', (event) => {
  logger.error({
    message: event.message,
    filename: event.filename,
    lineno: event.lineno,
    colno: event.colno,
    error: event.error,
  }, 'Global error');
});
```

**Error.cause polyfill note**

```ts
// Error.cause is ES2022; for older targets, manually attach:
class CustomError extends Error {
  cause?: unknown;
  constructor(message: string, cause?: unknown) {
    super(message);
    this.name = 'CustomError';
    // Use assignment instead of parameter if targeting older environments
    if (cause) this.cause = cause;
  }
}
```

**Structured logs**

```ts
// shared/logger/logger.ts
export const log = (topic: string) => ({
  debug: (details: unknown, msg?: string) =>
    console.debug({ topic, timestamp: Date.now(), ...details }, msg),
  error: (details: unknown, msg?: string) =>
    console.error({ topic, timestamp: Date.now(), ...details }, msg),
});

// usage
const logger = log('cart:update');
logger.debug({ id, qty }, 'updating cart item');
```

**Assertions/invariants**

```ts
// shared/lib/invariant.ts
export function invariant(condition: boolean, message: string): asserts condition {
  if (!condition) {
    throw new Error(`Invariant violation: ${message}`);
  }
}

// usage
invariant(user?.id, 'User ID is required');
```

**Production debugging**

* **Source maps** in dev/staging always; evaluate trade-offs for production (enable with access control).
* **displayName** on complex components for clearer React DevTools trees.
* **Correlation/Trace IDs** for distributed tracing:

  ```ts
  // Generate trace ID once per user session
  const traceId = crypto.randomUUID();

  // Include in all API requests
  fetch('/api/data', {
    headers: {
      'X-Trace-Id': traceId,
      'X-Session-Id': sessionStorage.getItem('sessionId'),
    },
  });

  // Include in all logs
  logger.error({ traceId, userId, action: 'checkout' }, 'Payment failed');
  ```

* **Feature flag tracking**: log which flags were active when errors occur.
* **Session replay** tools (LogRocket, FullStory) for reproducing issues.
* **Console logs don't persist in production**: Use actual logging services (Sentry, Datadog, LogRocket) that send logs to your backend.

---

## 8) Common pitfalls & gotchas

**1. Circular dependencies**

```js
// ❌ features/user/index.ts imports features/cart/index.ts
// ❌ features/cart/index.ts imports features/user/index.ts
// → Runtime errors or undefined imports
```

**Prevention**: Dependency graphs should be acyclic; use `madge` or ESLint rules to detect:

```bash
npx madge --circular --extensions ts,tsx src/
```

**2. Memory leaks**

```js
// ❌ Common mistakes
useEffect(() => {
  window.addEventListener('resize', handleResize);
  // Missing cleanup!
}, []);

// ❌ Uncancelled subscriptions
useEffect(() => {
  const unsubscribe = store.subscribe(listener);
  // Missing return!
}, []);

// ✅ Always clean up
useEffect(() => {
  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []);

useEffect(() => {
  const unsubscribe = store.subscribe(listener);
  return unsubscribe;
}, []);
```

**3. Race conditions & stale closures**

```js
// ❌ Async operations with stale state
async function handleSearch(query) {
  const results = await fetchResults(query); // slow!
  setResults(results); // May set stale results if query changed
}

// ✅ Cancel stale requests
async function handleSearch(query) {
  const controller = new AbortController();
  setController((prev) => {
    prev?.abort();
    return controller;
  });

  const results = await fetchResults(query, { signal: controller.signal });
  setResults(results);
}

// ✅ Or use TanStack Query which handles this automatically
const { data } = useQuery({
  queryKey: ['search', query],
  queryFn: () => fetchResults(query),
});
```

**4. Over-abstraction (the DRY trap)**

* **Don't abstract until you have 3+ instances** of nearly identical code.
* **Wrong abstractions are worse than duplication** (harder to change, cognitive overhead).
* "Duplication is far cheaper than the wrong abstraction" - Sandi Metz.
* When in doubt, **duplicate first, abstract later** when patterns emerge.

**5. Import order side effects**

```js
// ❌ Order matters with side effects
import React from 'react';
import './polyfills';  // TOO LATE! Should be first

// ✅ Side effects first
import './polyfills';
import React from 'react';
import './global.css';  // CSS import order also matters
```

**6. Error Boundary limitations**

Error Boundaries only catch errors in:
- React render phase
- Lifecycle methods
- Constructors of class components

They **don't** catch:
- Event handlers (use try/catch)
- Async code (use try/catch or .catch())
- Server-side rendering
- Errors in Error Boundary itself

```tsx
// ❌ Error Boundary won't catch this
function MyComponent() {
  const handleClick = () => {
    throw new Error('Not caught!');
  };
  return <button onClick={handleClick}>Click</button>;
}

// ✅ Handle in event handler
function MyComponent() {
  const handleClick = () => {
    try {
      dangerousOperation();
    } catch (error) {
      logError(error);
      showErrorToast();
    }
  };
  return <button onClick={handleClick}>Click</button>;
}
```

**7. Code-splitting without Suspense**

```tsx
// ❌ Will error without Suspense boundary
const LazyRoute = lazy(() => import('./Route'));
<LazyRoute />

// ✅ Wrap in Suspense
<Suspense fallback={<Loading />}>
  <LazyRoute />
</Suspense>
```

**8. Third-party scripts performance**

```html
<!-- ❌ Blocks rendering -->
<script src="https://cdn.example.com/analytics.js"></script>

<!-- ✅ Non-blocking -->
<script async src="https://cdn.example.com/analytics.js"></script>
<!-- OR -->
<script defer src="https://cdn.example.com/analytics.js"></script>
```

---

## 8a) Common anti-patterns to avoid

**1. Prop drilling beyond 3 levels**

```tsx
// ❌ Deep prop drilling
<GrandParent user={user}>
  <Parent user={user}>
    <Child user={user}>
      <DeepChild user={user} />  // 4 levels deep!
    </Child>
  </Parent>
</GrandParent>

// ✅ Use Context or composition
const UserContext = createContext<User | null>(null);

<UserContext.Provider value={user}>
  <DeepChild />  // Access via useContext(UserContext)
</UserContext.Provider>

// ✅ Or use component composition
<GrandParent>
  <DeepChild user={user} />  // Pass directly to where it's needed
</GrandParent>
```

**2. Mutating state directly**

```tsx
// ❌ Direct mutation
const [cart, setCart] = useState({ items: [] });
cart.items.push(newItem);  // Doesn't trigger re-render!

// ✅ Immutable updates
setCart(prev => ({
  ...prev,
  items: [...prev.items, newItem]
}));
```

**3. Fetching data in useEffect**

```tsx
// ❌ Manual fetching in useEffect
const [data, setData] = useState(null);
const [loading, setLoading] = useState(false);
const [error, setError] = useState(null);

useEffect(() => {
  setLoading(true);
  fetch('/api/data')
    .then(res => res.json())
    .then(setData)
    .catch(setError)
    .finally(() => setLoading(false));
}, []);

// ✅ Use TanStack Query or SWR
const { data, isLoading, error } = useQuery({
  queryKey: ['data'],
  queryFn: () => fetch('/api/data').then(r => r.json())
});
```

**4. Premature optimization**

```tsx
// ❌ Memoizing everything "just in case"
const value = useMemo(() => a + b, [a, b]);  // Overhead > benefit
const onClick = useCallback(() => setCount(c => c + 1), []);  // Rarely needed

// ✅ Profile first, optimize what's slow
// Only memoize when:
// - Computation is expensive (profiled > 16ms)
// - Value is dependency of expensive operation
// - Preventing child re-renders (with React.memo)
```

**5. Duplicating server state in local state**

```tsx
// ❌ Two sources of truth
const [user, setUser] = useState();
const { data } = useQuery('user', getUser);  // Which one is correct?

// ✅ Single source of truth
const { data: user } = useQuery('user', getUser);
const displayName = user?.name ?? 'Guest';  // Derive, don't duplicate
```

**6. Over-memoization**

```tsx
// ❌ Memoizing simple operations
const doubled = useMemo(() => count * 2, [count]);  // Overhead > benefit

// ✅ Only memoize expensive operations
const filtered = useMemo(
  () => largeList.filter(item => item.active),  // Expensive!
  [largeList]
);
```

**7. Ignoring accessibility**

```tsx
// ❌ Non-semantic, inaccessible
<div onClick={handleClick}>Click me</div>

// ✅ Semantic, accessible
<button onClick={handleClick}>Click me</button>

// ❌ Missing labels
<input type="text" />

// ✅ Proper labels
<label htmlFor="email">Email</label>
<input id="email" type="email" />
```

**8. Storing derived state**

```tsx
// ❌ Storing derived state
const [firstName, setFirstName] = useState('');
const [lastName, setLastName] = useState('');
const [fullName, setFullName] = useState('');  // Redundant!

useEffect(() => {
  setFullName(`${firstName} ${lastName}`);
}, [firstName, lastName]);

// ✅ Derive on render
const [firstName, setFirstName] = useState('');
const [lastName, setLastName] = useState('');
const fullName = `${firstName} ${lastName}`;  // Computed
```

---

## 9) Coding guidelines the agent should follow (checklist)

* **File header**: purpose, public API, dependencies, side effects.
* **Exports first**: make the public API obvious at top or via `index.ts`.
* **No magic numbers/strings**: constantize; co-locate near use if domain-specific.
* **Input validation** at boundaries; avoid `any` / untyped objects crossing modules.
* **Short functions** (≈5–25 lines); prefer composition over branching.
* **Explicit deps**: take `{ fetchFn, logger, now = Date.now }` rather than importing globals.
* **Comment only to explain *why***; names should explain *what/how*.
* **Avoid cleverness**—prefer straightforward patterns.
* **Don't prematurely optimize**: Profile first, measure impact, then optimize.

---

## 9a) State management deep-dive

**Decision tree: Which state solution to use?**

```
Is it server data (API, database)?
├─ YES → TanStack Query / SWR / RTK Query
└─ NO → Continue...

Should it persist in the URL?
├─ YES → Router state (search params, path params)
└─ NO → Continue...

Do multiple distant components need it?
├─ YES → Is it global & changes rarely?
│   ├─ YES → Context API
│   └─ NO → Is it complex with many transitions?
│       ├─ YES → XState / state machine
│       └─ NO → Zustand / Jotai
└─ NO → useState (component-local)

Do multiple tabs need to sync?
└─ YES → localStorage + BroadcastChannel or storage events
```

**Cross-tab state synchronization**

```tsx
// Tab A: Update shared state
function updateCartInAllTabs(cart: Cart) {
  localStorage.setItem('cart', JSON.stringify(cart));

  // Notify other tabs
  const channel = new BroadcastChannel('cart-updates');
  channel.postMessage({ type: 'cart-updated', cart });
}

// Tab B: Listen for updates
useEffect(() => {
  // BroadcastChannel (modern, doesn't trigger in same tab)
  const channel = new BroadcastChannel('cart-updates');
  channel.onmessage = (event) => {
    if (event.data.type === 'cart-updated') {
      setCart(event.data.cart);
    }
  };

  // OR: storage event (older, only fires in OTHER tabs)
  const handleStorage = (e: StorageEvent) => {
    if (e.key === 'cart' && e.newValue) {
      setCart(JSON.parse(e.newValue));
    }
  };
  window.addEventListener('storage', handleStorage);

  return () => {
    channel.close();
    window.removeEventListener('storage', handleStorage);
  };
}, []);
```

**Optimistic updates with rollback**

```tsx
const mutation = useMutation({
  mutationFn: updateCartItem,

  // Optimistically update cache before API call
  onMutate: async (newItem) => {
    // Cancel outgoing refetches
    await queryClient.cancelQueries({ queryKey: ['cart'] });

    // Snapshot current value for rollback
    const previousCart = queryClient.getQueryData(['cart']);

    // Optimistically update cache
    queryClient.setQueryData(['cart'], (old: Cart) => ({
      ...old,
      items: [...old.items, newItem]
    }));

    // Return rollback context
    return { previousCart };
  },

  // Rollback on error
  onError: (err, newItem, context) => {
    if (context?.previousCart) {
      queryClient.setQueryData(['cart'], context.previousCart);
    }
    toast.error('Failed to update cart');
  },

  // Refetch to ensure sync
  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: ['cart'] });
  },
});
```

**Derived state patterns**

```tsx
// ❌ DON'T: Store derived state
const [items, setItems] = useState([]);
const [total, setTotal] = useState(0);
const [count, setCount] = useState(0);

useEffect(() => {
  setTotal(items.reduce((sum, item) => sum + item.price, 0));
  setCount(items.length);
}, [items]);

// ✅ DO: Derive on render
const [items, setItems] = useState([]);
const total = items.reduce((sum, item) => sum + item.price, 0);
const count = items.length;

// ✅ For expensive derivations, memoize
const expensiveTotal = useMemo(
  () => items.reduce((sum, item) => sum + item.price * item.qty, 0),
  [items]
);
```

**Context optimization patterns**

```tsx
// ❌ Single context causes all consumers to re-render
const AppContext = createContext({ user, theme, cart, settings });

// ✅ Split into separate contexts
const UserContext = createContext(null);
const ThemeContext = createContext(null);
const CartContext = createContext(null);

// ✅ Or use context + hook pattern with selector
function useAppSelector<T>(selector: (state: AppState) => T): T {
  const state = useContext(AppContext);
  return useMemo(() => selector(state), [state, selector]);
}

// Component only re-renders when user.name changes
const userName = useAppSelector(state => state.user.name);
```

---

## 10) Concrete examples an LLM can replicate

**Feature slice (API + schema + service)**

```ts
// features/cart/model/cart.schema.ts
import { z } from 'zod';

export const CartItem = z.object({
  id: z.string(),
  name: z.string(),
  price: z.number().nonnegative(),
  qty: z.number().int().positive(),
});

export const Cart = z.object({
  items: z.array(CartItem)
});

export type Cart = z.infer<typeof Cart>;
```

```ts
// features/cart/api/get-cart.ts
import { Cart } from '../model/cart.schema';

type Deps = {
  fetchFn?: typeof fetch;
  signal?: AbortSignal;
};

export async function getCart({ fetchFn = fetch, signal }: Deps = {}): Promise<Cart> {
  const res = await fetchFn('/api/cart', {
    headers: { 'Accept': 'application/json' },
    signal,
  });

  if (!res.ok) {
    throw new Error(`Failed to load cart: ${res.status}`);
  }

  const json = await res.json();
  return Cart.parse(json); // runtime validation
}
```

```ts
// features/cart/services/cart.service.ts
import { getCart } from '../api/get-cart';
import type { Cart } from '../model/cart.schema';

export async function loadCartSummary(deps?: Parameters<typeof getCart>[0]) {
  const cart = await getCart(deps);
  const total = cart.items.reduce((sum, i) => sum + i.price * i.qty, 0);
  return { count: cart.items.length, total };
}
```

**Test example**

```ts
// features/cart/services/cart.service.test.ts
import { loadCartSummary } from './cart.service';

test('computes count and total', async () => {
  const fetchFn = async () =>
    new Response(
      JSON.stringify({
        items: [{ id: '1', name: 'A', price: 10, qty: 3 }]
      }),
      { status: 200 }
    );

  await expect(loadCartSummary({ fetchFn })).resolves.toEqual({
    count: 1,
    total: 30
  });
});

test('throws on network error', async () => {
  const fetchFn = async () => new Response(null, { status: 500 });

  await expect(loadCartSummary({ fetchFn })).rejects.toThrow('Failed to load cart');
});
```

**React Server Component + Client Component pattern**

```tsx
// app/dashboard/page.tsx (Server Component)
import { getUser } from '@/features/user/api/get-user';
import { UserProfile } from './UserProfile';

export default async function DashboardPage() {
  const user = await getUser(); // Direct async/await
  return <UserProfile user={user} />;
}
```

```tsx
// app/dashboard/UserProfile.tsx (Client Component)
'use client';

import { useState } from 'react';
import type { User } from '@/features/user/model/user.types';

export function UserProfile({ user }: { user: User }) {
  const [isEditing, setIsEditing] = useState(false);

  return (
    <div>
      <h1>{user.name}</h1>
      <button onClick={() => setIsEditing(!isEditing)}>
        {isEditing ? 'Cancel' : 'Edit'}
      </button>
    </div>
  );
}
```

---

## 10a) Cache invalidation & data synchronization

**When to invalidate vs refetch vs setQueryData**

```tsx
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

// Reading data
const { data: cart } = useQuery({
  queryKey: ['cart'],
  queryFn: getCart,
  staleTime: 5 * 60 * 1000,  // Consider fresh for 5 minutes
  cacheTime: 30 * 60 * 1000, // Keep in cache for 30 minutes
});

// Updating data: Three strategies

// 1. invalidateQueries: Mark stale & refetch (safest)
const mutation = useMutation({
  mutationFn: addToCart,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['cart'] });
    // Triggers background refetch for all matching queries
  },
});

// 2. setQueryData: Immediate optimistic update (fastest UX)
const mutation = useMutation({
  mutationFn: addToCart,
  onMutate: async (newItem) => {
    // Cancel outgoing refetches
    await queryClient.cancelQueries({ queryKey: ['cart'] });

    // Update cache immediately
    queryClient.setQueryData(['cart'], (old: Cart) => ({
      ...old,
      items: [...old.items, newItem],
    }));
  },
  onSettled: () => {
    // Refetch to ensure sync with server
    queryClient.invalidateQueries({ queryKey: ['cart'] });
  },
});

// 3. refetchQueries: Force immediate refetch (for critical data)
const mutation = useMutation({
  mutationFn: updatePayment,
  onSuccess: () => {
    queryClient.refetchQueries({ queryKey: ['cart'], type: 'active' });
    // Fetches immediately, not in background
  },
});
```

**Stale-while-revalidate gotcha**

```tsx
// ⚠️ GOTCHA: staleTime = 0 (default) refetches on every mount
const { data } = useQuery({
  queryKey: ['user'],
  queryFn: getUser,
  // staleTime: 0 (default) - refetches every time component mounts!
});

// ✅ Set staleTime to reduce unnecessary refetches
const { data } = useQuery({
  queryKey: ['user'],
  queryFn: getUser,
  staleTime: 60 * 1000,  // Consider fresh for 1 minute
  // User sees cached data, background refetch only if stale
});

// ⚠️ GOTCHA: User sees stale data during background refetch
// Solution: Use refetchInterval for critical data
const { data } = useQuery({
  queryKey: ['stock-price'],
  queryFn: getStockPrice,
  staleTime: 10 * 1000,
  refetchInterval: 10 * 1000,  // Poll every 10 seconds
  refetchIntervalInBackground: false,  // Stop when tab not visible
});
```

**Partial cache updates**

```tsx
// ❌ BAD: Refetch entire list after updating one item
onSuccess: () => {
  queryClient.invalidateQueries({ queryKey: ['todos'] });  // Refetches all todos!
};

// ✅ GOOD: Update specific item in cache
onSuccess: (updatedTodo) => {
  queryClient.setQueryData(['todos'], (old: Todo[]) =>
    old.map(todo => todo.id === updatedTodo.id ? updatedTodo : todo)
  );

  // Also update detail view cache
  queryClient.setQueryData(['todo', updatedTodo.id], updatedTodo);
};
```

**Related query invalidation**

```tsx
// When updating a cart item, invalidate related queries
onSuccess: () => {
  // Invalidate multiple related queries
  queryClient.invalidateQueries({ queryKey: ['cart'] });
  queryClient.invalidateQueries({ queryKey: ['cart-summary'] });
  queryClient.invalidateQueries({ queryKey: ['checkout'] });

  // Or use query filters
  queryClient.invalidateQueries({
    predicate: (query) =>
      query.queryKey[0] === 'cart' ||
      query.queryKey[0] === 'checkout'
  });
};
```

---

## 11) Tooling & automation (the boring parts that keep you fast)

**ESLint configuration**

```json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended",
    "plugin:jsx-a11y/recommended"
  ],
  "plugins": ["import", "unused-imports"],
  "rules": {
    "import/order": ["error", {
      "groups": ["builtin", "external", "internal", "parent", "sibling", "index"],
      "newlines-between": "always",
      "alphabetize": { "order": "asc" }
    }],
    "unused-imports/no-unused-imports": "error",
    "no-console": ["warn", { "allow": ["warn", "error"] }]
  }
}
```

**Prettier**: Single source of formatting truth; never fight it in ESLint.

**Typecheck**: `tsc --noEmit` or `tsc --allowJs --checkJs`.

**Tests**: Vitest/Jest + Testing Library + Playwright for E2E.

**Git hooks**: `lint-staged` for format/lint/test changed files:

```json
// package.json
{
  "lint-staged": {
    "*.{ts,tsx,js,jsx}": ["prettier --write", "eslint --fix", "vitest related --run"],
    "*.{css,md,json}": ["prettier --write"]
  }
}
```

**CI gates**: lint, typecheck, test, build; enforce coverage thresholds for critical modules.

**Bundle analysis**

```json
// package.json
{
  "scripts": {
    "build": "vite build",
    "analyze": "vite-bundle-visualizer"
  }
}
```

**Dependency management**

* Use **lockfiles** (package-lock.json, pnpm-lock.yaml) and commit them.
* Run **security audits** regularly: `npm audit`, integrate Snyk or Dependabot.
* For **monorepos**: pnpm workspaces, Turborepo, or Nx.

**Common tooling gotchas**

* **Case-insensitive filesystems** (macOS, Windows) hide import bugs:

  ```ts
  // File: UserProfile.tsx
  // ❌ Works on macOS, breaks on Linux CI
  import { UserProfile } from './userprofile';

  // ✅ Match exact case
  import { UserProfile } from './UserProfile';

  // Add ESLint rule to catch this:
  // "import/no-unresolved": "error"
  ```

* **Module splitting criteria**: When to split a file?
  - **Lines of code**: >200 lines (soft limit)
  - **Cyclomatic complexity**: >10 per function
  - **Single Responsibility Principle**: Module does >1 thing
  - **Test files**: Separate large test suites into focused files

* **Barrel file tree-shaking cost**: Re-exports in `index.ts` can hurt tree-shaking:

  ```ts
  // ❌ BAD: Barrel imports entire module graph
  // features/cart/index.ts
  export * from './components';  // Imports ALL components!
  export * from './hooks';

  // ✅ GOOD: Explicit named re-exports
  export { CartPanel } from './components/CartPanel';
  export { useCart } from './hooks/useCart';

  // ✅ BETTER: Import directly, skip barrel
  import { CartPanel } from '@/features/cart/components/CartPanel';
  ```

* **Circular dependency detection**: Add to CI:

  ```json
  // package.json
  {
    "scripts": {
      "lint:circular": "madge --circular --extensions ts,tsx src/",
      "lint": "npm run lint:circular && eslint ."
    }
  }
  ```

---

## 12) Build & deployment

**Performance budgets**

```json
// package.json
{
  "bundlesize": [
    { "path": "./dist/main-*.js", "maxSize": "200 KB" },
    { "path": "./dist/vendor-*.js", "maxSize": "400 KB" }
  ]
}
```

**Environment management**

```ts
// shared/config/env.ts
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'staging', 'production']),
  API_URL: z.string().url(),
  FEATURE_FLAG_X: z.coerce.boolean().default(false),
});

export const env = envSchema.parse(process.env);
```

**CI/CD pipeline template**

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm run test -- --coverage
      - run: npm run build
      - run: npx bundlesize
```

**CDN & cache-busting strategy**

```ts
// vite.config.ts or webpack.config.js
export default {
  build: {
    // ✅ Content-based hashing for cache busting
    rollupOptions: {
      output: {
        entryFileNames: 'assets/[name].[hash].js',
        chunkFileNames: 'assets/[name].[hash].js',
        assetFileNames: 'assets/[name].[hash].[ext]',
      },
    },
  },
};

// Serve with long cache headers for hashed assets
// Cache-Control: public, max-age=31536000, immutable

// index.html should have short cache or no-cache
// Cache-Control: no-cache, must-revalidate
```

**Deployment & rollback strategies**

```yaml
# Blue-green deployment example
deploy:
  steps:
    # 1. Deploy to "green" environment
    - name: Deploy to staging slot
      run: |
        deploy --slot green --build-id ${{ github.sha }}

    # 2. Run smoke tests
    - name: Smoke test
      run: npm run test:smoke -- --url https://green.example.com

    # 3. Swap slots (instant rollback if needed)
    - name: Swap to production
      run: swap-slots green blue

    # 4. Monitor for errors
    - name: Monitor
      run: |
        sleep 300  # Wait 5 minutes
        check-error-rate
        if [ $? -ne 0 ]; then
          swap-slots blue green  # Instant rollback!
          exit 1
        fi
```

**Feature flag rollback**

```ts
// shared/config/features.ts
export const features = {
  newCheckout: env.FEATURE_NEW_CHECKOUT === 'true',
  aiRecommendations: env.FEATURE_AI_RECS === 'true',
};

// Usage
if (features.newCheckout) {
  return <NewCheckoutFlow />;
}
return <LegacyCheckoutFlow />;

// Instant rollback: Just flip environment variable, no redeploy needed!
```

**Build reproducibility**

```json
// package.json - use exact versions for reproducible builds
{
  "dependencies": {
    "react": "18.2.0",  // ❌ Don't use ^18.2.0 in production
    "react-dom": "18.2.0"
  },
  "engines": {
    "node": "20.10.0",  // Pin Node version
    "npm": "10.2.3"     // Pin npm version
  }
}

// .nvmrc
20.10.0

// Dockerfile
FROM node:20.10.0-alpine  # Exact version
```

---

## 13) Advanced patterns (when needed)

**State machines for complex flows**

```ts
import { createMachine } from 'xstate';

const loginMachine = createMachine({
  initial: 'idle',
  states: {
    idle: { on: { SUBMIT: 'loading' } },
    loading: {
      on: {
        SUCCESS: 'success',
        ERROR: 'error'
      }
    },
    success: {},
    error: { on: { RETRY: 'loading' } },
  },
});
```

**Internationalization (i18n)**

```tsx
import { useTranslation } from 'react-i18next';

function WelcomeMessage() {
  const { t } = useTranslation();
  return <h1>{t('welcome.title')}</h1>;
}
```

**GraphQL (when REST isn't sufficient)**

```ts
import { useQuery } from '@apollo/client';
import { gql } from 'graphql-tag';

const GET_USER = gql`
  query GetUser($id: ID!) {
    user(id: $id) { id name email }
  }
`;

function UserProfile({ id }) {
  const { data, loading, error } = useQuery(GET_USER, { variables: { id } });
  // ...
}
```

**Web Workers for heavy computation**

```ts
// worker.ts
self.onmessage = (e) => {
  const result = heavyComputation(e.data);
  self.postMessage(result);
};

// main.ts
const worker = new Worker(new URL('./worker.ts', import.meta.url));
worker.postMessage(data);
worker.onmessage = (e) => console.log(e.data);
```

**Service Workers for offline/PWA**

```ts
// service-worker.ts
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
```

---

## 13a) Performance budget template

Define and enforce performance budgets in CI:

```json
// package.json
{
  "bundlesize": [
    {
      "path": "./dist/index-*.js",
      "maxSize": "100 KB",
      "compression": "gzip"
    },
    {
      "path": "./dist/vendor-*.js",
      "maxSize": "200 KB",
      "compression": "gzip"
    },
    {
      "path": "./dist/**/*.css",
      "maxSize": "50 KB",
      "compression": "gzip"
    }
  ]
}
```

**Core Web Vitals thresholds** (Lighthouse CI):

```json
// lighthouserc.json
{
  "ci": {
    "assert": {
      "preset": "lighthouse:recommended",
      "assertions": {
        "first-contentful-paint": ["error", { "maxNumericValue": 1500 }],
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }],
        "total-blocking-time": ["error", { "maxNumericValue": 300 }],
        "speed-index": ["error", { "maxNumericValue": 3000 }],
        "interactive": ["error", { "maxNumericValue": 3800 }]
      }
    }
  }
}
```

**Network conditions**:
- Test on **3G connection** (slow, realistic)
- Test on **low-end devices** (4x CPU slowdown in Chrome DevTools)

**Metrics**:
```
✅ GOOD targets:
- Initial JS bundle: <100 KB gzipped
- Time to Interactive (TTI): <3s on 3G
- First Contentful Paint (FCP): <1.5s
- Largest Contentful Paint (LCP): <2.5s
- Cumulative Layout Shift (CLS): <0.1
- First Input Delay (FID) / INP: <100ms
- Total Blocking Time (TBT): <300ms
```

---

## 13b) API design & versioning

**URL-based versioning** (recommended for public APIs):

```ts
// ✅ Version in URL path
const API_BASE = '/api/v2';

fetch(`${API_BASE}/cart`)
  .then(r => r.json());

// Easy to route different versions to different servers
// Easy to maintain multiple versions simultaneously
```

**Header-based versioning** (alternative):

```ts
// ✅ Version in Accept header
fetch('/api/cart', {
  headers: {
    'Accept': 'application/vnd.myapp.v2+json'
  }
});

// Pros: Cleaner URLs
// Cons: Harder to test in browser, less visible
```

**Breaking changes strategy**:

```ts
// 1. Add new field (non-breaking)
type CartV1 = { items: Item[] };
type CartV2 = { items: Item[], total: number };  // Added total

// 2. Deprecate old field (mark as optional)
type CartV3 = {
  items: Item[],
  total: number,
  subtotal?: number,  // Old field, deprecated
};

// 3. Remove after grace period (breaking change → new version)
type CartV4 = {
  items: Item[],
  total: number,  // subtotal removed
};

// Client-side versioning
const apiVersion = '2024-01-15';  // Date-based
fetch('/api/cart', {
  headers: { 'API-Version': apiVersion }
});
```

**Pagination, filtering, sorting conventions**:

```ts
// ✅ Consistent query parameter naming
interface ListParams {
  page?: number;          // Default: 1
  limit?: number;         // Default: 20, max: 100
  sort?: string;          // e.g., 'createdAt' or '-createdAt' (descending)
  filter?: string;        // e.g., 'status:active,price>100'
}

// Example: GET /api/products?page=2&limit=50&sort=-price&filter=inStock:true

// Response format
interface ListResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}
```

---

## 13c) Accessibility (a11y) deep-dive

**Keyboard navigation essentials**:

```tsx
// ✅ Manage tab order with tabindex
<div role="dialog" aria-modal="true">
  <button onClick={close} tabIndex={0}>Close</button>
  <input tabIndex={0} />
  <button tabIndex={0}>Submit</button>
  {/* Background content should have tabIndex={-1} or inert */}
</div>

// ✅ Trap focus within modals
function Modal({ isOpen, onClose, children }) {
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isOpen) return;

    const focusableElements = modalRef.current?.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const firstElement = focusableElements?.[0] as HTMLElement;
    const lastElement = focusableElements?.[focusableElements.length - 1] as HTMLElement;

    const handleTab = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return;

      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          lastElement?.focus();
          e.preventDefault();
        }
      } else {
        if (document.activeElement === lastElement) {
          firstElement?.focus();
          e.preventDefault();
        }
      }
    };

    document.addEventListener('keydown', handleTab);
    firstElement?.focus();

    return () => document.removeEventListener('keydown', handleTab);
  }, [isOpen]);

  return isOpen ? <div ref={modalRef} role="dialog">{children}</div> : null;
}
```

**Screen reader testing**:

- **NVDA** (Windows, free)
- **JAWS** (Windows, paid but industry standard)
- **VoiceOver** (macOS, built-in): Cmd+F5
- Test actual flow, not just "does it read something"

```tsx
// ✅ Proper labeling for screen readers
<button aria-label="Close dialog">
  <CloseIcon aria-hidden="true" />  {/* Icon is decorative */}
</button>

// ✅ Announce dynamic content changes
const [message, setMessage] = useState('');

<div role="status" aria-live="polite" aria-atomic="true">
  {message}  {/* Screen reader announces changes */}
</div>

// Use aria-live="assertive" for urgent updates
<div role="alert" aria-live="assertive">
  Error: Payment failed
</div>
```

**Color contrast** (WCAG AA minimum):

```css
/* ❌ FAIL: Insufficient contrast */
.button {
  background: #777;
  color: #999;  /* Contrast ratio: 1.5:1 */
}

/* ✅ PASS: WCAG AA (4.5:1 for normal text, 3:1 for large text) */
.button {
  background: #0066cc;
  color: #ffffff;  /* Contrast ratio: 7.5:1 */
}

/* Use tools: Chrome DevTools, WebAIM Contrast Checker */
```

**ARIA gotchas**:

```tsx
// ❌ aria-label on non-interactive elements is ignored
<div aria-label="Product details">...</div>  // Screen reader ignores!

// ✅ Use aria-label on interactive elements or semantic HTML
<section aria-labelledby="product-heading">
  <h2 id="product-heading">Product Details</h2>
</section>

// ❌ Redundant ARIA
<button role="button" aria-label="Submit">Submit</button>

// ✅ Semantic HTML doesn't need role
<button>Submit</button>  // role="button" is implicit

// ❌ Incorrect ARIA relationships
<div role="tablist">
  <button role="tab" aria-controls="panel1">Tab 1</button>
  <div id="panel1">...</div>  {/* Missing role="tabpanel" */}
</div>

// ✅ Complete ARIA pattern
<div role="tablist">
  <button role="tab" aria-controls="panel1" aria-selected="true">Tab 1</button>
</div>
<div id="panel1" role="tabpanel" aria-labelledby="tab1">...</div>
```

**Automated accessibility testing**:

```tsx
// Install jest-axe
import { axe, toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);

test('has no accessibility violations', async () => {
  const { container } = render(<MyComponent />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});

// pa11y for CI
// package.json
{
  "scripts": {
    "test:a11y": "pa11y-ci --sitemap http://localhost:3000/sitemap.xml"
  }
}
```

---

## 14) Quick naming cheat sheet

| Thing             | Convention               | Example                  |
| ----------------- | ------------------------ | ------------------------ |
| Feature folder    | kebab-case               | `features/user-profile`  |
| Component folder  | PascalCase               | `Button/`                |
| Component file    | PascalCase               | `Button.tsx`             |
| Hook              | `useCamelCase`           | `useUserProfile.ts`      |
| Utility           | `camelCase`              | `formatPrice.ts`         |
| Class             | PascalCase               | `HttpError.ts`           |
| Test              | `name.test.ts(x)`        | `CartPanel.test.tsx`     |
| Mock              | `name.mock.ts`           | `http-client.mock.ts`    |
| Styles            | mirror component         | `Button.module.css`      |
| Entry/integration | fewer `index.ts` barrels | `features/cart/index.ts` |

---

## TL;DR for the LLM agent

1. Use **feature-first structure** and **consistent naming** (kebab-case files, PascalCase components).
2. Keep **logic pure**, **effects injected**, and **contracts typed + validated** at boundaries.
3. Write **small, named-export modules** (≤200 lines) with clear file headers.
4. Favor **deterministic, well-tested** code; test seams via adapters, mock at boundaries.
5. Make debugging easy: **structured logs**, **categorized error types**, **correlation IDs**, **source maps**.
6. Automate **lint/format/type/tests** to keep the bar high; add circular dependency checks.
7. **Avoid common pitfalls**: circular deps, memory leaks, race conditions, over-abstraction, derived state duplication.
8. Use **modern React patterns**: Server Components, Suspense, concurrent features (useTransition, useDeferredValue).
9. **State management decision tree**: Server data → TanStack Query; URL → router; global → Context; local → useState.
10. **Performance**: Profile before optimizing, use virtual scrolling for long lists, prevent request waterfalls, prefer build-time CSS-in-JS.
11. **Security**: DOMPurify for XSS, strict postMessage validation, CSRF tokens for server-rendered apps.
12. **Cache invalidation**: Use invalidateQueries for safety, setQueryData for optimistic updates, understand staleTime gotchas.
13. **Accessibility**: Keyboard nav, focus trapping, screen reader testing, WCAG AA contrast, proper ARIA usage.
14. **Deployment**: CDN cache-busting, blue-green deployments, feature flag rollbacks, performance budgets in CI.
15. **Don't prematurely optimize**: Profile first, measure impact, then optimize with data.

---

## Appendix: When NOT to follow this playbook

* **Prototypes/spikes**: Skip tests, structure, and tooling until the idea is validated.
* **Trivial scripts**: Overkill for one-off utilities; use plain JS/TS.
* **Framework constraints**: Some frameworks require specific patterns (e.g., Next.js default exports for pages).
* **Legacy codebases**: Gradually adopt patterns; don't rewrite everything at once.
* **Team disagreement**: Consistency > perfection; align with team conventions first.

---

**Version**: 3.0 (2025)
**Last updated**: Based on React 19, TypeScript 5.7, TanStack Query v5, modern browser support (2023+)

**Changelog from v2.0**:
- Added error categorization & unhandled rejection handlers
- Added comprehensive anti-patterns section
- Added state management decision tree & cross-tab synchronization
- Expanded performance with React.memo gotchas, virtual scrolling, request waterfall prevention
- Expanded security with XSS/CSRF/postMessage patterns
- Added flaky test prevention & test data factories
- Added cache invalidation deep-dive
- Added tooling gotchas (case-sensitive imports, barrel files)
- Added deployment strategies (blue-green, feature flag rollback, CDN cache-busting)
- Added performance budget template with Core Web Vitals thresholds
- Added API design & versioning patterns
- Added accessibility deep-dive with keyboard nav, screen readers, WCAG contrast
