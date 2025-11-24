---
name: safe-edit
description: Safely implement a scoped change in this repo using GPT‑5 mini
agent: 'DocsSteward'
model: 'GPT-5 mini'
argument-hint: 'Describe the change you want; optionally include #file / #codebase / #terminalSelection context.'
---

Task: Keep docs/design.md up to date. Only touch this file when architecture or contracts change.

When to update docs/design.md:
- YES:
  - A new feature or view is added (e.g., new page, panel, major toolbar, SPL view).
  - Core data contracts change (new schemas/types, new KO/graph shapes).
  - Responsibilities move between layers (page ↔ context panel ↔ canvas ↔ graph-utils/hooks).
  - Public APIs change (shared component props, exported helpers, Zod schemas).
- NO:
  - Pure styling changes (Tailwind class tweaks, spacing, colors).
  - Small local refactors that don’t change behavior or contracts.
  - Copy/label-only changes.

How to update:
- Keep it short and high-level; do NOT paste code.
- For each change:
  - Add or update a small subsection with:
    - Intent: what problem this feature/module solves.
    - Responsibilities: what this module owns vs what others own.
    - Data contracts: names of key types/schemas and their role (no full definitions).
    - Important invariants/constraints (e.g., “edges must reference existing nodes”).
- Remove or adjust any text that is now misleading.

Never edit docs/design.md in the same change for purely cosmetic UI tweaks. Only update it when the mental model of the system has changed.