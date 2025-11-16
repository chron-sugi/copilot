<priority_legend>
P0=MUST follow; breaking this invalidates the request.
P1=SHOULD follow; deviations need an explicit rationale.
P2=CAN follow; use when helpful but optional.
</priority_legend>

<rules>

CRITICAL
C1  [P0] Enforce priorities: refuse to ship CSS that violates P0; if external constraints force it, stop and return a clear rationale.

C2  [P0] Ensure BEM (Block Element Modifier) naming conventions are followed:
  - Block: `.block`
  - Element: `.block__element`
  - Modifier: `.block--modifier`, `.block__element--modifier`

C3  [P0] Use CSS variables for all design tokens (color, spacing, radius, z-index, typography). Define in :root and theme scopes; don’t hardcode literals inside components.

C4  [P0] Set global sizing model: html { box-sizing: border-box } *, *::before, *::after { box-sizing: inherit }.

C5  [P0] Normalize once: include a single modern reset/normalize in a reset layer; never duplicate resets per component.

C6  [P0] Keep specificity at level 2 or below: prefer class selectors; avoid IDs and selector chains > 2 levels; use :where() to zero specificity when scoping helpers.

C7  [P0] Manage cascade with layers: declare order and place rules inside them: @layer reset, tokens, base, utilities, components, overrides;

C8  [P0] Accessibility: meet WCAG contrast (text ≥ 4.5:1; large text/UI ≥ 3:1); never remove focus styles—style :focus-visible instead.

C9  [P0] Respect motion preferences: gate non-essential animation behind @media (prefers-reduced-motion: reduce); keep essential transitions brief.

C10 [P0] Responsive by default: prefer Grid/Flex; avoid fixed widths; use clamp()/min()/max() for fluid type/spacing.

C11 [P0] Internationalization: use logical properties (margin-inline, padding-block, inset-inline) instead of left/right where possible.

C12 [P0] Prevent layout shift: reserve space for media via width/height or aspect-ratio; use object-fit appropriately.

C13 [P0] Component isolation: scope styles to components (BEM/SUIT or equivalent); avoid global descendant rules like .card p {…} outside component scope.

C14 [P0] Avoid !important: only allowed in documented utilities or last-resort overrides with rationale.

C15 [P0] Progressive enhancement: wrap modern features (:has, container queries, subgrid) in @supports and provide reasonable fallbacks.

C16 [P0] Robust font loading: always include fallback stacks and font-display: swap; declare only axes you use for variable fonts.

C17 [P0] Unit conventions: use rem for global scales, em for component-relative sizing, and px for borders/hairlines; don’t mix units arbitrarily.

C18 [P0] Z-index discipline: define a small tokenized scale (e.g., --z-modal, --z-popover); create stacking contexts intentionally (isolation: isolate when needed).

C19 [P0] Theming via tokens: implement dark/high-contrast themes by swapping token values (e.g., [data-theme="dark"] { --bg: … })—don’t duplicate component CSS.

C20 [P0] Respect user control: never disable zoom; constrain readable text width (≈ 45–85ch) using max-width.

## Domain Section — Architecture & Naming

C21 [P1] Use a consistent property order (e.g., box model → typography → visuals → interactions) or strict alphabetical—be consistent.

C22 [P2] Prefer multiple focused files that the bundler concatenates; avoid circular imports and redundant re-exports.

Domain Section — Tokens & Theming

C23 [P1] Define a complete token set: --color-*, --space-*, --size-*, --radius-*, --shadow-*, --z-*, --font-*.

C24 [P1] Map semantic tokens to raw tokens (e.g., --btn-bg: var(--color-primary-600)), and reference semantic tokens in components.

C25 [P2] Provide constrained utility classes generated from tokens (e.g., .p-4, .gap-2), limited to your approved scale.

Domain Section — Layout

C26 [P1] Use Grid for page/2D layout and Flex for 1D alignment; avoid floats/table layouts except for legacy content.

C27 [P1] Prefer container queries over viewport breakpoints when component width dictates behavior.

C28 [P2] Offer layout primitives (e.g., .stack, .cluster, .sidebar) to reduce bespoke CSS.

C29 [P1] Avoid magic numbers; derive sizes from tokens; leverage fr, auto-fit/auto-fill, and minmax() patterns.

Domain Section — Typography

C30 [P1] Build a typographic scale with clamp(); use unitless line-height and consistent rhythm.

C31 [P1] Limit to ≤ 3 font families and ≤ 4 weights where feasible; prefer variable fonts to reduce requests.

C32 [P2] Use ch for measure-sensitive widths and hyphens: auto for long words in body copy.

## Domain Section — States & Interactions

C33 [P1] Style :hover, :focus-visible, :active, :disabled, and ARIA states ([aria-pressed="true"], etc.); ensure touch-friendly targets.

C34 [P1] Hide visually without removing from accessibility tree using a .visually-hidden utility (clip/clip-path approach).

C35 [P2] Use :has() for parent-state styling gated by @supports (selector(:has(*))).

</rules>
