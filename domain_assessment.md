Here are the instructions:

-----

**Task**

Assess the codebase for separation of concerns between domain-specific and non-domain (generic) components. Identify entanglement between OS-specific code and reusable generic code. Evaluate what refactoring would be needed to enable reuse for other domains.

Do not make any changes. Only analyze and report.

**Background**

The goal is to have generic components that can be reused across domains (OS, software, hardware, etc.) and domain-specific components that contain the unique logic for each domain.

Generic components should have no knowledge of OS, vendors, families, or any domain concepts.

Domain-specific components should use generic components and add domain-specific behavior.

**Step 1: Identify all modules and their current location**

List all modules in the package.

For each module, note:

- Module name
- Current folder location
- Brief description of what it does

**Step 2: Classify each module**

For each module, classify as:

**Generic (non-domain):**

- Could be used for any domain without modification
- No references to OS, vendor, family, edition, or other OS concepts
- Examples: token matching, canonical name building, file I/O utilities

**Domain-specific (OS):**

- Contains OS-specific logic or models
- References OS concepts like vendor, family, edition, version
- Examples: OS matcher, OS taxonomy registry, OS catalog models

**Mixed (entangled):**

- Contains both generic logic and domain-specific references
- Could be split into generic and domain parts

**Step 3: Analyze imports and dependencies**

For each module, list what it imports.

Identify cross-references:

- Does a generic module import domain-specific code? (problem)
- Does a domain-specific module import generic code? (correct)
- Do domain modules import from each other? (may be fine)

Flag any generic modules that have domain-specific imports. These are entanglement points.

**Step 4: Analyze models and data classes**

List all Pydantic models and data classes.

For each, classify as generic or domain-specific.

Identify any models that mix generic fields with domain-specific fields.

**Step 5: Analyze functions and methods**

For key modules, examine functions and methods.

Identify any that:

- Have generic logic but domain-specific parameter names
- Have hardcoded domain values
- Could be made generic with parameter changes

**Step 6: Identify entanglement patterns**

Report specific entanglement issues found:

Pattern A: Generic module imports domain module

- Which modules?
- What is imported?

Pattern B: Generic function has domain-specific parameters

- Which functions?
- What parameters?

Pattern C: Generic class has domain-specific attributes

- Which classes?
- What attributes?

Pattern D: Domain logic embedded in generic code

- Where?
- What logic?

**Step 7: Assess current folder structure**

Current structure has:

- matching/ (generic?)
- matching/os/ (domain-specific)
- config/os/ (domain-specific)
- catalog/ (generic or domain?)
- others?

Evaluate if folder structure supports separation.

Identify modules in wrong location.

**Step 8: Propose target architecture**

Describe ideal structure:

```
canonix/
├── core/                    # Generic, reusable
│   ├── matching/
│   ├── catalog/
│   ├── builders/
│   └── utils/
├── domains/
│   └── os/                  # OS-specific
│       ├── config/
│       ├── matching/
│       ├── models/
│       └── pipeline/
```

Or whatever structure makes sense based on findings.

**Step 9: List refactoring tasks**

For each entanglement found, describe:

- What needs to change
- Estimated complexity (small, medium, large)
- Dependencies or risks

Prioritize: What gives most reuse value with least effort?

**Step 10: Identify reusable components for other domains**

List components that would be immediately reusable for a new domain (e.g., software cataloging):

- TokenMatcher
- CanonicalBuilder
- CatalogRepository
- Others?

List components that need refactoring before reuse:

- What changes needed?

List components that are inherently domain-specific:

- Will need equivalent for each domain

**Report format**

Provide a summary report with:

1. Module classification table (module, location, classification)
1. Entanglement issues found
1. Proposed target architecture
1. Refactoring task list with priorities
1. Reusability assessment

**Rules**

Be thorough. Check every module. Do not assume based on folder location. Look at actual code and imports. Report findings clearly with specific examples.

**Do not**

Do not make any changes. Do not refactor anything. Only analyze and report. Changes will be planned based on your findings.

-----

Does that cover it?​​​​​​​​​​​​​​​​