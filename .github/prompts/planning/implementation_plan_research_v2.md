---

---

# Implementation Plan Research - Comprehensive Evidence-Based Guide

## What the evidence says (and what to include)

### 0) Start with Chain-of-Thought (the foundation)

Before diving into advanced techniques, understand the baseline:

- **Chain-of-Thought (CoT) prompting** asks models to generate intermediate reasoning steps before answering, significantly improving performance on complex tasks.
- Many advanced techniques (Plan-and-Solve, Tree-of-Thoughts, Reflexion) build upon or extend CoT.
- **Key principle**: Making reasoning explicit improves accuracy and debuggability.

**When to use**: Start with simple CoT for most tasks. Only escalate to more complex techniques (ToT, multi-agent systems) when CoT proves insufficient.

---

### 1) Provide a decomposed plan (not just "what")

A large body of work shows that **explicit task decomposition** boosts reliability across domains:

- **Plan-and-Solve** (Wang et al., ACL 2023): Asks the model to (a) devise a plan of subtasks, then (b) execute them. Outperforms Zero-shot-CoT by large margins across all datasets; comparable with 8-shot CoT on math reasoning. Specifically addresses calculation errors, missing-step errors, and semantic misunderstanding.

- **Least-to-Most Prompting**: Decomposes problems so each subproblem's output becomes input for the next. GPT-3 achieves 99% accuracy on SCAN with 14 exemplars vs. only 16% with standard CoT. Particularly effective on problems harder than the training examples.

- **Decomposed Prompting** (Khot et al., 2023): Delegates sub-tasks to a library of prompting-based LLMs, where each prompt can be optimized for its specific sub-task. Can incorporate symbolic retrieval and even replace sub-tasks with trained models.

- **Tree-of-Thoughts (ToT)** (Yao et al., 2023): Enables exploration and selection among alternative sub-plans through tree search. Shows dramatic gains: Game of 24 improved from 4% success (GPT-4 with CoT) to 74% (GPT-4 with ToT).

  ⚠️ **Important caveats**:
  - **Resource-intensive**: ToT requires many more API calls and tokens than linear approaches
  - **Can explore redundant paths**: No built-in mechanism to prioritize promising branches
  - **Latency**: Multiple LLM calls significantly increase response time
  - **Cost**: Easily 10-100x more expensive than simple CoT
  - **Recent improvements**: Tree of Uncertain Thoughts (TouT) adds uncertainty quantification to address some limitations

- **ReAct (Reason+Act)** (Yao et al., ICLR 2023): Interleaves planning with tool actions. Reasoning traces help induce, track, and update action plans while actions allow interfacing with external sources. Beats reason-only and act-only baselines; on ALFWorld and WebShop, outperforms imitation and RL methods by 34% and 10% absolute success rate.

- **Semantic Chain-of-Thought (SCoT)**: Outperforms standard CoT by up to 13.79% on code generation benchmarks by maintaining better semantic tracking of variables and conditions.

- For **software** specifically, **CodePlan** (Microsoft Research, FSE 2024) frames repository-level coding as a planning problem (multi-step chain of edits across files). Achieved 5/7 repositories passing validity checks vs. 0/7 for baselines. Uses incremental dependency analysis and adaptive planning for tasks requiring changes to 2-97 files.

**Takeaway:** Your implementation plan should **decompose the goal into verifiable steps** and let the agent iterate step-by-step, rather than only stating the end goal. Start simple (CoT or Plan-and-Solve) before escalating to resource-intensive approaches like ToT.

---

### 2) Include acceptance tests / a correctness oracle

Agents that can *run* tests and get executable feedback learn and correct faster:

- **SWE-bench and SWE-agent** (Princeton, NeurIPS 2024): 2,294 real-world GitHub issues from 12 Python repositories. SWE-agent achieved 12.5% pass@1 at publication, demonstrating that giving agents task oracles (human tests) and tight feedback/guardrails raises real-world bug-fix success vs. freeform shells.

  **Recent updates**:
  - **SWE-bench Verified** (Aug 2024): 500 human-validated test cases for higher-quality evaluation
  - **Current SOTA**: Claude 3.5 Sonnet achieves **49%** on SWE-bench Verified (as of late 2024)
  - **SWE-bench Pro**: 1,865 instances across 41 repos including commercial code

- **TiCoder** (Microsoft Research): Test-driven interactive generation improves pass@1 from 48.39% to 70.49% with single query, up to 85.48% with up to 5 queries. User study with 15 programmers confirmed it reduces cognitive load and helps both humans and LLMs. Uses generated tests to prune and rank candidate code suggestions.

**Takeaway:** Put **unit/acceptance tests** (or at least clear I/O examples) directly in the plan, and tell the agent to run them after each milestone. Tests provide executable feedback that prevents error propagation.

---

### 3) Add domain-matched **code examples**

For coding tasks, **few-shot, in-domain examples** are particularly helpful:

- **CEDAR** (Nashid et al., ICSE 2023): Retrieval-selected examples significantly improve program repair and assertion generation. Achieves 76% accuracy on assertion generation (333% better than existing models) and 52% on program repair (189% better than task-specific models). Uses embedding-based retrieval or frequency analysis to select relevant demonstrations.

- **Variable naming and structure matter**: Research consistently shows that realistic, descriptive variable names and idiomatic structure improve LLM code generation performance. While specific performance impacts vary by task and model, the effect is measurable and significant across multiple studies.

- **Example quality >> quantity**: 1-3 high-quality, stack-matched examples with realistic naming outperform larger sets of mediocre or off-domain examples.

- **Ablation studies** confirm that removing good naming conventions or using obfuscated variables degrades performance; descriptive names consistently outperform minimal or obfuscated alternatives.

**Takeaway:** Provide **1-3 short, idiomatic examples** that match your stack and naming conventions. Favor clarity, realism, and domain-match over volume. Poor or off-domain examples can actively hurt performance.

---

### 4) Give the **right context**: docs & APIs over generic text

Agents do better when the plan bundles *relevant* documentation:

- **DocPrompting** (Zhou et al., ICLR 2023): Retrieves relevant API docs and shows them in-prompt. Improves CodeT5 by 2.85% absolute in pass@1 (52% relative gain) and 4.39% in pass@10 on CoNaLa. Can add documentation for new libraries without retraining. Interestingly, LLMs can tolerate mild noise (typos, incorrect parameters) by referencing pre-trained knowledge.

- **API details beat similar snippets**: Recent studies show that "API details and nearby context help more than 'similar snippets' (which can add noise)." In-context code and API information significantly enhance LLM performance, whereas retrieved similar code often introduces noise, **degrading results by up to 15%**.

- **Context pruning**: Not all retrieved context is helpful. Measure retrieval quality and prune low-relevance context to reduce noise.

- **Retrieval quality varies**: "Retrieval models often fail to find the most relevant context." Don't assume retrieved context helps—validate it.

**Takeaway:** Link or inlay **minimal, high-relevance docs** (function signatures, constraints, versions), not long tutorial prose. **Measure retrieval quality** and prune noise. Example code with clear structure contributes more than descriptive text and parameter lists.

---

### 5) Balance *what* vs *how* (don't overconstrain)

- **Structured plans** (what + coarse how) help, but **over-tight format constraints** can hamper reasoning on complex tasks. For example, forcing heavy JSON schemas during reasoning (not just for final output) degrades performance. Use constraints for outputs that must be parsed, not for the agent's internal thought.

- **Lost-in-the-middle effect** (Liu et al., Stanford/UC Berkeley, TACL 2024): Models show a U-shaped performance curve in long contexts—best at using info at beginning/end, degraded performance for middle content. GPT-3.5-Turbo's multi-doc QA performance drops >20% in worst cases. **Even "explicitly long-context models" experience this effect as context increases.**

  **Implication**: Keep crucial instructions **at the top (and/or recap at the end)** to leverage primacy/recency effects.

- **Hierarchical prompting** (summary → action): In interactive settings, improves success on long, cluttered observations. Summarize large pages/logs before asking for actions. Combines well with ReAct (Thought-Action-Observation cycles).

- **Context window management**: Even with large context windows, more context ≠ better performance. Strategic placement and pruning matter more than raw capacity.

**Takeaway:** State **non-negotiable "what"** (requirements, constraints, success tests) clearly at the top. Give a **coarse "how"** (milestones/subtasks) without micromanaging every keystep. Avoid forcing overly rigid intermediate formats. Place critical info at start/end, not middle.

---

### 6) Close the loop: verification & reflection

Prompted **reflection/repair loops** improve coding and reasoning by injecting critique and retry stages using feedback from tests/tools:

- **Self-Refine** (arXiv:2303.17651): Same LLM acts as generator, refiner, and feedback provider. Iterative improvement without supervised training.

- **Reflexion** (arXiv:2303.11366, NeurIPS): Converts environment feedback into linguistic self-reflection; achieves SOTA on HumanEval, MBPP, Leetcode Hard. Uses Actor-Evaluator-Self-Reflection architecture.

- **Recent improvements**: Systems like BESTER combine reflection with tree search for better results.

⚠️ **Important caveats**:
- **Hallucination in self-critique**: Agents can generate confidently wrong self-critiques
- **Diminishing returns**: Too many reflection loops can lead to degradation
- **Cost/latency**: Each reflection round adds API calls and time

**Takeaway:** Your plan should explicitly ask the agent to **review failures, update the plan, then retry**. Self-reflection-guided refinement is more effective than refinement-only. But don't blindly trust agent self-critique—validate against executable tests.

---

### 7) Resource budgeting and practical constraints

⚠️ **Critical considerations often overlooked**:

**Token/Cost Budgets**:
- **ToT**: Can be 10-100x more expensive than linear CoT due to exploring multiple branches
- **Multi-step reflection loops**: Each iteration adds full LLM calls
- **Retrieval-augmented approaches**: Embedding generation and retrieval have costs
- **Best practice**: Set explicit cost/token budgets; use simpler techniques (CoT, Plan-and-Solve) by default

**Latency Considerations**:
- **Sequential tool calls**: Each round-trip adds latency (network + inference time)
- **Parallel execution**: Where possible, structure tasks to allow parallel tool calls
- **Streaming**: For user-facing applications, consider streaming partial results

**Error Propagation**:
- **Multi-step plans**: Errors in early steps compound in later steps
- **Mitigation**: Validate after each milestone, not just at end
- **Incremental testing**: Run tests frequently to catch errors early

**Context Window Limits**:
- Even long-context models have practical limits
- Token limits affect both input and output
- **Best practice**: Design plans that work within typical context windows (8k-32k); don't rely on 100k+ contexts

**Memory Mechanisms**:
- Long-running agents need to track state across many interactions
- Simple approaches: Summarization, key-value stores
- Advanced: Vector databases, hierarchical memory

**Escape Hatches**:
- Define clear conditions for when agent should stop and escalate to humans
- Prevent infinite loops in reflection/retry cycles
- Set maximum retry attempts

---

## Performance optimization principles

### Start Simple, Add Complexity as Needed

**Progression**:
1. **Simple prompt** → 2. **Chain-of-Thought** → 3. **Plan-and-Solve** → 4. **ReAct with tools** → 5. **Tree-of-Thoughts** (if needed)

Don't jump straight to ToT or complex multi-agent systems. Measure performance at each level and only add complexity if there's a clear benefit.

### Measure, Don't Assume

- **Retrieval quality**: Don't assume retrieved context helps—measure it
- **Example effectiveness**: Test whether your few-shot examples actually improve performance
- **Ablation testing**: Remove components to verify they're contributing value
- **Cost/performance tradeoffs**: Track both accuracy and resource usage

### Model-Specific Considerations

- Performance varies significantly across different LLMs
- Techniques optimized for GPT-4 may not transfer to other models
- Newer models (Claude 3.5 Sonnet, GPT-4, etc.) often reduce need for complex prompting
- Test your specific model before committing to elaborate scaffolding

---

## Common user mistakes to avoid

1. **Over-using expensive techniques**: Don't use ToT for simple tasks—wastes resources and time
2. **Trusting retrieved context blindly**: Can degrade performance by up to 15%; measure quality
3. **Too many examples**: 1-3 high-quality examples > 10 mediocre ones
4. **Over-constraining formats**: Rigid JSON schemas during reasoning hurt problem-solving
5. **Ignoring position effects**: Burying key instructions in the middle of long prompts
6. **No escape hatches**: Agent loops without stop conditions can run indefinitely
7. **Skipping incremental tests**: Waiting until end to validate allows error propagation
8. **No version control integration**: For repo-level tasks, not using git branches/commits
9. **Assuming more context = better**: Strategic placement and pruning beat raw context volume
10. **Not setting resource budgets**: Reflection loops and ToT can rack up unexpectedly high costs

---

## A one-page implementation-plan template (drop-in)

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
- ⚠️ Prune low-relevance context to reduce noise

## 4) Plan (COARSE HOW → STEPS)
1. [Milestone A] (what to change/where)
2. [Milestone B] …
3. [Milestone C] …
> After each milestone: run tests → record failures → update plan.
> Incremental validation prevents error propagation.

## 5) Examples (FEW-SHOT)
- Mini example of expected function/class structure (idiomatic names, realistic)
- Example of acceptable input/output transformation
- 1-3 high-quality examples; favor clarity over volume

## 6) Tooling Interface (for the agent)
- Commands allowed (build/test/run) and limits
- Files it may edit
- **Cost/step budget**: Max retries, token limits, when to stop and escalate
- Memory/state management approach (if long-running)

## 7) Risks & Rollback
- Likely failure modes + how to detect them
- Quick rollback instructions
- Escape hatches: when to escalate to humans

## 8) Output Format (FOR HUMANS/PIPELINES)
- Required artifacts (PR diff, changelog, test report JSON)
- Schema only for **final** structured outputs (avoid constraining intermediate reasoning)

## 9) Resource Constraints (NEW)
- Max token/cost budget
- Latency requirements (if user-facing)
- Context window considerations
- Acceptable error rate / retry limits
```

This template bakes in the evidence-based elements: explicit goal+tests (what), a decomposed plan (how), minimal but targeted docs, in-domain examples, verification/repair loop, and **practical resource constraints**.

---

## FAQ based on your questions

**"Are declarative sentences enough?"**
Usually not. Plans that *explicitly decompose* the work and interleave execution with verification outperform single-pass instructions on both generic reasoning and coding tasks. But start simple—basic CoT may be sufficient before escalating to complex multi-step approaches.

**"Should I include code examples?"**
Yes—1-3 concise, *stack-matched* examples with realistic naming. Retrieval-picked examples boost success; poor or off-domain examples can hurt. Quality >> quantity.

**"Should the plan focus on how vs what?"**
**Both**, but at different levels: make the *what* (requirements, tests, constraints) **hard** and the *how* **coarse** (milestones/subtasks). Over-prescribing formats or step granularity can degrade problem-solving; use structure mostly for final outputs and guardrails.

**"Anything about where to put key details?"**
Yes—put the critical requirements, constraints, and tests at the **top** (and optionally recap at the end) to mitigate long-context position sensitivity (lost-in-the-middle effect).

**"How do I know when to use expensive techniques like ToT?"**
Start with simpler approaches (CoT, Plan-and-Solve). Only escalate to ToT if: (1) the task requires exploring multiple solution paths, (2) simpler approaches fail, and (3) you have budget for 10-100x more API calls. Measure cost/performance tradeoffs explicitly.

**"What about model differences?"**
Performance varies significantly across LLMs. Test your specific model. Newer models (Claude 3.5 Sonnet, GPT-4) often reduce need for complex prompting scaffolding—what required ToT with GPT-3 might work with simple CoT on Claude 3.5.

**"How do I prevent runaway costs?"**
Set explicit budgets in your plan: max retries, token limits, cost caps. Implement escape hatches: conditions where agent stops and escalates to human. Monitor costs in real-time for long-running agents.

---

## Optional refinements (when you have them)

**Provide an Agent-Computer Interface (ACI)**:
- Whitelist specific actions (view/edit/run tests)
- Return concise, structured feedback after each action
- SWE-agent showed this alone improves performance
- **Key insight**: LM agents are a new category of end users with unique needs; benefit from specially-built interfaces (like humans benefit from IDEs)

**Use hierarchical prompts on large pages/logs**:
- Summarize first, then act
- Reduces cognitive load on cluttered observations
- Combines well with ReAct cycles

**Memory for long-running agents**:
- Short-term: Conversation context
- Medium-term: Summaries of completed milestones
- Long-term: Vector database of past solutions/patterns

**Version control integration**:
- For repository-level coding, use git branches
- Commit after each successful milestone
- Easy rollback if tests fail

**Context pruning strategies**:
- Remove redundant information in consecutive observations (Diff History approach)
- Prioritize recent and relevant context
- Summarize older context hierarchically

**Ask the agent to plan first, then execute**:
- "Plan, then act; revise if tests fail"
- Can inspect and approve plan before execution
- Allows cost estimation before committing

---

## References and further reading

### Core Techniques
- **Plan-and-Solve**: Wang et al., ACL 2023 (arXiv:2305.04091)
- **Least-to-Most**: Published in multiple venues, widely cited
- **Decomposed Prompting**: Khot et al., arXiv:2210.02406, 2023
- **Tree-of-Thoughts**: Yao et al., 2023 (arXiv:2305.10601)
- **ReAct**: Yao et al., ICLR 2023 (arXiv:2210.03629)

### Software-Specific
- **CodePlan**: Microsoft Research, FSE 2024 (arXiv:2309.12499)
- **SWE-bench**: NeurIPS 2024; SWE-bench Verified (Aug 2024)
- **SWE-agent**: Princeton, NeurIPS 2024 (arXiv:2405.15793)
- **TiCoder**: Microsoft Research/UPenn (arXiv:2404.10100)
- **CEDAR**: Nashid et al., ICSE 2023

### Retrieval & Context
- **DocPrompting**: Zhou et al., ICLR 2023 (arXiv:2207.05987)
- **Lost-in-the-middle**: Liu et al., TACL 2024 (arXiv:2307.03172)

### Reflection & Refinement
- **Self-Refine**: arXiv:2303.17651
- **Reflexion**: arXiv:2303.11366, NeurIPS track
- **BESTER**: Recent work combining reflection with tree search

### Foundational
- **Chain-of-Thought**: The foundation for most decomposition approaches
- **Semantic Chain-of-Thought**: Improves code generation tracking

---

## Version history

**v2 (Current)**:
- Removed unverifiable "30 points" claim; replaced with accurately sourced naming impact research
- Added section 0 on Chain-of-Thought as foundation
- Added section 7 on resource budgeting and practical constraints
- Added "Performance optimization principles" section
- Added "Common user mistakes to avoid" section
- Updated SWE-bench numbers to include Verified benchmark and Claude 3.5 Sonnet results
- Added caveats for ToT (resource intensity, latency, cost)
- Added caveats for reflection loops (hallucination, diminishing returns)
- Expanded context pruning and retrieval quality guidance
- Added memory mechanisms discussion
- Added model-specific considerations
- Enhanced template with resource constraints section
- Added References section with paper citations
- Expanded FAQ with cost/model questions

**v1 (Original)**:
- Initial evidence-based implementation plan guide
