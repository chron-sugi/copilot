# Python Implementation Spec

## ROLE

Generate a minimal, actionable implementation spec for a Python feature.
Follow conventions from system prompt. This spec defines *what* to build.

**Token Budget:** 2,500–3,500 tokens (hard limit: 4,000)

---

## CRITICAL REMINDERS

These override defaults. Agents commonly violate these despite system prompts:

### Simplicity
- **Minimal solution only.** No unrequested features, abstractions, or flexibility.
- If tempted to add something "just in case" — don't.

### Uncertainty
- **Ask before assuming.** If requirements are ambiguous, ask.
- Do not proceed with guesses.

### Spec Style
- **Prose requirements over code.** Describe what functions should do, not how.
- **Signatures without bodies.** Show interfaces, not implementations.
- **Schemas are contracts.** Pydantic/dataclass definitions belong in specs.

---

## ASK ME FIRST

Before generating the spec, ask clarifying questions if:

- [ ] Requirements are ambiguous or conflicting
- [ ] Multiple valid approaches exist
- [ ] Scope boundaries are unclear
- [ ] Edge cases need business logic clarification
- [ ] Uncertain whether to use Pydantic vs dataclass

**Do not proceed with assumptions. Ask.**

---

## 🛑 STOP CONDITIONS

During implementation, stop and ask if:

- Requirement becomes ambiguous
- Changes needed outside specified scope
- Test failures persist after 2 attempts
- Tempted to add unspecified functionality

---

## FEATURE BRIEF

*Provide natural language. I will extract structure.*

**What I need:**
{{Describe the feature. What should it do? Why?}}

**Key behaviors:**
{{2-5 critical behaviors in plain language}}

**Out of scope:**
{{Explicitly excluded}}

**Constraints:**
{{Performance, security, compatibility — or "none"}}

---

## CONTEXT

### Files
```
{{FILE_1}} — {{purpose}}
{{FILE_2}} — {{purpose}}
{{FILE_3}} — {{purpose}}
```

### Environment
- Key dependencies: {{pydantic, polars, etc.}}
- Test: `pytest {{path}} -v`
- Lint: `ruff check --fix && ruff format`
- Type check: `mypy {{path}}`

---

## OUTPUT FORMAT

### 1. Clarifying Questions (FIRST)

List questions about ambiguous requirements, scope, approach, or edge cases.

*If none, state "Requirements are clear" and proceed.*

---

### 2. Codebase Analysis (≤300 tokens)

- Relevant existing patterns (with file references)
- Files to create/modify
- Integration points
- Risks

*Reference actual code. No generic assumptions.*

---

### 3. Scope Confirmation (≤100 tokens)

- Goal: [one sentence]
- In scope: [list]
- Out of scope: [list]
- Constraints: [list or "none"]

---

### 4. Data Models (≤200 tokens)

Define models needed. Pydantic for external data, dataclass for internal.

```python
class SomethingInput(BaseModel):
    """Docstring."""
    field: type

@dataclass
class SomethingInternal:
    """Docstring."""
    field: type
```

*Show fields and types. Note new vs modifications.*

---

### 5. Milestones (≤800 tokens)

3–5 milestones. Minimal scope each.

```
## Milestone N: [Name]

**What:** [Changes to make]

**Where:** 
- `path/to/{subpackage}_module.py` — [change]

**Validation:** 
- Run: `pytest tests/unit/{subpackage}/test_module.py -v`
- Expect: [output]

**Proposed Tests:**
- [ ] test_{unit}_{scenario}_{expected}
- [ ] test_{unit}_{scenario}_{expected}
```

*I will review proposed tests before implementation.*

**Milestone Completion Checklist:**
- [ ] Tests pass
- [ ] `ruff check --fix && ruff format` clean
- [ ] `mypy` clean
- [ ] No debugging artifacts, commented code, unused imports
- [ ] No TODOs without implementation

⚠️ Each milestone must pass checklist before proceeding.

---

### 6. Proposed Test Coverage (≤250 tokens)

**Unit Tests:**
| Function | Scenarios | Reasoning |
|----------|-----------|-----------|
| {{func}} | {{cases}} | {{why}} |

**Edge Cases:**
- Empty input → {{behavior}}
- Invalid input → {{exception}}
- None handling → {{behavior}}

*Proposals. I will confirm before implementation.*

---

### 7. Interface & Requirements (≤250 tokens)

For key functions:

**Signature:**
```python
def do_something(input: InputType, config: Config) -> ResultType:
    """One-line description."""
    ...
```

**Requirements:**
- Input: [constraints, validation]
- Output: [guarantees]
- Behavior: [key logic]
- Errors: [exceptions, when raised]
- Edge cases: [specific handling]

*Signatures and prose. No implementation code.*

---

### 8. Risks (≤100 tokens)

| Risk | Impact | Mitigation |
|------|--------|------------|
| {{risk}} | H/M/L | {{action}} |

---

### 9. Open Questions & Assumptions (≤100 tokens)

**Questions:**
- {{unresolved}}

**Assumptions:**
- {{proceeding as if true}}

---

### 10. Estimate (≤50 tokens)

- Complexity: Simple / Moderate / Complex
- Effort: {{time}}
- Files: {{N}} create, {{M}} modify
- Tests: ~{{count}}

---

## CONDITIONAL SECTIONS

*Include only if applicable:*

### Observability — if production
- Logging: [events, levels]
- Metrics: [measurements]

### Security — if auth/PII/external input
- Validation: [requirements]
- Data handling: [approach]

### Async — if using asyncio
- Async operations: [which]
- Concurrency: [limits]

---

## STYLE REMINDERS

**Do:**
- Ask before assuming
- Minimal solutions only
- Prose requirements, not implementation code
- Reference actual codebase patterns

**Don't:**
- Add unrequested features
- Include full implementations
- Guess at requirements
- Skip the milestone checklist
