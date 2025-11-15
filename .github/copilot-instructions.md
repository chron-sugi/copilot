# Project Copilot Instructions

## Project Overview

This repository contains GitHub Copilot customization files including custom instructions, chat modes, and prompt files for AI-assisted development workflows.

## Purpose

- Standardize AI assistance
- Provide specialized chat modes for different development roles
- Create reusable prompt templates for common tasks
- Maintain consistent coding standards and best practices

# Project Copilot Instructions (repo-specific)

Purpose: give AI coding agents immediate, repository‑specific context so they can be productive without guessing project structure or workflows.

Key locations and intent
- `.github/chatmodes/`: persona chatmodes (CSS, JavaScript, etc.). Use these to match tone/role when generating code or reviews.
- `.github/prompts/` and `prompt_engineering/prompts/`: canonical prompt templates and engineering examples. Prefer these over ad-hoc prompts.
- `.github/instructions/` and `.github/custom_agents/README.md`: per-agent or per-mode rules. Consult before changing chatmode behavior.
- `docs/` and `raw/`: longer-form guides and prompt source material. Use for reference and examples.

What to do first (for any code task)
- Read the relevant chatmode file in `.github/chatmodes/<area>/` (e.g. `css/` or `javascript/`) to match style and constraints.
- If changing or adding prompts, mirror existing pattern: `.prompt.md` files use clear frontmatter and example inputs — follow the same file naming and structure.
- If a suggestion affects multiple prompt files, update the corresponding files under `.github/prompts/` and `prompt_engineering/prompts/`.

Developer workflows (explicit commands)
- Stage all workspace changes: `git add -A`
- Commit with a clear message: `git commit -m "<short description>"`
- Push to this repo: `git push -u origin main` (this repo uses `main` by default)
- To normalize line endings after changing `.gitattributes`:
  - `git add --renormalize .`
  - `git commit -m "Normalize line endings (.gitattributes)"`

Project conventions and gotchas
- File types: use `.chatmode.md`, `.prompt.md`, and `.instructions.md` consistently.
- Line endings: this repo is developed on Windows — you will see LF → CRLF warnings. Prefer adding a `.gitattributes` entry if you change many files.
- Reserved filenames: Windows device names (like `NUL`) may have existed and can break `git add`. Avoid creating such names.

Integration points and scope
- This is primarily a repository of prompts, modes, and docs — there are no service binaries or test suites detected. Focus on content, format, and consistency.
- Changes to prompts and chatmodes are plain-text edits; verify rendering by opening the file in the repo or running any internal validation the prompt templates include.

How AI agents should propose changes
- Provide a single, small change per PR: update or add one `.prompt.md` or `.chatmode.md` plus a short test/example in the same file.
- Include a one‑line commit message and a short PR description explaining the motivation and which chatmode(s) are affected.

Examples (from this repo)
- Use `.github/prompts/css/css-create-component.prompt.md` as the canonical CSS prompt template.
- Check `.github/chatmodes/javascript/js-developer.chatmode.md` for the JavaScript developer persona and constraints.

If you are unsure
- Look for similar files under `.github/` and copy their structure.
- Ask for clarification in the PR description and reference the chatmode that should approve the change.

Please review and tell me which sections need more detail (examples, commands, or references to specific files).
