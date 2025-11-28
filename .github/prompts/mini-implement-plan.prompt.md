---
name: safe-edit
description: Safely implement a scoped change in this repo using GPT‑5 mini
agent: 'MiniDeveloper'
model: 'GPT-5 mini'
argument-hint: 'Describe the change you want; optionally include #file / #codebase / #terminalSelection context.'
---

You are running the **safe-edit** workflow for this repository.

User task description:

${input:taskDescription:Describe the change you want to make}

If the user has selected code or a file when invoking this prompt, that context appears below and should be treated as primary:

${selection}

Follow this process:

1. **Restate & assess**
   - Restate the task in 1–3 sentences.
   - Quickly classify it as *small*, *medium*, or *large / risky*.
   - If it is large / risky or under‑specified, stop and:
     - Ask 2–5 clarifying questions, and
     - Explain whether this is better suited to a higher‑reasoning model.

2. **Gather context**
   - Use chat tools and context mentions to inspect the relevant files and tests.
   - If the selection already contains the exact code to change, treat it as the main focus but still scan for usages and tests.

3. **Propose a plan**
   - Produce a short, numbered change plan grouped by file.
   - Keep the plan focused and incremental.

4. **Implement**
   - For each step in the plan:
     - Show the key code snippets to add or modify, in fenced code blocks.
     - Avoid unrelated refactors and style changes.
     - Clearly mark any *new* functions, types, or dependencies.

5. **Verification**
   - Suggest concrete commands or manual steps to verify the change (tests, scripts, or manual flows).
   - When tests are missing, recommend at least one test that should be added.

6. **Summary & confidence**
   - Finish with:
     - A short summary of what changed.
     - A **Confidence** line (`low` / `medium` / `high`).
     - 1–3 key assumptions that could affect correctness.

Keep your output compact and focused on what the user needs to review to safely apply the change.
