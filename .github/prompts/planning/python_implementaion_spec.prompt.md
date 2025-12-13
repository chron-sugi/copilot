# Python Implementation Spec Request

## ROLE & CONSTRAINTS

**Role:** Senior Python architect generating a minimal, actionable implementation spec  
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

## PYTHON CONVENTIONS

### Code Style
- Python 3.11+ features permitted (match statements, tomllib, etc.)
- Type hints required on all function/method signatures
- Type hints on variables only when not inferrable
- Google-style docstrings for public functions/classes
- No bare `except:` - always specify exception types
- Use `pathlib.Path` over `os.path`
- Use f-strings over `.format()` or `%`

### Data Modeling
- Pydantic v2 for external data validation (API inputs, config, file parsing)
- dataclasses for internal data structures (no validation needed)
- Avoid raw dicts for structured data - define models

### Project Structure
- Colocate related files: `{subpackage}_enums.py`, `{subpackage}_schemas.py`, `{subpackage}_service.py`
- Prefix filenames with subpackage name for searchability
- Keep modules focused - split when exceeding ~300 lines

### Imports
- Order: stdlib → third-party → local
- Absolute imports preferred
- No wildcard imports (`from x import *`)
- Remove unused imports before completing milestone

### Error Handling
- Custom exceptions inherit from a project base exception
- Raise specific exceptions, not generic `Exception`
- Include context in error messages
- Log errors with structured context before re-raising

### Testing (pytest)
- Test files: `tests/unit/{subpackage}/test_{module}.py`
- Test naming: `test_{unit}_{scenario}_{expected}`
- Use fixtures for reusable setup
- Parametrize for multiple input cases
- AAA pattern: Arrange, Act, Assert (with blank lines separating)
- One behavior per test
- Mock external dependencies only (databases, APIs, filesystem)
- No `time.sleep` in tests - mock time-dependent code

### Linting & Formatting
- Run `ruff check --fix` before completing milestone
- Run `ruff format` before completing milestone
- Type check with `mypy --strict` (or project's mypy config)
- Zero lint errors before milestone completion

---

## ASK ME FIRST

Before generating the spec, ask clarifying questions if:

- [ ] Requirements are ambiguous or conflicting
- [ ] Multiple valid approaches exist (ask which I prefer)
- [ ] Scope boundaries are unclear
- [ ] Uncertain about existing patterns or conventions
- [ ] Tempted to add something not explicitly requested
- [ ] Edge cases need business logic clarification
- [ ] Unclear whether to use Pydantic vs dataclass for a model

**Do not proceed with assumptions. Ask.**

---

## 🛑 STOP CONDITIONS (during implementation)

The coding agent should stop and ask if:

- Requirement becomes ambiguous during implementation
- Changes needed outside specified scope
- Test failures persist after 2 attempts
- Discovers conflicting patterns in codebase
- Tempted to add unspecified functionality
- Type errors that require architectural decisions to resolve

---

## FEATURE BRIEF

*Provide a natural language description. I will extract structure.*

**What I need:**
{{Describe the feature in plain language. What should it do? Why?}}

**Key behaviors that must work:**
{{List 2-5 critical behaviors in plain language}}

**What's out of scope:**
{{Anything explicitly excluded}}

**Constraints (if any):**
{{Performance, security, compatibility - or "none"}}

---

## CONTEXT

### Codebase Access
```
{{FILE_1}} — {{purpose}}
{{FILE_2}} — {{purpose}}
{{FILE_3}} — {{purpose}}
```

### Technical Environment
- Python version: {{3.11 / 3.12}}
- Key dependencies: {{pydantic, polars, etc.}}
- Test command: `pytest {{path}} -v`
- Lint command: `ruff check --fix && ruff format`
- Type check: `mypy {{path}}`
- Relevant patterns: {{reference files or "analyze codebase"}}

---

## OUTPUT FORMAT

### 1. Clarifying Questions (FIRST)

Before generating the spec, list any questions about:
- Ambiguous requirements
- Scope boundaries
- Approach preferences
- Edge case handling
- Model choices (Pydantic vs dataclass)

*If no questions, state "Requirements are clear" and proceed.*

---

### 2. Codebase Analysis (≤400 tokens)

Demonstrate understanding:
- Project structure and relevant patterns
- Existing models, services, utilities to reuse
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

### 4. Data Models (≤200 tokens)

Define models needed:

```python
# Pydantic - for external data (validation required)
class SomethingInput(BaseModel):
    """Docstring."""
    field: type

# dataclass - for internal data (no validation)
@dataclass
class SomethingInternal:
    """Docstring."""
    field: type
```

*Show fields and types. Note which are new vs modifications to existing.*

---

### 5. Milestones (≤900 tokens)

3–6 milestones. Keep minimal.

```
## Milestone N: [Name]

**What:** [Minimal changes to make]

**Where:** 
- `path/to/subpackage_module.py` — [change]

**Validation:** 
- Run: `pytest tests/unit/subpackage/test_module.py -v`
- Expect: [output]

**Proposed Tests:**
- [ ] test_function_scenario_expected
- [ ] test_function_edge_case_expected
```

*I will review proposed tests and adjust before implementation.*

**Before marking milestone complete:**
- Remove all debugging artifacts (print statements, logging for debug)
- Remove commented-out code
- Remove unused imports
- Run `ruff check --fix && ruff format`
- Run `mypy` - resolve type errors
- Verify no TODO comments without implementation

⚠️ Each milestone must pass validation and cleanup before proceeding.

---

### 6. Proposed Test Coverage (≤300 tokens)

Based on the requirements, propose:

**Unit Tests:**
| Function/Method | Test Cases | Why |
|-----------------|------------|-----|
| {{function}} | {{scenarios}} | {{reasoning}} |

**Fixtures Needed:**
- `fixture_name` — {{what it provides}}

**Edge Cases to Cover:**
- Empty input → {{expected behavior}}
- Invalid input → {{expected exception}}
- Boundary values → {{specific cases}}

**Parametrized Tests:**
```python
@pytest.mark.parametrize("input,expected", [
    (case1, result1),
    (case2, result2),
])
def test_something(input, expected): ...
```

*These are proposals. I will confirm before implementation.*

---

### 7. Interface Sketch (≤200 tokens)

Key function/class signatures:

```python
# In subpackage_service.py
def process_something(
    input_data: SomethingInput,
    config: Config,
) -> SomethingResult:
    """One-line description.
    
    Args:
        input_data: Description.
        config: Description.
    
    Returns:
        Description of result.
    
    Raises:
        SpecificError: When X happens.
    """
    ...
```

*Show interfaces, not implementations. Match existing project style.*

---

### 8. Risks (≤150 tokens)

| Risk | Impact | Mitigation |
|------|--------|------------|
| {{risk}} | H/M/L | {{action}} |

*Include only likely risks.*

---

### 9. Open Questions & Assumptions (≤150 tokens)

**Unresolved (need answers):**
- {{question}}

**Assumptions (will proceed as if true):**
- {{assumption}}

---

### 10. Estimate (≤100 tokens)

- Complexity: Simple / Moderate / Complex
- Effort: {{time}}
- Files: {{N}} create, {{M}} modify
- Tests: ~{{count}}
- Models: {{N}} Pydantic, {{M}} dataclass

---

## CONDITIONAL SECTIONS

*Include only if applicable:*

### Observability — if production feature
- Logging: [events, levels, structured fields]
- Metrics: [measurements]

### Security — if handles auth/PII/external input
- Input validation: [Pydantic validators]
- Sanitization: [approach]

### Async — if using asyncio
- Which operations are async
- Concurrency limits
- Error handling in async context

### Database — if data persistence
- Schema changes needed
- Migration approach
- Query patterns (ORM vs raw SQL)

---

## STYLE RULES

**Do:**
- Ask questions before assuming
- Propose minimal solutions
- Reference actual codebase patterns
- Use type hints everywhere
- Make milestones independently verifiable
- Suggest tests (I'll approve)
- Colocate related files with subpackage prefix

**Don't:**
- Add unrequested features or abstractions
- Over-engineer for hypothetical future needs
- Include multiple implementation options
- Speculate about requirements
- Exceed token budgets
- Leave commented-out code or debugging artifacts
- Create unused imports or empty placeholder files
- Add TODO comments without implementing
- Use `# type: ignore` without justification
- Use bare `except:` clauses
- Use mutable default arguments
- Use `print()` for logging

---

## PYTHON ANTI-PATTERNS TO AVOID

```python
# ❌ Don't
def bad(items=[]):  # mutable default
    ...

except:  # bare except
    pass

from module import *  # wildcard import

data = {"key": value}  # raw dict for structured data

# ✅ Do
def good(items: list[str] | None = None):
    items = items or []
    ...

except SpecificError as e:
    logger.error("Context", exc_info=e)
    raise

from module import specific_thing

data = MyModel(key=value)
```

---

## SUMMARY

Python-specific implementation spec emphasizing:
- Type hints everywhere
- Pydantic for validation, dataclasses for internal data
- Colocated files with subpackage prefixes
- pytest conventions with fixtures and parametrize
- ruff + mypy for linting/type checking
- Explicit cleanup requirements per milestone
- Python anti-patterns explicitly banned