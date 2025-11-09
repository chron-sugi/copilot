---
description: "Generate prevention steps for CSS bug recurrence"
mode: 'agent'
tools: ['codebase', 'editor', 'search']
---

# Bug Prevention Plan Generator

Create prevention steps for: **${input:bugDescription}**

---

## Bug Context

**Component**: ${input:componentName}

**Bug summary**: ${input:bugDescription}

**Root cause**: ${input:rootCause}

**Fix applied**: ${input:fixDescription}

---

## Prevention Strategy

Generate artifacts to prevent this bug from recurring:

1. **Storybook Story** - Visual regression + documentation
2. **Automated Tests** - Catch regressions early
3. **Lint Rules** - Prevent pattern at authoring time
4. **Documentation** - Warn future developers

---

## 1. Storybook Story

### Purpose
- Document the bug scenario visually
- Enable visual regression testing
- Serve as living documentation

### Story Implementation

**File**: `${input:storybookPath:src/components/${input:componentName}/${input:componentName}.stories.js}`

**Story to add**:

```javascript
// Add this story to prevent regression of: ${input:bugDescription}
export const Bug${input:bugId:XXX}Regression = {
  name: 'Bug ${input:bugId}: ${input:bugDescription}',
  args: {
    variant: '${input:variant:primary}',
    size: '${input:size:md}',
    state: '${input:state:default}',
    // Additional props that trigger the bug scenario
  },
  parameters: {
    docs: {
      description: {
        story: \`
          **Bug ${input:bugId}**: ${input:bugDescription}

          **Root cause**: ${input:rootCause}

          **Expected**: ${input:expectedBehavior}

          **This story ensures**: The bug scenario is tested in visual regression.
        \`
      }
    },
    // Enable chromatic snapshot for this story
    chromatic: {
      disableSnapshot: false,
      modes: {
        light: { theme: 'light' },
        dark: { theme: 'dark' },
        highContrast: { theme: 'high-contrast' }
      }
    }
  },
  render: (args) => ({
    /* Component implementation */
  })
};
```

### Visual Regression Setup

**Tool**: ${input:visualRegressionTool:Chromatic/Percy/Storybook Test Runner}

**Configuration**:
```javascript
// Ensure story is captured in all themes
// Check for visual differences on every PR
```

---

## 2. Automated Tests

### Unit Test (if applicable)

**File**: `${input:testPath:src/components/${input:componentName}/${input:componentName}.test.js}`

**Test case**:

```javascript
describe('${input:componentName} - Bug ${input:bugId} Prevention', () => {
  it('should ${input:expectedBehavior}', () => {
    // Arrange: Set up component in bug scenario
    const component = render${input:componentName}({
      variant: '${input:variant}',
      size: '${input:size}',
      state: '${input:state}'
    });

    // Act: Trigger the scenario
    // (if interaction is needed)

    // Assert: Verify fix is working
    expect(component).toHaveComputedStyle({
      // Expected CSS values
    });
  });

  it('should not regress when multiple states are applied', () => {
    // Test edge case that caused the bug
    const component = render${input:componentName}({
      variant: '${input:variant}',
      state: '${input:conflictingState}'
    });

    // Assert: Variant still wins over state (or expected priority)
    expect(component).toHaveAttribute('data-variant', '${input:variant}');
  });
});
```

### Integration Test (if needed)

```javascript
// Test in context with other components
// Verify cross-component interactions don't break fix
```

---

## 3. Lint Rules

### Stylelint Rule (if pattern should be prevented)

**Scenario**: ${input:lintScenario:When should this pattern be caught?}

**Rule configuration**:

**File**: `.stylelintrc.json` or `stylelint.config.js`

```json
{
  "rules": {
    "${input:lintRule:rule-name}": ${input:lintConfig:true},

    // Custom rule (if needed)
    "plugin/custom-rule-name": [true, {
      "message": "${input:lintMessage:Avoid this pattern because it causes Bug ${input:bugId}}"
    }]
  }
}
```

### Common Lint Rules for Prevention

**Specificity issues**:
```json
{
  "selector-max-specificity": "0,3,0",
  "selector-max-id": 0,
  "selector-no-qualifying-type": true
}
```

**Token usage**:
```json
{
  "color-no-hex": true,  // Force use of tokens
  "declaration-property-value-allowed-list": {
    "color": ["/^var\\(--/"],  // Only allow custom properties
  }
}
```

**Layer enforcement**:
```json
{
  "at-rule-no-unknown": [true, {
    "ignoreAtRules": ["layer"]
  }]
}
```

---

## 4. Documentation Updates

### Component API Documentation

**File**: `${input:apiDocPath:src/components/${input:componentName}/README.md}`

**Section to add**:

```markdown
## Known Limitations

### ${input:bugDescription}

**Issue**: [Brief description of the edge case]

**Cause**: ${input:rootCause}

**Solution**: ${input:solutionGuidance}

**Example**:
\`\`\`html
<!-- ❌ Avoid this pattern -->
<${input:componentName}
  data-variant="primary"
  data-state="disabled"  <!-- Conflicts with variant -->
/>

<!-- ✅ Use this instead -->
<${input:componentName}
  data-variant="secondary"  <!-- Different variant for disabled state -->
  data-state="disabled"
/>
\`\`\`

**Reference**: See [Bug ${input:bugId}](link-to-issue) for full details.
```

### Team Knowledge Base

**File**: `.github/docs/css-bug-history.md` (or team wiki)

**Entry to add**:

```markdown
## Bug ${input:bugId}: ${input:bugDescription}

**Date**: ${input:date:2025-01-08}

**Component**: ${input:componentName}

**Root Cause**: ${input:rootCause}

**Fix**: ${input:fixDescription}

**Prevention**:
- Storybook story: \`${input:storyName}\`
- Lint rule: \`${input:lintRule}\`
- Test: \`${input:testName}\`

**Lessons Learned**:
${input:lessonsLearned:What did the team learn from this bug?}

**Related Bugs**: ${input:relatedBugs:None}
```

---

## 5. Design System Documentation (if applicable)

### Pattern Library Update

If this bug reveals a design pattern issue:

**File**: `design-system/patterns/state-management.md`

```markdown
## State and Variant Precedence

**Rule**: When both \`data-variant\` and \`data-state\` are present, state should NOT override variant colors.

**Rationale**: ${input:patternRationale}

**Implementation**:
\`\`\`css
/* ✅ Correct: Variant wins over state */
.c-component[data-variant="primary"]:not([data-state="disabled"]) {
  background: var(--color-primary);
}

/* ❌ Incorrect: State overrides variant */
.c-component[data-state="disabled"] {
  background: gray; /* This overrides variant! */
}
\`\`\`

**Reference**: Bug ${input:bugId}
```

---

## Prevention Checklist

Verify all prevention steps are complete:

### Immediate Actions
- [ ] Storybook story added for bug scenario
- [ ] Story includes all themes (light, dark, high-contrast)
- [ ] Visual regression enabled for story
- [ ] Test case added (unit or integration)
- [ ] Lint rule configured (if applicable)

### Documentation
- [ ] Component API updated with edge case warning
- [ ] Team knowledge base entry created
- [ ] Design pattern documented (if pattern issue)
- [ ] Related bugs cross-referenced

### Validation
- [ ] Story fails before fix, passes after fix
- [ ] Tests fail before fix, pass after fix
- [ ] Lint rule catches the pattern (if added)
- [ ] Documentation reviewed by team

---

## Output Format

Provide for each prevention artifact:

1. **File path** where it should be added
2. **Complete code** to add (copy-paste ready)
3. **Validation steps** to verify it works
4. **Rationale** for why this prevents recurrence

---

## Example Prevention Summary

```
Prevention Plan for Bug #123: Primary button shows gray when disabled

1. ✅ Storybook Story
   - File: src/components/Button/Button.stories.js
   - Story: Bug123Regression
   - Captures: variant="primary" + state="disabled"
   - Visual regression: Enabled for all themes

2. ✅ Automated Test
   - File: src/components/Button/Button.test.js
   - Test: "should apply variant color even when disabled"
   - Validates: Correct background color applied

3. ✅ Lint Rule
   - File: .stylelintrc.json
   - Rule: Custom rule prevents state overriding variant
   - Message: "State selectors should not override variant colors"

4. ✅ Documentation
   - File: src/components/Button/README.md
   - Added: "Known Limitations" section
   - Warns: About variant+state precedence
```

---

**Related**:
- [CSS Debugging Reference](../../docs/css-debugging-reference.md)
- [CSS Debugger Mode](../../chatmodes/css/css-debugger.chatmode.md)
- [Root Cause Analysis Template](../../prompts/css-debug-root-cause-analysis.prompt.md)
