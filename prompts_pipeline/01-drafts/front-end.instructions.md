# FROM GPT 

Use BEM

CSS Authoring Rules for Code Agents

<priority_legend>

P0=MUST follow; breaking this invalidates the request.
P1=SHOULD follow; deviations need an explicit rationale.
P2=CAN follow; use when helpful but optional.

</priority_legend>

<rules>
CRITICAL

R1 [P0] Enforce priorities (copilot instruction): refuse to ship CSS that violates P0; if external constraints force it, stop and return a clear rationale. For P1 deviations, add a /* rationale: … */ comment.

R2 [P0] Use CSS variables for all design tokens (color, spacing, radius, z-index, typography). Define in :root and theme scopes; don’t hardcode literals inside components. Example: color: var(--text, #222);

R3 [P0] Set global sizing model: html { box-sizing: border-box } * , *::before, *::after { box-sizing: inherit }.

R4 [P0] Normalize once: include a single modern reset/normalize in a reset layer; never duplicate resets per component.

R5 [P0] Keep specificity low: prefer class selectors; avoid IDs and selector chains > 2 levels; use :where() to zero specificity when scoping helpers.

R6 [P0] Manage cascade with layers: declare order and place rules inside them:
@layer reset, tokens, base, utilities, components, overrides;

R7 [P0] Accessibility: meet WCAG contrast (text ≥ 4.5:1; large text/UI ≥ 3:1); never remove focus styles—style :focus-visible instead.

R8 [P0] Respect motion preferences: gate non-essential animation behind @media (prefers-reduced-motion: reduce); keep essential transitions brief.

R9 [P0] Responsive by default: prefer Grid/Flex; avoid fixed widths; use clamp()/min()/max() for fluid type/spacing.

R10 [P0] Internationalization: use logical properties (margin-inline, padding-block, inset-inline) instead of left/right where possible.

R11 [P0] Prevent layout shift: reserve space for media via width/height or aspect-ratio; use object-fit appropriately.

R12 [P0] Component isolation: scope styles to components (BEM/SUIT or equivalent); avoid global descendant rules like .card p {…} outside component scope.

R13 [P0] Avoid !important: only allowed in documented utilities or last-resort overrides with rationale.

R14 [P0] Progressive enhancement: wrap modern features (:has, container queries, subgrid) in @supports and provide reasonable fallbacks.

R15 [P0] Robust font loading: always include fallback stacks and font-display: swap; declare only axes you use for variable fonts.

R16 [P0] Unit conventions: use rem for global scales, em for component-relative sizing, and px for borders/hairlines; don’t mix units arbitrarily.

R17 [P0] Z-index discipline: define a small tokenized scale (e.g., --z-modal, --z-popover); create stacking contexts intentionally (isolation: isolate when needed).

R18 [P0] Theming via tokens: implement dark/high-contrast themes by swapping token values (e.g., [data-theme="dark"] { --bg: … })—don’t duplicate component CSS.

R19 [P0] Respect user control: never disable zoom; constrain readable text width (≈ 45–85ch) using max-width.

Domain Section — Architecture & Naming

R20 [P1] Pick one naming scheme (BEM, SUIT, utility-first) and apply it consistently across the codebase.

R21 [P1] Namespace app classes (e.g., .app- or .c-) to avoid collisions with third-party styles.

R22 [P2] Co-locate a component’s CSS with its implementation; expose one entry file per component.

R23 [P1] Use a consistent property order (e.g., box model → typography → visuals → interactions) or strict alphabetical—be consistent.

R24 [P2] Prefer multiple focused files that the bundler concatenates; avoid circular imports and redundant re-exports.

Domain Section — Tokens & Theming

R25 [P1] Define a complete token set: --color-*, --space-*, --size-*, --radius-*, --shadow-*, --z-*, --font-*.

R26 [P1] Map semantic tokens to raw tokens (e.g., --btn-bg: var(--color-primary-600)), and reference semantic tokens in components.

R27 [P2] Provide constrained utility classes generated from tokens (e.g., .p-4, .gap-2), limited to your approved scale.

Domain Section — Layout

R28 [P1] Use Grid for page/2D layout and Flex for 1D alignment; avoid floats/table layouts except for legacy content.

R29 [P1] Prefer container queries over viewport breakpoints when component width dictates behavior.

R30 [P2] Offer layout primitives (e.g., .stack, .cluster, .sidebar) to reduce bespoke CSS.

R31 [P1] Avoid magic numbers; derive sizes from tokens; leverage fr, auto-fit/auto-fill, and minmax() patterns.

Domain Section — Typography

R32 [P1] Build a typographic scale with clamp(); use unitless line-height and consistent rhythm.

R33 [P1] Limit to ≤ 3 font families and ≤ 4 weights where feasible; prefer variable fonts to reduce requests.

R34 [P2] Use ch for measure-sensitive widths and hyphens: auto for long words in body copy.

Domain Section — States & Interactions

R35 [P1] Style :hover, :focus-visible, :active, :disabled, and ARIA states ([aria-pressed="true"], etc.); ensure touch-friendly targets.

R36 [P1] Hide visually without removing from accessibility tree using a .visually-hidden utility (clip/clip-path approach).

R37 [P2] Use :has() for parent-state styling gated by @supports (selector(:has(*))).

Domain Section — Performance

R38 [P1] Minimize unused CSS (purge/tree-shake safely); avoid costly selectors (*, deep :not() chains).

R39 [P1] Animate only transform and opacity; apply will-change sparingly and clean it up.

R40 [P2] Inline critical CSS for initial paint; code-split route-specific CSS for SPAs/MPAs.

Domain Section — Compatibility & Testing

R41 [P1] Use Autoprefixer with a documented browserslist; verify features via @supports/Can I Use; provide fallbacks.

R42 [P1] Lint with Stylelint and run visual regression tests; block merges on P0 violations.

R43 [P2] Provide print styles (@page margins; hide navigation/chrome).

Domain Section — Documentation & Delivery

R44 [P1] Start each file with a header comment noting its layer, role, and ownership; link to token source.

R45 [P1] When deviating from P1/P0, annotate with /* rationale: … (owner, date) */.

R46 [P2] Generate a style inventory page (colors, type scale, spacing) for QA and design review.

Domain Section — CSS-in-JS / Frameworks

R47 [P1] Even with CSS-in-JS or utility frameworks, enforce tokens and accessibility; don’t hardcode ad‑hoc values.

R48 [P2] In CSS Modules, export intent-revealing class names (component role), not purely presentational names.

</rules>


# FROM Claude

## Standards Verification Checklist

### 1. Specificity & Selector Complexity

Check each selector against these criteria:

- [ ] **Specificity ≤ (0,1,0)** for component styles
  - Count ID selectors (avoid in components)
  - Count class/attribute selectors
  - Check for unnecessary element selectors

- [ ] **No deep descendant chains** (max 2-3 levels)
  - Example violation: `.sidebar .widget .item .link` (4 levels)
  - Should use BEM: `.sidebar__link`

- [ ] **No ID selectors** in component CSS
  - IDs have specificity (1,0,0) - too high
  - Use classes or data-attributes

- [ ] **`:where()` used appropriately** for zero-specificity resets
  - Resets should use `:where()` to be easily overridden

- [ ] **Minimal nesting**
  - BEM should eliminate most nesting needs
  - Deep nesting indicates poor selector strategy

**Findings**:
[Report any specificity violations with file:line and suggested fix]

---

### 2. Design Tokens & Values

Verify token usage:

- [ ] **Semantic tokens used** in components
  - NOT palette tokens: `var(--palette-blue-600)` ❌
  - YES semantic tokens: `var(--color-primary)` ✅

- [ ] **No magic literals**
  - Colors: No hex/rgb values
  - Spacing: No pixel/rem values
  - Typography: No font-size literals
  - Radii: No border-radius literals

- [ ] **Rationale documented** if literals required
  - Comment explaining why token can't be used

- [ ] **`@property` rules** for animated custom properties
  - Type-safe tokens with syntax definition

**Findings**:
[Report magic literals with: file:line, literal value, which token to use]

---

### 3. Variants & Component API

Check variant implementation:

- [ ] **`data-*` attributes** for variants
  - `data-variant="primary"` ✅
  - NOT class explosion: `.button-primary-large` ❌

- [ ] **State classes** use `is-*` or `has-*` prefix
  - `.is-active`, `.has-error` ✅
  - NOT generic names: `.active` ❌

- [ ] **Base class remains stable**
  - Single base class: `.c-button`
  - Variants don't change base class

- [ ] **Component API documented**
  - YAML schema or comment header
  - Lists all data-* attributes, custom properties

**Findings**:
[Report variant implementation issues]

---

### 4. Cascade Layers (@layer)

Verify layer usage:

- [ ] **Correct @layer placement**
  - Components in `@layer components`
  - Utilities in `@layer utilities`
  - Overrides in `@layer overrides` (rare)

- [ ] **Layer order respected**
  - Declared: `@layer reset, base, tokens, utilities, objects, components, overrides`
  - Later layers override earlier (regardless of specificity)

- [ ] **No unlayered styles** in components
  - Unlayered styles beat ALL layered styles
  - Can cause unexpected overrides

- [ ] **`!important` usage justified**
  - Utilities only (for .u-hidden, .u-sr-only)
  - Documented exceptions
  - NOTE: In @layer, !important works in REVERSE

**Findings**:
[Report layer issues]

---

### 5. Accessibility (WCAG 2.2 AA)

Critical accessibility checks:

- [ ] **Focus styles visible**
  - `:focus-visible` on all interactive elements
  - Focus indicator contrast ≥ 3:1
  - Visible on all themes

- [ ] **Color contrast** meets standards
  - Normal text: ≥ 4.5:1
  - Large text (18pt+/14pt bold+): ≥ 3:0
  - UI components: ≥ 3:1
  - Verify in all themes (light, dark, high-contrast)

- [ ] **`prefers-reduced-motion: reduce`** honored
  - Animations disabled or simplified
  - Transitions duration reduced

- [ ] **Complex animations** have controls (WCAG 2.2.2)
  - Pause/stop/hide controls
  - OR respect prefers-reduced-motion

- [ ] **High-contrast modes** supported
  - `forced-colors: active` tested
  - `prefers-contrast: high` tested

- [ ] **Semantic HTML** used
  - Not relying on CSS alone for meaning
  - Proper heading hierarchy, landmarks

- [ ] **Touch targets ≥ 44×44px** (WCAG 2.5.5)
  - All interactive elements
  - Includes padding/clickable area

**Findings**:
[Report accessibility violations - these are HIGH PRIORITY]

---

### 6. Responsiveness

Check responsive implementation:

- [ ] **Container queries** for component-level responsiveness
  - Parent has `container-type: inline-size`
  - `@container` queries used for component breakpoints

- [ ] **Media queries** for global layout only
  - Viewport-based breakpoints
  - User preference queries (`prefers-color-scheme`, etc.)

- [ ] **Logical properties** for i18n
  - `margin-inline-start` NOT `margin-left`
  - `padding-block` NOT `padding-top/bottom`
  - RTL support built-in

- [ ] **Fluid sizing** with `clamp()`
  - Responsive typography
  - Responsive spacing
  - Example: `font-size: clamp(1rem, 2vw, 1.5rem)`

**Findings**:
[Report responsiveness issues]

---

### 7. Performance

Performance impact assessment:

- [ ] **No unused selectors** or dead code
  - Verify with CSS coverage tools
  - Remove commented-out code

- [ ] **Reasonable selector complexity**
  - Avoid overly specific selectors
  - Avoid slow selectors (complex :nth-child)

- [ ] **Minimal expensive properties**
  - `box-shadow`: Use sparingly, especially on hover
  - `filter`: GPU-accelerated but expensive
  - `backdrop-filter`: Very expensive

- [ ] **GPU-accelerated animations**
  - Use `transform` and `opacity` ✅
  - AVOID animating `width`, `height`, `top`, `left` ❌

- [ ] **Bundle size within budget**
  - < 50KB gzipped per component library
  - Report size delta for this PR

**Findings**:
[Report performance concerns with impact assessment]

---

### 8. Cross-Browser Compatibility

Browser support verification:

- [ ] **Target browser testing**
  - Chrome (latest - 1)
  - Firefox (latest - 1)
  - Safari (latest - 1)
  - Edge (latest - 1)

- [ ] **Modern feature fallbacks**
  - Container queries (support 93%)
  - @layer (support 95%)
  - @property (support 85%)
  - CSS nesting (may need transpilation)

- [ ] **Progressive enhancement documented**
  - Graceful degradation strategy
  - Core functionality works in older browsers

- [ ] **Autoprefixer used**
  - No hand-written vendor prefixes
  - PostCSS pipeline configured

**Findings**:
[Report browser compatibility issues]

---

### 9. Testing & Documentation

Verify test coverage and documentation:

- [ ] **Visual regression tests updated**
  - Chromatic/Percy/Storybook snapshots
  - All variants captured
  - All themes tested

- [ ] **Accessibility tests passing**
  - axe-core automated tests
  - Lighthouse accessibility score
  - Manual keyboard navigation tested

- [ ] **Storybook stories complete**
  - States: default, hover, focus, active, disabled
  - Variants: All data-variant values
  - Sizes: All data-size values
  - Themes: light, dark, high-contrast
  - Edge cases: loading, error, empty states

- [ ] **Component API documented**
  - Comment header or YAML schema
  - All data-* attributes listed
  - All custom property override hooks listed
  - Usage examples provided

- [ ] **Migration guide** (if breaking changes)
  - What changed
  - How to migrate
  - Deprecation timeline

**Findings**:
[Report testing/documentation gaps]

---

## Standards Violations Summary

Categorize findings by severity:

### Critical (🔴 Blocker)
[Issues that MUST be fixed before merge]
- Accessibility violations (WCAG failures)
- Security concerns
- Breaking changes without migration

### High (🟠 Required)
[Issues that should be fixed before merge]
- Magic literals instead of tokens
- Missing focus states
- Performance regressions

### Medium (🟡 Recommended)
[Issues that should be addressed but not blocking]
- Minor accessibility improvements
- Documentation gaps
- Missing edge case tests

### Low (🟢 Nice to have)
[Optional improvements]
- Code organization suggestions
- Future enhancements
- Refactoring opportunities

---

## Review Output Format

Generate findings report:

```markdown
# Comprehensive Review: ${input:component}

## Summary
- **Total files reviewed**: X
- **Standards violations**: X critical, X high, X medium, X low
- **Recommendation**: [APPROVE / REQUEST CHANGES / BLOCK]

## Critical Issues (🔴)
[List with file:line, description, suggested fix]

## High Priority Issues (🟠)
[List with file:line, description, suggested fix]

## Medium Priority Issues (🟡)
[List with file:line, description]

## Low Priority Suggestions (🟢)
[List]

## Merge Decision
[APPROVE / REQUEST CHANGES / BLOCK]

**Rationale**: [Explain decision based on findings]

**Required actions** (if REQUEST CHANGES or BLOCK):
1. [Action 1]
2. [Action 2]