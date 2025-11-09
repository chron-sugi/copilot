---
description: "Document CSS code review findings systematically"
mode: 'ask'
tools: []
---

# CSS Review Findings Documentation

Document findings from CSS code review systematically.

---

## Review Information

**PR Number**: #${input:prNumber}

**PR Title**: ${input:prTitle}

**Reviewer**: ${input:reviewer}

**Date**: ${input:reviewDate:2025-01-08}

**Components Reviewed**: ${input:components}

---

## Summary Assessment

**Overall Status**: ${input:status:APPROVED / CHANGES REQUESTED / BLOCKED}

**Risk Level**: ${input:riskLevel:LOW / MEDIUM / HIGH / CRITICAL}

**Files Changed**: ${input:filesCount} files

**Lines Changed**: +${input:linesAdded} -${input:linesRemoved}

---

## Findings by Category

### Specificity & Selectors

**Status**: ${input:specificityStatus:✅ Compliant / ⚠️ Minor issues / ❌ Issues found}

**Findings**:
${input:specificityFindings:List findings or "No issues found"}

**Examples**:
```css
/* Issue found */
${input:specificityExample}

/* Suggested fix */
${input:specificitySuggestion}
```

**Impact**: ${input:specificityImpact:Low / Medium / High}

---

### Design Tokens & Values

**Status**: ${input:tokensStatus:✅ Compliant / ⚠️ Minor issues / ❌ Issues found}

**Magic Literals Found**: ${input:literalsCount:0}

**Findings**:
${input:tokensFindings:List each literal with file:line and suggested token}

**Examples**:
```css
/* ❌ Before (magic literal) */
${input:literalExample}

/* ✅ After (semantic token) */
${input:tokenSuggestion}
```

**Impact**: ${input:tokensImpact:Low / Medium / High}

---

### Variants & Component API

**Status**: ${input:variantsStatus:✅ Compliant / ⚠️ Minor issues / ❌ Issues found}

**Findings**:
${input:variantsFindings}

**API Documentation**: ${input:apiDocStatus:Complete / Incomplete / Missing}

**Impact**: ${input:variantsImpact:Low / Medium / High}

---

### Cascade Layers

**Status**: ${input:layersStatus:✅ Compliant / ⚠️ Minor issues / ❌ Issues found}

**Findings**:
${input:layersFindings}

**Unlayered Styles**: ${input:unlayeredCount:0} found

**Impact**: ${input:layersImpact:Low / Medium / High}

---

### Accessibility (WCAG 2.2 AA)

**Status**: ${input:a11yStatus:✅ Compliant / ⚠️ Minor issues / ❌ VIOLATIONS}

**Critical Issues**: ${input:a11yCritical:0}

**Findings**:

**Focus States**:
- ${input:focusFindings:Status}

**Color Contrast**:
- ${input:contrastFindings:All text meets 4.5:1, UI meets 3:1}

**Motion Preferences**:
- ${input:motionFindings:prefers-reduced-motion honored}

**Touch Targets**:
- ${input:touchFindings:All targets ≥ 44×44px}

**High-Contrast Support**:
- ${input:highContrastFindings:forced-colors tested}

**Impact**: ${input:a11yImpact:LOW / MEDIUM / HIGH / **CRITICAL**}

---

### Responsiveness

**Status**: ${input:responsiveStatus:✅ Compliant / ⚠️ Minor issues / ❌ Issues found}

**Container Queries**: ${input:containerQueriesStatus:Used appropriately / Not used / Issues found}

**Logical Properties**: ${input:logicalPropsStatus:Used for i18n / Not used / Issues found}

**Findings**:
${input:responsiveFindings}

**Impact**: ${input:responsiveImpact:Low / Medium / High}

---

### Performance

**Status**: ${input:performanceStatus:✅ Within budget / ⚠️ Monitor / ❌ Regression}

**Bundle Size Impact**: ${input:bundleDelta:+0.0KB (gzipped)}

**Expensive Properties**:
- ${input:expensiveProps:None / List properties with usage count}

**Animation Performance**:
- ${input:animationPerf:GPU-accelerated / Issues found}

**Selector Complexity**:
- ${input:selectorComplexity:Reasonable / Overly complex selectors found}

**Impact**: ${input:performanceImpact:Low / Medium / High}

---

### Cross-Browser Compatibility

**Status**: ${input:browserStatus:✅ Compatible / ⚠️ Minor issues / ❌ Issues found}

**Modern Features Used**:
- ${input:modernFeatures:List features and browser support %}

**Fallbacks Provided**:
- ${input:fallbacks:Yes / No / Partial}

**Testing**:
- Chrome: ${input:chromeTest:✅ Tested / ⚠️ Not tested}
- Firefox: ${input:firefoxTest:✅ Tested / ⚠️ Not tested}
- Safari: ${input:safariTest:✅ Tested / ⚠️ Not tested}
- Edge: ${input:edgeTest:✅ Tested / ⚠️ Not tested}

**Impact**: ${input:browserImpact:Low / Medium / High}

---

### Testing & Documentation

**Status**: ${input:testingStatus:✅ Complete / ⚠️ Gaps / ❌ Missing}

**Visual Regression Tests**:
- Status: ${input:visualRegStatus:Updated / Not updated}
- Stories added: ${input:storiesAdded:0}
- Themes covered: ${input:themesCovered:light, dark, high-contrast}

**Accessibility Tests**:
- axe-core: ${input:axeStatus:Passing / Failing / Not run}
- Lighthouse: ${input:lighthouseScore:100 / score}
- Manual keyboard test: ${input:keyboardTest:Passed / Not done}

**Documentation**:
- Component API: ${input:apiDocStatus:Complete / Incomplete / Missing}
- Migration guide: ${input:migrationStatus:N/A / Provided / Missing}

**Missing Tests/Stories**:
${input:missingTests:List or "None"}

**Impact**: ${input:testingImpact:Low / Medium / High}

---

## Severity Breakdown

### Critical Issues (🔴 BLOCKER)
**Count**: ${input:criticalCount:0}

${input:criticalIssues:List each issue with:
- Description
- File:line
- Why it's critical
- Required fix
}

### High Priority Issues (🟠 REQUIRED)
**Count**: ${input:highCount:0}

${input:highIssues:List each issue}

### Medium Priority Issues (🟡 RECOMMENDED)
**Count**: ${input:mediumCount:0}

${input:mediumIssues:List each issue}

### Low Priority Suggestions (🟢 NICE TO HAVE)
**Count**: ${input:lowCount:0}

${input:lowIssues:List each suggestion}

---

## Anti-Patterns Identified

${input:antiPatterns:List any anti-patterns found with examples}

Example:
- **Deep descendant chains**: `.sidebar .widget .item .link` at components/card.css:42
  - Should use BEM: `.sidebar__link`

---

## Suggested Changes

### Required Changes (Before Merge)

**File: ${input:file1}**
```diff
- ${input:before1}
+ ${input:after1}
```
**Rationale**: ${input:rationale1}

[Repeat for each required change]

### Recommended Changes (Post-Merge)

**File: ${input:file2}**
```diff
- ${input:before2}
+ ${input:after2}
```
**Rationale**: ${input:rationale2}

[Repeat for each recommended change]

---

## Merge Decision

**Decision**: ${input:mergeDecision:APPROVE / REQUEST CHANGES / BLOCK}

### Rationale

${input:mergeRationale}

### Required Actions (if REQUEST CHANGES or BLOCK)

**Must complete before merge**:
1. ${input:requiredAction1}
2. ${input:requiredAction2}

**Estimated effort**: ${input:effortEstimate:X hours}

### Conditional Approval Criteria (if REQUEST CHANGES)

Approve when:
- [ ] ${input:approvalCriteria1}
- [ ] ${input:approvalCriteria2}

---

## Follow-Up Items

**Post-Merge Improvements**:
- [ ] ${input:followUp1}
- [ ] ${input:followUp2}

**Future Enhancements**:
- [ ] ${input:enhancement1}
- [ ] ${input:enhancement2}

---

## Standards Compliance Summary

| Category | Status | Issues | Impact |
|----------|--------|--------|--------|
| Specificity | ${input:specificityStatus} | ${input:specificityIssues:0} | ${input:specificityImpact} |
| Tokens | ${input:tokensStatus} | ${input:tokensIssues:0} | ${input:tokensImpact} |
| Variants | ${input:variantsStatus} | ${input:variantsIssues:0} | ${input:variantsImpact} |
| Layers | ${input:layersStatus} | ${input:layersIssues:0} | ${input:layersImpact} |
| Accessibility | ${input:a11yStatus} | ${input:a11yIssues:0} | ${input:a11yImpact} |
| Responsive | ${input:responsiveStatus} | ${input:responsiveIssues:0} | ${input:responsiveImpact} |
| Performance | ${input:performanceStatus} | ${input:performanceIssues:0} | ${input:performanceImpact} |
| Browser | ${input:browserStatus} | ${input:browserIssues:0} | ${input:browserImpact} |
| Testing | ${input:testingStatus} | ${input:testingIssues:0} | ${input:testingImpact} |

**Overall Compliance**: ${input:overallCompliance:85%}

---

## Reviewer Notes

${input:reviewerNotes:Any additional context, concerns, or observations}

---

## Next Steps

**If APPROVED**:
1. Merge pull request
2. Monitor in staging
3. Deploy to production
4. Address follow-up items in next sprint

**If CHANGES REQUESTED**:
1. Developer addresses required actions
2. Re-review after changes
3. Approval when criteria met

**If BLOCKED**:
1. Discuss critical issues with team
2. Plan remediation approach
3. Re-submit when issues resolved

---

**Reviewed by**: ${input:reviewer}
**Review Date**: ${input:reviewDate}
**Next Review**: ${input:nextReview:After developer addresses changes}

---

**Related**:
- [CSS Core Standards](../../instructions/css.instructions.md)
- [CSS Code Reviewer Mode](../../chatmodes/css/css-code-reviewer.chatmode.md)
- [Review Template](../../prompts/css-code-review-template.prompt.md)
- [Review Checklist](../../prompts/css-review-checklist.prompt.md)
