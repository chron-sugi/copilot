# Scripts

Development tools and utilities for this project.

## CSS Specificity Checker

A Python script that analyzes CSS selectors and calculates their specificity scores according to the W3C specification. Helps maintain low-specificity CSS following BEM methodology.

### Features

- ✅ Accurate W3C-compliant specificity calculation
- ✅ Analyzes entire CSS files or individual selectors
- ✅ Configurable specificity thresholds
- ✅ Handles complex selectors (`:not()`, `:is()`, `:where()`, pseudo-elements)
- ✅ JSON and text output formats
- ✅ Exit codes for CI/CD integration

### Usage

#### Analyze a CSS file
```bash
python scripts/css-specificity-checker.py path/to/styles.css
```

#### Analyze a single selector
```bash
python scripts/css-specificity-checker.py --selector "#nav .menu li a"
```

#### Set custom threshold
```bash
# Default is 0,1,3,3 (inline, IDs, classes, elements)
python scripts/css-specificity-checker.py styles.css --threshold "0,2,4,4"
```

#### JSON output (for tooling integration)
```bash
python scripts/css-specificity-checker.py styles.css --format json
```

### Specificity Format

Specificity is shown as `inline,ids,classes,elements`:

- `0,0,1,0` - `.button` (1 class)
- `0,1,0,0` - `#header` (1 ID)
- `0,1,2,1` - `#nav .menu .item a` (1 ID, 2 classes, 1 element)
- `1,0,0,0` - Inline styles (highest specificity)

### Examples

```bash
# Check if selectors follow BEM-style low specificity
python scripts/css-specificity-checker.py src/styles/main.css

# Stricter threshold for utility-first CSS
python scripts/css-specificity-checker.py styles.css --threshold "0,0,2,2"

# Quick test of a selector
python scripts/css-specificity-checker.py --selector ".btn.btn-primary:hover"
```

### Integration with CI/CD

Add to your workflow:

```yaml
# .github/workflows/css-quality.yml
- name: Check CSS Specificity
  run: python scripts/css-specificity-checker.py src/**/*.css
```

The script exits with code 1 if any selectors exceed the threshold.

### Default Threshold

The default threshold `0,1,3,3` is suitable for:
- BEM methodology
- Component-based CSS
- Modern CSS architectures

Selectors exceeding this are flagged as high specificity.

### Requirements

- Python 3.6+
- No external dependencies (uses standard library only)
