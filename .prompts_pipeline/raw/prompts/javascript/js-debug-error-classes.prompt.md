---
description: "Generate error categorization boilerplate classes for JavaScript projects"
mode: 'agent'
model: Auto
tools: ['codebase', 'edit']
---

# Generate Error Categorization Classes

Generate error categorization boilerplate for: **${input:projectName}**

---

## Project Information

**Project Name**: ${input:projectName}

**Framework**: ${input:framework:React/Next.js/Node.js/Other}

**TypeScript**: ${input:typescript:Yes/No}

**Target File**: ${input:targetFile:src/shared/errors.ts}

---

## Requirements

Create error categorization classes following the JavaScript playbook pattern:

### Error Categories

1. **DomainError**
   - User-facing errors
   - Show to user
   - Don't retry
   - Examples: validation errors, business rule violations

2. **TechnicalError**
   - System/infrastructure errors
   - Log and retry (if retryable)
   - Don't show technical details to user
   - Examples: network errors, database errors

3. **FatalError**
   - Unrecoverable errors
   - Circuit breaker pattern
   - Alert on-call team
   - Examples: configuration errors, critical system failures

4. **HttpError** (extends TechnicalError)
   - HTTP-specific errors
   - Status-based retry strategy
   - 5xx = retryable, 4xx = not retryable

---

## Implementation Template

Generate code following this structure:

```typescript
// Base error classes with .cause support

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
  constructor(
    message: string,
    public readonly status: number,
    cause?: unknown
  ) {
    super(message, status >= 500, cause);  // 5xx are retryable
    this.name = 'HttpError';
  }
}

// Type guards for error handling

export function isDomainError(error: unknown): error is DomainError {
  return error instanceof DomainError;
}

export function isTechnicalError(error: unknown): error is TechnicalError {
  return error instanceof TechnicalError;
}

export function isFatalError(error: unknown): error is FatalError {
  return error instanceof FatalError;
}

export function isHttpError(error: unknown): error is HttpError {
  return error instanceof HttpError;
}

// Error.cause polyfill for older browsers (if needed)
if (!('cause' in Error.prototype)) {
  Object.defineProperty(Error.prototype, 'cause', {
    get() {
      return (this as any)._cause;
    },
    set(value) {
      (this as any)._cause = value;
    },
  });
}
```

---

## Additional Error Types (Optional)

Based on project needs, consider adding:

**ValidationError** (extends DomainError):
```typescript
export class ValidationError extends DomainError {
  constructor(
    message: string,
    public readonly field: string,
    public readonly value: unknown,
    cause?: unknown
  ) {
    super(message, cause);
    this.name = 'ValidationError';
  }
}
```

**AuthenticationError** (extends DomainError):
```typescript
export class AuthenticationError extends DomainError {
  constructor(message: string = 'Authentication required', cause?: unknown) {
    super(message, cause);
    this.name = 'AuthenticationError';
  }
}
```

**AuthorizationError** (extends DomainError):
```typescript
export class AuthorizationError extends DomainError {
  constructor(
    message: string = 'Insufficient permissions',
    public readonly requiredPermission?: string,
    cause?: unknown
  ) {
    super(message, cause);
    this.name = 'AuthorizationError';
  }
}
```

**NotFoundError** (extends DomainError):
```typescript
export class NotFoundError extends DomainError {
  constructor(
    public readonly resource: string,
    public readonly id: string | number,
    cause?: unknown
  ) {
    super(`${resource} with ID ${id} not found`, cause);
    this.name = 'NotFoundError';
  }
}
```

---

## Usage Examples

Include usage examples in comments or separate documentation:

```typescript
// Example 1: HTTP request with error categorization
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
    if (error instanceof HttpError) {
      throw error;  // Already categorized
    }
    throw new TechnicalError(
      'Network error updating cart',
      true,  // Retryable
      error
    );
  }
}

// Example 2: Error handling strategy
try {
  await updateCart(item);
} catch (error) {
  if (isDomainError(error)) {
    // Show to user, don't retry
    showErrorToast(error.message);
  } else if (isTechnicalError(error)) {
    // Log and retry if retryable
    logger.error({ error, userId, traceId });
    if (error.retryable) {
      await retryWithBackoff(() => updateCart(item));
    }
  } else if (isFatalError(error)) {
    // Circuit breaker, alert on-call
    circuitBreaker.open();
    alertOnCall(error);
  }
}
```

---

## Testing Boilerplate (Optional)

Generate test file: **${input:testFile:src/shared/errors.test.ts}**

```typescript
import { describe, it, expect } from 'vitest';
import {
  DomainError,
  TechnicalError,
  FatalError,
  HttpError,
  isDomainError,
  isTechnicalError,
  isFatalError,
  isHttpError,
} from './errors';

describe('Error Classes', () => {
  describe('DomainError', () => {
    it('creates error with message', () => {
      const error = new DomainError('Invalid input');
      expect(error.message).toBe('Invalid input');
      expect(error.name).toBe('DomainError');
    });

    it('preserves cause', () => {
      const cause = new Error('Root cause');
      const error = new DomainError('Validation failed', cause);
      expect(error.cause).toBe(cause);
    });
  });

  describe('TechnicalError', () => {
    it('marks as retryable', () => {
      const error = new TechnicalError('Network error', true);
      expect(error.retryable).toBe(true);
    });

    it('marks as non-retryable', () => {
      const error = new TechnicalError('Parse error', false);
      expect(error.retryable).toBe(false);
    });
  });

  describe('HttpError', () => {
    it('marks 5xx as retryable', () => {
      const error = new HttpError('Server error', 500);
      expect(error.retryable).toBe(true);
      expect(error.status).toBe(500);
    });

    it('marks 4xx as non-retryable', () => {
      const error = new HttpError('Bad request', 400);
      expect(error.retryable).toBe(false);
      expect(error.status).toBe(400);
    });
  });

  describe('Type guards', () => {
    it('identifies DomainError', () => {
      const error = new DomainError('Test');
      expect(isDomainError(error)).toBe(true);
      expect(isTechnicalError(error)).toBe(false);
    });

    it('identifies HttpError as TechnicalError', () => {
      const error = new HttpError('Test', 500);
      expect(isHttpError(error)).toBe(true);
      expect(isTechnicalError(error)).toBe(true);
    });
  });
});
```

---

## Deliverables

After running this prompt, you should have:

- ✅ Error classes file created at **${input:targetFile}**
- ✅ Base error classes (Domain, Technical, Fatal, Http)
- ✅ Type guards for error handling
- ✅ Error.cause polyfill (if needed)
- ✅ Optional: Additional error types (Validation, Auth, NotFound)
- ✅ Optional: Test file with coverage
- ✅ Optional: Usage examples in comments

---

## Next Steps

After generating error classes:

1. **Update imports** in existing error handling code
2. **Categorize existing errors** by replacing generic Error
3. **Add type guards** to error handling logic
4. **Setup logging** with structured error context (use #js-debug-logging-setup)
5. **Add global handlers** (use #js-debug-error-handler-setup)
6. **Test error flows** with new categorization

---

**Related:**
- [JavaScript Debugging Reference](../../docs/javascript-debugging-reference.md#1-error-categorization)
- [JavaScript Debugger Mode](../../chatmodes/javascript/js-debugger.chatmode.md)
- [Logging Setup Prompt](./js-debug-logging-setup.prompt.md)
