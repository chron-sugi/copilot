---
applyTo: "**/*.js,**/*.jsx,**/*.ts,**/*.tsx"
description: "Core JavaScript/TypeScript standards - error handling, logging, testing, React patterns"
---

# JavaScript Shared Standards

> **Version:** 1.0 (2025-01-09)
> **Purpose:** Core principles and standards applied automatically to all JavaScript/TypeScript work
> **Reference:** [JavaScript Web App Playbook](../../prompt_engineering/prompts/javascript-web-app-playbook.md)

---

## Error Handling Standards

### Error Categorization (Required)

**Categorize all errors** into one of these classes:

```typescript
// DomainError - User-facing, show to user, don't retry
export class DomainError extends Error {
  constructor(message: string, cause?: unknown) {
    super(message);
    this.name = 'DomainError';
    this.cause = cause;
  }
}

// TechnicalError - Log & retry with backoff
export class TechnicalError extends Error {
  constructor(
    message: string,
    public readonly retryable: boolean,
    cause?: unknown
  ) {
    super(message);
    this.name = 'TechnicalError';
    this.cause = cause;
  }
}

// FatalError - Circuit breaker, alert on-call
export class FatalError extends Error {
  constructor(message: string, cause?: unknown) {
    super(message);
    this.name = 'FatalError';
    this.cause = cause;
  }
}

// HttpError - Status-based retry strategy
export class HttpError extends TechnicalError {
  constructor(message: string, public readonly status: number, cause?: unknown) {
    super(message, status >= 500, cause);  // 5xx are retryable
    this.name = 'HttpError';
  }
}
```

**When to use each:**
- **DomainError**: Validation errors, business rule violations, user input errors
- **TechnicalError**: Network errors, database errors, API failures
- **FatalError**: Configuration errors, missing environment variables, critical system failures
- **HttpError**: HTTP request failures with status codes

### Error.cause Chaining (Required)

**Always preserve error context** with `.cause`:

```typescript
// ❌ Don't lose context
try {
  await fetchUser(id);
} catch (error) {
  throw new Error('Failed to get user');  // Context lost!
}

// ✅ Preserve error chain
try {
  await fetchUser(id);
} catch (error) {
  throw new TechnicalError(
    'Failed to get user',
    false,  // Not retryable
    error   // Preserve original error
  );
}
```

### Async Error Handling (Required)

**Never leave promises unhandled:**

```typescript
// ❌ Unhandled promise
async function fetchData() {
  return fetch('/api/data');  // No error handling!
}

// ✅ Handled with try/catch
async function fetchData() {
  try {
    const response = await fetch('/api/data');
    if (!response.ok) {
      throw new HttpError('Fetch failed', response.status);
    }
    return response.json();
  } catch (error) {
    throw new TechnicalError('Network error', true, error);
  }
}

// ✅ Or with .catch()
function fetchData() {
  return fetch('/api/data')
    .then(res => {
      if (!res.ok) throw new HttpError('Fetch failed', res.status);
      return res.json();
    })
    .catch(error => {
      throw new TechnicalError('Network error', true, error);
    });
}
```

---

## Structured Logging Standards

### Objects, Not Strings (Required)

**Use structured logging with queryable fields:**

```typescript
// ❌ String concatenation
console.log('User ' + userId + ' logged in at ' + timestamp);

// ✅ Structured logging
logger.info({
  userId,
  timestamp: Date.now(),
  traceId: getCurrentTraceId(),
  sessionId: getSessionId()
}, 'User logged in');
```

### Correlation IDs (Required)

**Include trace/session/user IDs in all logs:**

```typescript
// Required fields in log context
interface LogContext {
  traceId?: string;      // Per-request trace ID
  sessionId?: string;    // Per-session ID
  userId?: string;       // Authenticated user ID
  [key: string]: unknown;
}

// Usage
logger.error({
  traceId: getCurrentTraceId(),
  sessionId: getSessionId(),
  userId: getCurrentUserId(),
  error: error.message,
  errorStack: error.stack
}, 'Operation failed');
```

### Topic-Based Loggers (Required)

**Organize logs by feature area:**

```typescript
// Create topic-specific loggers
const authLogger = log('auth:login');
const paymentLogger = log('checkout:payment');
const apiLogger = log('api:http');

// Use throughout the feature
authLogger.info({ userId, traceId }, 'Login successful');
paymentLogger.error({ userId, orderId, error }, 'Payment failed');
```

### No console.log in Production (Required)

**Use logging service in production:**

```typescript
// ❌ Don't use console.log directly
console.log('Debug info', data);

// ✅ Use logger that integrates with services
logger.debug({ data, traceId }, 'Debug info');

// Logger sends to Sentry/Datadog/LogRocket in production
// Pretty prints to console in development
```

---

## React Standards

### Modern Patterns (React 19+)

**Use modern React patterns:**

```typescript
// ✅ Server Components (default)
export default function ProductList() {
  const products = await fetchProducts();  // No useEffect!
  return <div>{products.map(p => <Product key={p.id} {...p} />)}</div>;
}

// ✅ Client Components (only when needed)
'use client';

export function InteractiveButton() {
  const [count, setCount] = useState(0);  // Needs client
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}

// ✅ Suspense for async data
<Suspense fallback={<Loading />}>
  <AsyncComponent />
</Suspense>
```

### State Management Decision Tree

```
Is it server data (API, database)?
├─ YES → TanStack Query / SWR / RTK Query
└─ NO → Is it global client state?
    ├─ YES → Does it need persistence?
    │   ├─ YES → Zustand with persist middleware
    │   └─ NO → Zustand or Context
    └─ NO → Is it URL state (filters, pagination)?
        ├─ YES → URL search params
        └─ NO → Local useState/useReducer
```

### Error Boundaries (Required)

**Wrap components with Error Boundaries:**

```tsx
<ErrorBoundary fallback={<ErrorFallback />}>
  <App />
</ErrorBoundary>
```

**Remember limitations:**
- ✅ Catches: Render errors, lifecycle methods, constructors
- ❌ Doesn't catch: Event handlers, async code, SSR

**Use try/catch in event handlers:**

```tsx
// ❌ Error Boundary won't catch this
const handleClick = () => {
  throw new Error('Failed');  // Not caught!
};

// ✅ Use try/catch
const handleClick = async () => {
  try {
    await processAction();
  } catch (error) {
    logger.error({ error, traceId }, 'Action failed');
    showError('Action failed');
  }
};
```

---

## Testing Standards

### Testing Pyramid

```
       E2E (few)
      /         \
  Component   Contract
 /                    \
Unit (most)         Unit (most)
```

**Distribution:**
- **70%** Unit tests (pure functions, utilities, hooks)
- **20%** Component tests (user interactions, rendering)
- **10%** E2E tests (critical user flows)

### Test Structure (Required)

```typescript
describe('ComponentName', () => {
  it('renders with default props', () => {
    // Arrange
    const props = { name: 'Test' };

    // Act
    render(<Component {...props} />);

    // Assert
    expect(screen.getByText('Test')).toBeInTheDocument();
  });

  it('handles user interaction', async () => {
    // Arrange
    const handleClick = vi.fn();
    render(<Button onClick={handleClick} />);

    // Act
    await userEvent.click(screen.getByRole('button'));

    // Assert
    expect(handleClick).toHaveBeenCalledOnce();
  });
});
```

### Prevent Flaky Tests

**Avoid:**
- ❌ Hardcoded timeouts: `setTimeout()`
- ❌ Random data: `Math.random()`
- ❌ Current date/time: `new Date()`
- ❌ Order-dependent tests

**Use:**
- ✅ `waitFor()`, `findBy*()` for async
- ✅ Deterministic test data
- ✅ Mock timers: `vi.useFakeTimers()`
- ✅ Independent tests

---

## TypeScript Standards

### Strict Mode (Required)

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  }
}
```

### No any (Required)

```typescript
// ❌ Don't use any
function process(data: any) {  // Defeats TypeScript!
  return data.value;
}

// ✅ Use proper types
function process(data: { value: string }): string {
  return data.value;
}

// ✅ Or unknown if truly unknown
function process(data: unknown): string {
  if (typeof data === 'object' && data !== null && 'value' in data) {
    return String(data.value);
  }
  throw new DomainError('Invalid data');
}
```

### Async Safety (Required with ESLint)

```javascript
// .eslintrc.cjs
module.exports = {
  rules: {
    '@typescript-eslint/no-floating-promises': 'error',
    '@typescript-eslint/no-misused-promises': 'error',
    '@typescript-eslint/await-thenable': 'error',
  }
};
```

---

## Performance Standards

### Code Splitting (Required)

```typescript
// ✅ Dynamic imports for routes
const Dashboard = lazy(() => import('./Dashboard'));
const Settings = lazy(() => import('./Settings'));

// ✅ Conditional loading
if (user.isAdmin) {
  const AdminPanel = await import('./AdminPanel');
  return <AdminPanel.default />;
}
```

### Memoization (Use Sparingly)

```typescript
// ❌ Don't memoize everything
const Component = memo(() => {  // Usually unnecessary!
  return <div>Simple component</div>;
});

// ✅ Only memoize expensive components
const ExpensiveList = memo(({ items }: { items: Item[] }) => {
  return items.map(item => <ExpensiveItem key={item.id} {...item} />);
});

// ✅ Memoize expensive calculations
const sortedItems = useMemo(
  () => items.sort((a, b) => complexSort(a, b)),
  [items]  // Only recalculate when items change
);
```

---

## Security Standards

### XSS Prevention (Required)

```typescript
// ❌ Dangerous innerHTML
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// ✅ Sanitize HTML
import DOMPurify from 'dompurify';

const clean = DOMPurify.sanitize(html, {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
  ALLOWED_ATTR: ['href']
});

<div dangerouslySetInnerHTML={{ __html: clean }} />
```

### postMessage Validation (Required)

```typescript
// ❌ No origin validation
window.addEventListener('message', (event) => {
  processData(event.data);  // Dangerous!
});

// ✅ Validate origin
window.addEventListener('message', (event) => {
  if (event.origin !== 'https://trusted-domain.com') {
    return;  // Reject untrusted origins
  }

  // Validate data structure
  if (typeof event.data !== 'object' || !('action' in event.data)) {
    return;
  }

  processData(event.data);
});
```

---

## Global Error Handlers (Required)

**Setup once at app initialization:**

```typescript
// app/layout.tsx or main.tsx
useEffect(() => {
  // Catch unhandled promise rejections
  window.addEventListener('unhandledrejection', (event) => {
    logger.error({
      reason: event.reason,
      traceId: getCurrentTraceId()
    }, 'Unhandled promise rejection');
    event.preventDefault();
  });

  // Catch global errors
  window.addEventListener('error', (event) => {
    logger.error({
      message: event.message,
      filename: event.filename,
      lineno: event.lineno,
      error: event.error,
      traceId: getCurrentTraceId()
    }, 'Global error');
  });
}, []);
```

---

## Anti-Patterns to Avoid

### 1. Prop Drilling Beyond 3 Levels

```typescript
// ❌ Prop drilling
<Level1 user={user}>
  <Level2 user={user}>
    <Level3 user={user}>
      <Level4 user={user} />  // Too deep!
    </Level3>
  </Level2>
</Level1>

// ✅ Use Context or state management
const UserContext = createContext<User | null>(null);

<UserContext.Provider value={user}>
  <Level1><Level2><Level3><Level4 /></Level3></Level2></Level1>
</UserContext.Provider>
```

### 2. Fetching Data in useEffect

```typescript
// ❌ Manual fetching in useEffect
useEffect(() => {
  fetch('/api/users').then(res => res.json()).then(setUsers);
}, []);

// ✅ Use TanStack Query
const { data: users } = useQuery({
  queryKey: ['users'],
  queryFn: fetchUsers
});
```

### 3. Duplicating Server State

```typescript
// ❌ Copying server data to local state
const [users, setUsers] = useState([]);

useEffect(() => {
  fetchUsers().then(setUsers);  // Duplicate state!
}, []);

// ✅ Let TanStack Query manage it
const { data: users } = useQuery({
  queryKey: ['users'],
  queryFn: fetchUsers
});
```

---

## Remember

When working with JavaScript/TypeScript:

1. **Categorize all errors** (Domain/Technical/Fatal)
2. **Use structured logging** with correlation IDs
3. **Include trace context** in all logs and errors
4. **Handle all promises** (no floating promises)
5. **Setup global error handlers** once at app init
6. **Use Error Boundaries** for React component errors
7. **Follow React 19+ patterns** (Server Components, Suspense)
8. **Test with pyramid approach** (70% unit, 20% component, 10% E2E)
9. **Enable TypeScript strict mode** with async safety rules
10. **Prevent security issues** (XSS, postMessage validation)

---

**Related Resources:**
- [JavaScript Web App Playbook](../../prompt_engineering/prompts/javascript-web-app-playbook.md)
- [JavaScript Debugging Reference](../docs/javascript-debugging-reference.md)
- [JavaScript Debugger Chat Mode](../chatmodes/javascript/js-debugger.chatmode.md)

**Prompt Files for Setup:**
- [Error Classes Setup](../prompts/javascript/js-debug-error-classes.prompt.md)
- [Logging Setup](../prompts/javascript/js-debug-logging-setup.prompt.md)
- [Error Handler Setup](../prompts/javascript/js-debug-error-handler-setup.prompt.md)
- [Correlation ID Setup](../prompts/javascript/js-debug-correlation-id-setup.prompt.md)

---

**Last Updated:** 2025-01-09
**Maintained by:** JavaScript Architecture Team
