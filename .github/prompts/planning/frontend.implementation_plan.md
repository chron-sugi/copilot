

# Frontend Implementation Spec

## ROLE

Generate a minimal, actionable implementation spec for a React/TypeScript feature.
Follow conventions from system prompt. This spec defines *what* to build.

**Token Budget:** 2,500–3,500 tokens (hard limit: 4,000)

---

## CRITICAL REMINDERS

### Simplicity
- **Minimal solution only.** No unrequested features, components, or abstractions.
- If tempted to add something "just in case" — don't.

### Uncertainty
- **Ask before assuming.** If requirements are ambiguous, ask.
- Do not proceed with guesses.

### Spec Style
- **Prose requirements over code.** Describe what components should do, not how.
- **Props and types without implementations.** Show interfaces, not full components.
- **Schemas are contracts.** Zod schemas and TypeScript types belong in specs.

---

## ASK ME FIRST

Before generating the spec, ask clarifying questions if:

- [ ] Requirements are ambiguous or conflicting
- [ ] Component hierarchy is unclear
- [ ] State management approach is uncertain (local vs. Zustand vs. URL)
- [ ] Data fetching needs are unclear (what endpoints, what shape)
- [ ] Accessibility requirements need clarification
- [ ] Routing/navigation behavior is unspecified

**Do not proceed with assumptions. Ask.**

---

## 🛑 STOP CONDITIONS

During implementation, stop and ask if:

- Requirement becomes ambiguous
- Changes needed outside specified scope (other slices, shared components)
- Test failures persist after 2 attempts
- Tempted to add unspecified functionality
- Need to modify existing components beyond what's scoped

---

## FEATURE BRIEF

*Provide natural language. I will extract structure.*

**What I need:**
{{Describe the feature. What should it do? What user problem does it solve?}}

**Key behaviors:**
{{2-5 critical behaviors in plain language}}

**UI states:**
{{Loading, error, empty, success — what should each look like?}}

**Out of scope:**
{{Explicitly excluded}}

**Constraints:**
{{Accessibility, responsive, performance — or "none"}}

---

## CONTEXT

### Files
```
{{FILE_1}} — {{purpose}}
{{FILE_2}} — {{purpose}}
{{FILE_3}} — {{purpose}}
```

### Routes (if applicable)
```
{{ROUTE_PATH}} — {{page/component}}
```

### Environment
- Layer: {{app / pages / widgets / features / entities / shared}}
- Slice: {{slice name, or "new slice: name"}}
- Data source: {{API endpoint, existing query, local only}}

### Commands
- Lint: `npm run lint`
- Type check: `npm run typecheck`
- Test: `npm run test -- {{path}}`
- Dev: `npm run dev`

---

## OUTPUT FORMAT

### 1. Clarifying Questions (FIRST)

List questions about ambiguous requirements, component hierarchy, state, data, or accessibility.

*If none, state "Requirements are clear" and proceed.*

---

### 2. Codebase Analysis (≤300 tokens)

- Relevant existing patterns (with file references)
- Components to create/modify
- Hooks to create/modify
- Integration points
- Risks

*Reference actual code. No generic assumptions.*

---

### 3. Scope Confirmation (≤100 tokens)

- Goal: [one sentence]
- In scope: [list]
- Out of scope: [list]
- Constraints: [list or "none"]

---

### 4. Component Hierarchy (≤150 tokens)

```
PageOrFeature
├── ComponentA
│   ├── SubComponentA1
│   └── SubComponentA2
└── ComponentB
```

Note which are new vs. existing.

---

### 5. Types & Schemas (≤200 tokens)

Define types and Zod schemas needed.

```typescript
type ComponentProps = {
  id: string;
  onAction?: (id: string) => void;
};

const ResponseSchema = z.object({
  id: z.string(),
  name: z.string(),
});

type Response = z.infer<typeof ResponseSchema>;
```

*Show types and props. Note new vs. modifications.*

---

### 6. State Management (≤150 tokens)

| State | Type | Location |
|-------|------|----------|
| {{state name}} | server / client / URL / local | {{TanStack Query / Zustand store / router param / useState}} |

Note any new stores or queries to create.

---

### 7. Milestones (≤800 tokens)

3–5 milestones. Minimal scope each.

```
## Milestone N: [Name]

**What:** [Changes to make]

**Where:** 
- `src/features/{{slice}}/ui/Component.tsx` — [new/modify]
- `src/features/{{slice}}/api/useQuery.ts` — [new/modify]

**UI States:**
- Loading: [what to show]
- Error: [what to show]
- Empty: [what to show]
- Success: [what to show]

**Validation:** 
- Run: `npm run test -- src/features/{{slice}}`
- Expect: [output]

**Proposed Tests:**
- [ ] renders loading state
- [ ] renders error state
- [ ] renders empty state
- [ ] renders data correctly
- [ ] handles user interaction
```

*I will review proposed tests before implementation.*

**Milestone Completion Checklist:**
- [ ] Tests pass
- [ ] `npm run lint` clean
- [ ] `npm run typecheck` clean
- [ ] All UI states handled
- [ ] No console.log, debugging artifacts, commented code
- [ ] Accessible (labels, keyboard, focus)

⚠️ Each milestone must pass checklist before proceeding.

---

### 8. Proposed Test Coverage (≤250 tokens)

**Component Tests:**
| Component | Scenarios |
|-----------|-----------|
| {{Component}} | renders, loading, error, empty, interaction |

**Hook Tests (if applicable):**
| Hook | Scenarios |
|------|-----------|
| {{useHook}} | returns data, handles error, handles loading |

**User Interactions:**
- Click {{element}} → {{expected behavior}}
- Submit {{form}} → {{expected behavior}}
- Navigate {{action}} → {{expected behavior}}

*Proposals. I will confirm before implementation.*

---

### 9. Accessibility Requirements (≤100 tokens)

- Keyboard navigation: {{requirements}}
- Focus management: {{requirements}}
- Screen reader: {{labels, announcements}}
- ARIA: {{specific attributes if needed}}

---

### 10. Risks (≤100 tokens)

| Risk | Impact | Mitigation |
|------|--------|------------|
| {{risk}} | H/M/L | {{action}} |

---

### 11. Open Questions & Assumptions (≤100 tokens)

**Questions:**
- {{unresolved}}

**Assumptions:**
- {{proceeding as if true}}

---

### 12. Estimate (≤50 tokens)

- Complexity: Simple / Moderate / Complex
- Components: {{N}} new, {{M}} modify
- Hooks: {{N}} new, {{M}} modify
- Tests: ~{{count}}

---

## CONDITIONAL SECTIONS

*Include only if applicable:*

### Routing — if adding/modifying routes
- Route path: {{path}}
- Params: {{url params}}
- Navigation: {{how users get here}}

### Forms — if feature includes forms
- Fields: {{list}}
- Validation: {{Zod schema name}}
- Submission: {{mutation or action}}

### Animations — if motion is required
- Transitions: {{what animates}}
- Library: {{Tailwind transitions / Framer Motion / CSS}}

---

## STYLE REMINDERS

**Do:**
- Ask before assuming
- Minimal solutions only
- Prose requirements, not implementation code
- Reference actual codebase patterns
- Specify all UI states

**Don't:**
- Add unrequested features or components
- Include full component implementations
- Guess at requirements
- Skip the milestone checklist
- Forget accessibility