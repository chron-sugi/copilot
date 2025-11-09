---
description: "Generate validation checklist for CSS bug fix"
mode: 'ask'
tools: []
---

# Fix Validation Checklist Generator

Create validation checklist for fix to: **${input:bugDescription}**

---

## Bug & Fix Context

**Bug ID**: ${input:bugId:XXX}

**Bug summary**: ${input:bugDescription}

**Component**: ${input:componentName}

**Fix applied**: ${input:fixDescription}

**Fixed by**: ${input:developer:css-developer}

---

## Validation Checklist

### 1. Visual Verification

**Original bug scenario**:
- [ ] Bug scenario now displays correctly
- [ ] Expected behavior matches actual behavior
- [ ] No visual glitches or artifacts

**Component variants**:
- [ ] Primary variant: ${input:hasPrimaryVariant:✅/❌}
- [ ] Secondary variant: ${input:hasSecondaryVariant:✅/❌}
- [ ] Ghost variant: ${input:hasGhostVariant:✅/❌}
- [ ] Danger variant: ${input:hasDangerVariant:✅/❌}
- [ ] Other variants: ${input:otherVariants:None}

**Component sizes**:
- [ ] Small (sm): ${input:hasSmallSize:✅/❌}
- [ ] Medium (md): ${input:hasMediumSize:✅/❌}
- [ ] Large (lg): ${input:hasLargeSize:✅/❌}
- [ ] Extra large (xl): ${input:hasXLSize:✅/❌}

**Component states**:
- [ ] Default state
- [ ] Hover state (`:hover`)
- [ ] Focus state (`:focus-visible`)
- [ ] Active state (`:active`)
- [ ] Disabled state (`[data-state="disabled"]`)
- [ ] Loading state (`[data-state="loading"]`)
- [ ] Error state (`[data-state="error"]`)

**Themes**:
- [ ] Light theme (default)
- [ ] Dark theme (`[data-theme="dark"]`)
- [ ] High-contrast theme (`[data-theme="high-contrast"]`)
- [ ] Brand themes: ${input:brandThemes:None}

---

### 2. Cross-Browser Testing

**Desktop browsers**:
- [ ] Chrome ${input:chromeVersion:Latest} (Windows/macOS)
- [ ] Firefox ${input:firefoxVersion:Latest} (Windows/macOS)
- [ ] Safari ${input:safariVersion:Latest} (macOS)
- [ ] Edge ${input:edgeVersion:Latest} (Windows)

**Mobile browsers** (if applicable):
- [ ] Safari iOS ${input:safariIOSVersion:Latest}
- [ ] Chrome Android ${input:chromeAndroidVersion:Latest}

**Browser-specific checks**:
- [ ] No console errors in any browser
- [ ] Feature fallbacks work in older browsers
- [ ] Vendor prefixes applied correctly (via Autoprefixer)

---

### 3. Regression Testing

**Related components**:
- [ ] Fix doesn't break similar components: ${input:relatedComponents:List components}
- [ ] Shared styles still work correctly
- [ ] Token changes don't affect other components

**Specificity impact**:
- **Before fix**: Specificity was `${input:specificityBefore:(0,1,0)}`
- **After fix**: Specificity is `${input:specificityAfter:(0,1,0)}`
- [ ] Specificity didn't increase unnecessarily
- [ ] Fix uses minimal specificity possible
- [ ] No new `!important` declarations added (unless justified)

**Cascade & layer impact**:
- [ ] Fix is in correct `@layer` (${input:layer:@layer components})
- [ ] Layer order unchanged (or documented if changed)
- [ ] No unlayered styles added
- [ ] Fix doesn't override other components' styles

**Performance**:
- [ ] No unnecessary complexity added
- [ ] No expensive properties on frequent interactions (box-shadow, filter)
- [ ] Animations use GPU-accelerated properties (transform, opacity)

---

### 4. Automated Testing

**Visual regression tests**:
- [ ] Chromatic/Percy/Storybook snapshots pass
- [ ] All stories captured (including new bug story)
- [ ] No unintended visual changes

**Unit/integration tests**:
- [ ] All existing tests pass
- [ ] New test added for bug scenario
- [ ] Test fails before fix, passes after fix

**Lint checks**:
- [ ] Stylelint passes (no new violations)
- [ ] ESLint passes (if JavaScript changes)
- [ ] Prettier formatting applied

---

### 5. Accessibility Verification

**Color contrast**:
- [ ] Text contrast ≥ 4.5:1 (WCAG AA for normal text)
- [ ] UI component contrast ≥ 3:1 (WCAG AA for UI)
- [ ] Contrast maintained in all themes

**Focus indicators**:
- [ ] Focus styles visible on all interactive elements
- [ ] Focus indicator contrast ≥ 3:1
- [ ] `:focus-visible` used (not just `:focus`)

**Motion preferences**:
- [ ] `prefers-reduced-motion: reduce` honored
- [ ] Animations disabled or simplified when preference set

**High-contrast modes**:
- [ ] Works in `forced-colors: active` mode
- [ ] Works in `prefers-contrast: high` mode
- [ ] System high-contrast themes supported

---

### 6. Responsive Behavior

**Container queries** (if applicable):
- [ ] Parent has `container-type` set correctly
- [ ] Container query breakpoints functional
- [ ] Component responds to container size (not viewport)

**Media queries** (if applicable):
- [ ] Breakpoints work as expected
- [ ] Mobile view tested (< 768px)
- [ ] Tablet view tested (768px - 1024px)
- [ ] Desktop view tested (> 1024px)

**Logical properties** (for RTL support):
- [ ] Uses `inline-start`/`inline-end` instead of `left`/`right`
- [ ] Uses `block-start`/`block-end` instead of `top`/`bottom`
- [ ] Tested in RTL mode (if applicable)

---

### 7. Prevention Validation

**Storybook story**:
- [ ] Story added: `${input:storyName:ComponentName/BugXXXRegression}`
- [ ] Story reproduces original bug scenario
- [ ] Story includes documentation of bug and fix
- [ ] Visual regression enabled for story

**Test coverage**:
- [ ] Test case added for bug scenario
- [ ] Test validates fix is working
- [ ] Test will catch regression if bug reoccurs

**Lint rules** (if applicable):
- [ ] Lint rule configured: ${input:lintRule:None}
- [ ] Lint rule catches the problematic pattern
- [ ] Error message is clear and helpful

**Documentation**:
- [ ] Component API updated (if edge case)
- [ ] Known limitations documented (if any)
- [ ] Migration guide provided (if breaking change)
- [ ] Team knowledge base updated

---

### 8. Code Quality

**CSS quality**:
- [ ] Follows BEM naming conventions
- [ ] Uses design tokens (not magic literals)
- [ ] Token-first approach maintained
- [ ] No hard-coded colors/spacing values
- [ ] Comments explain WHY, not WHAT

**Maintainability**:
- [ ] Fix is minimal (no over-engineering)
- [ ] Fix is surgical (doesn't touch unrelated code)
- [ ] Fix is understandable (clear intent)
- [ ] Fix is documented (root cause explained)

**Git**:
- [ ] Commit message references bug ID
- [ ] Commit includes before/after explanation
- [ ] Changes are focused (one bug, one commit)

---

## Validation Summary

### Critical Checks (Must Pass)

1. ✅ Original bug scenario fixed
2. ✅ No regressions in related components
3. ✅ All automated tests pass
4. ✅ Cross-browser compatibility verified
5. ✅ Accessibility standards maintained

### Recommended Checks (Should Pass)

6. ⚠️ Visual regression tests added
7. ⚠️ Prevention story added
8. ⚠️ Documentation updated
9. ⚠️ Specificity minimized

### Nice-to-Have Checks (Optional)

10. 💡 Lint rules added for pattern prevention
11. 💡 Team knowledge base updated
12. 💡 Design pattern documented

---

## Sign-Off

**Tested by**: ${input:tester:Name}

**Date**: ${input:testDate:2025-01-08}

**Status**: ${input:status:✅ Approved / ⚠️ Needs fixes / ❌ Rejected}

**Notes**: ${input:notes:Any additional observations or concerns}

---

## Next Steps

Based on validation results:

### If ✅ Approved
- [ ] Merge pull request
- [ ] Deploy to staging
- [ ] Verify in staging environment
- [ ] Deploy to production
- [ ] Monitor for issues

### If ⚠️ Needs Fixes
- [ ] Document issues found: ${input:issuesFound}
- [ ] Return to css-developer for fixes
- [ ] Re-test after fixes applied

### If ❌ Rejected
- [ ] Document why fix doesn't work: ${input:rejectionReason}
- [ ] Re-analyze root cause (may be incorrect)
- [ ] Propose alternative fix strategy

---

**Related**:
- [CSS Debugging Reference](../../docs/css-debugging-reference.md)
- [CSS Debugger Mode](../../chatmodes/css/css-debugger.chatmode.md)
- [Root Cause Analysis Template](../../prompts/css-debug-root-cause-analysis.prompt.md)
- [Prevention Plan Template](../../prompts/css-debug-prevention-plan.prompt.md)
