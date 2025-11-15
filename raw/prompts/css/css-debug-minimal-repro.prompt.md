---
description: "Generate minimal reproducible CSS bug scenario"
mode: 'ask'
tools: ['codebase']
---

# Minimal Reproducible Bug Generator

Create a minimal reproduction case for: **${input:bugDescription}**

---

## Context

**Bug summary**: ${input:bugDescription}

**Affected component**: ${input:componentName:Unknown}

**Browser/version**: ${input:browser:Chrome/Firefox/Safari}

**Current complexity**: ${input:currentComplexity:Full application with many components}

---

## Requirements

Generate the **simplest possible** HTML + CSS that reproduces the bug.

### Goals

1. **Minimal HTML**: Fewest elements needed to show the issue
2. **Minimal CSS**: Only styles directly related to the bug
3. **No dependencies**: No frameworks, libraries, or build tools
4. **Self-contained**: Copy-paste into CodePen/JSFiddle and it works

### What to Remove

- ❌ JavaScript (unless bug requires JS to trigger)
- ❌ Unrelated components
- ❌ Complex layouts
- ❌ Animations and transitions
- ❌ Icons, images, real content
- ❌ Framework-specific syntax
- ❌ Build tool dependencies (Sass, PostCSS)

### What to Keep

- ✅ Component structure (classes, data-attributes)
- ✅ CSS rules that affect the bug
- ✅ Minimal states/variants showing the issue
- ✅ Container context (if container queries involved)
- ✅ Theme context (if theming involved)

---

## Output Format

Generate a complete, copy-paste-ready HTML file:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bug Reproduction: ${input:bugDescription}</title>
  <style>
    /* ===================================
       MINIMAL CSS TO REPRODUCE BUG
       =================================== */

    /* Reset (if needed for bug) */
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    /* Container (if needed) */

    /* Component styles */

    /* State/variant that shows bug */

  </style>
</head>
<body>
  <!-- ===================================
       MINIMAL HTML TO REPRODUCE BUG
       =================================== -->

  <!-- Component markup -->

  <!-- Note: This is the SIMPLEST structure that shows the bug -->
</body>
</html>
```

---

## Documentation to Include

After the HTML, provide:

### Expected Behavior
**What SHOULD happen**: [Clear description]

### Actual Behavior
**What ACTUALLY happens**: [Clear description]

### Steps to Reproduce
1. [First step]
2. [Second step]
3. [Third step]

### Environment
- **Browser**: ${input:browser}
- **OS**: ${input:os:Windows/macOS/Linux}
- **Viewport**: ${input:viewport:Desktop/Mobile}

### Additional Notes
- Any browser-specific details
- Any timing/interaction requirements
- Screenshots or screen recording links (if provided)

---

## Validation Checklist

Before submitting, verify:

- [ ] Code is copy-paste ready (no placeholders)
- [ ] Minimal (removed all non-essential code)
- [ ] Self-contained (no external dependencies)
- [ ] Bug reproduces consistently
- [ ] Expected vs actual behavior documented
- [ ] Browser/environment specified

---

## Example Output Structure

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    .container {
      container-type: inline-size;
      width: 500px;
    }

    .card {
      padding: 1rem;
      background: lightblue;
    }

    /* Bug: This never fires even though container is 500px wide */
    @container (min-width: 400px) {
      .card {
        background: lightcoral; /* Should be coral, stays lightblue */
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="card">Card content</div>
  </div>
</body>
</html>
```

**Expected**: Card background should be coral (container is 500px)
**Actual**: Card background stays lightblue
**Browser**: Chrome 120

---

**Related**:
- [CSS Debugging Reference](../../docs/css-debugging-reference.md)
- [CSS Debugger Mode](../../chatmodes/css/css-debugger.chatmode.md)
