# AST Recipes - Direct Python AST Usage

This directory contains **pure examples** of using Python's `ast` module directly, with **no abstraction or wrapper functions**.

## Philosophy

❌ **No wrapper functions**  
❌ **No helper classes**  
❌ **No abstraction layers**  

✅ **Pure `ast` module usage**  
✅ **Copy-paste ready code**  
✅ **Learn by example**  

## How to Use

Each recipe is a standalone Python script showing how to accomplish a specific task using `ast` module directly.

1. **Read the recipe** - Understand the pattern
2. **Copy the code** - Use it in your own project
3. **Modify as needed** - Adapt to your specific needs

## Recipe Index

### Basic Operations
- `01_parse_code.py` - Parse Python code into AST
- `02_walk_tree.py` - Traverse AST nodes
- `03_find_all_classes.py` - Find all class definitions
- `04_find_all_functions.py` - Find all function definitions

### Class Information
- `05_get_class_bases.py` - Extract base classes
- `06_get_class_methods.py` - Extract class methods
- `07_get_class_attributes.py` - Extract class attributes
- `08_check_decorators.py` - Check for decorators

### Function/Method Information
- `09_get_parameters.py` - Extract function parameters
- `10_get_return_type.py` - Extract return type annotation
- `11_get_docstring.py` - Extract docstrings
- `12_check_method_type.py` - Check if property/static/class method

### Type Annotations
- `13_get_type_annotations.py` - Extract type hints
- `14_parse_complex_types.py` - Handle complex type expressions

### Imports
- `15_find_imports.py` - Find import statements
- `16_extract_import_names.py` - Extract imported names

### Custom Queries
- `17_filter_by_condition.py` - Custom filtering
- `18_find_by_name.py` - Find nodes by name
- `19_count_calls.py` - Count function calls
- `20_analyze_complexity.py` - Calculate complexity metrics

### Generate UML
- `21_generate_class_diagram.py` - Generate Mermaid class diagram
- `22_generate_sequence_diagram.py` - Generate sequence diagram from calls

## Example Structure

Each recipe follows this structure:

```python
#!/usr/bin/env python3
"""
Recipe: [What it does]

Direct usage of ast module to [accomplish task].
No wrapper functions - pure ast operations.
"""

import ast

# Sample code to analyze
SAMPLE_CODE = '''
# Your sample Python code here
'''

# Main example code
if __name__ == "__main__":
    # Parse code
    tree = ast.parse(SAMPLE_CODE)
    
    # Direct ast operations
    # ... your code here ...
    
    # Print results
    print(results)
```

## Learning Path

### Beginner
Start with: 01, 02, 03, 04, 11

### Intermediate
Continue with: 05, 06, 09, 15, 17

### Advanced
Master: 19, 20, 21, 22

## Key ast Module Functions

### Parsing
- `ast.parse(source)` - Parse code string into AST
- `ast.unparse(node)` - Convert AST node back to code

### Traversal
- `ast.walk(node)` - Recursively yield all nodes
- `ast.NodeVisitor` - Visitor pattern for traversal

### Node Types
- `ast.Module`, `ast.ClassDef`, `ast.FunctionDef`
- `ast.Import`, `ast.ImportFrom`
- `ast.Assign`, `ast.AnnAssign`
- `ast.Call`, `ast.Attribute`, `ast.Name`

### Utilities
- `ast.get_docstring(node)` - Get docstring
- `ast.dump(node)` - Debug print AST structure
- `isinstance(node, ast.ClassDef)` - Type checking

## Tips

1. **Start simple** - Begin with basic recipes
2. **Print AST structure** - Use `ast.dump()` to understand nodes
3. **Check node types** - Use `isinstance()` to filter
4. **Access attributes directly** - `node.name`, `node.args`, etc.
5. **Combine recipes** - Mix and match patterns for complex queries

## No Abstractions!

All code in these recipes uses `ast` module directly. If you need reusable functions, create them yourself by extracting patterns from these examples.

The goal is to **teach you how to use ast**, not to provide a library.

