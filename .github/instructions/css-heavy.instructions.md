CSS Authoring Rules for Code Agents

<priority_legend>

P0=MUST follow; breaking this invalidates the request.
P1=SHOULD follow; deviations need an explicit rationale.
P2=CAN follow; use when helpful but optional.

</priority_legend>

<rules>
CRITICAL

R1 [P0] Enforce priorities (copilot instruction): refuse to ship CSS that violates P0; if external constraints force it, stop and return a clear rationale. For P1 deviations, add a /* rationale: … */ comment.

R2 [P0] Use CSS variables for all design tokens (color, spacing, radius, z-index, typography). Define in :root and theme scopes; don’t hardcode literals inside components. 

R3 [P0] Set global sizing model: html { box-sizing: border-box } * , *::before, *::after { box-sizing: inherit }.

R4 [P0] Normalize once: include a single modern reset/normalize in a reset layer; never duplicate resets per component.

R5 [P0] Keep specificity low: prefer class selectors; avoid IDs and selector chains > 2 levels; use :where() to zero specificity when scoping helpers.

R6 [P0] Manage cascade with layers: declare order and place rules inside them:
@layer reset, tokens, base, utilities, components, overrides;

R7 [P0] Accessibility: meet WCAG contrast (text ≥ 4.5:1; large text/UI ≥ 3:1); never remove focus styles—style :focus-visible instead.

R8 [P0] Respect motion preferences: gate non-essential animation behind @media (prefers-reduced-motion: reduce); keep essential transitions brief.

R9 [P0] Responsive by default: prefer Grid/Flex; avoid fixed widths; use clamp()/min()/max() for fluid type/spacing.

R10 [P0] Internationalization: use logical properties (margin-inline, padding-block, inset-inline) instead of left/right where possible.

R11 [P0] Prevent layout shift: reserve space for media via width/height or aspect-ratio; use object-fit appropriately.

R12 [P0] Component isolation: scope styles to components (BEM/SUIT or equivalent); avoid global descendant rules like .card p {…} outside component scope.

R13 [P0] Avoid !important: only allowed in documented utilities or last-resort overrides with rationale.

R14 [P0] Progressive enhancement: wrap modern features (:has, container queries, subgrid) in @supports and provide reasonable fallbacks.

R15 [P0] Robust font loading: always include fallback stacks and font-display: swap; declare only axes you use for variable fonts.

R16 [P0] Unit conventions: use rem for global scales, em for component-relative sizing, and px for borders/hairlines; don’t mix units arbitrarily.

R17 [P0] Z-index discipline: define a small tokenized scale (e.g., --z-modal, --z-popover); create stacking contexts intentionally (isolation: isolate when needed).

R18 [P0] Theming via tokens: implement dark/high-contrast themes by swapping token values (e.g., [data-theme="dark"] { --bg: … })—don’t duplicate component CSS.

R19 [P0] Respect user control: never disable zoom; constrain readable text width (≈ 45–85ch) using max-width.

Domain Section — Architecture & Naming

R20 [P1] Pick one naming scheme (BEM, SUIT, utility-first) and apply it consistently across the codebase.

R21 [P1] Namespace app classes (e.g., .app- or .c-) to avoid collisions with third-party styles.

R22 [P2] Co-locate a component’s CSS with its implementation; expose one entry file per component.

R23 [P1] Use a consistent property order (e.g., box model → typography → visuals → interactions) or strict alphabetical—be consistent.

R24 [P2] Prefer multiple focused files that the bundler concatenates; avoid circular imports and redundant re-exports.

Domain Section — Tokens & Theming

R25 [P1] Define a complete token set: --color-*, --space-*, --size-*, --radius-*, --shadow-*, --z-*, --font-*.

R26 [P1] Map semantic tokens to raw tokens (e.g., --btn-bg: var(--color-primary-600)), and reference semantic tokens in components.

R27 [P2] Provide constrained utility classes generated from tokens (e.g., .p-4, .gap-2), limited to your approved scale.

Domain Section — Layout

R28 [P1] Use Grid for page/2D layout and Flex for 1D alignment; avoid floats/table layouts except for legacy content.

R29 [P1] Prefer container queries over viewport breakpoints when component width dictates behavior.

R30 [P2] Offer layout primitives (e.g., .stack, .cluster, .sidebar) to reduce bespoke CSS.

R31 [P1] Avoid magic numbers; derive sizes from tokens; leverage fr, auto-fit/auto-fill, and minmax() patterns.

Domain Section — Typography

R32 [P1] Build a typographic scale with clamp(); use unitless line-height and consistent rhythm.

R33 [P1] Limit to ≤ 3 font families and ≤ 4 weights where feasible; prefer variable fonts to reduce requests.

R34 [P2] Use ch for measure-sensitive widths and hyphens: auto for long words in body copy.

Domain Section — States & Interactions

R35 [P1] Style :hover, :focus-visible, :active, :disabled, and ARIA states ([aria-pressed="true"], etc.); ensure touch-friendly targets.

R36 [P1] Hide visually without removing from accessibility tree using a .visually-hidden utility (clip/clip-path approach).

R37 [P2] Use :has() for parent-state styling gated by @supports (selector(:has(*))).

Domain Section — Performance

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