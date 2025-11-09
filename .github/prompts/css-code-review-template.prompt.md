---
description: "Generate structured CSS code review with findings and recommendations"
mode: 'ask'
tools: ['codebase', 'search', 'problems']
---

# CSS Code Review Template

Generate a structured code review for: **PR #${input:prNumber}** - ${input:prTitle}

---

## Review Context

**Component(s) changed**: ${input:components}

**Files changed**: ${input:filesChanged}

**Type of changes**: ${input:changeType:New component / Enhancement / Bug fix / Refactor}

**Reviewer**: ${input:reviewer:Reviewer name}

---

## Review Template

Generate a comprehensive review following this structure:

```markdown
## Summary
[✅ PASS | ⚠️ NEEDS WORK | ❌ FAIL] — Risk level: **[LOW | MEDIUM | HIGH | CRITICAL]**

[1-2 sentence overall assessment]

---

## Findings

### Specificity & Selectors
[Check against CSS Core Standards for specificity rules]

- ✅ [Compliant items]
- ⚠️ [Minor issues with file:line references]
- ❌ [Blocking issues with file:line references]

### Design Tokens & Values
[Verify semantic token usage, no magic literals]

- ✅ [Compliant items]
- ❌ [Issues found - provide file:line and specific token to use]

### Variants & API
[Check data-* attributes, base class stability]

- ✅ [Compliant items]
- ⚠️ [Issues found]

### Cascade Layers
[Verify correct @layer usage]

- ✅ [Compliant items]
- ❌ [Issues found]

### Accessibility
[WCAG AA compliance check]

- ✅ [Compliant items]
- ❌ [Critical: Focus states, contrast, motion preferences]

### Responsiveness
[Container queries, media queries, logical properties]

- ✅ [Compliant items]
- ⚠️ [Issues found]

### Performance
[Bundle size, selector complexity, expensive properties]

- ✅ Bundle size impact: +X.XKB (within budget)
- ⚠️ [Performance concerns]

### Testing & Documentation
[Visual regression, accessibility tests, stories, API docs]

- ❌ [Missing tests or documentation]
- ✅ [Complete testing]

---

## Suggested Changes

[For each issue, provide specific file:line and code suggestion]

**[file-path]:[line]**
\`\`\`diff
- [current code]
+ [suggested fix]
\`\`\`

**Rationale**: [Why this change is needed]

---

## Missing Tests/Stories

- [ ] [Specific test or story needed]
- [ ] [Another test needed]

---

## Anti-Patterns Flagged

[If any anti-patterns found, list them with examples]

**[Anti-pattern name]**: [Description]
- Found at: [file:line]
- Should be: [Correct approach]

---

## Merge Readiness

**[YES | NO | CONDITIONAL]**

[If NO or CONDITIONAL, list required actions]:
1. [Required action 1]
2. [Required action 2]

[If YES]:
- All standards compliance verified
- Tests updated and passing
- Documentation complete
- No blocking issues

---

## Follow-up Items

[Optional improvements or future enhancements]:
- [ ] [Item 1]
- [ ] [Item 2]
```

---

## Review Guidelines

### Risk Level Definitions

**LOW**: Minor style improvements, no functional impact
- Documentation updates
- Code formatting
- Comment improvements

**MEDIUM**: Standards violations that should be fixed but don't block
- Magic literals instead of tokens
- Missing tests for new variants
- Minor accessibility issues

**HIGH**: Significant issues that must be addressed before merge
- Missing accessibility features (focus states, contrast)
- Performance regressions
- Breaking changes without migration guide

**CRITICAL**: Blockers that prevent merge
- WCAG violations
- Security issues
- Breaking changes to public API
- Major performance regressions

### Merge Decision Criteria

**✅ PASS (YES)**:
- All critical and high-risk findings addressed
- Standards compliance verified
- Tests updated and passing
- Documentation complete

**⚠️ NEEDS WORK (CONDITIONAL)**:
- Medium-risk findings need addressing
- Tests missing or incomplete
- Documentation gaps
- Minor accessibility issues

**❌ FAIL (NO)**:
- Critical accessibility violations
- Security concerns
- Breaking changes without migration path
- Major performance regressions
- Missing required tests

---

## Standards Reference

Review all changes against [CSS Core Standards](../../instructions/css.instructions.md):

**Key areas**:
1. Specificity (prefer 0,1,0)
2. Semantic token usage
3. WCAG AA compliance
4. Performance budgets
5. Test coverage

---

## Output Requirements

Provide:
1. **Clear summary** with risk level
2. **Categorized findings** (use emojis: ✅ ⚠️ ❌)
3. **Specific file:line references** for all issues
4. **Code suggestions** in diff format
5. **Merge decision** with clear rationale
6. **Action items** if changes needed

---

**Related**:
- [CSS Core Standards](../../instructions/css.instructions.md)
- [CSS Code Reviewer Mode](../../chatmodes/css/css-code-reviewer.chatmode.md)
- [Review Checklist](../../prompts/css-review-checklist.prompt.md)
