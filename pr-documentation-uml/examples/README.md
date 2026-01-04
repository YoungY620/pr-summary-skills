# Static Analysis Examples

This directory contains executable Python examples demonstrating how to use the static analysis tool for different code patterns.

## Available Examples

### 01_basic_class_analysis.py
Demonstrates analyzing a simple class with methods and attributes.

**Run:**
```bash
python3 01_basic_class_analysis.py
```

**Functions:**
- `analyze_basic_class(code: str) -> dict` - Analyze a basic class
- `generate_mermaid_class_diagram(analysis_result: dict) -> str` - Generate UML

### 02_inheritance_analysis.py
Demonstrates analyzing class hierarchies with inheritance relationships.

**Run:**
```bash
python3 02_inheritance_analysis.py
```

**Functions:**
- `analyze_inheritance(code: str) -> dict` - Analyze inheritance
- `generate_mermaid_inheritance_diagram(analysis_result: dict) -> str` - Generate UML

### 03_decorator_analysis.py
Demonstrates analyzing classes with decorators, properties, static/class methods.

**Run:**
```bash
python3 03_decorator_analysis.py
```

**Functions:**
- `analyze_decorators(code: str) -> dict` - Analyze decorators
- `generate_mermaid_with_decorators(analysis_result: dict) -> str` - Generate UML

## Usage

Each example can be:

1. **Run directly** to see demonstration output:
   ```bash
   python3 01_basic_class_analysis.py
   ```

2. **Imported as a module** to use the functions:
   ```python
   import sys
   from pathlib import Path
   sys.path.insert(0, str(Path("../scripts")))
   
   import importlib.util
   spec = importlib.util.spec_from_file_location("example", "01_basic_class_analysis.py")
   example = importlib.util.module_from_spec(spec)
   spec.loader.exec_module(example)
   
   result = example.analyze_basic_class(your_code)
   ```

3. **Used as reference** for your own analysis code

## Testing

Each example has corresponding tests in the `tests/` directory:

```bash
cd ../tests
python3 test_01_basic_class_analysis.py
python3 test_02_inheritance_analysis.py
python3 test_03_decorator_analysis.py
```

Or run all tests:

```bash
cd ../tests
python3 -m pytest
```

## Example Output

Running an example produces:

1. **Sample Code** - The code being analyzed
2. **Analysis Result** - Extracted structure (classes, methods, etc.)
3. **Full Analysis Output** - Detailed text format
4. **Generated Mermaid Diagram** - Ready-to-use UML code
5. **Key Points** - What to note about accuracy

## Integration with PR Documentation

Use these examples as templates for your own PR documentation workflow:

1. Identify modified files in your PR
2. Run analysis on each file
3. Extract exact names (classes, methods, parameters)
4. Use names to generate accurate UML diagrams
5. Include diagrams in PR documentation

## Requirements

- Python 3.10+
- No external dependencies (uses standard library)
- Access to `../scripts/analyze_code.py`

