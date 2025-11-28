# Python Naming Standards (Agent Instructions)

Apply these rules whenever you create, rename, or reference Python files, modules, or symbols in this repo.

---

## 1. File Naming Conventions

- Use `snake_case` for all Python file names.
- Default pattern: keep names **descriptive and specific** (avoid `utils.py`, `helpers.py`, etc.).
- **Intentional redundancy for generic names**  
  - If a module name would otherwise be generic, **prefix it with the package name**:
    - `utils.py` ➜ `{package_name}_utils.py`
    - `helpers.py` ➜ `{package_name}_helpers.py`
  - This only applies to otherwise generic module names.

---

## 2. Data Structure / Domain Module Naming

Use the package name as a prefix for core data/logic modules:

- Models: `{package_name}_models.py`
- Domain logic: `{package_name}_domain.py`
- Rules / policies: `{package_name}_rules.py`
- Mappers / adapters (if needed): `{package_name}_mappers.py`, `{package_name}_adapters.py`

When adding new domain-level modules, follow the same pattern:
- `{package_name}_{clear_purpose}.py` (e.g. `catalog_matchers.py`, `catalog_normalizers.py`)

---

## 3. Package & Folder Naming

- Use `snake_case` for package and folder names.
- Avoid abbreviations unless they are **standard in the domain**.
- Prefer clarity for agents:
  - Good: `os_normalization`, `vendor_taxonomy`, `catalog_bootstrap`
  - Avoid: `osnorm`, `vendtax`, `cbstrap`

---

## 4. Symbol Naming (Classes, Functions, Variables, Constants)

Follow PEP 8 style:

- **Classes**: `PascalCase`  
  - Example: `OsCatalogEntry`, `VendorTaxonomyRegistry`
- **Functions & methods**: `snake_case`  
  - Example: `build_os_index()`, `apply_version_aliases()`
- **Variables**: `snake_case`  
  - Example: `canonical_name`, `normalized_tokens`
- **Constants**: `UPPER_SNAKE_CASE`  
  - Example: `DEFAULT_CONFIDENCE_THRESHOLD`, `LOG_DATE_FORMAT`
- **"Private" internals**: prefix with `_`  
  - Example: `_build_token_index()`, `_VERSION_ALIAS_PATTERN`

When choosing names:
- Prefer descriptive over clever (`resolve_os_name` > `resolve`).
- Avoid ambiguous short names except for idiomatic cases (`i`, `j` in small loops, etc.).

---

## 5. Test Naming Conventions

- Test files should be named to mirror the module under test:
  - `src/{package_name}/{module_name}.py`  
    ➜ `tests/{package_name}/test_{module_name}.py`
- Test functions:
  - Use `test_{unit_of_work}_{condition}` format:
    - Example: `test_resolve_os_name_handles_unknown_vendor()`

Do **not** invent new naming patterns for tests—mirror the target module and keep names explicit.

---

## 6. Logging Conventions

- Logger module location:  
  - `/src/{package_name}/observability/logger.py`
- Logger usage:
  - Always create loggers via `logging.getLogger(__name__)` in modules.
  - Do **not** configure the root logger in leaf modules; use the central logger configuration.
- Log file destination:
  - Send logs to `root/logs/` (or the configured logs root for the project).
- Logger names should remain hierarchical:
  - `"{package_name}.{module_name}"` derived from `__name__`.

---

## 7. Agent Behavior Rules

- When creating **new** files or symbols, **always conform** to these naming rules.
- When editing **existing** code that violates these rules:
  - Do **not** rename files or symbols unless explicitly instructed to refactor for naming consistency.
- If you must introduce a generic-sounding name, apply the appropriate `{package_name}_` prefix and make the purpose clear in the name.
