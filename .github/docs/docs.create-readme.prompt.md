---
name: docs.create-readme
description: Creates readme for package or subpackage
model: GPT-5 mini
agent: 'DocsSteward'
---
version: 1.0
---

# README.md Generation – Core Agent Instructions
You are an expert technical writer and software maintainer.

Goal: Write a clear, practical `README.md` for this package so a developer can start using it in under 5 minutes.

Target length: roughly 1,500–2,000 tokens. If the README starts to feel long or repetitive, move detail into linked docs instead of expanding the file.

---

## 1. Analyze the package before writing

Use your available tools to inspect the code and docs.

You MUST, at minimum:

- List the package root contents (source, tests, docs, examples, config).
- Identify:
  - Package name and main entry point(s) (e.g. `__init__.py`, `index.ts`, etc.).
  - Main public classes/functions/modules that callers are expected to use.
  - Any tests or examples that show realistic usage.
  - Key dependencies and configuration mechanisms (env vars, config files, etc.).

From this, build a short internal summary (for yourself) answering:

- What problem does this package solve?
- Who is supposed to use it and in what context?
- What are the main public entry points?
- What are the critical dependencies and requirements?

Do NOT guess. Base everything on the actual code and existing docs.

---

## 2. Required README structure (in order)

Use these standard section names. They are important for both humans and AI tools.

1. `# {Package Name}` + one-line description  
2. `## Overview`  
3. `## Installation`  
4. `## Quick Start`  
5. `## Features` (and, if relevant, `## Architecture`)  
6. `## API Summary`  
7. `## Usage Examples`  
8. `## Configuration` (only if the package is configurable)  
9. `## Testing`, `## Dependencies`, `## Related Packages` (as applicable)  
10. `## Contributing` and `## License` (even if very short)

If some sections truly do not apply (for example, no configuration), you may omit them.

---

## 3. Section-by-section guidelines

### 3.1 Title & brief description

- H1 = package name.
- One concise sentence (10–20 words) explaining what it does and when you’d use it.
- Optional: a few badges (license, version, build status) if this is a public package.

### 3.2 Overview

In 1–3 short paragraphs, explain:

- What problem this package solves and why it exists.
- Where it fits in the larger system or project.
- Who the intended users are (e.g. “backend services using X”, “data engineers”, “front-end features in Y”).

Avoid implementation details here. Focus on “what” and “why”.

### 3.3 Installation

- Show the simplest production install command (e.g. `pip install`, `npm install`, or internal import pattern).
- If local development setup is different, show that briefly.
- Mention important prerequisites or version constraints only if they are actually enforced.

Keep this to a few lines. Troubleshooting and OS-specific details belong in separate docs.

### 3.4 Quick Start

Provide ONE minimal, runnable example that shows the most common usage.

- Use real code from the package (no pseudocode).
- Include necessary imports and basic setup.
- Show the main entry point in action and the typical output or effect.
- Add 1–3 sentences explaining what the example demonstrates.

Do NOT include multiple variations here. Additional scenarios go into `Usage Examples` or external docs.

### 3.5 Features (and Architecture)

Under `## Features`:

- Bullet list of the main capabilities (3–8 bullets).
- Be concrete: what can the user actually do with this package?

If the package has a non-trivial structure, add a short `## Architecture` section:

- One short paragraph describing the pattern (e.g. layered, hexagonal, simple module, etc.).
- Optionally, a tiny directory tree showing the main folders and their roles.
- No deep design narratives; link to architecture docs if they exist.

### 3.6 API Summary

Summarize the public surface area at a high level:

- Focus on the primary classes, functions, or modules that callers interact with.
- For each major class or function, provide:
  - A one-line purpose.
  - A few key methods or patterns with short descriptions.
  - A small code fragment for the most important ones (optional if already shown in Quick Start/Examples).

Do NOT:

- List every method or internal helper.
- Copy full docstrings or parameter tables.
- Describe private or internal-only APIs.

If a full reference exists, link to it (e.g. `docs/api-reference.md`).

### 3.7 Usage Examples

If the package benefits from more than one usage pattern:

- Add 2–3 short, realistic examples (different scenarios).
- Each example should be complete and runnable.
- Precede each example with a one-line explanation (e.g. “Batch processing with caching enabled”).

If there is an `examples/` folder or other detailed examples, link to it instead of adding many examples here.

### 3.8 Configuration (if applicable)

If the package is configurable:

- Show a compact configuration snippet (dict/object/env vars, as appropriate).
- List only important options and defaults.
- Mention any key environment variables and their purpose.

Link to a full configuration reference if it exists.

### 3.9 Testing, Dependencies, Related, Contributing, License

Keep these sections brief:

- `## Testing`: one or two example commands (e.g. `pytest`, `npm test`).
- `## Dependencies`: list important external dependencies and their roles; link to full list if needed.
- `## Related Packages`: link to nearby modules or packages and explain how they relate.
- `## Contributing`: link to `CONTRIBUTING.md` if present.
- `## License`: state the license and link to the license file.

---

## 4. Progressive disclosure rules

The README is an entry point, not a full manual.

- Keep the README focused on:
  - What this package does.
  - How to install it.
  - One clear way to use it.
  - Where to find more information.
- Prefer links over inlining for:
  - Complete API reference.
  - Advanced examples.
  - Detailed architecture and design decisions.
  - Full configuration and changelog.
  - Detailed contributing guidelines.

Whenever you notice a section getting long or highly detailed, extract that content into `docs/` or `examples/` and link to it from the README.

---

## 5. Style and formatting

- Use clear, direct language. Avoid jargon or define it briefly when needed.
- Always use language-specific fenced code blocks (e.g. ` ```python`, ` ```ts`) when showing code.
- Ensure all code examples are consistent with the actual package API and can run as-is with reasonable setup.
- Use standard section names (`Overview`, `Installation`, `Quick Start`, `API Summary`, etc.) rather than creative headings.
- Keep lists and tables simple and easy to scan.

---

## 6. Final checklist (after writing)

Before you consider the README done, verify:

- It accurately reflects the package’s current code and behavior (no guesses).
- A developer can:
  - Understand what the package does.
  - Install it.
  - Run at least one concrete example.
  - See where to look for deeper docs.
- The Quick Start example is complete and runnable.
- The README feels like a 5–10 minute read (roughly 1,500–2,000 tokens).
- Detailed material (full API, deep architecture, exhaustive configuration, long history) lives in linked docs, not in the README.

