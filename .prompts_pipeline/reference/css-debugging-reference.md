CSS Debugging Reference — Bullet Summary
Common Culprits
Container Query Issues


Missing container-type


Container smaller than query breakpoint


Wrong or missing container-name


Browser support gaps


Use Chrome’s Container Query visualizer


Token Inheritance Issues


Token not defined or out of scope


Shadow DOM / iframe boundaries


[data-theme] missing


Typos in custom properties


Fallbacks overriding unintentionally


Use Computed tab to trace var() resolution


Specificity Conflicts


Third-party CSS overrides


Unlayered CSS overrides layered CSS


!important is reversed inside @layer


Inline styles dominating


Use :where() to zero specificity


Check specificity hover in Chrome


State / Variant Mismatches


Misspelled data attributes


Wrong element receiving attributes


JS not applying state


Conflicting variant values


Selector mismatch between HTML and CSS


Browser / Feature Support


Container queries, nesting, @layer, @property, :has() may lack support in older browsers


Use @supports for fallbacks


Check MDN / CanIUse



Modern DevTools Features
Chrome


Selector specificity hover


@layer visualization


Nesting-aware inspector


Container Query Inspector


Forced Colors emulation


CSS Overview panel


Firefox


Inactive CSS indicators


Grid/Flexbox inspector


Accessibility inspector


Fonts panel


Safari


CSS changes timeline


Responsive Design Mode


Audit tab


Layers panel



Common DevTools Workflows


Identify winning rule via Styles → Computed


Trace custom properties


Test responsive/container behavior


Compare specificity rules



Debugging Techniques
Isolation


Comment out half (bisection)


Create minimal reproduction


Remove unrelated JS/animations


Simplification


Flatten selectors


Hard-code values to isolate token issues


Remove nesting


Comparison


Compare working vs broken DOM/CSS


Cross-browser testing


Use git bisect to find breaking commit


Systematic Elimination


Change one variable at a time, document results


CSS-Specific Tools


Force pseudo-states


Trace custom properties


Comment out layers


Reduce specificity with :where()


Visualize cascade in DevTools



Debugging Workflow Examples
1. Primary button wrong color


Variant rule overridden by state rule


Fix: adjust selector or remove conflicting data-state


2. Container query not firing


Container smaller than required breakpoint


Fix: adjust min-width or container size


3. Theme not applying


Palette token missing


Fix: define missing token or use literal value



Related Resources


CSS Debugger Chat Mode


CSS Core Standards


Chrome/Firefox DevTools CSS docs

