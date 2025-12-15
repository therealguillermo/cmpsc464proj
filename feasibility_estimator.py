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
# Modern computers can do 100 billion to 1 trillion operations per second.
# Accounting for ~1000x overhead due to inefficiency, checking, etc.,
# we use a conservative estimate of 10 billion operations per second.
OPERATIONS_PER_SECOND = 10_000_000_000  # 10 billion operations per second


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
    
    # If no binary rules, only terminal rules - this is linear and very fast!
    # Skip heuristic checks and go straight to calculation
    if num_binary_rules == 0:
        estimated_operations = estimate_worst_case_operations(grammar, string_length)
        estimated_seconds = estimated_operations / OPERATIONS_PER_SECOND
        if estimated_seconds <= 300:  # 5 minutes
            return True, f"Estimated operations: {estimated_operations:,} (grammar has no binary rules, ~{estimated_seconds:.2f} seconds)"
        else:
            return False, f"Estimated operations: {estimated_operations:,} (grammar has no binary rules but ~{estimated_seconds:.2f} seconds exceeds 300 seconds)"
    
    # Estimate how many operations we'll need
    # The calculation will correctly identify infeasible cases based on actual grammar structure
    estimated_operations = estimate_worst_case_operations(grammar, string_length)
    
    # Key threshold: 1 billion possibilities × 1000x overhead = 1 trillion operations
    # This is the threshold for feasibility in a few minutes
    ONE_TRILLION_OPS = 1_000_000_000_000  # 1 trillion operations
    
    # Direct check: if we're under 1 trillion operations, it's feasible
    if estimated_operations <= ONE_TRILLION_OPS:
        estimated_seconds = estimated_operations / OPERATIONS_PER_SECOND
        return True, f"Estimated operations: {estimated_operations:,} (≤ 1 trillion threshold, ~{estimated_seconds:.2f} seconds)"
    
    # If over 1 trillion, estimate time and check against time limit
    estimated_seconds = estimated_operations / OPERATIONS_PER_SECOND
    time_limit_seconds = 300  # 5 minutes (few minutes)
    
    if estimated_seconds > time_limit_seconds:
        return False, f"Estimated operations: {estimated_operations:,} (exceeds 1 trillion threshold, ~{estimated_seconds:.2f} seconds, exceeds {time_limit_seconds} seconds)"
    
    return True, f"Estimated operations: {estimated_operations:,} (exceeds 1 trillion threshold but ~{estimated_seconds:.2f} seconds within {time_limit_seconds} seconds)"
