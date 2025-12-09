"""
Grammar Parser Module

Parses grammar files in the specified format:
- First line: number n (number of rules)
- Next n lines: rules in format VAR=production1|production2|...
- Variables: uppercase letters (S reserved for start)
- Terminals: lowercase letters, digits 0-9, $ (epsilon)
- Right arrow: =
- Separator: |
"""

import re
from typing import Dict, List, Tuple, Set


class Grammar:
    """Represents a Context-Free Grammar"""
    
    def __init__(self):
        self.start = 'S'
        self.variables: Set[str] = set()
        self.terminals: Set[str] = set()
        self.rules: Dict[str, List[Tuple]] = {}
    
    def add_rule(self, variable: str, productions: List[str]):
        """Add a rule to the grammar"""
        if variable not in self.rules:
            self.rules[variable] = []
        
        self.variables.add(variable)
        
        for prod in productions:
            # Parse production into tuple representation
            prod_tuple = self._parse_production(prod.strip())
            self.rules[variable].append(prod_tuple)
            
            # Track terminals and variables in production
            for symbol in prod_tuple:
                if symbol == '$':
                    self.terminals.add('$')
                elif symbol.islower() or symbol.isdigit():
                    self.terminals.add(symbol)
                elif symbol.isupper():
                    self.variables.add(symbol)
    
    def _parse_production(self, production: str) -> Tuple:
        """Parse a production string into tuple representation"""
        # Remove whitespace
        production = production.strip()
        
        # Handle case where production is just epsilon
        if production == '$':
            return ('$',)
        
        # Split into symbols (each symbol is a single character)
        # Don't validate CNF format here - let CNF checker do that
        symbols = list(production)
        return tuple(symbols)
    
    def get_binary_rules(self) -> List[Tuple[str, str, str]]:
        """Get all binary rules (A -> BC) as list of (A, B, C) tuples"""
        binary_rules = []
        for var, productions in self.rules.items():
            for prod in productions:
                if len(prod) == 2:
                    binary_rules.append((var, prod[0], prod[1]))
        return binary_rules
    
    def get_terminal_rules(self) -> List[Tuple[str, str]]:
        """Get all terminal rules (A -> a) as list of (A, a) tuples"""
        terminal_rules = []
        for var, productions in self.rules.items():
            for prod in productions:
                if len(prod) == 1 and prod[0] != '$':
                    terminal_rules.append((var, prod[0]))
        return terminal_rules
    
    def has_epsilon_rule(self) -> bool:
        """Check if grammar has epsilon production"""
        for var, productions in self.rules.items():
            for prod in productions:
                if len(prod) == 1 and prod[0] == '$':
                    return True
        return False
    
    def get_epsilon_variable(self) -> str:
        """Get the variable that has epsilon production, or None"""
        for var, productions in self.rules.items():
            for prod in productions:
                if len(prod) == 1 and prod[0] == '$':
                    return var
        return None


def parse_grammar_file(filename: str) -> Grammar:
    """
    Parse a grammar file and return a Grammar object.
    
    File format:
    - First line: number n
    - Next n lines: rules in format VAR=prod1|prod2|...
    """
    grammar = Grammar()
    
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    if not lines:
        raise ValueError("Empty grammar file")
    
    # First line should be number of rules
    try:
        num_rules = int(lines[0])
    except ValueError:
        raise ValueError(f"First line must be a number, got: {lines[0]}")
    
    if len(lines) - 1 != num_rules:
        raise ValueError(f"Expected {num_rules} rules, found {len(lines) - 1} lines")
    
    # Parse each rule
    for i in range(1, num_rules + 1):
        line = lines[i]
        
        # Split by = to get variable and productions
        if '=' not in line:
            raise ValueError(f"Invalid rule format (missing =): {line}")
        
        parts = line.split('=', 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid rule format: {line}")
        
        variable = parts[0].strip()
        productions_str = parts[1].strip()
        
        # Validate variable
        if not variable.isupper() or len(variable) != 1:
            raise ValueError(f"Invalid variable (must be single uppercase letter): {variable}")
        
        if variable != 'S' and variable == 'S':
            # This is redundant but keeping for clarity
            pass
        
        # Split productions by |
        productions = [p.strip() for p in productions_str.split('|')]
        
        if not productions:
            raise ValueError(f"No productions found for variable {variable}")
        
        # Add rule to grammar
        grammar.add_rule(variable, productions)
    
    return grammar

