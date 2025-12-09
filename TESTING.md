# Testing Documentation

This document describes the comprehensive test suite for the CNF Grammar Analyzer.

## Test Files Overview

### Test Suites

1. **`test_all_examples.py`** - Basic CNF validation test
   - Tests all grammar files in `examples/valid/` and `examples/invalid/`
   - Verifies CNF validation works correctly
   - Quick validation check

2. **`test_pipeline.py`** - Comprehensive test pipeline
   - Tests all three functionalities: CNF validation, membership testing, feasibility estimation
   - Tests CLI interface
   - Provides detailed failure reports
   - **Recommended for full testing**

## Running Tests

### Quick Test (CNF Validation Only)
```bash
python3 test_all_examples.py
```

### Comprehensive Test (All Functionalities)
```bash
python3 test_pipeline.py
```

## Test Coverage

### Test 1: CNF Validation
- **24 valid CNF grammars** - All should return YES
- **36 invalid CNF grammars** - All should return NO
- **Total: 60 test cases**

### Test 2: Membership Testing
- Tests membership algorithm on various grammars
- Tests valid strings, invalid strings, epsilon cases
- **Total: 12 test cases**

### Test 3: Feasibility Estimation
- Tests feasibility estimator for various string lengths
- Tests edge cases (epsilon, short strings, long strings)
- **Total: 6 test cases**

### Test 4: CLI Interface
- Tests all three CLI commands
- Verifies correct output format
- **Total: 5 test cases**

**Grand Total: 83 test cases**

## Test Results

All tests should pass with 100% success rate:
```
Total tests: 83
Passed: 83
Failed: 0
Success rate: 100.0%
```

## Test File Organization

### Valid CNF Grammars (`examples/valid/`)
24 files testing various valid CNF structures:
- Basic structures (binary, terminal, mixed)
- Epsilon handling
- Multiple rules per variable
- Different terminal types (letters, digits)
- Complex grammars
- S on right side (when no epsilon)

### Invalid CNF Grammars (`examples/invalid/`)
36 files testing various invalid CNF cases:
- Too many symbols in production
- Invalid epsilon usage
- Epsilon + S on right side conflict
- Invalid production formats
- Invalid characters
- Structural issues

## Expected Behavior

### CNF Validation
- Valid grammars: Should return `YES` with confirmation message
- Invalid grammars: Should return `NO` with error explanation

### Membership Testing
- Valid strings: Should return `YES`
- Invalid strings: Should return `NO`
- Epsilon: Use `epsilon` or `ε` as string argument

### Feasibility Estimation
- Short strings (≤5): Usually `FEASIBLE`
- Medium strings (6-15): May be `FEASIBLE` or `INFEASIBLE` depending on grammar
- Long strings (>15): Usually `INFEASIBLE`
- Epsilon (length 0): Always `FEASIBLE`

## Troubleshooting

### If tests fail:

1. **Check grammar file format**
   - First line must be number of rules
   - Rules must be in format `VAR=prod1|prod2|...`
   - No extra blank lines

2. **Verify file paths**
   - Test scripts assume they're run from project root
   - Grammar files should be in `examples/valid/` or `examples/invalid/`

3. **Check Python version**
   - Requires Python 3.6+
   - Run `python3 --version` to verify

4. **Review error messages**
   - Test pipeline provides detailed failure reports
   - Check expected vs actual output

## Continuous Integration

The test pipeline can be integrated into CI/CD:
```bash
python3 test_pipeline.py
exit_code=$?
if [ $exit_code -ne 0 ]; then
    echo "Tests failed!"
    exit 1
fi
```

## Adding New Tests

To add new test cases:

1. **CNF Validation**: Add grammar files to `examples/valid/` or `examples/invalid/`
2. **Membership Testing**: Add test cases to `test_pipeline.py` in `test_membership()` method
3. **Feasibility**: Add test cases to `test_pipeline.py` in `test_feasibility()` method
4. **CLI**: Add commands to `test_pipeline.py` in `test_cli_interface()` method

Run tests after adding new cases to ensure they pass.

