---
name: docs.add-jsdoc-comments
description: Keeps docs/design.md up to date with architecture and contract changes.
agent: 'DocsSteward'
model: 'GPT-5 mini'
argument-hint: 'Describe the change you want; optionally include #file / #codebase / #terminalSelection context.'

---

### Instructions

- Add JSDoc-style comments to each module and function. 

- For the module-level docstring, provide a brief description of what the entire file does at the top. 

- For each function, include a comment above it that describes its purpose, its parameters (with `@param`), and its return value (with `@returns`).

- Follow the typical JSDoc convention and ensure each function has a clear, concise summary.
