---
description: "Generate structured JavaScript code review with findings and recommendations"
mode: 'ask'
tools: ['codebase', 'search', 'problems']
---

# JavaScript Code Review Template

---

## Review Context

**Component(s) changed**: ${input:components}

**Files changed**: ${input:filesChanged}

**Type of changes**: ${input:changeType:New feature / Enhancement / Bug fix / Refactor / Performance / Security}

**Reviewer**: ${input:reviewer:Reviewer name}

---

## Review Template

Generate a comprehensive review following this structure:

```markdown
## Summary
[✅ APPROVED | ⚠️ CHANGES REQUESTED | 🚫 BLOCKED] — Risk level: **[LOW | MEDIUM | HIGH | CRITICAL]**

[1-2 sentence overall assessment]

---

## Findings

### Architecture & Organization
[Check feature-first structure, module boundaries, DI, circular deps]

- ✅ [Compliant items]
- ⚠️ [Minor issues with file:line references]
- ❌ [Blocking issues with file:line references]

### State Management
[Verify TanStack Query usage, derived state, no duplication]

- ✅ [Compliant items]
- ❌ [Issues found - provide file:line and specific fix]

### Error Handling & Logging
[Check error categorization, structured logging, correlation IDs]

- ✅ [Compliant items]
- ❌ [Issues found - missing error handling, no correlation IDs]

### Testing
[Verify unit, component, E2E coverage, error paths, flaky prevention]

- ✅ [Compliant items]
- ❌ [Missing tests with file:line]

### Performance
[Bundle size, memoization, virtual scrolling, code splitting]

- ✅ Bundle size impact: +X.XKB (within budget)
- ⚠️ [Performance concerns - premature optimization, missing virtualization]

### Security
[XSS prevention, postMessage validation, dependency vulnerabilities]

- ✅ [Compliant items]
- ❌ [Critical: XSS vulnerability, unsanitized HTML]

### Accessibility
[Keyboard nav, WCAG AA compliance, screen reader support]

- ✅ [Compliant items]
- ❌ [Critical: Missing focus styles, insufficient contrast]

---

## Suggested Changes

[For each issue, provide specific file:line and code suggestion]

**[file-path]:[line]**
\`\`\`diff
- // Current code (problematic)
+ // Suggested fix
\`\`\`

**Rationale**: [Why this change is needed]

---

## Missing Tests

- [ ] Unit test: [Specific scenario]
- [ ] Component test: [User interaction]
- [ ] Error path: [Network failure, validation error]
- [ ] Edge case: [Empty state, loading, overflow]

---

## Anti-Patterns Flagged

[If any anti-patterns found, list them with examples]

**[Anti-pattern name]**: [Description]
- Found at: [file:line]
- Should be: [Correct approach from JavaScript Core Standards]

---

## Merge Readiness

**[APPROVE | REQUEST CHANGES | BLOCK]**

[If BLOCK or REQUEST CHANGES, list required actions]:
1. [Required action 1 - SEVERITY]
2. [Required action 2 - SEVERITY]

[If APPROVE]:
- All standards compliance verified
- Tests updated and passing
- Documentation complete
- No blocking issues

**Conditional approval criteria** (if applicable):
- Once [specific issue] is fixed, can merge
- Medium-severity issues can be follow-ups

---

## Follow-up Items

[Optional improvements or future enhancements]:
- [ ] Refactor [module] to reduce complexity
- [ ] Add performance monitoring
- [ ] Improve error messages
```

---

## Review Guidelines

### Risk Level Definitions

**LOW**: Minor improvements, no functional impact
- Code formatting
- Comment improvements
- Non-critical refactoring

**MEDIUM**: Standards violations that should be fixed but don't block
- Missing dependency injection
- Modules >200 lines
- Missing test coverage for edge cases
- String-based logging instead of structured

**HIGH**: Significant issues that must be addressed before merge
- State duplication
- Missing error handling
- No tests for new functionality
- Memory leaks or race conditions
- Accessibility issues (missing focus, contrast)

**CRITICAL**: Blockers that prevent merge
- Security vulnerabilities (XSS, exposed secrets)
- Circular dependencies
- Breaking changes without migration path
- Critical accessibility violations
- Major performance regressions

### Merge Decision Criteria

**✅ APPROVE**:
- All critical and high-risk findings addressed
- Standards compliance verified
- Tests updated and passing
- Documentation complete
- Low risk of regression

**⚠️ REQUEST CHANGES**:
- High-severity issues present (must fix before merge)
- Medium-severity issues that should be addressed
- Missing tests for new functionality
- Medium risk of regression

**🚫 BLOCK**:
- Critical issues present (security, breaking changes, a11y violations)
- Standards violations that fundamentally break architecture
- No tests for significant new functionality
- High/critical risk of regression

---

## Standards Reference

Review all changes against [JavaScript Core Standards](../../instructions/javascript.instructions.md):

**Key areas**:
1. Feature-first architecture
2. Module boundaries (≤200 lines)
3. Dependency injection
4. Error categorization
5. State management (no duplication)
6. Testing coverage (70/20/10 pyramid)
7. Performance budgets
8. Security (XSS, postMessage)
9. Accessibility (WCAG AA)
10. Anti-patterns avoidance

---

## Output Requirements

Provide:
1. **Clear summary** with risk level
2. **Categorized findings** (use emojis: ✅ ⚠️ ❌ 🚫)
3. **Specific file:line references** for all issues
4. **Code suggestions** in diff format
5. **Merge decision** with clear rationale
6. **Action items** with severity levels
7. **Testing gaps** identified

---
