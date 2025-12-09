# CNF Grammar Analyzer

A Python program for analyzing Context-Free Grammars (CFGs) in Chomsky Normal Form (CNF). This project implements three main functionalities:

1. **CNF Validation**: Check if a grammar is in Chomsky Normal Form
2. **Membership Testing**: Determine if a string belongs to a CNF grammar using a naive brute force algorithm
3. **Feasibility Estimation**: Estimate whether the naive algorithm can complete within 1 minute for a given string length

## File Format

Grammar files follow this format:
- First line: number `n` (number of rules)
- Next `n` lines: rules in format `VAR=production1|production2|...`

**Symbols:**
- **Variables**: Uppercase letters (A-Z), with `S` reserved for the start variable
- **Terminals**: Lowercase letters (a-z), digits (0-9), and `$` (represents epsilon/empty string)
- **Right arrow**: `=` (replaces →)
- **Separator**: `|` (separates alternative productions)

**Example:**
```
3
S=1B0|1
B=1B
B=$
```

## Chomsky Normal Form (CNF) Requirements

A grammar is in CNF if all productions are in one of these forms:
1. `A → BC` (two non-terminals)
2. `A → a` (single terminal, not epsilon)
3. `S → ε` (only start variable `S` can derive epsilon)

**Additional constraint**: If `S → ε` exists, `S` cannot appear on the right side of any production.

## Installation

No external dependencies required. Uses only Python standard library.

**Requirements**: Python 3.6+

## Usage

### Command 1: Check CNF

Check if a grammar is in Chomsky Normal Form:

```bash
python3 main.py check_cnf <grammar_file>
```

**Example:**
```bash
python3 main.py check_cnf examples/simple_cnf.txt
```

**Output:**
- `YES` if grammar is in CNF
- `NO` if grammar is not in CNF (with explanation)

### Command 2: Test Membership

Test if a string belongs to a CNF grammar:

```bash
python3 main.py test_membership <grammar_file> <string>
```

**Special cases:**
- Use `epsilon` or `ε` to test for empty string membership

**Example:**
```bash
python3 main.py test_membership examples/simple_cnf.txt ab
python3 main.py test_membership examples/valid_cnf1.txt epsilon
```

**Output:**
- `YES` if string belongs to grammar
- `NO` if string does not belong to grammar

**Note**: The grammar must be in CNF. The program will check this first and report an error if not.

### Command 3: Estimate Feasibility

Estimate whether the naive algorithm can complete within 1 minute for a given string length:

```bash
python3 main.py estimate <grammar_file> <string_length>
```

**Example:**
```bash
python3 main.py estimate examples/simple_cnf.txt 10
```

**Output:**
- `YES` if estimated to complete within 1 minute
- `NO` if estimated to exceed 1 minute (with explanation)

## Algorithm Details

### Membership Testing Algorithm

The naive brute force algorithm uses the key property of CNF grammars:
- For a string of length `n ≥ 1`, any derivation has exactly `2n - 1` steps

The algorithm:
1. Enumerates all possible derivations up to the `2n - 1` step limit
2. Tries all binary rule applications and string splits
3. Uses memoization to avoid redundant computations
4. Has exponential worst-case time complexity

**Time Complexity**: O((num_binary_rules × n)^(2n-1)) in worst case

### Feasibility Estimation

The feasibility estimator:
1. Counts binary rules in the grammar
2. Estimates worst-case operations based on string length
3. Uses conservative benchmarks to estimate execution time
4. Returns feasibility based on 60-second threshold

## Example Grammars

### Valid CNF Grammar (`examples/simple_cnf.txt`)
```
3
S=AB
A=a
B=b
```
- Generates: `ab`
- CNF: ✓ Valid

### Valid CNF with Epsilon (`examples/valid_cnf1.txt`)
```
4
S=AB|a
A=a
B=b
S=$
```
- Generates: `ab`, `a`, `ε` (empty string)
- CNF: ✓ Valid

### Invalid CNF (`examples/invalid_cnf1.txt`)
```
2
S=ABC
A=a
```
- CNF: ✗ Invalid (production has 3 symbols)

### Invalid CNF (`examples/invalid_cnf2.txt`)
```
2
A=$
A=a
```
- CNF: ✗ Invalid (epsilon production not allowed for non-start variable)

## Project Structure

```
proj464/
├── README.md                  # This file
├── PROJECT_PLAN.md            # Detailed implementation plan
├── main.py                    # Main CLI interface
├── grammar_parser.py          # Grammar file parser
├── cnf_checker.py             # CNF validation module
├── membership_tester.py       # Naive membership testing algorithm
├── feasibility_estimator.py   # Feasibility estimation module
└── examples/                  # Example grammar files
    ├── example1.txt           # Example from assignment (not CNF)
    ├── simple_cnf.txt         # Simple valid CNF grammar
    ├── valid_cnf1.txt         # Valid CNF with epsilon
    ├── invalid_cnf1.txt       # Invalid CNF examples
    └── invalid_cnf2.txt
```

## Testing

Test the implementation with provided examples:

```bash
# Test CNF checking
python3 main.py check_cnf examples/simple_cnf.txt
python3 main.py check_cnf examples/invalid_cnf1.txt

# Test membership
python3 main.py test_membership examples/simple_cnf.txt ab
python3 main.py test_membership examples/simple_cnf.txt aa

# Test feasibility
python3 main.py estimate examples/simple_cnf.txt 5
python3 main.py estimate examples/simple_cnf.txt 20
```

## Limitations

1. **Exponential Complexity**: The naive membership algorithm has exponential worst-case time complexity. It becomes impractical for:
   - Long strings (typically > 15 characters)
   - Grammars with many binary rules (> 10 rules)

2. **Feasibility Estimation**: The feasibility estimator uses conservative heuristics and may not be perfectly accurate for all cases.

3. **Grammar Format**: The parser expects strict adherence to the specified file format.

## Notes

- The membership tester requires the grammar to be in CNF. It will verify this before testing.
- The algorithm is intentionally naive (brute force) as specified in the requirements.
- Memoization is used to improve performance while maintaining the naive approach.
- Epsilon (empty string) is represented as `$` in grammar files and can be tested using `epsilon` or `ε` as the string argument.

## Author

Implementation for CNF Grammar Analysis project.

# cmpsc464proj
