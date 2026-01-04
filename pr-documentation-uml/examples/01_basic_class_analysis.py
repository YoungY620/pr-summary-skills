#!/usr/bin/env python3
"""
Example: Basic Class Analysis

Demonstrates how to analyze a simple class and generate accurate UML class diagrams.
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from analyze_code import analyze_file, format_text


# Sample code to analyze
SAMPLE_CODE = """
from datetime import datetime
from typing import Optional


class User:
    \"\"\"User model representing a registered user.\"\"\"
    
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email
        self.created_at = datetime.now()
        self.is_active: bool = True
    
    def activate(self) -> None:
        \"\"\"Activate the user account.\"\"\"
        self.is_active = True
    
    def deactivate(self) -> None:
        \"\"\"Deactivate the user account.\"\"\"
        self.is_active = False
    
    def update_email(self, new_email: str) -> bool:
        \"\"\"Update user email address.\"\"\"
        if "@" in new_email:
            self.email = new_email
            return True
        return False
"""


def analyze_basic_class(code: str) -> dict:
    """
    Analyze a basic Python class and extract structure information.
    
    Args:
        code: Python source code as string
        
    Returns:
        Dictionary containing analysis results with keys:
        - class_name: Name of the class
        - methods: List of method names
        - attributes: List of attribute names
        - analysis: Full FileAnalysis object
    """
    # Write code to temporary file
    temp_file = Path("/tmp/analyze_sample_basic.py")
    temp_file.write_text(code)
    
    try:
        # Analyze the file
        analysis = analyze_file(temp_file)
        
        # Extract class information
        if not analysis.classes:
            return {
                "class_name": None,
                "methods": [],
                "attributes": [],
                "analysis": analysis
            }
        
        cls = analysis.classes[0]
        
        return {
            "class_name": cls.name,
            "methods": [m.name for m in cls.methods],
            "attributes": [a.name for a in cls.attributes],
            "analysis": analysis
        }
    finally:
        # Cleanup
        if temp_file.exists():
            temp_file.unlink()


def generate_mermaid_class_diagram(analysis_result: dict) -> str:
    """
    Generate Mermaid class diagram from analysis result.
    
    Args:
        analysis_result: Result from analyze_basic_class()
        
    Returns:
        Mermaid diagram code as string
    """
    analysis = analysis_result["analysis"]
    
    if not analysis.classes:
        return "No classes found"
    
    cls = analysis.classes[0]
    
    lines = ["```mermaid", "classDiagram"]
    lines.append(f"    class {cls.name} {{")
    
    # Add attributes
    for attr in cls.attributes:
        type_str = f" {attr.annotation}" if attr.annotation else ""
        lines.append(f"        +{attr.name}:{type_str}")
    
    # Add methods
    for method in cls.methods:
        if method.name == "__init__":
            continue  # Skip constructor in UML
        
        params = ", ".join(f"{p.name}: {p.annotation}" if p.annotation else p.name 
                          for p in method.parameters)
        return_type = method.return_type or ""
        lines.append(f"        +{method.name}({params}) {return_type}")
    
    lines.append("    }")
    lines.append("```")
    
    return "\n".join(lines)


def main():
    """Main function to demonstrate basic class analysis."""
    print("=" * 80)
    print("Example: Basic Class Analysis")
    print("=" * 80)
    print()
    
    print("Sample Code:")
    print("-" * 80)
    print(SAMPLE_CODE)
    print()
    
    print("Analysis Result:")
    print("-" * 80)
    result = analyze_basic_class(SAMPLE_CODE)
    
    print(f"Class Name: {result['class_name']}")
    print(f"Methods: {', '.join(result['methods'])}")
    print(f"Attributes: {', '.join(result['attributes']) if result['attributes'] else 'None detected'}")
    print()
    
    print("Full Analysis Output:")
    print("-" * 80)
    print(format_text(result['analysis']))
    print()
    
    print("Generated Mermaid Diagram:")
    print("-" * 80)
    print(generate_mermaid_class_diagram(result))
    print()
    
    print("Key Points:")
    print("- ✓ Exact class name: User")
    print("- ✓ Exact method names: activate, deactivate, update_email")
    print("- ✓ Exact parameter names: username, email, new_email")
    print("- ✓ Exact return types: None, bool")


if __name__ == "__main__":
    main()

