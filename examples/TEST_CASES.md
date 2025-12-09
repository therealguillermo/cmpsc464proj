# Comprehensive Test Cases for CNF Grammar Analyzer

This document describes all test cases created to verify CNF validation covers every possible scenario.

## Test Organization

- **`valid/`**: Contains 24 grammars that are valid CNF (should return YES)
- **`invalid/`**: Contains 35 grammars that are invalid CNF (should return NO)

## Valid CNF Test Cases

### Basic Structures
1. **01_simple_binary.txt**: Simple binary rule (S -> AB)
2. **02_simple_terminal.txt**: Simple terminal rule (S -> a)
3. **03_mixed_binary_terminal.txt**: Mix of binary and terminal rules
4. **11_single_binary_rule.txt**: Grammar with only one binary rule

### Epsilon Handling
5. **04_with_epsilon.txt**: Valid epsilon for start variable S
6. **06_only_epsilon.txt**: Grammar that only generates epsilon
7. **13_epsilon_with_binary.txt**: Epsilon combined with binary rules
8. **14_epsilon_only_option.txt**: Epsilon as one option among others
9. **16_complex_with_epsilon.txt**: Complex grammar with epsilon
10. **19_epsilon_with_many_rules.txt**: Many rules including epsilon

### Multiple Rules
11. **05_multiple_rules_per_var.txt**: Variables with multiple production options
12. **20_maximal_valid.txt**: Maximum complexity valid grammar

### Terminal Types
13. **08_digits_as_terminals.txt**: Using digits as terminals
14. **09_mixed_digits_letters.txt**: Mix of digits and letters as terminals
15. **17_all_digits.txt**: All terminals are digits

### Complex Structures
16. **07_complex_grammar.txt**: Multiple variables and rules
17. **10_chain_binary.txt**: Chain of binary productions
18. **12_all_variables.txt**: Uses all uppercase letters A-Z
19. **15_large_alphabet.txt**: Large number of rules
20. **18_minimal_grammar.txt**: Minimal valid grammar

### S on Right Side (Valid Cases)
21. **21_s_on_right_no_epsilon.txt**: S on right side when S -> ε doesn't exist (VALID)
22. **22_single_terminal.txt**: Single terminal production (S -> s)
23. **23_s_in_second_no_epsilon.txt**: S in second position, no epsilon
24. **24_s_in_both_no_epsilon.txt**: S in both positions, no epsilon

**Note**: S can appear on the right side ONLY if S -> ε does NOT exist.

## Invalid CNF Test Cases

### Too Many Symbols
1. **01_three_symbols.txt**: Production with 3 symbols (S -> ABC)
2. **02_four_symbols.txt**: Production with 4 symbols (S -> ABCD)
3. **13_long_production.txt**: Very long production (11+ symbols)

### Invalid Epsilon Usage
4. **03_epsilon_non_start.txt**: Epsilon for non-start variable (A -> ε)
5. **11_multiple_epsilon.txt**: Multiple variables with epsilon
6. **19_dollar_as_terminal.txt**: $ used as terminal (not epsilon for S)

### Epsilon + S on Right Side (Invalid)
7. **06_s_on_right_with_epsilon.txt**: S -> ε exists AND S on right side
8. **07_s_on_right_with_epsilon.txt**: S -> ε exists AND S on right side (AS)
9. **25_s_epsilon_but_s_in_production.txt**: S -> ε exists AND S in production
10. **26_s_in_second_with_epsilon.txt**: S -> ε exists AND S in second position
11. **27_s_in_both_with_epsilon.txt**: S -> ε exists AND S in both positions
12. **35_s_epsilon_with_s_chain.txt**: S -> ε exists AND S in chain
13. **36_s_epsilon_with_s_indirect.txt**: S -> ε exists AND S indirectly

### Invalid Production Formats
14. **04_single_variable_production.txt**: Single variable production (S -> A)
15. **08_terminal_and_variable_mixed.txt**: Terminal + variable (S -> aB)
16. **14_binary_with_terminal_mix.txt**: Binary + terminal mix (S -> ABa)
17. **15_terminal_binary_mix.txt**: Terminal + binary mix (S -> aBC)
18. **18_epsilon_in_binary.txt**: Epsilon in binary production (S -> A$)
19. **23_terminal_after_binary.txt**: Terminal after binary (S -> ABc)
20. **24_terminal_before_binary.txt**: Terminal before binary (S -> aBC)
21. **32_terminal_in_middle.txt**: Terminal in middle (S -> AaB)

### Invalid Characters
22. **09_lowercase_variable.txt**: Lowercase used as variable
23. **10_uppercase_terminal.txt**: Uppercase used as terminal (S -> A, A -> B)
24. **16_single_lowercase_variable.txt**: Single lowercase (should be terminal)
25. **17_binary_with_digit_variable.txt**: Digit in variable position (S -> A1)
26. **20_special_char.txt**: Special character (@) in production
27. **29_invalid_char.txt**: Invalid character (!) in production
28. **30_multi_char_variable.txt**: Multi-character variable (AB)
29. **31_multi_char_terminal.txt**: Multi-character terminal (ab)
30. **33_only_terminals_binary.txt**: Only terminals in binary (S -> ab)
31. **34_only_digits_binary.txt**: Only digits in binary (S -> 12)

### Structural Issues
32. **05_start_not_s.txt**: Start variable is not S
33. **12_empty_production.txt**: Empty production (S -> )
34. **21_missing_start.txt**: No start variable S defined
35. **22_space_in_production.txt**: Space in production (S -> A B)
36. **28_no_productions.txt**: No productions for variable

## Key CNF Rules Tested

### ✅ Valid CNF Rules:
1. **A -> BC**: Two non-terminals ✓
2. **A -> a**: Single terminal ✓
3. **S -> ε**: Only start variable can have epsilon ✓
4. **S on right side**: Allowed ONLY if S -> ε does NOT exist ✓

### ❌ Invalid CNF Rules:
1. **A -> BCD**: More than 2 symbols ✗
2. **A -> B**: Single variable (not terminal) ✗
3. **A -> ε**: Epsilon for non-start variable ✗
4. **S -> ε AND S on right**: Both conditions together ✗
5. **A -> aB**: Mixed terminal and variable ✗
6. **Invalid characters**: Special chars, wrong case ✗

## Running Tests

Use the test script to verify all cases:

```bash
python3 test_all_examples.py
```

This will test all 59 grammar files and report which ones pass/fail.

## Coverage Summary

- **Total test cases**: 59
- **Valid CNF**: 24 cases
- **Invalid CNF**: 35 cases
- **Coverage areas**:
  - Basic CNF structures ✓
  - Epsilon handling ✓
  - S on right side constraint ✓
  - Invalid production formats ✓
  - Character validation ✓
  - Edge cases ✓

All test cases are designed to ensure 100% coverage of CNF validation requirements.

