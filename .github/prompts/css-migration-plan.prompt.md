---
description: "Generate detailed CSS migration plan with phases, codemods, and timelines"
mode: agent
model: claude-sonnet-4-5
tools: ["codebase", "search", "terminal"]
---

# CSS Migration Plan Generator

Generate a comprehensive migration plan for modernizing CSS architecture to use:
- CSS Cascade Layers (@layer)
- Token-driven design system
- Data-attribute variants
- Modern specificity management

## Project Context

**Current CSS state:**
${input:currentState:Describe current CSS (bundle size, architecture, pain points)}

**Target architecture:**
${input:targetArchitecture:Describe desired architecture (layers, tokens, naming)}

**Team size:** ${input:teamSize:Number of developers}

**Timeline constraint:** ${input:timeline:Available weeks for migration}

**Critical constraints:** ${input:constraints:Budget, legacy browser support, other limitations}

---

## Required Analysis

### Phase 1: Assessment (Week 1)
Analyze and report:
1. Total CSS size and dead code percentage
2. Specificity distribution (average, max, problematic selectors)
3. Token usage vs literals (count of hex colors, pixel values)
4. Browser compatibility issues
5. Top pain points from developers

### Phase 2: Foundation (Weeks 2-3)
Plan:
1. Define layer order and document rationale
2. Create palette tokens (colors, spacing, typography, etc.)
3. Create semantic tokens (map to use cases)
4. Configure Stylelint rules
5. Set up folder structure

### Phase 3: Automation (Weeks 4-5)
Create codemods for:
1. **Rename classes:** `.button` → `.c-button`
2. **Convert variants:** `.button-primary` → `data-variant="primary"`
3. **Replace literals:** `color: #3B82F6` → `color: var(--color-primary)`
4. **Wrap in layers:** Add `@layer components { ... }` declarations

Provide example codemod scripts using:
- jscodeshift for HTML/JSX transformations
- postcss plugins for CSS transformations

### Phase 4: Incremental Migration (Weeks 6-12)
Prioritization strategy:
1. **New components:** Use new architecture immediately
2. **High-value components:** Most used, most bugs (migrate first)
3. **Low-risk legacy:** If it works, defer migration

Track metrics:
- % of components migrated
- Bundle size reduction
- CSS-related bug frequency

### Phase 5: Testing & Validation (Ongoing)
Testing requirements:
1. Visual regression tests for migrated components
2. Cross-browser testing (Chrome, Firefox, Safari, Edge)
3. Performance monitoring (bundle size, Lighthouse scores)
4. Developer feedback loops

### Phase 6: Cleanup (Final weeks)
Deprecation process:
1. Mark legacy patterns as deprecated (lint warnings)
2. Set hard deadline for legacy removal
3. Celebrate wins and share results

---

## Deliverables

1. **Migration roadmap:** Phase-by-phase with week-by-week milestones
2. **Codemod scripts:** Automated refactoring tools
3. **Stylelint configuration:** Enforcement rules
4. **Risk assessment:** Potential blockers and mitigations
5. **Success metrics:** KPIs to track (bundle size, specificity, bug rate)
6. **Timeline with milestones:** Specific dates and success criteria
7. **Communication plan:** How to inform and train team

---

## Output Format

Provide migration plan in Markdown with:
- Executive summary
- Phase-by-phase breakdown with tasks
- Codemod examples (actual code snippets)
- Timeline table with milestones
- Risk matrix with mitigations
- Success metrics dashboard spec

Refer to [CSS Architecture Reference](../docs/css-architecture-reference.md) for detailed examples.
