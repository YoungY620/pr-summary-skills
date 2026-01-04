#!/usr/bin/env python3
"""
Recipe 06: Get Class Methods

Shows how to extract methods from a class definition.
Direct ast operations - no wrappers.
"""

import ast

SAMPLE_CODE = '''
class DataProcessor:
    cache_size: int = 100
    
    def __init__(self, name: str):
        self.name = name
    
    def process(self, data: list) -> list:
        """Process data."""
        return data
    
    @property
    def status(self) -> str:
        return "ready"
    
    @staticmethod
    def validate(data: dict) -> bool:
        return True
    
    @classmethod
    def from_config(cls, config: dict):
        return cls(config['name'])
    
    def _private_method(self):
        pass
'''

if __name__ == "__main__":
    print("=" * 60)
    print("Recipe 06: Get Class Methods")
    print("=" * 60)
    
    tree = ast.parse(SAMPLE_CODE)
    
    # Find the class
    cls = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)][0]
    print(f"\nAnalyzing class: {cls.name}")
    
    # Get all methods (FunctionDef nodes in class body)
    print("\n1. All methods:")
    methods = [node for node in cls.body if isinstance(node, ast.FunctionDef)]
    for method in methods:
        print(f"  - {method.name}")
    
    # Get method parameters
    print("\n2. Methods with parameters:")
    for method in methods:
        params = [arg.arg for arg in method.args.args]
        print(f"  - {method.name}({', '.join(params)})")
    
    # Get method return types
    print("\n3. Methods with return type annotations:")
    for method in methods:
        if method.returns:
            ret_type = ast.unparse(method.returns)
            print(f"  - {method.name}() -> {ret_type}")
    
    # Check decorators
    print("\n4. Methods with decorators:")
    for method in methods:
        if method.decorator_list:
            decorators = [ast.unparse(d) for d in method.decorator_list]
            print(f"  - {method.name}: {decorators}")
    
    # Filter by decorator type
    print("\n5. Property methods:")
    properties = [
        method for method in methods
        if any('property' in ast.unparse(d) for d in method.decorator_list)
    ]
    print(f"  {[m.name for m in properties]}")
    
    print("\n6. Static methods:")
    static_methods = [
        method for method in methods
        if any('staticmethod' in ast.unparse(d) for d in method.decorator_list)
    ]
    print(f"  {[m.name for m in static_methods]}")
    
    # Filter by name pattern
    print("\n7. Public methods (not starting with _):")
    public_methods = [m for m in methods if not m.name.startswith('_')]
    print(f"  {[m.name for m in public_methods]}")
    
    print("\n8. Private methods (starting with _):")
    private_methods = [m for m in methods if m.name.startswith('_') and not m.name.startswith('__')]
    print(f"  {[m.name for m in private_methods]}")
    
    print("\n✓ cls.body - list of all statements in class")
    print("✓ isinstance(node, ast.FunctionDef) - check if method")
    print("✓ method.args.args - list of parameters")
    print("✓ method.returns - return type annotation (or None)")
    print("✓ method.decorator_list - list of decorators")
    print("✓ ast.unparse(node) - convert AST back to code")

