# Implementation Plan Request — Evidence-Based Template v2

## 🎯 CRITICAL CONSTRAINTS (READ FIRST)

**ROLE:** Tech-agnostic senior software architect and implementation planner

**YOUR TASK:**
Generate a precise, verifiable implementation plan for a new feature.

**Hard limit: < 4,000 tokens total output.**
Target: 2,800–3,600 tokens for optimal detail density.

**MANDATORY FIRST STEP:**
Before planning, you MUST thoroughly analyze the existing codebase:
- Repository structure, technology stack, architectural patterns
- Build/test/CI systems, configurations, environment settings
- Database schemas, migrations, data models, API contracts
- Existing patterns (naming, testing, error handling, similar features)
- Dependencies, constraints (performance, security, compliance)
- Event/message schemas, feature flags, logging/metrics, IaC files

**OUTPUT REQUIREMENTS:**
1. Use Chain-of-Thought reasoning internally but **keep output concise**
2. Output only the structured sections below (no verbose explanations)
3. Make plans **actionable and verifiable** (tests after each milestone)
4. Use **tech-agnostic language** (patterns over framework names: "HTTP handler" not "Express route")
5. State unknowns explicitly in "Open Questions & Assumptions"—never speculate
6. Adhere strictly to per-section token budgets

---

## 📋 FEATURE SPECIFICATION

### Feature Brief
- **Feature Name:** {{FEATURE_NAME}}
- **One-Sentence Goal:** {{ONE_SENTENCE_GOAL}}
- **In Scope:** {{IN_SCOPE}}
- **Out of Scope:** {{OUT_OF_SCOPE}}
- **Non-Functional Constraints:** {{NFR_CONSTRAINTS}}
  - Performance: {{PERF_REQUIREMENTS}}
  - Security: {{SECURITY_REQUIREMENTS}}
  - Compliance: {{COMPLIANCE_REQUIREMENTS}}
  - Accessibility: {{A11Y_REQUIREMENTS}}
  - Licensing: {{LICENSE_CONSTRAINTS}}
  - Style/Standards: {{STYLE_STANDARDS}}

### Success Criteria
- **Definition of Done:** {{DEFINITION_OF_DONE}}
- **Acceptance Tests (3–8 specific test cases):**
  - Test 1: {{TEST_NAME_1}}
    - Scenario: {{GIVEN_WHEN_THEN_1}}
    - Input: {{INPUT_1}}
    - Expected: {{EXPECTED_OUTPUT_1}}
  - Test 2: {{TEST_NAME_2}}
    - Scenario: {{GIVEN_WHEN_THEN_2}}
    - Input: {{INPUT_2}}
    - Expected: {{EXPECTED_OUTPUT_2}}
  - [Add 1–6 more tests as needed]
- **Demo Script:** {{DEMO_COMMANDS_OR_STEPS}}

### Technical Context
- **Repository Access:** {{REPO_URL_OR_PATH}}
- **Entry Points/Modules Likely Involved:** {{ENTRY_POINTS}}
- **APIs/Contracts to Respect:** {{API_CONTRACTS}}
  - Versions: {{VERSIONS}}
  - Signatures: {{KEY_SIGNATURES}}
  - Backward Compatibility Requirements: {{COMPAT_REQUIREMENTS}}
- **Config/Env Variables & Feature Flags:** {{CONFIG_AND_FLAGS}}
- **Data Models/DB Schemas/Migrations:** {{SCHEMAS_AND_MODELS}}
- **Relevant Documentation (only essential snippets):** {{DOC_SNIPPETS}}
- **Known Constraints:**
  - Authentication/Authorization: {{AUTH_CONSTRAINTS}}
  - Multi-tenancy: {{TENANCY_CONSTRAINTS}}
  - Rate Limits: {{RATE_LIMITS}}
  - Data Locality/Residency: {{DATA_LOCALITY}}
- **Allowed Tools/Commands:**
  - Read/Edit Permissions: {{PERMISSIONS}}
  - Build Command: {{BUILD_CMD}}
  - Test Command: {{TEST_CMD}}
  - Run/Deploy Command: {{RUN_CMD}}

---

## 📤 OUTPUT FORMAT (STRICT ORDER — FOLLOW TOKEN BUDGETS)

Generate your plan using exactly these sections in order:

### 1. Repository Reconnaissance (≤ 450 tokens)
**Purpose:** Demonstrate understanding of the codebase BEFORE planning.

Include:
- Project structure summary (monorepo/multi-repo, key directories)
- Technology stack identified (languages, frameworks, libraries)
- Build/test systems and CI/CD setup
- Configuration management approach
- Database/schema/migration strategy
- Existing patterns for similar functionality
- API contracts and integration points
- Potential conflicts or risks discovered
- Files/modules that will be involved

⚠️ This section is mandatory—no generic assumptions allowed.

---

### 2. Goal & Scope (≤ 150 tokens)
- One-sentence goal
- In/out of scope boundaries
- Non-functional constraints (performance, security, compliance, style)

---

### 3. Success Criteria & Acceptance Tests (≤ 400 tokens)
- Definition of Done (3–5 bullets)
- 3–8 acceptance tests with exact inputs/outputs or CLI/cURL examples
- Demo scenario (specific commands to demonstrate feature works)

---

### 4. Implementation Milestones (≤ 1,200 tokens)
Break work into 4–8 coarse-grained milestones:

**For each milestone:**
- **Name:** Brief descriptor
- **What:** What will be built/changed
- **Where:** Specific file paths or modules
- **Validation:** How to verify completion (test command + expected result)

**Format:**
```
Milestone 1: [Name]
- What: [Description of changes]
- Where: [file/path/module.ext]
- Validation: Run `[test command]`, expect [specific output/behavior]

Milestone 2: [Name]
...
```

⚠️ After EACH milestone, tests must be run and failures addressed before proceeding.

---

### 5. Code Patterns & Examples (≤ 300 tokens)
Provide 1–3 minimal code sketches (≤ 15 lines each) showing:
- Expected function/class signatures (using project's actual naming conventions)
- Input/output transformations
- Integration points with existing code

Use realistic, idiomatic examples extracted from the codebase analysis.
Focus on interfaces and contracts, not full implementations.

---

### 6. Testing Strategy (≤ 300 tokens)
- **Unit Tests:** What to test at function/class level
- **Integration Tests:** Component interactions to verify
- **End-to-End Tests:** User scenarios to validate
- **Test Execution:** Specific commands and expected outputs
- **Coverage Target:** Minimum acceptable coverage (if applicable)

---

### 7. Observability, Security & Compliance (≤ 350 tokens)

**Observability:**
- Logging: What events/errors to log, at what levels
- Metrics: What to measure (latency, error rates, usage)
- Tracing: Distributed tracing requirements (if applicable)
- Alerting: Conditions that should trigger alerts

**Security & Privacy:**
- Authentication/Authorization requirements
- Data encryption (in transit, at rest)
- Input validation and sanitization
- Secrets management
- PII/sensitive data handling

**Compliance:**
- Regulatory requirements (GDPR, HIPAA, SOC2, etc.)
- Audit logging needs
- Data retention policies

---

### 8. Release, Deployment & Rollback (≤ 350 tokens)

**Deployment Strategy:**
- Deployment method (blue-green, canary, rolling, etc.)
- Feature flags for gradual rollout
- Database migration approach (if applicable)
- Dependency deployment order

**Rollback Plan:**
- Conditions triggering rollback
- Rollback procedure (step-by-step)
- Data migration rollback (if applicable)
- Quick rollback command/script

**Post-Deployment Validation:**
- Smoke tests to run immediately after deployment
- Monitoring to watch for first 24–48 hours

---

### 9. Resource Estimates & Constraints (≤ 300 tokens)

**Effort Estimate:**
- Complexity: [Simple / Moderate / Complex]
- Estimated time: [e.g., "2–4 hours", "1–2 days", "1–2 weeks"]
- Justification: [Brief reasoning]

**Scope:**
- Files to create: [count and paths]
- Files to modify: [count and paths]
- Tests to write: [estimated count]
- Database migrations: [count]

**Resource Budgets:**
- Max token/cost budget for implementation
- Latency requirements (if user-facing)
- Max reflection/retry attempts: ≤ 2 iterations
- Context window considerations

**Escalation Conditions (when to stop and ask for human help):**
- [Condition 1]
- [Condition 2]
- [Condition 3]

---

### 10. Risks & Mitigation (≤ 300 tokens)
Identify 3–6 likely failure modes:

**For each risk:**
- **Risk:** [What could go wrong]
- **Likelihood:** [Low / Medium / High]
- **Impact:** [Low / Medium / High]
- **Detection:** [How to identify this problem early]
- **Mitigation:** [How to prevent or recover]

Include at least one risk each for: technical, security, and operational concerns.

---

### 11. Open Questions & Assumptions (≤ 250 tokens)

**Open Questions (require clarification):**
- [Question 1]
- [Question 2]
- [Question 3]

**Assumptions (explicitly stated):**
- [Assumption 1]
- [Assumption 2]
- [Assumption 3]

⚠️ Never speculate beyond these stated assumptions. If uncertain, list as Open Question.

---

### 12. Self-Critique & Validation (≤ 200 tokens)

Review your plan and identify:
- Potential gaps or weaknesses
- Areas of uncertainty
- Suggested improvements
- Alternative approaches considered (and why rejected)

This is your one opportunity for self-reflection—use it to catch issues before implementation.

---

### 13. Executive Summary (≤ 150 tokens)

**Recap in 4–6 bullets:**
- [Key point 1: What's being built]
- [Key point 2: Main technical approach]
- [Key point 3: Biggest risk/challenge]
- [Key point 4: Success criteria]
- [Optional: Timeline/effort]
- [Optional: Dependencies/blockers]

---

## 📐 STYLE & QUALITY RULES

✅ **DO:**
- Extract real examples from codebase (Repository Recon section)
- Use tech-agnostic patterns ("ORM migration" not "Alembic migration")
- Place critical constraints at top of each section
- Keep milestone descriptions actionable and verifiable
- State unknowns explicitly in Open Questions
- Ruthlessly prune low-relevance context
- Use concise bullets (≤ 2 sentences each)

❌ **DON'T:**
- Exceed 4,000 tokens total
- Include generic tutorial content or advice
- Over-specify implementation details (avoid micromanaging HOW)
- Add unverified/speculative information about the codebase
- Force rigid intermediate formats (JSON schemas during reasoning)
- Include more than 3 code examples
- Bury critical information in the middle of long sections
- Show verbose reasoning traces (keep output concise)

---

## ✅ PRE-GENERATION CHECKLIST FOR THE MODEL

Before generating output, verify:

1. ☑️ I have read and understood all provided project materials (code, configs, schemas, docs)
2. ☑️ I have decomposed the goal into verifiable milestones with validation steps
3. ☑️ I have integrated acceptance tests and Definition of Done
4. ☑️ I have included verification loops (tests after each milestone)
5. ☑️ I have applied resource limits and escalation conditions
6. ☑️ I have explicitly stated all assumptions and open questions
7. ☑️ I have identified risks and mitigation strategies
8. ☑️ I have adhered to per-section token budgets
9. ☑️ My total output will be < 4,000 tokens
10. ☑️ I have used tech-agnostic language (patterns over framework names)

---

## 📦 END OF TEMPLATE

**To use this template:**
1. Replace all {{PLACEHOLDERS}} with your feature details
2. Delete this instruction section
3. Submit to GPT-5 or Claude Sonnet 4.5 with access to your codebase
4. Receive a focused, verifiable implementation plan < 4,000 tokens
