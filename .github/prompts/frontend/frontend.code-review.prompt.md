---
name: frontend.code-review
description: "Code Review Task Prompt for Frontend Implementations"
model: GPT-5 (copilot)
agent: FrontendcodeReviewer
---
version: 1.0
---

# Code Review Task Prompt

## Instructions

Review the attached code against the implementation spec below. Verify the developer implemented the spec correctly and followed project standards.

**Important:** The spec is not infallible. If the developer deviated from the spec, evaluate whether the deviation was justified. The developer may have discovered edge cases, technical constraints, or better approaches during implementation.

---

## Implementation Spec

{{PASTE IMPLEMENTATION SPEC HERE}}

---

## Review Checklist

### 1. Spec Compliance
- [ ] All requirements from spec are implemented (or deviation is justified)
- [ ] No unspecified features added without justification
- [ ] Scope boundaries respected
- [ ] Edge cases from spec are handled

### 2. Component Structure
- [ ] Component hierarchy matches spec
- [ ] Props and types match spec definitions
- [ ] All UI states implemented (loading, error, empty, success)

### 3. Project Standards
- [ ] TypeScript strict, no `any`, proper types
- [ ] Named exports only (no default exports)
- [ ] Imports use `@/` alias, no `../../`
- [ ] Files in correct FSD layer/slice
- [ ] File naming follows conventions

### 4. Data & State
- [ ] TanStack Query for server state
- [ ] Zustand selectors are specific (not pulling entire store)
- [ ] Zod validation at data boundaries
- [ ] Forms use React Hook Form + Zod

### 5. Quality
- [ ] No console.log or debugging artifacts
- [ ] No commented-out code
- [ ] No unused imports/variables
- [ ] Tests exist for new code
- [ ] Accessible (labels, keyboard, semantic HTML)

---

## Output Format

### Summary

[1-2 sentences: Does the implementation match the spec? Any major concerns?]

### Spec Compliance

| Requirement | Status | Notes |
|-------------|--------|-------|
| [from spec] | ✅ / ❌ / ⚠️ | [if ❌, what's wrong; if ⚠️, deviation noted below] |
| [from spec] | ✅ / ❌ / ⚠️ | |

### Spec Deviations

Document any cases where the implementation differs from the spec:

#### Justified Deviations (spec should be updated)

| Deviation | Justification | Recommendation |
|-----------|---------------|----------------|
| [what differs] | [why it's correct] | Update spec to reflect this |

#### Unjustified Deviations (code should be fixed)

| Deviation | Expected (per spec) | Action |
|-----------|---------------------|--------|
| [what differs] | [what spec required] | See issue below |

*If no deviations, state "None - implementation matches spec."*

### Issues Found

#### 🔴 Must Fix (blocks approval)

**Issue:** [what's wrong]
**File:** `path/to/file.tsx` (line X)
**Spec requirement:** [what the spec said]
**Fix:** 
```tsx
// What to change
```

---

#### 🟡 Should Fix (recommended before merge)

**Issue:** [what's wrong]
**File:** `path/to/file.tsx` (line X)
**Fix:**
```tsx
// What to change
```

---

#### 🟢 Consider (optional improvements)

- [minor suggestion]

---

### Verdict

- [ ] ✅ **Approved** — Implements spec correctly, meets standards. Ready for tester.
- [ ] ✅ **Approved with spec updates** — Implementation correct but deviates from spec. Update spec to match, then ready for tester.
- [ ] 🔄 **Revisions needed** — See Must Fix / Should Fix items above.

---

### Developer Handoff (if revisions needed)

**Priority fixes:**
1. [First thing to fix]
2. [Second thing to fix]

**After fixing, verify:**
- `npm run typecheck` passes
- `npm run lint` passes
- `npm run test` passes

---

## Review Guidelines

**Focus on:**
- Does it match the spec, or is the deviation justified?
- Does it follow project conventions?
- Is it correct?

**When evaluating deviations:**
- Did the developer find an edge case the spec missed?
- Is there a technical constraint the spec didn't anticipate?
- Is the deviation a genuine improvement?
- If yes to any → Justified deviation, recommend spec update
- If no → Unjustified deviation, flag as issue

**Don't flag:**
- Style preferences beyond project standards
- Alternative approaches that aren't clearly better
- Premature optimization suggestions
- Things outside the implementation scope

**If unclear:**
- State what's unclear
- Ask for clarification rather than assuming
