# API Comparison: Low-Level vs High-Level

This document shows side-by-side comparisons of using the low-level API (`ast_utils.py`) vs the high-level API (`analyze_code.py`).

## Example 1: Get All Class Names

### Low-Level API ✨
```python
from ast_utils import *

tree = parse_file("myfile.py")
classes = get_classes(tree)
class_names = [cls.name for cls in classes]
```

**Pros**: Direct, simple, no overhead  
**Lines**: 4

### High-Level API
```python
from analyze_code import analyze_file

analysis = analyze_file("myfile.py")
class_names = [cls.name for cls in analysis.classes]
```

**Pros**: Structured output  
**Lines**: 3

**Winner**: Tie - both are simple for this case

---

## Example 2: Find Properties Only

### Low-Level API ✨
```python
from ast_utils import *

tree = parse_file("myfile.py")
cls = get_classes(tree)[0]
properties = get_properties(cls)
prop_names = [p.name for p in properties]
```

**Pros**: Dedicated function for properties  
**Lines**: 5

### High-Level API
```python
from analyze_code import analyze_file

analysis = analyze_file("myfile.py")
cls = analysis.classes[0]
prop_names = [m.name for m in cls.methods if m.is_property]
```

**Pros**: All info in one structure  
**Lines**: 4

**Winner**: Low-level - more direct

---

## Example 3: Custom Filter (Methods with >3 params)

### Low-Level API ✨✨✨
```python
from ast_utils import *

tree = parse_file("myfile.py")
complex_methods = filter_nodes(tree, lambda n:
    isinstance(n, ast.FunctionDef) and
    len(get_function_parameters(n)) > 3
)
```

**Pros**: Easy custom filtering  
**Lines**: 5

### High-Level API
```python
# NOT POSSIBLE without modifying CodeAnalyzer class!
# You'd need to add a new visitor method or post-process
from analyze_code import analyze_file

analysis = analyze_file("myfile.py")
# Have to iterate through all classes and functions manually
complex_methods = []
for cls in analysis.classes:
    for method in cls.methods:
        if len(method.parameters) > 3:
            complex_methods.append(method)
for func in analysis.functions:
    if len(func.parameters) > 3:
        complex_methods.append(func)
```

**Cons**: Verbose, no direct filtering  
**Lines**: 10+

**Winner**: Low-level - much more flexible!

---

## Example 4: Extract Method Call Graph

### Low-Level API ✨✨✨
```python
from ast_utils import *

tree = parse_file("myfile.py")

def get_called_functions(func):
    """Extract all function calls in a function."""
    calls = find_nodes(func, ast.Call)
    return [unparse_node(call.func) for call in calls]

call_graph = {}
for func in get_functions(tree):
    call_graph[func.name] = get_called_functions(func)
```

**Pros**: Full control over extraction  
**Lines**: 10

### High-Level API
```python
# NOT DIRECTLY SUPPORTED!
# Would need to:
# 1. Parse the file again with ast
# 2. Or add this feature to CodeAnalyzer
# 3. Or use ast_utils anyway

# Cannot extract call graph from FileAnalysis structure
```

**Winner**: Low-level - high-level doesn't support this!

---

## Example 5: Analyze Single Method

### Low-Level API ✨
```python
from ast_utils import *

tree = parse_file("myfile.py")
cls = get_classes(tree)[0]
method = find_nodes_by_name(cls, ast.FunctionDef, "process_data")[0]

info = {
    'name': method.name,
    'params': [p.arg for p in get_function_parameters(method)],
    'return_type': get_return_annotation(method),
    'decorators': get_decorators(method),
    'docstring': get_docstring(method)
}
```

**Pros**: Extract only what you need  
**Lines**: 10

### High-Level API
```python
from analyze_code import analyze_file

analysis = analyze_file("myfile.py")  # Analyzes ENTIRE file
cls = analysis.classes[0]
method = next(m for m in cls.methods if m.name == "process_data")

info = {
    'name': method.name,
    'params': [p.name for p in method.parameters],
    'return_type': method.return_type,
    'decorators': method.decorators,
    'docstring': method.docstring
}
```

**Cons**: Analyzes whole file even if you need one method  
**Lines**: 11

**Winner**: Low-level - more efficient

---

## Example 6: Build a Custom Mermaid Generator

### Low-Level API ✨✨✨
```python
from ast_utils import *

def generate_simple_class_diagram(file_path):
    """Generate minimal class diagram."""
    tree = parse_file(file_path)
    
    lines = ["```mermaid", "classDiagram"]
    
    for cls in get_classes(tree):
        lines.append(f"    class {cls.name} {{")
        
        # Only public methods
        for method in get_public_methods(cls):
            params = ", ".join(p.arg for p in get_function_parameters(method))
            lines.append(f"        +{method.name}({params})")
        
        lines.append("    }")
        
        # Inheritance
        for base in get_class_bases(cls):
            lines.append(f"    {base} <|-- {cls.name}")
    
    lines.append("```")
    return "\n".join(lines)
```

**Pros**: Full control over output format  
**Lines**: 23

### High-Level API
```python
from analyze_code import analyze_file

def generate_simple_class_diagram(file_path):
    """Generate minimal class diagram."""
    analysis = analyze_file(file_path)
    
    lines = ["```mermaid", "classDiagram"]
    
    for cls in analysis.classes:
        lines.append(f"    class {cls.name} {{")
        
        # Have to filter manually
        for method in cls.methods:
            if not method.name.startswith('_'):
                params = ", ".join(p.name for p in method.parameters)
                lines.append(f"        +{method.name}({params})")
        
        lines.append("    }")
        
        for base in cls.bases:
            lines.append(f"    {base} <|-- {cls.name}")
    
    lines.append("```")
    return "\n".join(lines)
```

**Cons**: Same length but less flexible  
**Lines**: 22

**Winner**: Low-level - easier to customize

---

## Summary

| Use Case | Low-Level API | High-Level API | Winner |
|----------|---------------|----------------|--------|
| Get all class names | ✓ Simple | ✓ Simple | Tie |
| Find properties | ✓✓ Dedicated function | ✓ Manual filter | Low-level |
| Custom filtering | ✓✓✓ Easy | ✗ Difficult | Low-level |
| Call graph analysis | ✓✓✓ Supported | ✗ Not supported | Low-level |
| Single method analysis | ✓✓ Efficient | ✓ Inefficient | Low-level |
| Custom UML generator | ✓✓✓ Full control | ✓ Limited | Low-level |
| Complete file analysis | ✓ Manual | ✓✓ Automatic | High-level |
| JSON serialization | ✗ Manual | ✓✓✓ Built-in | High-level |
| Command-line usage | ✓ Possible | ✓✓✓ Ready | High-level |

## Recommendations

### Use Low-Level API (`ast_utils.py`) when:

✅ Building custom analyzers  
✅ Need fine-grained control  
✅ Extracting specific information  
✅ Handling edge cases  
✅ Performance is important  
✅ Exploring/experimenting  

### Use High-Level API (`analyze_code.py`) when:

✅ Need complete file analysis  
✅ Want JSON output  
✅ Using from command line  
✅ Quick prototyping  
✅ Standard use cases  

## The Best Approach: Use Both!

```python
# Start with low-level for exploration
from ast_utils import *

tree = parse_file("myfile.py")
classes = get_classes(tree)

# Once you know what you need, build a specialized function
def extract_my_data(tree):
    # Use ast_utils functions
    return custom_result

# For standard analysis, use high-level
from analyze_code import analyze_file
full_analysis = analyze_file("myfile.py")  # Get everything
```

**The low-level API is the foundation - use it to build exactly what you need!**

