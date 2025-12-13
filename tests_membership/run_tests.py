#!/usr/bin/env python3
"""
Run Membership Test Suite

Automatically runs all membership test cases and reports results.
"""

import os
import sys

# Add parent directory to path to import AIO
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import AIO


class TestResult:
    """Represents a single test result"""
    def __init__(self, grammar_file: str, test_string: str, expected: bool, actual: bool):
        self.grammar_file = grammar_file
        self.test_string = test_string
        self.expected = expected
        self.actual = actual
        self.passed = (expected == actual)


def run_membership_tests() -> tuple[list[TestResult], int, int]:
    """
    Run all membership test cases.
    
    Returns:
        (results, passed_count, failed_count)
    """
    test_dir = os.path.dirname(__file__)
    grammar_files = sorted([f for f in os.listdir(test_dir) if f.endswith('.txt')])
    
    all_results = []
    total_passed = 0
    total_failed = 0
    
    print("=" * 80)
    print("MEMBERSHIP TEST SUITE")
    print("=" * 80)
    
    for grammar_file in grammar_files:
        base_name = grammar_file.replace('.txt', '')
        test_file = f"{base_name}.test"
        test_path = os.path.join(test_dir, test_file)
        
        if not os.path.exists(test_path):
            print(f"\n⚠ Skipping {grammar_file}: No test file found")
            continue
        
        grammar_path = os.path.join(test_dir, grammar_file)
        
        # Parse grammar
        try:
            grammar = AIO.parse_grammar_file(grammar_path)
        except Exception as e:
            print(f"\n✗ {grammar_file}: Error parsing grammar: {e}")
            total_failed += 1
            continue
        
        # Verify CNF
        is_cnf, msg = AIO.is_cnf(grammar)
        if not is_cnf:
            print(f"\n✗ {grammar_file}: Grammar is not CNF: {msg}")
            total_failed += 1
            continue
        
        # Read test cases
        print(f"\nTesting: {grammar_file}")
        print("-" * 80)
        
        with open(test_path, 'r') as f:
            test_lines = [line.strip() for line in f.readlines() if line.strip()]
        
        grammar_passed = 0
        grammar_failed = 0
        
        for line in test_lines:
            if '|' not in line:
                print(f"  ⚠ Invalid test line: {line}")
                continue
            
            test_string, expected_str = line.split('|', 1)
            expected = expected_str.strip() == 'YES'
            
            # Handle epsilon
            actual_string = '' if test_string.strip() in ['epsilon', 'ε'] else test_string.strip()
            
            # Test membership
            try:
                result = AIO.test_membership(grammar, actual_string)
            except Exception as e:
                print(f"  ✗ '{test_string}': ERROR - {e}")
                grammar_failed += 1
                all_results.append(TestResult(grammar_file, test_string, expected, False))
                continue
            
            # Check result
            test_result = TestResult(grammar_file, test_string, expected, result)
            all_results.append(test_result)
            
            if test_result.passed:
                print(f"  ✓ '{test_string}': Expected {expected_str}, got {'YES' if result else 'NO'}")
                grammar_passed += 1
            else:
                print(f"  ✗ '{test_string}': Expected {expected_str}, got {'YES' if result else 'NO'}")
                grammar_failed += 1
        
        print(f"  Summary: {grammar_passed} passed, {grammar_failed} failed")
        total_passed += grammar_passed
        total_failed += grammar_failed
    
    return all_results, total_passed, total_failed


def main():
    """Main entry point"""
    results, passed, failed = run_membership_tests()
    
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    total = passed + failed
    print(f"Total tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    if total > 0:
        print(f"Success rate: {100 * passed / total:.1f}%")
    print("=" * 80)
    
    # Show failed tests
    failed_tests = [r for r in results if not r.passed]
    if failed_tests:
        print("\nFAILED TESTS:")
        print("-" * 80)
        for result in failed_tests:
            print(f"  {result.grammar_file}: '{result.test_string}'")
            print(f"    Expected: {'YES' if result.expected else 'NO'}")
            print(f"    Got: {'YES' if result.actual else 'NO'}")
    
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())

