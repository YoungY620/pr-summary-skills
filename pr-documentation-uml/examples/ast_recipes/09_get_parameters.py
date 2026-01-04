#!/usr/bin/env python3
"""
Recipe 09: Get Function Parameters

Shows how to extract parameter information including types and defaults.
Pure ast operations.
"""

import ast

SAMPLE_CODE = '''
def simple(a, b):
    pass

def with_types(name: str, age: int) -> str:
    return f"{name} is {age}"

def with_defaults(x: int = 10, y: str = "default"):
    pass

def complex(
    required: str,
    optional: int = 0,
    *args: int,
    flag: bool = True,
    **kwargs: str
) -> dict:
    pass
'''

if __name__ == "__main__":
    print("=" * 60)
    print("Recipe 09: Get Function Parameters")
    print("=" * 60)
    
    tree = ast.parse(SAMPLE_CODE)
    functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    
    for func in functions:
        print(f"\nFunction: {func.name}")
        
        # Regular arguments
        print("  Parameters:")
        args = func.args
        
        # Get regular args
        for i, arg in enumerate(args.args):
            param_name = arg.arg
            
            # Get type annotation
            type_ann = ast.unparse(arg.annotation) if arg.annotation else "no type"
            
            # Get default value (if any)
            # defaults are aligned with the LAST args
            num_args = len(args.args)
            num_defaults = len(args.defaults)
            default_offset = num_args - num_defaults
            
            if i >= default_offset:
                default_idx = i - default_offset
                default_val = ast.unparse(args.defaults[default_idx])
                print(f"    {param_name}: {type_ann} = {default_val}")
            else:
                print(f"    {param_name}: {type_ann}")
        
        # *args
        if args.vararg:
            vararg_type = ast.unparse(args.vararg.annotation) if args.vararg.annotation else "any"
            print(f"    *{args.vararg.arg}: {vararg_type}")
        
        # Keyword-only args
        if args.kwonlyargs:
            for kwarg, default in zip(args.kwonlyargs, args.kw_defaults):
                kwarg_name = kwarg.arg
                kwarg_type = ast.unparse(kwarg.annotation) if kwarg.annotation else "no type"
                kwarg_default = ast.unparse(default) if default else "required"
                print(f"    {kwarg_name}: {kwarg_type} = {kwarg_default}")
        
        # **kwargs
        if args.kwarg:
            kwarg_type = ast.unparse(args.kwarg.annotation) if args.kwarg.annotation else "any"
            print(f"    **{args.kwarg.arg}: {kwarg_type}")
        
        # Return type
        if func.returns:
            print(f"  Returns: {ast.unparse(func.returns)}")
    
    print("\n" + "=" * 60)
    print("Key Points:")
    print("=" * 60)
    print("✓ func.args - arguments object")
    print("✓ func.args.args - list of regular parameters")
    print("✓ func.args.defaults - default values (aligned from right)")
    print("✓ func.args.vararg - *args parameter (or None)")
    print("✓ func.args.kwonlyargs - keyword-only parameters")
    print("✓ func.args.kw_defaults - defaults for keyword-only")
    print("✓ func.args.kwarg - **kwargs parameter (or None)")
    print("✓ arg.arg - parameter name")
    print("✓ arg.annotation - type annotation (or None)")
    print("✓ func.returns - return type annotation (or None)")

