# Instruction Rules Template

Use this structure to keep instruction sets consistent, easy to review, and machine friendly. Replace placeholder rows with your actual rules or duplicate the template block as needed.

## Legend

| Priority | Meaning |
| --- | --- |
| `P0` | MUST follow; breaking this invalidates the request. |
| `P1` | SHOULD follow; deviations need an explicit rationale. |
| `P2` | CAN follow; use when helpful but optional. |

## Rules

| Rule ID | Priority | Title | Instruction | Notes / Examples |
| --- | --- | --- | --- | --- |
| `R1` | `P0` | Primary guidance | Describe the non‑negotiable rule here. | Optional: explain intent, dependencies, or link to docs. |
| `R2` | `P1` | Secondary guidance | Capture best practices or preferences. | Optional example: “Prefer async APIs over sync ones.” |
| `R3` | `P2` | Nice-to-have | Specify optional behaviors. | Optional: when to skip this rule. |

## References (optional)

- Link to related specifications, coding standards, or policy docs.
- Note rule dependencies (e.g., `R3` depends on `R1`).
