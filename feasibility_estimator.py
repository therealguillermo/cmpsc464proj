"""
Feasibility Estimator Module

This module estimates whether the membership testing algorithm can finish
within 1 minute for a given grammar and string length.

Why is this important?
The membership algorithm uses brute force, which can be VERY slow for long strings.
This module helps us decide if it's worth even trying.
"""

from grammar_parser import Grammar
from typing import Tuple


# Rough estimate: how many operations can we do per second?
# This is a conservative guess - actual speed depends on your computer
OPERATIONS_PER_SECOND = 1000000  # 1 million operations per second


def estimate_worst_case_operations(grammar: Grammar, string_length: int) -> int:
    """
    Estimate the worst-case number of operations needed.
    
    The algorithm tries all possible ways to derive a string. For a string of
    length n, this can be exponential - meaning it grows VERY fast!
    
    Args:
        grammar: The grammar to test
        string_length: Length of the string we want to test
    
    Returns:
        Estimated number of operations (could be huge!)
    
    Example:
        ops = estimate_worst_case_operations(grammar, 10)
        print(f"Will need about {ops} operations")
    """
    # Empty string is very fast - just check if S -> ε exists
    if string_length == 0:
        return 1
    
    # Count how many binary rules the grammar has
    num_binary_rules = len(grammar.get_binary_rules())
    
    # If no binary rules, only terminal rules - this is very fast!
    if num_binary_rules == 0:
        num_terminal_rules = len(grammar.get_terminal_rules())
        return string_length * num_terminal_rules
    
    # Single character is also fast
    if string_length == 1:
        return num_binary_rules + len(grammar.get_terminal_rules())
    
    # For longer strings, the algorithm grows exponentially
    # At each step, we try:
    #   - All binary rules (num_binary_rules options)
    #   - All ways to split the string (string_length - 1 options)
    # So we have roughly: (num_binary_rules * string_length)^(2*string_length - 1)
    
    max_steps = 2 * string_length - 1
    branching_factor = num_binary_rules * (string_length - 1)
    
    # Avoid overflow (numbers getting too big)
    if branching_factor == 0:
        return 1
    
    # Calculate estimate, but cap it to avoid overflow
    estimated_operations = min(branching_factor ** max_steps, 10**18)
    
    return estimated_operations


def is_feasible(grammar: Grammar, string_length: int) -> Tuple[bool, str]:
    """
    Decide if it's feasible to test a string of given length.
    
    "Feasible" means we think the algorithm can finish within 1 minute.
    
    Args:
        grammar: The grammar to test
        string_length: Length of string we want to test
    
    Returns:
        Tuple of (is_feasible, explanation)
        - is_feasible: True if we think it will finish in time, False otherwise
        - explanation: Human-readable explanation
    
    Example:
        feasible, reason = is_feasible(grammar, 10)
        if feasible:
            print(f"Yes, should be fast enough: {reason}")
        else:
            print(f"No, will be too slow: {reason}")
    """
    # Negative length doesn't make sense
    if string_length < 0:
        return False, "String length must be non-negative"
    
    # Count binary rules (these make the algorithm slower)
    num_binary_rules = len(grammar.get_binary_rules())
    
    # Empty string is always fast
    if string_length == 0:
        return True, "Epsilon check is very fast"
    
    # Single character is always fast
    if string_length == 1:
        return True, "Single character check is very fast"
    
    # Very long strings are definitely too slow
    if string_length > 20:
        return False, f"String length {string_length} is too long (threshold: 20)"
    
    # Many binary rules + long string = probably too slow
    if num_binary_rules > 10 and string_length > 10:
        return False, f"Too many binary rules ({num_binary_rules}) for string length {string_length}"
    
    # Estimate how many operations we'll need
    estimated_operations = estimate_worst_case_operations(grammar, string_length)
    
    # Estimate how long it will take (in seconds)
    estimated_seconds = estimated_operations / OPERATIONS_PER_SECOND
    
    # Check if it's within our 1-minute limit
    if estimated_seconds > 60:
        return False, f"Estimated worst-case time: {estimated_seconds:.2f} seconds (exceeds 60 seconds)"
    
    return True, f"Estimated worst-case time: {estimated_seconds:.4f} seconds (within 60 seconds)"
