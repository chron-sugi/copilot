---
description: "Generate component token pattern with override hooks and semantic token consumption"
mode: 'ask'
tools: ['codebase']
---

# Component Token Pattern Generator

Generate component token implementation for: **${input:componentName:Component}**

---

## Requirements

Create a component CSS implementation using the **component-scoped token pattern** with override hooks.

### Pattern to Follow

```css
/**
 * Component: ${input:componentName}
 * Layer: components
 * Override hooks: [list of custom properties consumers can override]
 * Semantic tokens: [list of semantic tokens consumed]
 */

@layer components {
  .c-${input:componentName} {
    /* ----------------------------------------
       Step 1: Define component-scoped tokens
       ----------------------------------------
       These provide override hooks for consumers
       and establish semantic token consumption
    */
    --[prefix]-bg: var(--color-[semantic]);
    --[prefix]-fg: var(--color-[semantic]);
    --[prefix]-border: var(--color-[semantic]);
    --[prefix]-radius: var(--radius-[size]);
    --[prefix]-padding-inline: var(--spacing-[size]);
    --[prefix]-padding-block: var(--spacing-[size]);

    /* ----------------------------------------
       Step 2: Use component tokens in rules
       ----------------------------------------
       Never use semantic tokens directly here
    */
    background: var(--[prefix]-bg);
    color: var(--[prefix]-fg);
    border: 1px solid var(--[prefix]-border);
    border-radius: var(--[prefix]-radius);
    padding-inline: var(--[prefix]-padding-inline);
    padding-block: var(--[prefix]-padding-block);

    /* Other CSS properties */
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-family: inherit;
    font-size: var(--font-size-body);
    font-weight: var(--font-weight-medium);
    cursor: pointer;
    transition: all 0.2s ease;
  }

  /* ----------------------------------------
     Child elements (BEM style)
     ---------------------------------------- */
  .c-${input:componentName}__icon {
    --icon-size: 1em;
    width: var(--icon-size);
    height: var(--icon-size);
    margin-inline-end: var(--spacing-xs);
  }

  /* ----------------------------------------
     Variants (override component tokens)
     ---------------------------------------- */
  .c-${input:componentName}[data-variant="secondary"] {
    --[prefix]-bg: var(--color-secondary);
    --[prefix]-fg: var(--color-on-secondary);
  }

  .c-${input:componentName}[data-variant="ghost"] {
    --[prefix]-bg: transparent;
    --[prefix]-fg: var(--color-primary);
    --[prefix]-border: var(--color-border);
  }

  /* ----------------------------------------
     Sizes (override spacing tokens)
     ---------------------------------------- */
  .c-${input:componentName}[data-size="sm"] {
    --[prefix]-padding-inline: var(--spacing-sm);
    --[prefix]-padding-block: var(--spacing-xs);
    font-size: var(--font-size-sm);
  }

  .c-${input:componentName}[data-size="lg"] {
    --[prefix]-padding-inline: var(--spacing-lg);
    --[prefix]-padding-block: var(--spacing-md);
    font-size: var(--font-size-lg);
  }

  /* ----------------------------------------
     States
     ---------------------------------------- */
  .c-${input:componentName}:hover {
    opacity: 0.9;
  }

  .c-${input:componentName}:focus-visible {
    outline: 2px solid var(--color-border-focus);
    outline-offset: 2px;
  }

  .c-${input:componentName}[data-state="disabled"],
  .c-${input:componentName}:disabled {
    --[prefix]-bg: var(--color-surface-variant);
    --[prefix]-fg: var(--color-text-disabled);
    cursor: not-allowed;
    opacity: 0.6;
  }

  /* ----------------------------------------
     Motion preferences
     ---------------------------------------- */
  @media (prefers-reduced-motion: reduce) {
    .c-${input:componentName} {
      transition: none;
    }
  }
}
```

---

## Component Details

**Component name:** ${input:componentName}

**Variants needed:**
${input:variants:primary, secondary, ghost, danger}

**Sizes needed:**
${input:sizes:sm, md, lg}

**States needed:**
${input:states:default, hover, focus, disabled, loading}

**Child elements:**
${input:childElements:None}

---

## Token Naming Convention

**Prefix pattern:**
- Short, memorable abbreviation of component name
- Examples:
  - Button → `btn`
  - Input → `input`
  - Card → `card`
  - Modal → `modal`
  - Dropdown → `dropdown`

**Custom property naming:**
```
--[prefix]-[property]
```

Examples:
- `--btn-bg`
- `--input-border`
- `--card-padding`

---

## Best Practices to Apply

1. **Two-layer token system:**
   - Component tokens (--prefix-*) reference semantic tokens (--color-*, --spacing-*)
   - Semantic tokens reference palette tokens (--palette-*)
   - **Never skip layers**: Component → Palette is forbidden

2. **Override hooks:**
   - All component tokens are override hooks
   - Document which ones consumers can safely override
   - Use semantic defaults

3. **Variants via token override:**
   - Don't duplicate CSS properties per variant
   - Only override the component tokens
   - Keeps variant definitions clean and maintainable

4. **Theming:**
   - Component never checks [data-theme]
   - Theming happens by semantic tokens changing values
   - Component is theme-agnostic

5. **Accessibility:**
   - Include :focus-visible styles
   - Support prefers-reduced-motion
   - Ensure minimum contrast ratios
   - Document ARIA requirements in comments

---

## Output Requirements

Generate:

1. **Complete component CSS** with:
   - Component-scoped tokens
   - All requested variants
   - All requested sizes
   - All requested states
   - Child elements (if any)
   - Accessibility features

2. **Documentation comment** listing:
   - Override hooks (custom properties)
   - Semantic tokens consumed
   - Accessibility notes
   - Example HTML usage

3. **Theming notes:**
   - Which semantic tokens affect this component
   - How themes will change component appearance

4. **Usage example:**
   - HTML structure
   - Common variant/size combinations

---

**Related:**
- [Design System Architecture](../../docs/design-system-architecture.md)
- [CSS Core Standards](../../instructions/css.instructions.md)
- [CSS Component API Template](../../prompts/css-component-api-template.prompt.md)
