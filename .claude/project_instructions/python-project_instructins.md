# Python Development Instructions

Apply these conventions and guidelines when working on Python code in this project.

---

## Development Conventions

### Stack
- Python 3.11+
- Pydantic v2 for external data, dataclasses for internal
- pytest with fixtures and parametrize
- ruff for linting/formatting, mypy for type checking

### Typing
- Type hints on all function signatures
- `X | None`, not `Optional[X]`
- `collections.abc` types, not `typing` equivalents
- No `Any` without justification
- No `# type: ignore` without specific error code

### Pydantic
- Models for all structured data crossing function boundaries
- `field_validator` for single fields, `model_validator` for cross-field
- `pydantic-settings` for configuration
- `frozen=True` when mutation isn't needed
- Never v1 syntax

### Function Design
- Single responsibility
- Early returns, not deep nesting
- No `**kwargs` unless decorators/wrappers
- Under ~50 lines; split when larger
- Dependencies as parameters, not global state
- Return types over exceptions for expected cases (`User | None` over `UserNotFoundError`)

### Naming
- Verbose, semantic names over abbreviations
- Functions: `verb_noun` (`get_user_by_id`, `process_records`)
- Variables: descriptive, no single letters except loop indices

### Error Handling
- No bare `except:` — catch specific exceptions
- Domain exceptions inherit from project base exception
- Include context in error messages
- Let Pydantic's `ValidationError` propagate

### File Organization
- Prefix common filenames with subpackage:
  - `{subpackage}_enums.py`, `{subpackage}_models.py`, `{subpackage}_schemas.py`
  - `{subpackage}_constants.py`, `{subpackage}_exceptions.py`, `{subpackage}_utils.py`
- One concept per file when practical
- Modules under ~300 lines
- Export public interfaces in `__init__.py`

### Documentation
- Google-style docstrings for public functions/classes
- Skip docstrings for obvious one-liners and private helpers
- Don't restate type hints in docstrings

### Quality Gates
Before completing any task:
- Remove debugging artifacts, commented code, unused imports
- `ruff check --fix && ruff format`
- `mypy` clean
- No TODOs without implementation

### Behavior
- Minimal solution only — no unrequested features
- No "just in case" abstractions
- Ask before assuming on ambiguous requirements

---

## Code Review Guidelines

When reviewing code, evaluate against these criteria.

### Severity Levels
- **🔴 Must Fix:** Bugs, security issues, missing tests, type errors
- **🟡 Should Fix:** Design problems, unclear names, missing edge cases
- **🟢 Consider:** Minor improvements, optional

### Review Checklist
- Type hints complete, `X | None` not `Optional[X]`
- Pydantic for external data, no raw dicts crossing boundaries
- Descriptive names, no magic values
- No bare `except:`, errors handled explicitly
- Edge cases covered (empty, None, invalid input)
- New/changed code has tests
- No hardcoded secrets, sensitive data not logged

### Don't Comment On
- Formatting (ruff handles this)
- Code outside changed files
- Personal preferences without clear improvement

### Output Structure
```markdown
## Summary
[1-2 sentences]

## 🔴 Must Fix
[Findings or "None"]

## 🟡 Should Fix
[Findings or "None"]

## 🟢 Consider
[Findings or "None"]
```

---

## Debugging Approach

When fixing bugs, follow this methodology.

### Before Editing
1. See the failure — run or read failing test/stack trace
2. Read stack trace bottom-up; crash site ≠ bug site
3. Trace data flow upstream — where did the bad value originate?
4. State one-sentence root-cause hypothesis before patching

### Principles
- Fix causes, not symptoms
- Smallest safe change only
- Don't add defensive code that obscures invariants
- Tests are ground truth — never weaken assertions

### Process
- Outline planned changes before editing
- Run fix — never present untested patches
- After 2 unsuccessful attempts, stop and ask for guidance

### Don't
- Fix symptoms at crash site without tracing root cause
- Add `if x is not None` checks without understanding why x is None
- Silence errors with `except: pass`
- Guess when information is missing — ask instead

---

## Testing Guidelines

When creating or evaluating tests.

### Structure
```
tests/
├── conftest.py
├── unit/{subpackage}/test_{module}.py
├── integration/test_{feature}.py
└── e2e/test_{workflow}.py
```

### Test Naming
`test_{unit}_{scenario}_{expected}`

### AAA Pattern
```python
def test_process_valid_item_returns_result():
    # Arrange
    item = create_item()
    
    # Act
    result = process(item)
    
    # Assert
    assert result.status == Status.COMPLETE
```

### Principles
- Test behavior, not implementation
- Every test needs meaningful assertions
- Each test independent — no shared mutable state
- One behavior per test

### Edge Cases to Cover
- Empty input, None, single item
- Boundary values (0, -1, max)
- Invalid types, unicode, whitespace
- Error paths

### Fixtures
- Use for reusable test data, not one-off setup
- Name descriptively: `valid_queue_item`, `empty_batch`
- Place shared fixtures in `conftest.py`
- Don't over-fixture simple cases

### Mocking
- Mock external dependencies only (HTTP, DB, filesystem)
- Don't mock the unit under test
- Don't mock internal helpers or pure transformations

### Coverage Analysis
```bash
pytest --cov=src --cov-report=term-missing
```

Analyze semantic coverage, not just lines:
- All branches exercised?
- Edge cases covered?
- Error paths tested?

---

## Data Transform Context

When building data processing (ETL, normalization, entity resolution).

### Additional Concerns
- Define input/output schemas explicitly
- Specify error handling per error type (skip/fail/quarantine)
- Consider idempotency — can it rerun safely?
- Track quality metrics (records in/out, error rate)

### Error Handling Strategy

| Error Type | Options |
|------------|---------|
| Validation failure | skip / fail / quarantine |
| Transform error | skip / fail / quarantine |
| Missing reference | skip / fail / default |

Define thresholds: max error rate before aborting.

### Edge Cases for Data Work
- Empty batch
- All records invalid
- All records valid
- Mixed valid/invalid
- Duplicates
- Threshold boundaries

---

## When Unsure

Ask clarifying questions before proceeding. Don't guess at:
- Requirements or scope
- Architecture decisions
- Business logic
- Edge case handling

Asking is always preferable to assuming.