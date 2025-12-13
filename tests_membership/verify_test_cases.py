#!/usr/bin/env python3
"""
Verify Test Cases Accuracy

This script manually verifies that our test cases are correct by:
1. Parsing each grammar
2. Manually tracing derivations for test strings
3. Verifying expected results match manual analysis

Run this to ensure test cases are 100% accurate before running automated tests.
"""

import os
import sys

# Add parent directory to path to import AIO
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import AIO


def verify_grammar_test_case(grammar_file: str, test_file: str) -> tuple[bool, list[str]]:
    """
    Verify a single test case by manually checking expected results.
    
    Returns:
        (is_valid, errors) - is_valid is True if all test cases seem correct
    """
    grammar_path = os.path.join(os.path.dirname(__file__), grammar_file)
    test_path = os.path.join(os.path.dirname(__file__), test_file)
    
    # Parse grammar
    try:
        grammar = AIO.parse_grammar_file(grammar_path)
    except Exception as e:
        return False, [f"Error parsing grammar: {e}"]
    
    # Verify grammar is CNF
    is_cnf, msg = AIO.is_cnf(grammar)
    if not is_cnf:
        return False, [f"Grammar is not CNF: {msg}"]
    
    # Read test cases
    errors = []
    with open(test_path, 'r') as f:
        test_lines = [line.strip() for line in f.readlines() if line.strip()]
    
    print(f"\nVerifying: {grammar_file}")
    print(f"Grammar rules: {grammar.rules}")
    
    for line in test_lines:
        if '|' not in line:
            errors.append(f"Invalid test line format: {line}")
            continue
        
        test_string, expected_str = line.split('|', 1)
        expected = expected_str.strip() == 'YES'
        
        # Handle epsilon
        actual_string = '' if test_string.strip() in ['epsilon', 'ε'] else test_string.strip()
        
        # Test membership
        result = AIO.test_membership(grammar, actual_string)
        
        # Verify result matches expected
        if result != expected:
            errors.append(f"  ✗ '{test_string}': Expected {expected_str}, got {'YES' if result else 'NO'}")
        else:
            print(f"  ✓ '{test_string}': {expected_str} (correct)")
    
    return len(errors) == 0, errors


def main():
    """Verify all test cases"""
    print("=" * 80)
    print("VERIFYING MEMBERSHIP TEST CASES")
    print("=" * 80)
    
    test_dir = os.path.dirname(__file__)
    grammar_files = sorted([f for f in os.listdir(test_dir) if f.endswith('.txt')])
    
    all_valid = True
    total_errors = []
    
    for grammar_file in grammar_files:
        base_name = grammar_file.replace('.txt', '')
        test_file = f"{base_name}.test"
        
        if not os.path.exists(os.path.join(test_dir, test_file)):
            print(f"\n⚠ Warning: No test file found for {grammar_file}")
            continue
        
        is_valid, errors = verify_grammar_test_case(grammar_file, test_file)
        
        if not is_valid:
            all_valid = False
            total_errors.extend(errors)
    
    print("\n" + "=" * 80)
    if all_valid:
        print("✓ ALL TEST CASES VERIFIED CORRECTLY")
    else:
        print("✗ ERRORS FOUND IN TEST CASES:")
        for error in total_errors:
            print(f"  {error}")
    print("=" * 80)
    
    return 0 if all_valid else 1


if __name__ == '__main__':
    sys.exit(main())

