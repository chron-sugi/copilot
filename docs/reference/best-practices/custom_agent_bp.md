Purpose: Tell Copilot how to behave and how to think.

## Include:

* Persona framing — e.g. “You are a Senior Front-End Engineer specializing in JavaScript, CSS, and accessibility.”

* Reasoning heuristics — “First analyze, then propose fix; cite reasoning inline.”

* Output structure — “Always return result + short rationale + checklist.”

Tool use rules — “Use built-in explainCode() or generateTests() tools when applicable.”

Interaction tone — “Be concise, assertive, professional.”

Internal goals — “Prioritize maintainability and readability over micro-optimizations.”

## Exclude:

* Specific coding standards (naming, syntax, etc.) → move to instructions file.

* Project-specific context (library versions, folder names).

* Example code (burns tokens fast and crowds context).

## Rationale:
This layer is agentic meta-behavior — it’s how the LLM interprets your task environment. Research on prompt specialization (Anthropic’s “Constitutional AI”, OpenAI’s system-prompt tuning, etc.) shows that separating “how to reason” from “what to do” yields more stable output.

## Heuristics 
Make every line start with a verb (strong imperative signal).

Avoid long clauses after “;” where possible (LLMs sometimes truncate the “second half”).

Separate reasoning order and output style (you already mostly do, just minor polish).