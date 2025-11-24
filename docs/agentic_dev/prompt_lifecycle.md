For every new feature or change, follow this loop:

1) Define a small, focused slice + acceptance criteria.

2) Define or update data contracts first:
   - Add/extend Zod schemas in *.schema.ts.
   - Infer TS types via z.infer in *.types.ts.
   - Validate only at boundaries (fetch, storage, URL params).

3) Design tests before heavy implementation:
   - Unit tests for pure logic (e.g., mapping JSON → nodes/edges).
   - Component tests for UI states and interactions.
   - Include happy path, at least one edge case, and one error case.

4) Implement in small, reviewable modules:
   - Keep functions short and cohesive.
   - Extract shared logic to lib/model; avoid duplicating functions.
   - Move configurable values (URLs, thresholds, SPL refs) into config/constants modules, not hard-coded inline.

5) Run automatic gates locally:
   - tsc --noEmit
   - ESLint (TypeScript + React rules)
   - Relevant tests
   - Optional static analysis/security checks

6) Submit a small PR and perform code review using a checklist:
   - Look for duplicated logic that should be extracted.
   - Look for hard-coded values that belong in config/constants.
   - Ensure existing types/schemas are reused.
   - Confirm tests cover new behavior and error paths.

7) Refactor with tests green, then merge.
