# AST Recipes Index

Complete list of available recipes with quick reference.

## Recipe List

### ✅ Available Now

| # | Recipe | Description | Difficulty |
|---|--------|-------------|------------|
| 01 | `parse_code.py` | Parse Python code into AST | ⭐ Beginner |
| 03 | `find_all_classes.py` | Find all class definitions | ⭐ Beginner |
| 06 | `get_class_methods.py` | Extract methods from classes | ⭐⭐ Intermediate |
| 09 | `get_parameters.py` | Extract function parameters with types | ⭐⭐ Intermediate |
| 17 | `filter_by_condition.py` | Custom filtering patterns | ⭐⭐⭐ Advanced |
| 21 | `generate_class_diagram.py` | Generate Mermaid class diagram | ⭐⭐⭐ Advanced |

### 📝 To Be Added

| # | Recipe | Description |
|---|--------|-------------|
| 02 | `walk_tree.py` | Different ways to traverse AST |
| 04 | `find_all_functions.py` | Find function definitions |
| 05 | `get_class_bases.py` | Extract base classes |
| 07 | `get_class_attributes.py` | Extract class attributes |
| 08 | `check_decorators.py` | Work with decorators |
| 10 | `get_return_type.py` | Extract return annotations |
| 11 | `get_docstring.py` | Extract docstrings |
| 12 | `check_method_type.py` | Identify method types |
| 13 | `get_type_annotations.py` | Work with type hints |
| 14 | `parse_complex_types.py` | Handle complex types |
| 15 | `find_imports.py` | Find import statements |
| 16 | `extract_import_names.py` | Extract imported names |
| 18 | `find_by_name.py` | Find nodes by name |
| 19 | `count_calls.py` | Analyze function calls |
| 20 | `analyze_complexity.py` | Calculate complexity |
| 22 | `generate_sequence_diagram.py` | Generate sequence diagram |

## Quick Reference

### Parse Code
```python
import ast
tree = ast.parse(source_code)
```

### Find Nodes
```python
classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
```

### Extract Information
```python
# Class name
cls.name

# Base classes
[ast.unparse(base) for base in cls.bases]

# Methods
[n for n in cls.body if isinstance(n, ast.FunctionDef)]

# Parameters
[arg.arg for arg in func.args.args]

# Type annotation
ast.unparse(arg.annotation) if arg.annotation else None

# Return type
ast.unparse(func.returns) if func.returns else None

# Decorators
[ast.unparse(d) for d in node.decorator_list]

# Docstring
ast.get_docstring(node)
```

### Filter by Condition
```python
# Find all methods returning 'User'
[node for node in ast.walk(tree)
 if isinstance(node, ast.FunctionDef)
 and node.returns
 and 'User' in ast.unparse(node.returns)]
```

## Node Types Reference

### Common AST Node Types

| Node Type | Description | Key Attributes |
|-----------|-------------|----------------|
| `ast.Module` | Root node | `body` |
| `ast.ClassDef` | Class definition | `name`, `bases`, `body`, `decorator_list` |
| `ast.FunctionDef` | Function/method | `name`, `args`, `returns`, `body`, `decorator_list` |
| `ast.Import` | import statement | `names` |
| `ast.ImportFrom` | from-import | `module`, `names` |
| `ast.Assign` | Assignment | `targets`, `value` |
| `ast.AnnAssign` | Annotated assignment | `target`, `annotation`, `value` |
| `ast.Call` | Function call | `func`, `args`, `keywords` |
| `ast.Name` | Variable name | `id` |
| `ast.Attribute` | Attribute access | `value`, `attr` |
| `ast.arg` | Function argument | `arg`, `annotation` |

## Pattern Library

### Find all classes with specific base
```python
[cls for cls in ast.walk(tree)
 if isinstance(cls, ast.ClassDef)
 and any('BaseClass' in ast.unparse(base) for base in cls.bases)]
```

### Find methods with specific decorator
```python
[method for method in ast.walk(tree)
 if isinstance(method, ast.FunctionDef)
 and any('property' in ast.unparse(d) for d in method.decorator_list)]
```

### Find functions with >N parameters
```python
[func for func in ast.walk(tree)
 if isinstance(func, ast.FunctionDef)
 and len(func.args.args) > N]
```

### Find classes with specific methods
```python
[cls for cls in ast.walk(tree)
 if isinstance(cls, ast.ClassDef)
 and any(isinstance(n, ast.FunctionDef) and n.name == 'process'
         for n in cls.body)]
```

## Tips

1. **Always use `ast.unparse()`** to convert AST nodes back to code
2. **Use list comprehensions** for filtering
3. **Check `None` values** before accessing (e.g., `node.returns`)
4. **Use `ast.get_docstring()`** for docstrings (handles edge cases)
5. **Print `ast.dump(node)`** when exploring new node types

## Learning Path

### Day 1: Basics
- 01_parse_code.py
- 03_find_all_classes.py

### Day 2: Information Extraction
- 06_get_class_methods.py
- 09_get_parameters.py

### Day 3: Custom Queries
- 17_filter_by_condition.py

### Day 4: Building Tools
- 21_generate_class_diagram.py

## Why No Wrapper Functions?

✅ **Learn ast directly** - Understand how it really works  
✅ **Copy-paste ready** - Use code directly in your projects  
✅ **No dependencies** - Just Python stdlib  
✅ **Full flexibility** - Adapt to any use case  
✅ **Better debugging** - See exactly what's happening  

If you need reusable functions, **extract patterns from these examples** and build your own library!

