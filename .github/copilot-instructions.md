# Project Copilot Instructions

## Project Overview

This repository contains GitHub Copilot customization files including custom instructions, chat modes, and prompt files for AI-assisted development workflows.

## Purpose

- Standardize AI assistance
- Provide specialized chat modes for different development roles
- Create reusable prompt templates for common tasks
- Maintain consistent coding standards and best practices

## Tech Stack

- **Documentation:** Markdown
- **Version Control:** Git
- **AI Tooling:** GitHub Copilot with custom extensions

## General Coding Guidelines

- Use clear, descriptive file names
- Follow GitHub Copilot conventions for file extensions:
  - `.instructions.md` for custom instructions
  - `.chatmode.md` for chat modes
  - `.prompt.md` for prompt files
- Keep documentation concise and actionable
- Version control all customizations in `.github/` directory

## File Organization

```
.github/
├── copilot-instructions.md         # This file (repo-wide standards)
├── instructions/                    # Custom instructions (auto-applied)
├── chatmodes/                       # Specialized AI personas
└── prompts/                         # Reusable task templates
```

## Best Practices
- Keep instruction files under 2 pages
- Use YAML frontmatter for configuration
- Test prompt files before committing
- Document handoff workflows between chat modes
