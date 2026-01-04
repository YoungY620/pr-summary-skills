#!/usr/bin/env python3
"""
Recipe 21: Generate Mermaid Class Diagram

Shows how to generate UML class diagram from AST.
Pure ast operations - builds Mermaid syntax directly.
"""

import ast

SAMPLE_CODE = '''
from typing import Optional

class BaseAuthenticator:
    def authenticate(self, credentials: dict) -> Optional[str]:
        pass
    
    def validate_token(self, token: str) -> bool:
        pass

class JWTAuthenticator(BaseAuthenticator):
    secret_key: str
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
    
    def authenticate(self, credentials: dict) -> Optional[str]:
        return "token"
    
    def validate_token(self, token: str) -> bool:
        return True
    
    def generate_token(self, user_id: int) -> str:
        return "jwt_token"
    
    @staticmethod
    def parse_token(token: str) -> dict:
        return {}
'''

if __name__ == "__main__":
    print("=" * 60)
    print("Recipe 21: Generate Mermaid Class Diagram")
    print("=" * 60)
    
    tree = ast.parse(SAMPLE_CODE)
    
    # Start Mermaid diagram
    lines = ["```mermaid", "classDiagram"]
    
    # Find all classes
    classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    
    for cls in classes:
        # Add class definition
        lines.append(f"    class {cls.name} {{")
        
        # Add class-level attributes
        for item in cls.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                attr_name = item.target.id
                attr_type = ast.unparse(item.annotation) if item.annotation else "any"
                lines.append(f"        +{attr_name}: {attr_type}")
        
        # Add methods (skip __init__ and private for clarity)
        methods = [n for n in cls.body if isinstance(n, ast.FunctionDef)]
        for method in methods:
            # Skip __init__ and dunder methods
            if method.name.startswith('__'):
                continue
            
            # Check if static/class method
            is_static = any('staticmethod' in ast.unparse(d) for d in method.decorator_list)
            is_classmethod = any('classmethod' in ast.unparse(d) for d in method.decorator_list)
            
            # Get parameters (skip self/cls)
            params = []
            for i, arg in enumerate(method.args.args):
                if i == 0 and arg.arg in ('self', 'cls'):
                    continue
                param_str = arg.arg
                if arg.annotation:
                    param_str += f": {ast.unparse(arg.annotation)}"
                params.append(param_str)
            
            param_str = ", ".join(params)
            
            # Get return type
            ret_str = ""
            if method.returns:
                ret_str = f" {ast.unparse(method.returns)}"
            
            # Add $ for static methods
            method_marker = "$" if (is_static or is_classmethod) else ""
            
            lines.append(f"        +{method.name}({param_str}){method_marker}{ret_str}")
        
        lines.append("    }")
        lines.append("")
    
    # Add inheritance relationships
    for cls in classes:
        for base in cls.bases:
            base_name = ast.unparse(base)
            lines.append(f"    {base_name} <|-- {cls.name}")
    
    lines.append("```")
    
    # Print result
    diagram = "\n".join(lines)
    print("\nGenerated Mermaid Diagram:")
    print(diagram)
    
    print("\n" + "=" * 60)
    print("Key Steps:")
    print("=" * 60)
    print("1. Find all classes with ast.walk(tree)")
    print("2. For each class:")
    print("   - Extract attributes from AnnAssign nodes")
    print("   - Extract methods from FunctionDef nodes")
    print("   - Check decorator_list for @staticmethod/@classmethod")
    print("   - Build method signature from args.args and returns")
    print("3. Extract inheritance from cls.bases")
    print("4. Build Mermaid syntax string")
    print("\n✓ No wrapper functions needed!")
    print("✓ Direct control over output format")
    print("✓ Easy to customize diagram style")

