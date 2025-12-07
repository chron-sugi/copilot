

# CSS/Tailwind Code Review

## Purpose

Review the styling implementation of a feature or component to identify issues that harm readability and maintainability for LLM coding agents. Produce actionable recommendations to make styles more predictable, traceable, and safe to modify.

## Core Principle

The ideal styling implementation allows an agent to:

1. Find the styles affecting a component by searching class names
2. Understand what a style does by reading it in isolation
3. Predict the full impact of a change before making it
4. Modify styles confidently without unintended side effects

Review against these criteria.

---

## Review Checklist

### 1. Co-location

**Goal:** Styles should live with or near the components they affect.

Review for:

- Styles defined in distant global files that could be co-located
- Component-specific styles buried in shared stylesheets
- Overrides in global CSS that exist only to fix one component

**Recommendations should address:**

- Moving component-specific styles into component files or adjacent CSS modules
- Eliminating distance between style definition and usage

---

### 2. Traceability

**Goal:** Given a class name in markup, an agent should find its definition via simple search.

Review for:

- Dynamically constructed class names (`btn-${variant}`, template literals)
- Generic class names that match too many results (`.container`, `.wrapper`, `.item`)
- Classes applied via runtime logic that obscures the source (`cn()`, `clsx()` with complex conditions)

**Recommendations should address:**

- Replacing dynamic construction with explicit class lists where possible
- Renaming generic classes with component-scoped prefixes
- Simplifying conditional class logic or adding comments listing possible values

---

### 3. Specificity

**Goal:** Styles should win by being the right style, not by being more specific.

Review for:

- Selectors beyond single class (`.parent .child`, `.foo.bar`, element selectors)
- ID selectors
- `!important` declarations
- Specificity escalation patterns (increasingly specific selectors to override earlier rules)

**Recommendations should address:**

- Flattening nested selectors to single classes
- Removing `!important` by fixing the underlying specificity conflict
- Refactoring override chains into single-source-of-truth styles

---

### 4. Tailwind Consistency

**Goal:** If using Tailwind, use it consistently. Mixed approaches create unpredictability.

Review for:

- Custom CSS that duplicates what Tailwind utilities provide
- `@apply` usage (often a sign of working against Tailwind's model)
- Tailwind utilities overridden by custom CSS
- Arbitrary values (`[32px]`) that should be theme tokens
- Inconsistent approaches across similar components

**Recommendations should address:**

- Replacing custom CSS with equivalent Tailwind utilities
- Converting `@apply` blocks to direct utility usage or extracting to proper components
- Extending Tailwind config for repeated arbitrary values
- Standardizing the styling approach across the feature

---

### 5. Inheritance & Implicit Dependencies

**Goal:** A component's appearance should be understood from its own code.

Review for:

- Styles that only work because of inherited properties from ancestors
- Reliance on CSS reset or base layer styles that aren't obvious
- Components that break when moved to a different DOM context
- CSS custom properties used without clear indication of where they're defined

**Recommendations should address:**

- Making inherited assumptions explicit (add the class/utility directly)
- Documenting or co-locating CSS variable definitions
- Adding comments when context-dependent styling is intentional

---

### 6. Change Radius

**Goal:** Modifying a style should have predictable, limited impact.

Review for:

- Utility classes or global styles shared across many components
- Styles that affect children via descendant selectors
- Single class names that serve multiple unrelated purposes
- No clear boundary between "this component's styles" and "shared styles"

**Recommendations should address:**

- Splitting shared classes into component-scoped versions where purposes diverge
- Replacing descendant selectors with explicit classes on target elements
- Documenting intentionally shared styles and their dependents

---

### 7. Explicitness

**Goal:** The reason for each style should be apparent from local context.

Review for:

- Magic numbers without explanation (`margin-top: 37px`)
- Styles that exist only to counteract other styles (negative margins fixing layout issues)
- Non-obvious z-index values
- Styles with no clear purpose or that appear to be dead code

**Recommendations should address:**

- Replacing magic numbers with theme tokens or adding explanatory comments
- Refactoring "fix" styles by addressing the root cause
- Establishing z-index scale in theme config
- Removing dead styles (verify unused first)

---

## Review Output Format

### Summary

Brief overview (2-3 sentences) of the overall styling health and the most significant issues.

### Issues

For each issue found:

```
#### [Issue Title]

**Location:** [file:line or file + selector/class]
**Category:** [Co-location | Traceability | Specificity | Tailwind Consistency | Inheritance | Change Radius | Explicitness]
**Impact:** [How this harms agent readability/maintainability]
**Recommendation:** [Specific action to resolve]
```

### Positive Patterns

Note any exemplary practices worth preserving or extending to other areas.

---

## Example Review Output

### Summary

This component uses Tailwind utilities well for spacing and typography but has accumulated several global overrides that create hidden dependencies. The main risks are two unscoped class names and a specificity conflict requiring `!important`.

### Issues

#### Generic `.card` class name

**Location:** `globals.css:45`, used in `FeatureCard.tsx:12`
**Category:** Traceability
**Impact:** Searching for `.card` returns 34 results across the codebase. An agent cannot determine which styles apply without manual verification.
**Recommendation:** Rename to `.feature-card` or migrate to Tailwind utilities. If shared intentionally, document in a comment which components use it.

#### Specificity override chain

**Location:** `globals.css:89-94`
**Category:** Specificity
**Impact:** `.sidebar .card` overrides `.card`, then `.sidebar .card.active` overrides that. An agent modifying card styles cannot predict which selector will win in which context.
**Recommendation:** Flatten to single classes: `.sidebar-card` and `.sidebar-card-active`. Apply directly in markup rather than relying on ancestor context.

#### `!important` on box-shadow

**Location:** `FeatureCard.module.css:23`
**Category:** Specificity
**Impact:** Indicates a specificity conflict exists elsewhere. Agent cannot safely add shadow utilities—they will lose.
**Recommendation:** Trace what this overrides (likely `.card` in globals), resolve by removing the global shadow or increasing locality, then remove `!important`.

#### Arbitrary Tailwind value repeated

**Location:** `FeatureCard.tsx:8, 14, 22` — `p-[18px]` appears 3 times
**Category:** Tailwind Consistency
**Impact:** Magic number not tied to design system. If spacing changes, agent must find all instances.
**Recommendation:** Add `18` (or `4.5` as `1.125rem`) to Tailwind spacing scale in config, then use `p-4.5` or similar.

### Positive Patterns

- Typography is handled entirely through Tailwind utilities with consistent scale usage
- Component-specific hover states are co-located in the component file
- CSS custom properties for colors are well-organized in `theme.css` with clear naming