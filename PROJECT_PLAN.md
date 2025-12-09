# CNF Grammar Analyzer - Project Plan

## Overview
This project analyzes Context-Free Grammars (CFGs) in Chomsky Normal Form (CNF), implements a naive membership testing algorithm, and estimates feasibility of the algorithm for given string lengths.

## Language Selection: **Python**

**Rationale:**
- Excellent string manipulation and parsing capabilities
- Built-in data structures (sets, dictionaries, lists) ideal for grammar representation
- Easy file I/O
- Good for rapid prototyping and testing
- Clear syntax for complex algorithms
- Can easily handle exponential algorithms (though limited by performance)

**Alternative considerations:**
- **C++**: Better performance but more verbose, harder to debug
- **Java**: More verbose, similar performance to Python
- **Haskell**: Good for parsing but steeper learning curve

## Project Structure

```
proj464/
├── README.md
├── grammar_parser.py      # Parse input file into grammar representation
├── cnf_checker.py         # Task 1: Verify CNF compliance
├── membership_tester.py   # Task 2: Naive brute force membership testing
├── feasibility_estimator.py  # Task 3: Estimate if algorithm completes in 1 min
├── main.py                # Main entry point / CLI interface
├── tests/                 # Test cases
│   ├── test_grammars/     # Sample grammar files
│   └── test_*.py          # Unit tests
└── examples/              # Example grammar files
```

## Data Structures Design

### Grammar Representation
```python
Grammar = {
    'start': 'S',                    # Start variable
    'variables': set(),              # Set of all variables (uppercase letters)
    'terminals': set(),              # Set of terminals (lowercase, digits, $)
    'rules': {                       # Dictionary mapping variable -> list of productions
        'S': [('1', 'B', '0'), ('1',)],  # S -> 1B0 | 1
        'B': [('1', 'B'), ('$',)]        # B -> 1B | ε
    }
}
```

### Production Representation
- Binary productions: `('A', 'B')` for A → BC
- Terminal productions: `('a',)` for A → a
- Epsilon productions: `('$',)` for A → ε

## Task 1: CNF Validation

### CNF Rules to Check:
1. **Rule Format Validation:**
   - Each production must be one of:
     - Two non-terminals: `A → BC` (where B, C are variables)
     - Single terminal: `A → a` (where a is a terminal, not $)
     - Epsilon: Only `S → ε` is allowed, and only if S doesn't appear on right side

2. **Epsilon Rule Validation:**
   - If `S → ε` exists:
     - S cannot appear on the right side of any production
   - No other variable can have epsilon production

3. **Variable/Terminal Validation:**
   - Variables: Only uppercase letters (A-Z, excluding S for start)
   - Terminals: Lowercase letters (a-z), digits (0-9), $ (epsilon only)
   - Start variable: Must be S

### Algorithm:
```
1. Parse grammar file
2. For each rule:
   a. Check format (must be 1 or 2 symbols on right side)
   b. If 1 symbol: must be terminal (not $) OR S → $
   c. If 2 symbols: both must be variables
   d. If S → $ exists, check S doesn't appear on right side
3. Return True if all checks pass, False otherwise
```

## Task 2: Naive Membership Testing

### Key Insight:
For CNF grammar, any derivation of string w of length n≥1 has exactly **2n-1 steps**.

### Algorithm (Brute Force):
```
function MEMBERSHIP_TEST(grammar, string):
    n = length(string)
    max_steps = 2*n - 1
    
    function DERIVE(start_var, steps_remaining, target_string):
        if steps_remaining == 0:
            return start_var == target_string
        
        if length(target_string) == 0:
            return can_derive_epsilon(start_var)
        
        if length(target_string) == 1:
            # Terminal production
            return check_terminal_rule(start_var, target_string[0])
        
        # Try all possible binary splits and rule applications
        for each rule A → BC:
            for split_point in [1..length(target_string)-1]:
                left_part = target_string[0:split_point]
                right_part = target_string[split_point:]
                if DERIVE(B, steps_remaining-1, left_part) and 
                   DERIVE(C, steps_remaining-1, right_part):
                    return True
        
        return False
    
    return DERIVE('S', max_steps, string)
```

### Optimization Considerations:
- Memoization/caching to avoid recomputing same subproblems
- Early termination when impossible
- However, keep it "naive" - don't use CYK algorithm

## Task 3: Feasibility Estimation

### Goal:
Determine if worst-case execution can complete within 1 minute.

### Approach:
1. **Estimate worst-case operations:**
   - For string length n, we have 2n-1 steps
   - At each step, we try all binary rules × all split points
   - Number of binary rules: `num_binary_rules`
   - Number of split points for string of length k: `k-1`
   
2. **Calculate worst-case complexity:**
   - At each recursive call, we branch:
     - Binary rules: `num_binary_rules`
     - Split points: `n-1` (worst case)
   - Total branches per level: `num_binary_rules × (n-1)`
   - Depth: `2n-1`
   - Worst case nodes: `(num_binary_rules × (n-1))^(2n-1)`
   
3. **Estimate execution time:**
   - Benchmark: Count operations per second (rough estimate)
   - Assume each recursive call takes ~1 microsecond (conservative)
   - Calculate: `worst_case_nodes / operations_per_second < 60 seconds`
   
4. **Heuristic:**
   - For practical purposes, limit based on:
     - String length n
     - Number of binary rules
     - Set conservative threshold (e.g., if n > 10 and binary_rules > 5, likely infeasible)

### Algorithm:
```
function IS_FEASIBLE(grammar, string_length):
    n = string_length
    num_binary_rules = count_binary_rules(grammar)
    
    if n == 0:
        # Epsilon check - very fast
        return True
    
    # Rough estimate: worst case exponential growth
    # Conservative threshold
    if n > 15:
        return False
    
    # More sophisticated: estimate operations
    max_operations = estimate_worst_case_operations(n, num_binary_rules)
    estimated_seconds = max_operations / ESTIMATED_OPS_PER_SECOND
    
    return estimated_seconds <= 60
```

## Implementation Phases

### Phase 1: Core Infrastructure
1. Grammar parser (file → data structure)
2. Basic validation (syntax checking)
3. Test with provided example

### Phase 2: CNF Checker
1. Implement all CNF validation rules
2. Test with valid/invalid CNF grammars
3. Edge case handling

### Phase 3: Membership Tester
1. Implement naive brute force algorithm
2. Handle epsilon cases
3. Test with small examples
4. Add memoization (optional optimization)

### Phase 4: Feasibility Estimator
1. Implement operation counting
2. Benchmark performance
3. Set thresholds
4. Test estimation accuracy

### Phase 5: Integration & CLI
1. Create main entry point
2. Command-line interface:
   - `python main.py check_cnf <grammar_file>`
   - `python main.py test_membership <grammar_file> <string>`
   - `python main.py estimate <grammar_file> <string_length>`
3. Error handling
4. User-friendly output

### Phase 6: Testing & Documentation
1. Create comprehensive test suite
2. Test edge cases
3. Document code
4. Create README with usage examples

## Edge Cases to Handle

1. **Empty string (ε):**
   - Check if S → $ exists
   - Handle separately from normal membership test

2. **Invalid input:**
   - Malformed file format
   - Invalid characters
   - Missing start variable
   - Duplicate rules

3. **Grammar with no binary rules:**
   - Only terminal productions
   - Membership test becomes trivial

4. **Grammar with many rules:**
   - Performance considerations
   - Feasibility estimation accuracy

5. **Very short strings:**
   - Length 0 (epsilon)
   - Length 1 (single terminal)

## Testing Strategy

### Unit Tests:
- Grammar parser: various file formats
- CNF checker: valid/invalid grammars
- Membership tester: known examples
- Feasibility estimator: various scenarios

### Integration Tests:
- End-to-end workflows
- Example from assignment description

### Test Grammars:
- Simple CNF grammar (provided example)
- Invalid CNF grammars
- Edge cases (epsilon, single terminal, etc.)

## Performance Considerations

- **Naive algorithm is intentionally exponential** - don't optimize too much
- Use memoization to avoid redundant computations (still naive, just smarter)
- Set reasonable limits for feasibility estimation
- Provide clear warnings when algorithm may be slow

## Deliverables

1. Working program(s) that handle all 3 tasks
2. Clear command-line interface
3. README with usage instructions
4. Test suite with example grammars
5. Code comments explaining algorithm choices

