# CSS ↔ JavaScript Integration Rules

<priority_legend>

P0 = MUST follow; breaking this invalidates the request.  
P1 = SHOULD follow; deviations need an explicit rationale.  
P2 = CAN follow; use when helpful but optional.

</priority_legend>

<rules>

## CRITICAL
- R1 [P0] Separate state from style  
  JavaScript manages *logic and events*; CSS manages *presentation*.  
  Use classes or `data-*` attributes to express state transitions.

- R2 [P0] Prefer CSS variables and classes over inline styles  
  JS updates runtime values via custom properties (`--token`) or toggled classes.  
  Inline styles break the cascade and increase maintenance cost.

- R3 [P0] Animate with CSS, orchestrate with JS  
  Let CSS handle transitions/keyframes for `transform` and `opacity`.  
  JS should only trigger or cancel animations, not calculate frames.

- R4 [P0] Batch DOM reads and writes  
  Always read layout before writing styles.  
  Use `requestAnimationFrame`, `IntersectionObserver`, or `ResizeObserver` to avoid layout thrashing.

- R5 [P0] Keep state logic in JS, not computed styles  
  Never read CSS values to drive logic.  
  Persist UI state through attributes, classes, or ARIA properties.

- R6 [P0] Feature-detect, don’t sniff  
  Use `CSS.supports()` and `@supports()` for progressive enhancement.  
  Avoid UA or browser detection.

- R7 [P0] Respect user accessibility and motion settings  
  Honor `prefers-reduced-motion`, `prefers-color-scheme`, and ARIA state mapping.  
  JS must not override these preferences.

- R8 [P0] Synchronize initial render and hydration  
  Default HTML classes/attributes must match the initial JS state  
  to prevent FOUC (flash of unstyled content) and layout shift.

- R9 [P0] Treat dynamic CSS as untrusted  
  Sanitize user-derived style inputs.  
  Never inject unsanitized text into `<style>` or `cssText`; whitelist tokens or class names.

- R10 [P0] Coordinate naming and cascade across both layers  
  Maintain a single source of truth for class/tokens/z-index scales.  
  JS imports class maps (for CSS Modules) or references approved tokens;  
  CSS defines cascade layers predictably.

---

## RECOMMENDED PRACTICES
- R11 [P1] Expose design tokens through JS for theme switching and dynamic layouts.  
- R12 [P1] Use logical properties (`margin-inline`, `padding-block`) for RTL compatibility.  
- R13 [P1] Guard expensive animations with visibility checks before toggling classes.  
- R14 [P1] Document each CSS–JS contract (class, attribute, or variable)  
  in code comments or schema files.

</rules>
