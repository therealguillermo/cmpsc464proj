#!/usr/bin/env python3
"""
Test script to verify all example grammars are correctly classified.
Runs CNF checker on all valid and invalid examples.
"""

import os
import sys
from cnf_checker import check_cnf_file


def test_examples():
    """Test all example grammars"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    valid_dir = os.path.join(base_dir, 'examples', 'valid')
    invalid_dir = os.path.join(base_dir, 'examples', 'invalid')
    
    print("=" * 70)
    print("Testing VALID CNF Grammars (should all return YES)")
    print("=" * 70)
    
    valid_files = sorted([f for f in os.listdir(valid_dir) if f.endswith('.txt')])
    valid_passed = 0
    valid_failed = 0
    
    for filename in valid_files:
        filepath = os.path.join(valid_dir, filename)
        is_cnf, message = check_cnf_file(filepath)
        
        if is_cnf:
            print(f"✓ {filename:40s} - YES (correct)")
            valid_passed += 1
        else:
            print(f"✗ {filename:40s} - NO  (ERROR: {message})")
            valid_failed += 1
    
    print(f"\nValid grammars: {valid_passed} passed, {valid_failed} failed")
    
    print("\n" + "=" * 70)
    print("Testing INVALID CNF Grammars (should all return NO)")
    print("=" * 70)
    
    invalid_files = sorted([f for f in os.listdir(invalid_dir) if f.endswith('.txt')])
    invalid_passed = 0
    invalid_failed = 0
    
    for filename in invalid_files:
        filepath = os.path.join(invalid_dir, filename)
        is_cnf, message = check_cnf_file(filepath)
        
        if not is_cnf:
            print(f"✓ {filename:40s} - NO  (correct: {message[:50]})")
            invalid_passed += 1
        else:
            print(f"✗ {filename:40s} - YES (ERROR: Should be invalid!)")
            invalid_failed += 1
    
    print(f"\nInvalid grammars: {invalid_passed} passed, {invalid_failed} failed")
    
    print("\n" + "=" * 70)
    total_tests = len(valid_files) + len(invalid_files)
    total_passed = valid_passed + invalid_passed
    total_failed = valid_failed + invalid_failed
    print(f"SUMMARY: {total_passed}/{total_tests} tests passed, {total_failed} failed")
    print("=" * 70)
    
    return total_failed == 0


if __name__ == '__main__':
    success = test_examples()
    sys.exit(0 if success else 1)

