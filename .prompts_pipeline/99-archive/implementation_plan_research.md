Great question. Short answer: **a plain declarative spec is rarely enough**. The strongest results in the research literature consistently come from giving agents (1) a clear goal and success tests, **plus** (2) a *coarse* “how” in the form of a decomposed plan or milestones, **plus** (3) *concrete, domain‑matched examples* and relevant docs. Below is a concise, evidence‑backed recipe and a one‑page template you can drop into your own agent briefs.

---

## What the evidence says (and what to include)

### 1) Provide a decomposed plan (not just “what”)
A large body of work shows that **explicit task decomposition** boosts reliability across domains:

- *Plan‑then‑execute / decomposition prompts* (“Plan‑and‑Solve”, “Least‑to‑Most”, “Decomposed Prompting”) ask the model to (a) sketch a plan of subtasks, then (b) execute them. This reduces missing steps and improves accuracy vs. a single declarative instruction or vanilla chain‑of‑thought. 
- *Search‑style planning* (Tree‑of‑Thoughts) improves success by exploring and selecting among alternative sub‑plans, showing large gains on tasks requiring non‑trivial planning.
- For **software** specifically, *repository‑level coding* is framed as a **planning** problem (multi‑step chain of edits across files). Systems like **CodePlan** synthesize and then execute a plan, which outperforms single‑shot code generation on repo‑scale tasks.
- In interactive agents, **reason+act** prompting (ReAct) interleaves planning with tool actions and beats “reason‑only” or “act‑only” baselines.

**Takeaway:** your implementation plan should **decompose the goal into verifiable steps** and let the agent iterate step‑by‑step, rather than only stating the end goal.

---

### 2) Include acceptance tests / a correctness oracle
Agents that can *run* tests and get executable feedback learn and correct faster:

- SWE‑bench and **SWE‑agent** demonstrate that giving agents a task oracle (human tests) and tight feedback/guardrails raises real‑world bug‑fix success vs. freeform shells.
- **Test‑driven interactive generation** (e.g., TiCoder) improves correctness while reducing cognitive load; embedding tests in the workflow measurably helps both humans and LLMs.

**Takeaway:** Put **unit/acceptance tests** (or at least clear I/O examples) directly in the plan, and tell the agent to run them after each milestone.

---

### 3) Add domain‑matched **code examples**
For coding tasks, **few‑shot, in‑domain examples** are particularly helpful:

- Retrieval‑selected examples and demonstrations (e.g., **CEDAR**) significantly improve program repair and assertion generation.
- A 2025 ablation study on **what makes code examples effective** finds that realistic naming and structure matter; removing good names can drop performance by **up to 30 points**.

**Takeaway:** Provide **1–3 short, idiomatic examples** that match your stack and naming conventions. Favor clarity and realism over volume.

---

### 4) Give the **right context**: docs & APIs over generic text
Agents do better when the plan bundles *relevant* documentation:

- **DocPrompting** (retrieve the relevant API docs and show them in‑prompt) consistently improves NL→code accuracy, especially on unfamiliar libraries.
- Broader studies on retrieval‑augmented code generation show that **API details and nearby context** help more than “similar snippets” (which can add noise).

**Takeaway:** Link or inlay **minimal, high‑relevance docs** (function signatures, constraints, versions), not long tutorial prose.

---

### 5) Balance *what* vs *how* (don’t overconstrain)
- **Structured plans** (what + coarse how) help, but **over‑tight format constraints** can hamper reasoning on complex tasks (e.g., forcing heavy JSON schemas during reasoning). Use constraints for outputs that must be parsed, not for the agent’s internal thought.
- Keep crucial instructions **at the top (and/or recap at the end)**: models show a “lost‑in‑the‑middle” effect in long contexts; primacy/recency placement helps.
- In interactive settings, **hierarchical prompting** (summary → action) improves success on long, cluttered observations—use summaries of large pages/logs before asking for actions.

**Takeaway:** State **non‑negotiable “what”** (requirements, constraints, success tests) and give a **coarse “how”** (milestones/subtasks). Avoid micromanaging every keystep or forcing overly rigid intermediate formats.

---

### 6) Close the loop: verification & reflection
Prompted **reflection/repair loops** (Self‑Refine; Reflexion) improve coding and reasoning by injecting critique and retry stages using feedback from tests/tools. Your plan should explicitly ask the agent to **review failures, update the plan, then retry**.

---

## A one‑page implementation‑plan template (drop‑in)

```markdown
# Implementation Plan — <Project / Issue ID>

## 1) Goal (WHAT)
- One-sentence goal:
- Scope boundaries (in/out):
- Non-functional constraints (perf, security, licensing, style):

## 2) Success Criteria & Oracle
- Acceptance tests to pass (list test names / cases with exact I/O)
- Demo scenario (exact CLI/curl/script to run)
- Definition of Done (bulleted, unambiguous)

## 3) Context (KEEP TIGHT & RELEVANT)
- Codebase entry points/files likely involved:
- API/contracts to respect (version, signatures):
- Links or *snippets* from docs (only the needed bits):

## 4) Plan (COARSE HOW → STEPS)
1. [Milestone A] (what to change/where)
2. [Milestone B] …
3. [Milestone C] …
> After each milestone: run tests → record failures → update plan.

## 5) Examples (FEW-SHOT)
- Mini example of expected function/class structure (idiomatic names)
- Example of acceptable input/output transformation

## 6) Tooling Interface (for the agent)
- Commands allowed (build/test/run) and limits
- Files it may edit
- Cost/step budget, and when to stop and escalate

## 7) Risks & Rollback
- Likely failure modes + how to detect them
- Quick rollback instructions

## 8) Output Format (FOR HUMANS/PIPELINES)
- Required artifacts (PR diff, changelog, test report JSON)
- Schema only for **final** structured outputs (avoid constraining intermediate reasoning)
```

This template bakes in the evidence‑based elements above: explicit goal+tests (what), a decomposed plan (how), minimal but targeted docs, and a couple of in‑domain examples, with a verification/repair loop.

---

## FAQ based on your questions

- **“Are declarative sentences enough?”**  
  Usually not. Plans that *explicitly decompose* the work and interleave execution with verification outperform single‑pass instructions on both generic reasoning and coding tasks.

- **“Should I include code examples?”**  
  Yes—1–3 concise, *stack‑matched* examples with realistic naming. Retrieval‑picked examples boost success; poor or off‑domain examples can hurt.

- **“Should the plan focus on how vs what?”**  
  **Both**, but at different levels: make the *what* (requirements, tests, constraints) **hard** and the *how* **coarse** (milestones/subtasks). Over‑prescribing formats or step granularity can degrade problem‑solving; use structure mostly for final outputs and guardrails.

- **“Anything about where to put key details?”**  
  Yes—put the critical requirements, constraints, and tests at the **top** (and optionally recap at the end) to mitigate long‑context position sensitivity.

---

## Optional refinements (when you have them)

- **Provide an Agent‑Computer Interface (ACI)**: whitelist actions (view/edit/run tests), and return concise, structured feedback after each action—this alone improved SWE‑bench performance in **SWE‑agent**.
- **Use hierarchical prompts on large pages/logs**: summarize first, then act.
- **Ask the agent to plan first, then execute** (“plan, then act; revise if tests fail”).

