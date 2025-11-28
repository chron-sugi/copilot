You are a coding agent working in a modern TypeScript front-end codebase (feature-first architecture).  
Follow these rules exactly when creating, updating, or refactoring **constants** and **configuration**.

1. General rules
   - Keep constants/config **immutable** and **declarative** (no side effects, no business logic).
   - Use **TypeScript**, not JSON, for constants and config.
   - Prefer many small, focused files over large mixed “god files”.
   - Always use **high-signal filenames** that include both the domain and the role.

2. File locations and names — feature-specific
   - If a value is used only inside a single feature, place it under that feature’s folder.
   - Use this naming pattern:
     - `src/features/{featureName}/{featureName}.constants.ts`
     - `src/features/{featureName}/{featureName}.config.ts`
   - Examples:
     - `src/features/diagram/diagram.constants.ts`
     - `src/features/diagram/diagram.config.ts`
     - `src/features/search/search.constants.ts`
     - `src/features/search/search.config.ts`

3. File locations and names — shared/global
   - If a value is used across multiple features, treat it as shared.
   - Place shared **constants** in: `src/constants/{domain}.constants.ts`
   - Place shared **config** in: `src/config/{domain}.config.ts`
   - Example shared constants files:
     - `src/constants/app.constants.ts`
     - `src/constants/ui.constants.ts`
     - `src/constants/layout.constants.ts`
     - `src/constants/spl.constants.ts`
     - `src/constants/errors.constants.ts`
     - `src/constants/keyboard.constants.ts`
   - Example shared config files:
     - `src/config/env.config.ts`
     - `src/config/api.config.ts`
     - `src/config/routes.config.ts`
     - `src/config/feature-flags.config.ts`
     - `src/config/theme.config.ts`

4. Forbidden filenames
   - Do **not** create or keep ambiguous files like:
     - `constants.ts`
     - `config.ts`
     - `helpers.ts`
     - `misc.ts`
   - Always include the **domain** and **role** in the filename, using `{domain}.{role}.ts`.

5. Export style and typing
   - Use **named exports only**. Do **not** use default exports for constants or config.
   - For primitive constants, use `UPPER_SNAKE_CASE`:
     ```ts
     export const DEFAULT_PAGE_SIZE = 25;
     export const MAX_NODES_PER_DIAGRAM = 500;
     ```
   - For structured config objects, use `camelCase` and `as const`:
     ```ts
     export const apiConfig = {
       timeoutMs: 10000,
       retries: 3,
     } as const;
     ```
   - For collections of literals, use `as const` and derive types:
     ```ts
     export const LAYOUT_MODES = ["hierarchical", "radial", "grid"] as const;
     export type LayoutMode = (typeof LAYOUT_MODES)[number];
     ```
   - Never mutate constants or config objects at runtime.

6. Environment configuration
   - Do **not** read environment variables directly in components or feature files.
   - Always access them through `src/config/env.config.ts`.
   - In `env.config.ts`, define a single exported object, for example:
     ```ts
     export const envConfig = {
       appEnv: import.meta.env.VITE_APP_ENV ?? "development",
       apiBaseUrl: import.meta.env.VITE_API_BASE_URL,
     } as const;
     ```
   - Use this in other files via:
     ```ts
     import { envConfig } from "@/config/env.config";
     ```
   - Respect framework prefixes:
     - Vite: `VITE_*`
     - Next.js: `NEXT_PUBLIC_*`
   - If there is an env schema/validation, update it whenever you add or change env variables.

7. Design tokens and theming
   - Do **not** scatter design tokens (colors, spacing, typography, radii, etc.) into feature constants or random files.
   - Store design tokens only in:
     - `tailwind.config.(js|ts)`, and/or
     - `src/config/theme.config.ts`, and/or
     - CSS variables (e.g. `:root { --color-primary: ... }`).
   - If you encounter duplicated or hard-coded tokens in constants, prefer centralizing them in the theme configuration.

8. Behavior rules
   - Do **not** put business logic, API calls, or side effects in constants or config files.
   - If dynamic behavior depending on configuration is needed, keep the logic in services/hooks/components, not in the config module.
   - Test **behavior that depends on constants/config**, not the literal values themselves.

9. When adding or refactoring constants/config
   - Decide if the value is **feature-local** or **shared**.
   - Choose the correct location:
     - Feature-local → `src/features/{featureName}/{featureName}.constants.ts` or `.config.ts`.
     - Shared → `src/constants/{domain}.constants.ts` or `src/config/{domain}.config.ts`.
   - Ensure the filename follows `{domain}.{role}.ts`.
   - Use named exports and proper casing (`UPPER_SNAKE_CASE` for primitives, `camelCase` for config objects).
   - Use `as const` where it helps preserve literal types.
   - Update all imports to reference the new or renamed modules.
   - If a file mixes multiple unrelated domains, split it into separate `{domain}.{role}.ts` files.

10. Target structure (reference)
   - When possible, shape the project towards this structure:
     - `src/features/diagram/diagram.constants.ts`
     - `src/features/diagram/diagram.config.ts`
     - `src/features/search/search.constants.ts`
     - `src/features/search/search.config.ts`
     - `src/constants/app.constants.ts`
     - `src/constants/ui.constants.ts`
     - `src/constants/layout.constants.ts`
     - `src/constants/spl.constants.ts`
     - `src/constants/errors.constants.ts`
     - `src/constants/keyboard.constants.ts`
     - `src/config/env.config.ts`
     - `src/config/api.config.ts`
     - `src/config/routes.config.ts`
     - `src/config/feature-flags.config.ts`
     - `src/config/theme.config.ts`

Always apply these rules when creating, moving, or editing constants and configuration.
