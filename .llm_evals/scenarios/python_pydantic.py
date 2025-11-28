"""
Pydantic Model Generation Test Scenarios

Test cases for evaluating LLM-generated Pydantic models.
"""
from typing import List
from deepeval.test_case import LLMTestCase


class PydanticScenarios:
    """Collection of test scenarios for Pydantic model generation."""
    
    @staticmethod
    def basic_model() -> LLMTestCase:
        """Test case for generating a simple Pydantic model."""
        return LLMTestCase(
            input=(
                "Create a Pydantic model for a User with fields: "
                "id (int), name (str), email (str), is_active (bool)."
            ),
            actual_output="",  # To be filled by LLM
            expected_output=(
                "A Pydantic BaseModel class named User with properly typed fields "
                "and basic field validation."
            ),
            context=[
                "The model should inherit from pydantic.BaseModel",
                "All fields should have type hints",
                "Email should have validation"
            ]
        )
    
    @staticmethod
    def nested_model() -> LLMTestCase:
        """Test case for generating nested Pydantic models."""
        return LLMTestCase(
            input=(
                "Create Pydantic models for an Order system with Order containing "
                "order_id, customer info (name, email), and a list of OrderItems "
                "(product_name, quantity, price)."
            ),
            actual_output="",  # To be filled by LLM
            expected_output=(
                "Multiple Pydantic models with proper nesting, including Order, "
                "Customer, and OrderItem classes with appropriate relationships."
            ),
            context=[
                "Use nested models for customer information",
                "OrderItems should be a list of Pydantic models",
                "Include proper type hints for all nested structures"
            ]
        )
    
    @staticmethod
    def validation_model() -> LLMTestCase:
        """Test case for Pydantic models with custom validation."""
        return LLMTestCase(
            input=(
                "Create a Pydantic model for a Product with price validation "
                "(must be positive), category (enum), and stock quantity (non-negative)."
            ),
            actual_output="",  # To be filled by LLM
            expected_output=(
                "A Pydantic model with custom validators using @validator decorators "
                "or field validators, including bounds checking and enum constraints."
            ),
            context=[
                "Use Pydantic validators for price and quantity checks",
                "Category should use Enum from typing or Pydantic",
                "Include helpful error messages for validation failures"
            ]
        )
    
    @classmethod
    def all_scenarios(cls) -> List[LLMTestCase]:
        """Return all Pydantic test scenarios."""
        return [
            cls.basic_model(),
            cls.nested_model(),
            cls.validation_model(),
        ]


# Convenience exports
def get_pydantic_scenarios() -> List[LLMTestCase]:
    """Get all Pydantic model generation test scenarios."""
    return PydanticScenarios.all_scenarios()
