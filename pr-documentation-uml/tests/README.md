# Tests

Comprehensive tests for the static analysis examples to ensure correctness and reliability.

## Test Files

- `test_01_basic_class_analysis.py` - Tests for basic class analysis (8 tests)
- `test_02_inheritance_analysis.py` - Tests for inheritance analysis (10 tests)
- `test_03_decorator_analysis.py` - Tests for decorator analysis (14 tests)
- `conftest.py` - Shared fixtures and configuration
- `run_all_tests.py` - Legacy test runner (deprecated)

## Setup

Install test dependencies:

```bash
pip install -r requirements-dev.txt
```

Or install just pytest:

```bash
pip install pytest
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run with Verbose Output

```bash
pytest -v
```

### Run Specific Test File

```bash
pytest tests/test_01_basic_class_analysis.py
pytest tests/test_02_inheritance_analysis.py
pytest tests/test_03_decorator_analysis.py
```

### Run Specific Test Function

```bash
pytest tests/test_01_basic_class_analysis.py::test_analyze_basic_class
```

### Run Tests by Marker

```bash
# Run only basic tests
pytest -m basic

# Run only inheritance tests
pytest -m inheritance

# Run only decorator tests
pytest -m decorators
```

### Run Tests in Parallel

```bash
pytest -n auto
```

### Generate Coverage Report

```bash
pytest --cov=scripts --cov=examples --cov-report=html
```

Then open `htmlcov/index.html` to view the report.

## Test Coverage

### test_01_basic_class_analysis.py (8 tests)

✓ **Basic Analysis Tests** (`@pytest.mark.basic`)
- Class name extraction
- Method detection
- Method signatures with parameters and return types
- Import detection
- Mermaid diagram generation
- Empty code handling
- Simple class fixture
- Grouped tests for class name extraction

### test_02_inheritance_analysis.py (10 tests)

✓ **Inheritance Tests** (`@pytest.mark.inheritance`)
- Inheritance relationship detection
- Methods grouped by class
- Abstract method detection
- Method overriding detection
- Class-specific methods
- Mermaid inheritance diagram generation
- Method signature preservation
- Simple inheritance fixture
- Single level inheritance
- Multiple inheritance

### test_03_decorator_analysis.py (14 tests)

✓ **Decorator Tests** (`@pytest.mark.decorators`)
- Property vs method distinction
- Static method detection
- Class method detection
- Custom decorator capture (lru_cache, etc.)
- Class-level attribute detection
- Type annotation preservation
- Property setter detection
- Mermaid diagram with decorators
- Method parameter extraction
- Decorator fixture
- Property decorator
- Staticmethod decorator
- Classmethod decorator

**Total: 32 tests**

## Test Philosophy

These tests ensure that:

1. **Accuracy**: All extracted names match actual code exactly
2. **Completeness**: All relevant code elements are detected
3. **Correctness**: Analysis logic handles edge cases properly
4. **Reliability**: Functions work with various code patterns

## Pytest Features Used

### Fixtures (conftest.py)

- `example_01`, `example_02`, `example_03` - Session-scoped example modules
- `analyze_code` - Import analyze_code utilities
- `simple_class_code` - Sample simple class code
- `inheritance_code` - Sample inheritance code
- `decorator_code` - Sample decorator code

### Markers

Tests are marked for selective execution:
- `@pytest.mark.basic` - Basic class analysis tests
- `@pytest.mark.inheritance` - Inheritance tests
- `@pytest.mark.decorators` - Decorator tests

### Test Classes

Related tests are grouped using classes:
- `TestClassNameExtraction`
- `TestInheritanceDetection`
- `TestDecoratorTypes`

## Adding New Tests

When adding a new example, create a test file:

```python
"""Tests for your new example."""

import pytest

@pytest.mark.your_category
def test_your_feature(example_04):
    """Test your new feature using fixture."""
    result = example_04.your_function(example_04.SAMPLE_CODE)
    assert result["expected_key"] == "expected_value"
```

Add fixture to `conftest.py`:

```python
@pytest.fixture(scope="session")
def example_04():
    """Load your new example."""
    return load_example_module("04_your_example")
```

## CI/CD Integration

These tests are designed to be easily integrated into CI/CD pipelines:

```bash
# In your CI script
cd skills/pr-documentation-uml/tests
for test_file in test_*.py; do
    python3 "$test_file" || exit 1
done
```

Or with pytest:

```bash
cd skills/pr-documentation-uml
pytest tests/ --verbose
```

## Requirements

- Python 3.10+
- No external dependencies for basic test execution
- pytest (optional, for advanced features)

## Expected Output

### Pytest Output

```bash
$ pytest -v

========================== test session starts ===========================
collected 32 items

tests/test_01_basic_class_analysis.py::test_analyze_basic_class PASSED [ 3%]
tests/test_01_basic_class_analysis.py::test_method_signatures PASSED [ 6%]
tests/test_01_basic_class_analysis.py::test_imports_detected PASSED [ 9%]
tests/test_01_basic_class_analysis.py::test_generate_mermaid_diagram PASSED [12%]
tests/test_01_basic_class_analysis.py::test_empty_code PASSED [15%]
tests/test_01_basic_class_analysis.py::test_simple_class_fixture PASSED [18%]
tests/test_01_basic_class_analysis.py::TestClassNameExtraction::test_single_class PASSED [21%]
tests/test_01_basic_class_analysis.py::TestClassNameExtraction::test_class_with_docstring PASSED [25%]
...
========================== 32 passed in 0.50s ============================
```

### With Coverage

```bash
$ pytest --cov=scripts --cov=examples --cov-report=term-missing

---------- coverage: platform darwin, python 3.12.0 -----------
Name                                    Stmts   Miss  Cover   Missing
---------------------------------------------------------------------
scripts/analyze_code.py                   200      5    97%   45-47
examples/01_basic_class_analysis.py        50      0   100%
examples/02_inheritance_analysis.py        65      0   100%
examples/03_decorator_analysis.py          75      0   100%
---------------------------------------------------------------------
TOTAL                                     390      5    99%
```

## Troubleshooting

If tests fail:

1. **Check Python version**: Requires 3.10+
2. **Verify paths**: Tests expect specific directory structure
3. **Check analyze_code.py**: Ensure the analysis tool is working
4. **Read error messages**: Tests provide descriptive failure messages

