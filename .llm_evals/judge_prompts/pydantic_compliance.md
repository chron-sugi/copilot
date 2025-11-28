# Pydantic Model Compliance Rubric

## Overview
This rubric evaluates the quality and correctness of LLM-generated Pydantic models.

## Evaluation Criteria

### 1. Correctness (40 points)
- **Syntax Validity (15 points)**
  - Code is syntactically valid Python
  - No import errors or typos
  - Proper indentation and structure

- **Pydantic Compliance (15 points)**
  - Inherits from `pydantic.BaseModel`
  - Uses proper Pydantic field syntax
  - Follows Pydantic v2 best practices (if applicable)

- **Type Annotations (10 points)**
  - All fields have correct type hints
  - Uses appropriate types from `typing` module when needed
  - Type hints match the requirements

### 2. Validation & Constraints (25 points)
- **Field Validation (15 points)**
  - Includes validators where specified
  - Validators have correct logic
  - Uses appropriate Pydantic validation methods

- **Constraints (10 points)**
  - Proper use of Field() with constraints
  - Min/max values where appropriate
  - Regex patterns for string fields if needed

### 3. Structure & Design (20 points)
- **Model Organization (10 points)**
  - Logical field ordering
  - Proper use of nested models
  - Clear model names

- **Reusability (10 points)**
  - Models are composable
  - Avoids unnecessary duplication
  - Follows single responsibility principle

### 4. Documentation (10 points)
- **Docstrings (5 points)**
  - Class docstring present
  - Field descriptions when helpful

- **Comments (5 points)**
  - Complex validators are explained
  - Non-obvious design choices documented

### 5. Best Practices (5 points)
- Follows PEP 8 naming conventions
- Uses Config class appropriately if needed
- Proper use of Optional, Union, etc.

## Scoring Guide
- **90-100**: Excellent - Production-ready code
- **75-89**: Good - Minor improvements needed
- **60-74**: Acceptable - Several issues to address
- **Below 60**: Needs significant revision

## Common Issues to Flag
1. Missing type hints
2. Incorrect inheritance (not from BaseModel)
3. Missing or incorrect validation
4. Poor field naming (not snake_case)
5. Overly complex validation logic
6. Missing docstrings for complex models
7. Incorrect use of Pydantic v1 vs v2 syntax
8. Missing imports
9. Inefficient nested structures
10. Lack of error handling in validators
