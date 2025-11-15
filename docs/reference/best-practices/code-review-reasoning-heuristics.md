# Code Review Reasoning Heuristics

**Purpose**: Explicit reasoning heuristics for LLM agents performing code review to ensure predictable, thorough, and standards-compliant reviews.

**Scope**: CSS, JavaScript, TypeScript, React

**Last Updated**: 2025-11-15

---

## Overview

This document defines **48 reasoning heuristics** organized into:

1. **Meta-heuristics (1-5)**: How the agent thinks before reviewing code
2. **Code-level heuristics (6-12)**: What to look for in the code
3. **Testing & verification heuristics (13-15)**: Test coverage and verification
4. **Interaction heuristics (16-20)**: How to communicate findings
5. **Self-checking heuristics (21-23)**: Agent quality control
6. **CSS-specific heuristics (24-32)**: Domain-specific CSS rules
7. **JavaScript-specific heuristics (33-45)**: Domain-specific JS/TS/React rules
8. **Cross-cutting heuristics (46-48)**: Rules for all web code

---

## 1. Meta-Heuristics (How the Agent Thinks Before Touching Code)

### Heuristic 1: Context First, Changes Second

**Rule**: Always read in this order:
1. Problem statement → Requirements → Existing code → Diff/proposed change
2. Summarize in 1-3 sentences what the code *is supposed* to do before critiquing

**Rationale**: Understanding intent prevents suggesting changes that fix style but break functionality.

**Example**: Before reviewing a refactor, state: "This change extracts authentication logic into a reusable hook to reduce duplication across three components."

---

### Heuristic 2: Assume the Spec is Primary, Not the Current Code

**Rule**:
- If code and requirements disagree, treat the requirements as the source of truth
- Explicitly call out: "Code matches/does not match the stated intent because…"

**Rationale**: Code often drifts from original intent; requirements clarify what's correct.

**Example**: "The requirement states 'users must confirm deletion,' but this code auto-deletes on button click without confirmation."

---

### Heuristic 3: Minimize Disruption

**Rule**:
- Prefer the smallest change that:
  - Fixes the bug, OR
  - Meets the requirement
- Avoid refactors unless requested or absolutely required for correctness

**Rationale**: Large refactors increase risk and review time; ship incremental improvements.

**Example**: Don't suggest rewriting an entire component when adding a single prop fix solves the issue.

---

### Heuristic 4: Review by Priority Order

**Rule**: Always reason in this order:
1. **Correctness & bugs** (Does it work?)
2. **Security / data safety** (Is it safe?)
3. **Performance** (Is it fast enough?)
4. **Maintainability & readability** (Can others understand it?)
5. **Style / formatting** (Does it look consistent?)

**Rationale**: A perfectly styled, fast, readable function that returns wrong results is worthless.

**Example**: Report the XSS vulnerability before suggesting the variable be renamed.

---

### Heuristic 5: Explain Reasoning at a High Level

**Rule**:
- Provide *just enough* explanation for a human developer
- Avoid verbose step-by-step chain-of-thought
- Format: "This will fail for [edge case] because [reason]"

**Rationale**: Developers need actionable insights, not AI reasoning traces.

**Example**:
- ✅ "This will fail for empty arrays because `.shift()` returns `undefined`"
- ❌ "Let me analyze this code. First, I see a `.shift()` call. Then I consider what happens when... [300 words]"

---

## 2. Code-Level Heuristics (What to Look for in the Code)

### Heuristic 6: Invariants & Edge Cases First

**Rule**:
- Ask: "What must *always* be true here?"
- Check edge cases: empty input, null/undefined, large values, bad data, timeouts

**Rationale**: Edge cases cause production bugs; happy paths are usually correct.

**Example**: For a `getUserById(id)` function, check:
- What if `id` is null?
- What if the user doesn't exist?
- What if the database is down?

---

### Heuristic 7: Input-Output Contract Checking

**Rule**:
For each function/class, identify:
- Expected inputs (types, shapes, allowed ranges)
- Expected outputs
- Flag any code that violates that contract or doesn't guard against bad inputs

**Rationale**: Explicit contracts prevent runtime type errors and undefined behavior.

**Example**:
```typescript
// ❌ No contract enforcement
function calculateDiscount(price, percent) {
  return price * (percent / 100);
}

// ✅ Contract enforced
function calculateDiscount(price: number, percent: number): number {
  if (price < 0 || percent < 0 || percent > 100) {
    throw new DomainError('Invalid discount parameters', { price, percent });
  }
  return price * (percent / 100);
}
```

---

### Heuristic 8: Data-Flow and State Sanity

**Rule**:
- Trace how data moves: params → local vars → return value → consumers
- Be suspicious of:
  - Hidden globals
  - Shared mutable state
  - Implicit side-effects
- Call out anything that can cause race conditions or inconsistent state

**Rationale**: Unpredictable state is the #1 source of hard-to-debug issues.

**Example**: Flag a function that modifies a global variable without documentation.

---

### Heuristic 9: Error Handling Heuristics

**Rule**:
Check that errors are:
- Caught where appropriate
- Logged or surfaced to users
- Not silently swallowed

Prefer explicit error paths over "catch all and ignore."

**Rationale**: Silent failures cause data corruption and poor user experience.

**Example**:
```javascript
// ❌ Silent failure
try {
  await saveUserData(data);
} catch (e) {
  // Ignored
}

// ✅ Explicit handling
try {
  await saveUserData(data);
} catch (error) {
  logger.error({ userId: data.id, error }, 'Failed to save user data');
  throw new TechnicalError('Could not save user data', { cause: error });
}
```

---

### Heuristic 10: Security Heuristics

**Rule**:
Scan for unsafe patterns:
- Direct string concatenation in SQL, shell, or HTML
- Unvalidated user input
- Secrets in code

Recommend concrete safer patterns (parameterized queries, escaping, DOMPurify, etc.).

**Rationale**: Security vulnerabilities cause data breaches and reputational damage.

**Example**: Flag `innerHTML = userInput` and recommend `DOMPurify.sanitize(userInput)`.

---

### Heuristic 11: Complexity & Readability Threshold

**Rule**:
- If a function is doing "too many things" (multiple responsibilities), suggest splitting
- If logic is deeply nested (>3 levels), suggest guard clauses or decomposition
- Prefer clear, intention-revealing names over comments that explain bad names

**Rationale**: Complex code is bug-prone and hard to maintain.

**Example**:
```javascript
// ❌ Deeply nested
function processUser(user) {
  if (user) {
    if (user.isActive) {
      if (user.hasPermission) {
        // ... 20 lines of logic
      }
    }
  }
}

// ✅ Guard clauses
function processUser(user) {
  if (!user) return;
  if (!user.isActive) return;
  if (!user.hasPermission) return;

  // ... 20 lines of logic
}
```

---

### Heuristic 12: Performance Sanity Checks

**Rule**:
Only critique performance when there's an obvious red flag:
- Unnecessary O(n²) loops
- Repeated expensive calls inside loops
- Synchronous blocking in hot paths

Don't prematurely optimize otherwise.

**Rationale**: Premature optimization wastes time; fix actual bottlenecks.

**Example**: Flag `array.map().filter().map()` and suggest combining passes.

---

## 3. Testing & Verification Heuristics

### Heuristic 13: Think in Tests

**Rule**:
For every non-trivial change, imagine at least 2-3 tests:
- "Happy path"
- At least one edge case
- At least one failure case

If tests are missing, suggest them specifically: which inputs, what expected outputs.

**Rationale**: Untested code is broken code waiting to be discovered.

**Example**: "Add tests for: (1) valid user login, (2) invalid password, (3) non-existent user."

---

### Heuristic 14: Prefer Tests Over Speculation

**Rule**:
When unsure if something's safe, formulate it as a test recommendation instead of guessing.

**Rationale**: Tests provide proof; speculation creates confusion.

**Example**:
- ❌ "This probably handles null correctly"
- ✅ "Add a test where `userId` is null and verify the function returns an error"

---

### Heuristic 15: Check Consistency Between Code and Tests

**Rule**:
If tests exist:
- Make sure they actually cover the change
- Call out mismatches: "This test says behavior X, but code implements Y"

**Rationale**: Outdated tests are worse than no tests—they create false confidence.

**Example**: "The test expects the function to throw, but the code now returns null instead."

---

## 4. Interaction Heuristics (How the Code Reviewer Agent Responds)

### Heuristic 16: Be Specific, Not Vague

**Rule**:
Avoid "this is bad" or "this is not ideal."

Always include:
- The exact location / snippet
- The reason
- A concrete suggestion

**Rationale**: Vague feedback wastes developer time.

**Example**:
- ❌ "The error handling could be better"
- ✅ "In `UserService.ts:42`, the catch block silently swallows errors. Add logging and re-throw a TechnicalError with the original error as `cause`."

---

### Heuristic 17: Separate Hard Blockers from Nits

**Rule**:
Distinguish:
- **CRITICAL/HIGH**: Must fix before merge (security, bugs, data loss)
- **MEDIUM**: Strong suggestions (architecture, performance, maintainability)
- **LOW**: Nice-to-have / style (formatting, naming)

**Rationale**: This prevents over-correction and helps developers prioritize.

**Example**: Use severity labels consistently:
- 🚫 **BLOCKER**: XSS vulnerability in user input handling
- ⚠️ **MEDIUM**: Function exceeds 50-line limit
- ℹ️ **LOW**: Variable could be renamed for clarity

---

### Heuristic 18: Preserve Author's Intent and Style Where Reasonable

**Rule**:
- Don't rewrite the whole file "because it can be prettier"
- Only propose larger refactors when:
  - There's duplicated logic
  - Complexity is clearly harming correctness

**Rationale**: Respect the author's approach unless it's causing real problems.

**Example**: Don't suggest switching from `map` to `forEach` if both work equally well.

---

### Heuristic 19: Avoid Hallucinated APIs and Patterns

**Rule**:
- Prefer patterns already present in the codebase
- If suggesting a new API or library, explicitly say: "If this project uses X, consider…; otherwise keep the current approach"

**Rationale**: Hallucinated APIs waste developer time and erode trust.

**Example**:
- ❌ "Use the `validateUser()` utility" (when it doesn't exist)
- ✅ "If the project has a user validation utility, use it here. Otherwise, add inline validation."

---

### Heuristic 20: Defer to Existing Conventions

**Rule**:
If the project clearly uses a pattern (naming, file layout, error style), follow it unless it's causing clear bugs.

**Rationale**: Consistency is more valuable than personal preference.

**Example**: If the project uses `snake_case` for CSS custom properties, don't suggest `camelCase`.

---

## 5. Self-Checking Heuristics (For the LLM Itself)

### Heuristic 21: Double-Check Diffs That Change Behavior

**Rule**:
Before finalizing suggestions, quickly re-read:
- "Does this change really preserve behavior except where I intend to change it?"
- If it might be breaking, label it explicitly as a behavior change

**Rationale**: Unintended behavior changes cause bugs.

**Example**: Before suggesting a refactor, verify it produces the same outputs for the same inputs.

---

### Heuristic 22: Avoid Overconfidence When Uncertain

**Rule**:
If the context is incomplete, say so:
- "Based on the visible code, this might be an issue if…"
- Suggest follow-ups: "Check file X / config Y to confirm"

**Rationale**: Admitting uncertainty is better than guessing wrong.

**Example**: "I don't see the `UserSchema` definition. If it allows null emails, this validation may fail."

---

### Heuristic 23: Prefer Incremental Guidance Over Full Rewrites

**Rule**:
- When the code is mostly fine, suggest small patches instead of dumping a fully new version
- Full rewrites should be rare and clearly motivated

**Rationale**: Small changes are easier to review and less likely to introduce bugs.

**Example**: Suggest changing 3 lines instead of rewriting a 100-line function.

---

## 6. CSS-Specific Heuristics

### Heuristic 24: Specificity Budget Enforcement

**Rule**:
- Calculate specificity of all selectors before approving CSS
- **BLOCKER**: Any selector exceeding (0,1,0) without `:where()` wrapper
- **Tool check**: Run `python scripts/css-specificity-checker.py`

**Rationale**: High specificity causes cascade conflicts and makes components impossible to override.

**Example**:
```css
/* ❌ BLOCKER - specificity (0,2,0) */
.c-button.c-button--primary { }

/* ✅ Acceptable - specificity (0,1,0) via :where() */
.c-button:where(.c-button--primary) { }

/* ✅ Better - specificity (0,1,0) via data attribute */
.c-button[data-variant="primary"] { }
```

**Reference**: See [docs/reference/css-architecture-reference.md](../../css-architecture-reference.md) for specificity guidelines.

---

### Heuristic 25: Cascade Layer Verification

**Rule**:
Check that all CSS is assigned to the correct `@layer`.

**Expected order**: `reset → base → tokens → utilities → objects → components → overrides`

**BLOCKER** if:
- Component styles in utility layer
- Utilities in component layer
- No `@layer` declaration for new CSS

**Rationale**: The system depends on explicit layer ordering for predictable cascade behavior.

**Example**:
```css
/* ❌ BLOCKER - component in wrong layer */
@layer utilities {
  .c-card { /* components should be in @layer components */ }
}

/* ✅ Correct layer assignment */
@layer components {
  .c-card { }
}
```

**Reference**: See [raw/instructions/css.instructions.md](../../../raw/instructions/css.instructions.md) for layer strategy.

---

### Heuristic 26: Design Token Contract

**Rule**:
Verify all hardcoded values should be custom properties.

**BLOCKER**: Any color/spacing/typography value not referencing a token

**Exceptions** (allowed hardcoded values):
- Intrinsic values: `0`, `1px`, `100%`, `inherit`, `currentColor`, `auto`
- Component-specific calculations: `calc(var(--space-4) + 2px)`

**Check**: Does the value appear in your design token registry?

**Rationale**: Hardcoded values break theming and design system consistency.

**Example**:
```css
/* ❌ BLOCKER - hardcoded color */
.c-button {
  background-color: #3b82f6;
}

/* ✅ Uses design token */
.c-button {
  background-color: var(--color-primary-500);
}
```

**Reference**: See token definitions in [raw/instructions/css.instructions.md](../../../raw/instructions/css.instructions.md).

---

### Heuristic 27: BEM Naming Compliance

**Rule**:
All component classes must follow naming conventions:
- Components: `c-componentName__element--modifier`
- Objects: `o-*` (layout primitives)
- Utilities: `u-*` (single-purpose)
- State: `is-*` (active, disabled, loading)
- Context: `has-*` (has-dropdown, has-icon)

**BLOCKER**: Mixed naming conventions (e.g., `camelCase` mixed with `kebab-case`, or arbitrary class names)

**Tool check**: Regex pattern validation in Stylelint

**Rationale**: Consistent naming makes the system predictable and prevents class name collisions.

**Example**:
```css
/* ❌ BLOCKER - inconsistent naming */
.Button { }
.button_text { }
.button-primary { }

/* ✅ Consistent BEM */
.c-button { }
.c-button__text { }
.c-button--primary { }
```

**Reference**: See BEM guidelines in [raw/instructions/css.instructions.md](../../../raw/instructions/css.instructions.md).

---

### Heuristic 28: Variant API Pattern

**Rule**:
Components should use `data-variant="value"` not modifier classes for variant props.

**BLOCKER**: More than 3 variant modifier classes on a single component (suggests `data-*` migration needed)

**Rationale**: Data attributes create cleaner component APIs and prevent class explosion.

**Example**:
```html
<!-- ❌ Class explosion (4 variants) -->
<button class="c-button c-button--primary c-button--large c-button--rounded c-button--icon">

<!-- ✅ Clean data-attribute API -->
<button class="c-button"
        data-variant="primary"
        data-size="large"
        data-rounded="true"
        data-icon="true">
```

**CSS**:
```css
/* ✅ Style variants via data attributes */
.c-button[data-variant="primary"] { }
.c-button[data-size="large"] { }
```

**Reference**: See component API patterns in [raw/instructions/css.instructions.md](../../../raw/instructions/css.instructions.md).

---

### Heuristic 29: Container Query Appropriateness

**Rule**:
- **Component-level responsiveness** → container queries (`@container`)
- **Global layout responsiveness** → media queries (`@media`)

**BLOCKER**: Media queries inside component CSS that change component internals (should be container queries)

**Check**: Is the breakpoint about the component's size or the viewport?

**Rationale**: Container queries make components portable across different layouts.

**Example**:
```css
/* ❌ BLOCKER - media query for component internals */
.c-card__title {
  font-size: 1rem;
}

@media (min-width: 768px) {
  .c-card__title {
    font-size: 1.5rem; /* Component cares about viewport, not container */
  }
}

/* ✅ Container query for component responsiveness */
.c-card {
  container-type: inline-size;
  container-name: card;
}

.c-card__title {
  font-size: 1rem;
}

@container card (min-width: 400px) {
  .c-card__title {
    font-size: 1.5rem; /* Component cares about its own width */
  }
}
```

**Reference**: See responsive patterns in [raw/instructions/css.instructions.md](../../../raw/instructions/css.instructions.md).

---

### Heuristic 30: Performance Budget Check

**Rule**:
- CSS bundle must be **<50KB gzipped**
- **STRONG SUGGESTION**: Split CSS >40KB into critical + deferred
- **BLOCKER**: Adding styles that push bundle >60KB

**Tool check**: Analyze bundle size report from build output

**Rationale**: Large CSS files block rendering and harm Core Web Vitals.

**Actions**:
- If >40KB: Suggest code-splitting by route or feature
- If >50KB: Require splitting plan before approval
- If >60KB: Block merge

**Reference**: See performance budgets in [raw/instructions/css.instructions.md](../../../raw/instructions/css.instructions.md).

---

### Heuristic 31: Accessibility Pattern Verification

**Rule**:
All interactive states must have appropriate accessibility features:
- **BLOCKER**: Interactive elements without `:focus-visible` styles
- **BLOCKER**: Animations without `prefers-reduced-motion` fallback
- **BLOCKER**: Color-only state indicators (need icon/text/pattern too)

**Check media queries**:
- `@media (prefers-reduced-motion: reduce)` - disable/simplify animations
- `@media (forced-colors: active)` - high contrast mode support
- `@media (prefers-contrast: more)` - enhanced contrast

**Rationale**: Accessibility is a baseline requirement, not optional.

**Example**:
```css
/* ❌ BLOCKER - no reduced motion support */
.c-modal {
  animation: slideIn 300ms ease-out;
}

/* ✅ Respects user motion preferences */
.c-modal {
  animation: slideIn 300ms ease-out;
}

@media (prefers-reduced-motion: reduce) {
  .c-modal {
    animation: none;
  }
}

/* ❌ BLOCKER - color-only indicator */
.c-input--error {
  border-color: red;
}

/* ✅ Multi-sensory indicator */
.c-input--error {
  border-color: var(--color-error-500);
  border-width: 2px; /* Visual difference */
}

.c-input--error::after {
  content: '⚠'; /* Icon indicator */
}
```

**Reference**: See accessibility requirements in [raw/instructions/css.instructions.md](../../../raw/instructions/css.instructions.md).

---

### Heuristic 32: Animation GPU-Acceleration Check

**Rule**:
Only animate properties that can be GPU-accelerated:
- **Allowed**: `transform`, `opacity`, `filter`, `backdrop-filter`
- **BLOCKER**: Animating `left`, `top`, `width`, `height`, `margin`, `padding` (triggers layout)

**Suggestion**: Rewrite layout animations using `transform`.

**Rationale**: Layout-triggering animations cause jank and poor performance.

**Example**:
```css
/* ❌ BLOCKER - triggers layout (reflow) */
@keyframes slideIn {
  from { left: -100px; }
  to { left: 0; }
}

/* ✅ GPU-accelerated via transform */
@keyframes slideIn {
  from { transform: translateX(-100px); }
  to { transform: translateX(0); }
}

/* ❌ BLOCKER - triggers layout */
.c-dropdown {
  transition: height 300ms;
}

/* ✅ GPU-accelerated via transform */
.c-dropdown {
  transition: transform 300ms;
}
```

**Reference**: See performance guidelines in [raw/instructions/css.instructions.md](../../../raw/instructions/css.instructions.md).

---

## 7. JavaScript-Specific Heuristics

### Heuristic 33: Error Classification Check

**Rule**:
All thrown errors must extend one of the project's error classes:
- `DomainError` - business logic violations
- `TechnicalError` - infrastructure/API failures
- `FatalError` - unrecoverable errors
- `HttpError` - HTTP-specific errors

**BLOCKER**: Raw `throw new Error("message")` without classification

**Rationale**: Error types enable retry logic, proper logging, and user-facing error messages.

**Example**:
```javascript
// ❌ BLOCKER - unclassified error
function transferMoney(from, to, amount) {
  if (amount <= 0) {
    throw new Error('Invalid amount');
  }
}

// ✅ Classified domain error
function transferMoney(from, to, amount) {
  if (amount <= 0) {
    throw new DomainError('Transfer amount must be positive', {
      amount,
      from,
      to
    });
  }
}
```

**Reference**: See error handling in [raw/instructions/javascript.instructions.md](../../../raw/instructions/javascript.instructions.md).

---

### Heuristic 34: Error.cause Chain Verification

**Rule**:
When catching and re-throwing, must include `{ cause: originalError }`.

**BLOCKER**: Catch blocks that re-throw without preserving the original error.

**Check**: Search for `catch` blocks that don't preserve context.

**Rationale**: Error cause chains enable debugging by preserving the full error history.

**Example**:
```javascript
// ❌ BLOCKER - lost original error
try {
  await fetchUserData(userId);
} catch (error) {
  throw new TechnicalError('Failed to load user');
}

// ✅ Preserves error chain
try {
  await fetchUserData(userId);
} catch (error) {
  throw new TechnicalError('Failed to load user', {
    cause: error,
    userId
  });
}
```

**Reference**: See error handling in [raw/instructions/javascript.instructions.md](../../../raw/instructions/javascript.instructions.md).

---

### Heuristic 35: Structured Logging Pattern

**Rule**:
All logs must be objects, not strings:
- Format: `logger.info({ userId, action }, "message")`
- Must include correlation ID for request tracing
- **BLOCKER**: `console.log()` or string-only logs in production code

**Tool check**: ESLint rule `no-console` + custom logger enforcement

**Rationale**: Structured logs enable filtering, searching, and correlation in production.

**Example**:
```javascript
// ❌ BLOCKER - string logging
console.log('User logged in: ' + userId);

// ❌ BLOCKER - string-only log
logger.info('User logged in');

// ✅ Structured logging
logger.info({
  userId,
  correlationId: req.correlationId,
  timestamp: Date.now()
}, 'User logged in');
```

**Reference**: See logging standards in [raw/instructions/javascript.instructions.md](../../../raw/instructions/javascript.instructions.md).

---

### Heuristic 36: Feature-First Module Boundary

**Rule**:
Files must follow feature-first structure:
- `features/*/` - feature modules
- `shared/*` - shared utilities

**BLOCKER**: Cross-feature imports (e.g., `import from '../../otherFeature'`)

**Tool check**: Run `npx madge --circular` to detect violations

**Rationale**: Feature boundaries prevent tight coupling and enable independent development.

**Example**:
```javascript
// ❌ BLOCKER - cross-feature import
// File: features/orders/OrderList.tsx
import { UserAvatar } from '../../users/UserAvatar';

// ✅ Import from shared
// File: features/orders/OrderList.tsx
import { UserAvatar } from '@/shared/components/UserAvatar';
```

**File structure**:
```
features/
  orders/
    OrderList.tsx
    OrderDetail.tsx
  users/
    UserProfile.tsx
shared/
  components/
    UserAvatar.tsx  ← Shared by multiple features
```

**Reference**: See architecture in [raw/instructions/javascript.instructions.md](../../../raw/instructions/javascript.instructions.md).

---

### Heuristic 37: Dependency Injection Verification

**Rule**:
Functions must accept side effects as parameters for testability:
- `fetch`, `localStorage`, `Date.now`, `Math.random`, `window`, `document`

**BLOCKER**: Direct usage of side effects in business logic

**Check**: Can this function be tested without mocking globals?

**Rationale**: Dependency injection enables unit testing without complex mocks.

**Example**:
```javascript
// ❌ BLOCKER - hardcoded dependencies
async function saveUser(user) {
  const timestamp = Date.now();
  await fetch('/api/users', {
    method: 'POST',
    body: JSON.stringify({ ...user, timestamp })
  });
}

// ✅ Dependencies injected
async function saveUser(
  user,
  { fetch, getTimestamp = Date.now }
) {
  const timestamp = getTimestamp();
  await fetch('/api/users', {
    method: 'POST',
    body: JSON.stringify({ ...user, timestamp })
  });
}

// Easy to test
test('saveUser includes timestamp', async () => {
  const mockFetch = jest.fn();
  const mockTimestamp = () => 1234567890;

  await saveUser(
    { name: 'John' },
    { fetch: mockFetch, getTimestamp: mockTimestamp }
  );

  expect(mockFetch).toHaveBeenCalledWith('/api/users', {
    method: 'POST',
    body: JSON.stringify({ name: 'John', timestamp: 1234567890 })
  });
});
```

**Reference**: See testing patterns in [raw/instructions/javascript.instructions.md](../../../raw/instructions/javascript.instructions.md).

---

### Heuristic 38: State Management Decision Tree

**Rule**:
Choose state management based on data source:
- **Server data** → TanStack Query (or similar cache)
- **Local UI state** → `useState` / `useReducer`
- **Derived state** → `useMemo` or direct computation
- **URL state** → Query parameters or route params

**BLOCKER**: Duplicating server data in local state

**Check**: Is this state already available from the server cache?

**Rationale**: Duplicated state causes sync issues and bugs.

**Example**:
```javascript
// ❌ BLOCKER - duplicating server state
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(r => r.json())
      .then(setUser);
  }, [userId]);

  return <div>{user?.name}</div>;
}

// ✅ Use server cache (TanStack Query)
function UserProfile({ userId }) {
  const { data: user } = useQuery({
    queryKey: ['users', userId],
    queryFn: () => fetch(`/api/users/${userId}`).then(r => r.json())
  });

  return <div>{user?.name}</div>;
}

// ❌ BLOCKER - duplicating derived state
function Cart({ items }) {
  const [total, setTotal] = useState(0);

  useEffect(() => {
    setTotal(items.reduce((sum, item) => sum + item.price, 0));
  }, [items]);
}

// ✅ Derive on render
function Cart({ items }) {
  const total = items.reduce((sum, item) => sum + item.price, 0);
}
```

**Reference**: See state management in [raw/instructions/javascript.instructions.md](../../../raw/instructions/javascript.instructions.md).

---

### Heuristic 39: React 19+ Pattern Enforcement

**Rule**:
Use modern React patterns:
- **Server Components by default** (no `'use client'` unless needed)
- **Suspense boundaries** for async data loading
- **`use()` hook** for promises instead of `useEffect` data fetching

**STRONG SUGGESTION**: Migrate `useEffect` data fetching to `use()` hook

**Check**: Is this pattern aligned with React 19 best practices?

**Rationale**: Modern patterns improve performance and developer experience.

**Example**:
```javascript
// ❌ Old pattern - useEffect data fetching
'use client';
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]);

  if (!user) return <div>Loading...</div>;
  return <div>{user.name}</div>;
}

// ✅ React 19 pattern - use() hook with Suspense
'use client';
import { use } from 'react';

function UserProfile({ userPromise }) {
  const user = use(userPromise);
  return <div>{user.name}</div>;
}

// Parent with Suspense boundary
function Page({ userId }) {
  const userPromise = fetchUser(userId);

  return (
    <Suspense fallback={<div>Loading...</div>}>
      <UserProfile userPromise={userPromise} />
    </Suspense>
  );
}

// ✅ Even better - Server Component (no 'use client')
async function UserProfile({ userId }) {
  const user = await fetchUser(userId);
  return <div>{user.name}</div>;
}
```

**Reference**: See React patterns in [raw/instructions/javascript.instructions.md](../../../raw/instructions/javascript.instructions.md).

---

### Heuristic 40: Module Size Limit

**Rule**:
- **Files** must be ≤200 lines (excluding tests)
- **Functions** must be ≤50 lines
- **STRONG SUGGESTION**: Split files >150 lines
- **BLOCKER**: New files >250 lines

**Tool check**: File length linting (ESLint `max-lines`)

**Rationale**: Large modules violate Single Responsibility Principle and are hard to understand.

**Example**:
```javascript
// ❌ 300-line UserService.js (BLOCKER)
// Should be split into:
// - UserService.js (coordination)
// - UserValidator.js (validation logic)
// - UserTransformer.js (data transformation)
// - UserRepository.js (data access)

// ✅ Each file <200 lines
```

**Reference**: See architecture in [raw/instructions/javascript.instructions.md](../../../raw/instructions/javascript.instructions.md).

---

### Heuristic 41: Testing Pyramid Compliance

**Rule**:
Target test distribution:
- **70% unit tests** - pure functions, utilities
- **20% integration tests** - component + hooks
- **10% E2E tests** - critical user flows

**BLOCKER**: New feature without any tests
**STRONG SUGGESTION**: Add tests for changed code paths

**Check**: Does this change include appropriate test coverage?

**Rationale**: Balanced testing catches bugs early without excessive maintenance cost.

**Example**:
```javascript
// ❌ BLOCKER - new feature without tests
// File: features/orders/OrderService.ts
export function calculateOrderTotal(items, discountCode) {
  // ... 50 lines of logic
}

// ✅ Includes unit tests
// File: features/orders/OrderService.test.ts
describe('calculateOrderTotal', () => {
  it('calculates total for multiple items', () => {
    const items = [
      { price: 10, quantity: 2 },
      { price: 5, quantity: 3 }
    ];
    expect(calculateOrderTotal(items)).toBe(35);
  });

  it('applies discount code', () => {
    const items = [{ price: 100, quantity: 1 }];
    expect(calculateOrderTotal(items, 'SAVE20')).toBe(80);
  });

  it('handles invalid discount code', () => {
    const items = [{ price: 100, quantity: 1 }];
    expect(calculateOrderTotal(items, 'INVALID')).toBe(100);
  });
});
```

**Reference**: See testing strategy in [raw/instructions/javascript.instructions.md](../../../raw/instructions/javascript.instructions.md).

---

### Heuristic 42: Flaky Test Prevention

**Rule**:
Prevent flaky tests by:
- **No `waitFor()` without explicit timeout**
- **No relying on wall-clock time** (use `jest.useFakeTimers()`)
- **Use test data factories**, not hard-coded data
- **No network timing dependencies**

**BLOCKER**: Tests that rely on wall-clock time or network timing

**Rationale**: Flaky tests erode confidence and waste CI time.

**Example**:
```javascript
// ❌ BLOCKER - flaky timing
test('debounced search', async () => {
  renderSearchInput();
  userEvent.type(screen.getByRole('textbox'), 'query');
  await waitFor(() => {
    expect(mockSearch).toHaveBeenCalled();
  }); // No timeout, may fail randomly
});

// ✅ Explicit timeout and fake timers
test('debounced search', async () => {
  jest.useFakeTimers();
  renderSearchInput();
  userEvent.type(screen.getByRole('textbox'), 'query');

  jest.advanceTimersByTime(300); // Explicit debounce delay

  expect(mockSearch).toHaveBeenCalledWith('query');
  jest.useRealTimers();
});

// ❌ BLOCKER - hard-coded data
test('displays user', () => {
  render(<UserCard user={{ id: 1, name: 'John' }} />);
});

// ✅ Test data factory
const createUser = (overrides = {}) => ({
  id: Math.random(),
  name: 'Test User',
  email: 'test@example.com',
  ...overrides
});

test('displays user', () => {
  const user = createUser({ name: 'John' });
  render(<UserCard user={user} />);
});
```

**Reference**: See testing best practices in [raw/instructions/javascript.instructions.md](../../../raw/instructions/javascript.instructions.md).

---

### Heuristic 43: Security Pattern Verification

**Rule**:
All user input must be sanitized:
- **HTML**: Use DOMPurify before `dangerouslySetInnerHTML`
- **postMessage**: Validate `event.origin`
- **URL parameters**: Validate and sanitize
- **File uploads**: Validate type and size

**BLOCKER**:
- `dangerouslySetInnerHTML` without DOMPurify
- `postMessage` listener without origin check
- Unvalidated user input used in security-sensitive contexts

**Rationale**: XSS and injection attacks cause data breaches.

**Example**:
```javascript
// ❌ BLOCKER - XSS vulnerability
function UserBio({ bio }) {
  return <div dangerouslySetInnerHTML={{ __html: bio }} />;
}

// ✅ Sanitized HTML
import DOMPurify from 'dompurify';

function UserBio({ bio }) {
  const sanitized = DOMPurify.sanitize(bio);
  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
}

// ❌ BLOCKER - no origin validation
window.addEventListener('message', (event) => {
  const data = event.data;
  updateUserSettings(data);
});

// ✅ Origin validated
window.addEventListener('message', (event) => {
  if (event.origin !== 'https://trusted-domain.com') {
    return;
  }
  const data = event.data;
  updateUserSettings(data);
});
```

**Reference**: See security in [raw/instructions/javascript.instructions.md](../../../raw/instructions/javascript.instructions.md).

---

### Heuristic 44: Bundle Budget Check

**Rule**:
- **Initial bundle** <100KB gzipped
- **Route bundles** <200KB gzipped

**STRONG SUGGESTION**: Code-split routes >150KB
**BLOCKER**: Adding code that pushes any bundle >200KB

**Tool check**: webpack-bundle-analyzer or similar

**Rationale**: Large bundles harm Time to Interactive and user experience.

**Actions**:
- If route bundle >150KB: Suggest lazy loading
- If initial bundle >100KB: Suggest vendor splitting
- If any bundle >200KB: Block merge until split

**Example**:
```javascript
// ❌ All routes in main bundle (large bundle)
import { OrderList } from './features/orders/OrderList';
import { UserProfile } from './features/users/UserProfile';
import { AdminDashboard } from './features/admin/AdminDashboard';

const routes = [
  { path: '/orders', component: OrderList },
  { path: '/profile', component: UserProfile },
  { path: '/admin', component: AdminDashboard }
];

// ✅ Code-split routes (smaller initial bundle)
const OrderList = lazy(() => import('./features/orders/OrderList'));
const UserProfile = lazy(() => import('./features/users/UserProfile'));
const AdminDashboard = lazy(() => import('./features/admin/AdminDashboard'));

const routes = [
  { path: '/orders', component: OrderList },
  { path: '/profile', component: UserProfile },
  { path: '/admin', component: AdminDashboard }
];
```

**Reference**: See performance budgets in [raw/instructions/javascript.instructions.md](../../../raw/instructions/javascript.instructions.md).

---

### Heuristic 45: Anti-Pattern Detection

**Rule**:
Check against documented anti-patterns:

1. **Storing derived state** - compute from source of truth
2. **Premature abstraction** - wait for 3 use cases before abstracting
3. **God components** - components >300 lines
4. **Prop drilling >3 levels** - use context or composition
5. **Inline object creation in deps arrays** - causes infinite loops
6. **Missing error boundaries** - all routes need error boundaries
7. **Sync storage in renders** - use useEffect for localStorage writes
8. **Unhandled promise rejections** - all promises need error handling

**BLOCKER**: Anti-patterns 1, 5, 6, 8 (cause bugs)
**STRONG SUGGESTION**: Anti-patterns 2, 3, 4, 7 (harm maintainability)

**Example**:
```javascript
// ❌ BLOCKER - Anti-pattern #5 (infinite loop)
function UserList() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetchUsers({ filter: { active: true } }); // New object every render!
  }, [{ active: true }]); // Infinite loop
}

// ✅ Stable dependency
function UserList() {
  const [users, setUsers] = useState([]);
  const filter = useMemo(() => ({ active: true }), []);

  useEffect(() => {
    fetchUsers(filter);
  }, [filter]);
}

// ❌ BLOCKER - Anti-pattern #8 (unhandled rejection)
function saveData() {
  fetch('/api/save').then(r => r.json()); // No error handling
}

// ✅ Error handling
async function saveData() {
  try {
    const response = await fetch('/api/save');
    return await response.json();
  } catch (error) {
    logger.error({ error }, 'Failed to save data');
    throw new TechnicalError('Save failed', { cause: error });
  }
}
```

**Reference**: See anti-patterns in [raw/instructions/javascript.instructions.md](../../../raw/instructions/javascript.instructions.md).

---

## 8. Cross-Cutting Heuristics (All Web Code)

### Heuristic 46: WCAG 2.2 AA Compliance Gate

**Rule**:
**BLOCKER** severity for:
- Color contrast <4.5:1 for normal text, <3:1 for large text
- Missing keyboard navigation (no `tabindex` or focus management)
- Missing focus indicators (no `:focus` or `:focus-visible` styles)
- Missing alt text for images
- Automatic motion without user control

**Tool check**: Automated accessibility testing (pa11y, axe-core)

**Rationale**: Accessibility is a legal and ethical requirement.

**Example**:
```jsx
// ❌ BLOCKER - missing alt text
<img src="/user-avatar.jpg" />

// ✅ Descriptive alt text
<img src="/user-avatar.jpg" alt="User profile picture for John Doe" />

// ❌ BLOCKER - poor contrast (gray on white)
.c-button {
  background: #f0f0f0;
  color: #999999; /* Contrast ratio 2.4:1 - fails WCAG */
}

// ✅ Sufficient contrast
.c-button {
  background: #f0f0f0;
  color: #333333; /* Contrast ratio 8.3:1 - passes AAA */
}
```

**Reference**: See accessibility standards in [raw/instructions/css.instructions.md](../../../raw/instructions/css.instructions.md) and [raw/instructions/javascript.instructions.md](../../../raw/instructions/javascript.instructions.md).

---

### Heuristic 47: Version-Specific Feature Check

**Rule**:
Verify browser/runtime support for modern features:

**CSS features to check**:
- Cascade layers (`@layer`) - Chrome 99+, Safari 15.4+
- Container queries (`@container`) - Chrome 105+, Safari 16+
- `@property` - Chrome 85+, Safari 15.4+

**JavaScript features to check**:
- React Server Components - React 19+
- `use()` hook - React 19+
- Top-level await - ES2022

**Check**: Does the project's browserslist/target environment support this feature?

**STRONG SUGGESTION**: Add progressive enhancement or polyfills for features not universally supported

**Rationale**: Shipping unsupported features breaks the app for some users.

**Example**:
```css
/* Check browserslist before using */
@layer components {
  /* Only works in modern browsers */
}

/* Add fallback for older browsers */
.c-button {
  background: #3b82f6; /* Fallback */
  background: var(--color-primary-500); /* Modern */
}
```

**Reference**: See compatibility in [raw/instructions/css.instructions.md](../../../raw/instructions/css.instructions.md) and [raw/instructions/javascript.instructions.md](../../../raw/instructions/javascript.instructions.md).

---

### Heuristic 48: Risk Level Calibration

**Rule**:
Assign severity based on impact:

**CRITICAL** (Block merge immediately):
- Security vulnerabilities (XSS, injection, exposed secrets)
- Data loss or corruption
- Accessibility violations (WCAG failures)
- Breaking changes without migration path

**HIGH** (Must fix before merge):
- Performance budget violations
- Architecture violations (cross-feature imports, circular deps)
- Missing error handling
- Unhandled edge cases that cause bugs

**MEDIUM** (Strong suggestion, can merge with plan to fix):
- Specificity violations
- Missing tests for new features
- Readability issues (complex nesting, unclear names)
- Module size violations

**LOW** (Nice-to-have, optional):
- Style inconsistencies (naming, formatting)
- Minor optimizations
- Documentation improvements
- Refactoring suggestions

**Rationale**: Severity guides prioritization and prevents blocking on nitpicks.

**Example**:
- 🚫 **CRITICAL**: `dangerouslySetInnerHTML` with unsanitized user input
- ⛔ **HIGH**: Route bundle 230KB (exceeds 200KB budget)
- ⚠️ **MEDIUM**: Component file 215 lines (exceeds 200 line guideline)
- ℹ️ **LOW**: Variable named `data` could be more descriptive

**Reference**: See risk levels in [.github/css-code-review.md](../../../.github/css-code-review.md).

---

## Quick Reference: Heuristics by Scenario

### Reviewing a New Component

**Apply heuristics**: 1, 4, 6, 7, 13, 16, 17, 24-32 (CSS), 33-45 (JS), 46, 48

**Focus on**:
- Correct behavior (6, 7)
- Accessibility (31, 46)
- Component API (28)
- Test coverage (13, 41)
- Bundle impact (30, 44)

---

### Reviewing a Bug Fix

**Apply heuristics**: 1, 2, 6, 9, 13, 14, 21, 48

**Focus on**:
- Does it actually fix the bug? (1, 2)
- Edge cases covered? (6)
- Error handling improved? (9, 33-34)
- Tests added for regression? (13, 14)
- Unintended side effects? (21)

---

### Reviewing a Refactor

**Apply heuristics**: 3, 11, 18, 21, 23, 40

**Focus on**:
- Minimal disruption (3)
- Actually improves readability? (11)
- Preserves behavior (21)
- Incremental approach (23)
- Doesn't violate size limits (40)

---

### Reviewing a Performance Optimization

**Apply heuristics**: 4, 12, 14, 30, 32, 44

**Focus on**:
- Actual performance impact (12)
- Tests prove improvement (14)
- Doesn't harm correctness (4)
- Bundle budget compliance (30, 44)
- GPU-accelerated animations (32)

---

### Reviewing Security-Sensitive Code

**Apply heuristics**: 4, 10, 33-35, 43, 48

**Focus on**:
- Security as top priority (4)
- Input validation (10, 43)
- Error handling doesn't leak info (33-35)
- CRITICAL severity for vulnerabilities (48)

---

## Tool Integration Matrix

| Heuristic | Automated Check | Tool | When to Run |
|-----------|----------------|------|-------------|
| 24 - CSS Specificity | ✅ | `python scripts/css-specificity-checker.py` | Pre-commit |
| 25 - Cascade Layers | ⚠️ Partial | Stylelint plugin | Pre-commit |
| 26 - Design Tokens | ⚠️ Partial | Stylelint custom rule | Pre-commit |
| 27 - BEM Naming | ✅ | Stylelint `selector-class-pattern` | Pre-commit |
| 30 - CSS Bundle Size | ✅ | Build tooling | CI |
| 31 - Accessibility | ✅ | pa11y, axe-core | CI |
| 32 - GPU Animations | ⚠️ Partial | Stylelint custom rule | Pre-commit |
| 33 - Error Classification | ⚠️ Partial | ESLint custom rule | Pre-commit |
| 35 - Structured Logging | ✅ | ESLint `no-console` | Pre-commit |
| 36 - Module Boundaries | ✅ | `madge --circular` | CI |
| 40 - Module Size | ✅ | ESLint `max-lines` | Pre-commit |
| 41 - Test Coverage | ✅ | Jest coverage | CI |
| 43 - Security Patterns | ✅ | ESLint security plugin | Pre-commit |
| 44 - JS Bundle Size | ✅ | webpack-bundle-analyzer | CI |
| 46 - WCAG Compliance | ✅ | pa11y, axe-core | CI |

**Legend**:
- ✅ Fully automated
- ⚠️ Partially automated (requires manual review)
- ❌ Manual review only

---

## Summary

This document defines 48 reasoning heuristics for code review:

- **General heuristics (1-23)**: Apply to all code
- **CSS-specific (24-32)**: Specificity, layers, tokens, BEM, variants, container queries, performance, accessibility, animations
- **JavaScript-specific (33-45)**: Errors, logging, architecture, DI, state, React, testing, security, bundles, anti-patterns
- **Cross-cutting (46-48)**: Accessibility, version compatibility, severity calibration

**Key Principles**:
1. Correctness > Security > Performance > Maintainability > Style
2. Be specific with location, reason, and suggestion
3. Separate blockers from suggestions
4. Preserve author intent where reasonable
5. Automate what can be automated

**Next Steps**:
- Integrate automated checks (see Tool Integration Matrix)
- Reference this document in code review agent prompts
- Update heuristics as standards evolve
