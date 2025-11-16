


1) What a “custom chat mode” actually does

A custom chat mode is a Markdown file (*.chatmode.md) that packages role instructions + a curated tool set + (optionally) a model and “handoffs”. When you switch into that mode, Copilot applies those settings to the next turn(s) in your chat. The body of the file (your guidelines) is prepended to the user prompt, so every turn starts with your role’s doctrine. 
Visual Studio Code

The file lives in your workspace (shareable via VCS) or your user profile (reusable across projects).

How coding agents respond to a custom mode

In Agent mode, the agent autonomously chooses and invokes tools from the enabled list (including those you specify in your mode). Your mode’s tools limit or expand what the agent is allowed to do. You can still force a specific tool in any mode with #toolName (e.g., #fetch url). 
Visual Studio Code

In Ask mode, the assistant answers conversationally; it won’t autonomously call tools unless you reference them with #. In Edit mode, it proposes edits with an overlay for you to review and apply. (See “Built‑in chat modes” for the behavioral differences.) 
Visual Studio Code

Model capabilities matter. If the selected model doesn’t support tool calling, it won’t appear when you’re in Agent mode. 

You can also use Auto model selection or provide your own model key; both influence how your mode behaves at runtime. 
Visual Studio Code

## INTERACTION WITH GLOBAL INSTRUCTIONS ##

Global instructions (like workspace .github/copilot-instructions.md or fine‑grained *.instructions.md) can also apply. Your mode adds on top of that, and 

The tool list priority is: Prompt file ► Mode ► Default. 



Think of a custom mode as a persona + capabilities you can switch on instantly, and that the coding agent then follows—within the guardrails you set.

## DESIGN FRAMEWORK ##

Use this checklist for any role you want to encode.

Define the job

Goal: What outcome should the role produce?

Scope & non‑goals: What must it not do?

Definition of Done (DoD): Observable acceptance criteria (format, tests, artifacts).

Choose base chat behavior per task phase

Ask for research/analysis/triage.

Edit for surgical, reviewable changes.

Agent for multi‑step work that benefits from tools and autonomy. 
Visual Studio Code
+1

## TOOLS ##

Start with read‑only tool sets for research roles (#search, #fetch, #githubRepo, #codebase, #usages).

Grant editing tools (#edit, terminal, file ops) only for implementation roles—and pair them with checkpoints or review instructions.

Keep tool count lean (model limit 128 tools per request; enable only what’s relevant). 
Visual Studio Code

If needed, extend via MCP servers (e.g., databases, cloud APIs). Govern with chat.mcp.access and keep configs in mcp.json (workspace or profile). 

Use tool approval prompts and avoid globally auto‑approving powerful tools/commands; if you must, scope approvals narrowly and understand the risks. 

## MODEL STRATEGY ##

Prefer Auto when you value resilience and throughput; pin models when you need determinism or specific capabilities (vision, tool calling). 
Visual Studio Code

Write doctrine (instructions) that drive the agent’s choices

Lead with mission, constraints, and DoD.

Specify context‑gathering steps (what to read, which tools to use first).

Declare output schemas (headings, tables, code fences, JSON shapes).

### ESCALATION RULES ###

Add escalation rules (“ask for missing inputs”, “propose handoff to Review mode”).

Plan for safety & review


## MINIMUM IMPLEMENTATION ##

3) Implementation: minimal but powerful .chatmode.md
---
description: Focused planner that gathers context and outputs a step-by-step plan. No edits.
# Tool sets or specific tools. Keep read-only for planning.
tools: ['search', 'fetch', 'githubRepo', 'codebase', 'usages']
# Optional: pin a model (else the chat picker / Auto is used)
model: Auto


# Planning Mode

**Mission:** Propose a concrete implementation plan. Do not edit files.

**Context to gather (in order):**
1. Use `#githubRepo <owner/repo>` (if relevant) and `#codebase` references to locate impacted modules.
2. Use `#search` and `#usages` to find related symbols.
3. Use `#fetch` for external standards or docs if needed.

**Output (Markdown):**
- Overview
- Assumptions / Open questions (ask before proceeding)
- Implementation Steps (numbered, small PRs)
- Risks & Alternatives
- Test Plan (unit/integration/e2e)
- Rollout & Observability


Why this works: the body becomes part of the prompt every time you use this mode; the limited tool list keeps the agent from making edits; the handoffs invite a guided, reviewable flow. 
Visual Studio Code

Store in .github/chatmodes/ to share with your team. Use Settings Sync if you keep it in your user profile. 
Visual Studio Code

4) Complementary building blocks that raise quality
A) Prompt files for repeatable tasks

Use *.prompt.md for on‑demand runbooks (e.g., “Generate a REST client”, “Draft ADR”). Prompt files support their own mode, tools, and variables like ${selection} or ${input:var}. Tool priority is prompt ► mode ► default. 
Visual Studio Code
+1

Skeleton:

---
mode: 'agent'              # 'ask' | 'edit' | 'agent'
model: Auto
tools: ['search', 'codebase', 'edit']
description: Create an ADR
---
Title: ${input:title}
Scope: ${input:scope}
Constraints: ${input:constraints:List constraints or "none"}
Deliver a well-formed ADR in Markdown.

B) Workspace & file‑scoped instructions

Workspace‑wide: .github/copilot-instructions.md (applies to all chat).

File‑scoped: *.instructions.md with applyTo: "**/*.py" (auto‑applies for edits/creates).
Both integrate cleanly with your custom mode. 
Visual Studio Code

## TOOLING STRATEGY ## 

Prefer built‑in tools first; add MCP tools for external systems (DBs, cloud, proprietary APIs), and extension tools for deep editor integrations. Govern installation with chat.mcp.access, and share workspace MCP config via .vscode/mcp.json (or Dev Containers). 
Visual Studio Code

Keep tools purpose‑built by mode (e.g., Review mode: #search, #codebase, #problems; Implement mode: add #edit, terminal). In Agent mode the agent will pick autonomously from the enabled tools, and you can still direct it with #tool. 


Watch the 128‑tool cap; large MCP servers can exceed it—curate or use virtual tools selectively. 
Visual Studio Code

### TOOL SAFETY AND APPROVALS ###

Approve tool invocations thoughtfully (especially terminal and file mutations). You can tune auto‑approve patterns, but avoid blanket approvals. 
Visual Studio Code

Encourage Edit mode or checkpoints before applying large diffs; make the agent propose changes and let humans apply. 
Visual Studio Code

Put team‑wide norms in workspace instructions and review mode files via pull requests.

7) Observability & continuous improvement

Use Chat Debug view to see the full composite prompt (your mode + instructions + context), the tool calls, and responses. This is the fastest way to diagnose “why did it do that?” and tighten your guidance. 
Visual Studio Code

Iterate: simplify instructions, reduce tools, clarify DoD, and add handoffs where the flow gets bumpy.

8) Example role kits (mix & match)

Planner (Ask): read‑only tools, output plan + questions, handoff to Implement.

Implementer (Agent): #edit, terminal, file ops enabled; doctrine mandates small PRs, tests, and self‑review; handoff to Review. 
Visual Studio Code

Reviewer (Ask or Edit): read‑only tools; output structured findings (security, perf, correctness), suggested diffs via Edit.

Tester (Ask/Agent): generate failing tests (Ask), then handoff to Agent to make them pass. (Great handoff pattern.) 
Visual Studio Code

SRE/On‑call (Ask): #search, #fetch, #codebase; explicitly no edits; output RCA template + runbook links.

Security (Ask): curated checklists; limited tools; strong non‑goal (“do not modify code”).

9) Copilot Coding Agent vs Agent mode (when to delegate)

Agent mode runs locally in VS Code and edits files directly in your workspace under your supervision.

Copilot coding agent runs in GitHub’s cloud, works from an assigned issue or delegated chat context, and creates a PR you can review. You can even delegate from chat via #copilotCodingAgent. Use it for well‑scoped background work that should land as a PR. 
Visual Studio Code

10) Quality checklist (print this)

 Clear mission, constraints, and DoD at the top of the mode body

 Minimal, relevant tool set (respect the 128‑tool cap) 
Visual Studio Code

 Model strategy chosen (Auto vs pinned; ensure tool calling if using Agent) 
Visual Studio Code

 Handoffs defined for multi‑step flows (Insiders) 
Visual Studio Code

 Safety: approvals on; large edits via Edit mode/checkpoints 
Visual Studio Code
+1

 Observability: validate in Chat Debug view; iterate text + tools 
Visual Studio Code

 Shared in .github/chatmodes/ with PR review; global norms in .github/copilot-instructions.md 
Visual Studio Code
+1

### APPENDIX ###

Custom modes: file format, storage, handoffs, and “instructions are prepended.” 
Visual Studio Code

Built‑in chat modes (Ask/Edit/Agent) and how tools are used. 
Visual Studio Code
+1

Prompt files: *.prompt.md with mode, model, tools, variables, and priority relative to modes. 
Visual Studio Code
+1

Tools: types (built‑in, MCP, extension), explicit #tool, approval, 128‑tool limit. 
Visual Studio Code

Language models: Auto selection, BYOK, tool‑calling requirement for Agent mode. 
Visual Studio Code

MCP: enabling, governing access, sharing config, Dev Containers. 
Visual Studio Code

Debugging: Chat Debug view surfaces system prompt, context, tools, responses. 
Visual Studio Code

Final takeaway

To create an “effective” custom chat mode for any role, be opinionated about (1) the job to be done, (2) the minimal tools needed, (3) the model capabilities, and (4) a crisp doctrine and output schema. Start narrow, wire in handoffs to orchestrate your workflow, and iterate with the Chat Debug view until the agent’s behavior matches your intent—consistently and safely.


## UPCOMING HANDOFF MODE ##
Handoffs (Insiders) let you chain modes with one‑click buttons (e.g., Planning → Implementation → Review), optionally pre‑filling or auto‑sending the next prompt. Use them to orchestrate multi‑step workflows with checkpoints. 
Visual Studio Code


Add handoffs to guide the next step (e.g., “Implement Plan” → Agent; “Run Security Review” → Ask). 
Visual Studio Code


chain into implementation or review phases
handoffs:
  - label: Implement Plan
    agent: agent     # switch to Agent mode
    prompt: Implement the plan above. Make small, reviewable commits.
    send: false
  - label: Request Review
    agent: review    # a custom review mode name you define
    prompt: Review the plan for security, performance, and testability.
    send: false
---

## Reference ##
https://code.visualstudio.com/docs/copilot/customization/custom-chat-modes?wt.md_id=AZ-MVP-5004796


# TO SYNTHESIZE #