"""
Feasibility Estimator Module

Estimates whether the naive brute force membership algorithm can complete
within 1 minute for a given grammar and string length.
"""

from grammar_parser import Grammar
from typing import Tuple
import time


# Estimated operations per second (conservative estimate)
# This is a rough benchmark - actual performance depends on many factors
ESTIMATED_OPS_PER_SECOND = 1000000  # 1 million operations per second


def estimate_worst_case_operations(grammar: Grammar, string_length: int) -> int:
    """
    Estimate worst-case number of operations for naive algorithm.
    
    For string length n:
    - Max steps: 2n - 1
    - At each step, we branch on:
      * Number of binary rules
      * Number of split points (n-1 for string of length n)
    
    Worst case: exponential growth
    """
    if string_length == 0:
        # Epsilon check - very fast
        return 1
    
    num_binary_rules = len(grammar.get_binary_rules())
    
    if num_binary_rules == 0:
        # No binary rules - only terminal rules, very fast
        return string_length * len(grammar.get_terminal_rules())
    
    # Rough estimate: at each level we try all binary rules × all splits
    # This is a very rough upper bound
    # Actual algorithm is more complex due to step distribution
    
    # Conservative estimate: (num_binary_rules * string_length)^(2*string_length - 1)
    # But this grows extremely fast, so we use a more practical heuristic
    
    max_steps = 2 * string_length - 1
    
    # Estimate: each recursive call tries num_binary_rules * (n-1) possibilities
    # With depth max_steps
    # This is exponential: (num_binary_rules * (n-1))^max_steps
    
    if string_length == 1:
        return num_binary_rules + len(grammar.get_terminal_rules())
    
    # For longer strings, estimate grows exponentially
    branching_factor = num_binary_rules * (string_length - 1)
    
    # Cap the estimate to avoid overflow
    if branching_factor == 0:
        return 1
    
    # Rough exponential estimate
    # Use min to avoid overflow
    estimated_ops = min(branching_factor ** max_steps, 10**18)
    
    return estimated_ops


def is_feasible(grammar: Grammar, string_length: int) -> Tuple[bool, str]:
    """
    Determine if it's feasible to run the naive algorithm for given string length.
    
    Returns:
        (is_feasible: bool, explanation: str)
    """
    if string_length < 0:
        return False, "String length must be non-negative"
    
    # Quick heuristic checks
    num_binary_rules = len(grammar.get_binary_rules())
    
    # Very conservative thresholds
    if string_length == 0:
        return True, "Epsilon check is very fast"
    
    if string_length == 1:
        return True, "Single character check is very fast"
    
    # For longer strings, check based on estimated operations
    if string_length > 20:
        return False, f"String length {string_length} is too long (threshold: 20)"
    
    if num_binary_rules > 10 and string_length > 10:
        return False, f"Too many binary rules ({num_binary_rules}) for string length {string_length}"
    
    # Estimate worst-case operations
    estimated_ops = estimate_worst_case_operations(grammar, string_length)
    
    # Estimate time in seconds
    estimated_seconds = estimated_ops / ESTIMATED_OPS_PER_SECOND
    
    if estimated_seconds > 60:
        return False, f"Estimated worst-case time: {estimated_seconds:.2f} seconds (exceeds 60 seconds)"
    
    return True, f"Estimated worst-case time: {estimated_seconds:.4f} seconds (within 60 seconds)"

