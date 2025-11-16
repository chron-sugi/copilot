---
description: "Document CSS bug root cause analysis systematically"
mode: 'ask'
tools: []
---

# Root Cause Analysis Documentation

Document the root cause analysis for: **${input:bugSummary}**

---

## Bug Information

**Summary**: ${input:bugSummary}

**Reporter**: ${input:reporter:Unknown}

**Date**: ${input:date:2025-01-08}

**Priority**: ${input:priority:Medium}

---

## Analysis

### Root Cause (1-3 sentences)

**Why this bug occurs**:
[Explain the underlying reason in plain language. Focus on WHY, not just WHAT.]

Example:
> "The button's primary color doesn't apply because the element has both `data-variant="primary"` and `data-state="disabled"` attributes, and the disabled state selector (`.c-button[data-state="disabled"]`) comes later in the cascade and overrides the variant selector."

---

### Evidence

**Winning selector**:
```css
[The CSS selector that is actually being applied]
```

**Specificity**: `(X, Y, Z)`
- ID selectors: X
- Class/attribute/pseudo-class selectors: Y
- Element selectors: Z

**Cascade layer**: `@layer [layer-name]` or `(unlayered)`

**Computed value**: `[actual computed CSS value from DevTools]`

**Expected value**: `[what value should be applied]`

---

### Why This Happened

Select all that apply:

- [ ] **Specificity conflict**: Higher specificity selector overriding intended rule
- [ ] **Cascade layer issue**: Wrong layer order or unlayered styles beating layered
- [ ] **Token resolution failure**: Custom property not resolving (typo, scope, missing definition)
- [ ] **Missing container-type**: Container query parent lacks `container-type` declaration
- [ ] **State/variant mismatch**: Misspelled `data-*` attribute or wrong element
- [ ] **Browser compatibility**: Feature not supported in target browser
- [ ] **Inheritance issue**: Unexpected cascading from parent
- [ ] **JavaScript timing**: Styles applied before/after DOM manipulation
- [ ] **Third-party override**: External library CSS overriding component styles
- [ ] **Other**: [Explain]

---

### Minimal Reproducible Scenario

**Component**: `${input:componentName}`

**Required markup**:
```html
[Minimal HTML that reproduces the bug]
```

**Required state**:
- Variant: `${input:variant:default}`
- Size: `${input:size:md}`
- State: `${input:state:default}`
- Theme: `${input:theme:light}`

**Conditions**:
- Viewport: ${input:viewport:Desktop (>1024px)}
- Container width: ${input:containerWidth:Auto}
- Browser: ${input:browser:All browsers}

---

### Investigation Steps Taken

Document what you checked:

1. **Cascade investigation**:
   - [ ] Checked DevTools Computed tab for winning rule
   - [ ] Verified cascade layer order
   - [ ] Identified specificity values

2. **Token resolution** (if applicable):
   - [ ] Verified custom property is defined
   - [ ] Checked scope (shadow DOM, theme context)
   - [ ] Tested with hard-coded values

3. **State/variant validation** (if applicable):
   - [ ] Verified `data-*` attributes present and spelled correctly
   - [ ] Checked attributes on correct element
   - [ ] Tested JavaScript state management

4. **Browser testing** (if applicable):
   - [ ] Tested in Chrome
   - [ ] Tested in Firefox
   - [ ] Tested in Safari
   - [ ] Tested in Edge
   - [ ] Checked feature support tables

---

## Fix Plan

### Proposed Solution

**What to change**:
[Specific change to make]

**Where to change it**:
- File: `${input:file:path/to/file.css}`
- Line(s): `${input:lines:XX-YY}`
- Layer: `${input:layer:@layer components}`

**Why this fixes it**:
[Explanation of how the change resolves the root cause]

### Fix Strategy

- [ ] **Minimal fix**: Small, surgical change (preferred)
- [ ] **Specificity adjustment**: Use `:where()` or refactor selector
- [ ] **Layer reordering**: Adjust `@layer` declaration order
- [ ] **Token fix**: Correct custom property definition or scope
- [ ] **Attribute fix**: Correct `data-*` attribute name or placement
- [ ] **Fallback addition**: Add browser compatibility fallback
- [ ] **Documentation only**: Edge case is expected behavior

### Before (Current CSS)
```css
[Show current problematic CSS]
```

### After (Fixed CSS)
```css
[Show proposed fix]
```

### Specificity Impact

**Before**: `(X, Y, Z)`
**After**: `(X, Y, Z)`

**Change**: [Increased/Decreased/Same] - [Explanation]

**Goal**: Keep specificity as low as possible (prefer `0,1,0` for components)

---

## Prevention Steps

### Immediate Prevention

1. **Add Storybook story**:
   - Story name: `${input:componentName}/${input:storyName:Bug-XXX}`
   - Purpose: Reproduce the exact bug scenario
   - Acceptance: Should FAIL before fix, PASS after fix

2. **Add visual regression test**:
   - Tool: ${input:testTool:Chromatic/Percy/Storybook Test Runner}
   - Coverage: Bug scenario + related states

3. **Add lint rule** (if pattern should be prevented):
   - Rule: `${input:lintRule:stylelint-rule-name}`
   - Config: [Stylelint configuration]
   - Message: [Error message explaining why]

4. **Update documentation**:
   - File: `${input:docFile:component-api.md}`
   - Add: Edge case, limitation, or usage warning

### Long-term Prevention

- [ ] Team knowledge sharing (post-mortem, docs)
- [ ] Pattern library update (if common pattern)
- [ ] Tooling improvement (linter, tests, types)
- [ ] Design system documentation

---

## Testing Verification

### Manual Testing Checklist

After fix is implemented:

- [ ] Bug scenario now works correctly
- [ ] No regressions in related components
- [ ] All variants tested (${input:variantsList:primary, secondary, ghost})
- [ ] All sizes tested (${input:sizesList:sm, md, lg})
- [ ] All themes tested (light, dark, high-contrast)
- [ ] Cross-browser tested (Chrome, Firefox, Safari, Edge)

### Automated Testing

- [ ] Visual regression tests pass
- [ ] Unit tests pass (if component has tests)
- [ ] Storybook story added for bug scenario
- [ ] Lint rules pass

---

## Handoff Checklist

Ready to hand off to css-developer when:

- [ ] Root cause clearly documented
- [ ] Evidence collected and verified
- [ ] Fix plan is minimal and low-risk
- [ ] Specificity impact assessed
- [ ] Prevention steps identified
- [ ] Testing criteria defined

---

## Additional Notes

${input:additionalNotes:Any other relevant information, screenshots, DevTools values, etc.}

---

## References

- **Related issues**: ${input:relatedIssues:None}
- **Similar bugs**: ${input:similarBugs:None}
- **Documentation**: [Links to relevant docs]
- **Screenshots**: [Links to screenshots/recordings]

---

**Related**:
- [CSS Debugging Reference](../../docs/css-debugging-reference.md)
- [CSS Debugger Mode](../../chatmodes/css/css-debugger.chatmode.md)
- [CSS Developer Mode](../../chatmodes/css/css-developer.chatmode.md)
