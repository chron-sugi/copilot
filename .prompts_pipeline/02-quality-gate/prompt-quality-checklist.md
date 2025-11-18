# GitHub Copilot Prompt Evaluation Checklist

Use this checklist to evaluate whether a GitHub Copilot prompt file (or individual prompt) is well-designed for software engineering tasks.

## 1. Context & Goals
- [ ] Task objective is clearly stated in 1–3 sentences.
- [ ] Success criteria / definition of done is explicit (e.g., behaviors, edge cases, performance).
- [ ] Only relevant project context is included (files, modules, architecture), avoiding noise.
- [ ] Constraints are specified (language, frameworks, style guides, performance, portability).

## 2. Input Structure & Clarity
- [ ] Assistant role is clearly defined (e.g., "You are a senior X engineer…").
- [ ] There is a single primary intent, or multiple intents are clearly separated/prioritized.
- [ ] Complex tasks request a stepwise workflow (plan → implement → test/validate → summarize).
- [ ] Vague verbs ("optimize", "improve") are clarified with concrete goals (e.g., speed, readability).

## 3. Code & Artifacts Referencing
- [ ] File paths are explicit (e.g., `src/observability/logger.py`) and unambiguous.
- [ ] Only relevant snippets or sections are included; large files are scoped to specific regions.
- [ ] Instructions tell the model to preserve existing contracts (public APIs, signatures, behavior) unless change is allowed.
- [ ] Dependencies, runtime versions, and important frameworks are mentioned when relevant.

## 4. Style, Quality, and Safety Requirements
- [ ] Coding style expectations are clear (e.g., "match existing style in this file" or explicit guide).
- [ ] Testing expectations are defined (what tests to write/update and where they live).
- [ ] Expected error handling and edge cases are included or referenced.
- [ ] Security/privacy constraints are explicit (e.g., no secrets in logs, validate/sanitize input).
- [ ] Performance constraints or targets are noted when important.

## 5. Interaction & Output Formatting
- [ ] Desired answer format is specified (code-only, code + brief explanation, structured sections, etc.).
- [ ] Expected verbosity is defined (e.g., concise summary vs. detailed walkthrough).
- [ ] Explicit "do" / "don’t" behaviors are listed (e.g., don’t modify unrelated files, don’t add deps silently).
- [ ] Use of headings, bullets, or sections is requested for complex answers.

## 6. Tooling & Execution Expectations
- [ ] Environment is described (OS, shell, language runtime, key tools).
- [ ] The prompt asks for copy-pasteable commands to run tests/build/lint using the correct shell.
- [ ] The model is asked to ensure solutions are testable and to reference how to validate them.
- [ ] Any CI/CD, lint, or formatting requirements are mentioned if they impact the changes.

## 7. Prompt Robustness & Maintainability
- [ ] Hidden assumptions are minimized; non-obvious requirements are spelled out.
- [ ] Instructions avoid internal conflicts (e.g., not both "extremely concise" and "explain every step").
- [ ] The prompt is modularly structured (role, context, task, constraints, output format) for reuse.
- [ ] There is guidance for updating the prompt as the repository or process evolves.

## 8. Evaluation & Self-Check Hooks
- [ ] The prompt encourages grounding in provided files and context ("only modify X/Y unless instructed").
- [ ] For ambiguous requests, the model is prompted to state assumptions or propose clarifying questions.
- [ ] The model is asked to briefly self-check its output against the acceptance criteria.
- [ ] Optional: The prompt suggests small, verifiable steps (e.g., summarize plan before large edits).
