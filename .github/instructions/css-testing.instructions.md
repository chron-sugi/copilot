## TESTING & VALIDATION

- R91 [P1] Validate CSS using W3C CSS Validator or CSS linters (Stylelint) to catch syntax errors and enforce conventions.
- R2 [P0] Use a source
- R92 [P1] Test with real, variable-length content. Lorem ipsum hides layout issues with different text lengths, line wrapping, and overflow.
- R93 [P1] Check color contrast using automated tools (WebAIM Contrast Checker, Lighthouse) AND manual verification.
- R94 [P2] Test responsive designs at various viewport sizes, not just standard breakpoints. Content should work between breakpoints too.
- R95 [P2] Test with assistive technology: screen readers (NVDA, JAWS, VoiceOver), keyboard-only navigation, voice control.
- R96 [P2] Test both light and dark modes if implementing `prefers-color-scheme`. Ensure contrast ratios are maintained in both.