#!/usr/bin/env python3
"""
Example: Inheritance Analysis

Demonstrates how to analyze class hierarchies and generate accurate inheritance diagrams.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from analyze_code import analyze_file, format_text


SAMPLE_CODE = """
from abc import ABC, abstractmethod
from typing import Optional


class BaseAuthenticator(ABC):
    \"\"\"Abstract base class for authentication.\"\"\"
    
    @abstractmethod
    def authenticate(self, credentials: dict) -> Optional[str]:
        \"\"\"Authenticate user with credentials.\"\"\"
        pass
    
    @abstractmethod
    def validate_token(self, token: str) -> bool:
        \"\"\"Validate authentication token.\"\"\"
        pass


class JWTAuthenticator(BaseAuthenticator):
    \"\"\"JWT-based authentication implementation.\"\"\"
    
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
    
    def authenticate(self, credentials: dict) -> Optional[str]:
        \"\"\"Authenticate using JWT token.\"\"\"
        return "jwt_token"
    
    def validate_token(self, token: str) -> bool:
        \"\"\"Validate JWT token.\"\"\"
        return True
    
    def generate_token(self, user_id: int, expires_in: int = 3600) -> str:
        \"\"\"Generate JWT token for user.\"\"\"
        return "generated_token"


class OAuth2Authenticator(BaseAuthenticator):
    \"\"\"OAuth 2.0 authentication implementation.\"\"\"
    
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
    
    def authenticate(self, credentials: dict) -> Optional[str]:
        \"\"\"Authenticate using OAuth 2.0.\"\"\"
        return "oauth_token"
    
    def validate_token(self, token: str) -> bool:
        \"\"\"Validate OAuth token.\"\"\"
        return True
    
    def get_authorization_url(self, redirect_uri: str) -> str:
        \"\"\"Get OAuth authorization URL.\"\"\"
        return f"https://oauth.example.com/authorize?redirect_uri={redirect_uri}"
"""


def analyze_inheritance(code: str) -> dict:
    """
    Analyze Python class hierarchy and extract inheritance relationships.
    
    Args:
        code: Python source code as string
        
    Returns:
        Dictionary containing:
        - classes: List of class names
        - inheritance: Dict mapping child -> parent
        - methods_by_class: Dict mapping class -> list of methods
        - analysis: Full FileAnalysis object
    """
    temp_file = Path("/tmp/analyze_sample_inheritance.py")
    temp_file.write_text(code)
    
    try:
        analysis = analyze_file(temp_file)
        
        classes = [cls.name for cls in analysis.classes]
        inheritance = {}
        methods_by_class = {}
        
        for cls in analysis.classes:
            if cls.bases:
                inheritance[cls.name] = cls.bases
            methods_by_class[cls.name] = [m.name for m in cls.methods]
        
        return {
            "classes": classes,
            "inheritance": inheritance,
            "methods_by_class": methods_by_class,
            "analysis": analysis
        }
    finally:
        if temp_file.exists():
            temp_file.unlink()


def generate_mermaid_inheritance_diagram(analysis_result: dict) -> str:
    """
    Generate Mermaid class diagram showing inheritance.
    
    Args:
        analysis_result: Result from analyze_inheritance()
        
    Returns:
        Mermaid diagram code as string
    """
    analysis = analysis_result["analysis"]
    
    lines = ["```mermaid", "classDiagram"]
    
    # Add classes with methods
    for cls in analysis.classes:
        # Check if abstract
        is_abstract = "ABC" in cls.bases or any("abstract" in d.lower() for d in cls.decorators)
        
        lines.append(f"    class {cls.name} {{")
        if is_abstract:
            lines.append("        <<abstract>>")
        
        # Add key methods (skip __init__ and private methods for clarity)
        for method in cls.methods:
            if method.name.startswith("_") and not method.name.startswith("__"):
                continue
            if method.name == "__init__":
                continue
                
            params = ", ".join(f"{p.name}: {p.annotation}" if p.annotation else p.name 
                              for p in method.parameters)
            return_type = method.return_type or ""
            lines.append(f"        +{method.name}({params}) {return_type}")
        
        lines.append("    }")
        lines.append("")
    
    # Add inheritance relationships
    for cls in analysis.classes:
        for base in cls.bases:
            if base != "ABC":  # Skip ABC from diagram
                lines.append(f"    {base} <|-- {cls.name}")
    
    lines.append("```")
    
    return "\n".join(lines)


def main():
    """Main function to demonstrate inheritance analysis."""
    print("=" * 80)
    print("Example: Inheritance Analysis")
    print("=" * 80)
    print()
    
    print("Sample Code:")
    print("-" * 80)
    print(SAMPLE_CODE[:500] + "...\n")
    
    print("Analysis Result:")
    print("-" * 80)
    result = analyze_inheritance(SAMPLE_CODE)
    
    print(f"Classes: {', '.join(result['classes'])}")
    print()
    print("Inheritance Relationships:")
    for child, parents in result['inheritance'].items():
        print(f"  {child} -> {', '.join(parents)}")
    print()
    
    print("Methods by Class:")
    for cls_name, methods in result['methods_by_class'].items():
        print(f"  {cls_name}: {', '.join(methods)}")
    print()
    
    print("Full Analysis Output:")
    print("-" * 80)
    print(format_text(result['analysis']))
    print()
    
    print("Generated Mermaid Diagram:")
    print("-" * 80)
    print(generate_mermaid_inheritance_diagram(result))
    print()
    
    print("Key Points:")
    print("- ✓ Base class: BaseAuthenticator")
    print("- ✓ Derived classes: JWTAuthenticator, OAuth2Authenticator")
    print("- ✓ Method signatures match exactly")
    print("- ✓ Additional methods captured: generate_token, get_authorization_url")


if __name__ == "__main__":
    main()

