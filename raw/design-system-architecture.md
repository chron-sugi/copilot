# Design System Architecture Reference

> **Purpose:** Comprehensive reference for design token architecture, theming systems, and cross-framework distribution
> **Last Updated:** 2025-01-08

---

## Table of Contents

1. [Two-Tier Token System](#two-tier-token-system)
2. [Token Naming Conventions](#token-naming-conventions)
3. [Multi-Theme Implementation](#multi-theme-implementation)
4. [Component Token Patterns](#component-token-patterns)
5. [Package Structure](#package-structure)
6. [Design Tool Integration](#design-tool-integration)
7. [Cross-Framework Distribution](#cross-framework-distribution)

---

## Two-Tier Token System

### Architecture Overview

**Tier 1: Palette Tokens (Raw Values)**
- Define the raw color/spacing/typography values
- Naming pattern: `--palette-{category}-{variant}-{shade}`
- **Rule**: Referenced ONLY by semantic tokens, never directly in components
- Purpose: Single source of truth for raw design values

**Tier 2: Semantic Tokens (Contextual Meaning)**
- Map palette tokens to use cases and contexts
- Naming pattern: `--{category}-{purpose}-{variant?}-{state?}`
- **Rule**: Used directly in components
- Purpose: Provide meaning and enable theming

### Why Two Tiers?

1. **Separation of concerns**: Raw values (palette) vs. meaning (semantic)
2. **Theming flexibility**: Swap semantic → palette mappings per theme
3. **Maintenance**: Change palette value once, affects all semantic references
4. **Documentation**: Semantic names are self-documenting

---

## Token Naming Conventions

### Palette Tokens (Tier 1)

**Colors:**
```css
--palette-blue-50     /* Lightest */
--palette-blue-100
--palette-blue-200
--palette-blue-300
--palette-blue-400
--palette-blue-500
--palette-blue-600    /* Base */
--palette-blue-700
--palette-blue-800
--palette-blue-900    /* Darkest */

--palette-gray-50
--palette-gray-100
/* ... */
--palette-gray-900

--palette-white
--palette-black
```

**Spacing:**
```css
--palette-spacing-1   /* 0.25rem / 4px */
--palette-spacing-2   /* 0.5rem / 8px */
--palette-spacing-4   /* 1rem / 16px */
--palette-spacing-6   /* 1.5rem / 24px */
--palette-spacing-8   /* 2rem / 32px */
--palette-spacing-12  /* 3rem / 48px */
--palette-spacing-16  /* 4rem / 64px */
```

**Typography:**
```css
--palette-font-size-xs    /* 0.75rem / 12px */
--palette-font-size-sm    /* 0.875rem / 14px */
--palette-font-size-md    /* 1rem / 16px */
--palette-font-size-lg    /* 1.125rem / 18px */
--palette-font-size-xl    /* 1.25rem / 20px */
--palette-font-size-2xl   /* 1.5rem / 24px */

--palette-font-weight-normal  /* 400 */
--palette-font-weight-medium  /* 500 */
--palette-font-weight-bold    /* 700 */
```

### Semantic Tokens (Tier 2)

**Colors:**
```css
/* Brand */
--color-primary
--color-secondary
--color-tertiary

/* Surfaces */
--color-surface
--color-surface-variant
--color-background

/* Text */
--color-text
--color-text-secondary
--color-text-disabled

/* Inverse (for use on primary/secondary backgrounds) */
--color-on-primary
--color-on-secondary
--color-on-surface

/* State */
--color-error
--color-warning
--color-success
--color-info

/* Borders */
--color-border
--color-border-focus
```

**Spacing:**
```css
--spacing-xs   /* Maps to palette-spacing-1 */
--spacing-sm   /* Maps to palette-spacing-2 */
--spacing-md   /* Maps to palette-spacing-4 */
--spacing-lg   /* Maps to palette-spacing-6 */
--spacing-xl   /* Maps to palette-spacing-8 */
```

**Typography:**
```css
--font-size-body
--font-size-heading
--font-size-caption
--font-size-label

--font-weight-normal
--font-weight-heading
--font-weight-bold
```

**Other Common Tokens:**
```css
--radius-sm
--radius-md
--radius-lg
--radius-full

--shadow-sm
--shadow-md
--shadow-lg

--z-dropdown
--z-modal
--z-tooltip
--z-toast
```

---

## Multi-Theme Implementation

### Theme Contract

**Core principle**: Themes ONLY swap semantic token values. Component CSS rules never change per theme.

### Implementation Pattern

```css
/* ============================================
   PALETTE TOKENS (Tier 1 - Theme Independent)
   ============================================ */
:root {
  /* Blues */
  --palette-blue-50: #eff6ff;
  --palette-blue-100: #dbeafe;
  --palette-blue-200: #bfdbfe;
  --palette-blue-300: #93c5fd;
  --palette-blue-400: #60a5fa;
  --palette-blue-500: #3b82f6;
  --palette-blue-600: #2563eb;
  --palette-blue-700: #1d4ed8;
  --palette-blue-800: #1e40af;
  --palette-blue-900: #1e3a8a;

  /* Grays */
  --palette-gray-50: #f9fafb;
  --palette-gray-100: #f3f4f6;
  --palette-gray-200: #e5e7eb;
  --palette-gray-300: #d1d5db;
  --palette-gray-400: #9ca3af;
  --palette-gray-500: #6b7280;
  --palette-gray-600: #4b5563;
  --palette-gray-700: #374151;
  --palette-gray-800: #1f2937;
  --palette-gray-900: #111827;

  /* Spacing (8px base) */
  --palette-spacing-1: 0.25rem;
  --palette-spacing-2: 0.5rem;
  --palette-spacing-4: 1rem;
  --palette-spacing-6: 1.5rem;
  --palette-spacing-8: 2rem;
}

/* ============================================
   LIGHT THEME (Default)
   ============================================ */
:root {
  /* Brand colors */
  --color-primary: var(--palette-blue-600);
  --color-secondary: var(--palette-gray-700);
  --color-on-primary: var(--palette-white);
  --color-on-secondary: var(--palette-white);

  /* Surfaces */
  --color-surface: var(--palette-white);
  --color-surface-variant: var(--palette-gray-50);
  --color-background: var(--palette-gray-100);

  /* Text */
  --color-text: var(--palette-gray-900);
  --color-text-secondary: var(--palette-gray-600);
  --color-text-disabled: var(--palette-gray-400);

  /* Borders */
  --color-border: var(--palette-gray-300);
  --color-border-focus: var(--palette-blue-500);

  /* Semantic spacing */
  --spacing-sm: var(--palette-spacing-2);
  --spacing-md: var(--palette-spacing-4);
  --spacing-lg: var(--palette-spacing-6);
}

/* ============================================
   DARK THEME
   ============================================ */
[data-theme="dark"] {
  /* Brand colors (lighter shades for dark bg) */
  --color-primary: var(--palette-blue-400);
  --color-secondary: var(--palette-gray-300);
  --color-on-primary: var(--palette-gray-900);
  --color-on-secondary: var(--palette-gray-900);

  /* Surfaces */
  --color-surface: var(--palette-gray-900);
  --color-surface-variant: var(--palette-gray-800);
  --color-background: var(--palette-gray-950, #000000);

  /* Text */
  --color-text: var(--palette-gray-50);
  --color-text-secondary: var(--palette-gray-300);
  --color-text-disabled: var(--palette-gray-600);

  /* Borders */
  --color-border: var(--palette-gray-700);
  --color-border-focus: var(--palette-blue-400);
}

/* ============================================
   HIGH-CONTRAST THEME
   ============================================ */
[data-theme="high-contrast"] {
  /* Pure contrast colors (no palette references) */
  --color-primary: #0000ff;
  --color-secondary: #000000;
  --color-on-primary: #ffffff;
  --color-on-secondary: #ffffff;

  --color-surface: #ffffff;
  --color-surface-variant: #ffffff;
  --color-background: #ffffff;

  --color-text: #000000;
  --color-text-secondary: #000000;
  --color-text-disabled: #666666;

  --color-border: #000000;
  --color-border-focus: #0000ff;
}
```

### Theme Switching Logic

**JavaScript:**
```javascript
// Set theme
function setTheme(themeName) {
  document.documentElement.setAttribute('data-theme', themeName);
  localStorage.setItem('theme', themeName);
}

// Initialize theme on load
function initTheme() {
  // 1. Check user preference in localStorage
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    setTheme(savedTheme);
    return;
  }

  // 2. Check system preference
  if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    setTheme('dark');
    return;
  }

  // 3. Default to light
  setTheme('light');
}

// Listen for system preference changes
window.matchMedia('(prefers-color-scheme: dark)')
  .addEventListener('change', (e) => {
    if (!localStorage.getItem('theme')) {
      setTheme(e.matches ? 'dark' : 'light');
    }
  });

initTheme();
```

---

## Component Token Patterns

### Pattern: Component-Scoped Override Hooks

```css
/**
 * Component: Button
 * Override hooks: --btn-bg, --btn-fg, --btn-border, --btn-radius, --btn-padding-inline, --btn-padding-block
 */
@layer components {
  .c-button {
    /* Step 1: Define component tokens with semantic fallbacks */
    --btn-bg: var(--color-primary);
    --btn-fg: var(--color-on-primary);
    --btn-border: transparent;
    --btn-radius: var(--radius-md);
    --btn-padding-inline: var(--spacing-md);
    --btn-padding-block: var(--spacing-sm);

    /* Step 2: Use component tokens in CSS rules */
    background: var(--btn-bg);
    color: var(--btn-fg);
    border: 1px solid var(--btn-border);
    border-radius: var(--btn-radius);
    padding-inline: var(--btn-padding-inline);
    padding-block: var(--btn-padding-block);
  }

  /* Variants override component tokens, not CSS properties */
  .c-button[data-variant="secondary"] {
    --btn-bg: var(--color-secondary);
    --btn-fg: var(--color-on-secondary);
  }

  .c-button[data-variant="ghost"] {
    --btn-bg: transparent;
    --btn-fg: var(--color-primary);
    --btn-border: var(--color-border);
  }

  /* Sizes override spacing tokens */
  .c-button[data-size="sm"] {
    --btn-padding-inline: var(--spacing-sm);
    --btn-padding-block: var(--spacing-xs);
  }

  .c-button[data-size="lg"] {
    --btn-padding-inline: var(--spacing-lg);
    --btn-padding-block: var(--spacing-md);
  }
}
```

### Why This Pattern Works

1. **Theming**: When themes swap `--color-primary`, button updates automatically
2. **Customization**: Consumers can override `--btn-bg` without touching component CSS
3. **Variants**: Clean, declarative variant definitions
4. **Maintainability**: Change token logic, not scattered CSS properties

---

## Package Structure

### Multi-Framework Distribution

```
@design-system/
├── tokens/                    # Design token packages
│   ├── css/
│   │   ├── palette.css       # Tier 1: Palette tokens
│   │   ├── semantic.css      # Tier 2: Semantic tokens
│   │   ├── themes/
│   │   │   ├── light.css
│   │   │   ├── dark.css
│   │   │   └── high-contrast.css
│   │   └── index.css         # Combines all
│   ├── scss/
│   │   ├── _palette.scss
│   │   ├── _semantic.scss
│   │   └── index.scss
│   ├── js/
│   │   ├── palette.js        # JavaScript tokens object
│   │   ├── semantic.js
│   │   └── index.js
│   ├── json/
│   │   ├── palette.json      # Platform-agnostic source
│   │   └── semantic.json
│   └── package.json
│
├── components/                # Component library packages
│   ├── css/
│   │   ├── button.css
│   │   ├── input.css
│   │   ├── card.css
│   │   └── index.css
│   ├── react/
│   │   ├── Button.jsx
│   │   ├── Button.css
│   │   └── index.js
│   ├── vue/
│   │   ├── Button.vue
│   │   └── index.js
│   ├── web-components/
│   │   ├── ds-button.js
│   │   └── index.js
│   └── package.json
│
└── docs/                      # Documentation site
    └── package.json
```

---

## Design Tool Integration

### Figma Tokens → Style Dictionary → Multi-Platform Output

```
┌─────────────┐
│   Figma     │  Design source
│  (Tokens)   │
└──────┬──────┘
       │
       │ Export via Figma Tokens plugin
       ▼
┌─────────────┐
│ tokens.json │  Platform-agnostic JSON
└──────┬──────┘
       │
       │ Transform with Style Dictionary
       ▼
┌─────────────────────────────────┐
│     Multi-Platform Outputs      │
├─────────────────────────────────┤
│ CSS Custom Properties           │
│ Sass Variables                  │
│ JavaScript/TypeScript Objects   │
│ iOS (Swift)                     │
│ Android (XML)                   │
└─────────────────────────────────┘
```

### Style Dictionary Configuration

**config.json:**
```json
{
  "source": ["tokens/**/*.json"],
  "platforms": {
    "css": {
      "transformGroup": "css",
      "buildPath": "dist/css/",
      "files": [
        {
          "destination": "tokens.css",
          "format": "css/variables"
        }
      ]
    },
    "scss": {
      "transformGroup": "scss",
      "buildPath": "dist/scss/",
      "files": [
        {
          "destination": "_tokens.scss",
          "format": "scss/variables"
        }
      ]
    },
    "js": {
      "transformGroup": "js",
      "buildPath": "dist/js/",
      "files": [
        {
          "destination": "tokens.js",
          "format": "javascript/es6"
        }
      ]
    }
  }
}
```

---

## Cross-Framework Distribution

### Framework-Agnostic Core Principle

**Use vanilla CSS custom properties** as the foundation:
- Widest compatibility (all modern frameworks support CSS variables)
- No build-time dependencies
- Runtime theming support
- SSR-friendly

### Framework-Specific Wrappers

**React Example:**
```jsx
import './Button.css'; // Vanilla CSS with custom properties

export function Button({ variant = 'primary', size = 'md', children }) {
  return (
    <button
      className="c-button"
      data-variant={variant}
      data-size={size}
    >
      {children}
    </button>
  );
}
```

**Vue Example:**
```vue
<template>
  <button
    class="c-button"
    :data-variant="variant"
    :data-size="size"
  >
    <slot />
  </button>
</template>

<script>
export default {
  props: {
    variant: { type: String, default: 'primary' },
    size: { type: String, default: 'md' }
  }
};
</script>

<style src="./Button.css"></style>
```

### Publishing Strategy

**Separate npm packages:**
- `@design-system/tokens` - Platform-agnostic tokens
- `@design-system/components` - Vanilla CSS components
- `@design-system/react` - React wrappers
- `@design-system/vue` - Vue wrappers
- `@design-system/web-components` - Web Components

**Monorepo with workspaces** (recommended):
- Consistent versioning across packages
- Shared build tooling
- Easier cross-package development

---

**Related Resources:**
- [Style Dictionary Documentation](https://amzn.github.io/style-dictionary/)
- [Figma Tokens Plugin](https://www.figmatokens.com/)
- [CSS Custom Properties (MDN)](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)
- [Design Tokens Community Group](https://www.w3.org/community/design-tokens/)
