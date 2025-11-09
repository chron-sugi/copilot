---
description: "Comprehensive CSS review checklist against core standards"
mode: 'ask'
tools: ['codebase', 'search', 'problems']
---

# CSS Review Comprehensive Checklist

Run comprehensive standards review for: **${input:component}**

**Files to review**: ${input:files}

---

## Review Scope

This checklist verifies compliance with all standards in [CSS Core Standards](../../instructions/css.instructions.md).

---

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
```

---

**Related**:
- [CSS Core Standards](../../instructions/css.instructions.md) - Verification source
- [CSS Code Reviewer Mode](../../chatmodes/css/css-code-reviewer.chatmode.md)
- [Code Review Template](../../prompts/css-code-review-template.prompt.md)
