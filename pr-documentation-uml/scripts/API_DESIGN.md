# API Design: High-Level vs Low-Level

This document explains the two-tier API design for code analysis.

## Problem with Original Design

The original `analyze_code.py` had these issues:

1. **Over-abstraction**: Forced use of specific data structures (ClassInfo, Method, etc.)
2. **Lack of flexibility**: Hard to customize for specific needs
3. **Difficult to extend**: Adding new features required modifying core classes
4. **Coarse-grained**: No way to extract just one piece of information

### Example of the Problem

```python
# Want to just get method names? You get the whole ClassInfo structure!
analysis = analyze_file("myfile.py")
class_info = analysis.classes[0]
method_names = [m.name for m in class_info.methods]  # Unnecessarily complex
```

## New Two-Tier Design

### Tier 1: Low-Level API (`ast_utils.py`)

**Philosophy**: Provide fine-grained, composable functions that directly work with AST nodes.

**Benefits**:
- ✅ Fine-grained control
- ✅ Composable functions
- ✅ No forced data structures
- ✅ Direct AST access
- ✅ Easy to extend
- ✅ Handles edge cases

**Example**:
```python
from ast_utils import *

tree = parse_file("myfile.py")
classes = get_classes(tree)
for cls in classes:
    methods = get_class_methods(cls)
    method_names = [m.name for m in methods]  # Simple and direct
```

### Tier 2: High-Level API (`analyze_code.py`)

**Philosophy**: Convenience layer built on top of `ast_utils` for common use cases.

**Benefits**:
- ✅ Quick to use for standard cases
- ✅ Structured output
- ✅ JSON serialization
- ✅ Pretty-print formatting

**When to use**: When you need a complete analysis with all details.

**Example**:
```python
from analyze_code import analyze_file

result = analyze_file("myfile.py")
# Get everything at once
```

## Function Layers in `ast_utils.py`

### Layer 1: Raw AST Operations
Thin wrappers around `ast` module:
- `parse_file()` / `parse_code()`
- `unparse_node()`
- `get_docstring()`
- `dump_tree()`
- `walk_nodes()`

### Layer 2: Node Extraction
Find and filter nodes:
- `find_nodes(tree, ast.ClassDef)`
- `filter_nodes(tree, predicate)`
- `get_classes()` / `get_functions()` / `get_imports()`

### Layer 3: Information Extraction
Extract info from specific nodes:
- `get_class_bases(class_node)`
- `get_function_parameters(func_node)`
- `get_decorators(node)`
- `get_annotation(node)`

### Layer 4: Composite Queries
Higher-level convenience functions:
- `get_public_methods(class_node)`
- `get_properties(class_node)`
- `is_property()` / `is_staticmethod()` / `is_classmethod()`

## Comparison

### Task: Get all property methods from a class

**Low-Level API** (ast_utils.py):
```python
from ast_utils import *

tree = parse_file("file.py")
cls = get_classes(tree)[0]
properties = get_properties(cls)  # Direct and simple
```

**High-Level API** (analyze_code.py):
```python
from analyze_code import analyze_file

analysis = analyze_file("file.py")
cls = analysis.classes[0]
properties = [m for m in cls.methods if m.is_property]  # More abstraction
```

### Task: Custom analysis (find methods with >3 parameters)

**Low-Level API**:
```python
from ast_utils import *

tree = parse_file("file.py")
complex_methods = filter_nodes(tree, lambda n:
    isinstance(n, ast.FunctionDef) and
    len(get_function_parameters(n)) > 3
)
# Easy to write custom logic!
```

**High-Level API**:
```python
# Not possible without modifying the analyzer!
# You'd need to extend CodeAnalyzer class
```

### Task: Build a custom UML generator

**Low-Level API**:
```python
from ast_utils import *

def generate_sequence_diagram(tree):
    functions = get_functions(tree)
    for func in functions:
        calls = find_nodes(func, ast.Call)
        # Build diagram from call graph
        # Full control over output format
```

**High-Level API**:
```python
# Constrained by the predefined data structures
# Have to work with FileAnalysis format
```

## Best Practices

### Use Low-Level API When:

1. **Building custom analyzers** - You need fine-grained control
2. **Extracting specific information** - Don't need everything
3. **Handling edge cases** - Unusual code patterns
4. **Performance critical** - Don't want unnecessary data structures
5. **Exploring code** - Iterative development

### Use High-Level API When:

1. **Standard analysis** - Need complete file information
2. **JSON output** - Want structured, serializable data
3. **Quick prototyping** - Don't need customization
4. **Command-line tool** - Using `analyze_code.py` directly

## Migration Path

The high-level API (`analyze_code.py`) should be **refactored** to use `ast_utils.py` internally:

```python
# Current: analyze_code.py does everything itself
class CodeAnalyzer(ast.NodeVisitor):
    def visit_ClassDef(self, node):
        # Manual extraction
        ...

# Better: Use ast_utils functions
from ast_utils import *

def analyze_file(path):
    tree = parse_file(path)
    
    return FileAnalysis(
        classes=[_extract_class_info(cls) for cls in get_classes(tree)],
        functions=[_extract_func_info(f) for f in get_functions(tree)],
        imports=[_extract_import_info(imp) for imp in get_imports(tree)]
    )
```

## Example: Building a Complexity Analyzer

Using low-level API, you can easily build specialized analyzers:

```python
from ast_utils import *

def analyze_complexity(file_path):
    """Custom complexity analyzer."""
    tree = parse_file(file_path)
    
    results = {}
    for func in get_functions(tree):
        results[func.name] = {
            'params': len(get_function_parameters(func)),
            'calls': len(find_nodes(func, ast.Call)),
            'branches': len(find_nodes(func, ast.If)),
            'loops': len(find_nodes(func, ast.For)) + len(find_nodes(func, ast.While)),
            'complexity_score': _calculate_score(func)
        }
    return results
```

This would be difficult with the high-level API!

## Conclusion

**The low-level API (`ast_utils.py`) is the foundation.**

- Provides maximum flexibility
- Easy to compose and extend
- Direct access to Python's AST
- No abstraction penalty

**The high-level API (`analyze_code.py`) is a convenience layer.**

- Built on top of `ast_utils`
- Good for standard use cases
- Pre-defined output format
- Command-line friendly

**Both APIs coexist** - use the right tool for the job!

