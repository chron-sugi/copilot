---
description: "Comprehensive JavaScript standards verification checklist for code reviews"
mode: 'ask'
tools: ['codebase', 'search', 'problems']
---

# JavaScript Review Checklist

Perform comprehensive standards verification against [JavaScript Core Standards](../../instructions/javascript.instructions.md).

---

## Review Context

**Component/Feature**: ${input:component:Component or feature name}

**Files to review**: ${input:files:List of file paths}

**Focus areas**: ${input:focus:All / Architecture / State / Testing / Performance / Security / A11y}

---

## Comprehensive Checklist

### 1. Architecture & Organization

**Feature-First Structure:**
- [ ] Files organized in `features/<feature>/` structure
- [ ] Components in `components/` subfolder
- [ ] Hooks in `hooks/` subfolder
- [ ] API calls in `api/` subfolder
- [ ] Types/schemas in `model/` subfolder
- [ ] Services in `services/` subfolder
- [ ] Public API exported in `index.ts`

**Module Boundaries:**
- [ ] All modules ≤200 lines
- [ ] Single responsibility per module
- [ ] Named exports used (except framework requirements)
- [ ] No circular dependencies (verify with `madge`)

**Dependency Injection:**
- [ ] Side effects injected (`fetch`, `localStorage`, `Date.now`)
- [ ] Functions accept deps parameter with defaults
- [ ] No hidden global dependencies
- [ ] Testable with mock dependencies

---

### 2. Error Handling & Logging

**Error Categorization:**
- [ ] Errors categorized (DomainError, TechnicalError, FatalError, HttpError)
- [ ] User-facing errors use DomainError
- [ ] Network/system errors use TechnicalError
- [ ] Critical failures use FatalError
- [ ] HTTP errors use HttpError with status codes

**Error.cause Chaining:**
- [ ] Original errors preserved with `.cause`
- [ ] Error context not lost during re-throws
- [ ] Meaningful error messages at each level

**Async Error Handling:**
- [ ] All promises have error handling
- [ ] No floating promises (ESLint rule enabled)
- [ ] try/catch or .catch() on all async operations
- [ ] AbortController used for cancellable requests

**Structured Logging:**
- [ ] Objects used, not string concatenation
- [ ] Correlation/trace IDs included
- [ ] Topic-based loggers used (`log('feature:action')`)
- [ ] No console.log in production code
- [ ] Logger integrates with monitoring service

**Global Error Handlers:**
- [ ] Unhandled rejection handler installed
- [ ] Global error handler installed
- [ ] Error boundaries used in React components

---

### 3. State Management

**Server State:**
- [ ] TanStack Query/SWR used for server data
- [ ] No duplication of server state in local state
- [ ] Query keys well-structured
- [ ] Stale time configured appropriately

**Derived State:**
- [ ] State computed, not stored
- [ ] useMemo only for expensive calculations (>16ms)
- [ ] No useEffect just to update derived state

**No State Duplication:**
- [ ] Single source of truth for each piece of state
- [ ] No copying server data to local state
- [ ] No storing what can be computed

**State Decision Tree Followed:**
- [ ] Server data → TanStack Query
- [ ] URL state → Search params
- [ ] Global client state → Zustand/Context
- [ ] Local state → useState

---

### 4. React Patterns (React 19+)

**Modern Patterns:**
- [ ] Server Components used by default
- [ ] Client Components only when needed (`'use client'`)
- [ ] Suspense boundaries for async data
- [ ] Streaming SSR considered

**Concurrent Features:**
- [ ] useTransition for non-urgent updates
- [ ] useDeferredValue for expensive re-renders
- [ ] use() hook for promises/context (React 19)

**Hydration:**
- [ ] No hydration mismatches
- [ ] suppressHydrationWarning used appropriately
- [ ] Client-only content handled correctly

**Error Boundaries:**
- [ ] Error boundaries at route/feature level
- [ ] Limitations understood (doesn't catch event handlers)
- [ ] try/catch used in event handlers
- [ ] Fallback UI user-friendly

---

### 5. Testing

**Testing Pyramid:**
- [ ] 70% unit tests (pure functions, utilities)
- [ ] 20% component tests (user interactions)
- [ ] 10% E2E tests (critical flows)

**Test Structure:**
- [ ] One describe block per function/component
- [ ] Arrange-Act-Assert pattern
- [ ] Meaningful test names (describe what, not how)

**Test Coverage:**
- [ ] Pure functions tested
- [ ] Error paths tested
- [ ] Edge cases covered (empty, loading, error states)
- [ ] User interactions tested (Testing Library)

**Flaky Test Prevention:**
- [ ] No arbitrary timeouts (`setTimeout`)
- [ ] waitFor() and findBy*() used for async
- [ ] Deterministic test data (no `Math.random()`, `new Date()`)
- [ ] Tests independent (no shared state)

**Test Data Factories:**
- [ ] Builders used for complex objects
- [ ] faker used for realistic data
- [ ] Overrides supported for test-specific data

**Mocking:**
- [ ] Mocked at boundaries (network, not internals)
- [ ] MSW used for API mocking
- [ ] Dependency injection enables easy mocking

---

### 6. TypeScript

**Strict Mode:**
- [ ] `strict: true` in tsconfig.json
- [ ] `noUncheckedIndexedAccess: true`
- [ ] `exactOptionalPropertyTypes: true`

**Type Safety:**
- [ ] No `any` types (use `unknown` if truly unknown)
- [ ] Proper types, not `any` or loose types
- [ ] Runtime validation at boundaries (Zod/Valibot)

**Async Safety:**
- [ ] `@typescript-eslint/no-floating-promises` enabled
- [ ] `@typescript-eslint/no-misused-promises` enabled
- [ ] `@typescript-eslint/await-thenable` enabled

---

### 7. Performance

**Bundle Size:**
- [ ] Initial bundle <100KB gzipped
- [ ] Vendor bundle <200KB gzipped
- [ ] Route chunks <50KB gzipped
- [ ] Bundle analyzer run and reviewed

**Code Splitting:**
- [ ] Routes lazy loaded
- [ ] Dynamic imports for conditional features
- [ ] Suspense boundaries for lazy components

**Virtual Scrolling:**
- [ ] Lists >100 items use virtual scrolling
- [ ] @tanstack/react-virtual or similar used

**Request Waterfalls:**
- [ ] Parallel fetching where possible
- [ ] Promise.all() for independent requests
- [ ] Suspense boundaries enable parallel fetching

**Memoization:**
- [ ] useMemo only for expensive operations (profiled)
- [ ] useCallback only with React.memo dependencies
- [ ] React.memo only for expensive re-renders
- [ ] No premature optimization

---

### 8. Security

**XSS Prevention:**
- [ ] User-generated HTML sanitized (DOMPurify)
- [ ] dangerouslySetInnerHTML avoided or sanitized
- [ ] Content Security Policy configured

**postMessage Validation:**
- [ ] Origin validated with strict equality
- [ ] Data structure validated
- [ ] Only trusted origins accepted

**CSRF Protection:**
- [ ] CSRF tokens in forms (if server-rendered)
- [ ] CSRF headers in fetch requests
- [ ] SameSite cookie attribute set

**Secrets:**
- [ ] No secrets in client code
- [ ] Environment variables for config only
- [ ] API keys not exposed

**Dependencies:**
- [ ] npm audit passing
- [ ] Dependabot/Snyk configured
- [ ] Known vulnerabilities addressed

---

### 9. Accessibility (WCAG AA)

**Contrast:**
- [ ] Normal text: 4.5:1 minimum
- [ ] Large text: 3:1 minimum
- [ ] UI components: 3:1 minimum
- [ ] Tested with contrast checker

**Keyboard Navigation:**
- [ ] All interactive elements keyboard accessible
- [ ] Focus styles visible (`:focus-visible`)
- [ ] Tab order logical
- [ ] Focus trap in modals

**Screen Reader Support:**
- [ ] Semantic HTML used (`<button>` not `<div>`)
- [ ] ARIA labels for icons/images
- [ ] Live regions for dynamic content
- [ ] Form labels associated with inputs

**Reduced Motion:**
- [ ] `prefers-reduced-motion` honored
- [ ] Animations disabled or minimal
- [ ] No auto-playing videos/carousels

**Testing:**
- [ ] jest-axe tests passing
- [ ] Keyboard navigation manually tested
- [ ] Screen reader tested (NVDA/VoiceOver)

---

### 10. Anti-Patterns (None Present)

**Architecture:**
- [ ] No circular dependencies
- [ ] No features importing other features directly
- [ ] No modules >200 lines
- [ ] No hidden global dependencies

**State:**
- [ ] No prop drilling >3 levels
- [ ] No state duplication
- [ ] No storing derived state
- [ ] No fetching in useEffect (use TanStack Query)

**React:**
- [ ] No direct state mutation
- [ ] No memory leaks (missing cleanup)
- [ ] No race conditions (stale async results)
- [ ] No premature optimization

---

## Review Output

Generate a structured report:

```markdown
# JavaScript Standards Verification

**Component/Feature**: ${component}
**Files Reviewed**: ${files}
**Date**: ${date}

## Summary
[✅ PASS | ⚠️ PARTIAL | ❌ FAIL] — X/Y checks passed

## Findings by Category

### Architecture & Organization
- ✅ Passed: [count] checks
- ⚠️ Issues: [count] checks
- ❌ Failed: [count] checks

[Details with file:line references]

### Error Handling & Logging
[Same format]

### State Management
[Same format]

... (continue for all categories)

## Critical Issues (Must Fix)
1. [Issue with file:line]
2. [Issue with file:line]

## High Priority Issues (Should Fix)
1. [Issue with file:line]
2. [Issue with file:line]

## Medium Priority Issues (Nice to Have)
1. [Issue with file:line]

## Recommendations
- [Specific recommendation]
- [Specific recommendation]

## Overall Assessment
[1-2 sentence summary and recommendation]
```

---

## Focus Mode

If reviewing specific areas only:

**Architecture Focus:**
- Review sections: 1 (Architecture), 10 (Anti-patterns)

**State Focus:**
- Review sections: 3 (State Management), 10 (Anti-patterns)

**Testing Focus:**
- Review sections: 5 (Testing)

**Performance Focus:**
- Review sections: 7 (Performance), 10 (Anti-patterns)

**Security Focus:**
- Review sections: 8 (Security)

**Accessibility Focus:**
- Review sections: 9 (Accessibility)

---

**Related**:
- [JavaScript Core Standards](../../instructions/javascript.instructions.md)
- [JavaScript Web Application Playbook](../../docs/javascript-web-app-playbook.md)
- [JS Code Reviewer Mode](../../chatmodes/javascript/js-code-reviewer.chatmode.md)
- [JS Code Review Template](./js-code-review-template.prompt.md)
