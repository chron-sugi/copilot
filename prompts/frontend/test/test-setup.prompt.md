---
name: SetupFrontEndTestEnvironment
description: Test setup for a React + TypeScript front-end project
agent: 'FrontEndDeveloper'
model: 'GPT-5 mini'
argument-hint: 'Describe the change you want; optionally include #file / #codebase / #terminalSelection context.'
---

t
You are a senior TypeScript + React engineer. Your task is to set up a unit/component testing environment for this project.

Context:
- This is a React + TypeScript app (with Vite or similar bundler).
- We want fast, modern, agent-friendly testing:
  - Vitest for unit/component tests
  - React Testing Library for React components
  - No E2E tests yet (Playwright/Cypress is out of scope for this task)

Constraints:
- Do NOT change any runtime app behavior.
- Keep changes minimal and localized to config, devDeps, and test setup.
- Use the existing package manager (npm/yarn/pnpm) based on existing lockfile.

--------------------------------
1) Detect stack & choose tools
--------------------------------
1. Inspect:
   - package.json
   - vite.config.* or equivalent bundler config
   - tsconfig.json
2. Confirm this is a Vite-like React + TS setup.
3. Choose:
   - vitest
   - @testing-library/react
   - @testing-library/user-event
   - @testing-library/jest-dom
   - jsdom (if not already present)

--------------------------------
2) Add dev dependencies
--------------------------------
1. Add the testing devDependencies to package.json using the existing package manager.
2. Do NOT remove or downgrade existing deps.
3. Keep versions compatible with:
   - current React version
   - current Vite version (if applicable)

--------------------------------
3) Configure Vitest
--------------------------------
1. If using Vite:
   - Update vite.config.* to include a `test` block, for example:

     test: {
       environment: 'jsdom',
       setupFiles: './src/test/setupTests.ts',
       globals: true,
     }

   - Adjust paths and filenames to match this repo’s structure.
2. If there is already a vitest config, extend it instead of replacing it.
3. Do NOT disable source maps or break existing dev/build configs.

--------------------------------
4) Testing setup file
--------------------------------
1. Create a setup file, e.g. `src/test/setupTests.ts` (adjust path if needed).
2. In that file:
   - Import `@testing-library/jest-dom` to extend expect matchers.
   - Optionally set basic global RTL config if needed.
3. Ensure vite.config / vitest config points to this setup file.

--------------------------------
5) NPM scripts
--------------------------------
1. In package.json, add or update scripts:

   - "test": "vitest run"
   - "test:watch": "vitest"
   - (optional) "test:unit": "vitest run"

2. Do NOT remove existing scripts.
3. If there is already a test script, adapt it to vitest instead of leaving it broken.

--------------------------------
6) Sample tests
--------------------------------
1. Add a small demo unit test file to verify setup, e.g.:

   - `src/lib/graph-utils.test.ts` if graph-utils exists, OR
   - `src/example/example.test.ts` if no clear candidate.

2. The test should:
   - import a real function/component from the repo,
   - assert a simple, deterministic behavior,
   - run successfully with `npm test` (or equivalent).

3. Add one tiny React component test using React Testing Library, e.g. a simple component or the smallest presentational component available:

   - Render it,
   - Assert text/role is present.

--------------------------------
7) Run & verify
--------------------------------
1. Run:
   - the main test script (e.g., `npm test`),
   - and ensure tests pass with a non-zero count.
2. Fix any config or import issues until the test suite is green.
3. Do NOT add a large number of tests in this task; the goal is to have a working test environment, not complete coverage.

--------------------------------
8) Documentation note
--------------------------------
1. Add a short note (3–5 lines) to an existing doc (e.g. README or TESTING.md if present) explaining:
   - that we use Vitest + React Testing Library,
   - how to run tests (`npm test`, `npm run test:watch`).

--------------------------------
9) Output
--------------------------------
In your final response:
- List the files you modified/created.
- Confirm the exact command to run tests.
- Confirm that the sample tests pass locally.
- Do NOT include full file contents unless specifically asked; summarize changes instead.
