# Instructions: Set Up and Validate Pipeline Metrics

You are an LLM coding agent and a senior data engineer collaborating on a data/ETL/pipeline project.

Your goal is to:
1. Understand how metrics are currently computed and logged.
2. Refactor or introduce **explicit metric computation functions** (if missing).
3. Create **automated validation tests** that prove those metrics are correct.
4. Keep the design **project-agnostic** so it can be reused across pipelines.

> BEFORE MAKING ANY CODE CHANGES:  
> - Pause and list any assumptions you are making.  
> - Ask the user any clarifying questions needed to resolve ambiguity about the metrics, the environment, or the expected behavior.

---

## 1. Understand the current environment and metrics

1. Locate the relevant code:
   - Search for folders or modules like: `observability`, `metrics`, `monitoring`, `logging`, or similar.
   - Search for logging calls or metric exports (e.g., `logger.info`, `logger.debug`, `metrics.`, `counter.`, `gauge.`, `histogram.`, etc.).
   - Identify any **metrics-specific modules** (e.g., `metrics.py`, `pipeline_metrics.py`, `observability/metrics_*`).

2. Build a quick inventory:
   - List each metric being produced, including:
     - Metric name / identifier.
     - What it is supposed to represent (in plain language).
     - The inputs used to compute it (tables, DataFrames, events, counts, etc.).
     - Where it is computed and where it is logged/exported.
   - Identify which metrics are:
     - **Run-level** (e.g., “total input rows”, “success/failure counts”).
     - **Step-level** (e.g., “rows after filtering”, “matches per source”).
     - **Performance-related** (e.g., “duration per stage”, “throughput”).

3. Ask the user:
   - To confirm which metrics are **critical** and must be validated.
   - Whether there are any **expected relationships/invariants** (e.g., “resolved + unresolved = total”, “consolidated <= resolved”).
   - Whether there are any **external metric sinks** (Prometheus, logs, data warehouse) that need to stay compatible with the current schema.

---

## 2. Separate metric computation from logging/export

Your objective is to make metric computation **testable and deterministic**.

1. For each important metric or metric group:
   - Identify the **current source** of truth: which function or part of the pipeline knows the relevant inputs.
   - If metrics are computed inline inside logging calls, plan to **extract that logic** into small, pure functions.

2. Create or refine metric computation functions:
   - Define clear, typed functions (or methods) like:

     - `compute_pipeline_run_metrics(...)`
     - `compute_stage_metrics(...)`
     - `compute_survivorship_metrics(...)`
     - `compute_catalog_bootstrap_metrics(...)`

   - These functions should:
     - Accept **inputs only** (e.g., DataFrames, lists, records, counts).
     - Return a structured metrics object (e.g., dataclass, dict, or typed model).
     - Contain **no logging, no I/O, no network calls**.

3. Update logging/export code:
   - Change logging/export lines to:
     - **Call the metric computation function**.
     - Log or export the returned structure.
   - Example pattern (pseudocode):

     - Compute metrics → `metrics = compute_*_metrics(...)`
     - Log/export metrics → `logger.info("pipeline_metrics", extra=metrics_as_dict)`

---

## 3. Define invariants and expected relationships

For each metric group, define what must **always be true**.

Examples (general patterns; adapt them to the project):

- Counts:
  - `total_input_rows == resolved_rows + unresolved_rows`
  - `sum(resolved_per_source.values()) == resolved_rows`
  - `processed_rows <= total_input_rows`
  - `failed_rows <= total_input_rows`

- Ratios:
  - `0.0 <= success_rate <= 1.0`
  - `0.0 <= error_rate <= 1.0`

- Structural:
  - No negative counts.
  - No NaN/None where a metric must be present.
  - Required keys exist in metric dicts (e.g., `{"total", "success", "failed"}`).

Create a **validation helper** to check these invariants, e.g.:

- `validate_pipeline_metrics(metrics)`
- `validate_stage_metrics(metrics)`

This helper should:
- Raise an error or assertion if an invariant is violated.
- Be suitable for use **both** in tests and optionally in runtime checks (e.g., with a toggle).

---

## 4. Design test strategy for metrics

Use a layered approach that works for any data pipeline:

### 4.1 Unit tests with synthetic data

Goal: Confirm metric computation logic is correct using small, explicit datasets.

1. For each metric computation function:
   - Create **tiny synthetic inputs** that are easy to reason about:
     - Example sizes: 3–20 rows or records.
     - Include edge cases: zero rows, all success, all failure, mixed states, multiple sources, etc.
   - Compute metrics using the synthetic inputs.

2. Write assertions:
   - Assert exact matches for counts and structures (e.g., dictionaries, arrays).
   - Assert invariants using the validation helper.

3. Avoid unnecessary mocks:
   - Use real in-memory data structures (e.g., DataFrames, lists, dicts).
   - Only mock external services or adapters, if any exist.

### 4.2 Integration tests with fixture data

Goal: Ensure that a **full pipeline or major segment** computes metrics correctly.

1. Create small but **realistic fixture data**:
   - Store fixtures in a standard test location (e.g., `tests/fixtures/`).
   - Fixtures can represent:
     - Input events/rows.
     - Intermediate tables (if needed).
     - Expected outputs or states.

2. Run the actual pipeline (or a well-bounded subset) in a test:
   - Capture the resulting metrics via the metric computation functions, not log output.
   - Compare against **expected “golden” metrics** that you pre-compute or document once.

3. Still apply invariants:
   - After computing metrics in the integration test, run the validation helper to ensure invariants hold.

### 4.3 Optional: validation on log payloads/exported metrics

If metrics are serialized (e.g., to JSON, logs, or an external metrics system):

1. Write tests that:
   - Parse the logged/exported metrics payload (e.g., from a helper, capture function, or in-memory sink).
   - Deserialize into a metrics object or dict.
   - Check that:
     - Required fields are present.
     - Types and shapes are correct.
     - Values match what the metric computation functions would produce.

2. Keep these tests focused on **data shape and compatibility**, not recalculating all business logic.

---

## 5. Implementation steps for the agent

When you implement this, follow this order:

1. **Discovery & questions**
   - Scan the codebase as described above.
   - Produce a short summary of:
     - Where metrics are defined.
     - Where they are computed.
     - Where they are logged/exported.
   - Identify any unclear or ambiguous metrics and **ask the user clarifying questions before proceeding**.

2. **Refactor (if needed)**
   - Introduce or refine pure metric computation functions.
   - Introduce a metrics validation helper enforcing invariants.
   - Update logging/export code to rely on these functions.

3. **Add tests**
   - Add unit tests for each metric computation function using synthetic data.
   - Add integration tests for key pipelines or stages with fixture data.
   - Optionally add tests for serialized/logged metrics shape.

4. **Wire into CI**
   - Ensure the new tests are automatically run as part of the existing test suite.
   - If appropriate, add a short note in the README or developer docs describing:
     - Where metric logic lives.
     - How metrics are tested.
     - How to add new metrics and their tests.

---

## 6. Communication and safety checks

Throughout the work:

- If you encounter:
  - Unclear metric definitions.
  - Conflicting logic in different components.
  - Metrics that don’t obey any obvious invariant.
- Then:
  - Stop and summarize what you found.
  - Ask the user targeted questions to clarify expected behavior.
  - Do **not** guess business meaning for metrics without confirmation.

Your final output should be:

- Clean, testable metric computation functions.
- A clear set of invariants and a validation helper.
- Unit and integration tests that demonstrate metric correctness.
- Minimal, well-structured changes to logging/export code that reuse the metric functions.