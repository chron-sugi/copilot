# GitHub Copilot Instructions Quality Checklist

- [ ] **Normative**  
  - Uses prescriptive language (`must`, `must not`, `should`, `may`) rather than suggestions or commentary.  
  - Avoids vague phrasing like “try to”, “it would be nice if”.

- [ ] **Operational**  
  - Every rule is something the agent can *actually execute* (no human-only actions like “ask the team”).  
  - Avoids references to unknown context the agent cannot see (e.g., “check the design doc” without a path or link).  

- [ ] **Directive**  
  - Tells the agent *what to do*, not just why (e.g., “Use `apply_patch` to modify files” instead of “Edits should be atomic”).  
  - Avoids purely descriptive or philosophical statements that don’t change behavior.

- [ ] **High-signal**  
  - No filler or restating obvious defaults (“be helpful”, “answer questions”) unless they encode a concrete constraint.  
  - Each rule either constrains behavior or resolves an ambiguity; remove redundant or overlapping bullets.  

- [ ] **≤ 300–800 words ideally**  
  - Full instructions (excluding examples/appendix) fall roughly within this range.  
  - If longer, high-priority behavioral rules are front‑loaded; lower‑priority details are clearly separated.

- [ ] **Written as rules the agent must follow**  
  - Uses clear, atomic rules instead of long paragraphs; one concern per rule.  
  - Avoids first‑person (“I/we”) and conversational fluff; speaks directly to the agent (“You must…”).

- [ ] **Has priority levels for each rule in `[P0]`, `[P1]`, or `[P2]` format**  
  - Every rule line includes exactly one priority tag, e.g., `R1 [P0] ...`.  
  - `[P0]` = must not be broken, `[P1]` = should follow, `[P2]` = nice-to-have.

- [ ] **Has priority level legend**  
  - A short `<priority_legend>` or equivalent section defines `[P0]`, `[P1]`, `[P2]` in 1–2 lines each.  
  - Legend appears near the top so the agent can interpret priorities before reading rules.

- [ ] **Has rule identifier**  
  - Each rule has a stable ID (e.g., `R1`, `J5`, `CSS12`) at the start of the line.  
  - IDs are unique within the file and stable over time (do not renumber when adding rules; append new IDs).  

- [ ] **Scoped to the target behavior/file**  
  - Instructions clearly state what they apply to (e.g., “JS/TS code”, “CSS files”, “this repository only”).  
  - Avoids rules that conflict with global system behavior unless explicitly marked as overrides.

- [ ] **Conflict-aware and ordered**  
  - Rules are grouped logically (e.g., “Core Behavior”, “Formatting”, “Safety”) with higher‑priority or more global rules first.  
  - Where conflicts are possible, the file states which rule/section wins (e.g., “P0 overrides P1/P2 on conflict”).

- [ ] **Tooling and environment‑aware**  
  - When referencing tools (e.g., `apply_patch`, `run_in_terminal`), names are exact and usage is clearly specified.  
  - OS/shell-specific constraints (e.g., “Windows PowerShell; use `;` instead of `&&`”) are explicitly documented if relevant.

- [ ] **Safety and compliance aligned**  
  - Rules do not instruct the agent to violate platform/content policies (e.g., copyright, safety).  
  - Any domain‑specific safety constraints (e.g., “do not touch `main` branch”, “never commit secrets”) are explicit.

- [ ] **Examples are clearly separated from rules**  
  - Examples are labeled as such and not written in a way that could be misread as additional rules.  
  - Rules do not depend on examples for correctness; examples only illustrate.

- [ ] **Versioning and ownership (optional but recommended)**  
  - File includes a short header with owner, last updated date, and scope.  
