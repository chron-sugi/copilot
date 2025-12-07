---
name: frontend.fsd-feature-audit
agent: agent
model: Claude Opus 4.5 (Preview) (copilot)
description: These instructions tell you, the coding agent, how to **audit a specific feature slice** in a React/TypeScript project for compliance with Feature-Sliced Design (FSD) principles.
argument-hint: Feature name
---

# Task: Assess Whether a Specific Feature Is FSD-Compliant

You are auditing **one specific feature slice** in a React/TypeScript project that targets **full Feature-Sliced Design (FSD)**.

Your goals:

1. Inspect `src/features/${input:feature_name}` only.
2. Check its **folder structure**, **imports**, and **responsibilities** against FSD rules.
3. Identify any **violations** (structure, layering, responsibilities, naming).
4. Produce a short **PASS / FAIL** summary plus a list of issues & recommendations.

---

## 0. Canonical FSD Context for This Check

FSD layers (top → bottom):

- `src/app`       – app shell, router, providers, global store wiring.
- `src/pages`     – route-level pages. Compose widgets/features/entities.
- `src/widgets`   – layout-level blocks (header, side nav, panels, toolbars).
- `src/features`  – user-facing capabilities / flows (this is what you are checking).
- `src/entities`  – domain entities (user, product, lineage, etc.).
- `src/shared`    – generic, reusable ui/lib/api/config/model/assets.
- `src/types`     – global, cross-cutting TypeScript types.

### What a “feature” is

A **feature** represents a **user-facing capability / flow**, not just a data type:

- Examples: `auth`, `spl-editor`, `dashboard-filters`, `change-password`, `export-results`.

---

## 1. Locate and Describe the Feature Slice

1. Verify the feature slice folder:

   - Expected path:

     ```txt
     src/features/${input:feature_name}/
     ```

2. If the folder does not exist:
   - Mark `feature_exists: false`.
   - Mark `fsd_feature_compliant: false`.
   - Stop the assessment.

3. If it exists, list its **immediate contents** (folders + key files).

---

## 2. Folder Structure Check

Check whether the feature uses the standard internal FSD segments.

### 2.1 Expected segments (some may be optional)

The canonical shape is:

```txt
src/features/${input:feature_name}/
  ui/        # React components (TSX/JSX) for this feature
  model/     # state, hooks, feature-level types/schemas/constants
  api/       # data fetching / side-effect calls for this feature
  lib/       # pure feature-specific helpers (no React)
  config/    # feature-level configuration (flags, options, defaults)
  index.ts   # public API of this feature slice
```

### 2.2 Evaluate structure

For `${input:feature_name}`:

- Check which of these folders are present: `ui`, `model`, `api`, `lib`, `config`.
- Check if there are **TSX/TS files directly under the feature root** (outside these folders).

Mark issues such as:

- `missing_ui_folder: true` (if UI components exist but are not under `ui/`).
- `has_files_in_root: true` (if feature logic/JSX is in root instead of segment folders).
- `missing_index_ts: true` (no public API barrel).

---

## 3. Import Direction & Layering Rules

For **all files** inside `src/features/${input:feature_name}`:

### 3.1 Allowed imports

- May import from:
  - `features/*` (other features, if really necessary – but keep minimal).
  - `entities/*`
  - `shared/*`
  - `types` (global types).
  - Local paths inside the same feature.

### 3.2 Forbidden imports

- MUST NOT import from:
  - `app/*`
  - `pages/*`
  - `widgets/*`

### 3.3 Assessment

1. Scan imports in `ui`, `model`, `api`, `lib`, `config` files.
2. Record violations, e.g.:

   - `imports_from_app: [file paths]`
   - `imports_from_pages: [file paths]`
   - `imports_from_widgets: [file paths]`

3. Note any **circular dependencies** within the feature (e.g. `ui` importing from `model`, but `model` also importing from `ui`), which is a structural smell.

---

## 4. Responsibility & Logic Placement

### 4.1 `ui/` folder

Check components under `ui/`:

- SHOULD:
  - Render JSX.
  - Compose hooks from `model` and components from `entities` / `shared/ui`.
- SHOULD NOT:
  - Contain large blocks of business logic.
  - Call raw HTTP clients (e.g. `fetch`, `axios`) directly.
  - Access global providers or router objects directly (preferred via feature hooks).

Mark issues like:

- `ui_contains_business_logic: true` with examples.
- `ui_calls_http_directly: true`.

### 4.2 `model/` folder

Check files under `model/`:

- SHOULD contain:
  - Hooks: `useFeatureX`, `useSomethingFor${input:feature_name}`.
  - Feature-local types & interfaces (state, form values).
  - Schemas & validators (Zod/Yup) for this feature.
  - Selectors/derivations of state.

- SHOULD NOT:
  - Import React components from `ui`.
  - Depend on `app` or `pages`.

Mark issues:

- `model_imports_ui: true`.
- `model_imports_app_or_pages: true`.

### 4.3 `api/` folder

Check files under `api/`:

- SHOULD:
  - Contain data fetching & side effects for this feature (HTTP calls, etc.).
  - Use shared HTTP clients (`shared/api`) if available.

- SHOULD NOT:
  - Export React components.
  - Be imported directly by pages; pages should use `model`/hooks.

Mark issues:

- `api_contains_jsx: true`.
- `api_used_directly_in_pages: true` (if visible).

### 4.4 `lib/` folder

Check `lib/` (if present):

- SHOULD:
  - Contain pure, reusable feature-specific helpers (no React, no side effects).
- SHOULD NOT:
  - Import React or other UI libraries.
  - Use global state/store directly if it can be handled via `model`.

Mark issues:

- `lib_imports_react: true`.
- `lib_contains_side_effects: true`.

### 4.5 `config/` folder

Check `config/` (if present):

- SHOULD:
  - Capture feature-specific config (flags, static maps, defaults).
- SHOULD NOT:
  - Contain executable business logic or side effects.

---

## 5. Types, Schemas, and Constants Location

For this feature:

1. Types:
   - Check that feature-specific types are under:
     - `src/features/${input:feature_name}/model/{something}.types.ts`
   - Confirm they are **not** incorrectly placed in `src/types` unless truly global.

2. Schemas & validation:
   - Feature-specific schemas (Zod/Yup) should live in `model/` (or `api/` for pure API contracts).

3. Constants:
   - Feature-local domain/constants should live in `model/` or `config/`.
   - They should not be scattered in random files at the feature root.

Mark issues such as:

- `feature_types_in_global_types_folder: true`
- `schemas_not_in_model_or_api: true`

---

## 6. Public API of the Feature

Check `src/features/${input:feature_name}/index.ts` (if present):

- SHOULD:
  - Re-export the **public** components/hooks of this feature.
  - Provide a small, clean interface to other layers (pages, widgets, other features).

Example pattern:

```ts
// src/features/${input:feature_name}/index.ts
export * from './ui/FeatureComponent';
export * from './model/useFeatureHook';
```

Assess:

- `has_index_ts: true | false`
- `index_exports_are_clean: true | false`  
  (i.e. not re-exporting internal-only helpers unnecessarily).

---

## 7. Feature Usage Check (Optional but Recommended)

If feasible, locate where this feature is imported:

- Pages (`src/pages/*`)
- Widgets (`src/widgets/*`)
- Other features (`src/features/*`)

Check that:

- Pages/widgets import from the **feature barrel** (`features/${input:feature_name}`) rather than deep internal paths when possible.
- There are no heavy two-way dependencies between this feature and another feature.

Mark issues:

- `deep_imports_into_feature: true` (pages/widgets importing deep files instead of barrel).
- `mutual_feature_dependencies: [featureA <-> featureB]`.

---

## 8. Final Assessment Summary

Produce a concise summary in a structured format, e.g.:

```json
{
  "feature_name": "${input:feature_name}",
  "feature_exists": true,
  "fsd_feature_compliant": true | false,
  "structure": {
    "has_ui": true,
    "has_model": true,
    "has_api": true,
    "has_lib": true,
    "has_config": false,
    "has_index_ts": true,
    "root_has_loose_files": false
  },
  "layering_issues": {
    "imports_from_app": [],
    "imports_from_pages": [],
    "imports_from_widgets": []
  },
  "responsibility_issues": {
    "ui_contains_business_logic": false,
    "ui_calls_http_directly": false,
    "model_imports_ui": false,
    "api_contains_jsx": false
  },
  "types_schemas_constants_issues": {
    "feature_types_in_global_types_folder": false,
    "schemas_not_in_model_or_api": false
  },
  "other_notes": [
    "Example: index.ts exports are clean and used by pages.",
    "Example: consider extracting shared helpers from lib to shared/lib if reused."
  ]
}
```

Set `"fsd_feature_compliant"` to:

- `true` if:
  - Folder structure is aligned (or very close) to `ui/model/api/lib/config/index.ts`,
  - There are no major layering violations,
  - Business logic is properly in `model/api/lib`, and
  - Types/schemas/constants are in appropriate locations.

- `false` if:
  - There are significant layering violations,
  - Page/app-level concerns leak into this feature, or
  - Core feature code is not segmented into FSD segments.

The output should clearly state:
- Whether the feature is FSD-compliant.
- What issues remain.
- Short recommendations for the next refactor steps.
