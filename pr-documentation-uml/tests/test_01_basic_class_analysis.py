"""Tests for basic class analysis example."""

import pytest


@pytest.mark.basic
def test_analyze_basic_class(example_01):
    """Test basic class analysis extracts correct information."""
    result = example_01.analyze_basic_class(example_01.SAMPLE_CODE)
    
    # Verify class name
    assert result["class_name"] == "User"
    
    # Verify methods
    assert "__init__" in result["methods"]
    assert "activate" in result["methods"]
    assert "deactivate" in result["methods"]
    assert "update_email" in result["methods"]
    
    # Verify analysis object
    assert result["analysis"] is not None
    assert len(result["analysis"].classes) == 1
    assert result["analysis"].classes[0].name == "User"


@pytest.mark.basic
def test_method_signatures(example_01):
    """Test that method signatures are correctly extracted."""
    result = example_01.analyze_basic_class(example_01.SAMPLE_CODE)
    analysis = result["analysis"]
    cls = analysis.classes[0]
    
    # Find activate method
    activate = next(m for m in cls.methods if m.name == "activate")
    assert activate.return_type == "None"
    assert len(activate.parameters) == 0  # No params except self
    
    # Find update_email method
    update_email = next(m for m in cls.methods if m.name == "update_email")
    assert update_email.return_type == "bool"
    assert len(update_email.parameters) == 1
    assert update_email.parameters[0].name == "new_email"
    assert update_email.parameters[0].annotation == "str"


@pytest.mark.basic
def test_imports_detected(example_01):
    """Test that imports are correctly detected."""
    result = example_01.analyze_basic_class(example_01.SAMPLE_CODE)
    analysis = result["analysis"]
    
    # Should detect imports
    assert len(analysis.imports) > 0
    
    # Check for specific imports
    import_modules = [imp.module for imp in analysis.imports]
    assert "datetime" in import_modules
    assert "typing" in import_modules


@pytest.mark.basic
def test_generate_mermaid_diagram(example_01):
    """Test Mermaid diagram generation."""
    result = example_01.analyze_basic_class(example_01.SAMPLE_CODE)
    diagram = example_01.generate_mermaid_class_diagram(result)
    
    # Verify diagram structure
    assert "```mermaid" in diagram
    assert "classDiagram" in diagram
    assert "class User" in diagram
    assert "activate" in diagram
    assert "deactivate" in diagram
    assert "update_email" in diagram


@pytest.mark.basic
def test_empty_code(example_01):
    """Test handling of empty code."""
    result = example_01.analyze_basic_class("")
    
    assert result["class_name"] is None
    assert len(result["methods"]) == 0
    assert len(result["attributes"]) == 0


@pytest.mark.basic
def test_simple_class_fixture(example_01, simple_class_code):
    """Test using simple class fixture."""
    result = example_01.analyze_basic_class(simple_class_code)
    
    assert result["class_name"] == "SimpleClass"
    assert "__init__" in result["methods"]
    assert "get_value" in result["methods"]


@pytest.mark.basic
class TestClassNameExtraction:
    """Group related tests for class name extraction."""
    
    def test_single_class(self, example_01):
        """Test extraction of single class name."""
        code = "class TestClass:\n    pass"
        result = example_01.analyze_basic_class(code)
        assert result["class_name"] == "TestClass"
    
    def test_class_with_docstring(self, example_01):
        """Test class with docstring."""
        code = '''class TestClass:
    """A test class."""
    pass'''
        result = example_01.analyze_basic_class(code)
        assert result["class_name"] == "TestClass"
        assert result["analysis"].classes[0].docstring == "A test class."
