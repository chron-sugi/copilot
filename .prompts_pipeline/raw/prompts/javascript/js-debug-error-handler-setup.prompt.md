---
description: "Setup global error handlers for unhandled rejections and errors"
mode: 'agent'
model: Auto
tools: ['codebase', 'edit']
---

# Setup Global Error Handlers

Configure global error handlers for: **${input:projectName}**

---

## Project Information

**Project Name**: ${input:projectName}

**Framework**: ${input:framework:React/Next.js/Vue/Vanilla}

**TypeScript**: ${input:typescript:Yes}

**Has Error Logging**: ${input:hasLogging:Yes (from js-debug-logging-setup)/No}

**Target File**: ${input:targetFile:src/app/error-handlers.ts}

---

## Requirements

Setup global error handlers to catch:

1. **Unhandled promise rejections** - `window.addEventListener('unhandledrejection')`
2. **Global errors** - `window.addEventListener('error')`
3. **React error boundaries** (if React) - Component-level error catching
4. **Logging integration** - Send to logging service
5. **User feedback** - Graceful error UI

---

## Implementation

### Core Error Handler Module

```typescript
// ${input:targetFile:src/app/error-handlers.ts}

${input:hasLogging === 'Yes' ? `import { log } from '@/shared/logger';` : ''}
${input:hasLogging === 'No' ? `// TODO: Setup structured logging first (use #js-debug-logging-setup)` : ''}
import { getCurrentTraceId } from '@/shared/tracing';

${input:hasLogging === 'Yes' ? `const logger = log('app:errors');` : ''}

/**
 * Setup global error handlers for unhandled rejections and errors
 * Call this once at app initialization
 */
export function setupGlobalErrorHandlers(): void {
  // Handle unhandled promise rejections
  window.addEventListener('unhandledrejection', handleUnhandledRejection);

  // Handle global errors
  window.addEventListener('error', handleGlobalError);

  ${input:framework.includes('React') ? `
  // Note: React Error Boundaries should be setup separately
  // See setupReactErrorBoundary() below
  ` : ''}
}

/**
 * Cleanup error handlers (useful for tests)
 */
export function cleanupGlobalErrorHandlers(): void {
  window.removeEventListener('unhandledrejection', handleUnhandledRejection);
  window.removeEventListener('error', handleGlobalError);
}

/**
 * Handle unhandled promise rejections
 */
function handleUnhandledRejection(event: PromiseRejectionEvent): void {
  const traceId = getCurrentTraceId();

  ${input:hasLogging === 'Yes' ? `
  logger.error({
    reason: event.reason,
    promise: event.promise,
    traceId,
    timestamp: Date.now(),
  }, 'Unhandled promise rejection');
  ` : `
  console.error('Unhandled promise rejection:', {
    reason: event.reason,
    traceId,
  });
  `}

  // Prevent default browser behavior (console error)
  event.preventDefault();

  // Show user-friendly error message
  showErrorToUser('Something went wrong. Please try again.');

  // Send to error monitoring service (Sentry, etc.)
  reportToErrorMonitoring(event.reason, 'unhandledRejection', { traceId });
}

/**
 * Handle global errors
 */
function handleGlobalError(event: ErrorEvent): void {
  const traceId = getCurrentTraceId();

  ${input:hasLogging === 'Yes' ? `
  logger.error({
    message: event.message,
    filename: event.filename,
    lineno: event.lineno,
    colno: event.colno,
    error: event.error,
    stack: event.error?.stack,
    traceId,
    timestamp: Date.now(),
  }, 'Global error');
  ` : `
  console.error('Global error:', {
    message: event.message,
    filename: event.filename,
    lineno: event.lineno,
    colno: event.colno,
    error: event.error,
    traceId,
  });
  `}

  // Show user-friendly error message
  showErrorToUser('An unexpected error occurred.');

  // Send to error monitoring service
  reportToErrorMonitoring(event.error || event.message, 'globalError', {
    traceId,
    filename: event.filename,
    lineno: event.lineno,
    colno: event.colno,
  });
}

/**
 * Show error message to user
 * Implement this based on your UI library (toast, modal, etc.)
 */
function showErrorToUser(message: string): void {
  // TODO: Implement based on your UI library
  // Examples:
  // - toast.error(message)
  // - showNotification({ type: 'error', message })
  // - alert(message) // Fallback

  console.error('[User Error]:', message);
}

/**
 * Report error to monitoring service
 */
function reportToErrorMonitoring(
  error: unknown,
  errorType: 'unhandledRejection' | 'globalError',
  context: Record<string, unknown>
): void {
  // Sentry integration
  if (typeof window !== 'undefined' && window.Sentry) {
    window.Sentry.captureException(
      error instanceof Error ? error : new Error(String(error)),
      {
        tags: { errorType },
        extra: context,
        level: 'error',
      }
    );
  }

  // Add other monitoring services here (Datadog, LogRocket, etc.)
}
```

---

## React Error Boundary (if using React)

```typescript
// ${input:targetFile.replace('error-handlers.ts', 'error-boundary.tsx')}

import { Component, ReactNode } from 'react';
${input:hasLogging === 'Yes' ? `import { log } from '@/shared/logger';` : ''}
import { getCurrentTraceId } from '@/shared/tracing';

${input:hasLogging === 'Yes' ? `const logger = log('app:error-boundary');` : ''}

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: React.ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error?: Error;
  errorInfo?: React.ErrorInfo;
}

/**
 * React Error Boundary
 * Catches errors in React component tree
 *
 * Usage:
 * <ErrorBoundary fallback={<ErrorFallback />}>
 *   <App />
 * </ErrorBoundary>
 */
export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo): void {
    const traceId = getCurrentTraceId();

    ${input:hasLogging === 'Yes' ? `
    logger.error({
      error: error.message,
      stack: error.stack,
      componentStack: errorInfo.componentStack,
      traceId,
      timestamp: Date.now(),
    }, 'Error boundary caught error');
    ` : `
    console.error('Error boundary caught error:', {
      error,
      errorInfo,
      traceId,
    });
    `}

    // Send to error monitoring
    if (typeof window !== 'undefined' && window.Sentry) {
      window.Sentry.captureException(error, {
        tags: { errorType: 'errorBoundary' },
        extra: { componentStack: errorInfo.componentStack, traceId },
        level: 'error',
      });
    }

    // Call custom error handler if provided
    this.props.onError?.(error, errorInfo);

    this.setState({ errorInfo });
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || <DefaultErrorFallback error={this.state.error} />;
    }

    return this.props.children;
  }
}

/**
 * Default error fallback UI
 */
function DefaultErrorFallback({ error }: { error?: Error }) {
  return (
    <div style={{ padding: '2rem', textAlign: 'center' }}>
      <h1>Something went wrong</h1>
      <p>We're sorry for the inconvenience. Please try refreshing the page.</p>
      {process.env.NODE_ENV === 'development' && error && (
        <details style={{ marginTop: '1rem', textAlign: 'left' }}>
          <summary>Error details</summary>
          <pre style={{ whiteSpace: 'pre-wrap', fontSize: '0.875rem' }}>
            {error.stack}
          </pre>
        </details>
      )}
      <button
        onClick={() => window.location.reload()}
        style={{ marginTop: '1rem', padding: '0.5rem 1rem' }}
      >
        Refresh Page
      </button>
    </div>
  );
}
```

---

## App Initialization

### React/Next.js Example

```typescript
// app/layout.tsx or app/providers.tsx

'use client';

import { useEffect } from 'react';
import { setupGlobalErrorHandlers, cleanupGlobalErrorHandlers } from './error-handlers';
import { ErrorBoundary } from './error-boundary';

export function Providers({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Setup global error handlers on mount
    setupGlobalErrorHandlers();

    // Cleanup on unmount
    return () => {
      cleanupGlobalErrorHandlers();
    };
  }, []);

  return (
    <ErrorBoundary fallback={<ErrorFallback />}>
      {children}
    </ErrorBoundary>
  );
}

function ErrorFallback() {
  return (
    <div className="error-container">
      <h1>Unexpected Error</h1>
      <p>We're sorry, something went wrong. Please refresh the page.</p>
      <button onClick={() => window.location.reload()}>
        Refresh
      </button>
    </div>
  );
}
```

### Vanilla JavaScript Example

```typescript
// main.ts

import { setupGlobalErrorHandlers } from './error-handlers';

// Setup error handlers immediately
setupGlobalErrorHandlers();

// Initialize your app
initializeApp();
```

---

## Important: Error Boundary Limitations

Error Boundaries in React **DO NOT** catch:

- ❌ **Event handlers** (use try/catch in the handler)
- ❌ **Async code** (use try/catch or .catch())
- ❌ **Server-side rendering**
- ❌ **Errors in the Error Boundary itself**

**They DO catch:**

- ✅ **Render phase errors**
- ✅ **Lifecycle methods**
- ✅ **Constructors of child components**

### Example: Event Handler Errors

```tsx
// ❌ Error Boundary won't catch this
function PaymentButton() {
  const handleClick = () => {
    throw new Error('Payment failed');  // Not caught!
  };

  return <button onClick={handleClick}>Pay</button>;
}

// ✅ Use try/catch in event handlers
function PaymentButton() {
  const handleClick = async () => {
    try {
      await processPayment();
      showSuccess('Payment successful');
    } catch (error) {
      logger.error({ error, traceId }, 'Payment failed');
      showError('Payment failed. Please try again.');
    }
  };

  return <button onClick={handleClick}>Pay</button>;
}
```

---

## TypeScript Type Declarations

```typescript
// src/types/global.d.ts

interface Window {
  Sentry?: {
    captureException(
      error: Error,
      options?: {
        tags?: Record<string, string>;
        extra?: Record<string, unknown>;
        level?: string;
      }
    ): void;
  };
}
```

---

## Testing Error Handlers

```typescript
// src/app/error-handlers.test.ts

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { setupGlobalErrorHandlers, cleanupGlobalErrorHandlers } from './error-handlers';

describe('Global Error Handlers', () => {
  beforeEach(() => {
    setupGlobalErrorHandlers();
    vi.spyOn(console, 'error').mockImplementation(() => {});
  });

  afterEach(() => {
    cleanupGlobalErrorHandlers();
    vi.restoreAllMocks();
  });

  it('catches unhandled promise rejections', async () => {
    const error = new Error('Test rejection');

    // Trigger unhandled rejection
    Promise.reject(error);

    // Wait for event to fire
    await new Promise(resolve => setTimeout(resolve, 0));

    expect(console.error).toHaveBeenCalledWith(
      expect.stringContaining('Unhandled promise rejection'),
      expect.objectContaining({ reason: error })
    );
  });

  it('catches global errors', () => {
    const error = new Error('Test error');

    // Trigger global error
    window.dispatchEvent(
      new ErrorEvent('error', {
        error,
        message: error.message,
        filename: 'test.js',
        lineno: 1,
        colno: 1,
      })
    );

    expect(console.error).toHaveBeenCalledWith(
      expect.stringContaining('Global error'),
      expect.objectContaining({ error })
    );
  });
});
```

---

## Deliverables

After running this prompt, you should have:

- ✅ Global error handlers module created
- ✅ Unhandled rejection handler
- ✅ Global error handler
- ✅ React Error Boundary (if React)
- ✅ Integration with logging system
- ✅ Error monitoring service integration
- ✅ User-friendly error UI
- ✅ App initialization code
- ✅ TypeScript type declarations
- ✅ Test coverage

---

## Next Steps

1. **Customize error UI** - Implement showErrorToUser with your UI library
2. **Configure error monitoring** - Setup Sentry/Datadog API keys
3. **Test error flows** - Trigger errors to verify catching
4. **Add correlation IDs** (use #js-debug-correlation-id-setup)
5. **Setup structured logging** (use #js-debug-logging-setup if not done)
6. **Add retry logic** - Implement exponential backoff for retryable errors

---

**Related:**
- [JavaScript Debugging Reference](../../docs/javascript-debugging-reference.md#3-unhandled-error-handlers)
- [JavaScript Debugger Mode](../../chatmodes/javascript/js-debugger.chatmode.md)
- [Error Classes Prompt](./js-debug-error-classes.prompt.md)
- [Logging Setup Prompt](./js-debug-logging-setup.prompt.md)
