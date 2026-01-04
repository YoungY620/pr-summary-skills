#!/usr/bin/env python3
"""
Recipe 17: Filter Nodes by Custom Condition

Shows how to find nodes matching custom criteria.
Direct ast.walk() + filtering.
"""

import ast

SAMPLE_CODE = '''
class UserService:
    def create_user(self, name: str, email: str) -> User:
        pass
    
    def update_user(self, user_id: int, data: dict) -> User:
        pass
    
    def delete_user(self, user_id: int) -> bool:
        pass
    
    def get_user(self, user_id: int) -> User:
        pass
    
    def _validate_email(self, email: str) -> bool:
        pass
    
    @staticmethod
    def hash_password(password: str) -> str:
        pass

def process_data(items: list):
    pass

def validate(data: dict) -> bool:
    pass
'''

if __name__ == "__main__":
    print("=" * 60)
    print("Recipe 17: Filter by Custom Condition")
    print("=" * 60)
    
    tree = ast.parse(SAMPLE_CODE)
    
    # Example 1: Find methods that return User
    print("\n1. Methods returning 'User':")
    user_returning_methods = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
        and node.returns
        and 'User' in ast.unparse(node.returns)
    ]
    for method in user_returning_methods:
        print(f"  - {method.name}()")
    
    # Example 2: Find methods with more than 2 parameters
    print("\n2. Methods with >2 parameters (excluding self):")
    complex_methods = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
        and len(node.args.args) > 2  # Includes self
    ]
    for method in complex_methods:
        params = [arg.arg for arg in method.args.args]
        print(f"  - {method.name}({', '.join(params)})")
    
    # Example 3: Find methods starting with 'get_' or 'create_'
    print("\n3. CRUD methods (get_*, create_*, update_*, delete_*):")
    crud_methods = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
        and any(node.name.startswith(prefix) 
                for prefix in ['get_', 'create_', 'update_', 'delete_'])
    ]
    for method in crud_methods:
        print(f"  - {method.name}()")
    
    # Example 4: Find methods with 'user' in their name (case-insensitive)
    print("\n4. Methods with 'user' in name:")
    user_methods = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
        and 'user' in node.name.lower()
    ]
    for method in user_methods:
        print(f"  - {method.name}()")
    
    # Example 5: Find methods with decorators
    print("\n5. Methods with decorators:")
    decorated_methods = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
        and node.decorator_list
    ]
    for method in decorated_methods:
        decorators = [ast.unparse(d) for d in method.decorator_list]
        print(f"  - {method.name}: {decorators}")
    
    # Example 6: Find methods that take dict parameter
    print("\n6. Methods taking dict parameter:")
    dict_param_methods = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
        and any(
            arg.annotation and 'dict' in ast.unparse(arg.annotation).lower()
            for arg in node.args.args
        )
    ]
    for method in dict_param_methods:
        print(f"  - {method.name}()")
    
    # Example 7: Find classes with specific methods
    print("\n7. Classes with 'create_*' methods:")
    classes_with_create = []
    for cls_node in [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]:
        has_create = any(
            isinstance(n, ast.FunctionDef) and n.name.startswith('create_')
            for n in cls_node.body
        )
        if has_create:
            classes_with_create.append(cls_node.name)
    print(f"  {classes_with_create}")
    
    print("\n" + "=" * 60)
    print("Pattern:")
    print("=" * 60)
    print("filtered = [")
    print("    node for node in ast.walk(tree)")
    print("    if isinstance(node, NodeType)")
    print("    and custom_condition(node)")
    print("]")

