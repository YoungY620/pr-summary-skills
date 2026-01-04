"""Tests for decorator and property analysis example."""

import pytest


@pytest.mark.decorators
def test_analyze_decorators(example_03):
    """Test decorator analysis extracts correct information."""
    result = example_03.analyze_decorators(example_03.SAMPLE_CODE)
    
    assert result["class_name"] == "Product"
    
    # Verify properties are detected
    assert "product_id" in result["properties"]
    assert "name" in result["properties"]
    assert "price" in result["properties"]
    assert "final_price" in result["properties"]
    
    # Verify static methods
    assert "validate_price" in result["static_methods"]
    
    # Verify class methods
    assert "create_from_dict" in result["class_methods"]
    
    # Verify regular methods
    assert "calculate_tax" in result["regular_methods"]


@pytest.mark.decorators
def test_property_detection(example_03):
    """Test that properties are correctly distinguished from methods."""
    result = example_03.analyze_decorators(example_03.SAMPLE_CODE)
    
    # These should be properties
    properties = result["properties"]
    assert "product_id" in properties
    assert "name" in properties
    assert "price" in properties
    assert "final_price" in properties
    
    # These should NOT be properties
    assert "validate_price" not in properties
    assert "create_from_dict" not in properties
    assert "calculate_tax" not in properties


@pytest.mark.decorators
def test_static_method_detection(example_03):
    """Test static method detection."""
    result = example_03.analyze_decorators(example_03.SAMPLE_CODE)
    
    assert "validate_price" in result["static_methods"]
    assert len(result["static_methods"]) == 1
    
    # Verify it has staticmethod decorator
    assert "staticmethod" in result["decorators"]["validate_price"]


@pytest.mark.decorators
def test_class_method_detection(example_03):
    """Test class method detection."""
    result = example_03.analyze_decorators(example_03.SAMPLE_CODE)
    
    assert "create_from_dict" in result["class_methods"]
    assert len(result["class_methods"]) == 1
    
    # Verify it has classmethod decorator
    assert "classmethod" in result["decorators"]["create_from_dict"]


@pytest.mark.decorators
def test_custom_decorators(example_03):
    """Test that custom decorators (like lru_cache) are captured."""
    result = example_03.analyze_decorators(example_03.SAMPLE_CODE)
    
    # calculate_tax has lru_cache decorator
    assert "calculate_tax" in result["decorators"]
    decorators = result["decorators"]["calculate_tax"]
    assert any("lru_cache" in d for d in decorators)


@pytest.mark.decorators
def test_class_level_attributes(example_03):
    """Test that class-level attributes are detected."""
    result = example_03.analyze_decorators(example_03.SAMPLE_CODE)
    analysis = result["analysis"]
    
    cls = analysis.classes[0]
    
    # Check for class-level attributes
    attr_names = [attr.name for attr in cls.attributes]
    # _discount is defined at class level, so it should be detected
    assert "_discount" in attr_names
    
    # Find the _discount attribute
    discount_attr = next(attr for attr in cls.attributes if attr.name == "_discount")
    assert discount_attr.annotation == "float"


@pytest.mark.decorators
def test_type_annotations(example_03):
    """Test that type annotations are preserved."""
    result = example_03.analyze_decorators(example_03.SAMPLE_CODE)
    analysis = result["analysis"]
    
    cls = analysis.classes[0]
    
    # Find property with return type
    product_id_prop = next(m for m in cls.methods if m.name == "product_id")
    assert product_id_prop.return_type == "int"
    
    name_prop = next(m for m in cls.methods if m.name == "name")
    assert name_prop.return_type == "str"
    
    price_prop = next(m for m in cls.methods if m.name == "price")
    assert price_prop.return_type == "float"


@pytest.mark.decorators
def test_property_setter_detection(example_03):
    """Test that property setters are detected."""
    result = example_03.analyze_decorators(example_03.SAMPLE_CODE)
    analysis = result["analysis"]
    
    cls = analysis.classes[0]
    
    # Count methods named 'name' (getter and setter)
    name_methods = [m for m in cls.methods if m.name == "name"]
    assert len(name_methods) == 2  # getter and setter


@pytest.mark.decorators
def test_generate_mermaid_with_decorators(example_03):
    """Test Mermaid diagram generation with decorators."""
    result = example_03.analyze_decorators(example_03.SAMPLE_CODE)
    diagram = example_03.generate_mermaid_with_decorators(result)
    
    # Verify diagram structure
    assert "```mermaid" in diagram
    assert "classDiagram" in diagram
    assert "class Product" in diagram
    
    # Verify class-level attributes are marked with -
    assert "-_discount" in diagram or "_discount:" in diagram
    
    # Verify properties are included
    assert "product_id:" in diagram
    assert "name:" in diagram
    
    # Verify static methods have $ marker
    assert "validate_price" in diagram
    assert "$" in diagram  # Static method marker
    
    # Verify note is included
    assert "note for Product" in diagram


@pytest.mark.decorators
def test_method_parameters(example_03):
    """Test that method parameters are correctly extracted."""
    result = example_03.analyze_decorators(example_03.SAMPLE_CODE)
    analysis = result["analysis"]
    
    cls = analysis.classes[0]
    
    # Check calculate_tax parameters
    calc_tax = next(m for m in cls.methods if m.name == "calculate_tax")
    assert len(calc_tax.parameters) == 1
    assert calc_tax.parameters[0].name == "tax_rate"
    assert calc_tax.parameters[0].annotation == "float"
    assert calc_tax.return_type == "float"


@pytest.mark.decorators
def test_decorator_fixture(example_03, decorator_code):
    """Test using decorator fixture."""
    result = example_03.analyze_decorators(decorator_code)
    
    assert result["class_name"] == "MyClass"
    assert "value" in result["properties"]
    assert "static_method" in result["static_methods"]
    assert "class_method" in result["class_methods"]


@pytest.mark.decorators
class TestDecoratorTypes:
    """Group related tests for different decorator types."""
    
    def test_property_decorator(self, example_03):
        """Test property decorator detection."""
        code = """
class TestClass:
    @property
    def value(self) -> int:
        return 42
"""
        result = example_03.analyze_decorators(code)
        assert "value" in result["properties"]
    
    def test_staticmethod_decorator(self, example_03):
        """Test staticmethod decorator detection."""
        code = """
class TestClass:
    @staticmethod
    def static() -> str:
        return "static"
"""
        result = example_03.analyze_decorators(code)
        assert "static" in result["static_methods"]
    
    def test_classmethod_decorator(self, example_03):
        """Test classmethod decorator detection."""
        code = """
class TestClass:
    @classmethod
    def cls_method(cls) -> str:
        return "class"
"""
        result = example_03.analyze_decorators(code)
        assert "cls_method" in result["class_methods"]
