#!/usr/bin/env python3
"""
Recipe 03: Find All Class Definitions

Shows how to find all classes in code using ast.walk() and isinstance().
No wrapper functions - direct ast operations.
"""

import ast

SAMPLE_CODE = '''
class BaseClass:
    pass

class DerivedClass(BaseClass):
    def method(self):
        pass

class AnotherClass:
    value: int = 10

def not_a_class():
    pass
'''

if __name__ == "__main__":
    print("=" * 60)
    print("Recipe 03: Find All Classes")
    print("=" * 60)
    
    # Parse code
    tree = ast.parse(SAMPLE_CODE)
    
    # Method 1: Using ast.walk() - walks entire tree
    print("\nMethod 1: Using ast.walk()")
    classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    
    for cls in classes:
        print(f"  Class: {cls.name}")
        print(f"    Line: {cls.lineno}")
        print(f"    Bases: {[ast.unparse(base) for base in cls.bases]}")
        print(f"    Methods: {len([n for n in cls.body if isinstance(n, ast.FunctionDef)])}")
    
    # Method 2: Direct iteration (only top-level)
    print("\nMethod 2: Direct iteration of tree.body (top-level only)")
    top_level_classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
    print(f"  Found {len(top_level_classes)} top-level classes")
    
    # Method 3: Using list comprehension with condition
    print("\nMethod 3: Find classes with specific characteristics")
    classes_with_bases = [
        node for node in ast.walk(tree) 
        if isinstance(node, ast.ClassDef) and len(node.bases) > 0
    ]
    print(f"  Classes with base classes: {[cls.name for cls in classes_with_bases]}")
    
    print("\n✓ ast.walk(tree) - recursively yields all nodes")
    print("✓ isinstance(node, ast.ClassDef) - check node type")
    print("✓ node.name - get class name")
    print("✓ node.bases - list of base class expressions")
    print("✓ node.body - list of statements in class body")

