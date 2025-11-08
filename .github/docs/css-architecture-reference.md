# CSS Architecture Reference Guide

> **Version:** 1.0 (2025-01-08)
> **Purpose:** Comprehensive reference for CSS architecture patterns, migration strategies, and detailed examples

This document provides detailed implementation examples and migration strategies referenced by CSS chat modes and prompts.

---

## Table of Contents

1. [Migration Strategy](#migration-strategy)
2. [Codemod Examples](#codemod-examples)
3. [Stylelint Configuration](#stylelint-configuration)
4. [Timeline & Milestones](#timeline-milestones)
5. [Risk Assessment](#risk-assessment)
6. [Example Architecture Decisions](#example-architecture-decisions)

---

## Migration Strategy

### Assessment Phase (Week 1-2)

**Audit existing CSS:**
* **Total size:** Use webpack-bundle-analyzer or source-map-explorer
* **Dead code percentage:** Chrome Coverage tool → (unused bytes / total bytes) × 100
* **Specificity distribution:** CSS Stats (https://cssstats.com/)
* **Token usage vs literals:** Grep for `#[0-9a-f]{3,6}` and `\d+px`
* **Browser compatibility:** Cross-browser testing matrix

**Tools:**
```bash
# Bundle size analysis
npx webpack-bundle-analyzer stats.json

# Find hex colors
grep -r "#[0-9a-fA-F]\{3,6\}" src/styles

# Find pixel values
grep -r "[0-9]\+px" src/styles

# CSS Stats
npm install -g cssstats
cssstats src/styles/main.css
```

**Identify pain points:**
* Developer survey (1-5 scale): "How difficult is it to add new CSS?"
* Bug tracker analysis: What % of bugs are CSS-related?
* Performance metrics: Current Lighthouse score, bundle size

**Set goals:**
* Performance: Bundle size < 50KB gzipped, Lighthouse ≥ 90
* Quality: Specificity average ≤ 0.15, test coverage 100%
* Developer experience: Time to component < 2 hours, satisfaction ≥ 8/10

---

### Foundation Phase (Weeks 2-3)

**Document current state:**
Create ADR (Architecture Decision Record) documenting:
* Why we're migrating (pain points, business case)
* What we're migrating to (target architecture)
* How we'll migrate (phases, timeline, risks)

**Define new architecture:**
```css
/* Layer order declaration */
@layer reset, base, tokens, utilities, objects, components, overrides;

/* Palette tokens */
:root {
  --palette-blue-600: #2563eb;
  --palette-gray-900: #111827;
  /* ... */
}

/* Semantic tokens */
:root {
  --color-primary: var(--palette-blue-600);
  --color-text: var(--palette-gray-900);
  /* ... */
}
```

**Folder structure:**
```
styles/
├── 00-reset/
│   └── normalize.css
├── 01-base/
│   ├── typography.css
│   └── elements.css
├── 02-tokens/
│   ├── palette.css
│   └── semantic.css
├── 03-utilities/
│   └── utilities.css
├── 04-objects/
│   ├── grid.css
│   └── stack.css
├── 05-components/
│   ├── button.css
│   └── card.css
└── 06-overrides/
    └── overrides.css
```

**Stylelint configuration:** See [Stylelint Configuration](#stylelint-configuration) section below

---

## Codemod Examples

### 1. Rename Classes (jscodeshift)

```javascript
// codemods/rename-classes.js
module.exports = function(fileInfo, api) {
  const j = api.jscodeshift;
  const root = j(fileInfo.source);

  // Rename mapping
  const renames = {
    'button': 'c-button',
    'card': 'c-card',
    'nav': 'c-nav',
    'modal': 'c-modal',
  };

  // Update class attributes in JSX/HTML
  root.find(j.JSXAttribute, {
    name: { name: 'className' }
  }).forEach(path => {
    const value = path.value.value;
    if (value.type === 'StringLiteral') {
      let updated = value.value;
      Object.keys(renames).forEach(old => {
        const regex = new RegExp(`\\b${old}\\b`, 'g');
        updated = updated.replace(regex, renames[old]);
      });
      value.value = updated;
    }
  });

  return root.toSource();
};

// Usage:
// npx jscodeshift -t codemods/rename-classes.js src/**/*.jsx
```

### 2. Convert Variant Classes to Data Attributes

```javascript
// codemods/data-attributes.js
module.exports = function(fileInfo, api) {
  const j = api.jscodeshift;
  const root = j(fileInfo.source);

  // Patterns to convert
  const patterns = {
    'c-button--primary': { attr: 'data-variant', value: 'primary' },
    'c-button--secondary': { attr: 'data-variant', value: 'secondary' },
    'c-button--large': { attr: 'data-size', value: 'lg' },
    'c-button--small': { attr: 'data-size', value: 'sm' },
  };

  root.find(j.JSXElement).forEach(path => {
    const openingElement = path.value.openingElement;
    const classAttr = openingElement.attributes.find(
      attr => attr.name && attr.name.name === 'className'
    );

    if (!classAttr || !classAttr.value) return;

    let classes = classAttr.value.value.split(' ');
    const newAttrs = {};

    // Extract variant classes and build data attributes
    classes = classes.filter(cls => {
      if (patterns[cls]) {
        const { attr, value } = patterns[cls];
        newAttrs[attr] = value;
        return false; // Remove this class
      }
      return true; // Keep this class
    });

    // Update className
    classAttr.value.value = classes.join(' ');

    // Add data attributes
    Object.keys(newAttrs).forEach(attr => {
      openingElement.attributes.push(
        j.jsxAttribute(
          j.jsxIdentifier(attr),
          j.stringLiteral(newAttrs[attr])
        )
      );
    });
  });

  return root.toSource();
};

// Usage:
// npx jscodeshift -t codemods/data-attributes.js src/**/*.jsx
```

### 3. Replace Literals with Tokens (PostCSS)

```javascript
// postcss-token-replace.js
const postcss = require('postcss');

// Token mapping
const tokenMap = {
  '#2563eb': 'var(--color-primary)',
  '#3B82F6': 'var(--color-primary)',
  '#1d4ed8': 'var(--color-primary-dark)',
  '16px': 'var(--spacing-md)',
  '8px': 'var(--spacing-sm)',
  '24px': 'var(--spacing-lg)',
  '0.25rem': 'var(--spacing-xs)',
  '0.5rem': 'var(--spacing-sm)',
  '1rem': 'var(--spacing-md)',
};

module.exports = postcss.plugin('postcss-token-replace', () => {
  return root => {
    root.walkDecls(decl => {
      let value = decl.value;
      Object.keys(tokenMap).forEach(literal => {
        const token = tokenMap[literal];
        value = value.replace(new RegExp(literal, 'g'), token);
      });
      if (value !== decl.value) {
        decl.value = value;
      }
    });
  };
});

// Usage in postcss.config.js:
// module.exports = {
//   plugins: [
//     require('./postcss-token-replace'),
//   ]
// };
```

---

## Stylelint Configuration

```yaml
# .stylelintrc.yml
extends:
  - stylelint-config-standard

plugins:
  - stylelint-scss
  - stylelint-order

rules:
  # Specificity budget
  selector-max-specificity: "0,2,0"

  # Naming patterns (BEM with prefixes)
  selector-class-pattern:
    - "^(c|o|u|is|has)-[a-z0-9-]+(__[a-z0-9-]+)?(--[a-z0-9-]+)?$"
    - message: "Class must follow pattern: c-*, o-*, u-*, is-*, has-*"

  # No ID selectors in components
  selector-max-id: 0

  # Prevent deep nesting
  max-nesting-depth: 3

  # Token enforcement
  scale-unlimited/declaration-strict-value:
    - ["/color$/", "fill", "stroke", "background-color", "border-color"]
    - ignoreValues: ["currentColor", "transparent", "inherit", "initial"]
      message: "Use design tokens for colors"

  # Property order
  order/properties-alphabetical-order: true

  # Layer usage (custom rule)
  csstools/use-layer:
    - "always"
    - message: "All styles must be within @layer"

  # No !important (except utilities)
  declaration-no-important:
    - true
    - severity: warning
      message: "Avoid !important (use @layer instead)"

  # Prevent magic numbers
  number-max-precision: 3
```

---

## Timeline & Milestones

### Detailed 16-Week Timeline

| Week | Phase | Milestone | Success Criteria |
|------|-------|-----------|------------------|
| 1 | Assessment | Audit complete | Baseline metrics documented |
| 2 | Foundation | ADR published | Stakeholders approved architecture |
| 3 | Foundation | Tokens defined | Palette + semantic tokens created |
| 4 | Tooling | Stylelint configured | Linting passes on new code |
| 5 | Tooling | Codemods ready | Automated refactors tested |
| 6 | Migration | 10% components migrated | High-value components updated |
| 7 | Migration | 20% components migrated | New components use new architecture |
| 8 | Migration | 30% components migrated | Bundle size reduction visible |
| 9 | Migration | 50% components migrated | Developer feedback positive |
| 10 | Migration | 60% components migrated | Test coverage maintained |
| 11 | Migration | 75% components migrated | Performance metrics improving |
| 12 | Migration | 85% components migrated | Legacy usage < 15% |
| 13 | Cleanup | Legacy deprecated | Lint warnings for legacy patterns |
| 14 | Cleanup | Hard deadline set | Migrate or update deadline announced |
| 15 | Cleanup | 95% migrated | Final stragglers being addressed |
| 16 | Complete | 100% migrated | Legacy removed, success metrics met |

---

## Risk Assessment

### Risk Matrix

| Risk | Likelihood | Impact | Severity | Mitigation Priority |
|------|------------|--------|----------|---------------------|
| Third-party CSS conflicts | High | High | **CRITICAL** | P0 - Address immediately |
| Token drift | Medium | Medium | **MEDIUM** | P1 - Automated checks |
| Developer resistance | Medium | High | **HIGH** | P1 - Training & communication |
| Browser support gaps | Low | Medium | **LOW** | P2 - Progressive enhancement |
| Timeline delays | Medium | Medium | **MEDIUM** | P1 - Buffer time in plan |

### Detailed Mitigations

**Risk 1: Third-party CSS Specificity Conflicts**
* **Impact:** High (silent overrides, production bugs)
* **Likelihood:** High (common with UI libraries)
* **Mitigation:**
  1. Wrap third-party CSS in `@layer third-party` (early in layer order)
  2. Use CSS Modules for isolation
  3. Consider postcss-prefix-selector to namespace third-party classes
  4. Document all third-party dependencies and their CSS impact
  5. Test integration in staging environment first

**Risk 2: Token Drift (Literals Creeping Back)**
* **Impact:** Medium (design system fragmentation)
* **Likelihood:** Medium (developers under time pressure)
* **Mitigation:**
  1. Stylelint rule flags hex colors and pixel values
  2. CI fails on violations
  3. Code review checklist includes token usage
  4. Regular audits (monthly grep for literals)
  5. Provide easy token lookup tool/docs

**Risk 3: Developer Resistance to Change**
* **Impact:** High (slows adoption, inconsistent codebase)
* **Likelihood:** Medium (change fatigue, learning curve)
* **Mitigation:**
  1. Involve team early (RFC process for architecture decisions)
  2. Weekly office hours for questions
  3. Pair programming sessions
  4. Codemods reduce manual work (80% automated)
  5. Celebrate wins publicly (blog posts, team meetings)
  6. Incentivize migration (gamification, sprint goals)

---

## Example Architecture Decisions

### Example ADR: Adopt CSS Cascade Layers

**Status:** Accepted

**Context:**
* Current CSS has specificity wars (`!important` in 15% of declarations)
* Developers spend ~30% of CSS debugging time on specificity issues
* Third-party CSS often overrides component styles unpredictably

**Decision:**
Adopt CSS Cascade Layers (`@layer`) with this order:
```css
@layer reset, base, tokens, utilities, objects, components, overrides;
```

**Rationale:**
* **Predictable cascade:** Layer order determines precedence, not specificity
* **Easier overrides:** No need for specificity hacks or `!important`
* **Third-party isolation:** Wrap vendor CSS in early layer
* **Browser support:** 96% (Safari 15.4+, Chrome 99+, Firefox 97+)
* **Progressive enhancement:** Gracefully degrades in older browsers

**Consequences:**
* **Positive:**
  * Eliminates most `!important` usage
  * Simplifies component CSS (single-class selectors)
  * Easier to reason about cascade
* **Negative:**
  * Requires build step for older browser support (PostCSS)
  * Team needs training on `!important` reverse behavior in layers
  * Migration effort for existing codebase

**Alternatives Considered:**
1. **CSS Modules:** Too React-specific, doesn't solve global CSS issues
2. **BEM only:** Helps but doesn't eliminate specificity wars
3. **Tailwind utility-first:** Requires complete rewrite, loses component semantics

**Implementation Plan:**
1. Add `@layer` declarations to main CSS entry
2. Update Stylelint to require all styles in layers
3. Create codemods to wrap existing styles
4. Gradual migration over 12 weeks

---

## Additional Resources

* [CSS Cascade Layers Spec](https://www.w3.org/TR/css-cascade-5/#layering)
* [Container Queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Container_Queries)
* [CSS Custom Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)
* [Style Dictionary](https://amzn.github.io/style-dictionary/)
* [jscodeshift](https://github.com/facebook/jscodeshift)
* [PostCSS](https://postcss.org/)

---

**Last Updated:** 2025-01-08
**Maintained by:** Front-End Architecture Team
