"""
Smoke test for DeepEval setup.

Verifies that DeepEval is installed and basic functionality works.
"""
import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric


def test_deepeval_import():
    """Verify DeepEval can be imported."""
    assert assert_test is not None
    assert LLMTestCase is not None


@pytest.mark.skip(reason="Requires API key - enable when ready to run live tests")
def test_basic_relevancy():
    """
    Basic smoke test for answer relevancy metric.
    
    This test is skipped by default to avoid API costs.
    Remove the skip decorator when you're ready to test with real API calls.
    """
    test_case = LLMTestCase(
        input="What is the capital of France?",
        actual_output="Paris is the capital of France.",
        expected_output="Paris"
    )
    
    metric = AnswerRelevancyMetric(threshold=0.7)
    metric.measure(test_case)
    
    assert_test(test_case, [metric])


def test_test_case_creation():
    """Verify we can create test cases without API calls."""
    test_case = LLMTestCase(
        input="Sample input",
        actual_output="Sample output",
        expected_output="Expected output"
    )
    
    assert test_case.input == "Sample input"
    assert test_case.actual_output == "Sample output"
    assert test_case.expected_output == "Expected output"
