"""
Pytest configuration and shared fixtures for PR Documentation with UML tests.
"""

import sys
from pathlib import Path
import importlib.util
import pytest


# Add scripts and examples to path
SKILL_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_ROOT / "scripts"))
sys.path.insert(0, str(SKILL_ROOT / "examples"))


def load_example_module(example_name: str):
    """
    Dynamically load an example module.
    
    Args:
        example_name: Name of the example file (e.g., "01_basic_class_analysis")
        
    Returns:
        Loaded module object
    """
    example_file = SKILL_ROOT / "examples" / f"{example_name}.py"
    spec = importlib.util.spec_from_file_location(example_name, example_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def example_01():
    """Load basic class analysis example."""
    return load_example_module("01_basic_class_analysis")


@pytest.fixture(scope="session")
def example_02():
    """Load inheritance analysis example."""
    return load_example_module("02_inheritance_analysis")


@pytest.fixture(scope="session")
def example_03():
    """Load decorator analysis example."""
    return load_example_module("03_decorator_analysis")


@pytest.fixture(scope="session")
def analyze_code():
    """Import analyze_code module."""
    from analyze_code import analyze_file, format_text, format_json
    return type('AnalyzeCode', (), {
        'analyze_file': analyze_file,
        'format_text': format_text,
        'format_json': format_json
    })


# Sample code fixtures for reuse
@pytest.fixture
def simple_class_code():
    """Simple class code for testing."""
    return """
class SimpleClass:
    def __init__(self, value: int):
        self.value = value
    
    def get_value(self) -> int:
        return self.value
"""


@pytest.fixture
def inheritance_code():
    """Code with inheritance for testing."""
    return """
class Base:
    def method(self) -> str:
        return "base"

class Derived(Base):
    def method(self) -> str:
        return "derived"
"""


@pytest.fixture
def decorator_code():
    """Code with decorators for testing."""
    return """
class MyClass:
    @property
    def value(self) -> int:
        return self._value
    
    @staticmethod
    def static_method() -> str:
        return "static"
    
    @classmethod
    def class_method(cls) -> str:
        return "class"
"""

