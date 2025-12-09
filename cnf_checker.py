"""
CNF Checker Module

Validates whether a grammar is in Chomsky Normal Form (CNF).

CNF Requirements:
1. All productions must be one of:
   - A -> BC (two non-terminals)
   - A -> a (single terminal, not epsilon)
   - S -> ε (only start variable can derive epsilon)
2. If S -> ε exists, S cannot appear on the right side of any production
"""

from grammar_parser import Grammar, parse_grammar_file
from typing import Tuple


def is_cnf(grammar: Grammar) -> Tuple[bool, str]:
    """
    Check if grammar is in CNF.
    
    Returns:
        (is_cnf: bool, error_message: str)
        If is_cnf is True, error_message is empty.
        If is_cnf is False, error_message explains why.
    """
    # Check 1: Start variable must be S
    if grammar.start != 'S':
        return False, f"Start variable must be S, found: {grammar.start}"
    
    # Check 2: Validate all rules
    epsilon_var = None
    
    for variable, productions in grammar.rules.items():
        # Validate variable name
        if not variable.isupper() or len(variable) != 1:
            return False, f"Invalid variable name: {variable} (must be single uppercase letter)"
        
        if variable != 'S' and variable == 'S':
            # Redundant check
            pass
        
        for prod in productions:
            # Check production format
            if len(prod) == 0:
                return False, f"Empty production found for variable {variable}"
            
            if len(prod) == 1:
                # Single symbol: must be terminal OR epsilon (only for S)
                symbol = prod[0]
                
                if symbol == '$':
                    # Epsilon production
                    if variable != 'S':
                        return False, f"Epsilon production only allowed for start variable S, found for {variable}"
                    epsilon_var = variable
                elif symbol.islower() or symbol.isdigit():
                    # Terminal production - valid
                    pass
                elif symbol.isupper():
                    # Single variable - not valid in CNF
                    return False, f"Invalid CNF production: {variable} -> {symbol} (single variable not allowed, use terminal or binary rule)"
                else:
                    return False, f"Invalid symbol in production: {symbol}"
            
            elif len(prod) == 2:
                # Two symbols: both must be variables (non-terminals)
                left, right = prod[0], prod[1]
                
                if not (left.isupper() and right.isupper()):
                    return False, f"Binary production {variable} -> {left}{right} must have two variables (uppercase letters)"
                
                # Check that they are valid variables
                if len(left) != 1 or len(right) != 1:
                    return False, f"Binary production {variable} -> {left}{right} must have single-character variables"
            
            else:
                # More than 2 symbols - invalid for CNF
                return False, f"Invalid CNF production: {variable} -> {''.join(prod)} (CNF allows max 2 symbols on right side)"
    
    # Check 3: If S -> ε exists, S cannot appear on right side of any production
    if epsilon_var == 'S':
        for variable, productions in grammar.rules.items():
            for prod in productions:
                if len(prod) == 2:
                    # Check binary production
                    if 'S' in prod:
                        return False, f"If S -> ε exists, S cannot appear on right side. Found: {variable} -> {prod[0]}{prod[1]}"
                # Note: S can't appear in terminal productions (those are terminals)
    
    # Check 4: Validate all symbols used are valid
    for variable, productions in grammar.rules.items():
        for prod in productions:
            for symbol in prod:
                if symbol == '$':
                    continue
                elif symbol.isupper():
                    # Variable - should be in grammar's variables
                    if symbol not in grammar.variables:
                        # This shouldn't happen if parsing is correct, but check anyway
                        pass
                elif symbol.islower() or symbol.isdigit():
                    # Terminal - valid
                    pass
                else:
                    return False, f"Invalid symbol found: {symbol}"
    
    return True, ""


def check_cnf_file(filename: str) -> Tuple[bool, str]:
    """
    Parse a grammar file and check if it's in CNF.
    
    Returns:
        (is_cnf: bool, message: str)
    """
    try:
        grammar = parse_grammar_file(filename)
        return is_cnf(grammar)
    except Exception as e:
        return False, f"Error parsing grammar: {str(e)}"

