# Tests

This directory contains all test files for the DyGETViz package.

## Running Tests

### Run All Tests

```bash
# From the project root
python tests/run_tests.py

# Or using unittest directly
python -m unittest discover tests/
```

### Run Specific Test

```bash
# Run a specific test file
python tests/run_tests.py test_data.py

# Or run directly
python tests/test_data.py
```

### Test Files

- `test_cli.py` - Command line interface tests
- `test_data.py` - Data loading and processing tests
- `test_imports.py` - Import functionality tests
- `test_models.py` - Model implementation tests
- `test_plotly_compatibility.py` - Plotly compatibility tests
- `test_html_replacement.py` - HTML component tests
- `test_mantine_provider.py` - Mantine component tests
- `simple_test.py` - Basic functionality tests
- `fix_plotly_compatibility.py` - Plotly compatibility fixes

## Test Coverage

The tests cover:
- Data loading and processing
- Model implementations
- CLI functionality
- Visualization components
- Import dependencies
- Plotly compatibility issues

## Adding New Tests

1. Create a new test file with the prefix `test_`
2. Use unittest.TestCase as the base class
3. Follow the naming convention: `test_<functionality>.py`
4. Add the test file to this directory 