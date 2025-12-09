"""
Grammar Parser Module

This module reads grammar files and converts them into a data structure we can work with.

File Format:
- First line: number n (how many rules)
- Next n lines: rules like VAR=production1|production2|...
- Variables: uppercase letters (A-Z), S is the start variable
- Terminals: lowercase letters (a-z), digits (0-9), $ means epsilon (empty string)
- Right arrow: = (instead of ->)
- Separator: | (separates different options)

Example file:
  3
  S=AB|a
  A=a
  B=b
"""

from typing import Dict, List, Tuple, Set


class Grammar:
    """
    Represents a Context-Free Grammar.
    
    This class stores all the information about a grammar:
    - What variables it has (like S, A, B)
    - What terminals it has (like a, b, 1, 2)
    - What rules it has (like S -> AB or A -> a)
    """
    
    def __init__(self):
        """Create a new empty grammar"""
        self.start = 'S'  # S is always the start variable
        self.variables: Set[str] = set()  # All variables (uppercase letters)
        self.terminals: Set[str] = set()  # All terminals (lowercase, digits, $)
        self.rules: Dict[str, List[Tuple]] = {}  # Maps variable -> list of productions
    
    def add_rule(self, variable: str, productions: List[str]):
        """
        Add a rule to the grammar.
        
        Example: add_rule('S', ['AB', 'a']) adds S -> AB | a
        
        Args:
            variable: The variable on the left side (like 'S' or 'A')
            productions: List of strings representing right sides (like ['AB', 'a'])
        """
        # Create empty list for this variable if it doesn't exist
        if variable not in self.rules:
            self.rules[variable] = []
        
        # Remember that this variable exists
        self.variables.add(variable)
        
        # Process each production option
        for production_string in productions:
            # Convert string like "AB" into tuple like ('A', 'B')
            production_tuple = self._parse_production(production_string.strip())
            self.rules[variable].append(production_tuple)
            
            # Track what symbols we see (for variables and terminals)
            for symbol in production_tuple:
                if symbol == '$':
                    # $ means epsilon (empty string)
                    self.terminals.add('$')
                elif symbol.islower() or symbol.isdigit():
                    # Lowercase letter or digit = terminal
                    self.terminals.add(symbol)
                elif symbol.isupper():
                    # Uppercase letter = variable
                    self.variables.add(symbol)
    
    def _parse_production(self, production_string: str) -> Tuple:
        """
        Convert a production string into a tuple of symbols.
        
        Examples:
            "AB" -> ('A', 'B')
            "a" -> ('a',)
            "$" -> ('$',)
        
        Args:
            production_string: The production as a string (like "AB" or "a")
        
        Returns:
            Tuple of symbols (like ('A', 'B') or ('a',))
        """
        production_string = production_string.strip()
        
        # Special case: epsilon is represented as $
        if production_string == '$':
            return ('$',)
        
        # Convert string to list of characters, then to tuple
        # Example: "AB" -> ['A', 'B'] -> ('A', 'B')
        symbols = list(production_string)
        return tuple(symbols)
    
    def get_binary_rules(self) -> List[Tuple[str, str, str]]:
        """
        Get all binary rules (rules with two variables).
        
        Example: If grammar has S -> AB, returns [('S', 'A', 'B')]
        
        Returns:
            List of (variable, first_var, second_var) tuples
        """
        binary_rules = []
        for variable, productions in self.rules.items():
            for production in productions:
                # Binary rule has exactly 2 symbols
                if len(production) == 2:
                    binary_rules.append((variable, production[0], production[1]))
        return binary_rules
    
    def get_terminal_rules(self) -> List[Tuple[str, str]]:
        """
        Get all terminal rules (rules with one terminal).
        
        Example: If grammar has A -> a, returns [('A', 'a')]
        
        Returns:
            List of (variable, terminal) tuples
        """
        terminal_rules = []
        for variable, productions in self.rules.items():
            for production in productions:
                # Terminal rule has 1 symbol that's not epsilon
                if len(production) == 1 and production[0] != '$':
                    terminal_rules.append((variable, production[0]))
        return terminal_rules
    
    def has_epsilon_rule(self) -> bool:
        """
        Check if grammar has any epsilon production (like S -> $).
        
        Returns:
            True if any variable can produce epsilon, False otherwise
        """
        for variable, productions in self.rules.items():
            for production in productions:
                # Epsilon production has 1 symbol that is $
                if len(production) == 1 and production[0] == '$':
                    return True
        return False
    
    def get_epsilon_variable(self) -> str:
        """
        Find which variable has epsilon production.
        
        Returns:
            The variable name (like 'S') if found, None otherwise
        """
        for variable, productions in self.rules.items():
            for production in productions:
                if len(production) == 1 and production[0] == '$':
                    return variable
        return None


def parse_grammar_file(filename: str) -> Grammar:
    """
    Read a grammar file and create a Grammar object.
    
    This is the main function to use - it reads the file and returns
    a Grammar object you can work with.
    
    Example:
        grammar = parse_grammar_file("my_grammar.txt")
        print(grammar.rules)  # See all the rules
    
    Args:
        filename: Path to the grammar file
    
    Returns:
        A Grammar object containing all the grammar information
    
    Raises:
        ValueError: If the file format is incorrect
    """
    grammar = Grammar()
    
    # Read all lines from the file, removing empty lines
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]
    
    if not lines:
        raise ValueError("Empty grammar file")
    
    # First line tells us how many rules to expect
    try:
        num_rules = int(lines[0])
    except ValueError:
        raise ValueError(f"First line must be a number, got: {lines[0]}")
    
    # Check that we have the right number of rule lines
    if len(lines) - 1 != num_rules:
        raise ValueError(f"Expected {num_rules} rules, found {len(lines) - 1} lines")
    
    # Process each rule line
    for i in range(1, num_rules + 1):
        rule_line = lines[i]
        
        # Each line should have format: VARIABLE=production1|production2|...
        if '=' not in rule_line:
            raise ValueError(f"Invalid rule format (missing =): {rule_line}")
        
        # Split into variable and productions
        parts = rule_line.split('=', 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid rule format: {rule_line}")
        
        variable = parts[0].strip()
        productions_string = parts[1].strip()
        
        # Validate variable name (must be single uppercase letter)
        if not variable.isupper() or len(variable) != 1:
            raise ValueError(f"Invalid variable (must be single uppercase letter): {variable}")
        
        # Split productions by | (each | separates an option)
        # Example: "AB|a" -> ["AB", "a"]
        productions = [p.strip() for p in productions_string.split('|')]
        
        if not productions:
            raise ValueError(f"No productions found for variable {variable}")
        
        # Add this rule to the grammar
        grammar.add_rule(variable, productions)
    
    return grammar
