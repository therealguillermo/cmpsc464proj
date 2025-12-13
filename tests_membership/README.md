# Membership Test Suite

This directory contains comprehensive test cases for membership testing functionality.

## Structure

- **Grammar files** (`.txt`): CNF grammar definitions
- **Test files** (`.test`): Test cases with expected results
- **`verify_test_cases.py`**: Script to verify test case accuracy
- **`run_tests.py`**: Script to run all membership tests

## Test Case Format

Each `.test` file contains lines in format:
```
<string>|<expected_result>
```

Where:
- `<string>`: The string to test (use `epsilon` or `ε` for empty string)
- `<expected_result>`: Either `YES` or `NO`

Example:
```
ab|YES
aa|NO
epsilon|YES
```

## Test Cases Included

1. **grammar_simple.txt**: Basic binary grammar (S -> AB, A -> a, B -> b)
2. **grammar_with_epsilon.txt**: Grammar with epsilon production
3. **grammar_single_terminal.txt**: Single terminal grammar
4. **grammar_only_epsilon.txt**: Grammar that only generates epsilon
5. **grammar_multiple_options.txt**: Grammar with multiple production options
6. **grammar_chain.txt**: Chained binary productions
7. **grammar_digits.txt**: Grammar using digits as terminals
8. **grammar_complex.txt**: Complex grammar with multiple variables
9. **grammar_long_chain.txt**: Long chain of binary productions
10. **grammar_epsilon_with_options.txt**: Epsilon combined with other options
11. **grammar_single_char_binary.txt**: Binary rule producing same character twice
12. **grammar_repeated.txt**: Grammar with recursive structure (S -> SS)
13. **grammar_three_level.txt**: Three-level binary derivation chain

## Usage

### Verify Test Cases (Check Accuracy)
```bash
python3 tests_membership/verify_test_cases.py
```

This verifies that all test cases are correctly specified by running them
and checking results match expectations.

### Run Test Suite
```bash
python3 tests_membership/run_tests.py
```

This runs all membership tests and reports which pass/fail.

## Verification Status

All test cases have been verified to be 100% accurate. Each test case has been
manually checked to ensure:
- Grammar is valid CNF
- Expected results match actual derivations
- Edge cases are properly covered

