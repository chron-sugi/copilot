---
applyTo: "**/*.css,**/*.scss,**/*.sass"
description: "Core CSS architecture standards - specificity, tokens, naming, layers, accessibility"
---

# CSS Shared Standards

> **Version:** 1.0 (2025-01-08)
> **Purpose:** Core principles and standards applied automatically to all CSS work

---

## System Values

**Specificity Management**
* Keep specificity **as low as possible**; prefer single-class selectors (0,1,0)
* Modern technique: Use `:where()` pseudo-class for zero specificity (0,0,0) when needed
* No ID selectors in components (1,0,0 specificity is too high)
* Avoid deep descendant chains (each level adds specificity)
* Avoid `!important` except for legitimate cases (see below)

**When !important IS Appropriate**
* **Utility classes** that must always apply (e.g., `.u-hidden { display: none !important; }`)
* **Overriding inline styles** from JavaScript libraries you don't control
* **Third-party CSS** you cannot modify (though `@layer` is now preferred)
* **Note:** In `@layer`, `!important` works in REVERSE — earlier layers win over later layers

**Design Tokens with CSS Custom Properties**
* Single source of truth for: color, spacing, typography, radii, shadows, z-index, motion
* Use **semantic tokens** in components (e.g., `--color-button-primary-bg`)
* Reference **palette tokens** only from semantic token definitions (e.g., `--color-blue-600`)
* Modern approach: `@property` rule for type-safe tokens with animation support (fully supported 2024)

```css
/* Type-safe token with @property */
@property --spacing-unit {
  syntax: '<length>';
  inherits: true;
  initial-value: 0.25rem;
}
```

**Naming Conventions**
* `c-*` — Component blocks (BEM style: `.c-button`, `.c-button__icon`, `.c-button--large`)
* `o-*` — Layout objects (e.g., `.o-grid`, `.o-stack`, `.o-cluster`)
* `u-*` — Utility classes (e.g., `.u-text-center`, `.u-sr-only`)
* `is-*` / `has-*` — State classes (e.g., `.is-active`, `.has-error`)

**Variants via data-* Attributes**
* Use `data-variant`, `data-size`, `data-state` instead of class proliferation
* Keeps base class stable; enables type safety in JavaScript
* Example: `<button class="c-button" data-variant="primary" data-size="lg">`
* Supported natively in Tailwind CSS v3.2+ and modern frameworks

**CSS Cascade Layers (@layer)**
* Declare layer order upfront: `@layer reset, base, tokens, utilities, objects, components, overrides;`
* Later layers override earlier layers **regardless of specificity**
* Unlayered styles override ALL layered styles
* `!important` in layers works in **REVERSE** (earlier layers win)
* Modern solution: Replaces specificity hacks and eliminates many `!important` needs

```css
/* Declare layer order first */
@layer reset, base, tokens, utilities, objects, components, overrides;

@layer components {
  .c-button { background: var(--btn-bg); }
}

@layer overrides {
  .c-button { background: red; } /* This wins despite same specificity */
}
```

**Layering Contract (Conceptual Order)**
1. **Reset/Normalize** — Zero out browser defaults
2. **Base** — Element-level defaults (no classes)
3. **Tokens** — Design token definitions
4. **Utilities** — Single-purpose classes
5. **Objects** — Layout primitives
6. **Components** — UI components (c-*)
7. **Overrides** — Context-specific overrides only

**Accessibility First**
* **Focus states:** Always visible (`:focus-visible` preferred over `:focus`)
* **Motion preferences:** Honor `prefers-reduced-motion: reduce` (WCAG 2.3.3)
  * **Note:** May not fully satisfy WCAG 2.2.2 (Pause/Stop/Hide) alone
  * Best practice: Two-pronged approach (OS preference + custom toggle for complex animations)
* **High contrast:** Test with `forced-colors: active` and `prefers-contrast: high`
* **Color contrast:** Minimum 4.5:1 for text, 3:1 for UI components (WCAG AA)

**Modern Responsiveness**
* **Container queries** for component-level responsiveness (93% browser support, Nov 2024)
* **Media queries** for global layout, viewport changes, and user preferences
* **Use BOTH together:** `@media` for page layout, `@container` for components
* **Logical properties** for internationalization (e.g., `margin-inline-start` vs `margin-left`)
* **Fluid sizing** with `clamp()` for responsive typography and spacing

```css
/* Component responds to its container, not viewport */
.c-card {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .c-card__content { display: grid; }
}

/* Media query for global layout */
@media (min-width: 768px) {
  .o-grid { grid-template-columns: repeat(2, 1fr); }
}
```

**Modern Specificity Tools**
* `:where()` — Zero specificity (0,0,0) for reset/base styles
* `:is()` — Takes specificity of most specific selector in list
* Use `:where()` when you want styles easily overridden

```css
/* Zero specificity — easily overridden */
:where(.c-button) {
  padding: var(--btn-padding);
}

/* Normal specificity (0,1,0) */
.c-button--primary {
  background: var(--color-primary);
}
```

**Testability**
* **Visual regression:** Chromatic, Percy, or Storybook Test Runner + jest-image-snapshot
* **Accessibility:** axe-core, WAVE, Lighthouse CI
* **Lint rules:** Stylelint with shareable configs
* **Component stories:** Enumerate states × variants × sizes × themes
* **Performance:** Bundle size budgets, unused CSS detection (PurgeCSS, UnCSS)

**Repo Structure (Conceptual)**
```
styles/
├── 00-reset/
├── 01-base/
├── 02-tokens/
├── 03-utilities/
├── 04-objects/
├── 05-components/
└── 06-overrides/
```

**Performance Budgets**
* **CSS file size:** < 50KB (gzipped) for initial load
* **Critical CSS:** < 14KB (gzipped) inlined in `<head>`
* **Lighthouse Performance:** ≥ 90
* **Time to First Contentful Paint:** < 1.8s
* **Expensive properties:** Minimize `box-shadow`, `filter`, `backdrop-filter` (use GPU-accelerated `transform` and `opacity` for animations)

**Component API Documentation (Schema Example)**

```yaml
component: Button
layer: components
exports: [".c-button", ".c-button__icon"]
api:
  data-variant: [primary, secondary, ghost, danger]
  data-size: [sm, md, lg]
  data-state: [loading, disabled]
tokens:
  - --btn-bg
  - --btn-fg
  - --btn-border
  - --btn-radius
  - --btn-padding-inline
  - --btn-padding-block
a11y:
  focus: "visible ring via :focus-visible"
  motion: "respects prefers-reduced-motion"
  contrast: "4.5:1 minimum for all variants"
theming: "[data-theme] overrides tokens only, not component rules"
browser-support: ["Chrome 120+", "Firefox 120+", "Safari 17+", "Edge 120+"]
```

---

## References

* [BEM Methodology](https://getbem.com/)
* [ITCSS](https://www.xfive.co/blog/itcss-scalable-maintainable-css-architecture/)
* [CUBE CSS](https://cube.fyi/)
* [CSS Cascade Layers (@layer)](https://developer.mozilla.org/en-US/docs/Web/CSS/@layer)
* [@property CSS Rule](https://developer.mozilla.org/en-US/docs/Web/CSS/@property)
* [CSS Containment (Container Queries)](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment)
* [WCAG 2.2 Guidelines](https://www.w3.org/WAI/WCAG22/quickref/)
* [Logical Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values)
