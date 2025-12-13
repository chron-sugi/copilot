# Data Transform Spec Supplement

Use with Python Implementation Spec for data transformation work.
Adds data-specific sections. Does not replace standard spec sections.

---

## WHEN TO USE

Apply this supplement when building:
- Batch data processing
- ETL/ELT transforms
- Normalization or canonicalization
- Entity resolution or matching
- Data validation or cleansing
- Any work where "records in, records out" is the pattern

---

## DATA CONTEXT

### Flow
- **Source:** {{where data comes from - system, file, API, upstream stage}}
- **Sink:** {{where data goes - table, file, downstream stage, queue}}
- **Trigger:** {{scheduled, event-driven, manual, called by orchestrator}}

### Volume
- **Records per run:** {{expected count or range}}
- **Record size:** {{small, medium, large - or bytes}}
- **Memory considerations:** {{can load all in memory, needs streaming/chunking, use Polars lazy}}

### Schemas

**Input:**
```python
class InputRecord(BaseModel):
    """What we receive."""
    field: type
```

**Output:**
```python
class OutputRecord(BaseModel):
    """What we produce."""
    field: type
```

**Schema strictness:** {{strict (reject invalid), coerce (fix what we can), lenient (pass through unknown fields)}}

---

## ERROR HANDLING STRATEGY

Define behavior for each error type:

| Error Type | Strategy | Destination | Notes |
|------------|----------|-------------|-------|
| Validation failure | skip / fail / quarantine | {{log, error table, queue}} | {{when to use}} |
| Transform error | skip / fail / quarantine | {{log, error table, queue}} | {{when to use}} |
| Missing reference data | skip / fail / default | {{behavior}} | {{e.g., unknown OS}} |

### Thresholds
- **Max error rate:** {{percentage before aborting, or "none"}}
- **Max consecutive failures:** {{count before aborting, or "none"}}

### Error Output
```python
class ErrorRecord(BaseModel):
    """What we capture for failed records."""
    original_record: dict
    error_type: str
    error_message: str
    stage: str
    timestamp: datetime
```

---

## TRANSFORMATION LOGIC

### Steps

Describe each transformation step in order:

**Step 1: {{Name}}**
- Input: {{what it receives}}
- Output: {{what it produces}}
- Logic: {{what happens - prose, not code}}
- Validation: {{rules applied}}
- Errors: {{what can fail, how handled}}

**Step 2: {{Name}}**
- ...

### Business Rules
- {{rule 1 - plain language}}
- {{rule 2 - plain language}}
- {{rule 3 - plain language}}

### Edge Cases
| Scenario | Behavior |
|----------|----------|
| Empty input | {{return empty, error, skip}} |
| All records invalid | {{return empty, error with count}} |
| Duplicate records | {{keep first, keep last, merge, error}} |
| Null/missing fields | {{default value, skip record, error}} |
| {{domain-specific}} | {{behavior}} |

---

## IDEMPOTENCY

- **Can rerun safely:** yes / no
- **Duplicate detection:** {{how to identify already-processed records}}
- **On duplicate:** skip / update / error
- **State tracking:** {{none, checkpoint file, database marker, idempotency key}}

---

## DATA QUALITY

### Validation Rules

| Field | Rule | On Failure |
|-------|------|------------|
| {{field}} | {{constraint}} | {{reject, default, coerce}} |
| {{field}} | {{constraint}} | {{reject, default, coerce}} |

### Quality Metrics
- **Completeness:** {{fields that must be non-null}}
- **Validity:** {{fields with format/value constraints}}
- **Consistency:** {{cross-field rules}}
- **Match rate:** {{if doing matching/resolution - expected percentage}}

### Quality Outputs
```python
class QualityReport(BaseModel):
    """Produced with each run."""
    records_in: int
    records_out: int
    records_errored: int
    error_rate: float
    # domain-specific metrics
```

---

## OBSERVABILITY

### Logging
- **Record counts:** in, out, errored - at completion
- **Timing:** duration, records/second
- **Errors:** type, count, sample of failed records
- **Sampling:** {{log every Nth record for debugging, or "errors only"}}

### Metrics
- `records_processed_total`
- `records_errored_total` (by error type)
- `processing_duration_seconds`
- {{domain-specific: match_rate, confidence_distribution, etc.}}

### Alerting (if applicable)
- {{condition}} → {{action}}

---

## TESTING STRATEGY

### Unit Tests
- Individual transformation functions
- Validation rules
- Business logic edge cases

### Data Scenario Tests

| Scenario | Input | Expected Output |
|----------|-------|-----------------|
| Happy path | {{valid records}} | {{transformed records}} |
| Empty input | `[]` | `[]` or error |
| All invalid | {{invalid records}} | empty + error report |
| Mixed valid/invalid | {{mix}} | valid transformed + errors captured |
| Duplicates | {{duplicate records}} | {{per idempotency strategy}} |
| {{domain scenario}} | {{input}} | {{output}} |

### Fixtures Needed
- `valid_input_record` - typical good record
- `invalid_input_record` - fails validation
- `edge_case_record` - boundary conditions
- `batch_mixed` - realistic mix for integration tests

### Performance Tests (if applicable)
- {{N}} records completes in {{time}}
- Memory stays under {{limit}}

---

## INTERFACE REQUIREMENTS

**Main entry point:**

```python
def process_{{domain}}(
    records: list[InputRecord],
    config: ProcessingConfig,
) -> ProcessingResult:
    """One-line description."""
    ...
```

**Requirements:**
- Input: List of validated input records
- Output: ProcessingResult containing:
  - Successful outputs
  - Error records with context
  - Quality report
- Idempotent: {{yes/no}}
- Side effects: {{none, writes to X, updates Y}}

**Result structure:**
```python
class ProcessingResult(BaseModel):
    """What the transform returns."""
    outputs: list[OutputRecord]
    errors: list[ErrorRecord]
    quality: QualityReport
```

---

## POLARS-SPECIFIC (if applicable)

### Patterns
- Use lazy frames for large datasets
- Prefer expressions over apply/map
- Use `collect()` only when needed

### Memory Management
- Chunk size: {{if processing in chunks}}
- Streaming: {{if using streaming API}}

### Schema Handling
```python
INPUT_SCHEMA = {
    "field": pl.Utf8,
    "field": pl.Int64,
}
```

---

## CHECKLIST

Before considering transform complete:

- [ ] Input/output schemas defined and tested
- [ ] All error types have defined handling
- [ ] Edge cases documented and tested
- [ ] Quality report produced
- [ ] Idempotency behavior verified
- [ ] Performance acceptable at expected volume
- [ ] Observability in place (logs, metrics)