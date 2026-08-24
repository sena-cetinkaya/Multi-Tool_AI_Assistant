import pytest

from src.agents.tools.calculator_tool import calculator
from src.utils.exceptions import ToolExecutionError

def test_calculator_basic_addition():
    result = calculator.invoke({"expression": "2 + 2"})
    assert "4" in result

def test_calculator_sqrt_function():
    result = calculator.invoke({"expression": "sqrt(144)"})
    assert "12" in result

def test_calculator_operator_precedence():
    result = calculator.invoke({"expression": "2 + 3 * 4"})
    assert "14" in result

def test_calculator_rejects_unsafe_expression():
    with pytest.raises(ToolExecutionError):
        calculator.invoke({"expression": "__import__('os').system('echo hi')"})

def test_calculator_rejects_unknown_name():
    with pytest.raises(ToolExecutionError):
        calculator.invoke({"expression": "undefined_variable + 1"})
