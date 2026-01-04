# Static Analysis Scripts

This directory contains tools for analyzing Python code to extract accurate structure information for UML diagram generation.

## Design Philosophy

### ❌ No Low-Level API - Use AST Recipes Instead!

We **don't provide wrapper functions**. Instead, we provide **recipes** showing how to use Python's `ast` module directly.

**Why?**
- ✅ Learn `ast` module properly
- ✅ No abstraction overhead
- ✅ Copy-paste ready code
- ✅ Full flexibility
- ✅ No dependencies beyond stdlib

**See**: `../examples/ast_recipes/` for pure AST usage examples.

### analyze_code.py (High-Level Tool)

**Command-line tool** for complete file analysis.

- Structured output (FileAnalysis)
- JSON serialization support
- Command-line interface
- Good for standard use cases

**When to use**: Quick file analysis, JSON output, standard UML generation.

### Usage

```bash
# Analyze a single file
python analyze_code.py path/to/file.py

# Analyze multiple files
python analyze_code.py src/module1.py src/module2.py src/module3.py

# Output as JSON
python analyze_code.py --format json path/to/file.py
```

### Features

- **Class Analysis**
  - Class names
  - Base classes (inheritance)
  - Class attributes with type annotations
  - Methods with signatures
  - Decorators
  - Docstrings

- **Method Analysis**
  - Method names
  - Parameters with type annotations
  - Return types
  - Decorators (@property, @staticmethod, @classmethod, etc.)
  - Public/private visibility

- **Function Analysis**
  - Function names
  - Parameters with type annotations
  - Return types
  - Decorators

- **Import Analysis**
  - Module imports
  - From imports
  - Import aliases

### Output Format

#### Text Format (Default)

```
File: src/models/user.py

Imports:
  - from datetime import import datetime
  - from typing import import Optional

Classes:
  User
    Attributes:
      - username: str
      - email: str
      - created_at: datetime
    Methods:
      + __init__(username: str, email: str) -> None
      + activate() -> None
      + deactivate() -> None

Functions:
  create_user(username: str, email: str) -> User
```

#### JSON Format

```json
{
  "file_path": "src/models/user.py",
  "imports": [...],
  "classes": [...],
  "functions": [...]
}
```

### Requirements

- Python 3.12+
- No external dependencies (uses standard library `ast` module)

### Limitations

- Only analyzes Python files (.py)
- Does not evaluate dynamic code
- Type annotations must be present in source code
- Complex type expressions may be simplified

### Examples

See `examples/analysis/` directory for detailed usage examples:

- `01-basic-class-analysis.md` - Simple class analysis
- `02-inheritance-analysis.md` - Class hierarchies
- `03-decorator-analysis.md` - Properties and decorators
- `04-complete-workflow.md` - End-to-end PR documentation workflow

### Integration with UML Generation

The analysis output provides exact names for UML diagrams:

1. Run `analyze_code.py` on modified files
2. Copy class/method/function names from output
3. Use exact names in Mermaid diagrams
4. Ensure all code elements match analysis

### Error Handling

- **File not found**: Error message, continues with other files
- **Syntax errors**: Reports error, skips file
- **Non-Python files**: Warning, skips file

### Exit Codes

- `0` - Success
- Non-zero - Errors occurred (check stderr)

