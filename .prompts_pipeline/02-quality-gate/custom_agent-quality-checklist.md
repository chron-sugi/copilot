# GitHub Copilot Custom Agent Validation Checklist

Effective custom agents formerly known as chat modes have a clear, narrow mission and doctrine, a minimal and appropriate tool/model configuration, and are wired into a safe, observable workflow with handoffs and shared governance. Aim for roles that are specific, testable, and iterated using real interactions.

**Agent files must stay under 1,000 tokens** to ensure fast loading and efficient context usage.

## Role

- [ ] Start with explicit **persona framing** (for example "You are a senior front-end JavaScript developer").
- [ ] Follow persona with "Your responsibilities:" heading.
- [ ] List **core responsibilities** as bullets under "Your responsibilities:" (what the role builds, maintains, or delivers).
- [ ] Explicitly state **scope** in responsibilities (what the role should and should not work on).
- [ ] List **non‑goals** if needed (what the role must not do).
- [ ] Write instructions as stable doctrine, not as a one‑off task prompt.

## Reasoning Heuristics

- [ ] List **numbered reasoning heuristics** (for example "1. Start from intent: restate the feature...").
- [ ] Include heuristics for context gathering (for example "Read first, code second: scan existing components...").
- [ ] Include heuristics for work decomposition (for example "Decompose work: structure → behavior → state → styling → tests").
- [ ] Include domain-specific reasoning patterns (for example data flow, async behavior, CSS integration).
- [ ] Include quality and safety heuristics (for example "Default to small, incremental changes").
- [ ] Include escalation guidance (for example "Label uncertainty and provide options when conventions are ambiguous").
- [ ] Use **strong imperative verbs** at the start of each heuristic.
- [ ] Keep heuristics scannable. Avoid long clauses after semicolons.

## Interaction Tone

- [ ] Define **interaction tone** with specific adjectives (for example "Collaborative, direct, and pragmatic").
- [ ] Specify communication style (for example "Prioritize clarity over verbosity").
- [ ] Include guidance on handling options and recommendations.
- [ ] Include guidance on handling missing information (for example "Ask for or clearly label missing context").

## Internal Goals

- [ ] List **numbered internal goals** as priorities.
- [ ] Include goals about output quality and alignment with project standards.
- [ ] Include goals about code maintainability and debuggability.
- [ ] Include goals about reuse and avoiding duplication.
- [ ] Include goals about test coverage.
- [ ] Include goals about outputs being useful for other agents and humans.

## Output Structure

- [ ] Define **output structure** with numbered sections or headings.
- [ ] Specify what each section should contain (for example "Intent & Constraints", "Code Changes", "Notes for Review").
- [ ] Include formatting guidance (for example "Provide complete updated functions/components/files when practical").
- [ ] Include token/length constraints if applicable (for example "Keep each response strictly under 4000 tokens").

## Tools, Capabilities & Safety

- [ ] Include a `tools` list in frontmatter with only relevant tools for the role.
- [ ] Limit read‑only roles (planner, reviewer, SRE, security) to read‑only tools (for example `search`, `fetch`, `githubRepo`, `codebase`, `usages`).
- [ ] Grant editing tools (for example `edit`, terminal, file operations) only to implementation roles.
- [ ] State explicitly in the body text that implementation roles may change files.
- [ ] Curate the total enabled tools (built‑in, MCP, extension) to stay comfortably below the 128‑tool per‑request limit.
- [ ] Specify in doctrine which tools to use first and in what order (for example "Start with `#search` + `#codebase` before editing").
- [ ] Include safety guidance: require approvals for powerful tools (terminal, file ops). Route large edits through Edit mode or checkpoints.
- [ ] Verify MCP tool servers/configs exist in workspace or profile MCP config and comply with organization governance.

## Additional Constraints

- [ ] Verify the **entire agent file is under 1,000 tokens** (including frontmatter, all sections, and examples).
- [ ] Include any **additional constraints** specific to the role (for example output preferences, file save requirements).
- [ ] Keep constraints brief and actionable.

## Model Strategy & Behavior

- [ ] Pin a `model` in frontmatter or explicitly use `Auto` with an intentional choice (determinism vs resilience/throughput).
- [ ] Verify the selected model supports tool calling for Agent‑style modes that rely on tools.
- [ ] Write doctrine to be as model‑agnostic as possible. Avoid hard dependencies on a single vendor unless required.

## Interaction with Instructions, Prompts & Workspace

- [ ] Store the mode in a shared, discoverable location (for example `.github/chatmodes/` in the repo or user profile for reuse).
- [ ] Ensure the mode's doctrine does not contradict workspace‑wide instructions (for example `.github/copilot-instructions.md`).
- [ ] Respect file‑scoped instructions (`*.instructions.md`) relevant to the role (for example `**/*.py`). Do not override them carelessly.
- [ ] Align companion prompt files (`*.prompt.md`) with this mode's `mode`, `agent`, and `tools` configs.
- [ ] Avoid hard‑coding project‑specific paths, secrets, or private identifiers that prevent reuse across repos.

## Handoffs, Workflow & Human Control

- [ ] Define `handoffs` in frontmatter for multi‑step workflows that represent the next logical steps (for example Plan → Implement → Review).
- [ ] Give each handoff a clear `label` describing the action (for example "Implement Plan", "Request Review").
- [ ] Ensure each handoff `agent` refers to a valid, documented mode name in the workspace.
- [ ] Match each handoff `prompt` to the target agent's role and input expectations.
- [ ] Set each handoff `send` appropriately (`false` where human approval is required before sending).
- [ ] Specify in doctrine when to propose or use each handoff (for example "After plan approval, use 'Implement Plan' handoff").

## Safety, Risk Management & Non‑Goals

- [ ] Explicitly list prohibited actions in the body text (for example "Do not modify code", "Do not run destructive commands", "No dependency upgrades").
- [ ] Direct the agent to ask for missing critical inputs or context instead of hallucinating or guessing.
- [ ] Encourage small, reviewable changes in implementation modes instead of broad, risky refactors.
- [ ] Emphasize analysis, checklists, and reporting in security/SRE/compliance roles over automated direct fixes.
- [ ] Discourage copying unvetted external code or scripts without human review.

## Observability, Testing & Iteration

- [ ] Test the mode on at least one real task and inspect behavior in Chat Debug view (composite prompt, tools, responses).
- [ ] Simplify instructions to be concise and non‑duplicative. Remove unnecessary or conflicting guidance.
- [ ] Include self‑review steps in doctrine (for example "Summarize assumptions and open questions before final output").
- [ ] Ensure expected outputs (sections, formats) can be quickly checked against the DoD by a human or simple script.
- [ ] Document a path to iterate on this mode (for example "owned by X team; update via PR to `.github/agents/...`").

## Sharing, Governance & Lifecycle

- [ ] Place the mode file under version control (tracked in Git) if others rely on it. Avoid local, unshared experiments.
- [ ] Review changes to the mode via pull requests or equivalent review process.
- [ ] Include a concise `description` in frontmatter that clearly explains the agent in the picker/dropdown.
- [ ] Provide a clear, human‑friendly `name` in frontmatter distinct from the filename when used in UIs (if supported).
- [ ] List available modes, their intent, and their paths in repository docs or `README`.
- [ ] Clearly mark or remove deprecated or superseded modes so only current, supported modes appear for users.

---

## References

- [VS Code: Custom Chat Modes](https://code.visualstudio.com/docs/copilot/customization/custom-chat-modes)
