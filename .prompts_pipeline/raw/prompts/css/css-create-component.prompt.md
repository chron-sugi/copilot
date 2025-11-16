---
description: "Create new CSS component with documented API, tokens, and comprehensive tests"
mode: agent
model: claude-sonnet-4-5
tools: ["codebase", "editor", "search"]
---

# Create CSS Component

Create a production-ready CSS component following modern architecture standards.

## Component Specification

**Component name:** ${input:componentName:Component name (e.g., Button, Card, Modal)}

**Description:** ${input:description:What does this component do?}

**Variants:** ${input:variants:List variants (e.g., primary, secondary, ghost)}

**Sizes:** ${input:sizes:List sizes (e.g., sm, md, lg)}

**States:** ${input:states:List states (e.g., loading, disabled, error)}

**Requirements:** ${input:requirements:Special requirements or features}

---

## Implementation Checklist

### 1. Public API Design (Before Writing CSS)

Define:
- [ ] Base class: `.c-${componentName}`
- [ ] Child elements (BEM): `.c-${componentName}__element`
- [ ] `data-*` attributes for variants/sizes/states
- [ ] Component-scoped custom properties (override hooks)
- [ ] Supported state classes (`is-*`, `has-*`)

### 2. Token Usage

Consume semantic tokens for:
- [ ] Colors: `--color-{purpose}` (not palette tokens)
- [ ] Spacing: `--spacing-{size}`
- [ ] Typography: `--font-size-{size}`, `--font-weight-{weight}`
- [ ] Radii: `--radius-{size}`
- [ ] Shadows: `--shadow-{size}`

Define component override hooks:
- [ ] `--${componentName}-bg`: Background color
- [ ] `--${componentName}-fg`: Foreground/text color
- [ ] `--${componentName}-border`: Border color
- [ ] Additional as needed

### 3. Component Structure

```css
/**
 * Component: ${componentName}
 * Layer: components
 * Version: 1.0.0
 *
 * Description: [Brief description]
 *
 * Exports:
 *   - .c-${componentName} (base class, required)
 *   [List child elements]
 *
 * API - data attributes:
 *   data-variant: [list variants]
 *   data-size: [list sizes]
 *   data-state: [list states]
 *
 * API - custom properties:
 *   [List override hooks with descriptions]
 *
 * Tokens consumed:
 *   [List semantic tokens used]
 *
 * Accessibility:
 *   - Focus: Visible ring via :focus-visible
 *   - Contrast: WCAG AA compliance
 *   - Motion: Respects prefers-reduced-motion
 *
 * Browser support:
 *   Chrome 120+, Firefox 120+, Safari 17+, Edge 120+
 */

@layer components {
  .c-${componentName} {
    /* Component token definitions */
    --${componentName}-bg: var(--color-surface);
    --${componentName}-fg: var(--color-text);

    /* Implementation */
    background: var(--${componentName}-bg);
    color: var(--${componentName}-fg);

    /* Ensure accessibility */
    &:focus-visible {
      outline: 2px solid var(--color-focus);
      outline-offset: 2px;
    }
  }

  /* Variants */
  .c-${componentName}[data-variant="..."] {
    /* Override component tokens */
  }

  /* Sizes */
  .c-${componentName}[data-size="..."] {
    /* Size adjustments */
  }

  /* States */
  .c-${componentName}[data-state="..."] {
    /* State styles */
  }
}
```

### 4. Responsiveness

- [ ] Use container queries for component-level responsiveness
- [ ] Use media queries only for global layout
- [ ] Use logical properties for i18n (RTL support)
- [ ] Fluid sizing with `clamp()` where appropriate
- [ ] Touch targets ≥ 44×44px

### 5. Accessibility

- [ ] Focus styles with `:focus-visible`
- [ ] Color contrast ≥ 4.5:1 (text), ≥ 3:1 (UI)
- [ ] `prefers-reduced-motion` support
- [ ] `forced-colors` mode support
- [ ] Semantic HTML guidance

### 6. Testing Requirements

Create Storybook stories for:
- [ ] **States:** default, hover, focus, active, disabled, loading, error
- [ ] **Variants:** All `data-variant` values
- [ ] **Sizes:** All `data-size` values
- [ ] **Themes:** Light, dark, high-contrast
- [ ] **Edge cases:** Long text, empty state, overflow

Add tests:
- [ ] Visual regression (Chromatic/Percy)
- [ ] Accessibility (axe-core)
- [ ] Keyboard navigation

---

## File Locations

Create files at:
- CSS: `${workspaceFolder}/src/components/${componentName}/${componentName}.css`
- Stories: `${workspaceFolder}/src/components/${componentName}/${componentName}.stories.js`
- Tests: `${workspaceFolder}/src/components/${componentName}/${componentName}.test.js`

---

## Success Criteria

Component is complete when:
- ✅ Public API documented in CSS header
- ✅ All variants/sizes/states implemented
- ✅ Uses semantic tokens only (no literals)
- ✅ Placed in `@layer components`
- ✅ Accessibility requirements met
- ✅ Storybook stories cover all combinations
- ✅ Tests pass (visual regression, a11y)
- ✅ Cross-browser tested

---

Refer to:
- [CSS Core Standards](../.github/instructions/css.instructions.md) for standards
- [CSS Developer Mode](../.github/chatmodes/css-developer.chatmode.md) for implementation guidance
