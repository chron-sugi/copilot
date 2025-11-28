# Implementation Plan Request Template

## CRITICAL CONSTRAINTS (Read First)
- **Token Limit**: Your implementation plan must be < 4,000 tokens
- **Codebase Analysis Required**: You MUST thoroughly analyze the existing codebase before planning
- **Reasoning Approach**: Use Chain-of-Thought reasoning; show your understanding before planning
- **Output**: A structured, actionable implementation plan with verifiable milestones

---

## YOUR TASK

Create a comprehensive implementation plan for the following feature:

**Feature Description:**
[REPLACE: Describe the feature/functionality to be implemented in 2-4 sentences]

**Business Context:**
[REPLACE: Why is this needed? What problem does it solve?]

**User/Stakeholder Requirements:**
[REPLACE: List specific requirements, or write "See feature description above"]

---

## STEP 1: ANALYZE THE CODEBASE (Required)

Before creating your plan, you MUST:

1. **Identify the project structure and technology stack**
   - What languages, frameworks, and libraries are in use?
   - What architectural patterns are evident (MVC, microservices, monolith, etc.)?
   - What build/test systems exist?

2. **Locate relevant files and modules**
   - Which existing files/modules will this feature interact with?
   - What are the entry points for similar functionality?
   - Where do configuration files, schemas, and models reside?

3. **Understand existing patterns and conventions**
   - What naming conventions are used?
   - How is similar functionality currently implemented?
   - What testing patterns exist?
   - What error handling patterns are used?

4. **Identify constraints and dependencies**
   - What APIs, databases, or external services must be respected?
   - What performance, security, or compliance requirements exist?
   - What are the current versions of key dependencies?

**Show your findings in a brief "Codebase Analysis" section (200-400 tokens max)** before proceeding to the plan.

---

## STEP 2: CREATE THE IMPLEMENTATION PLAN

Structure your plan using the sections below. Balance specificity with brevity—be concrete about WHAT and WHY, but keep HOW at a milestone level (not step-by-step instructions).

### Format Your Plan As Follows:

#### 1. GOAL & SCOPE
- **One-sentence goal**: [Clear, measurable objective]
- **In scope**: [What this feature includes]
- **Out of scope**: [What it explicitly does NOT include]
- **Non-functional constraints**: [Performance, security, licensing, style requirements]

#### 2. SUCCESS CRITERIA
- **Acceptance tests**: List 2-4 specific test cases with expected inputs/outputs
- **Demo scenario**: Exact command/script/interaction to demonstrate the feature works
- **Definition of Done**: 3-5 bulleted, unambiguous completion criteria

#### 3. TECHNICAL CONTEXT
- **Files/modules to modify**: List specific paths and what changes (create/modify/delete)
- **APIs/contracts to respect**: Critical interfaces, signatures, or protocols
- **Key dependencies**: Libraries, services, or data structures this feature relies on
- **Relevant documentation snippets**: Only include essential API details, not prose

⚠️ Keep this section focused—only include high-signal context. Exclude generic or obvious information.

#### 4. IMPLEMENTATION MILESTONES
Break the work into 3-6 coarse-grained milestones. For each:
- **What** will be built/changed
- **Where** in the codebase (file paths/modules)
- **Validation**: How to verify this milestone is complete (test to run, expected output)

**Example format:**
1. **[Milestone Name]**: Create data model for [X] in `path/to/file`
   - Validation: Run `test command`, expect [specific output]
2. **[Milestone Name]**: Implement API endpoint for [Y]
   - Validation: `curl` command returns expected JSON schema
3. **[Milestone Name]**: Add UI component that calls the API
   - Validation: Manual test shows [specific behavior]

⚠️ After each milestone, tests should be run and failures addressed before proceeding.

#### 5. CODE PATTERNS & EXAMPLES
Provide 1-3 **minimal** code sketches showing:
- Expected function/class signatures (using project's naming conventions)
- Input/output transformations
- Integration points with existing code

Use realistic, idiomatic examples that match the project's style. Focus on interfaces and contracts, not full implementations.

#### 6. TESTING STRATEGY
- **Unit tests**: What should be tested at the function/class level?
- **Integration tests**: What interactions between components need verification?
- **End-to-end tests**: What user scenarios should be validated?
- **Test execution**: Specific commands to run tests

#### 7. RISKS & MITIGATION
Identify 2-4 likely failure modes:
- **Risk**: [What could go wrong]
- **Detection**: [How to identify this problem early]
- **Mitigation**: [How to prevent or recover]

Include rollback strategy if the feature needs to be reverted.

#### 8. RESOURCE CONSTRAINTS
- **Estimated complexity**: [Simple/Moderate/Complex - with brief justification]
- **Implementation time estimate**: [Rough range, e.g., "2-4 hours" or "1-2 days"]
- **Dependencies on other work**: Any blockers or prerequisites?
- **Breaking changes**: Will this require migration or coordination?

---

## QUALITY GUIDELINES

As you create the plan:

✅ **DO:**
- Use Chain-of-Thought reasoning to show your understanding
- Extract real examples from the codebase (don't invent hypothetical ones)
- Place critical constraints at the top of each section
- Keep milestone descriptions actionable and verifiable
- Identify specific files/functions to modify
- Include concrete test commands and expected outputs
- Use the project's actual naming conventions and patterns
- Prune low-relevance context ruthlessly

❌ **DO NOT:**
- Exceed 4,000 tokens for the complete plan
- Include generic advice or tutorial content
- Over-specify implementation details (avoid micromanaging HOW)
- Add speculative or unverified information about the codebase
- Force rigid intermediate formats (JSON schemas during reasoning)
- Include more than 3 code examples
- Bury critical information in the middle of long sections

---

## OUTPUT FORMAT

Present your complete response in this order:

1. **Codebase Analysis** (200-400 tokens)
   - Brief findings from your exploration

2. **Implementation Plan** (3,200-3,600 tokens)
   - Sections 1-8 as specified above

3. **Total Token Count** (for transparency)
   - Report the approximate token count of your plan

---

## ADDITIONAL CONTEXT (Optional)

[REPLACE: Add any additional context, links to relevant documentation, or specific technical constraints that aren't captured above. Delete this section if not needed.]

---

## EXAMPLE FEATURE REQUEST (Delete Before Use)

**Feature Description:**
Add user authentication using JWT tokens. Users should be able to register, login, and access protected endpoints. Tokens should expire after 24 hours.

**Business Context:**
Currently the application has no authentication. We need to restrict access to certain API endpoints to authorized users only.

**User/Stakeholder Requirements:**
- New users can register with email and password
- Existing users can login and receive a JWT token
- Protected endpoints reject requests without valid tokens
- Tokens expire and require re-authentication
- Passwords must be hashed, never stored in plain text

[Rest of the form would be filled in per the template above]
