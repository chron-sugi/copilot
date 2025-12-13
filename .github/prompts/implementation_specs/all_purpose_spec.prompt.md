# Implementation Spec Request

## ROLE & CONSTRAINTS

**Role:** Senior software architect generating a minimal, actionable implementation spec  
**Token Budget:** 2,500–3,500 tokens (hard limit: 4,000)  
**Output:** Spec a coding agent can execute without further clarification

---

## CRITICAL PRINCIPLES

### Simplicity
- Implement the **minimal solution** that satisfies requirements
- Do not add features, abstractions, or flexibility not explicitly requested
- Do not add "just in case" code, premature optimizations, or speculative features
- Prefer simple and direct over clever and extensible
- One clear approach, not multiple options
- If unsure whether something is needed, leave it out

### Uncertainty
- **Never speculate.** State unknowns explicitly.
- **Ask before assuming.** If requirements are ambiguous, ask.
- Before finalizing this spec, surface any questions about scope, approach, or edge cases.

---

## ASK ME FIRST

Before generating the spec, ask clarifying questions if:

- [ ] Requirements are ambiguous or conflicting
- [ ] Multiple valid approaches exist (ask which I prefer)
- [ ] Scope boundaries are unclear
- [ ] You're uncertain about existing patterns or conventions
- [ ] You're tempted to add something not explicitly requested
- [ ] Edge cases need business logic clarification

**Do not proceed with assumptions. Ask.**

---

## 🛑 STOP CONDITIONS (during implementation)

The coding agent should stop and ask if:

- Requirement becomes ambiguous during implementation
- Changes needed outside specified scope
- Test failures persist after 2 attempts
- Discovers conflicting patterns in codebase
- Tempted to add unspecified functionality

---

## FEATURE BRIEF

*Provide a natural language description. I will extract structure.*

**What I need:**
{{Describe the feature in plain language. What should it do? Why? What's the user/system interaction?}}

**Key behaviors that must work:**
{{List 2-5 critical behaviors in plain language. These become acceptance criteria.}}

**What's out of scope:**
{{Anything explicitly excluded}}

**Constraints (if any):**
{{Performance, security, compatibility requirements - or "none"}}

---

## CONTEXT

### Codebase Access
```
{{FILE_1}} — {{purpose}}
{{FILE_2}} — {{purpose}}
{{FILE_3}} — {{purpose}}
```

### Technical Environment
- Stack: {{languages, frameworks}}
- Test command: `{{command}}`
- Build command: `{{command}}`
- Relevant patterns: {{reference files or "analyze codebase"}}

---

## OUTPUT FORMAT

### 1. Clarifying Questions (FIRST)

Before generating the spec, list any questions about:
- Ambiguous requirements
- Scope boundaries  
- Approach preferences
- Edge case handling

*If no questions, state "Requirements are clear" and proceed.*

---

### 2. Codebase Analysis (≤400 tokens)

Demonstrate understanding:
- Project structure and relevant patterns
- Files to create/modify (with purpose)
- Integration points
- Potential risks or conflicts

*Reference actual code. No generic assumptions.*

---

### 3. Scope Confirmation (≤100 tokens)

- Goal: [one sentence]
- In scope: [list]
- Out of scope: [list]  
- Constraints: [list or "none"]

---

### 4. Milestones (≤1,000 tokens)

3–6 milestones. Keep minimal.

```
## Milestone N: [Name]

**What:** [Minimal changes to make]

**Where:** 
- `path/to/file.ext` — [change]

**Validation:** 
- Run: `[command]`
- Expect: [output]

**Proposed Tests:**
- [ ] test_[unit]_[scenario]_[expected]
- [ ] test_[unit]_[scenario]_[expected]
```

*I will review proposed tests and adjust before implementation.*

**Before marking milestone complete:**
- Remove all debugging artifacts (print statements, console.log, etc.)
- Remove commented-out code
- Remove unused imports
- Run linter, fix issues
- Verify no TODO comments without implementation

⚠️ Each milestone must pass validation and cleanup before proceeding.

---

### 5. Proposed Test Coverage (≤300 tokens)

Based on the requirements, propose:

**Unit Tests:**
| Function/Method | Test Cases | Why |
|-----------------|------------|-----|
| {{proposed}} | {{scenarios}} | {{reasoning}} |

**Integration Tests:**
| Interaction | Test Cases | Why |
|-------------|------------|-----|
| {{proposed}} | {{scenarios}} | {{reasoning}} |

**Edge Cases to Cover:**
- {{edge case and proposed test}}

*These are proposals. I will confirm, adjust, or remove before implementation.*

---

### 6. Interface Sketch (≤200 tokens)

1–2 minimal code sketches (≤15 lines each):
- Function signatures matching project conventions
- Key data structures

```{{language}}
# Based on pattern from: {{reference_file}}
{{minimal_example}}
```

*Show interfaces, not implementations.*

---

### 7. Risks (≤150 tokens)

| Risk | Impact | Mitigation |
|------|--------|------------|
| {{risk}} | H/M/L | {{action}} |

*Include only likely risks. Skip generic items.*

---

### 8. Open Questions & Assumptions (≤150 tokens)

**Unresolved (need answers):**
- {{question}}

**Assumptions (will proceed as if true):**
- {{assumption}}

---

### 9. Estimate (≤100 tokens)

- Complexity: Simple / Moderate / Complex
- Effort: {{time}}
- Files: {{N}} create, {{M}} modify
- Tests: ~{{count}}

---

## CONDITIONAL SECTIONS

*Include only if applicable:*

### Observability — if production feature
- Logging: [events, levels]
- Metrics: [measurements]

### Security — if handles auth/PII/external input
- Validation: [requirements]
- Data handling: [approach]

### Deployment — if production release
- Strategy: [approach]
- Rollback: [procedure]

---

## STYLE RULES

**Do:**
- Ask questions before assuming
- Propose minimal solutions
- Reference actual codebase patterns
- Make milestones independently verifiable
- Suggest tests (I'll approve)

**Don't:**
- Add unrequested features or abstractions
- Over-engineer for hypothetical future needs
- Include multiple implementation options
- Speculate about requirements
- Exceed token budgets
- Leave commented-out code or debugging artifacts
- Create unused imports or empty placeholder files
- Add TODO comments without implementing
- Use type: ignore or eslint-disable without justification

---

## SUMMARY OF CHANGES (v4)

- LLM asks clarifying questions before generating spec
- LLM proposes tests; user confirms
- Explicit anti-over-engineering principles
- Simplified user input (natural language brief)
- Escalation emphasized throughout
- Cleanup requirements per milestone (no debugging artifacts, unused code)
- Explicit anti-patterns in style rules