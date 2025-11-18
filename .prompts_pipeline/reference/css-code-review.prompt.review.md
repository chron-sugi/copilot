## Summary
REQUEST CHANGES — Risk: MEDIUM

## Findings

### Prompt Structure — Medium
- ⚠️ L1-L9: Missing environment/runtime context (OS, build tooling, browser support scope) reduces precision for cross-browser and performance review.
- ⚠️ L9: Token limit ("under 4000 tokens") conflicts with internal reviewer mode guideline (<3000). Potential mismatch may cause overlong outputs.
- ⚠️ L104-L129: Output spec lacks instruction to summarize aggregated severity counts (e.g., number of CRITICAL/HIGH). Adds manual effort post-review.
- ⚠️ L104-L129: No directive to include a self-check or assumptions section when code context is partial.
- ⚠️ L154-L157: Final instruction omits grounding clause (e.g., "Only evaluate provided CSS files; do not infer absent code"). Risk of hallucinated file paths.

### Standards Alignment — Medium
- ⚠️ L71-L73: Cascade layer order deviates from earlier global guidance (common pattern: reset, tokens, base, theme, components, utilities, overrides). Given tokens dependence, placing `base` before `tokens` can hinder variable usage clarity.
- ⚠️ L37-L41: Tokens section omits requirement for fallbacks for advanced color functions (the line mentions fallbacks but does not mandate fallback implementation example). Could leave ambiguity in enforcement.
- ⚠️ L30-L33: Specificity policy defines (0,1,1) but does not clarify handling pseudo-class additions or attribute selectors; ambiguity may lead to inconsistent severity ratings.

### Accessibility Coverage — Low
- ✅ L45-L54: Strong coverage of contrast, focus, target size.
- ⚠️ L45-L54: Missing explicit mention of keyboard-only focus order verification and color contrast for focus indicators themselves.
- ⚠️ L50-L53: Forced colors guidance present but lacks example mapping (e.g., system color usage snippet). Could cause uneven implementation.

### Responsiveness & Layout — Medium
- ✅ L58-L63: Encourages container queries & logical properties.
- ⚠️ L58-L63: No fallback strategy for browsers lacking container queries beyond generic `@supports`; suggest explicit guidance to default to mobile-first flex/grid.
- ⚠️ L62-L63: Modern viewport units listed but no caution about iOS Safari dynamic viewport quirks; risk of layout shift.

### Performance & Rendering — Low
- ✅ L77-L81: Clear animation and expensive property constraints.
- ⚠️ L77-L82: Missing mention of limiting stacking contexts and paint containment (`contain: layout paint size style`).

### Cross-Browser & Progressive Enhancement — Medium
- ⚠️ L85-L88: Browserslist reference lacks explicit directive to include it in review output (e.g., cite current targets). Reduces actionable cross-browser notes.
- ⚠️ L87-L88: `@supports` fallback mention lacks prioritization guidance (which features to gate first: container queries, `@property`, nesting). Ambiguous triage ordering.

### Variants & State API — Low
- ✅ L92-L96: Clear separation of visual variants (data-*) vs state (ARIA/native attributes).
- ⚠️ L92-L96: No guidance for interaction between disabled state and variant classes (e.g., ignoring variant styling when disabled).

### Output Format Precision — Medium
- ⚠️ L109-L113: Example findings include placeholder file paths; lacks requirement to map real file paths & ensure deterministic sorting (by severity then file then line).
- ⚠️ L114-L121: Diff example does not mandate limiting diff context or marking multi-line changes; could lead to bloated output.
- ⚠️ L121-L126: Missing tests list excludes high contrast (forced-colors) interactive focus regression scenario combining reduced motion + forced colors.

### Risk & Severity Taxonomy — Low
- ✅ L133-L138: Clear tier definitions.
- ⚠️ L133-L138: Missing explicit mapping from finding types to default severity when ambiguous (e.g., non-token color usage auto HIGH vs MEDIUM). Reviewer discretion may vary.

### Hallucination Mitigation — Medium
- ⚠️ Global: No explicit prohibition against introducing new utility classes or layers not present in code. Risk of speculative suggestions.
- ⚠️ Global: LLM failure modes (L142-L150) helpful but lacks directive to flag any occurrence explicitly (e.g., "Always elevate these to at least HIGH").

### Consistency & Formatting — Low
- ⚠️ Multiple headings (e.g., L11, L27, L100, L133) end with stray `**` unmatched; minor markdown consistency issue potentially impacting rendering.

## Suggested Changes
**L71-L73 (Cascade Layer Order)**
```diff
-  @layer reset, base, tokens, theme, components, utilities, overrides;
+  @layer reset, tokens, base, theme, components, utilities, overrides;
```
**L9 (Token Limit Alignment)**
```diff
- Your output must be concise, high-signal, and strictly under 4000 tokens.
+ Your output must be concise, high-signal, and strictly under 3000 tokens.
```
**After L9 (Add Environment Context)**
```diff
+ Target environment: modern evergreen browsers per project Browserslist; note any IE/Safari quirks explicitly. Assume OS-agnostic unless platform-specific issues arise.
```
**L104-L129 (Output Format Enhancements)**
```diff
- ## Summary
+ ## Summary
+ Include counts: CRITICAL/HIGH/MEDIUM/LOW findings.
```
**After L109 (Clarify Sorting & Real Paths)**
```diff
+ Sort findings by severity (CRITICAL→LOW), then file path alphabetically, then ascending line number. Use actual repository-relative paths.
```
**After L121 (Expand Missing Tests)**
```diff
+ - [ ] Combined forced-colors + reduced-motion focus visibility
+ - [ ] High-contrast theme variant rendering
```
**L37-L41 (Token Fallback Clarification)**
```diff
- Prefer **OKLCH** and `color-mix()` with documented fallbacks.
+ Prefer **OKLCH** and `color-mix()` with documented fallbacks (always provide sRGB hex fallback immediately before advanced declarations).
```
**Add Hallucination Guard (After L154)**
```diff
+ Do not invent new classes, layers, or token names not present in the provided code; flag absent constructs instead of suggesting them.
```
**Heading Cleanup (Example L11)**
```diff
- ## 1. Review Objectives (P0 – MUST)**
+ ## 1. Review Objectives (P0 – MUST)
```
(Repeat for sections with trailing `**`.)

## Missing Tests
- [ ] Forced colors + reduced motion combined focus scenario
- [ ] High contrast theme token fallback rendering
- [ ] Container query absence fallback behavior
- [ ] Layer order regression visual diff
- [ ] Non-token literal detection (lint rule / static analysis)

## Merge Readiness
REQUEST CHANGES — Medium risk due to layering order inconsistency, missing hallucination safeguards, ambiguous severity mapping, and output format clarity gaps. Apply suggested diff edits, then re-run prompt evaluation against the checklist to ensure environment context, self-check, and hallucination guards are present. After updates, risk expected to drop to LOW.
