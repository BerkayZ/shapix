# Testing Guide for Shapix

This document describes the testing strategy and how to run tests for the Shapix geometry engine.

## Test Structure

```
tests/
├── __init__.py              # Test package init
├── conftest.py             # Pytest fixtures and configuration
├── pytest.ini             # Pytest configuration
├── run_tests.py            # Test runner script
├── unit/                   # Unit tests
│   ├── test_core.py       # Tests for core classes
│   ├── test_shapes.py     # Tests for shape classes
│   └── test_syntax.py     # Tests for syntax parsing
├── integration/           # Integration tests
│   └── test_end_to_end.py # End-to-end workflow tests
└── fixtures/              # Test data and fixtures
    └── sample_geometries.py # Sample geometry syntax
```

## Running Tests

### Basic Test Commands

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/unit/test_core.py

# Run specific test class
pytest tests/unit/test_shapes.py::TestCircle

# Run specific test method
pytest tests/unit/test_core.py::TestPoint::test_point_creation
```

### Using the Test Runner

```bash
# Run all tests
python tests/run_tests.py

# Run only unit tests
python tests/run_tests.py --unit

# Run only integration tests
python tests/run_tests.py --integration

# Run with coverage
python tests/run_tests.py --coverage

# Skip GUI-requiring tests
python tests/run_tests.py --no-gui

# Quick development tests
python tests/run_tests.py --quick
```

### Comprehensive Test Suite

```bash
# Run everything (tests + examples)
python run_all_tests.py
```

## Test Categories

### Unit Tests
- **Core Tests** (`test_core.py`): Point and GeometricShape base classes
- **Shape Tests** (`test_shapes.py`): Individual shape classes (Circle, Triangle, etc.)
- **Syntax Tests** (`test_syntax.py`): Geometry syntax parsing and export

### Integration Tests
- **End-to-End Tests** (`test_end_to_end.py`): Complete workflows from syntax to PNG
- **Performance Tests**: Large geometry parsing and memory usage
- **Mathematical Tests**: Verification of geometric relationships

### Test Fixtures
- Sample geometry definitions for consistent testing
- Temporary file handling for PNG export tests
- Mock objects for shapes and points

## Test Coverage

The test suite covers:

✅ **Core Classes**
- Point creation, manipulation, and calculations
- GeometricShape base functionality
- Property management and inheritance

✅ **Shape Classes**
- All shape types (Point, Line, Circle, Triangle, Angle)
- Mathematical calculations (area, perimeter, angles)
- Geometric relationships and containment

✅ **Syntax Parsing**
- Complete geometry syntax parsing
- Property extraction and application
- Error handling and edge cases

✅ **PNG Export**
- Coordinate transformation
- Canvas rendering (where display available)
- Auto-scaling functionality

✅ **Integration Workflows**
- Complete syntax → shapes → PNG pipeline
- Mathematical theorem verification
- Complex geometric constructions

## Test Markers

Tests are marked for selective execution:

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.gui` - Tests requiring display/GUI
- `@pytest.mark.slow` - Long-running tests

## Continuous Integration

### GitHub Actions (example)
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11]
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        pip install -e .[dev]
    - name: Run tests
      run: |
        python tests/run_tests.py --no-gui --coverage
```

### Tox Testing
```bash
# Test multiple Python versions
tox

# Run linting
tox -e lint

# Run type checking
tox -e type-check

# Generate coverage report
tox -e coverage
```

## Writing New Tests

### Test Structure
```python
import pytest
from shapix.core import Point
from shapix.shapes import Circle

class TestNewFeature:
    """Test new feature functionality"""
    
    def test_feature_creation(self):
        """Test basic feature creation"""
        # Arrange
        expected_value = 42
        
        # Act
        result = new_feature_function()
        
        # Assert
        assert result == expected_value
    
    def test_feature_edge_case(self):
        """Test edge case handling"""
        with pytest.raises(ValueError):
            invalid_feature_call()
```

### Using Fixtures
```python
def test_with_fixtures(sample_circle, temp_dir):
    """Test using predefined fixtures"""
    assert sample_circle.radius == 50
    
    output_file = os.path.join(temp_dir, "test.png")
    # Test file operations in temporary directory
```

## Test Data

Sample geometries are provided in `tests/fixtures/sample_geometries.py`:

- `SIMPLE_TRIANGLE` - Basic triangle
- `COMPLEX_CONSTRUCTION` - Advanced geometric construction
- `PYTHAGOREAN_DEMO` - Educational example
- And many more...

## Debugging Tests

### Verbose Output
```bash
pytest -v --tb=long
```

### Print Debugging
```bash
pytest -s  # Don't capture stdout
```

### Debug Specific Test
```bash
pytest --pdb tests/unit/test_core.py::TestPoint::test_point_creation
```

## Performance Testing

Performance tests verify:
- Large geometry parsing (400+ shapes)
- Memory usage with repeated operations
- PNG export with complex geometries

## Known Issues

- PNG export tests may fail on headless systems (no display)
- GUI-related tests are automatically skipped when display unavailable
- Some mathematical precision tests may vary slightly on different platforms

## Contributing Tests

When adding new features:

1. Write unit tests for individual components
2. Add integration tests for complete workflows
3. Include edge cases and error conditions
4. Update fixtures if needed
5. Ensure tests pass on multiple Python versions

## Test Performance

Target performance metrics:
- Unit tests: < 0.1s each
- Integration tests: < 5s each
- Complete suite: < 30s
- Coverage: > 90%