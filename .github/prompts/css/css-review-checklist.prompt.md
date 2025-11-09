---
description: "Comprehensive CSS code review checklist for PR evaluation"
mode: ask
model: claude-sonnet-4-5
tools: ["codebase", "search", "problems"]
---

# CSS Code Review Checklist

Run a comprehensive code review on CSS changes in a pull request.

## PR Information

**PR Number/URL:** ${input:prNumber:PR number or URL}

**Changed files:** ${input:files:List CSS files changed}

**Description:** ${input:description:Brief description of changes}

---

## Review Categories

Evaluate the following areas and provide structured feedback:

### 1. Specificity & Selectors
- [ ] Specificity kept as low as possible (prefer 0,1,0)
- [ ] No ID selectors in component styles
- [ ] Shallow selectors (avoid deep chains like `.a .b .c .d`)
- [ ] Minimal nesting (BEM eliminates most nesting)
- [ ] Use of `:where()` for zero-specificity when appropriate

**Findings:**
[List issues with file:line references]

### 2. Design Tokens & Values
- [ ] Uses semantic tokens (not palette tokens)
- [ ] No magic literals (hex colors, pixel values without tokens)
- [ ] Rationale provided if literals are necessary
- [ ] `@property` rules for type-safe animated tokens

**Findings:**
[List issues with suggested token replacements]

### 3. Variants & API
- [ ] Variants use `data-*` attributes
- [ ] State classes use `is-*` or `has-*` prefix
- [ ] Base class remains stable (no class proliferation)
- [ ] Component API documented

**Findings:**
[List API issues or missing documentation]

### 4. Cascade Layers
- [ ] Rules in correct `@layer`
- [ ] Layer order respected
- [ ] No unlayered styles overriding layered styles
- [ ] `!important` limited to utilities

**Findings:**
[List layer violations]

### 5. Accessibility
- [ ] Focus states visible (`:focus-visible`)
- [ ] Color contrast meets WCAG AA (4.5:1 text, 3:1 UI)
- [ ] `prefers-reduced-motion` honored
- [ ] `forced-colors` and high-contrast tested
- [ ] Touch targets ≥ 44×44px

**Findings:**
[List accessibility issues with severity]

### 6. Responsiveness
- [ ] Container queries for component-level
- [ ] Media queries for global layout only
- [ ] Logical properties for i18n
- [ ] Fluid sizing with `clamp()`

**Findings:**
[List responsive design issues]

### 7. Performance
- [ ] No unused selectors
- [ ] Reasonable selector complexity
- [ ] GPU-accelerated animations (`transform`, `opacity`)
- [ ] Minimal expensive properties (`box-shadow`, `filter`)
- [ ] Bundle size impact within budget (< 50KB gzipped)

**Findings:**
[List performance concerns]

### 8. Cross-Browser Compatibility
- [ ] Tested in target browsers
- [ ] Fallbacks for features < 95% support
- [ ] Progressive enhancement documented
- [ ] Vendor prefixes via Autoprefixer

**Findings:**
[List compatibility issues]

### 9. Testing & Documentation
- [ ] Visual regression tests updated
- [ ] Accessibility tests pass (axe)
- [ ] Stories cover states × variants × sizes × themes
- [ ] Component API docs updated
- [ ] Migration guide if breaking changes

**Findings:**
[List missing tests or documentation]

---

## Anti-Patterns Check

Flag if present:
- [ ] Deep descendant chains (> 3 levels)
- [ ] ID selectors in components
- [ ] `!important` outside utilities
- [ ] Palette tokens in components
- [ ] Magic literals (hex/px without rationale)
- [ ] Class proliferation (`.button-primary-large-disabled`)
- [ ] Theme-forked component rules
- [ ] Non-GPU-accelerated animations

**Anti-patterns found:**
[List with file:line and suggested fixes]

---

## Output Format

Provide review in this structure:

```markdown
## Summary
[PASS/FAIL] — Risk level: [LOW/MEDIUM/HIGH/CRITICAL]

## Findings by Category
[Organized list of issues]

## Suggested Changes
[Code diff snippets with file:line references]

## Missing Tests/Stories
[Checklist of test coverage gaps]

## Merge Readiness
[YES/NO] + rationale + required follow-up tasks

## Estimated Effort
[Time estimate to address findings]
```

---

Refer to:
- [CSS Core Standards](../.github/instructions/css.instructions.md) for standards
- [CSS Code Reviewer Mode](../.github/chatmodes/css-code-reviewer.chatmode.md) for review guidance
