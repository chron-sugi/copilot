# CSS Development Rules for AI Code Agents

<priority_legend>

P0=MUST follow; breaking this invalidates the request.
P1=SHOULD follow; deviations need an explicit rationale.
P2=CAN follow; use when helpful but optional.

</priority_legend>

<rules>

## CRITICAL

- R1 [P0] Use `box-sizing: border-box` globally. Set on `:root` or `html` element with universal inheritance to make width/height calculations predictable (padding and border included in dimensions).
- R2 [P0] Never use `!important` except for utility classes or critical overrides. It indicates a specificity problem that should be fixed at the architecture level.
- R3 [P0] Keep selector specificity as low as possible. Start with single classes and increase only when necessary. Avoid ID selectors for styling.

- R5 [P0] Never remove focus outlines without providing an alternative visible focus indicator with minimum 3:1 contrast ratio against both focused and unfocused states.
- R6 [P0] Meet WCAG AA minimum contrast ratios: 4.5:1 for normal text, 3:1 for large text (18pt+/14pt bold+) and UI components.
- R7 [P0] Always respect `prefers-reduced-motion` media query. Users with vestibular disorders, migraines, or ADHD can be harmed by animations. Example:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```
- R8 [P0] Never use `display: none` or `visibility: hidden` for screen-reader-only content. Use absolute positioning pattern instead:
```css
.sr-only {
  position: absolute;
  left: -10000px;
  width: 1px;
  height: 1px;
  overflow: hidden;
}
```
- R9 [P0] Never use placeholder attributes as substitutes for labels. Placeholders disappear on focus, fail contrast requirements, and are not reliably accessible.
- R10 [P0] Never disable zoom with `maximum-scale=1` or `user-scalable=no` in viewport meta tag. This violates WCAG 2.1 Success Criterion 1.4.4.
- R11 [P0] Place standard CSS properties after vendor-prefixed versions. The standard property must take precedence when browsers support it:
```css
.element {
  -webkit-transform: rotate(45deg);
  transform: rotate(45deg);
}
```
- R12 [P0] Avoid magic numbers. Use CSS custom properties with semantic names for numeric values that appear disconnected from their context.

## ACCESSIBILITY

- R13 [P1] Aim for WCAG AAA contrast ratios for critical content: 7:1 for normal text, 4.5:1 for large text.
- R14 [P1] Never rely solely on color to convey information. Supplement with icons, text labels, patterns, or other visual indicators.
- R15 [P1] Make focus indicators prominent with minimum 2px thickness. Consider using `:focus-visible` to show focus only for keyboard navigation while hiding for mouse clicks.
- R16 [P1] Ensure interactive elements have minimum 44x44px touch targets for mobile accessibility compliance.
- R17 [P1] Style all form input states explicitly: default, :hover, :focus, :disabled, :invalid, :valid, :required.
- R18 [P2] Implement `prefers-color-scheme` support for light/dark modes. Benefits users with light sensitivity, migraines, and low vision needs. Use semantic color custom properties that change per scheme:
```css
:root {
  --color-text: #000;
  --color-background: #fff;
}
@media (prefers-color-scheme: dark) {
  :root {
    --color-text: #fff;
    --color-background: #000;
  }
}
```
- R19 [P2] Never include critical information in `::before` or `::after` pseudo-element content. Screen readers may not reliably announce it.
- R20 [P2] Apply `scroll-behavior: smooth` only when users accept motion:
```css
@media (prefers-reduced-motion: no-preference) {
  html { scroll-behavior: smooth; }
}
```
- R21 [P2] Ensure placeholder text meets 4.5:1 contrast minimum. Default browser placeholders often fail WCAG requirements.

## LAYOUT & POSITIONING

- R22 [P1] Use CSS Grid for two-dimensional layouts where you control both rows and columns (page structure, dashboards, galleries).
- R23 [P1] Use Flexbox for one-dimensional layouts in a single row or column (navigation bars, component alignment, content distribution).
- R24 [P1] Combine Grid for macro layouts (page structure) and Flexbox for micro layouts (component internals).
- R25 [P1] Understand that stacking contexts are isolated. Elements inside a stacking context can never appear above elements in a parent stacking context regardless of z-index value.
- R26 [P1] Know what creates stacking contexts: positioned elements with z-index ≠ auto, opacity < 1, transform, filter, will-change, isolation: isolate, and many others.
- R27 [P1] Use `isolation: isolate` to explicitly create stacking contexts and prevent z-index from affecting outside elements.
- R28 [P1] Remember z-index only works on positioned elements (position ≠ static) or flex/grid items.
- R29 [P2] Reserve absolute positioning for overlays, tooltips, popovers, and dropdowns. Use Grid/Flexbox for primary layouts.
- R30 [P2] Use container queries (`@container`) for component-based responsive design where components respond to their container size, not viewport size.
- R31 [P2] Leverage `:has()` pseudo-class for parent selection and conditional styling based on child state.

## PERFORMANCE

- R32 [P1] Only animate `transform` and `opacity` properties. These are GPU-accelerated and don't trigger layout or paint.
- R33 [P1] Never animate layout properties (`width`, `height`, `margin`, `padding`, `top`, `left`, `right`, `bottom`). They cause expensive reflows.
- R34 [P1] Use `will-change` sparingly and only during the animation lifecycle. Overuse creates memory overhead:
```css
.element:hover {
  will-change: transform;
}
.element {
  will-change: auto;
}
```
- R35 [P2] Prefer CSS animations over JavaScript for simple animations. They run on the compositor thread when animating transform/opacity.
- R36 [P2] Minimize descendant selector depth. Browsers read selectors right-to-left, so `.nav ul li a` is less efficient than `.nav-link`.
- R37 [P2] Prefer simple class selectors over complex attribute or pseudo-class combinations for better performance.
- R38 [P2] Use the `contain` property to isolate element layout, style, paint, or size from the rest of the document for rendering optimization.
- R39 [P2] Inline critical above-the-fold CSS to improve First Contentful Paint. Defer non-critical CSS with async loading or media attributes.
- R40 [P2] Use `content-visibility: auto` on long content sections to defer rendering of off-screen content.

## RESPONSIVE DESIGN

- R41 [P1] Design mobile-first with progressive enhancement. Use `min-width` media queries to add complexity for larger screens.
- R42 [P1] Use relative units for scalable layouts: `rem` for font sizes (respects user preferences), `em` for component-scoped spacing, `%` for widths, `vh/vw` for viewport sizing. Reserve `px` for borders and precise small values.
- R43 [P1] Set base font-size on `:root` (typically 16px) so `rem` units scale predictably from a single source.
- R44 [P1] Use logical breakpoints based on content needs, not device sizes. Common breakpoints: 480px (small phones), 768px (tablets), 1024px (small desktops), 1280px (large desktops).
- R45 [P1] Set explicit `aspect-ratio` on images and videos to prevent cumulative layout shift during page load.
- R46 [P2] Use `clamp()` for fluid typography that scales between defined minimum and maximum sizes:
```css
font-size: clamp(1rem, 2.5vw, 2rem);
/* min: 1rem, preferred: 2.5% of viewport width, max: 2rem */
```
- R47 [P2] Combine `aspect-ratio` with `object-fit` for responsive images that maintain proportions:
```css
img {
  aspect-ratio: 16 / 9;
  width: 100%;
  object-fit: cover; /* fills space, crops if needed */
}
```
- R48 [P2] Use `object-fit: cover` for thumbnails/hero images where filling space is prioritized. Use `object-fit: contain` when the entire image must be visible.
- R49 [P2] Implement fluid spacing that scales between breakpoints using `clamp()`, viewport units, or calc() for harmonious responsive layouts.

## MAINTAINABILITY

- R50 [P1] Use consistent naming methodology throughout the project (BEM, SMACSS, or custom convention). Document the chosen approach.
- R51 [P1] Use semantic, purpose-based class names that describe function, not appearance: `.error-message` not `.red-text`, `.primary-button` not `.blue-button`.
- R52 [P1] Group related styles together. Keep component styles co-located.
- R53 [P1] Use CSS custom properties for theme values, repeated values, and magic numbers:
```css
:root {
  --color-primary: #007bff;
  --spacing-unit: 8px;
  --border-radius-default: 4px;
}
```
- R54 [P1] Define custom properties at appropriate scope: `:root` for global themes, component root for component-specific values.
- R55 [P1] Use unitless `line-height` values to prevent compounding in nested elements: `line-height: 1.5` not `line-height: 1.5em`.
- R56 [P2] Follow consistent property ordering: positioning, display/box model, typography, visual (colors/borders), transforms/animations. Use Stylelint to enforce.
- R57 [P2] Write one selector per line for better readability and cleaner git diffs.
- R58 [P2] Provide fallback values for custom properties in case they're undefined:
```css
color: var(--custom-color, #000000);
```
- R59 [P2] Document complex selectors, browser-specific hacks, and unavoidable magic numbers with comments explaining why they exist.
- R60 [P2] Use section headers to organize CSS files into logical groups (layout, typography, components, utilities).

## BROWSER COMPATIBILITY

- R61 [P1] Provide fallbacks for modern CSS features using `@supports` feature queries:
```css
.grid {
  display: flex; /* fallback */
}
@supports (display: grid) {
  .grid {
    display: grid;
  }
}
```
- R62 [P1] Use PostCSS Autoprefixer instead of manually writing vendor prefixes. Configure browserslist to define target browser support.
- R63 [P1] Test in target browsers. Don't assume cross-browser compatibility without verification.
- R64 [P2] Consider graceful degradation where core functionality works everywhere but enhancements appear in modern browsers.
- R65 [P2] Check Can I Use (caniuse.com) for property browser support before using cutting-edge features.
- R66 [P2] Use logical properties (`margin-inline-start` instead of `margin-left`) for better internationalization and RTL language support.

## FORMS & INPUTS

- R67 [P1] Ensure labels are properly associated with inputs using `for`/`id` attributes. Visual proximity alone is insufficient for accessibility.
- R68 [P1] Style validation feedback clearly using color PLUS text/icons for accessibility (not color alone).
- R69 [P1] Make form inputs visually distinct in all states. Users must easily identify which field is focused, which have errors, and which are disabled.
- R70 [P2] Use `:invalid` and `:valid` pseudo-classes for real-time validation styling, but avoid showing validation before user interaction.
- R71 [P2] Consider using `:user-invalid` (modern browsers) to show validation only after user has interacted with the field.
- R72 [P2] Style autofilled inputs appropriately. Browser default autofill styles may clash with your design:
```css
input:-webkit-autofill {
  -webkit-box-shadow: 0 0 0 1000px white inset;
}
```

## MODERN CSS FEATURES

- R73 [P2] Use cascade layers (`@layer`) to organize styles with explicit precedence order without specificity wars:
```css
@layer base, components, utilities;
@layer base { /* lowest priority */ }
@layer utilities { /* highest priority */ }
```
- R74 [P2] Leverage container queries for truly component-based responsive design where components adapt to their container:
```css
@container (min-width: 400px) {
  .card { display: grid; }
}
```
- R75 [P2] Use `:has()` for powerful conditional styling based on descendant state:
```css
.form:has(:invalid) { border-color: red; }
```
- R76 [P2] Consider `color-mix()` for dynamic color manipulation without preprocessors:
```css
background: color-mix(in srgb, var(--primary) 80%, white);
```
- R77 [P2] Use `:is()` and `:where()` for grouping selectors. `:is()` takes highest specificity of arguments, `:where()` has zero specificity.
- R78 [P2] Implement View Transitions API for smooth, performant page/state transitions in single-page applications.

## COMMON PITFALLS

- R79 [P1] Understand margin collapse: vertical margins between adjacent siblings/parent-child collapse to the larger value.
- R80 [P1] Remember that percentage heights require parent to have explicit height. `height: 100%` fails if parent height is `auto`.
- R81 [P1] Don't use pixels for font sizes. It prevents user scaling and violates accessibility. Use `rem` or `em` instead.
- R82 [P1] Understand that `em` units compound in nested elements. Prefer `rem` for consistency unless component-scoped scaling is desired.
- R83 [P1] Remember `position: fixed` is positioned relative to viewport, not parent (except when parent has `transform`, `filter`, or `perspective`).
- R84 [P2] Avoid overly specific selectors that are hard to override: `.sidebar .nav ul li a` is less maintainable than `.nav-link`.
- R85 [P2] Don't use inline styles. They have high specificity (only `!important` overrides), are hard to maintain, and bypass style organization.
- R86 [P2] Floats remove elements from document flow. Parent containers won't contain floated children without clearfix or using modern layout methods.

## PRINT STYLES

- R87 [P2] Create print-specific styles in `@media print` queries to optimize content for printing.
- R88 [P2] Hide non-printable elements in print styles: navigation, ads, video players, interactive widgets.
- R89 [P2] Use `page-break-inside: avoid` on tables, figures, and blockquotes to prevent awkward breaks across pages.
- R90 [P2] Include URL references for links in print:
```css
@media print {
  a[href]:after {
    content: " (" attr(href) ")";
  }
}
```



</rules>
