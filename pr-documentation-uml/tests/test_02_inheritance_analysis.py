"""Tests for inheritance analysis example."""

import pytest


@pytest.mark.inheritance
def test_analyze_inheritance(example_02):
    """Test inheritance analysis extracts correct relationships."""
    result = example_02.analyze_inheritance(example_02.SAMPLE_CODE)
    
    # Verify all classes found
    assert "BaseAuthenticator" in result["classes"]
    assert "JWTAuthenticator" in result["classes"]
    assert "OAuth2Authenticator" in result["classes"]
    
    # Verify inheritance relationships
    assert "JWTAuthenticator" in result["inheritance"]
    assert "BaseAuthenticator" in result["inheritance"]["JWTAuthenticator"]
    assert "OAuth2Authenticator" in result["inheritance"]
    assert "BaseAuthenticator" in result["inheritance"]["OAuth2Authenticator"]


@pytest.mark.inheritance
def test_methods_by_class(example_02):
    """Test that methods are correctly grouped by class."""
    result = example_02.analyze_inheritance(example_02.SAMPLE_CODE)
    
    # Base class methods
    base_methods = result["methods_by_class"]["BaseAuthenticator"]
    assert "authenticate" in base_methods
    assert "validate_token" in base_methods
    
    # JWT methods (includes base + additional)
    jwt_methods = result["methods_by_class"]["JWTAuthenticator"]
    assert "authenticate" in jwt_methods
    assert "validate_token" in jwt_methods
    assert "generate_token" in jwt_methods
    
    # OAuth methods
    oauth_methods = result["methods_by_class"]["OAuth2Authenticator"]
    assert "authenticate" in oauth_methods
    assert "validate_token" in oauth_methods
    assert "get_authorization_url" in oauth_methods


@pytest.mark.inheritance
def test_abstract_methods(example_02):
    """Test that abstract methods are detected."""
    result = example_02.analyze_inheritance(example_02.SAMPLE_CODE)
    analysis = result["analysis"]
    
    base_class = next(cls for cls in analysis.classes if cls.name == "BaseAuthenticator")
    
    # Check for abstractmethod decorators
    for method in base_class.methods:
        if method.name in ["authenticate", "validate_token"]:
            assert "abstractmethod" in method.decorators


@pytest.mark.inheritance
def test_method_overriding(example_02):
    """Test that method overriding is properly detected."""
    result = example_02.analyze_inheritance(example_02.SAMPLE_CODE)
    
    # Both derived classes should override authenticate and validate_token
    jwt_methods = result["methods_by_class"]["JWTAuthenticator"]
    oauth_methods = result["methods_by_class"]["OAuth2Authenticator"]
    
    for method_name in ["authenticate", "validate_token"]:
        assert method_name in jwt_methods
        assert method_name in oauth_methods


@pytest.mark.inheritance
def test_additional_methods(example_02):
    """Test that class-specific methods are captured."""
    result = example_02.analyze_inheritance(example_02.SAMPLE_CODE)
    
    jwt_methods = result["methods_by_class"]["JWTAuthenticator"]
    oauth_methods = result["methods_by_class"]["OAuth2Authenticator"]
    
    # JWT-specific method
    assert "generate_token" in jwt_methods
    assert "generate_token" not in oauth_methods
    
    # OAuth-specific method
    assert "get_authorization_url" in oauth_methods
    assert "get_authorization_url" not in jwt_methods


@pytest.mark.inheritance
def test_generate_mermaid_inheritance_diagram(example_02):
    """Test Mermaid inheritance diagram generation."""
    result = example_02.analyze_inheritance(example_02.SAMPLE_CODE)
    diagram = example_02.generate_mermaid_inheritance_diagram(result)
    
    # Verify diagram structure
    assert "```mermaid" in diagram
    assert "classDiagram" in diagram
    
    # Verify classes
    assert "class BaseAuthenticator" in diagram
    assert "class JWTAuthenticator" in diagram
    assert "class OAuth2Authenticator" in diagram
    
    # Verify inheritance arrows
    assert "BaseAuthenticator <|-- JWTAuthenticator" in diagram
    assert "BaseAuthenticator <|-- OAuth2Authenticator" in diagram
    
    # Verify abstract marker
    assert "<<abstract>>" in diagram


@pytest.mark.inheritance
def test_method_signatures(example_02):
    """Test that method signatures are preserved correctly."""
    result = example_02.analyze_inheritance(example_02.SAMPLE_CODE)
    analysis = result["analysis"]
    
    jwt_class = next(cls for cls in analysis.classes if cls.name == "JWTAuthenticator")
    generate_token = next(m for m in jwt_class.methods if m.name == "generate_token")
    
    # Check parameters
    assert len(generate_token.parameters) == 2
    assert generate_token.parameters[0].name == "user_id"
    assert generate_token.parameters[0].annotation == "int"
    assert generate_token.parameters[1].name == "expires_in"
    assert generate_token.parameters[1].default == "3600"
    
    # Check return type
    assert generate_token.return_type == "str"


@pytest.mark.inheritance
def test_simple_inheritance_fixture(example_02, inheritance_code):
    """Test using simple inheritance fixture."""
    result = example_02.analyze_inheritance(inheritance_code)
    
    assert "Base" in result["classes"]
    assert "Derived" in result["classes"]
    assert "Derived" in result["inheritance"]
    assert "Base" in result["inheritance"]["Derived"]


@pytest.mark.inheritance
class TestInheritanceDetection:
    """Group related tests for inheritance detection."""
    
    def test_single_level_inheritance(self, example_02):
        """Test single level inheritance."""
        code = """
class Parent:
    pass

class Child(Parent):
    pass
"""
        result = example_02.analyze_inheritance(code)
        assert "Child" in result["inheritance"]
        assert "Parent" in result["inheritance"]["Child"]
    
    def test_multiple_inheritance(self, example_02):
        """Test multiple inheritance."""
        code = """
class A:
    pass

class B:
    pass

class C(A, B):
    pass
"""
        result = example_02.analyze_inheritance(code)
        assert "C" in result["inheritance"]
        assert "A" in result["inheritance"]["C"]
        assert "B" in result["inheritance"]["C"]
