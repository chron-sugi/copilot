### 1. Planning Phase
**Before writing any code:**
- [ ] Define feature boundaries (what's in scope?)
- [ ] Identify data contracts (API schemas, types)
- [ ] Plan state management strategy (server vs local, derived state)
- [ ] Design error handling approach (error categories, retry logic)
- [ ] Define test strategy (what to test, how to test)
- [ ] Review [JavaScript Web Application Playbook](../../docs/javascript-web-app-playbook.md)

### 2. Implementation Phase
**Critical requirements** (from playbook):
- [ ] Feature-first structure: `features/<name>/` with components/, hooks/, api/, model/, services/
- [ ] Modules ≤200 lines with single responsibility
- [ ] Named exports (except framework requirements)
- [ ] Dependency injection for side effects (fetch, storage, logger, clock)
- [ ] Runtime validation at boundaries (Zod/Valibot)
- [ ] TypeScript strict mode or JSDoc + `// @ts-check`
- [ ] Error categorization (Domain/Technical/Fatal/Http)
- [ ] Structured logging with correlation IDs

### 3. Quality Assurance
**Must verify before committing:**
- [ ] All code type-safe (TypeScript strict or JSDoc)
- [ ] Error handling comprehensive (no empty catch blocks)
- [ ] Performance budgets met (bundle <100KB gzipped)
- [ ] WCAG AA compliance (4.5:1 contrast, keyboard nav)
- [ ] No circular dependencies (run `madge`)
- [ ] No security vulnerabilities (`npm audit`)
- [ ] Source maps enabled for debugging
- [ ] Cross-browser tested (Chrome, Firefox, Safari, Edge)

### 4. Testing & Documentation
**Tests required:**
- [ ] **Unit tests**: Pure functions, selectors, utilities
- [ ] **Component tests**: User interactions via Testing Library
- [ ] **Error path tests**: Network failures, timeouts, validation errors
- [ ] **Edge case tests**: Empty states, loading, long content
- [ ] **Accessibility tests**: `jest-axe`, keyboard navigation
- [ ] **Visual regression**: Chromatic, Percy, or Playwright screenshots

**Documentation deliverables:**
- [ ] JSDoc comments on public APIs
- [ ] Usage examples in Storybook or README
- [ ] Error handling documentation
- [ ] Performance considerations documented
- [ ] Migration guide if breaking changes

---

## Definition of Done

A feature is complete when:

**Code Quality:**
- ✅ Feature-first structure with clear module boundaries
- ✅ Modules ≤200 lines with single responsibility
- ✅ Dependency injection for all side effects
- ✅ No circular dependencies (verified with madge)
- ✅ Consistent naming conventions followed
- ✅ TypeScript strict mode or JSDoc + `// @ts-check`

**Error Handling & Observability:**
- ✅ Errors categorized (Domain/Technical/Fatal/Http)
- ✅ Structured logging with correlation/trace IDs
- ✅ Unhandled rejection handlers in place
- ✅ Error boundaries for React components
- ✅ Meaningful error messages for users

**State Management:**
- ✅ Server state managed with TanStack Query/SWR
- ✅ Derived state computed, not stored
- ✅ Optimistic updates with rollback implemented
- ✅ No state duplication across sources
- ✅ Single source of truth maintained

**Testing:**
- ✅ Unit tests for pure functions (>80% coverage)
- ✅ Component tests via Testing Library
- ✅ Error paths tested (network, validation)
- ✅ Edge cases covered (empty, loading, error)
- ✅ Accessibility tests passing (`jest-axe`)
- ✅ No flaky tests (proper `waitFor` usage)

**Performance:**
- ✅ Bundle size within budget (<100KB gzipped)
- ✅ Core Web Vitals met (LCP <2.5s, CLS <0.1, FID <100ms)
- ✅ Large lists virtualized (>100 items)
- ✅ Request waterfalls prevented
- ✅ Code splitting applied appropriately

**Security:**
- ✅ User-generated HTML sanitized (DOMPurify)
- ✅ postMessage origins validated strictly
- ✅ CSRF protection implemented (if needed)
- ✅ No secrets in client code
- ✅ Dependencies scanned (`npm audit` passing)

**Accessibility:**
- ✅ WCAG AA compliance (4.5:1 contrast)
- ✅ Keyboard navigation working
- ✅ `:focus-visible` styles present
- ✅ Screen reader compatible
- ✅ `prefers-reduced-motion` honored

**Documentation:**
- ✅ Public APIs documented with JSDoc
- ✅ Usage examples provided
- ✅ Error handling documented
- ✅ Performance considerations noted
- ✅ Migration guide (if breaking changes)

---

## Feature Development Template

### Step 1: Create Feature Structure

```bash
features/<feature-name>/
  ├── components/           # UI components
  │   ├── FeaturePanel/
  │   │   ├── FeaturePanel.tsx
  │   │   ├── FeaturePanel.test.tsx
  │   │   └── FeaturePanel.module.css
  ├── hooks/                # React hooks
  │   ├── useFeature.ts
  │   └── useFeature.test.ts
  ├── api/                  # Network calls
  │   ├── get-feature.ts
  │   └── update-feature.ts
  ├── model/                # Types, schemas, selectors
  │   ├── feature.types.ts
  │   ├── feature.schema.ts
  │   └── feature.selectors.ts
  ├── services/             # Orchestration
  │   ├── feature.service.ts
  │   └── feature.service.test.ts
  └── index.ts              # Public API (named exports)
```

### Step 2: Define Data Contract

```typescript
// model/feature.schema.ts
import { z } from 'zod';

export const FeatureItem = z.object({
  id: z.string(),
  name: z.string(),
  status: z.enum(['active', 'inactive']),
  createdAt: z.string().datetime(),
});

export const Feature = z.object({
  items: z.array(FeatureItem),
  total: z.number().nonnegative(),
});

export type Feature = z.infer<typeof Feature>;
export type FeatureItem = z.infer<typeof FeatureItem>;
```

### Step 3: Implement API Layer with DI

```typescript
// api/get-feature.ts
import { Feature } from '../model/feature.schema';

type Deps = {
  fetchFn?: typeof fetch;
  signal?: AbortSignal;
};

export async function getFeature(
  id: string,
  { fetchFn = fetch, signal }: Deps = {}
): Promise<Feature> {
  const res = await fetchFn(`/api/features/${id}`, {
    headers: { 'Accept': 'application/json' },
    signal,
  });

  if (!res.ok) {
    throw new HttpError(`Failed to load feature: ${res.status}`, res.status);
  }

  const json = await res.json();
  return Feature.parse(json); // Runtime validation
}
```

### Step 4: Create Service Layer

```typescript
// services/feature.service.ts
import { getFeature } from '../api/get-feature';
import type { Feature } from '../model/feature.schema';

type Deps = Parameters<typeof getFeature>[1];

export async function loadFeatureSummary(
  id: string,
  deps?: Deps
): Promise<{ count: number; activeCount: number }> {
  const feature = await getFeature(id, deps);

  return {
    count: feature.items.length,
    activeCount: feature.items.filter(item => item.status === 'active').length,
  };
}
```

### Step 5: Implement React Component

```tsx
// components/FeaturePanel/FeaturePanel.tsx
import { useQuery } from '@tanstack/react-query';
import { getFeature } from '../../api/get-feature';
import type { Feature } from '../../model/feature.types';

interface FeaturePanelProps {
  featureId: string;
}

export function FeaturePanel({ featureId }: FeaturePanelProps) {
  const { data: feature, isLoading, error } = useQuery({
    queryKey: ['feature', featureId],
    queryFn: () => getFeature(featureId),
  });

  if (isLoading) return <LoadingSkeleton />;
  if (error) return <ErrorMessage error={error} />;
  if (!feature) return null;

  return (
    <div className="feature-panel">
      <h2>{feature.items.length} Items</h2>
      <ul>
        {feature.items.map(item => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

### Step 6: Write Comprehensive Tests

```typescript
// services/feature.service.test.ts
import { loadFeatureSummary } from './feature.service';
import { buildFeature } from '@/shared/test-utils/builders';

describe('loadFeatureSummary', () => {
  test('computes count and activeCount', async () => {
    const mockFeature = buildFeature({
      items: [
        { id: '1', name: 'A', status: 'active', createdAt: '2025-01-01T00:00:00Z' },
        { id: '2', name: 'B', status: 'inactive', createdAt: '2025-01-02T00:00:00Z' },
      ],
    });

    const fetchFn = async () =>
      new Response(JSON.stringify(mockFeature), { status: 200 });

    const result = await loadFeatureSummary('123', { fetchFn });

    expect(result).toEqual({ count: 2, activeCount: 1 });
  });

  test('throws on network error', async () => {
    const fetchFn = async () => new Response(null, { status: 500 });

    await expect(loadFeatureSummary('123', { fetchFn }))
      .rejects.toThrow('Failed to load feature: 500');
  });
});
```

---

## Error Handling Implementation

### 1. Define Error Classes

```typescript
// shared/lib/errors/error-types.ts

// User-facing errors: show to user, don't retry
export class DomainError extends Error {
  constructor(
    message: string,
    public readonly userMessage: string,
    cause?: unknown
  ) {
    super(message);
    this.name = 'DomainError';
    if (cause) this.cause = cause;
  }
}

// Technical errors: log & retry with backoff
export class TechnicalError extends Error {
  constructor(
    message: string,
    public readonly retryable: boolean = true,
    cause?: unknown
  ) {
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

### 2. Implement Structured Logging

```typescript
// shared/lib/logger/logger.ts
export const log = (topic: string) => ({
  debug: (details: unknown, msg?: string) =>
    console.debug({ topic, timestamp: Date.now(), ...details }, msg),
  error: (details: unknown, msg?: string) =>
    console.error({ topic, timestamp: Date.now(), ...details }, msg),
});

// Usage
const logger = log('feature:load');
logger.error({ featureId, traceId, error }, 'Failed to load feature');
```

### 3. Add Global Error Handlers

```typescript
// app/error-handlers.ts

// Unhandled promise rejections
window.addEventListener('unhandledrejection', (event) => {
  logger.error({
    reason: event.reason,
    promise: event.promise,
  }, 'Unhandled promise rejection');

  event.preventDefault();
});

// Global errors
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

---

## State Management Patterns

### Decision Tree

```
Is it server data (API, database)?
├─ YES → TanStack Query / SWR
└─ NO → Continue...

Should it persist in the URL?
├─ YES → Router state (search params, path params)
└─ NO → Continue...

Do multiple distant components need it?
├─ YES → Is it global & changes rarely?
│   ├─ YES → Context API
│   └─ NO → Zustand / Jotai
└─ NO → useState (component-local)
```

### Optimistic Updates Pattern

```tsx
const mutation = useMutation({
  mutationFn: updateFeature,

  onMutate: async (newFeature) => {
    // Cancel outgoing refetches
    await queryClient.cancelQueries({ queryKey: ['feature'] });

    // Snapshot for rollback
    const previous = queryClient.getQueryData(['feature']);

    // Optimistically update
    queryClient.setQueryData(['feature'], newFeature);

    return { previous };
  },

  onError: (err, newFeature, context) => {
    // Rollback on error
    if (context?.previous) {
      queryClient.setQueryData(['feature'], context.previous);
    }
    toast.error('Failed to update feature');
  },

  onSettled: () => {
    // Refetch to ensure sync
    queryClient.invalidateQueries({ queryKey: ['feature'] });
  },
});
```

---

## Performance Optimization

### 1. Code Splitting

```tsx
// Lazy load routes
const Dashboard = lazy(() => import('./pages/Dashboard'));

<Suspense fallback={<Loading />}>
  <Dashboard />
</Suspense>
```

### 2. Virtual Scrolling (>100 items)

```tsx
import { useVirtualizer } from '@tanstack/react-virtual';

function LargeList({ items }) {
  const parentRef = useRef(null);
  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
  });

  return (
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      <div style={{ height: `${virtualizer.getTotalSize()}px` }}>
        {virtualizer.getVirtualItems().map(virtualRow => (
          <div
            key={virtualRow.index}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              transform: `translateY(${virtualRow.start}px)`,
            }}
          >
            {items[virtualRow.index].name}
          </div>
        ))}
      </div>
    </div>
  );
}
```

### 3. Prevent Request Waterfalls

```tsx
// ❌ Sequential waterfalls
const user = await getUser();
const posts = await getPosts(user.id);

// ✅ Parallel fetching
const [user, categories] = await Promise.all([
  getUser(),
  getCategories()
]);
```

---

## Accessibility Implementation

### Keyboard Navigation

```tsx
function Dialog({ isOpen, onClose, children }) {
  const dialogRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isOpen) return;

    const focusableElements = dialogRef.current?.querySelectorAll(
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

  return isOpen ? (
    <div ref={dialogRef} role="dialog" aria-modal="true">
      {children}
    </div>
  ) : null;
}
```

### WCAG AA Compliance

```css
/* Color contrast: 4.5:1 for normal text, 3:1 for large text */
.button {
  background: #0066cc;
  color: #ffffff; /* Contrast ratio: 7.5:1 ✅ */
}

/* Focus visible styles */
.button:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Related Resources

**Standards & Modes:**
- [JavaScript Web Application Playbook](../../docs/javascript-web-app-playbook.md) — Comprehensive standards
- [JS Code Reviewer Mode](./js-code-reviewer.chatmode.md) — Review standards
- [JS Debugger Mode](./js-debugger.chatmode.md) — Debugging patterns
- [JS Refactorer Mode](./js-refactorer.chatmode.md) — Refactoring patterns
- [JS Test Engineer Mode](./js-test-engineer.chatmode.md) — Testing strategies

---

## Remember

Your goal is to ship **production-ready features** that are:
- Testable and well-tested
- Observable and debuggable
- Performant and accessible
- Secure and maintainable
- Following feature-first architecture

Prioritize **quality over speed**. Write code that's easy to understand, test, and change.

---

**Last Updated:** 2025-01-09
**Maintained by:** JavaScript Architecture Team
