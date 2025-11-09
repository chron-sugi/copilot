# JavaScript Debugging Reference

> **Version:** 1.0 (2025-01-09)
> **Purpose:** Comprehensive examples and patterns for JavaScript error handling, structured logging, and production debugging
> **Related:** [JavaScript Debugger Chat Mode](../chatmodes/javascript/js-debugger.chatmode.md)

---

## Table of Contents

1. [Error Categorization](#1-error-categorization)
2. [Structured Logging](#2-structured-logging)
3. [Unhandled Error Handlers](#3-unhandled-error-handlers)
4. [Correlation IDs](#4-correlation-ids)
5. [Error Boundary Patterns](#5-error-boundary-patterns)
6. [Error Chaining with .cause](#6-error-chaining-with-cause)
7. [Production Logging](#7-production-logging)

---

## 1. Error Categorization

### Problem
Generic Error class doesn't indicate error handling strategy (retry? show user? alert on-call?)

### Solution
Categorize errors into Domain/Technical/Fatal classes with explicit retry behavior.

### ❌ Before - Generic Error

```ts
export async function updateCart(item: CartItem) {
  const res = await fetch('/api/cart', {
    method: 'POST',
    body: JSON.stringify(item)
  });

  if (!res.ok) {
    throw new Error('Failed to update cart');  // Generic!
  }
}
```

**Issues:**
- Can't determine if error is user-facing or technical
- No retry strategy
- No context preservation
- Hard to debug in production

### ✅ After - Categorized Errors

```ts
// Base error classes
export class DomainError extends Error {
  constructor(message: string, cause?: unknown) {
    super(message);
    this.name = 'DomainError';
    this.cause = cause;
  }
}

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

export class FatalError extends Error {
  constructor(message: string, cause?: unknown) {
    super(message);
    this.name = 'FatalError';
    this.cause = cause;
  }
}

export class HttpError extends TechnicalError {
  constructor(message: string, public readonly status: number, cause?: unknown) {
    super(message, status >= 500, cause);  // 5xx are retryable
    this.name = 'HttpError';
  }
}

// Usage
export async function updateCart(item: CartItem) {
  try {
    const res = await fetch('/api/cart', {
      method: 'POST',
      body: JSON.stringify(item)
    });

    if (!res.ok) {
      throw new HttpError(
        'Failed to update cart',
        res.status,
        await res.text()
      );
    }

    return res.json();
  } catch (error) {
    throw new TechnicalError(
      'Network error updating cart',
      true,  // Retryable
      error
    );
  }
}
```

**Benefits:**
- ✅ Clear error handling strategy (retry 5xx, don't retry 4xx)
- ✅ User-facing vs technical distinction
- ✅ Context preserved via `.cause`
- ✅ Type-safe error handling

### Error Handling Strategy

```ts
try {
  await updateCart(item);
} catch (error) {
  if (error instanceof DomainError) {
    // Show to user, don't retry
    showErrorToast(error.message);
  } else if (error instanceof TechnicalError) {
    // Log and retry if retryable
    logger.error({ error, userId, traceId });
    if (error.retryable) {
      await retryWithBackoff(() => updateCart(item));
    }
  } else if (error instanceof FatalError) {
    // Circuit breaker, alert on-call
    circuitBreaker.open();
    alertOnCall(error);
  }
}
```

---

## 2. Structured Logging

### Problem
String concatenation makes logs hard to query, missing context, poor debugging.

### ❌ Before - String Soup

```ts
console.log('User ' + userId + ' failed payment for order ' + orderId);
console.error('Payment error: ' + error.message);
```

**Issues:**
- Can't query by userId or orderId
- No trace ID for distributed tracing
- Missing context (amount, payment method, etc.)
- Hard to parse programmatically

### ✅ After - Structured Logging

```ts
import { log } from '@/shared/logger';

const logger = log('checkout:payment');

logger.debug({
  userId,
  orderId,
  amount,
  timestamp: Date.now()
}, 'Payment initiated');

logger.error({
  userId,
  orderId,
  error: error.message,
  errorStack: error.stack,
  traceId: getCurrentTraceId(),
  timestamp: Date.now()
}, 'Payment failed');
```

**Benefits:**
- ✅ Queryable by any field
- ✅ Trace ID for distributed systems
- ✅ Rich context for debugging
- ✅ Parseable by logging services (Datadog, Sentry, etc.)

### Logger Implementation Example

```ts
// shared/logger.ts
export type LogLevel = 'debug' | 'info' | 'warn' | 'error';

export interface LogContext {
  [key: string]: unknown;
  userId?: string;
  traceId?: string;
  sessionId?: string;
}

export function log(topic: string) {
  return {
    debug(context: LogContext, message: string) {
      this._log('debug', topic, context, message);
    },
    info(context: LogContext, message: string) {
      this._log('info', topic, context, message);
    },
    warn(context: LogContext, message: string) {
      this._log('warn', topic, context, message);
    },
    error(context: LogContext, message: string) {
      this._log('error', topic, context, message);
    },
    _log(level: LogLevel, topic: string, context: LogContext, message: string) {
      const entry = {
        level,
        topic,
        message,
        ...context,
        timestamp: Date.now(),
      };

      // Development: pretty print
      if (process.env.NODE_ENV === 'development') {
        console.log(`[${level.toUpperCase()}] [${topic}] ${message}`, context);
      } else {
        // Production: send to logging service
        sendToLoggingService(entry);
      }
    },
  };
}
```

---

## 3. Unhandled Error Handlers

### Problem
Unhandled promise rejections and global errors cause silent failures.

### ✅ Solution - Global Error Handlers

```tsx
// app/layout.tsx or app/providers.tsx
useEffect(() => {
  // Catch unhandled promise rejections
  const handleRejection = (event: PromiseRejectionEvent) => {
    logger.error({
      reason: event.reason,
      promise: event.promise,
      traceId: getCurrentTraceId(),
    }, 'Unhandled promise rejection');

    // Prevent default browser behavior
    event.preventDefault();

    // Optional: Show error UI to user
    showErrorToast('Something went wrong');
  };

  // Catch global errors
  const handleError = (event: ErrorEvent) => {
    logger.error({
      message: event.message,
      filename: event.filename,
      lineno: event.lineno,
      colno: event.colno,
      error: event.error,
      traceId: getCurrentTraceId(),
    }, 'Global error');
  };

  window.addEventListener('unhandledrejection', handleRejection);
  window.addEventListener('error', handleError);

  return () => {
    window.removeEventListener('unhandledrejection', handleRejection);
    window.removeEventListener('error', handleError);
  };
}, []);
```

**Benefits:**
- ✅ Catches all unhandled promise rejections
- ✅ Catches global errors
- ✅ Logs to monitoring service
- ✅ Graceful UX degradation

### Integration with Error Monitoring

```ts
// With Sentry
const handleRejection = (event: PromiseRejectionEvent) => {
  Sentry.captureException(event.reason, {
    tags: { errorType: 'unhandledRejection' },
    extra: { traceId: getCurrentTraceId() },
  });
  event.preventDefault();
};
```

---

## 4. Correlation IDs

### Problem
Can't trace requests across services in distributed systems.

### ❌ Before - No Correlation

```ts
export async function apiRequest(url: string) {
  return fetch(url);
}
```

**Issues:**
- Can't correlate frontend → backend → database logs
- Hard to debug distributed system failures
- No user session tracking

### ✅ After - With Correlation IDs

```ts
// Trace ID management
let currentTraceId: string | null = null;

export function getOrCreateTraceId(): string {
  if (!currentTraceId) {
    currentTraceId = crypto.randomUUID();
  }
  return currentTraceId;
}

export function getCurrentTraceId(): string | null {
  return currentTraceId;
}

export function setTraceId(traceId: string): void {
  currentTraceId = traceId;
}

// HTTP client with correlation IDs
export async function apiRequest(url: string, options: RequestInit = {}) {
  const traceId = getOrCreateTraceId();
  const sessionId = getSessionId();

  return fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'X-Trace-Id': traceId,
      'X-Session-Id': sessionId,
    },
  });
}

// Include in all logs
logger.error({
  traceId,
  sessionId,
  userId,
  action: 'checkout',
  error: error.message
}, 'Payment failed');
```

**Benefits:**
- ✅ Trace requests across all services
- ✅ Correlate frontend and backend logs
- ✅ Debug distributed system issues
- ✅ Track user sessions

### Backend Correlation

```ts
// Express middleware
app.use((req, res, next) => {
  const traceId = req.headers['x-trace-id'] || crypto.randomUUID();
  const sessionId = req.headers['x-session-id'];

  req.traceId = traceId;
  req.sessionId = sessionId;

  res.setHeader('X-Trace-Id', traceId);
  next();
});
```

---

## 5. Error Boundary Patterns

### Problem
Expecting Error Boundary to catch all errors (it doesn't catch event handlers).

### ❌ Before - Misunderstanding Error Boundaries

```tsx
function PaymentForm() {
  const handleSubmit = () => {
    throw new Error('Payment failed');  // Not caught by Error Boundary!
  };

  return (
    <form onSubmit={handleSubmit}>
      <button type="submit">Pay</button>
    </form>
  );
}
```

**Issues:**
- Error Boundaries don't catch event handler errors
- Uncaught error crashes app
- Poor UX

### ✅ After - Proper Event Handler Error Handling

```tsx
function PaymentForm() {
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    try {
      await processPayment();
      showSuccess('Payment successful');
    } catch (error) {
      logger.error({
        error,
        userId,
        traceId: getCurrentTraceId()
      }, 'Payment failed');

      showErrorToast('Payment failed. Please try again.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <button type="submit">Pay</button>
    </form>
  );
}
```

### Error Boundary Implementation

```tsx
import { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    logger.error({
      error: error.message,
      stack: error.stack,
      componentStack: errorInfo.componentStack,
      traceId: getCurrentTraceId(),
    }, 'Error boundary caught error');
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }

    return this.props.children;
  }
}
```

### What Error Boundaries Catch

**Error Boundaries CATCH:**
- ✅ Render phase errors
- ✅ Lifecycle methods
- ✅ Constructors of child components

**Error Boundaries DON'T CATCH:**
- ❌ Event handlers (use try/catch)
- ❌ Async code (use try/catch or .catch())
- ❌ Server-side rendering
- ❌ Errors in the Error Boundary itself

---

## 6. Error Chaining with .cause

### Problem
Error context lost when wrapping errors, making debugging difficult.

### ❌ Before - Context Lost

```ts
export async function getUserProfile(id: string) {
  try {
    const data = await fetchUser(id);
    return parseUser(data);
  } catch (error) {
    throw new Error('Failed to get user profile');
    // Original error lost!
  }
}
```

**Issues:**
- Original error stack lost
- Can't see root cause
- Hard to debug production issues

### ✅ After - Preserve Error Chain

```ts
export async function getUserProfile(id: string) {
  try {
    const data = await fetchUser(id);
    return parseUser(data);
  } catch (error) {
    throw new TechnicalError(
      'Failed to get user profile',
      false,  // Not retryable (parse error)
      error   // Preserve original error as cause
    );
  }
}
```

### Logging Error Chains

```ts
logger.error({
  error: error.message,
  cause: error.cause,
  stack: error.stack,
  causeStack: error.cause?.stack,
  traceId
}, 'User profile fetch failed');
```

### Error.cause Browser Support

```ts
// Polyfill for older browsers
if (!('cause' in Error.prototype)) {
  Object.defineProperty(Error.prototype, 'cause', {
    get() {
      return this._cause;
    },
    set(value) {
      this._cause = value;
    },
  });
}
```

---

## 7. Production Logging

### Problem
console.log doesn't persist in production, can't query, no correlation.

### ❌ Before - Console.log Everywhere

```ts
console.log('User logged in:', userId);
console.error('Payment failed:', error);
```

**Issues:**
- Logs don't persist
- Can't query by user/session
- No correlation IDs
- Missing context

### ✅ After - Logging Service

```ts
import { log } from '@/shared/logger';

const logger = log('auth');

logger.debug({
  userId,
  timestamp: Date.now(),
  traceId: getCurrentTraceId()
}, 'User logged in');

logger.error({
  userId,
  error: error.message,
  errorStack: error.stack,
  traceId: getCurrentTraceId(),
  featureFlags: getActiveFlags()
}, 'Payment failed');
```

### Production Logger Configuration

```ts
// shared/logger.ts
function sendToLoggingService(entry: LogEntry) {
  if (process.env.NODE_ENV === 'production') {
    // Sentry
    if (entry.level === 'error') {
      Sentry.captureException(entry.error || new Error(entry.message), {
        tags: { topic: entry.topic },
        extra: entry,
      });
    }

    // Datadog
    if (window.DD_LOGS) {
      window.DD_LOGS.logger.log(entry.message, entry, entry.level);
    }

    // LogRocket
    if (window.LogRocket) {
      window.LogRocket.log(entry.level, entry.message, entry);
    }
  }
}
```

### Feature Flag Tracking

```ts
// Track active feature flags in errors
export function getActiveFlags(): string[] {
  return Object.entries(featureFlags)
    .filter(([_, enabled]) => enabled)
    .map(([flag]) => flag);
}

logger.error({
  error: error.message,
  featureFlags: getActiveFlags(),
  traceId,
}, 'Error occurred');
```

---

## Best Practices Summary

### Error Handling
1. **Categorize errors** (Domain/Technical/Fatal)
2. **Include `.cause`** for error chaining
3. **Make user-facing errors actionable**
4. **Log technical errors** with full context
5. **Handle unhandled rejections** globally

### Logging
1. **Use structured logging** (objects, not strings)
2. **Include correlation/trace IDs**
3. **Use topic-based loggers**
4. **Send to logging service** in production
5. **Include relevant context** (userId, action, timestamp)

### Production Debugging
1. **Enable source maps** in dev/staging
2. **Use correlation IDs** for distributed tracing
3. **Set displayName** on complex React components
4. **Track active feature flags** in errors
5. **Use session replay tools**

### Error Boundaries
1. **Place at strategic points** (route level, feature level)
2. **Understand limitations** (doesn't catch event handlers)
3. **Use try/catch in event handlers**
4. **Provide user-friendly fallback UI**
5. **Log errors before showing fallback**

---

## Related Resources

**Chat Modes:**
- [JavaScript Debugger](../chatmodes/javascript/js-debugger.chatmode.md) - Diagnose and fix errors
- [JavaScript Test Engineer](../chatmodes/javascript/js-test-engineer.chatmode.md) - Write error tests
- [JavaScript Security Specialist](../chatmodes/javascript/js-security-specialist.chatmode.md) - Security implications

**Prompt Files:**
- [Error Classes Setup](../prompts/javascript/js-debug-error-classes.prompt.md)
- [Logging Setup](../prompts/javascript/js-debug-logging-setup.prompt.md)
- [Error Handler Setup](../prompts/javascript/js-debug-error-handler-setup.prompt.md)
- [Correlation ID Setup](../prompts/javascript/js-debug-correlation-id-setup.prompt.md)

**Documentation:**
- [JavaScript Web App Playbook](../../prompt_engineering/prompts/javascript-web-app-playbook.md)
- [JavaScript Core Standards](../instructions/javascript.instructions.md)

---

**Last Updated:** 2025-01-09
**Maintained by:** JavaScript Architecture Team
