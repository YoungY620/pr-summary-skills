#!/usr/bin/env python3
"""
Example: Decorator and Property Analysis

Demonstrates how to analyze classes with decorators, properties, static methods, etc.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from analyze_code import analyze_file, format_text


SAMPLE_CODE = """
from functools import lru_cache
from typing import Optional


class Product:
    \"\"\"Product model with cached properties.\"\"\"
    
    _discount: float = 0.0  # Class-level attribute with type annotation
    
    def __init__(self, product_id: int, name: str, price: float):
        self._product_id = product_id
        self._name = name
        self._price = price
    
    @property
    def product_id(self) -> int:
        \"\"\"Get product ID.\"\"\"
        return self._product_id
    
    @property
    def name(self) -> str:
        \"\"\"Get product name.\"\"\"
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        \"\"\"Set product name.\"\"\"
        if value:
            self._name = value
    
    @property
    def price(self) -> float:
        \"\"\"Get product price.\"\"\"
        return self._price
    
    @property
    def final_price(self) -> float:
        \"\"\"Calculate final price after discount.\"\"\"
        return self._price * (1 - self._discount / 100)
    
    @staticmethod
    def validate_price(price: float) -> bool:
        \"\"\"Validate if price is valid.\"\"\"
        return price >= 0
    
    @classmethod
    def create_from_dict(cls, data: dict) -> "Product":
        \"\"\"Create Product from dictionary.\"\"\"
        return cls(
            product_id=data["product_id"],
            name=data["name"],
            price=data["price"]
        )
    
    @lru_cache(maxsize=128)
    def calculate_tax(self, tax_rate: float) -> float:
        \"\"\"Calculate tax amount (cached).\"\"\"
        return self.final_price * tax_rate
"""


def analyze_decorators(code: str) -> dict:
    """
    Analyze Python class with decorators and properties.
    
    Args:
        code: Python source code as string
        
    Returns:
        Dictionary containing:
        - class_name: Name of the class
        - properties: List of property names
        - static_methods: List of static method names
        - class_methods: List of class method names
        - regular_methods: List of regular method names
        - decorators: Dict mapping method -> list of decorators
        - analysis: Full FileAnalysis object
    """
    temp_file = Path("/tmp/analyze_sample_decorators.py")
    temp_file.write_text(code)
    
    try:
        analysis = analyze_file(temp_file)
        
        if not analysis.classes:
            return {}
        
        cls = analysis.classes[0]
        
        properties = []
        static_methods = []
        class_methods = []
        regular_methods = []
        decorators = {}
        
        for method in cls.methods:
            if method.name == "__init__":
                continue
                
            decorators[method.name] = method.decorators
            
            if method.is_property:
                properties.append(method.name)
            elif method.is_static:
                static_methods.append(method.name)
            elif method.is_class_method:
                class_methods.append(method.name)
            else:
                regular_methods.append(method.name)
        
        return {
            "class_name": cls.name,
            "properties": properties,
            "static_methods": static_methods,
            "class_methods": class_methods,
            "regular_methods": regular_methods,
            "decorators": decorators,
            "analysis": analysis
        }
    finally:
        if temp_file.exists():
            temp_file.unlink()


def generate_mermaid_with_decorators(analysis_result: dict) -> str:
    """
    Generate Mermaid class diagram highlighting different method types.
    
    Args:
        analysis_result: Result from analyze_decorators()
        
    Returns:
        Mermaid diagram code as string
    """
    analysis = analysis_result["analysis"]
    
    if not analysis.classes:
        return "No classes found"
    
    cls = analysis.classes[0]
    
    lines = ["```mermaid", "classDiagram"]
    lines.append(f"    class {cls.name} {{")
    
    # Add attributes (private ones)
    for attr in cls.attributes:
        visibility = "-" if attr.name.startswith("_") else "+"
        type_str = f" {attr.annotation}" if attr.annotation else ""
        lines.append(f"        {visibility}{attr.name}:{type_str}")
    
    # Add properties
    for prop in analysis_result["properties"]:
        method = next(m for m in cls.methods if m.name == prop)
        return_type = method.return_type or ""
        lines.append(f"        +{prop}: {return_type}")
    
    # Add static methods
    for method_name in analysis_result["static_methods"]:
        method = next(m for m in cls.methods if m.name == method_name)
        params = ", ".join(f"{p.name}: {p.annotation}" if p.annotation else p.name 
                          for p in method.parameters)
        return_type = method.return_type or ""
        lines.append(f"        +{method.name}({params})$ {return_type}")
    
    # Add class methods
    for method_name in analysis_result["class_methods"]:
        method = next(m for m in cls.methods if m.name == method_name)
        params = ", ".join(f"{p.name}: {p.annotation}" if p.annotation else p.name 
                          for p in method.parameters)
        return_type = method.return_type or ""
        lines.append(f"        +{method.name}({params})$ {return_type}")
    
    # Add regular methods
    for method_name in analysis_result["regular_methods"]:
        method = next(m for m in cls.methods if m.name == method_name)
        params = ", ".join(f"{p.name}: {p.annotation}" if p.annotation else p.name 
                          for p in method.parameters)
        return_type = method.return_type or ""
        lines.append(f"        +{method.name}({params}) {return_type}")
    
    lines.append("    }")
    lines.append("")
    lines.append(f"    note for {cls.name} \"Properties: {', '.join(analysis_result['properties'])}\\n")
    lines.append(f"Static: {', '.join(analysis_result['static_methods'])}\\n")
    lines.append(f"Class methods: {', '.join(analysis_result['class_methods'])}\"")
    lines.append("```")
    
    return "\n".join(lines)


def main():
    """Main function to demonstrate decorator analysis."""
    print("=" * 80)
    print("Example: Decorator and Property Analysis")
    print("=" * 80)
    print()
    
    print("Sample Code:")
    print("-" * 80)
    print(SAMPLE_CODE[:600] + "...\n")
    
    print("Analysis Result:")
    print("-" * 80)
    result = analyze_decorators(SAMPLE_CODE)
    
    print(f"Class Name: {result['class_name']}")
    print(f"Properties: {', '.join(result['properties'])}")
    print(f"Static Methods: {', '.join(result['static_methods'])}")
    print(f"Class Methods: {', '.join(result['class_methods'])}")
    print(f"Regular Methods: {', '.join(result['regular_methods'])}")
    print()
    
    print("Decorators:")
    for method_name, decorators in result['decorators'].items():
        if decorators:
            print(f"  {method_name}: {', '.join(decorators)}")
    print()
    
    print("Full Analysis Output:")
    print("-" * 80)
    print(format_text(result['analysis']))
    print()
    
    print("Generated Mermaid Diagram:")
    print("-" * 80)
    print(generate_mermaid_with_decorators(result))
    print()
    
    print("Key Points:")
    print("- ✓ Properties distinguished from methods")
    print("- ✓ Private attributes marked with -")
    print("- ✓ Static and class methods identified")
    print("- ✓ Decorators captured (property, staticmethod, classmethod, lru_cache)")


if __name__ == "__main__":
    main()

