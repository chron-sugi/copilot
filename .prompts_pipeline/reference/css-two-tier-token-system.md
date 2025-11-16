# Design System Architecture Reference — Bullet Summary

> Purpose: Design token architecture, theming systems, and cross-framework distribution  
> Last Updated: 2025-01-08  

---

## Two-Tier Token System

- **Architecture Overview**
  - **Tier 1 – Palette Tokens**
    - Raw values for color, spacing, typography.
    - Naming: `--palette-{category}-{variant}-{shade}`.
    - Used **only by semantic tokens**, never directly in components.
    - Single source of truth for base values.
  - **Tier 2 – Semantic Tokens**
    - Map palette tokens to contextual use cases.
    - Naming: `--{category}-{purpose}-{variant?}-{state?}`.
    - Used directly by components.
    - Encode meaning and support theming.

- **Why Two Tiers**
  - Clear separation: raw values vs semantic meaning.
  - Flexible theming: remap semantic → palette per theme.
  - Easier maintenance: update one palette value to affect many usages.
  - Better documentation: semantic names explain intent.

---

## Token Naming Conventions

- **Palette Tokens (Tier 1)**
  - **Colors**
    - Scales like `--palette-blue-50` … `--palette-blue-900`.
    - Grays: `--palette-gray-50` … `--palette-gray-900`.
    - Neutrals: `--palette-white`, `--palette-black`.
  - **Spacing**
    - Size steps tied to rem/px: `--palette-spacing-1`, `-2`, `-4`, `-6`, etc.
    - Encodes consistent spacing scale (e.g., 4px/8px/16px…).
  - **Typography**
    - Font sizes: `--palette-font-size-xs` … `--palette-font-size-2xl`.
    - Font weights: `--palette-font-weight-normal|medium|bold`.

- **Semantic Tokens (Tier 2)**
  - **Colors**
    - Brand: `--color-primary`, `--color-secondary`, `--color-tertiary`.
    - Surfaces: `--color-surface`, `--color-surface-variant`, `--color-background`.
    - Text: `--color-text`, `--color-text-secondary`, `--color-text-disabled`.
    - “On” colors: `--color-on-primary`, `--color-on-secondary`, `--color-on-surface`.
    - States: `--color-error`, `--color-warning`, `--color-success`, `--color-info`.
    - Borders: `--color-border`, `--color-border-focus`.
  - **Spacing**
    - Semantic sizes: `--spacing-xs|sm|md|lg|xl` mapped to palette spacing.
  - **Typography**
    - Roles: `--font-size-body|heading|caption|label`.
    - Weights: `--font-weight-normal|heading|bold`.
  - **Other Common Tokens**
    - Radii: `--radius-sm|md|lg|full`.
    - Shadows: `--shadow-sm|md|lg`.
    - Z-index tiers: `--z-dropdown|modal|tooltip|toast`.

---

## Multi-Theme Implementation

- **Theme Contract**
  - Themes only change **semantic token values**.
  - Component CSS stays the same across themes.
  - Palette tokens remain theme-independent (defined on `:root`).

- **Implementation Pattern**
  - `:root`
    - Defines all **palette tokens** (colors, grays, spacing, etc.).
    - Defines **default (light) theme** semantic tokens.
  - `[data-theme="dark"]`
    - Remaps semantic tokens to appropriate palette shades for dark UI.
    - Adjusts surfaces, text, and borders for contrast on dark backgrounds.
  - `[data-theme="high-contrast"]`
    - Uses explicit high-contrast values (often not palette-based).
    - Focused on maximum accessibility and clarity.

- **Theme Switching Logic (JS)**
  - `setTheme(themeName)`
    - Applies `data-theme` to `<html>` / `document.documentElement`.
    - Stores preference in `localStorage`.
  - `initTheme()`
    - 1) Uses `localStorage` if present.
    - 2) Falls back to `prefers-color-scheme: dark` when applicable.
    - 3) Defaults to `light`.
  - Listens for system dark-mode changes and updates theme when no user override exists.

---

## Component Token Patterns

- **Component-Scoped Override Hooks**
  - Components (e.g., `.c-button`) define internal tokens:
    - Example: `--btn-bg`, `--btn-fg`, `--btn-border`, `--btn-radius`, `--btn-padding-inline`, `--btn-padding-block`.
  - Pattern:
    - Step 1: Component tokens get defaults from **semantic tokens**.
    - Step 2: CSS rules use only **component tokens**, not raw semantic tokens.
  - Variants:
    - Set variant tokens via attributes: `[data-variant="secondary"]`, `[data-variant="ghost"]` override `--btn-bg`, `--btn-fg`, etc.
  - Sizes:
    - `[data-size="sm"]`, `[data-size="lg"]` override spacing-related tokens.

- **Why This Pattern Works**
  - Theming: Changing `--color-primary` updates all components automatically.
  - Flexibility: Consumers can override component-level tokens (e.g., `--btn-bg`) without changing core CSS.
  - Clean variants: Variants and sizes are expressed as token overrides, not duplicated CSS.
  - Maintainable: Centralizes styling logic in tokens instead of scattered declarations.

---

## Package Structure

- **Multi-Framework Design**
  - **tokens/**
    - `css/`: `palette.css`, `semantic.css`, `themes/*.css`, `index.css`.
    - `scss/`: `_palette.scss`, `_semantic.scss`, `index.scss`.
    - `js/`: `palette.js`, `semantic.js`, `index.js`.
    - `json/`: `palette.json`, `semantic.json` (platform-agnostic source of truth).
  - **components/**
    - `css/`: raw CSS components (button, input, card, index).
    - `react/`, `vue/`, `web-components/`: framework-specific wrappers using the same tokens/CSS.
  - **docs/**
    - Documentation site package.

- **Key Idea**
  - Separate **tokens**, **components**, and **framework bindings**.
  - Treat JSON as the canonical token definition, with tooling to generate platform formats.

---

## Design Tool Integration

- **Figma → Style Dictionary → Platforms**
  - Figma (with tokens plugin) is the design source of truth.
  - Tokens exported as a **platform-agnostic JSON** (e.g., `tokens.json`).
  - Style Dictionary ingests JSON and outputs multiple platform representations:
    - CSS custom properties.
    - Sass variables.
    - JS/TS objects.
    - Native platform tokens (iOS, Android).

- **Style Dictionary Configuration**
  - `source`: token JSON files (`tokens/**/*.json`).
  - `platforms`:
    - **css**: build to `dist/css/tokens.css` with `css/variables` format.
    - **scss**: build to `dist/scss/_tokens.scss` with `scss/variables` format.
    - **js**: build to `dist/js/tokens.js` with ES6 export format.

---

## Cross-Framework Distribution

- **Framework-Agnostic Core**
  - Base layer uses **vanilla CSS custom properties**:
    - Works with any framework.
    - No framework-specific build-time dependencies.
    - Supports runtime theming and SSR.

- **Framework-Specific Wrappers**
  - **React**
    - Simple components importing shared CSS: `className="c-button"`, `data-variant`, `data-size`.
  - **Vue**
    - Components bind `data-variant` and `data-size` via props.
    - Reuse shared `Button.css` via `<style src="./Button.css">`.
  - Other frameworks:
    - Apply the same pattern: thin UI wrappers over the shared CSS + tokens.

- **Publishing Strategy**
  - Separate npm packages:
    - `@design-system/tokens` for token distribution.
    - `@design-system/components` for framework-agnostic CSS components.
    - `@design-system/react`, `@design-system/vue`, `@design-system/web-components` for framework bindings.
  - Prefer a **monorepo with workspaces**:
    - Shared tooling, consistent versioning, easier cross-package development.

---

## Related Resources

- Style Dictionary documentation.
- Figma Tokens plugin.
- MDN docs for CSS custom properties.
- W3C Design Tokens Community Group.
