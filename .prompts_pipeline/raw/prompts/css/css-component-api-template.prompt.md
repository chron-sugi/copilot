---
description: "Generate CSS component API documentation header"
mode: 'ask'
tools: ['codebase']
---

# CSS Component API Documentation Generator

Generate a comprehensive CSS component API documentation header for the component: **${input:componentName}**

---

## Requirements

Create a CSS documentation block comment following this structure:

```css
/**
 * Component: ${input:componentName}
 * Layer: ${input:layer:components}
 * Version: ${input:version:1.0.0}
 *
 * Description:
 *   [Brief description of what this component does and when to use it]
 *
 * Exports:
 *   - .c-[component-name] (base class, required)
 *   - .c-[component-name]__[child] (optional child elements)
 *   - .c-[component-name]--[modifier] (optional modifiers)
 *
 * API - data attributes:
 *   data-variant: [list all variant values]
 *   data-size: [list all size values]
 *   data-state: [list all state values]
 *
 * API - custom properties (override hooks):
 *   --[prefix]-bg: Background color
 *   --[prefix]-fg: Text/icon color
 *   --[prefix]-border: Border color
 *   --[prefix]-radius: Border radius
 *   --[prefix]-padding-inline: Horizontal padding
 *   --[prefix]-padding-block: Vertical padding
 *   [Add component-specific properties]
 *
 * Tokens consumed:
 *   [List all design tokens used: --color-*, --spacing-*, --radius-*, etc.]
 *
 * Accessibility:
 *   - Focus: [How focus is handled]
 *   - Contrast: [Contrast ratios for all variants]
 *   - Motion: [Motion preferences handling]
 *   - Touch: [Minimum touch target size]
 *   [Add component-specific a11y notes]
 *
 * Theming:
 *   [data-theme] swaps tokens only, not component rules
 *   Supports: light, dark, high-contrast
 *   [Add theming notes specific to this component]
 *
 * Browser support:
 *   Chrome 120+, Firefox 120+, Safari 17+, Edge 120+
 *   [Note any progressive enhancement strategies]
 *
 * Examples:
 *   [Provide 2-3 HTML usage examples showing common variants]
 */

@layer ${input:layer:components} {
  .c-${input:componentName} {
    /* Implementation here */
  }
}
```

---

## Template Guidelines

**Description Section**:
- Keep it concise (1-2 sentences)
- Explain WHAT it does and WHEN to use it
- Example: "Primary interactive control for triggering actions. Use for form submissions, actions, and navigation."

**Exports Section**:
- List all CSS classes exported by this component
- Indicate if classes are required or optional
- Follow BEM naming: base, __child, --modifier

**API - data attributes**:
- Document all supported `data-*` attributes
- List all possible values for each attribute
- Example: `data-variant: primary | secondary | ghost | danger`

**API - custom properties**:
- Document all CSS custom properties that consumers can override
- Explain what each property controls
- Use consistent naming: `--[component-prefix]-[property]`

**Tokens consumed**:
- List all design tokens referenced in the component
- Helps track token dependencies
- Example: `--color-primary`, `--spacing-md`, `--radius-sm`

**Accessibility**:
- Document WCAG compliance level (AA minimum)
- Specify focus handling (`:focus-visible` preferred)
- Note color contrast ratios (4.5:1 text, 3:1 UI)
- Document motion handling (`prefers-reduced-motion`)
- Specify minimum touch target size (44×44px)

**Theming**:
- Explain how theming works (token swaps only)
- List supported theme modes
- Note any theme-specific considerations

**Browser support**:
- Specify minimum browser versions
- Document any progressive enhancement
- Note fallbacks for modern features

**Examples**:
- Provide 2-3 realistic usage examples
- Show different variants/sizes
- Include proper HTML structure

---

## Output Format

Return ONLY the formatted CSS documentation block comment, ready to paste at the top of the component's CSS file.

Ensure:
- ✅ All sections are filled with realistic, specific information
- ✅ Custom property naming is consistent with component name
- ✅ Data attribute values are comprehensive
- ✅ Examples show proper HTML structure
- ✅ Accessibility notes are specific and actionable
- ✅ Token dependencies are clearly listed

---

**Related:** [CSS Developer Mode](../.github/chatmodes/css/css-developer.chatmode.md)
