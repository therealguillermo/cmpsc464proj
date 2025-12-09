"""
CNF Checker Module

This module checks if a grammar is in Chomsky Normal Form (CNF).

What is CNF?
A grammar is in CNF if every rule follows one of these patterns:
1. A -> BC  (two variables, like S -> AB)
2. A -> a   (one terminal, like A -> a)
3. S -> ε   (epsilon, only allowed for start variable S)

Special Rule: If S -> ε exists, then S cannot appear on the right side
             of any production (like in S -> AS would be invalid).
"""

from grammar_parser import Grammar, parse_grammar_file
from typing import Tuple


def is_cnf(grammar: Grammar) -> Tuple[bool, str]:
    """
    Check if a grammar is in Chomsky Normal Form.
    
    This function goes through all the rules and checks if they follow
    the CNF requirements.
    
    Args:
        grammar: The grammar to check
    
    Returns:
        Tuple of (is_valid_cnf, error_message)
        - If valid: (True, "")
        - If invalid: (False, "explanation of why")
    
    Example:
        grammar = parse_grammar_file("grammar.txt")
        is_valid, message = is_cnf(grammar)
        if is_valid:
            print("Grammar is in CNF!")
        else:
            print(f"Not CNF: {message}")
    """
    # Rule 1: Start variable must be S
    if grammar.start != 'S':
        return False, f"Start variable must be S, found: {grammar.start}"
    
    # We'll track if we find an epsilon production for S
    has_s_epsilon = False
    
    # Check each rule in the grammar
    for variable, productions in grammar.rules.items():
        # Make sure variable name is valid (single uppercase letter)
        if not variable.isupper() or len(variable) != 1:
            return False, f"Invalid variable name: {variable} (must be single uppercase letter)"
        
        # Check each production for this variable
        for production in productions:
            # Empty production is not allowed
            if len(production) == 0:
                return False, f"Empty production found for variable {variable}"
            
            # Check production with 1 symbol
            if len(production) == 1:
                symbol = production[0]
                
                if symbol == '$':
                    # This is an epsilon production ($ means epsilon)
                    if variable != 'S':
                        return False, f"Epsilon production only allowed for start variable S, found for {variable}"
                    has_s_epsilon = True
                    
                elif symbol.islower() or symbol.isdigit():
                    # This is a terminal (like 'a' or '1') - this is valid!
                    pass
                    
                elif symbol.isupper():
                    # This is a single variable (like A -> B) - NOT allowed in CNF
                    return False, f"Invalid CNF production: {variable} -> {symbol} (single variable not allowed, use terminal or binary rule)"
                    
                else:
                    # Invalid symbol (not letter, digit, or $)
                    return False, f"Invalid symbol in production: {symbol}"
            
            # Check production with 2 symbols
            elif len(production) == 2:
                left_symbol = production[0]
                right_symbol = production[1]
                
                # Both symbols must be variables (uppercase letters)
                if not (left_symbol.isupper() and right_symbol.isupper()):
                    return False, f"Binary production {variable} -> {left_symbol}{right_symbol} must have two variables (uppercase letters)"
                
                # Make sure they're single characters
                if len(left_symbol) != 1 or len(right_symbol) != 1:
                    return False, f"Binary production {variable} -> {left_symbol}{right_symbol} must have single-character variables"
            
            # Production with more than 2 symbols is not allowed
            else:
                production_string = ''.join(production)
                return False, f"Invalid CNF production: {variable} -> {production_string} (CNF allows max 2 symbols on right side)"
    
    # Special check: If S -> ε exists, S cannot appear on right side of any rule
    if has_s_epsilon:
        for variable, productions in grammar.rules.items():
            for production in productions:
                # Check binary productions (S can only appear in binary productions)
                if len(production) == 2:
                    # If S appears anywhere in this production, it's invalid
                    if 'S' in production:
                        return False, f"If S -> ε exists, S cannot appear on right side. Found: {variable} -> {production[0]}{production[1]}"
    
    # Check that all symbols used are valid (uppercase = variable, lowercase/digit = terminal)
    for variable, productions in grammar.rules.items():
        for production in productions:
            for symbol in production:
                if symbol == '$':
                    continue  # Epsilon is fine
                elif symbol.isupper():
                    # Variable - should be tracked in grammar.variables
                    pass  # Already checked above
                elif symbol.islower() or symbol.isdigit():
                    # Terminal - valid
                    pass
                else:
                    # Invalid symbol
                    return False, f"Invalid symbol found: {symbol}"
    
    # If we got here, the grammar is valid CNF!
    return True, ""


def check_cnf_file(filename: str) -> Tuple[bool, str]:
    """
    Read a grammar file and check if it's in CNF.
    
    This is a convenience function that combines parsing and checking.
    
    Args:
        filename: Path to the grammar file
    
    Returns:
        Tuple of (is_valid_cnf, message)
    
    Example:
        is_valid, message = check_cnf_file("my_grammar.txt")
        print("YES" if is_valid else "NO")
    """
    try:
        grammar = parse_grammar_file(filename)
        return is_cnf(grammar)
    except Exception as e:
        return False, f"Error parsing grammar: {str(e)}"
