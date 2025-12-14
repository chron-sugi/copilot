---
name: frontend.test-assessment
description: "Task Prompt for Frontend Test Assessment"
model: GPT-5 (copilot)
agent: FrontendTester


# Test Assessment Task Prompt

## Instructions

Assess test coverage for the attached code. Evaluate the quality of existing tests, identify coverage gaps, write missing tests, and report any bugs discovered during testing.

---

## Implementation Spec

{{PASTE IMPLEMENTATION SPEC HERE}}

---

## Assessment Process

### 1. Run Existing Tests
```bash
npm run test -- src/features/{{slice}}/ --coverage
```

Capture:
- Pass/fail status
- Coverage percentage per file

### 2. Evaluate Existing Test Quality

For each test file, check:
- [ ] Tests behavior, not implementation
- [ ] Meaningful assertions (not trivial)
- [ ] All UI states covered (loading, error, empty, success)
- [ ] User interactions tested
- [ ] Edge cases covered
- [ ] Uses Testing Library queries (role, label, text) not test IDs
- [ ] Uses `userEvent` over `fireEvent`
- [ ] Mocks API at network level (MSW), not hook level
- [ ] No snapshot tests (or flag as low-confidence)

### 3. Assess Coverage Against Criteria

**Logic-heavy code (90% target):**
- Contains conditionals, loops, calculations, transformations, validation

**Presentational code (80% target):**
- Pure rendering, no business logic

### 4. Identify Missing Tests

Based on spec requirements and coverage gaps:
- Which behaviors are untested?
- Which edge cases are missing?
- Which error paths are uncovered?

### 5. Write Missing Tests

Fill coverage gaps with quality tests.

### 6. Report Bugs Found

If tests reveal bugs in source code, document them for developer handoff.

---

## Output Format

### Test Run Results

```
Command: npm run test -- src/features/{{slice}}/ --coverage
Status: X passed, Y failed, Z skipped
```

**Failed Tests (if any):**
| Test | Error | Analysis |
|------|-------|----------|
| [test name] | [error message] | [likely cause - bug in source or bug in test?] |

---

### Coverage Assessment

| File | Current | Has Logic? | Target | Status |
|------|---------|------------|--------|--------|
| `ComponentA.tsx` | 85% | Yes | 90% | ❌ Gap |
| `ComponentB.tsx` | 82% | No | 80% | ✅ Met |
| `useHook.ts` | 70% | Yes | 90% | ❌ Gap |
| `utils.ts` | 95% | Yes | 90% | ✅ Met |

**Overall:** X/Y files meet coverage targets

---

### Test Quality Assessment

#### Existing Tests: `ComponentA.test.tsx`

| Criteria | Status | Notes |
|----------|--------|-------|
| Tests behavior, not implementation | ✅ / ❌ | |
| Meaningful assertions | ✅ / ❌ | |
| Loading state tested | ✅ / ❌ | |
| Error state tested | ✅ / ❌ | |
| Empty state tested | ✅ / ❌ | |
| Success state tested | ✅ / ❌ | |
| User interactions tested | ✅ / ❌ | |
| Edge cases covered | ✅ / ❌ | |
| Uses proper queries | ✅ / ❌ | |
| Mocks at network level | ✅ / ❌ | |

**Quality issues found:**
- [Issue and recommendation]

---

### Coverage Gaps

| Gap | File | What's Missing | Priority |
|-----|------|----------------|----------|
| 1 | `ComponentA.tsx` | Error state not tested | High |
| 2 | `useHook.ts` | Edge case: empty input | High |
| 3 | `ComponentA.tsx` | Loading state interaction | Medium |

---

### Tests Written

#### `ComponentA.test.tsx` (additions)

```tsx
describe('ComponentA', () => {
  it('shows error message when query fails', async () => {
    server.use(
      http.get('/api/resource', () => {
        return HttpResponse.json({ error: 'Failed' }, { status: 500 });
      })
    );

    render(<ComponentA />);

    expect(await screen.findByRole('alert')).toHaveTextContent('Failed to load');
  });

  it('handles empty data state', () => {
    // ...
  });
});
```

#### `useHook.test.ts` (new file)

```tsx
describe('useHook', () => {
  it('returns empty array when input is empty', () => {
    const { result } = renderHook(() => useHook([]));
    expect(result.current).toEqual([]);
  });
});
```

---

### Bugs Found in Source Code

*If tests revealed bugs, document for developer handoff.*

| Bug | Location | Severity | Description | Found By |
|-----|----------|----------|-------------|----------|
| 1 | `ComponentA.tsx:45` | 🔴 High | Doesn't handle error state | Error state test |
| 2 | `useHook.ts:23` | 🟡 Medium | Returns undefined for empty input | Edge case test |

**None found** — Source code behaves as expected.

---

### Summary

**Coverage:**
- Before: X% overall
- After: Y% overall
- Files meeting target: X/Y → Z/Y

**Tests added:** N new tests across M files

**Quality issues fixed:** [list or "none"]

**Bugs found:** [count or "none"]

---

### Verdict

- [ ] ✅ **Tests complete** — Coverage targets met, quality standards satisfied, no bugs found.
- [ ] ✅ **Tests complete, bugs found** — Coverage adequate, but bugs need developer attention. See bugs table above.
- [ ] ⚠️ **Partial completion** — Some tests written, but [blocker reason]. Need guidance.

---

### Developer Handoff (if bugs found)

**Bugs to fix:**
1. [Bug description, file, line]
2. [Bug description, file, line]

**After fixing:**
- Run `npm run test` to verify tests pass
- Return to tester for re-verification if needed

---

## Testing Guidelines

**Write tests that:**
- Verify behavior from the implementation spec
- Cover all UI states (loading, error, empty, success)
- Test user interactions (click, type, submit)
- Handle edge cases (empty, null, boundary values)
- Use MSW for API mocking
- Use Testing Library best practices

**Don't write:**
- Snapshot tests
- Tests that check implementation details
- Tests with trivial assertions
- Tests that mock internal functions

**If a test reveals a bug:**
- Document it, don't fix the source code
- Continue testing to find all issues
- Report all bugs at the end
