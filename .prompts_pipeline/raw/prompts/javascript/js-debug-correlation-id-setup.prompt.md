---
description: "Setup correlation IDs for distributed tracing across frontend and backend"
mode: 'agent'
model: Auto
tools: ['codebase', 'edit']
---

# Setup Correlation IDs for Distributed Tracing

Configure correlation IDs for: **${input:projectName}**

---

## Project Information

**Project Name**: ${input:projectName}

**Frontend Framework**: ${input:frontendFramework:React/Next.js/Vue/Angular}

**Backend Framework**: ${input:backendFramework:Express/Fastify/Next.js API/None}

**TypeScript**: ${input:typescript:Yes}

**Has Logging**: ${input:hasLogging:Yes (from js-debug-logging-setup)/No}

**Target Files**:
- Frontend: ${input:frontendFile:src/shared/tracing.ts}
- Backend: ${input:backendFile:src/middleware/tracing.ts}

---

## Requirements

Setup correlation IDs to:

1. **Generate unique trace IDs** - Per user session or request
2. **Propagate IDs across requests** - Frontend → Backend → Database
3. **Include in HTTP headers** - X-Trace-Id, X-Session-Id
4. **Include in all logs** - Queryable by trace ID
5. **Support distributed systems** - Correlate logs across services

---

## Implementation

### Frontend: Trace ID Management

```typescript
// ${input:frontendFile:src/shared/tracing.ts}

/**
 * Current trace ID (scoped to request/session)
 */
let currentTraceId: string | null = null;

/**
 * Session ID (persisted across page loads)
 */
let sessionId: string | null = null;

/**
 * Initialize session ID from storage
 */
export function initializeSessionId(): void {
  if (typeof window === 'undefined') return;

  sessionId = sessionStorage.getItem('sessionId');

  if (!sessionId) {
    sessionId = crypto.randomUUID();
    sessionStorage.setItem('sessionId', sessionId);
  }
}

/**
 * Get or create a trace ID
 * Call at the start of each user action or request
 */
export function getOrCreateTraceId(): string {
  if (!currentTraceId) {
    currentTraceId = crypto.randomUUID();
  }
  return currentTraceId;
}

/**
 * Get current trace ID (may be null if not yet created)
 */
export function getCurrentTraceId(): string | null {
  return currentTraceId;
}

/**
 * Set trace ID explicitly (e.g., from server response)
 */
export function setTraceId(traceId: string): void {
  currentTraceId = traceId;
}

/**
 * Clear trace ID (e.g., after request completes)
 */
export function clearTraceId(): void {
  currentTraceId = null;
}

/**
 * Get session ID
 */
export function getSessionId(): string | null {
  return sessionId;
}

/**
 * Get user ID (from auth context)
 * Implement based on your auth system
 */
export function getUserId(): string | null {
  // TODO: Implement based on your auth system
  // Examples:
  // - return useAuth().user?.id
  // - return localStorage.getItem('userId')
  // - return getCurrentUser()?.id

  return null;
}

/**
 * Create trace context for logging
 * Use this in all log calls
 */
export function getTraceContext(): {
  traceId: string | null;
  sessionId: string | null;
  userId: string | null;
} {
  return {
    traceId: getCurrentTraceId(),
    sessionId: getSessionId(),
    userId: getUserId(),
  };
}
```

---

### Frontend: HTTP Client with Correlation IDs

```typescript
// ${input:frontendFile.replace('tracing.ts', 'http-client.ts')}

import { getOrCreateTraceId, getSessionId, getUserId } from './tracing';
${input:hasLogging === 'Yes' ? `import { log } from './logger';` : ''}

${input:hasLogging === 'Yes' ? `const logger = log('api:http');` : ''}

/**
 * HTTP client with automatic correlation ID injection
 */
export async function apiRequest<T>(
  url: string,
  options: RequestInit = {}
): Promise<T> {
  const traceId = getOrCreateTraceId();
  const sessionId = getSessionId();
  const userId = getUserId();

  ${input:hasLogging === 'Yes' ? `
  logger.debug({
    traceId,
    sessionId,
    userId,
    url,
    method: options.method || 'GET',
  }, 'API request started');
  ` : ''}

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        ...options.headers,
        'X-Trace-Id': traceId,
        'X-Session-Id': sessionId || '',
        'X-User-Id': userId || '',
        'Content-Type': 'application/json',
      },
    });

    // Extract trace ID from response (if server sends it back)
    const responseTraceId = response.headers.get('X-Trace-Id');
    if (responseTraceId) {
      // Server may have created a new trace ID
      // Use it for subsequent requests in this flow
    }

    if (!response.ok) {
      ${input:hasLogging === 'Yes' ? `
      logger.error({
        traceId,
        sessionId,
        userId,
        url,
        status: response.status,
      }, 'API request failed');
      ` : ''}

      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();

    ${input:hasLogging === 'Yes' ? `
    logger.debug({
      traceId,
      sessionId,
      userId,
      url,
      status: response.status,
    }, 'API request completed');
    ` : ''}

    return data;
  } catch (error) {
    ${input:hasLogging === 'Yes' ? `
    logger.error({
      traceId,
      sessionId,
      userId,
      url,
      error: error instanceof Error ? error.message : String(error),
    }, 'API request failed with error');
    ` : ''}

    throw error;
  }
}
```

---

### Frontend: App Initialization

```typescript
// app/layout.tsx or main.tsx

import { initializeSessionId } from '@/shared/tracing';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  // Initialize session ID on mount
  useEffect(() => {
    initializeSessionId();
  }, []);

  return <html>{children}</html>;
}
```

---

### Backend: Express Middleware

```typescript
// ${input:backendFile:src/middleware/tracing.ts}

import { Request, Response, NextFunction } from 'express';
import { randomUUID } from 'crypto';
${input:hasLogging === 'Yes' ? `import { log } from '../shared/logger';` : ''}

${input:hasLogging === 'Yes' ? `const logger = log('http:request');` : ''}

/**
 * Extend Express Request to include trace context
 */
declare global {
  namespace Express {
    interface Request {
      traceId: string;
      sessionId?: string;
      userId?: string;
    }
  }
}

/**
 * Express middleware to extract or create correlation IDs
 */
export function tracingMiddleware(
  req: Request,
  res: Response,
  next: NextFunction
): void {
  // Extract from headers or create new
  const traceId = (req.headers['x-trace-id'] as string) || randomUUID();
  const sessionId = req.headers['x-session-id'] as string;
  const userId = req.headers['x-user-id'] as string;

  // Attach to request object
  req.traceId = traceId;
  req.sessionId = sessionId;
  req.userId = userId;

  // Send trace ID back in response
  res.setHeader('X-Trace-Id', traceId);

  ${input:hasLogging === 'Yes' ? `
  // Log incoming request
  logger.info({
    traceId,
    sessionId,
    userId,
    method: req.method,
    url: req.url,
    userAgent: req.headers['user-agent'],
    ip: req.ip,
  }, 'Request received');

  // Log response on finish
  res.on('finish', () => {
    logger.info({
      traceId,
      sessionId,
      userId,
      method: req.method,
      url: req.url,
      status: res.statusCode,
    }, 'Request completed');
  });
  ` : ''}

  next();
}
```

---

### Backend: Using Trace Context

```typescript
// Example: Database query with trace context

import { log } from '../shared/logger';

const logger = log('data:users');

export async function getUserProfile(userId: string, req: Request) {
  logger.debug({
    traceId: req.traceId,
    sessionId: req.sessionId,
    userId: req.userId,
    targetUserId: userId,
  }, 'Fetching user profile');

  try {
    const user = await db.users.findById(userId);

    logger.info({
      traceId: req.traceId,
      sessionId: req.sessionId,
      userId: req.userId,
      targetUserId: userId,
    }, 'User profile fetched');

    return user;
  } catch (error) {
    logger.error({
      traceId: req.traceId,
      sessionId: req.sessionId,
      userId: req.userId,
      targetUserId: userId,
      error: error instanceof Error ? error.message : String(error),
    }, 'Failed to fetch user profile');

    throw error;
  }
}
```

---

### Backend: Express App Setup

```typescript
// app.ts or server.ts

import express from 'express';
import { tracingMiddleware } from './middleware/tracing';

const app = express();

// Add tracing middleware early in the chain
app.use(tracingMiddleware);

// Your other middleware and routes
app.use(express.json());
app.use('/api', apiRoutes);

export default app;
```

---

## Next.js API Routes

```typescript
// app/api/users/[id]/route.ts

import { NextRequest, NextResponse } from 'next/server';
import { randomUUID } from 'crypto';
${input:hasLogging === 'Yes' ? `import { log } from '@/shared/logger';` : ''}

${input:hasLogging === 'Yes' ? `const logger = log('api:users');` : ''}

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  // Extract or create trace ID
  const traceId = request.headers.get('x-trace-id') || randomUUID();
  const sessionId = request.headers.get('x-session-id');
  const userId = request.headers.get('x-user-id');

  ${input:hasLogging === 'Yes' ? `
  logger.info({
    traceId,
    sessionId,
    userId,
    targetUserId: params.id,
  }, 'Fetching user');
  ` : ''}

  try {
    const user = await getUserProfile(params.id);

    ${input:hasLogging === 'Yes' ? `
    logger.info({
      traceId,
      sessionId,
      userId,
      targetUserId: params.id,
    }, 'User fetched successfully');
    ` : ''}

    return NextResponse.json(user, {
      headers: {
        'X-Trace-Id': traceId,
      },
    });
  } catch (error) {
    ${input:hasLogging === 'Yes' ? `
    logger.error({
      traceId,
      sessionId,
      userId,
      targetUserId: params.id,
      error: error instanceof Error ? error.message : String(error),
    }, 'Failed to fetch user');
    ` : ''}

    return NextResponse.json(
      { error: 'Failed to fetch user' },
      {
        status: 500,
        headers: {
          'X-Trace-Id': traceId,
        },
      }
    );
  }
}
```

---

## Trace ID Lifecycle

### Frontend Flow

```
User Action
  ↓
getOrCreateTraceId()  // Create new trace ID
  ↓
apiRequest()          // Add to headers: X-Trace-Id
  ↓
Log request           // Include traceId in logs
  ↓
[Request sent]
  ↓
[Response received]
  ↓
Log response          // Same traceId
  ↓
clearTraceId()        // Optional: clear for next action
```

### Backend Flow

```
Request arrives
  ↓
tracingMiddleware()   // Extract or create trace ID
  ↓
req.traceId set       // Available in all route handlers
  ↓
Log request           // Include traceId
  ↓
Process request       // Pass traceId to services
  ↓
Log database ops      // Same traceId
  ↓
Send response         // Include X-Trace-Id header
```

---

## Querying Logs by Trace ID

### Example: Find all logs for a failed request

```
# In your logging service (Datadog, Splunk, etc.)
traceId:"550e8400-e29b-41d4-a716-446655440000"

# Results:
[2025-01-09 10:23:15] [INFO] [api:http] Request started
[2025-01-09 10:23:15] [DEBUG] [data:users] Fetching user profile
[2025-01-09 10:23:16] [ERROR] [data:users] Database connection failed
[2025-01-09 10:23:16] [ERROR] [api:http] Request failed
```

---

## Testing Correlation IDs

```typescript
// src/shared/tracing.test.ts

import { describe, it, expect, beforeEach } from 'vitest';
import {
  getOrCreateTraceId,
  getCurrentTraceId,
  setTraceId,
  clearTraceId,
  initializeSessionId,
  getSessionId,
} from './tracing';

describe('Tracing', () => {
  beforeEach(() => {
    clearTraceId();
    sessionStorage.clear();
  });

  it('creates new trace ID', () => {
    const traceId = getOrCreateTraceId();
    expect(traceId).toMatch(/^[0-9a-f-]{36}$/);
  });

  it('returns same trace ID on subsequent calls', () => {
    const traceId1 = getOrCreateTraceId();
    const traceId2 = getOrCreateTraceId();
    expect(traceId1).toBe(traceId2);
  });

  it('allows setting trace ID explicitly', () => {
    setTraceId('custom-trace-id');
    expect(getCurrentTraceId()).toBe('custom-trace-id');
  });

  it('clears trace ID', () => {
    getOrCreateTraceId();
    clearTraceId();
    expect(getCurrentTraceId()).toBeNull();
  });

  it('persists session ID', () => {
    initializeSessionId();
    const sessionId1 = getSessionId();

    // Simulate page reload
    initializeSessionId();
    const sessionId2 = getSessionId();

    expect(sessionId1).toBe(sessionId2);
  });
});
```

---

## Deliverables

After running this prompt, you should have:

- ✅ Frontend trace ID management module
- ✅ Session ID persistence
- ✅ HTTP client with automatic ID injection
- ✅ Backend tracing middleware (Express/Next.js)
- ✅ Trace context in all logs
- ✅ Response headers with trace ID
- ✅ Type declarations
- ✅ Test coverage
- ✅ Integration examples

---

## Next Steps

1. **Integrate with logging** (use #js-debug-logging-setup)
2. **Update all API calls** to use apiRequest() with correlation IDs
3. **Test distributed tracing** by searching logs by trace ID
4. **Add to error handlers** (use #js-debug-error-handler-setup)
5. **Monitor trace coverage** - Ensure all critical paths have trace IDs
6. **Document for backend team** - Ensure backend services propagate IDs

---

**Related:**
- [JavaScript Debugging Reference](../../docs/javascript-debugging-reference.md#4-correlation-ids)
- [JavaScript Debugger Mode](../../chatmodes/javascript/js-debugger.chatmode.md)
- [Logging Setup Prompt](./js-debug-logging-setup.prompt.md)
- [Error Handler Setup Prompt](./js-debug-error-handler-setup.prompt.md)
