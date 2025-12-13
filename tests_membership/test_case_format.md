# Membership Test Case Format

Each test case consists of:
1. A grammar file (`.txt`) - must be valid CNF
2. A test specification file (`.test`) - contains strings to test and expected results

## Test Specification Format

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
a|YES
```

## Test Case Naming

- Grammar files: `grammar_<name>.txt`
- Test files: `grammar_<name>.test`

Example:
- `grammar_simple.txt` (grammar file)
- `grammar_simple.test` (test cases)

