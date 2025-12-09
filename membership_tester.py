"""
Membership Tester Module

Implements naive brute force algorithm to check if a string belongs to a CNF grammar.

Key insight: For CNF grammar, any derivation of string w of length n≥1 has exactly 2n-1 steps.
This allows us to enumerate all possible derivations up to this limit.
"""

from grammar_parser import Grammar
from typing import Optional


class MembershipTester:
    """Tests string membership in CNF grammar using naive brute force"""
    
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.memo = {}  # Memoization cache: (variable, string, steps) -> bool
    
    def test_membership(self, string: str) -> bool:
        """
        Test if string belongs to the grammar.
        
        Args:
            string: The string to test (use '' for epsilon)
        
        Returns:
            True if string can be derived, False otherwise
        """
        # Handle epsilon case
        if string == '':
            return self._can_derive_epsilon('S')
        
        n = len(string)
        max_steps = 2 * n - 1
        
        # Clear memoization cache for new test
        self.memo.clear()
        
        return self._derive('S', string, max_steps)
    
    def _can_derive_epsilon(self, variable: str) -> bool:
        """Check if variable can derive epsilon"""
        if variable not in self.grammar.rules:
            return False
        
        for prod in self.grammar.rules[variable]:
            if len(prod) == 1 and prod[0] == '$':
                return True
        
        return False
    
    def _derive(self, variable: str, target_string: str, steps_remaining: int) -> bool:
        """
        Try to derive target_string from variable using at most steps_remaining steps.
        
        Uses memoization to avoid redundant computations.
        """
        # Memoization key
        memo_key = (variable, target_string, steps_remaining)
        if memo_key in self.memo:
            return self.memo[memo_key]
        
        # Base case: no steps remaining
        if steps_remaining == 0:
            result = (variable == target_string)
            self.memo[memo_key] = result
            return result
        
        # Base case: empty string
        if len(target_string) == 0:
            result = self._can_derive_epsilon(variable)
            self.memo[memo_key] = result
            return result
        
        # Base case: single character
        if len(target_string) == 1:
            # Check terminal rules
            if variable not in self.grammar.rules:
                self.memo[memo_key] = False
                return False
            
            for prod in self.grammar.rules[variable]:
                if len(prod) == 1 and prod[0] == target_string:
                    # Direct terminal production
                    if steps_remaining == 1:
                        self.memo[memo_key] = True
                        return True
                    # Can't use more steps for single terminal
                    continue
            
            self.memo[memo_key] = False
            return False
        
        # Recursive case: try all binary rules and all possible splits
        if variable not in self.grammar.rules:
            self.memo[memo_key] = False
            return False
        
        for prod in self.grammar.rules[variable]:
            if len(prod) == 2:
                # Binary production: A -> BC
                left_var, right_var = prod[0], prod[1]
                
                # Try all possible splits of target_string
                for split_point in range(1, len(target_string)):
                    left_part = target_string[:split_point]
                    right_part = target_string[split_point:]
                    
                    # Calculate exact steps needed for each part
                    # For string of length k (k≥1), we need exactly 2k - 1 steps
                    # For epsilon (k=0), we need 1 step if variable can derive epsilon
                    left_length = len(left_part)
                    right_length = len(right_part)
                    
                    # Calculate steps needed for left part
                    if left_length == 0:
                        # Epsilon: need 1 step if derivable, otherwise impossible
                        if not self._can_derive_epsilon(left_var):
                            continue
                        left_steps_needed = 1
                    else:
                        left_steps_needed = 2 * left_length - 1
                    
                    # Calculate steps needed for right part
                    if right_length == 0:
                        # Epsilon: need 1 step if derivable, otherwise impossible
                        if not self._can_derive_epsilon(right_var):
                            continue
                        right_steps_needed = 1
                    else:
                        right_steps_needed = 2 * right_length - 1
                    
                    # Check if we have enough steps total
                    # Total steps needed = 1 (for binary rule) + left_steps + right_steps
                    total_steps_needed = 1 + left_steps_needed + right_steps_needed
                    
                    if total_steps_needed > steps_remaining:
                        continue
                    
                    # Try with exact step counts
                    if (self._derive(left_var, left_part, left_steps_needed) and
                        self._derive(right_var, right_part, right_steps_needed)):
                        self.memo[memo_key] = True
                        return True
        
        self.memo[memo_key] = False
        return False


def test_membership(grammar: Grammar, string: str) -> bool:
    """
    Convenience function to test string membership.
    
    Args:
        grammar: CNF grammar
        string: String to test
    
    Returns:
        True if string belongs to grammar, False otherwise
    """
    tester = MembershipTester(grammar)
    return tester.test_membership(string)

