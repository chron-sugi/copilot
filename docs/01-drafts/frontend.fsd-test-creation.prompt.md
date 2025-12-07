# Unit Test Plan for SPLinter

A comprehensive testing specification for AI agents to implement tests across the Feature-Sliced Design architecture.

---

## General Testing Principles

When writing tests for this codebase, follow these conventions:

- Colocate test files directly alongside source files using the `.test.ts` or `.test.tsx` suffix
- Import from the file under test using relative imports (`./filename`)
- Prefer `userEvent` over `fireEvent` for simulating user interactions
- Use factories from `@test/utils/factories` for generating test data
- Mock external dependencies at the module level, not inline
- Each test should be independent and not rely on execution order
- Name test cases to describe the expected behavior, not the implementation

---

## Shared Layer Tests

### Chevrotain Lexer (`shared/lib/parser/lexer.ts`)

Write tests for the SPL lexer that tokenizes raw query strings.

**Happy path tests:**
- Tokenize a simple search command with a single field-value pair
- Tokenize multiple field-value pairs separated by spaces
- Tokenize queries with pipe operators separating commands
- Tokenize common SPL commands: search, stats, eval, table, fields, where, sort, dedup, rex, rename
- Tokenize numeric literals including integers, floats, and negative numbers
- Tokenize double-quoted strings preserving whitespace and special characters inside
- Tokenize single-quoted strings
- Tokenize comparison operators: =, !=, <, >, <=, >=
- Tokenize boolean operators: AND, OR, NOT (case insensitive)
- Tokenize wildcards in field values
- Tokenize parentheses for grouping expressions
- Tokenize function calls like `count()`, `sum(field)`, `avg(field)`
- Tokenize the `by` clause keyword
- Tokenize the `as` keyword for field renaming
- Tokenize time modifiers like `earliest`, `latest`
- Tokenize subsearch syntax with square brackets

**Edge case tests:**
- Empty string input returns empty token array with no errors
- Whitespace-only input returns empty token array
- Query with excessive whitespace between tokens normalizes correctly
- Field names containing underscores tokenize as single identifiers
- Field names containing dots (like `host.name`) tokenize correctly
- Field names starting with numbers should either error or tokenize based on SPL rules
- Quoted strings containing escaped quotes
- Quoted strings containing pipe characters (should not split)
- Quoted strings containing equals signs
- Very long field values (1000+ characters)
- Unicode characters in quoted strings
- Newlines within the query (multi-line SPL)
- Tab characters as whitespace
- Consecutive pipe operators
- Trailing pipe with no following command

**Adversarial tests:**
- Unclosed double quote should produce a lexer error with position information
- Unclosed single quote should produce a lexer error
- Invalid characters (backticks, semicolons outside strings) should error
- Null byte injection in query string
- Query consisting only of operators
- Extremely long query (10,000+ characters) completes without timeout
- Binary data or non-UTF8 sequences in input

---

### Chevrotain Parser (`shared/lib/parser/parser.ts`)

Write tests for the SPL parser that builds an AST from tokens.

**Happy path tests:**
- Parse `search index=main` into a SearchCommand node with one filter
- Parse `search index=main sourcetype=syslog` with multiple filters
- Parse `search index=main | stats count` into a Pipeline with two commands
- Parse `stats count by host` with aggregation and grouping
- Parse `stats count as total_events by host` with field aliasing
- Parse `eval new_field = old_field * 2` with arithmetic expression
- Parse `eval combined = field1 . field2` with string concatenation
- Parse `table field1, field2, field3` with field list
- Parse `fields - field1, field2` with field removal syntax
- Parse `where count > 10` with comparison expression
- Parse `where count > 10 AND status = "success"` with compound boolean
- Parse `sort - count` for descending sort
- Parse `sort + count, - host` for mixed sort directions
- Parse `dedup host` for basic deduplication
- Parse `dedup 3 host, source` with consecutive count and multiple fields
- Parse `rex field=_raw "(?<ip>\d+\.\d+\.\d+\.\d+)"` with regex extraction
- Parse `rename old_field as new_field` for field renaming
- Parse nested function calls like `eval x = round(avg(value), 2)`
- Parse subsearches: `search [search index=lookup | return ip]`
- Parse `head 10` and `tail 10` limit commands
- Parse `lookup table_name field OUTPUT new_field`

**Edge case tests:**
- Parse empty search (just `search` with no filters)
- Parse search with only boolean expression `search (error OR warn)`
- Parse stats with multiple aggregations `stats count, avg(bytes), max(duration)`
- Parse eval with no spaces around operators `eval x=a+b`
- Parse deeply nested parentheses in boolean expressions (5+ levels)
- Parse very long pipeline (20+ piped commands)
- Parse command with no arguments where optional
- Parse field names that match reserved keywords when quoted
- Parse numeric field names if SPL allows
- Parse `by` clause with single field vs multiple fields
- Parse `as` clause with quoted alias containing spaces

**Adversarial tests:**
- Missing required argument should produce descriptive ParseError
- Pipe at start of query with no preceding command
- Pipe at end of query with no following command
- Double pipe `||` should error
- Unknown command name should produce error with suggestions if possible
- Mismatched parentheses should error with position
- Mismatched brackets in subsearch should error
- stats without aggregation function
- eval without assignment
- where without boolean expression
- Circular subsearch reference handling (if detectable at parse time)
- Deeply nested subsearches (10+ levels) - verify no stack overflow
- Query that produces ambiguous parse - verify deterministic resolution

---

### AST Visitor / Field Lineage (`shared/lib/parser/visitor.ts`)

Write tests for the visitor that extracts field lineage from the AST.

**Happy path tests:**
- Extract input fields from search filters
- Extract input fields referenced in where clauses
- Track field creation through eval assignments
- Track field aliasing through `as` keyword in stats
- Track field removal through `fields -`
- Track field selection through `table` command
- Build dependency graph showing which output fields depend on which inputs
- Track fields through rename command
- Track fields extracted via rex command
- Track fields through multiple transformation steps
- Identify terminal fields (those in final output)
- Identify fields consumed but not produced

**Edge case tests:**
- Field used multiple times in different commands
- Field overwritten by eval with same name
- Field renamed then used under new name
- Wildcard field references `fields *`
- Self-referential eval `eval x = x + 1`
- Field referenced in subsearch
- Stats with `by` clause - by fields are both input and output
- Empty pipeline produces empty lineage
- Search with no explicit field references (implicit `_raw`)

**Adversarial tests:**
- Circular field dependencies through multiple eval statements
- Field lineage through 50+ commands (performance)
- Conflicting field operations (remove then reference)
- Malformed AST nodes (defensive handling)
- Null or undefined AST input

---

### UI Components with CVA (`shared/ui/`)

For each shared UI component, write tests covering:

**Button component:**
- Renders children text correctly
- Applies default variant classes
- Applies each variant option: default, destructive, outline, secondary, ghost, link
- Applies each size option: default, sm, lg, icon
- Combines variant and size classes correctly
- Forwards onClick handler and fires on click
- Forwards ref to underlying button element
- Applies disabled attribute and prevents click when disabled
- Merges custom className with CVA classes
- Renders as child component when `asChild` prop used (Radix slot)
- Keyboard accessibility: responds to Enter and Space

**Edge cases for Button:**
- Empty children renders accessible empty button
- Very long text content handles overflow
- Multiple rapid clicks with debouncing if implemented
- Button inside form triggers submit by default

**Dialog component (Radix):**
- Opens when trigger clicked
- Closes when overlay clicked
- Closes when close button clicked
- Closes on Escape key press
- Traps focus within dialog when open
- Returns focus to trigger when closed
- Renders title for accessibility
- Renders description for accessibility
- Portal renders dialog outside DOM hierarchy
- Controlled mode with open/onOpenChange props
- Prevents body scroll when open

**Edge cases for Dialog:**
- Multiple dialogs - only topmost receives focus
- Dialog containing form maintains form state
- Dialog with autofocus element
- Very long content scrolls within dialog
- Dialog opened programmatically without trigger

**Select component (Radix):**
- Opens dropdown on trigger click
- Renders all option items
- Selects item on click
- Closes after selection
- Displays selected value in trigger
- Keyboard navigation: arrow keys move focus
- Keyboard selection: Enter selects focused item
- Supports disabled options
- Supports option groups
- Controlled mode with value/onValueChange
- Placeholder text when no selection
- Forwards ref correctly

**Edge cases for Select:**
- Empty options array renders empty dropdown
- Very long option text truncates or wraps
- Options with duplicate values
- Rapid open/close cycles
- Select within a form submits correct value

---

## Entity Layer Tests

### Field Entity (`entities/field/`)

**Model tests (`field.model.ts`):**
- Create field with required properties (name, type)
- Create field with optional properties (description, source command)
- Validate field name format (no spaces, valid characters)
- Field equality comparison by name
- Field serialization to JSON
- Field deserialization from JSON
- Field type enumeration coverage: string, number, boolean, timestamp, ip, unknown
- Computed properties if any (display name, qualified name)

**Edge cases:**
- Empty string field name should error
- Field name with only whitespace should error
- Very long field name (255+ characters)
- Field name with special characters (underscore, dot)
- Reserved field names (`_time`, `_raw`, `_indextime`)
- Null or undefined properties handling

**Component tests (`Field.tsx`):**
- Renders field name
- Renders field type with appropriate styling/icon
- Renders source command badge if present
- Click handler fires with field data
- Hover state shows additional details if implemented
- Selected state applies highlight styling
- Draggable for use in React Flow if applicable

---

## Feature Layer Tests

### SPL Editor Feature (`features/spl-editor/`)

**Component tests (`SplEditor.tsx`):**
- Renders textarea/input for SPL entry
- Displays initial value from props
- Calls onChange with updated value on input
- Syntax highlighting applied via PrismJS
- Line numbers displayed if enabled
- Error highlighting on invalid syntax
- Autocomplete dropdown appears on trigger character
- Autocomplete filters suggestions as user types
- Autocomplete selection inserts text
- Keyboard shortcuts for common operations (if implemented)
- Resize handle works if resizable

**Integration tests:**
- Type query, verify parse result displayed
- Type invalid query, verify error indicator
- Paste multi-line query preserves formatting
- Undo/redo maintains history

**Edge cases:**
- Empty editor state
- Single character input
- Paste very large query (10,000 lines)
- Rapid typing doesn't cause performance issues
- Special characters render correctly in highlighting
- Tab key behavior (insert tab vs focus change)

**Adversarial tests:**
- HTML/script injection in query text (XSS prevention)
- Paste binary data
- Memory usage with very large queries

**Hook tests (`useSplEditor.ts`):**
- Initial state matches default props
- setValue updates internal state
- Parse is triggered on value change (debounced)
- Parse errors populate error state
- AST populates on successful parse
- Field lineage derived from AST
- Reset clears all state
- Loading state during async parse if applicable

---

### Field Lineage Graph Feature (`features/lineage-graph/`)

**React Flow integration tests:**
- Renders nodes for each field in lineage
- Renders edges connecting dependent fields
- Node positions calculated by layout algorithm
- Pan and zoom controls functional
- Node click selects node
- Node drag repositions node
- Edge click selects edge
- Minimap reflects current viewport
- Controls panel renders
- Fit view adjusts zoom to show all nodes

**Edge cases:**
- Empty lineage renders empty graph with message
- Single node lineage (no edges)
- Linear chain of 50+ nodes
- Highly connected graph (each node connects to many others)
- Disconnected subgraphs
- Self-referential edge (field depends on itself)

**Adversarial tests:**
- 1000+ nodes performance
- Circular dependencies don't cause infinite loops
- Rapid lineage updates (typing fast in editor)
- Invalid node/edge data handling

---

## Widget Layer Tests (if applicable)

### Syntax Highlighted Code Block (`widgets/code-block/`)

**PrismJS integration tests:**
- Applies SPL language grammar highlighting
- Keywords highlighted with correct class
- Strings highlighted distinctly
- Numbers highlighted distinctly
- Operators highlighted distinctly
- Comments highlighted if SPL supports
- Line highlighting for specific lines
- Copy button copies content to clipboard
- Line numbers match content lines

**Edge cases:**
- Very long single line
- Empty code block
- Code with only whitespace
- Mixed valid/invalid syntax
- Language switching if supported

---

## Test Utilities to Create

### Custom Render (`test/utils/render.tsx`)

Create a custom render function that wraps components with necessary providers:
- React Flow provider if testing flow components
- Theme provider if using themed components
- Any application-level context providers

### Factories (`test/utils/factories/`)

**Field factory:**
- Generate field with random valid name
- Generate field with specific type
- Generate field with lineage metadata
- Generate batch of related fields

**Node factory (React Flow):**
- Generate field node with position
- Generate command node
- Generate positioned node within bounds
- Generate connected node pair with edge

**AST factory:**
- Generate valid SearchCommand AST node
- Generate valid StatsCommand AST node
- Generate valid Pipeline with N commands
- Generate AST with specific field references

---

## Mocks to Create

### React Flow mock (`test/mocks/react-flow.ts`)

Mock the React Flow library to avoid canvas rendering in tests:
- Mock `ReactFlow` component to render children
- Mock `useNodes` hook to return controlled state
- Mock `useEdges` hook to return controlled state
- Mock `useReactFlow` hook with pan/zoom controls
- Mock node and edge change handlers

### PrismJS mock (`test/mocks/prismjs.ts`)

Mock PrismJS for tests that don't need actual highlighting:
- Mock `highlight` function to return input unchanged
- Mock `languages` registry
- Mock `highlightElement` for DOM highlighting

---

## Coverage Expectations by Layer

- **shared/lib**: 95%+ coverage (pure logic, easily testable)
- **shared/ui**: 90%+ coverage (component behavior)
- **entities**: 90%+ coverage (models and simple components)
- **features**: 85%+ coverage (complex interactions, some integration)
- **widgets**: 80%+ coverage (composition of lower layers)
- **app**: 70%+ coverage (integration, harder to unit test)