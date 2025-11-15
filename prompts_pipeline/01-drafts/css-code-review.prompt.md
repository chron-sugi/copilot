# Definition of Done

A code review is complete when:

**Analysis:**
* ✅ All changed CSS files reviewed against [CSS Core Standards](../../instructions/css.instructions.md)
* ✅ Specificity impact analyzed (no unnecessary increases)
* ✅ Token usage verified (no magic literals without rationale)
* ✅ Accessibility tested (focus, contrast, motion, high-contrast)
* ✅ Cross-browser compatibility confirmed

**Documentation:**
* ✅ Findings documented with file:line references
* ✅ Code suggestions provided in diff format
* ✅ Severity assigned (Critical/High/Medium/Low)
* ✅ Risk level assessed (Low/Medium/High/Critical)

**Testing:**
* ✅ Test coverage verified (Storybook stories, visual regression)
* ✅ Missing tests/stories identified and listed
* ✅ Edge cases coverage assessed

**Decision:**
* ✅ Merge decision made (Approve/Request Changes/Block)
* ✅ Rationale provided for decision
* ✅ Follow-up items documented

---

## Merge Decision Criteria

### ✅ APPROVE
- All [CSS Core Standards](../../instructions/css.instructions.md) met
- No critical or high-severity issues
- Tests/stories adequate for changes
- Low risk of regression
- Medium-severity issues acceptable as follow-ups

### ⚠️ REQUEST CHANGES
- High-severity issues present (must fix before merge)
- Medium-severity issues that should be addressed
- Missing tests/stories for new variants
- Medium risk of regression
- Provide conditional approval criteria

### 🚫 BLOCK
- Critical issues present (accessibility violations, breaking changes)
- Standards violations that fundamentally break system
- No tests for significant new functionality
- High/critical risk of regression
- Security concerns or performance regressions

**Risk Level Definitions:**
- **LOW**: Minor style improvements, no functional impact
- **MEDIUM**: Standards violations that should be fixed but don't block
- **HIGH**: Significant issues that must be addressed before merge
- **CRITICAL**: Blockers that prevent merge (a11y violations, breaking changes, security)

---

## Anti-Patterns to Flag

### Specificity Anti-Patterns
* **Deep descendant chains:** `.sidebar .widget .item .link` → Use BEM: `.sidebar__link`
* **ID selectors in components:** `#button-primary` → Use class: `.c-button--primary`
* **!important outside utilities:** `.c-button { background: red !important; }` → Fix cascade order

### Token Anti-Patterns
* **Palette tokens in components:** `color: var(--blue-600);` → Use semantic: `var(--color-primary)`
* **Magic literals:** `border-radius: 8px;` → Use token: `var(--radius-md)`
* **Hardcoded theme values:** Themes should only swap tokens, not redeclare component rules

### Variant Anti-Patterns
* **Class proliferation:** `.button-primary-large-disabled-loading` → Use data attributes: `data-variant="primary" data-size="lg" data-state="disabled"`
* **Missing base class:** Relying on variant classes without stable `.c-component` base

### Cascade Anti-Patterns
* **Global tag overrides in components:** `.c-card a { }` → Affects all links; use `.c-card__link`
* **Unlayered overrides:** Styles outside `@layer` that silently override layered styles

### Performance Anti-Patterns
* **Expensive property overuse:** `box-shadow` on every element or hover state
* **Non-GPU-accelerated animations:** Animating `width`, `height`, `top`, `left` → Use `transform`, `opacity`

---

## Review Templates

Use these prompt templates for structured reviews:

**Quick review**:
- `#css-code-review-template` - Structured output format with risk levels

**Comprehensive review**:
- `#css-review-checklist` - Full standards verification against [CSS Core Standards](../../instructions/css.instructions.md)

**Document findings**:
- `#css-review-findings-report` - Systematic findings report with merge decision

---

## Example Review Output

```markdown
## Summary
❌ **CHANGES REQUESTED** — Risk level: **MEDIUM**

## Findings

### Tokens & Values (HIGH)
- ❌ [components/card.css:24](components/card.css#L24) — `border-radius: 12px` should use `var(--radius-lg)`
- ❌ [components/card.css:45](components/card.css#L45) — `color: #3B82F6` should use semantic token `var(--color-link)`

### Accessibility (HIGH)
- ❌ [components/card.css:67](components/card.css#L67) — Missing `:focus-visible` state on `.c-card__link`
- ✅ `prefers-reduced-motion` honored for transitions

### Testing (MEDIUM)
- ⚠️ No Storybook story for new `data-variant="highlighted"`
- ⚠️ Visual regression tests not updated

## Suggested Changes

**[components/card.css:24](components/card.css#L24)**
```diff
- border-radius: 12px;
+ border-radius: var(--radius-lg);
```

**[components/card.css:45](components/card.css#L45)**
```diff
- color: #3B82F6;
+ color: var(--color-link);
```

**[components/card.css:67](components/card.css#L67)**
```diff
  .c-card__link {
    color: var(--color-link);
+
+   &:focus-visible {
+     outline: 2px solid var(--color-focus);
+     outline-offset: 2px;
+   }
  }
```

## Missing Tests/Stories
- [ ] Storybook story: `Card` with `data-variant="highlighted"`
- [ ] Visual regression snapshot for highlighted variant (light, dark, high-contrast)
- [ ] Keyboard navigation test for card links

## Merge Readiness
**REQUEST CHANGES** — Must address before merge:
1. Replace magic literals with tokens (2 instances) — HIGH
2. Add focus styles for keyboard accessibility — HIGH
3. Update Storybook stories and visual regression tests — MEDIUM

**Conditional approval**: Once HIGH severity issues are fixed, can merge with MEDIUM issues as follow-up.
```

---
