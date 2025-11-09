# CSS Debugging Reference

> **Purpose:** Comprehensive reference for CSS debugging techniques, common issues, and modern DevTools features
> **Last Updated:** 2025-01-08

---

## Table of Contents

1. [Common Culprits](#common-culprits)
2. [Modern DevTools Features](#modern-devtools-features)
3. [Debugging Techniques](#debugging-techniques)
4. [Debugging Workflow Examples](#debugging-workflow-examples)

---

## Common Culprits

Quick reference guide for the most frequent CSS bugs and their symptoms.

### Container Query Issues

**Symptom**: Component doesn't respond to container size changes

**Common Causes**:
- ❌ **Missing `container-type`**: Parent element lacks `container-type: inline-size;` declaration
- ❌ **Container too small**: Container query condition never met (container smaller than breakpoint)
- ❌ **Wrong container name**: `@container (name: foo)` references non-existent or misspelled container-name
- ❌ **Browser support**: Container queries require Chrome 105+, Safari 16+, Firefox 110+

**Debugging**:
```css
/* Check parent has container-type */
.parent {
  container-type: inline-size; /* Required! */
  container-name: card; /* Optional but recommended */
}

/* Check condition actually fires */
@container card (min-width: 400px) {
  .child { /* ... */ }
}
```

**DevTools**: Use Chrome's Container Query visualizer to see container boundaries.

---

### Token Inheritance Issues

**Symptom**: CSS custom properties showing fallback values or `initial`

**Common Causes**:
- ❌ **Token not defined**: Custom property never declared in current scope
- ❌ **Shadow DOM boundary**: Token defined outside shadow root, not accessible inside
- ❌ **iframe isolation**: Token defined in parent document, not in iframe
- ❌ **Theme not applied**: `[data-theme]` attribute missing on `<html>` or ancestor
- ❌ **Typo in var()**: `var(--color-primery)` instead of `var(--color-primary)`
- ❌ **Build process override**: Fallback literal in `var(--token, #fff)` silently replacing token

**Debugging**:
```javascript
// Trace custom property resolution
const el = document.querySelector('.c-button');
const computed = getComputedStyle(el);

// Check if token resolves
console.log(computed.getPropertyValue('--color-primary')); // Should show value, not empty

// Check where token is defined
console.log(computed.getPropertyValue('--color-primary')); // Inherited or local?
```

**DevTools**: Chrome's Computed tab shows inherited custom properties with their source.

---

### Specificity Conflicts

**Symptom**: Your CSS rule exists but doesn't apply; another rule wins

**Common Causes**:
- ❌ **Third-party CSS**: Library with higher specificity overriding your styles
- ❌ **Unlayered styles**: Styles outside `@layer` beat ALL layered styles (regardless of specificity)
- ❌ **`!important` in earlier layer**: In `@layer`, `!important` works REVERSE (earlier layers win)
- ❌ **Inline styles**: `style=""` attribute has highest specificity (1,0,0,0)
- ❌ **Specificity creep**: Overly-specific selectors (e.g., `0,3,1` beating intended `0,1,0`)

**Debugging**:
```css
/* Check layer order */
@layer reset, base, components, utilities; /* Earlier = lower priority */

/* In layers, !important reverses priority */
@layer base {
  button { color: red !important; } /* This WINS over... */
}

@layer components {
  .c-button { color: blue !important; } /* ...this, surprisingly! */
}

/* Use :where() to zero out specificity */
:where(.c-button) {
  /* Specificity: 0,0,0 - easily overridden */
}
```

**Specificity values**:
- ID: `1,0,0` (avoid in components)
- Class/attribute/pseudo-class: `0,1,0` (target for components)
- Element: `0,0,1`
- `:where()`: `0,0,0` (always)
- `:is()`, `:not()`: Takes highest specificity from list

**DevTools**: Chrome shows specificity on hover (2024+ feature).

---

### State/Variant Mismatches

**Symptom**: Component doesn't change appearance when state/variant changes

**Common Causes**:
- ❌ **Misspelled attribute**: `data-varient="primary"` instead of `data-variant="primary"`
- ❌ **Wrong element**: Attribute on child instead of parent (or vice versa)
- ❌ **JavaScript not updating DOM**: State change logic broken, attribute never applied
- ❌ **Multiple conflicting variants**: Both `data-variant="primary"` and `data-variant="secondary"` on same element
- ❌ **CSS selector mismatch**: Code expects `data-size="large"` but JS sets `data-size="lg"`

**Debugging**:
```html
<!-- Check attributes in DevTools Elements panel -->
<button
  class="c-button"
  data-variant="primary"  <!-- Check spelling! -->
  data-size="md"          <!-- Check value matches CSS! -->
  data-state="loading"    <!-- Check attribute exists! -->
>
  Click me
</button>
```

```css
/* Check selector matches exactly */
.c-button[data-variant="primary"] { /* Must match HTML exactly */ }
.c-button[data-size="md"] { /* Case-sensitive! */ }
```

**DevTools**: Use Elements panel → Properties tab to see all data-* attributes.

---

### Browser/Feature Support

**Symptom**: Works in Chrome, broken in Safari/Firefox

**Common Causes**:
- ❌ **Container queries**: Not supported in Safari < 16, Firefox < 110 (as of 2024: ~93% support)
- ❌ **CSS nesting**: Requires Safari 16.5+, may need transpilation
- ❌ **`@layer`**: Requires Safari 15.4+, Chrome 99+, Firefox 97+ (~95% support)
- ❌ **`@property`**: Requires Chrome 85+, Safari 16.4+ (~85% support)
- ❌ **`:has()` pseudo-class**: Safari 15.4+, Chrome 105+ (~90% support)
- ❌ **Missing vendor prefixes**: Should use Autoprefixer, don't hand-write prefixes

**Debugging**:
```css
/* Check feature support */
@supports (container-type: inline-size) {
  /* Container query styles */
}

@supports not (container-type: inline-size) {
  /* Fallback for older browsers */
}
```

**Resources**:
- [Can I Use](https://caniuse.com/) - Browser support tables
- [MDN Browser Compatibility Data](https://github.com/mdn/browser-compat-data)

---

## Modern DevTools Features (2024-2025)

### Chrome DevTools

**Specificity Hover** (Chrome 117+):
- Hover over any selector in Styles panel
- Shows specificity value (e.g., `(0,1,0)`)
- Compare multiple selectors to see which wins

**@layer Visualization** (Chrome 99+):
- Styles panel shows which `@layer` a rule belongs to
- Click to jump to layer definition
- See layer cascade order

**CSS Nesting Support** (Chrome 112+):
- Properly displays nested selectors
- Shows flattened selector on hover
- Preserves nesting in editable styles

**Container Query Inspector** (Chrome 105+):
- Visual overlay showing container boundaries
- Hover container to see query conditions
- Shows which queries are active
- Container size displayed in overlay

**Forced Colors Emulation** (Chrome 96+):
- Rendering tab → Emulate CSS media feature
- Test `forced-colors: active` mode
- Preview high-contrast system themes

**CSS Overview Panel** (Chrome 88+):
- Analyze unused styles
- Color palette extraction
- Font usage analysis
- Media queries summary

---

### Firefox DevTools

**Inactive CSS Indicators** (Firefox 70+):
- Grayed-out properties that have no effect
- Tooltip explains WHY property is inactive
- Example: `align-items` on non-flex/grid container

**Grid/Flexbox Inspector** (Firefox 65+):
- Visual overlays for layout debugging
- Shows grid lines, gaps, areas
- Flexbox alignment visualization
- Toggle overlays on/off per element

**Accessibility Inspector** (Firefox 61+):
- Check color contrast ratios
- Verify focus order
- ARIA attribute validation
- Keyboard navigation simulation

**Fonts Panel** (Firefox 63+):
- Shows all fonts on page
- Font rendering details
- Variable font controls
- Font feature inspection

---

### Safari Web Inspector

**CSS Changes Timeline** (Safari 13.1+):
- Track what CSS changed and when
- See JavaScript-triggered style changes
- Replay style modifications

**Responsive Design Mode** (Safari 13+):
- Test at various device sizes
- Simulate touch events
- Device orientation testing
- User agent spoofing

**Audit Tab** (Safari 13+):
- Accessibility checks
- Performance audits
- Best practices validation

**Layers Panel** (Safari 13.1+):
- Visualize paint layers
- Identify composite layers
- Optimize layer performance

---

### Common DevTools Workflows

#### 1. Identify Winning Rule
```
1. Right-click element → Inspect
2. Styles panel → See applied styles (not crossed out)
3. Computed tab → See final computed values
4. Look for specificity conflicts, layer overrides
```

#### 2. Debug Custom Properties
```
1. Inspect element
2. Computed tab → Filter: "color" (or property name)
3. Expand computed property to see var() resolution
4. Console: getComputedStyle(el).getPropertyValue('--token')
```

#### 3. Test Responsive Behavior
```
1. Toggle device toolbar (Cmd/Ctrl + Shift + M)
2. Select device or enter custom dimensions
3. Test container queries vs media queries
4. Use container query visualizer (Chrome)
```

#### 4. Compare Specificity
```
1. Hover over selector in Styles panel (Chrome)
2. Note specificity value
3. Compare with other rules targeting same element
4. Use :where() to reduce if needed
```

---

## Debugging Techniques

### 1. Isolation

**Goal**: Remove everything unrelated to narrow down the problem

**Techniques**:

**Binary search / Bisection**:
```css
/* Comment out half the CSS */
/* @import 'components.css'; */
/* @import 'utilities.css'; */

/* Does bug still occur? */
/* If yes, problem is in remaining half */
/* If no, problem is in commented half */
/* Repeat until you find the culprit */
```

**Minimal reproduction**:
```html
<!-- Simplest HTML that reproduces bug -->
<!DOCTYPE html>
<style>
  /* Only CSS needed to reproduce bug */
</style>
<body>
  <!-- Minimal markup -->
</body>
```

**Remove unrelated code**:
- Strip animations, transitions
- Remove pseudo-elements
- Eliminate JavaScript
- Use simple content (no images, icons)

---

### 2. Simplification

**Goal**: Reduce complexity until the issue becomes obvious

**Techniques**:

**Flatten selectors**:
```css
/* Complex (hard to debug) */
.parent .child > .grandchild:nth-child(2) { }

/* Simplified (easier to reason about) */
.grandchild-variant { }
```

**Hard-code values**:
```css
/* Using tokens (might have resolution issue) */
background: var(--color-primary);

/* Hard-coded (tests if token is the problem) */
background: #2563eb;
```

**Remove nesting**:
```scss
/* Nested (hard to see cascade) */
.parent {
  .child {
    .grandchild { color: red; }
  }
}

/* Flattened (easier to debug) */
.parent .child .grandchild { color: red; }
```

---

### 3. Comparison

**Goal**: Understand what's different between working and broken states

**Techniques**:

**Side-by-side comparison**:
```
Working component          Broken component
<button                vs  <button
  class="c-button"         class="c-button"
  data-variant="primary"   data-variant="primary"
  data-size="md"           data-size="lg"  ← Only difference!
>                        >
```

**Cross-browser comparison**:
- Works in Chrome? → Test in Safari
- Works in Firefox? → Test in Edge
- Difference found? → Check browser support tables

**Version comparison (git bisect)**:
```bash
# Find which commit broke it
git bisect start
git bisect bad HEAD        # Current (broken) version
git bisect good v1.2.3     # Last known working version
# Git will check out commits for you to test
```

---

### 4. Systematic Elimination

**Goal**: Change one thing at a time, observe results

**Approach**:

```
1. Document current state (screenshot, DevTools values)
2. Make ONE small change
3. Test if bug still occurs
4. If bug fixed → You found the cause!
5. If bug persists → Undo change, try something else
6. Keep notes on what you tried
```

**Example**:
```
Test 1: Remove data-variant → Bug persists ✗
Test 2: Remove data-size → Bug persists ✗
Test 3: Change container width → Bug FIXED! ✓
Conclusion: Container query condition was too high
```

---

### 5. CSS-Specific Techniques

**Force states in DevTools**:
```
1. Inspect element
2. Styles panel → :hov button
3. Check: :hover, :focus, :active, :visited
4. See styles that only apply in those states
```

**Custom property tracing**:
```javascript
// Trace where token is defined
const el = document.querySelector('.c-button');
const styles = getComputedStyle(el);

console.log(styles.getPropertyValue('--color-primary')); // Final value
console.log(styles.getPropertyValue('color')); // Computed value using token
```

**Layer isolation**:
```css
/* Comment out layers one at a time */
/* @layer reset { ... } */
@layer base { ... }
@layer components { ... }
/* @layer utilities { ... } */

/* Does bug still occur? Which layer caused it? */
```

**Specificity debugging with :where()**:
```css
/* Temporarily zero out specificity to test if that's the issue */
:where(.c-button[data-variant="primary"]) {
  /* Specificity: 0,0,0 */
  /* If this rule now applies, specificity was the problem */
}
```

**Cascade visualization**:
```
Chrome DevTools → Styles panel → See crossed-out rules
Look for:
- Which rules are overridden?
- What's doing the overriding?
- What's the specificity difference?
- Is it a layer issue?
```

---

## Debugging Workflow Examples

### Example 1: Button Not Showing Primary Color

**Symptom**: Button with `data-variant="primary"` shows gray instead of blue

**Systematic Triage**:

1. **Inspect element** → Class is `c-button`, layer is `components`
2. **Computed tab** → `background-color: rgb(229, 231, 235)` (gray)
3. **Styles tab** → Look for `data-variant="primary"` selector
4. **Find selector**: `.c-button[data-variant="primary"]` exists but is crossed out
5. **See override**: `.c-button[data-state="disabled"]` is winning
6. **Root cause**: Element has BOTH `data-variant="primary"` AND `data-state="disabled"`

**Fix**: Remove conflicting `data-state`, or adjust CSS to handle both:
```css
/* Fix: Make variant win when both present */
.c-button[data-variant="primary"]:not([data-state="disabled"]) {
  background: var(--color-primary);
}
```

---

### Example 2: Container Query Not Firing

**Symptom**: Component doesn't change layout when container resizes

**Systematic Triage**:

1. **Check parent has container-type**:
   ```css
   .card-container {
     container-type: inline-size; /* ✓ Present */
   }
   ```

2. **Check query condition**:
   ```css
   @container (min-width: 600px) { /* Breakpoint */ }
   ```

3. **Measure actual container width** → DevTools shows 400px
4. **Root cause**: Container too narrow (400px < 600px)

**Fix**: Lower breakpoint or make container wider
```css
@container (min-width: 400px) { /* Adjusted */ }
```

---

### Example 3: Theme Not Applying

**Symptom**: Dark theme styles not showing when `data-theme="dark"` is set

**Systematic Triage**:

1. **Check HTML** → `<html data-theme="dark">` ✓ Present
2. **Check CSS**:
   ```css
   [data-theme="dark"] {
     --color-primary: var(--palette-blue-400);
   }
   ```
3. **Test token resolution**:
   ```javascript
   getComputedStyle(document.documentElement)
     .getPropertyValue('--color-primary')
   // Returns: '' (empty!) ✗
   ```
4. **Root cause**: `--palette-blue-400` not defined!

**Fix**: Define palette token or use literal value:
```css
:root {
  --palette-blue-400: #60a5fa; /* Add missing palette token */
}
```

---

**Related Resources**:
- [CSS Debugger Chat Mode](../chatmodes/css/css-debugger.chatmode.md)
- [CSS Core Standards](../instructions/css.instructions.md)
- [Chrome DevTools CSS Documentation](https://developer.chrome.com/docs/devtools/css/)
- [Firefox DevTools CSS Documentation](https://firefox-source-docs.mozilla.org/devtools-user/page_inspector/how_to/examine_and_edit_css/)
