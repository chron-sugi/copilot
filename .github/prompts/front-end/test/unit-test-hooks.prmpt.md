You are now in **TESTING MODE**, not implementation mode.

Target:
Write Vitest tests for **Type 3 modules: React hooks** that encapsulate data fetching, stateful logic, or derived view models.

These tests should:
- Focus on **state transitions and returned values**.
- Treat hooks as logic units (no DOM layout concerns).
- Use mocks for network / API calls, not real I/O.

Do **NOT** modify production hook code in this task; only create test files.

---

## 1) General approach for Type 3 hooks

For each hook module (example names):

- `src/features/diagram/hooks/useDiagramData.ts`
- `src/features/diagram/hooks/useNodeDetails.ts`
- `src/features/diagram/hooks/useSplCode.ts`
- `src/features/diagram/hooks/useDiagramSearch.ts`

create a matching test file:

- `useDiagramData.test.ts`
- `useNodeDetails.test.ts`
- `useSplCode.test.ts`
- `useDiagramSearch.test.ts`

Use:

- **Vitest** (`describe`, `it`/`test`, `expect`)
- **React Testing Library**’s hook utilities:
  - Either `renderHook` (from RTL or `@testing-library/react-hooks` if present),
  - Or render a small test component that calls the hook and exposes its results.

---

## 2) Behavior to test (state transitions)

For each hook, design tests based on its responsibilities:

### Examples

1. `useDiagramData`
   - Should expose **loading → success → error** states.
   - Given a successful fetch:
     - returns normalized diagram data (nodes/edges) with expected structure.
   - Given a failed fetch (mocked network error):
     - sets `error` state,
     - does not leave stale `data` from previous run.

2. `useNodeDetails`
   - Given a selected node ID and raw diagram data:
     - returns `nodeDetails` with expected fields (name, type, owner, app, last_modified, description, hasSpl, etc.).
   - Given an unknown node ID:
     - returns `null` or an appropriate “no details” state.
   - Verify that changes in selected ID update the returned details.

3. `useSplCode`
   - Given a node with `spl_code`:
     - returns the SPL string and status flags (e.g., `isLoading`, `isError`).
   - If SPL is loaded from a separate endpoint:
     - mock success and failure paths.

4. `useDiagramSearch`
   - Given a query and a list of nodes:
     - returns matching node suggestions (id + label + type/app if applicable).
   - Edge cases:
     - empty query → no suggestions.
     - query with no matches → empty suggestions and “no results” state.

---

## 3) Test structure & mocking

### 3.1 Test file skeleton

Each test file should:

```ts
import { renderHook } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { useDiagramData } from './useDiagramData'; // adjust path as needed
