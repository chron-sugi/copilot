# FROM GPT 

Use BEM
- Keep specificity at 1 (single class). Maximum 2 for pseudo-classes only.
CSS Authoring Rules for Code Agents



 



## Domain Section — Performance

R38 [P1] Minimize unused CSS (purge/tree-shake safely); avoid costly selectors (*, deep :not() chains).

R39 [P1] Animate only transform and opacity; apply will-change sparingly and clean it up.

R40 [P2] Inline critical CSS for initial paint; code-split route-specific CSS for SPAs/MPAs.

Domain Section — Compatibility & Testing

R41 [P1] Use Autoprefixer with a documented browserslist; verify features via @supports/Can I Use; provide fallbacks.

R42 [P1] Lint with Stylelint and run visual regression tests; block merges on P0 violations.

R43 [P2] Provide print styles (@page margins; hide navigation/chrome).

Domain Section — Documentation & Delivery

R44 [P1] Start each file with a header comment noting its layer, role, and ownership; link to token source.

R45 [P1] When deviating from P1/P0, annotate with /* rationale: … (owner, date) */.

R46 [P2] Generate a style inventory page (colors, type scale, spacing) for QA and design review.

Domain Section — CSS-in-JS / Frameworks

R47 [P1] Even with CSS-in-JS or utility frameworks, enforce tokens and accessibility; don’t hardcode ad‑hoc values.

R48 [P2] In CSS Modules, export intent-revealing class names (component role), not purely presentational names.

</rules>




-Code should be self-documenting and easy to modify.

-Use BEM (Block Element Modifier) naming:<example>
  - Block: `.card`
  - Element: `.card__title`, `.card__image`
  - Modifier: `.card--featured`, `.card__title--large`</example>

-Keep specificity below 2 <example>
  - ✅ `.button`, `.card__header`
  - ✅ `.button--primary`, `.nav__link--active`
  - ❌ `.header .nav .link` (specificity: 3)
  - ❌ `div.container > ul li` (specificity: 3)
  </example>

**Avoid IDs for styling.** Use classes exclusively.

**Avoid nesting selectors.** Flat class names are more maintainable.

**Use CSS custom properties** for theming and repeated values:
```css
.button {
  background: var(--color-primary);
  padding: var(--spacing-sm);
}
```

## HTML Guidelines

**Write semantic HTML:**
- Use `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<footer>`
- Use `<button>` for actions, `<a>` for navigation
- Use proper heading hierarchy (`<h1>` to `<h6>`)

**Keep markup clean:**
- Avoid unnecessary wrapper divs
- Use BEM classes directly on semantic elements
- Add data attributes for JavaScript hooks: `data-action="submit"`

## JavaScript Guidelines

**Use modern ES6+ syntax:**
- Arrow functions, destructuring, template literals
- `const` and `let` (never `var`)
- Array methods: `.map()`, `.filter()`, `.reduce()`

**Separate concerns:**


**Write small, focused functions.** Each function should do one thing well.

## File Organization

```
styles/
  base/         - resets, typography, variables
  components/   - reusable UI components
  layouts/      - page structure
  utilities/    - helper classes

scripts/
  components/   - component logic
  utils/        - helper functions
```

## Development Workflow

1. **Start with HTML structure** using semantic elements and BEM classes
2. **Add base styles** with CSS custom properties for consistency
3. **Build components** one at a time with focused styles
4. **Add interactivity** with vanilla JavaScript or framework as needed
5. **Test responsively** at mobile, tablet, and desktop breakpoints

## Quick Reference

**BEM Pattern:**
```html
<div class="card card--featured">
  <h2 class="card__title">Title</h2>
  <p class="card__text">Content</p>
  <button class="card__button card__button--primary">Action</button>
</div>
```

**Low Specificity Styles:**
```css
.card { /* specificity: 1 */ }
.card--featured { /* specificity: 1 */ }
.card__title { /* specificity: 1 */ }
```

**Avoid:**
```css
.card .card__title { /* specificity: 2 - unnecessary */ }
.featured.card { /* specificity: 2 - use modifier instead */ }
```
