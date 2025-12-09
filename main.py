#!/usr/bin/env python3
"""
Main CLI Interface for CNF Grammar Analyzer

Usage:
    python main.py check_cnf <grammar_file>
    python main.py test_membership <grammar_file> <string>
    python main.py estimate <grammar_file> <string_length>
"""

import sys
import argparse
from grammar_parser import parse_grammar_file
from cnf_checker import check_cnf_file, is_cnf
from membership_tester import test_membership
from feasibility_estimator import is_feasible


def cmd_check_cnf(args):
    """Command: Check if grammar is in CNF"""
    is_cnf_result, message = check_cnf_file(args.grammar_file)
    
    if is_cnf_result:
        print("YES")
        print("The grammar is in Chomsky Normal Form.")
    else:
        print("NO")
        print(f"Reason: {message}")
    
    return 0 if is_cnf_result else 1


def cmd_test_membership(args):
    """Command: Test if string belongs to grammar"""
    try:
        grammar = parse_grammar_file(args.grammar_file)
    except Exception as e:
        print(f"Error parsing grammar file: {e}")
        return 1
    
    # First verify it's CNF
    is_cnf_result, message = is_cnf(grammar)
    if not is_cnf_result:
        print(f"Error: Grammar is not in CNF. {message}")
        print("Membership testing requires CNF grammar.")
        return 1
    
    # Test membership
    string = args.string
    if string == 'epsilon' or string == 'ε':
        string = ''  # Empty string for epsilon
    
    result = test_membership(grammar, string)
    
    if result:
        print("YES")
        if string == '':
            print("The empty string (epsilon) belongs to the grammar.")
        else:
            print(f"The string '{string}' belongs to the grammar.")
    else:
        print("NO")
        if string == '':
            print("The empty string (epsilon) does not belong to the grammar.")
        else:
            print(f"The string '{string}' does not belong to the grammar.")
    
    return 0


def cmd_estimate(args):
    """Command: Estimate feasibility of running algorithm"""
    try:
        grammar = parse_grammar_file(args.grammar_file)
    except Exception as e:
        print(f"Error parsing grammar file: {e}")
        return 1
    
    try:
        string_length = int(args.string_length)
    except ValueError:
        print(f"Error: Invalid string length: {args.string_length}")
        return 1
    
    feasible, explanation = is_feasible(grammar, string_length)
    
    if feasible:
        print("YES")
    else:
        print("NO")
    
    print(explanation)
    
    return 0


def main():
    parser = argparse.ArgumentParser(
        description='CNF Grammar Analyzer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py check_cnf grammar.txt
  python main.py test_membership grammar.txt 1010
  python main.py estimate grammar.txt 10
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # check_cnf command
    parser_check = subparsers.add_parser('check_cnf', help='Check if grammar is in CNF')
    parser_check.add_argument('grammar_file', help='Path to grammar file')
    
    # test_membership command
    parser_test = subparsers.add_parser('test_membership', help='Test if string belongs to grammar')
    parser_test.add_argument('grammar_file', help='Path to grammar file')
    parser_test.add_argument('string', help='String to test (use "epsilon" or "ε" for empty string)')
    
    # estimate command
    parser_estimate = subparsers.add_parser('estimate', help='Estimate feasibility for string length')
    parser_estimate.add_argument('grammar_file', help='Path to grammar file')
    parser_estimate.add_argument('string_length', help='String length to estimate for')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Route to appropriate command handler
    if args.command == 'check_cnf':
        return cmd_check_cnf(args)
    elif args.command == 'test_membership':
        return cmd_test_membership(args)
    elif args.command == 'estimate':
        return cmd_estimate(args)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())

