#!/usr/bin/env python3
"""
Comprehensive Test Pipeline for CNF Grammar Analyzer

Tests all three functionalities:
1. CNF validation
2. Membership testing  
3. Feasibility estimation

Verifies expected outputs match actual outputs.
"""

import os
import sys
import subprocess
from typing import List, Tuple, Dict
from cnf_checker import check_cnf_file
from grammar_parser import parse_grammar_file
from membership_tester import test_membership
from feasibility_estimator import is_feasible


class TestResult:
    """Represents a test result"""
    def __init__(self, name: str, passed: bool, expected: str, actual: str, error: str = ""):
        self.name = name
        self.passed = passed
        self.expected = expected
        self.actual = actual
        self.error = error


class TestPipeline:
    """Comprehensive test pipeline"""
    
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.valid_dir = os.path.join(self.base_dir, 'examples', 'valid')
        self.invalid_dir = os.path.join(self.base_dir, 'examples', 'invalid')
        self.results: List[TestResult] = []
    
    def test_cnf_validation(self) -> Tuple[int, int]:
        """Test CNF validation on all example files"""
        print("\n" + "=" * 80)
        print("TEST 1: CNF VALIDATION")
        print("=" * 80)
        
        valid_files = sorted([f for f in os.listdir(self.valid_dir) if f.endswith('.txt')])
        invalid_files = sorted([f for f in os.listdir(self.invalid_dir) if f.endswith('.txt')])
        
        passed = 0
        failed = 0
        
        # Test valid grammars (should return YES)
        print(f"\nTesting {len(valid_files)} VALID CNF grammars (should return YES):")
        print("-" * 80)
        for filename in valid_files:
            filepath = os.path.join(self.valid_dir, filename)
            is_cnf, message = check_cnf_file(filepath)
            
            if is_cnf:
                print(f"✓ {filename:45s} - YES")
                passed += 1
                self.results.append(TestResult(
                    f"CNF_VALID_{filename}", True, "YES", "YES"
                ))
            else:
                print(f"✗ {filename:45s} - NO  (ERROR: {message[:40]})")
                failed += 1
                self.results.append(TestResult(
                    f"CNF_VALID_{filename}", False, "YES", "NO", message
                ))
        
        # Test invalid grammars (should return NO)
        print(f"\nTesting {len(invalid_files)} INVALID CNF grammars (should return NO):")
        print("-" * 80)
        for filename in invalid_files:
            filepath = os.path.join(self.invalid_dir, filename)
            is_cnf, message = check_cnf_file(filepath)
            
            if not is_cnf:
                print(f"✓ {filename:45s} - NO  ({message[:45]})")
                passed += 1
                self.results.append(TestResult(
                    f"CNF_INVALID_{filename}", True, "NO", "NO"
                ))
            else:
                print(f"✗ {filename:45s} - YES (ERROR: Should be invalid!)")
                failed += 1
                self.results.append(TestResult(
                    f"CNF_INVALID_{filename}", False, "NO", "YES", "Should be invalid CNF"
                ))
        
        return passed, failed
    
    def test_membership(self) -> Tuple[int, int]:
        """Test membership testing on valid CNF grammars"""
        print("\n" + "=" * 80)
        print("TEST 2: MEMBERSHIP TESTING")
        print("=" * 80)
        
        # Test cases: (grammar_file, test_string, expected_result, description)
        test_cases = [
            # Simple grammar: S -> AB, A -> a, B -> b
            ("simple_cnf.txt", "ab", True, "Simple binary derivation"),
            ("simple_cnf.txt", "aa", False, "Invalid string"),
            ("simple_cnf.txt", "a", False, "Incomplete string"),
            ("simple_cnf.txt", "b", False, "Incomplete string"),
            ("simple_cnf.txt", "", False, "Empty string (no epsilon)"),
            
            # Grammar with epsilon: S -> AB | $, A -> a, B -> b
            ("valid_cnf1.txt", "ab", True, "Binary derivation"),
            ("valid_cnf1.txt", "a", True, "Terminal derivation"),
            ("valid_cnf1.txt", "epsilon", True, "Epsilon derivation"),
            ("valid_cnf1.txt", "aa", False, "Invalid string"),
            
            # Simple terminal: S -> a
            ("02_simple_terminal.txt", "a", True, "Single terminal"),
            ("02_simple_terminal.txt", "b", False, "Wrong terminal"),
            ("02_simple_terminal.txt", "", False, "Empty string"),
        ]
        
        passed = 0
        failed = 0
        
        print(f"\nTesting {len(test_cases)} membership test cases:")
        print("-" * 80)
        
        for grammar_file, test_string, expected, description in test_cases:
            # Find grammar file
            grammar_path = None
            if os.path.exists(os.path.join(self.base_dir, 'examples', grammar_file)):
                grammar_path = os.path.join(self.base_dir, 'examples', grammar_file)
            elif os.path.exists(os.path.join(self.valid_dir, grammar_file)):
                grammar_path = os.path.join(self.valid_dir, grammar_file)
            
            if not grammar_path:
                print(f"✗ {description:45s} - SKIPPED (grammar file not found: {grammar_file})")
                failed += 1
                continue
            
            try:
                grammar = parse_grammar_file(grammar_path)
                is_cnf, msg = check_cnf_file(grammar_path)
                
                if not is_cnf:
                    print(f"✗ {description:45s} - SKIPPED (grammar not CNF: {msg[:30]})")
                    failed += 1
                    continue
                
                # Handle epsilon string
                actual_string = "" if test_string == "epsilon" else test_string
                result = test_membership(grammar, actual_string)
                
                if result == expected:
                    print(f"✓ {description:45s} - {'YES' if result else 'NO'} (string: '{test_string}')")
                    passed += 1
                    self.results.append(TestResult(
                        f"MEMBERSHIP_{grammar_file}_{test_string}", True,
                        "YES" if expected else "NO", "YES" if result else "NO"
                    ))
                else:
                    print(f"✗ {description:45s} - Expected {'YES' if expected else 'NO'}, got {'YES' if result else 'NO'} (string: '{test_string}')")
                    failed += 1
                    self.results.append(TestResult(
                        f"MEMBERSHIP_{grammar_file}_{test_string}", False,
                        "YES" if expected else "NO", "YES" if result else "NO"
                    ))
            except Exception as e:
                print(f"✗ {description:45s} - ERROR: {str(e)[:50]}")
                failed += 1
                self.results.append(TestResult(
                    f"MEMBERSHIP_{grammar_file}_{test_string}", False,
                    "YES" if expected else "NO", "ERROR", str(e)
                ))
        
        return passed, failed
    
    def test_feasibility(self) -> Tuple[int, int]:
        """Test feasibility estimation"""
        print("\n" + "=" * 80)
        print("TEST 3: FEASIBILITY ESTIMATION")
        print("=" * 80)
        
        test_cases = [
            # (grammar_file, string_length, expected_feasible, description)
            ("simple_cnf.txt", 0, True, "Epsilon (length 0)"),
            ("simple_cnf.txt", 1, True, "Single character"),
            ("simple_cnf.txt", 5, True, "Short string"),
            ("simple_cnf.txt", 10, False, "Medium string (infeasible due to exponential)"),
            ("simple_cnf.txt", 20, False, "Long string (should be infeasible)"),
            ("02_simple_terminal.txt", 100, False, "Only terminals (length threshold)"),
        ]
        
        passed = 0
        failed = 0
        
        print(f"\nTesting {len(test_cases)} feasibility test cases:")
        print("-" * 80)
        
        for grammar_file, string_length, expected_feasible, description in test_cases:
            grammar_path = None
            if os.path.exists(os.path.join(self.base_dir, 'examples', grammar_file)):
                grammar_path = os.path.join(self.base_dir, 'examples', grammar_file)
            elif os.path.exists(os.path.join(self.valid_dir, grammar_file)):
                grammar_path = os.path.join(self.valid_dir, grammar_file)
            
            if not grammar_path:
                print(f"✗ {description:45s} - SKIPPED (grammar file not found)")
                failed += 1
                continue
            
            try:
                grammar = parse_grammar_file(grammar_path)
                is_cnf, msg = check_cnf_file(grammar_path)
                
                if not is_cnf:
                    print(f"✗ {description:45s} - SKIPPED (grammar not CNF)")
                    failed += 1
                    continue
                
                feasible, explanation = is_feasible(grammar, string_length)
                
                if feasible == expected_feasible:
                    print(f"✓ {description:45s} - {'FEASIBLE' if feasible else 'INFEASIBLE'} (length: {string_length})")
                    passed += 1
                    self.results.append(TestResult(
                        f"FEASIBILITY_{grammar_file}_{string_length}", True,
                        "FEASIBLE" if expected_feasible else "INFEASIBLE",
                        "FEASIBLE" if feasible else "INFEASIBLE"
                    ))
                else:
                    print(f"✗ {description:45s} - Expected {'FEASIBLE' if expected_feasible else 'INFEASIBLE'}, got {'FEASIBLE' if feasible else 'INFEASIBLE'}")
                    print(f"  Explanation: {explanation[:60]}")
                    failed += 1
                    self.results.append(TestResult(
                        f"FEASIBILITY_{grammar_file}_{string_length}", False,
                        "FEASIBLE" if expected_feasible else "INFEASIBLE",
                        "FEASIBLE" if feasible else "INFEASIBLE"
                    ))
            except Exception as e:
                print(f"✗ {description:45s} - ERROR: {str(e)[:50]}")
                failed += 1
                self.results.append(TestResult(
                    f"FEASIBILITY_{grammar_file}_{string_length}", False,
                    "FEASIBLE" if expected_feasible else "INFEASIBLE", "ERROR", str(e)
                ))
        
        return passed, failed
    
    def test_cli_interface(self) -> Tuple[int, int]:
        """Test CLI interface commands"""
        print("\n" + "=" * 80)
        print("TEST 4: CLI INTERFACE")
        print("=" * 80)
        
        test_cases = [
            # (command, expected_output_contains, description)
            (["python3", "main.py", "check_cnf", "examples/simple_cnf.txt"], "YES", "Check CNF command"),
            (["python3", "main.py", "check_cnf", "examples/invalid_cnf1.txt"], "NO", "Check invalid CNF"),
            (["python3", "main.py", "test_membership", "examples/simple_cnf.txt", "ab"], "YES", "Test membership YES"),
            (["python3", "main.py", "test_membership", "examples/simple_cnf.txt", "aa"], "NO", "Test membership NO"),
            (["python3", "main.py", "estimate", "examples/simple_cnf.txt", "5"], "YES", "Estimate feasibility"),
        ]
        
        passed = 0
        failed = 0
        
        print(f"\nTesting {len(test_cases)} CLI commands:")
        print("-" * 80)
        
        for cmd, expected_contains, description in test_cases:
            try:
                result = subprocess.run(
                    cmd,
                    cwd=self.base_dir,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                output = result.stdout + result.stderr
                
                if expected_contains in output and result.returncode in [0, 1]:
                    print(f"✓ {description:45s} - Command executed successfully")
                    passed += 1
                    self.results.append(TestResult(
                        f"CLI_{description}", True, expected_contains, "SUCCESS"
                    ))
                else:
                    print(f"✗ {description:45s} - Expected '{expected_contains}' in output")
                    print(f"  Output: {output[:100]}")
                    failed += 1
                    self.results.append(TestResult(
                        f"CLI_{description}", False, expected_contains, output[:50]
                    ))
            except subprocess.TimeoutExpired:
                print(f"✗ {description:45s} - TIMEOUT")
                failed += 1
            except Exception as e:
                print(f"✗ {description:45s} - ERROR: {str(e)[:50]}")
                failed += 1
        
        return passed, failed
    
    def run_all_tests(self):
        """Run all test suites"""
        print("\n" + "=" * 80)
        print("COMPREHENSIVE TEST PIPELINE")
        print("=" * 80)
        
        total_passed = 0
        total_failed = 0
        
        # Test 1: CNF Validation
        passed, failed = self.test_cnf_validation()
        total_passed += passed
        total_failed += failed
        
        # Test 2: Membership Testing
        passed, failed = self.test_membership()
        total_passed += passed
        total_failed += failed
        
        # Test 3: Feasibility Estimation
        passed, failed = self.test_feasibility()
        total_passed += passed
        total_failed += failed
        
        # Test 4: CLI Interface
        passed, failed = self.test_cli_interface()
        total_passed += passed
        total_failed += failed
        
        # Summary
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print(f"Total tests: {total_passed + total_failed}")
        print(f"Passed: {total_passed}")
        print(f"Failed: {total_failed}")
        print(f"Success rate: {100 * total_passed / (total_passed + total_failed):.1f}%")
        print("=" * 80)
        
        # Detailed failure report
        if total_failed > 0:
            print("\nFAILED TESTS:")
            print("-" * 80)
            for result in self.results:
                if not result.passed:
                    print(f"✗ {result.name}")
                    print(f"  Expected: {result.expected}")
                    print(f"  Actual: {result.actual}")
                    if result.error:
                        print(f"  Error: {result.error}")
                    print()
        
        return total_failed == 0


def main():
    """Main entry point"""
    pipeline = TestPipeline()
    success = pipeline.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

