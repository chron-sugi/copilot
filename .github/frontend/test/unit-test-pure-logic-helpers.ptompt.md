You are now in TESTING MODE, not implementation mode.

Target:
Write Vitest unit tests for all pure logic helpers in /src/
These are tests: focused, deterministic unit tests for pure functions (no React, no DOM).
Do NOT modify any production code in this task; only create test files.

High-level goal:
- Verify correct behavior for normal inputs (happy paths).
- Exercise edge cases and error conditions (adversarial/negative tests).
- Ensure functions behave deterministically and don’t rely on hidden globals.

--------------------------------
1) Test file & structure
--------------------------------
- Create a test file next to the helper file, e.g.:

  - <same-folder>/<helper-filename>.test.ts
  - Example: src/features/diagram/lib/splHelpers.test.ts

- Use Vitest:
  - `describe`, `it`/`test`, `expect`.

- Import only the public functions that should be tested from the helper module.

--------------------------------
2) Happy-path tests
--------------------------------
For each exported function that is part of the public API:

1. Write at least one test that covers a “normal” use case:
   - Choose clear, realistic inputs.
   - Assert on the exact expected output.
   - Keep tests small and deterministic (no randomness, no real network, no timers).

2. If the function has multiple typical modes (e.g., different flags or options), include a test per mode where it makes sense.

Examples of assertions:
- exact equality for simple values/objects,
- array contents and order,
- presence/absence of fields.

--------------------------------
3) Adversarial / edge-case tests
--------------------------------
Now design tests that should fail if the implementation is too weak or incorrect.

For each function, consider:

- Boundary inputs (empty arrays, empty strings, zero/negative numbers).
- Invalid inputs (wrong types, missing fields) if the function is expected to handle or reject them.
- Corner cases derived from the design:
  - e.g., “no matching items”, “multiple matches”, “circular references” (for graph-like logic).

Write tests that:
- Make the expected behavior explicit:
  - Should it throw? Return a default? Return an empty result?
- Use `expect(() => fn(...)).toThrow()` when errors are expected.
- Use clear names/comments for edge-case tests so intent is obvious.

You may mark in comments which tests would currently fail if you suspect the implementation is incomplete or too permissive.

--------------------------------
4) Style & scope
--------------------------------
- Keep tests focused:
  - One behavior per test.
  - One function (or closely related functions) per `describe` block.
- Avoid mocking unless absolutely necessary:
  - Prefer pure inputs/outputs over mocking internals.
  - If time-dependent logic exists, isolate Date/now into a parameter or small wrapper before testing.

- If helper functions depend on types (e.g., `NodeDetails`, `DiagramNode`), either:
  - import the type, or
  - construct minimal inline objects that satisfy the shape.

--------------------------------
5) Output expectations
--------------------------------
- Create the test file and write the tests.
- In your final response, list:
  - the test file path,
  - the `describe`/`it` names you added,
  - and a short sentence for what each test verifies.
- Do NOT modify the helper module in this task.
