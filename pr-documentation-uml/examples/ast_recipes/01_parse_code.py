#!/usr/bin/env python3
"""
Recipe 01: Parse Python Code into AST

Shows how to parse Python source code into an Abstract Syntax Tree.
Pure ast usage - no wrapper functions.
"""

import ast

# Sample code to parse
SAMPLE_CODE = '''
class MyClass:
    def my_method(self):
        return "Hello"

def my_function():
    pass
'''

if __name__ == "__main__":
    print("=" * 60)
    print("Recipe 01: Parse Code")
    print("=" * 60)
    
    # Parse code into AST
    tree = ast.parse(SAMPLE_CODE)
    
    print(f"Parsed successfully!")
    print(f"Root node type: {type(tree).__name__}")
    print(f"Number of top-level statements: {len(tree.body)}")
    
    # Show what's in the tree
    print("\nTop-level nodes:")
    for node in tree.body:
        print(f"  - {type(node).__name__}", end="")
        if hasattr(node, 'name'):
            print(f": {node.name}")
        else:
            print()
    
    # Debug: Print full AST structure
    print("\nFull AST structure (first 500 chars):")
    ast_dump = ast.dump(tree, indent=2)
    print(ast_dump[:500] + "...")
    
    print("\n✓ To parse a file: tree = ast.parse(Path('file.py').read_text())")
    print("✓ To parse a string: tree = ast.parse(source_code)")

