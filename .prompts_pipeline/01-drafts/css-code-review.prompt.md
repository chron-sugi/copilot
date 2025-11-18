---
name: CSSCodeReview
description: 'Perform a comprehensive CSS code review based on modern best practices, accessibility standards, and maintainability guidelines.'
agent: FrontEndCodeReviewer
model: GPT-5
---
version: 1.0
---
Your output must be concise, high-signal, and strictly under 4000 tokens.

## 1. Review Objectives (P0 – MUST)**

The review must:

1. **Verify correctness:** selectors, cascade, layers, structure.  
2. **Enforce accessibility:** WCAG 2.2 AA (contrast, focus, reduced motion, target size).  
3. **Validate design tokens:** no literals; semantic tokens only.  
4. **Check responsiveness:** logical properties, container queries, viewport-unit pitfalls.  
5. **Evaluate performance:** expensive properties, animations, paint/layout triggers.  
6. **Check cross-browser:** Safari/Firefox behaviors, fallbacks, `@supports`.  
7. **Check maintainability:** specificity discipline, nesting limits, state/variant consistency.  
8. **Identify missing tests:** a11y, Storybook variants, forced-colors, reduced-motion, regression.  
9. **Evaluate risks:** classify all issues by severity (Critical/High/Medium/Low).  

---

## 2. Core Standards (P0 – MUST)**

#### 2.1 Specificity & Selectors**
- Default: **≤ (0,1,1)**; avoid IDs; avoid `!important` (utilities only).  
- Limit CSS nesting to **≤3 levels**; avoid nested selectors that inflate specificity.  
- Use `:where()` for zero-specificity scopes.  
- Use `:has()` only inside components; avoid global anchors (`body:has(...)`).  

---

#### 2.2 Tokens & Custom Properties**
- Use **semantic tokens** (e.g., `--color-primary`) not palette tokens.  
- No magic literals (colors, radii, spacing).  
- Prefer **OKLCH** and `color-mix()` with documented fallbacks.  
- Use **typed custom properties** with `@property` when animating.  

---

#### 2.3 Accessibility (WCAG 2.2 AA)**
- **Contrast**: text ≥ 4.5:1; large text ≥ 3:1; UI ≥ 3:1.  
- **Focus**: must meet WCAG 2.4.13 “Focus Appearance” and **not be obscured**:  
  - Use `:focus-visible`  
  - Use `scroll-padding` / `scroll-margin` to prevent hidden focus.  
- **Reduced motion:** respect `prefers-reduced-motion`; disable motion-heavy effects.  
- **Forced colors:** use system colors; prefer `forced-color-adjust:auto`.  
- **Target size:** **≥ 24×24 CSS px (WCAG)**. Platform guidance:  
  - iOS ≥ 44×44  
  - Material ≥ 48×48  

---

#### 2.4 Responsiveness**
- Logical properties only: `margin-inline-start`, not `margin-left`.  
- Use **container queries** for component-level breakpoints.  
- Guard with: `@supports (container-type: inline-size)` and provide defaults.  
- Prefer **modern viewport units**: `dvh`, `svh`, `lvh`.  
- Use container units (`cqw`, `cqh`) when appropriate.  

---

#### 2.5 Cascade Layers**
- **All component CSS MUST be inside a layer.**  
- **Unlayered CSS overrides all layered CSS regardless of order.**  
- Recommended order:  
  ```
  @layer reset, base, tokens, theme, components, utilities, overrides;
  ```

---

#### 2.6 Performance**
- Use `content-visibility: auto` + `contain-intrinsic-size` for large areas.  
- Animate only `transform` and `opacity`.  
- Avoid: `backdrop-filter`, complex `filter`, large `box-shadow`.  
- Use `will-change` sparingly and remove when done.  

---

#### 2.7 Cross-Browser**
- Use project-wide **Browserslist**; avoid `last 2 versions`.  
- Add `@supports` fallbacks for `@property`, nesting, container queries.  
- Document Safari/Firefox quirks when relevant.  

---

#### 2.8 Variants & Component API**
- Use `data-*` attributes for **visual variants** only.  
- Use **ARIA/native attributes** for **state** (`disabled`, `aria-pressed`).  
- Base class must remain stable.  
- Avoid compound classes (`.btn-primary-large-disabled`).  

---

## 3. Output Format (P0 – MUST)**

Produce output in this exact structure:

## Summary
[DECISION: APPROVE | REQUEST CHANGES | BLOCK] — Risk: LOW/MEDIUM/HIGH/CRITICAL

## Findings

### [Category] — [Severity]
- ❌ file.css:L12 — issue description
- ⚠️ file.css:L48 — issue description
- ✅ Passing check description

## Suggested Changes
**file.css:L12**
```diff
- old code
+ new code
```

## Missing Tests
- [ ] Accessibility (contrast, focus, reduced-motion)
- [ ] Forced colors / high contrast
- [ ] Container query variants
- [ ] Storybook stories (states, sizes, themes)
- [ ] Visual regression coverage

## Merge Readiness
[Decision with rationale and required steps]

---

## 4. Severity Rules (P0 – MUST)**

- **CRITICAL 🔴** – a11y failures, focus obscured, breaking layouts, unlayered overrides.  
- **HIGH 🟠** – missing tokens, invalid responsiveness, perf hazards, unsafe selectors.  
- **MEDIUM 🟡** – missing docs/tests, non‑optimal patterns.  
- **LOW 🟢** – refactor/cleanup suggestions.  

---

## 5. Common LLM Failure Modes (avoid & correct)**

- Removing outlines without compliant focus styles.  
- Using physical properties like `margin-left`.  
- Overusing `!important`.  
- Adding global `:has()` selectors.  
- Hardcoded `100vh` mobile layouts.  
- Unlayered overrides.  
- Animating layout properties.  

---

## 6. Final Instruction**

**Perform a full CSS code review using these standards.  
Return only the structured report.**
