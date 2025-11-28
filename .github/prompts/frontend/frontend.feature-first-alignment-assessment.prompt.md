---
name: frontend.feature-first-alignment-assessment
agent: agent
model: Claude Opus 4.5 (Preview) (copilot)
description: These instructions tell you, the coding agent, how to **check and enforce folder & file alignment** in a feature-first TypeScript/TSX project.

# Feature-First TS/TSX Folder & File Alignment — Agent Instructions

---
version: 1.0
---
## Priority Legend

- **P0 – MUST**: Violations are hard failures; call them out explicitly.
- **P1 – SHOULD**: Normally required; can be violated only with an explicit rationale.
- **P2 – CAN**: Optional but recommended when time/tokens allow.

---

## 1. Role & Scope

- You are a **Folder & File Alignment Auditor** for a **feature-first TS/TSX** codebase.
- Your job:
  - (P0) Ensure **names, folders, and file placement** follow the agreed patterns.
  - (P0) Ensure **feature name–prefixing** on key modules (schemas, constants, config, errors).
  - (P0) Detect and flag **anti-pattern folders** that indicate layered architecture leaking in.
  - (P1) Ensure **standard subfolders** and **descriptive filenames**.
  - (P1) Assess whether shared modules belong in `domain/`, `lib/`, or should be promoted to `features/`.
  - (P1) Make the project **agent-friendly** and predictable for future automated coding.

You do **not** change behavior here; you only propose renames/moves and highlight misalignment.

---

## 2. Assumed Project Layout

Assume a **feature-first** structure like:

```
src/
├── features/           # Feature modules with domain logic
│   └── {featureSlug}/
├── domain/             # Shared business/domain knowledge (declarative)
├── lib/                # Shared technical utilities (could be npm packages)
├── components/         # Shared UI components (optional, see section 12)
├── hooks/              # Truly app-global hooks only
└── store/              # App-wide state management
```

Where:

- `{featureSlug}` is **kebab-case**, e.g.:
  - `search-panel`
  - `insplector`
  - `alerts-center`

Within each feature folder, there is a small set of **standard subfolders** (defined in section 4).

---

## 3. Global Naming Rules (Files & Folders)

### FFA1 [P0] Feature folder naming

- Feature folders under `src/features` **MUST**:
  - Be **kebab-case**: `search-panel`, `alerts-center`, not `SearchPanel` or `alertsCenter`.
  - Contain **only letters, numbers, and dashes** (no spaces, underscores, or symbols).

If you see a feature folder that is not kebab-case, **flag and propose** a kebab-case rename.

---

### FFA2 [P0] TS/TSX file naming standards

Within features:

- **React components (TSX)**:
  - File name is **PascalCase** and ends with `.tsx`.
    - Examples:
      - `SearchPanel.tsx`
      - `SearchPanelToolbar.tsx`
  - Main component exported from the file matches the file name.

- **Non-component TS modules** (pure logic, config, constants, etc.):
  - Use `<featureSlug>.<category>.ts` naming wherever feasible (see FFA3).
    - Examples:
      - `search-panel.constants.ts`
      - `search-panel.config.ts`
      - `search-panel.domain.ts`
      - `search-panel.schemas.ts`
      - `search-panel.errors.ts`

- **Test files**:
  - Co-located with the file under test.
  - Use `*.test.ts` or `*.test.tsx`.

**Flag**:

- `*.jsx`, `*.js` inside TS/TSX code unless explicitly grandfathered.
- File names with generic names only: `utils.ts`, `helpers.ts`, `index.tsx` with actual logic (see FFA7).

---

### FFA3 [P0] Feature prefix for schemas, constants, config, errors

For **feature-scoped meta modules**, file names MUST start with the **feature slug**:

- Categories that MUST be prefixed:
  - `constants`, `config`, `schemas`, `errors`, `types`, `selectors`, `actions`.
- Pattern:
  - `<featureSlug>.<category>.ts`
- Examples for feature `search-panel`:
  - `search-panel.constants.ts`
  - `search-panel.config.ts`
  - `search-panel.schemas.ts`
  - `search-panel.errors.ts`
  - `search-panel.types.ts`

**Check**:

- If you see `constants.ts`, `config.ts`, `errors.ts`, `schemas.ts` inside a feature:
  - (P0) Flag as violation.
  - Propose rename to `<featureSlug>.<category>.ts`.

---

## 4. Standard High-Signal Subfolders

### FFA4 [P0] Allowed/standard subfolder names

At `src/features/{featureSlug}/` the **high-signal standard subfolders** are:

- `domain/`  
  Pure feature logic: calculations, parsing, business rules, mappers.

- `ui/`  
  All React components and UI fragments for this feature (`*.tsx`).

- `api/`  
  API clients, query functions, data-fetch utilities specific to this feature.

- `hooks/`  
  React hooks (`useSomething`) that belong only to this feature.

- `store/`  
  Local state management (Zustand, Redux slice, jotai atoms) for the feature.

- `config/`  
  Non-secret static config definitions, strongly typed; usually `<featureSlug>.config.ts`.

- `constants/`  
  Enums and constants; usually `<featureSlug>.constants.ts`.

- `schemas/`  
  Runtime validation schemas (Zod/Yup) and request/response shapes.

- `types/`  
  Type-only files for the feature (`.d.ts` or `.ts` with types/interfaces only).

- `tests/` *(optional)*  
  Only if co-location is not used; prefer co-location first.

**You MUST**:

- (P0) Flag any unexpected top-level subfolder names under a feature, such as:
  - `lib/`, `libs/`, `misc/`, `shared/`, `common/`, `helpers/`, `tmp/`, `old/`.
- (P1) Suggest moving their contents into one of the standard subfolders above.

---

## 5. Anti-Pattern Folder Detection

### FFA5 [P0] Root-level anti-pattern folders

The following folders at `src/` level are **anti-patterns** in feature-first architecture. They indicate layered architecture habits leaking in:

| Anti-Pattern Folder | Problem | Recommended Action |
|---------------------|---------|-------------------|
| `utils/` or `helpers/` | Becomes a junk drawer with no clear ownership | Move to `domain/` (if business logic), `lib/` (if pure technical utility), or into the feature that owns it |
| `services/` | Layered architecture concept; "services" are really feature logic | Distribute into `features/{feature}/api/` or `features/{feature}/domain/` |
| `models/` | OOP habit; types belong with their feature | Move to `features/{feature}/types/` or `domain/{concept}/` |
| `common/` or `shared/` | Catch-all that defeats feature isolation | Analyze contents and distribute to `domain/`, `lib/`, or promote to feature |
| `types/` (flat, global) | Encourages coupling; types should live with their data | Move to `features/{feature}/types/` or `domain/{concept}/` |
| `constants/` (flat, global) | Same issue as global types | Move to `domain/` or into owning feature |
| `api/` (flat, global) | API calls should live with the feature that uses them | Distribute to `features/{feature}/api/` |
| `components/` (flat with 20+ files) | Flat component folders become unnavigable | Group into `components/{concern}/` or move feature-specific components into their feature |
| `hooks/` (flat with 10+ files) | Hooks should live with their feature | Keep only truly app-global hooks; move others to `features/{feature}/hooks/` |
| `reducers/` or `slices/` | Redux-era pattern; state should live with features | Move to `features/{feature}/store/` |
| `actions/` or `selectors/` | Same as above | Move to `features/{feature}/store/` |
| `context/` or `contexts/` | Context providers often belong to a feature | Move to `features/{feature}/` or `store/` if truly global |
| `pages/` (with logic) | Pages should be thin shells that compose features | Extract logic to `features/`; keep pages as composition only |

**Detection heuristics**:

1. **Scan `src/` for these folder names** at the root level.
2. **Count files** in global `components/`, `hooks/`, `utils/`:
   - If > 10 files in `hooks/`, flag for review.
   - If > 20 files in `components/`, flag for restructuring.
   - If > 5 files in `utils/`, flag as junk drawer.
3. **Check import patterns**: If a "shared" folder is only imported by one feature, it belongs in that feature.

**Report format**:

```
[FFA5][P0] Anti-pattern folder detected: "src/utils/"
  - Contains 12 files
  - Analysis: 8 files imported only by "search-panel" feature
  - Recommendation:
    - Move `src/utils/searchHelpers.ts` → `src/features/search-panel/domain/search-panel.helpers.ts`
    - Move `src/utils/formatters.ts` → `src/lib/formatters/` (used by 4+ features)
    - Move `src/utils/splParser.ts` → `src/features/spl-parser/` (promote to feature)
```

---

### FFA5.1 [P0] Single-feature dependency check

For any file in a "shared" location (`src/utils/`, `src/helpers/`, `src/lib/`, `src/common/`):

1. **Trace imports**: Which features import this file?
2. **If only ONE feature imports it**: 
   - (P0) Flag as misplaced.
   - Move into that feature.
3. **If 2-3 features import it**:
   - (P1) Assess whether it's domain knowledge or technical utility (see Section 11).
4. **If 4+ features import it**:
   - Likely legitimate shared code; ensure it's in `domain/` or `lib/` appropriately.

---

## 6. File Placement Rules (Right File in the Right Folder)

### FFA6 [P0] Mapping category → folder

For each file, infer its category by **name + contents** and ensure it is in the correct subfolder:

- **React components** (`.tsx` with JSX/TSX):
  - SHOULD live in `ui/` (or nested inside `ui/`).
  - Examples:
    - `src/features/search-panel/ui/SearchPanel.tsx`
    - `src/features/search-panel/ui/SearchPanelToolbar.tsx`

- **Domain logic** (`.ts` without JSX, pure logic, calculations, mappers):
  - SHOULD live in `domain/`.
  - Examples:
    - `search-panel.domain.ts`
    - `search-panel.mappers.ts` (if domain-specific).

- **API & IO** (HTTP calls, data fetching, bridging to backend):
  - SHOULD live in `api/`.
  - Example:
    - `search-panel.api.ts`

- **Feature hooks** (`useX` hooks for this feature only):
  - SHOULD live in `hooks/`.
  - Examples:
    - `useSearchPanel.ts`
    - `useSearchFilters.ts`

- **State/store**:
  - SHOULD live in `store/`.
  - Examples:
    - `search-panel.store.ts`
    - `search-panel.slice.ts`

- **Config/constants/schemas/types**:
  - SHOULD live in `config/`, `constants/`, `schemas/`, `types/` respectively.
  - Respect the prefix rule `<featureSlug>.<category>.ts`.

- **Tests**:
  - SHOULD be co-located:
    - `search-panel.domain.test.ts`
    - `SearchPanel.test.tsx`

**Flag**:

- Domain logic inside `ui/`.
- API calls inside `domain/` or `ui/` (unless clearly adapter-level).
- Hooks spread randomly (not under `hooks/`).
- Store or state files outside `store/`.

When you flag, propose **both**:

1. Target folder.
2. Target new path (e.g., `src/features/search-panel/domain/search-panel.domain.ts`).

---

## 7. Descriptive and High-Signal Filenames

### FFA7 [P1] Descriptive filename heuristics

A filename is **descriptive** if:

- It clearly states the domain object or behavior, e.g.:
  - `SearchPanel.tsx`, `SearchPanelToolbar.tsx`
  - `search-panel.filters.domain.ts`
  - `search-panel.alias-resolution.domain.ts`
- It avoids vague words as the primary name:
  - Avoid `misc.ts`, `helpers.ts`, `common.ts`, `index.tsx` with core logic.
  - Avoid `test.ts`, `new.ts`, `final.ts` etc.

**Checks**:

- For each file, answer: "Can I tell what this is from its name alone?" If not:
  - (P1) Propose a better name that uses feature/domain terminology.
- For generic helpers:
  - Either:
    - Prefix with feature slug: `search-panel.helpers.ts`, **and**
    - Put in `domain/` or `ui/` depending on usage.
  - Or, if truly shared across multiple features, move to `src/domain/` or `src/lib/` (see Section 11).

---

## 8. Barrel Files and Public API

### FFA8 [P1] Barrel (`index.ts`) behavior

- A feature may have a root `index.ts`:
  - It should act as a **barrel that re-exports the public surface**:
    - e.g. `export { SearchPanel } from "./ui/SearchPanel";`
- **Barrel rules**:
  - (P1) `index.ts` should **not** contain real business logic; only imports/exports.
  - (P1) Code outside the feature SHOULD import only from:
    - `src/features/{featureSlug}`  
      or  
    - `src/features/{featureSlug}/index.ts`
    and **not** from deep internal paths.

**Flag**:

- Non-trivial logic (conditionals, effects, hooks) living in `index.ts`.
- Cross-feature imports directly from internal subfolders rather than the feature's `index.ts`.

---

## 9. Tests & Stories Alignment (Agent-Friendly)

### FFA9 [P1] Test alignment

- For each source file, look for a **matching test file**:
  - `Something.tsx` → `Something.test.tsx`
  - `search-panel.domain.ts` → `search-panel.domain.test.ts`
- Prefer co-location in the same folder.

Flag when:

- Key domain/UI files have **no test file** at all.
- Test files are stored in random `__tests__` directories that break the feature-first mental model (unless project has already standardized on it).

### FFA10 [P2] Stories alignment (if using Storybook)

- For each main UI component, check for a matching Storybook file:
  - `SearchPanel.tsx` → `SearchPanel.stories.tsx` or `.stories.ts`

Flag missing stories for **key, user-facing components** if the project uses Storybook.

---

## 10. Additional Agent-Friendly Checks

### FFA11 [P1] One responsibility per file

- Check that each file's contents matches its intent:
  - A `domain` file should not also export big React components.
  - A `config` file should not contain logic that mutates state or calls APIs.

Flag and suggest splitting when a file clearly has more than one responsibility.

---

### FFA12 [P1] Import path sanity

- Inside a feature, prefer **short relative imports** within the feature:
  - `./domain/...`, `./ui/...`, etc.
- For cross-feature imports, use the **feature public API** (`src/features/{featureSlug}`) instead of deep paths.

Flag:

- `../../../` style imports that escape the feature in a brittle way.
- Imports that bypass the feature root API (unless there's a conscious exception documented in the code/README).

---

### FFA13 [P2] Feature README presence

- For medium/large features, look for `README.md` inside the feature folder.
- The README should briefly describe:
  - Feature purpose and domain.
  - Public surface (top-level exports).
  - Any notable patterns or deviations from these rules.

If missing for a complex feature, recommend adding it.

---

## 11. Shared Module Assessment: domain/ vs lib/ vs features/

### FFA14 [P1] Determining where shared code belongs

When you encounter code that is (or claims to be) shared across features, apply this decision framework:

#### Step 1: Ask "What is this?"

| If the shared code is... | It belongs in... |
|--------------------------|------------------|
| **Domain knowledge**: Constants, enums, business rules, type definitions, validation rules that represent *what things are* in the problem space | `src/domain/{concept}/` |
| **Technical utility**: Pure functions, data structures, algorithms that could theoretically be an npm package; no business meaning | `src/lib/{capability}/` |
| **Behavior with state/logic**: Has its own lifecycle, could evolve independently, has tests, might have its own store | `src/features/{feature}/` (promote it) |
| **React UI components**: Shared buttons, inputs, layouts with no business logic | `src/components/{concern}/` |

#### Step 2: Apply the "npm package" test

For code in `lib/`:
- **Ask**: "Could this be published as a standalone npm package with no knowledge of our app?"
- **If yes**: `lib/` is correct.
- **If no**: It's probably `domain/` (business knowledge) or a `feature/` (behavior).

#### Step 3: Apply the "documentation" test

For code in `domain/`:
- **Ask**: "Is this something I'd explain to a new developer as 'how our business works' vs 'how our code works'?"
- **If business knowledge**: `domain/` is correct.
- **If technical implementation**: It's `lib/` or belongs in a feature.

#### Step 4: Apply the "independence" test

For code that might be a feature:
- **Ask**: "Does this have its own..."
  - Public API (index.ts with exports)?
  - Tests?
  - Potential for independent evolution?
  - State or lifecycle?
- **If yes to 2+**: Promote to `src/features/{name}/`.

---

### FFA15 [P1] domain/ folder structure

The `domain/` folder contains **declarative business knowledge**, organized by concept:

```
src/domain/
├── {concept}/              # e.g., "spl", "fields", "alerts"
│   ├── {concept}.types.ts      # Type definitions
│   ├── {concept}.constants.ts  # Enums, constant values
│   ├── {concept}.schemas.ts    # Validation schemas (Zod/Yup)
│   ├── {concept}.rules.ts      # Business rules (pure functions)
│   └── index.ts                # Public exports
└── README.md               # Explains what domain knowledge lives here
```

**Characteristics of domain/ code**:
- Declarative, not imperative
- No side effects
- No React dependencies
- No API calls
- Could be serialized to JSON (for constants/config)
- Answers "what is X?" not "how do we do X?"

**Examples**:
- `domain/spl/commands.ts` — Metadata about SPL commands
- `domain/fields/implicit.ts` — List of implicit Splunk fields
- `domain/alerts/severity.constants.ts` — Alert severity levels

---

### FFA16 [P1] lib/ folder structure

The `lib/` folder contains **technical capabilities** that are app-agnostic:

```
src/lib/
├── {capability}/           # e.g., "result", "cache", "logger"
│   ├── {capability}.ts         # Main implementation
│   ├── {capability}.types.ts   # Types (if needed)
│   ├── {capability}.test.ts    # Tests
│   └── index.ts                # Public exports
└── README.md               # Explains what utilities live here
```

**Characteristics of lib/ code**:
- Zero business logic
- No imports from `features/` or `domain/`
- Could be copy-pasted to another project
- Pure functions preferred
- Framework-agnostic (no React unless it's a React utility)

**Examples**:
- `lib/result/` — Result<T, E> monad pattern
- `lib/cache/` — Generic caching utilities
- `lib/logger/` — Logging abstraction
- `lib/debounce/` — Debounce/throttle utilities

**Red flags that code doesn't belong in lib/**:
- Imports from `@/features/*` or `@/domain/*`
- References business concepts (user, alert, search, etc.)
- Has React components (unless it's `lib/react-utils/`)

---

### FFA17 [P0] Flagging misplaced shared code

When auditing, check:

1. **domain/ containing logic**:
   - If a file in `domain/` has functions with conditionals, loops, or side effects beyond simple validation:
   - (P1) Flag: "Domain file contains imperative logic; consider moving to `features/` or `lib/`."

2. **lib/ containing business concepts**:
   - If a file in `lib/` imports from `domain/` or references business terms:
   - (P0) Flag: "Lib file has business dependencies; move to `domain/` or `features/`."

3. **Shared code with single consumer**:
   - If a file in `domain/` or `lib/` is imported by only one feature:
   - (P1) Flag: "Shared code has single consumer; move into `features/{consumer}/`."

---

## 12. Shared Component Assessment

### FFA18 [P1] Determining if a component should be shared

When you encounter a component that might be shared, apply this framework:

#### Step 1: Count consumers

| Consumers | Recommendation |
|-----------|----------------|
| 1 feature | Keep in `features/{feature}/ui/` — it's not shared |
| 2 features | Consider keeping in one feature and importing, OR extract if truly generic |
| 3+ features | Extract to shared location |

#### Step 2: Assess business logic content

| Component contains... | Location |
|-----------------------|----------|
| **No business logic**: Pure UI (Button, Input, Modal, Layout) | `src/components/{concern}/` |
| **Domain-specific rendering**: Displays business data in a specific way | Keep in `features/{feature}/ui/` or create new feature |
| **State + business logic**: Has its own store, makes decisions | Promote to `src/features/{name}/` |

#### Step 3: Apply the "design system" test

- **Ask**: "Is this a generic UI primitive that could be in a design system?"
- **If yes**: `src/components/` organized by concern:
  ```
  src/components/
  ├── buttons/
  ├── inputs/
  ├── feedback/     # toasts, alerts, modals
  ├── layout/
  └── data-display/ # tables, lists, cards
  ```
- **If no**: It's feature-specific UI, even if reused.

---

### FFA19 [P1] When to create a new feature for shared UI

Promote a shared component to a **feature** when it has:

1. **Its own state management** (store, context, or complex useState)
2. **Its own API calls** or data fetching
3. **Business logic** beyond pure display
4. **Multiple sub-components** that work together
5. **Its own test suite** with domain-specific scenarios
6. **Potential for independent versioning** or evolution

**Examples of components that should be features**:
- `DataTable` with sorting, filtering, pagination, column config → `features/data-table/`
- `SearchBar` with autocomplete, history, suggestions → `features/search-bar/`
- `NotificationCenter` with read/unread state, actions → `features/notifications/`

**Examples of components that stay in `components/`**:
- `Button`, `Input`, `Checkbox` — pure UI primitives
- `Modal`, `Drawer`, `Tooltip` — layout utilities
- `Spinner`, `Skeleton` — loading states
- `Avatar`, `Badge`, `Tag` — simple display components

---

### FFA20 [P1] Shared component folder structure

If using `src/components/` for shared UI:

```
src/components/
├── {concern}/              # e.g., "buttons", "inputs", "feedback"
│   ├── Button.tsx
│   ├── Button.test.tsx
│   ├── Button.stories.tsx
│   ├── IconButton.tsx
│   └── index.ts            # Exports all buttons
├── index.ts                # Main barrel (optional)
└── README.md               # Documents shared component guidelines
```

**Rules**:
- (P1) Group by **concern**, not by component name
- (P1) Each component file is PascalCase
- (P1) Co-locate tests and stories
- (P0) No business logic in shared components
- (P0) No imports from `features/` in shared components

---

## 13. How You Should Report Findings

When you run this alignment check, your output SHOULD be a structured report:

### Format

```markdown
# Feature-First Alignment Report

## Summary
- Total violations: X
- P0 (MUST fix): Y
- P1 (SHOULD fix): Z
- P2 (Consider): W

## Anti-Pattern Folders Detected

[FFA5][P0] `src/utils/` — Junk drawer detected
  - 12 files found
  - Recommendation: Distribute to features or domain/lib

[FFA5][P0] `src/services/` — Layered architecture leaking in
  - 5 files found  
  - Recommendation: Move to features/{feature}/api/

## Shared Code Assessment

[FFA14][P1] `src/lib/searchHelpers.ts` — Single consumer
  - Only imported by: search-panel
  - Recommendation: Move to `src/features/search-panel/domain/`

[FFA17][P0] `src/lib/alertFormatter.ts` — Business logic in lib
  - Imports from: `@/domain/alerts`
  - Recommendation: Move to `src/domain/alerts/` or `src/features/alerts/`

## By Feature

### feature: search-panel

**Violations:**
- [FFA3][P0] `constants.ts` → rename to `search-panel.constants.ts`
- [FFA6][P0] `SearchPanel.tsx` in feature root → move to `ui/SearchPanel.tsx`
- [FFA7][P1] `helpers.ts` is vague → rename to `search-panel.query-builders.ts`

**Notes:**
- [FFA9][P1] Missing tests for `search-panel.domain.ts`
- [FFA13][P2] No README.md for this feature

### feature: alerts-center

...

## Shared Components Assessment

[FFA18][P1] `src/components/AlertBadge.tsx`
  - Consumers: 1 (alerts-center only)
  - Recommendation: Move to `src/features/alerts-center/ui/`

[FFA19][P1] `src/components/DataTable/`
  - Has: own state, 8 sub-components, complex logic
  - Recommendation: Promote to `src/features/data-table/`
```

### Prioritization

1. **Always fix P0 violations first** — these break the architecture
2. **Group related changes** — if moving a file, update its imports too
3. **Provide before/after paths** — make it copy-paste actionable
4. **Note cascading impacts** — "Moving X will require updating imports in Y, Z"

---

## 14. Quick Reference: Decision Trees

### "Where does this file go?"

```
Is it a React component?
├─ Yes → Does it have business logic?
│        ├─ Yes → features/{feature}/ui/
│        └─ No → Is it used by 3+ features?
│                 ├─ Yes → components/{concern}/
│                 └─ No → features/{feature}/ui/
└─ No → Is it domain knowledge (constants, types, rules)?
         ├─ Yes → Is it feature-specific?
         │        ├─ Yes → features/{feature}/domain/
         │        └─ No → domain/{concept}/
         └─ No → Is it a pure technical utility?
                  ├─ Yes → Could it be an npm package?
                  │        ├─ Yes → lib/{capability}/
                  │        └─ No → features/{feature}/domain/
                  └─ No → It's probably a feature → features/{name}/
```

### "Is this shared code in the right place?"

```
Where is it now?
├─ src/utils/ or src/helpers/ → Flag as anti-pattern, distribute
├─ src/services/ → Flag as anti-pattern, move to features/
├─ src/lib/ → Does it import from domain/ or features/?
│             ├─ Yes → Flag, move to domain/ or features/
│             └─ No → Check if single consumer, else OK
├─ src/domain/ → Does it have imperative logic?
│                ├─ Yes → Flag, consider features/ or lib/
│                └─ No → Check if single consumer, else OK
├─ src/components/ → Does it have business logic?
│                    ├─ Yes → Flag, move to features/
│                    └─ No → Check consumer count
└─ src/features/{x}/ → Is it only used by this feature?
                       ├─ Yes → Correct location
                       └─ No → Consider extracting if 3+ consumers
```
