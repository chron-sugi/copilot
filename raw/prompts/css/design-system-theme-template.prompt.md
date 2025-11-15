---
description: "Generate multi-theme CSS implementation with palette and semantic tokens"
mode: 'ask'
tools: ['codebase']
---

# Design System Theme Template Generator

Generate a complete multi-theme CSS implementation for: **${input:themeName:New Theme}**

---

## Requirements

Create a comprehensive theme implementation following the two-tier token architecture:

### Structure to Generate

```css
/* ============================================
   THEME: ${input:themeName}
   Description: ${input:description:Theme description}
   ============================================ */

[data-theme="${input:themeName}"] {
  /* ----------------
     Brand Colors
     ---------------- */
  --color-primary: [value];
  --color-secondary: [value];
  --color-tertiary: [value];
  --color-on-primary: [value];
  --color-on-secondary: [value];
  --color-on-tertiary: [value];

  /* ----------------
     Surfaces
     ---------------- */
  --color-surface: [value];
  --color-surface-variant: [value];
  --color-background: [value];

  /* ----------------
     Text
     ---------------- */
  --color-text: [value];
  --color-text-secondary: [value];
  --color-text-disabled: [value];

  /* ----------------
     State Colors
     ---------------- */
  --color-error: [value];
  --color-warning: [value];
  --color-success: [value];
  --color-info: [value];

  /* ----------------
     Borders
     ---------------- */
  --color-border: [value];
  --color-border-focus: [value];

  /* ----------------
     Spacing (if theme-specific)
     ---------------- */
  /* Usually spacing is theme-independent, but include if needed */
}
```

---

## Theme Characteristics to Consider

**Light Theme:**
- Bright backgrounds (#ffffff, #f9fafb)
- Dark text (#111827, #1f2937)
- Saturated primary colors (blue-600, green-600)

**Dark Theme:**
- Dark backgrounds (#111827, #1f2937)
- Light text (#f9fafb, #e5e7eb)
- Lighter primary colors for contrast (blue-400, green-400)

**High-Contrast Theme:**
- Pure black/white (#000000, #ffffff)
- No grays (or very limited)
- High saturation colors
- Thicker borders

**Brand Theme (e.g., "Corporate"):**
- Company-specific brand colors
- Custom palette references
- Unique accent colors

---

## Guidelines

1. **Reference existing palette tokens** when possible:
   - Use `var(--palette-blue-600)` format
   - Only use literal values for high-contrast or brand-specific colors

2. **Ensure WCAG AA compliance**:
   - Text contrast ≥ 4.5:1 (normal text)
   - UI component contrast ≥ 3:1 (buttons, inputs)

3. **Maintain semantic naming**:
   - Don't rename semantic tokens per theme
   - Only swap the VALUES they reference

4. **Test with components**:
   - Verify theme works with existing components
   - Check all states (hover, focus, disabled)

5. **Document theme purpose**:
   - Add comment describing when to use this theme
   - Note any special considerations (accessibility, branding)

---

## Additional Context

**If migrating from existing design:**
- Provide current color values: ${input:currentColors:None}
- Brand guidelines: ${input:brandGuidelines:None}
- Accessibility requirements: ${input:a11yRequirements:WCAG AA}

**If creating from scratch:**
- Desired color mood: ${input:colorMood:Professional, warm, energetic, etc.}
- Target audience: ${input:targetAudience:General, enterprise, creative, etc.}

---

## Output Format

Return:
1. **Complete CSS code** ready to paste into theme file
2. **Color contrast report** (estimated WCAG compliance)
3. **Usage instructions** (how to apply this theme)
4. **Palette token references** (which palette tokens were used)

---

**Related:**
- [Design System Architecture](../../docs/design-system-architecture.md)
- [CSS Core Standards](../../instructions/css.instructions.md)
