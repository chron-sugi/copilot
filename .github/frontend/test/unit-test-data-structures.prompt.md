You are now in TESTING MODE, not implementation mode.

Target:
Write Vitest tests for the Zod schemas and related types in:

  <REPLACE_WITH_SCHEMA_FILE_PATH>  // e.g. src/features/diagram/model/diagram.schema.ts

These are Type 1 tests: validation/invariant tests for data contracts.
Do NOT modify any production code in this task; only create a test file.

High-level goal:
- Confirm that valid examples pass validation.
- Confirm that clearly invalid examples fail with Zod errors.
- Capture important invariants encoded in the schemas (required fields, type constraints, relationships).

--------------------------------
1) Test file & structure
--------------------------------
- Create a test file next to the schema file, e.g.:

  - <same-folder>/<schema-filename>.test.ts
  - Example: src/features/diagram/model/diagram.schema.test.ts

- Use Vitest:
  - `describe`, `it`/`test`, `expect`.

--------------------------------
2) Valid (happy-path) tests
--------------------------------
For each exported schema that is part of the public contract (not internal helpers):

1. Create at least one **valid example** object:
   - Based on the type definition / Zod shape.
   - Use realistic values when possible (IDs, names, timestamps, etc.).

2. Write tests that:
   - Use `schema.parse(example)` or `schema.safeParse(example)`.
   - Assert that valid examples are accepted:
     - parse: does not throw.
     - safeParse: `success === true` and `data` matches the input shape.

3. For schemas that include nested arrays/objects, include at least one valid nested example.

--------------------------------
3) Invalid (adversarial) tests
--------------------------------
Now design tests that should FAIL if the schema is working correctly.

For each schema, include invalid examples such as:

- Missing required fields.
- Wrong types (string where number is expected, etc.).
- Extra fields if the schema is strict.
- Violations of obvious invariants derived from comments/types, such as:
  - IDs that must be non-empty.
  - Enums with unsupported values.
  - Relationships that must exist (e.g. references to IDs that must be present elsewhere, if enforced by the schema).

Tests should:

- Use `schema.safeParse(invalid)` and assert:
  - `success === false`.
  - Optionally, that `error.issues` contains at least one issue touching the offending field.

Mark a few of these as “edge cases” in comments so it’s clear they’re stress-testing the contract.

--------------------------------
4) Style & scope
--------------------------------
- Keep each test focused on a single schema/aspect:
  - “accepts a valid DiagramSubgraph”
  - “rejects subgraph missing nodes”
  - “rejects invalid enum value for node kind”
- Use small helper builders inside the test file if that improves readability (e.g. base valid object + overrides).
- Do NOT over-generate tests; 3–6 well-chosen tests per important schema is enough for now.

--------------------------------
5) Output expectations
--------------------------------
- Create the test file and write the tests.
- In your final response, list:
  - the test file path,
  - the describe/it names you added,
  - and a short sentence for what each test verifies.
- Do NOT modify the schema file in this task.
