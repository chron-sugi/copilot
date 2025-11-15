---
description: "Setup structured logging with topic-based loggers and production integration"
mode: 'agent'
model: Auto
tools: ['codebase', 'edit']
---

# Setup Structured Logging

Configure structured logging for: **${input:projectName}**

---

## Project Information

**Project Name**: ${input:projectName}

**Framework**: ${input:framework:React/Next.js/Node.js/Express}

**TypeScript**: ${input:typescript:Yes}

**Logging Service**: ${input:loggingService:Sentry/Datadog/LogRocket/Custom/None}

**Target File**: ${input:targetFile:src/shared/logger.ts}

---

## Requirements

Create a structured logging system that:

1. **Uses objects, not strings** - Queryable fields
2. **Includes correlation/trace IDs** - Distributed tracing
3. **Topic-based loggers** - Organized by feature area
4. **Production integration** - Sends to logging service
5. **Development-friendly** - Pretty prints locally

---

## Implementation

### Core Logger Implementation

```typescript
// ${input:targetFile:src/shared/logger.ts}

export type LogLevel = 'debug' | 'info' | 'warn' | 'error';

export interface LogContext {
  [key: string]: unknown;
  userId?: string;
  traceId?: string;
  sessionId?: string;
  error?: Error | string;
  errorStack?: string;
}

interface LogEntry {
  level: LogLevel;
  topic: string;
  message: string;
  timestamp: number;
  [key: string]: unknown;
}

/**
 * Create a topic-based logger
 *
 * @param topic - Feature area (e.g., 'checkout:payment', 'auth:login')
 * @returns Logger instance with debug, info, warn, error methods
 *
 * @example
 * const logger = log('checkout:payment');
 * logger.info({ userId, orderId, amount }, 'Payment initiated');
 */
export function log(topic: string) {
  return {
    debug(context: LogContext, message: string): void {
      this._log('debug', topic, context, message);
    },

    info(context: LogContext, message: string): void {
      this._log('info', topic, context, message);
    },

    warn(context: LogContext, message: string): void {
      this._log('warn', topic, context, message);
    },

    error(context: LogContext, message: string): void {
      this._log('error', topic, context, message);
    },

    _log(level: LogLevel, topic: string, context: LogContext, message: string): void {
      const entry: LogEntry = {
        level,
        topic,
        message,
        timestamp: Date.now(),
        ...context,
      };

      // Development: pretty print to console
      if (process.env.NODE_ENV === 'development') {
        logToDevelopmentConsole(level, topic, message, context);
      } else {
        // Production: send to logging service
        sendToLoggingService(entry);
      }
    },
  };
}

/**
 * Pretty print logs in development
 */
function logToDevelopmentConsole(
  level: LogLevel,
  topic: string,
  message: string,
  context: LogContext
): void {
  const colors = {
    debug: '\x1b[36m',  // Cyan
    info: '\x1b[32m',   // Green
    warn: '\x1b[33m',   // Yellow
    error: '\x1b[31m',  // Red
  };
  const reset = '\x1b[0m';
  const color = colors[level];

  console.log(
    `${color}[${level.toUpperCase()}]${reset} [${topic}] ${message}`,
    context
  );
}

/**
 * Send logs to production logging service
 */
function sendToLoggingService(entry: LogEntry): void {
  // Add your logging service integration here
  // Examples below for common services

  ${input:loggingService === 'Sentry' ? `
  // Sentry integration
  if (entry.level === 'error' && typeof window !== 'undefined' && window.Sentry) {
    window.Sentry.captureException(
      entry.error instanceof Error ? entry.error : new Error(entry.message),
      {
        tags: { topic: entry.topic },
        extra: entry,
        level: 'error',
      }
    );
  }
  ` : ''}

  ${input:loggingService === 'Datadog' ? `
  // Datadog integration
  if (typeof window !== 'undefined' && window.DD_LOGS) {
    window.DD_LOGS.logger.log(entry.message, entry, entry.level);
  }
  ` : ''}

  ${input:loggingService === 'LogRocket' ? `
  // LogRocket integration
  if (typeof window !== 'undefined' && window.LogRocket) {
    window.LogRocket.log(entry.level, entry.message, entry);
  }
  ` : ''}

  // Fallback: structured console logging
  console.log(JSON.stringify(entry));
}
```

---

## Integration Examples

### React Component Example

```typescript
import { log } from '@/shared/logger';
import { getCurrentTraceId } from '@/shared/tracing';

const logger = log('checkout:payment');

export function PaymentForm() {
  const handleSubmit = async (formData: FormData) => {
    const amount = formData.get('amount');
    const userId = getCurrentUserId();
    const traceId = getCurrentTraceId();

    logger.info({
      userId,
      traceId,
      amount,
      timestamp: Date.now(),
    }, 'Payment form submitted');

    try {
      await processPayment({ amount });

      logger.info({
        userId,
        traceId,
        amount,
      }, 'Payment successful');

      showSuccess('Payment completed');
    } catch (error) {
      logger.error({
        userId,
        traceId,
        amount,
        error: error instanceof Error ? error.message : String(error),
        errorStack: error instanceof Error ? error.stack : undefined,
      }, 'Payment failed');

      showError('Payment failed. Please try again.');
    }
  };

  return <form onSubmit={handleSubmit}>{/* ... */}</form>;
}
```

### API Client Example

```typescript
import { log } from '@/shared/logger';
import { getCurrentTraceId } from '@/shared/tracing';

const logger = log('api:http');

export async function apiRequest<T>(
  url: string,
  options: RequestInit = {}
): Promise<T> {
  const traceId = getCurrentTraceId();
  const startTime = Date.now();

  logger.debug({
    traceId,
    url,
    method: options.method || 'GET',
  }, 'API request started');

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        ...options.headers,
        'X-Trace-Id': traceId || '',
      },
    });

    const duration = Date.now() - startTime;

    if (!response.ok) {
      logger.warn({
        traceId,
        url,
        status: response.status,
        duration,
      }, 'API request failed with non-2xx status');

      throw new HttpError('Request failed', response.status);
    }

    logger.debug({
      traceId,
      url,
      status: response.status,
      duration,
    }, 'API request completed');

    return response.json();
  } catch (error) {
    const duration = Date.now() - startTime;

    logger.error({
      traceId,
      url,
      error: error instanceof Error ? error.message : String(error),
      errorStack: error instanceof Error ? error.stack : undefined,
      duration,
    }, 'API request failed with error');

    throw error;
  }
}
```

### Node.js/Express Middleware Example

```typescript
import { log } from './logger';

const logger = log('http:request');

export function requestLoggingMiddleware(
  req: Request,
  res: Response,
  next: NextFunction
): void {
  const startTime = Date.now();
  const traceId = req.headers['x-trace-id'] as string || crypto.randomUUID();

  logger.info({
    traceId,
    method: req.method,
    url: req.url,
    userAgent: req.headers['user-agent'],
    ip: req.ip,
  }, 'Request received');

  res.on('finish', () => {
    const duration = Date.now() - startTime;

    logger.info({
      traceId,
      method: req.method,
      url: req.url,
      status: res.statusCode,
      duration,
    }, 'Request completed');
  });

  next();
}
```

---

## TypeScript Type Declarations (if using third-party services)

```typescript
// src/types/global.d.ts

interface Window {
  Sentry?: {
    captureException(error: Error, options?: {
      tags?: Record<string, string>;
      extra?: Record<string, unknown>;
      level?: string;
    }): void;
  };

  DD_LOGS?: {
    logger: {
      log(message: string, context: Record<string, unknown>, level: string): void;
    };
  };

  LogRocket?: {
    log(level: string, message: string, context: Record<string, unknown>): void;
  };
}
```

---

## Common Logging Topics

Establish consistent topic naming conventions:

**Format**: `{domain}:{feature}:{action?}`

**Examples**:
- `auth:login` - User login
- `auth:logout` - User logout
- `auth:register` - User registration
- `checkout:payment` - Payment processing
- `checkout:shipping` - Shipping calculation
- `api:http` - HTTP requests
- `api:graphql` - GraphQL queries
- `data:cache` - Cache operations
- `data:sync` - Data synchronization
- `ui:error` - UI error handling
- `ui:performance` - Performance tracking

---

## Migration Strategy

### Replace console.log Calls

**❌ Before:**
```typescript
console.log('User logged in:', userId);
console.error('Payment failed:', error);
```

**✅ After:**
```typescript
import { log } from '@/shared/logger';
const logger = log('auth:login');

logger.info({ userId, traceId }, 'User logged in');
logger.error({
  userId,
  traceId,
  error: error.message,
  errorStack: error.stack
}, 'Payment failed');
```

### Find and Replace Pattern

Use your editor to find: `console\.(log|info|warn|error)\(`

Then refactor to structured logging with appropriate topic.

---

## Testing the Logger

```typescript
// ${input:testFile:src/shared/logger.test.ts}

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { log } from './logger';

describe('Logger', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.spyOn(console, 'log').mockImplementation(() => {});
  });

  it('creates topic-based logger', () => {
    const logger = log('test:feature');
    expect(logger).toHaveProperty('debug');
    expect(logger).toHaveProperty('info');
    expect(logger).toHaveProperty('warn');
    expect(logger).toHaveProperty('error');
  });

  it('logs with context', () => {
    const logger = log('test:feature');
    logger.info({ userId: '123', action: 'test' }, 'Test message');

    expect(console.log).toHaveBeenCalled();
  });

  it('includes timestamp', () => {
    const logger = log('test:feature');
    const beforeTime = Date.now();

    logger.info({ userId: '123' }, 'Test message');

    const afterTime = Date.now();
    const call = (console.log as any).mock.calls[0];
    const context = call[1];

    expect(context.timestamp).toBeGreaterThanOrEqual(beforeTime);
    expect(context.timestamp).toBeLessThanOrEqual(afterTime);
  });
});
```

---

## Deliverables

After running this prompt, you should have:

- ✅ Logger module created at **${input:targetFile}**
- ✅ Type-safe logging with LogLevel and LogContext
- ✅ Topic-based logger factory function
- ✅ Development console pretty printing
- ✅ Production logging service integration
- ✅ Usage examples for React, API, Node.js
- ✅ TypeScript type declarations (if needed)
- ✅ Migration strategy documented
- ✅ Test coverage

---

## Next Steps

1. **Integrate with error classes** (use #js-debug-error-classes)
2. **Setup correlation IDs** (use #js-debug-correlation-id-setup)
3. **Add global error handlers** (use #js-debug-error-handler-setup)
4. **Migrate existing console.log** calls to structured logging
5. **Configure logging service** (Sentry, Datadog, etc.)
6. **Add logging to critical paths** (auth, checkout, API calls)

---

**Related:**
- [JavaScript Debugging Reference](../../docs/javascript-debugging-reference.md#2-structured-logging)
- [JavaScript Debugger Mode](../../chatmodes/javascript/js-debugger.chatmode.md)
- [Error Classes Prompt](./js-debug-error-classes.prompt.md)
- [Correlation ID Setup Prompt](./js-debug-correlation-id-setup.prompt.md)
