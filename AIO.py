#!/usr/bin/env python3
"""
CNF Grammar Analyzer - All-In-One Version

This single file contains all functionality for analyzing Context-Free Grammars
in Chomsky Normal Form (CNF).

Features:
1. Parse grammar files
2. Check if grammar is in CNF
3. Test if strings belong to grammar
4. Estimate if algorithm is feasible for given string length

File Format:
- First line: number n (how many rules)
- Next n lines: rules like VAR=production1|production2|...
- Variables: uppercase letters (A-Z), S is the start variable
- Terminals: lowercase letters (a-z), digits (0-9), $ means epsilon
- Right arrow: = (instead of ->)
- Separator: | (separates different options)

Usage:
    python3 AIO.py check_cnf <grammar_file>
    python3 AIO.py test_membership <grammar_file> <string>
    python3 AIO.py estimate <grammar_file> <string_length>
"""

import sys
import argparse
from typing import Dict, List, Tuple, Set


# ============================================================================
# GRAMMAR PARSER
# ============================================================================

class Grammar:
    """
    Represents a Context-Free Grammar (CFG).
    
    This class stores all the information about a grammar including variables,
    terminals, and production rules. It provides methods to query and manipulate
    the grammar structure.
    
    Attributes:
        start (str): The start variable of the grammar. Always 'S' for CNF grammars.
        variables (Set[str]): Set of all variables (non-terminals) in the grammar.
                             Variables are single uppercase letters (A-Z).
        terminals (Set[str]): Set of all terminals in the grammar. Includes
                             lowercase letters (a-z), digits (0-9), and '$' for epsilon.
        rules (Dict[str, List[Tuple]]): Dictionary mapping each variable to a list
                                        of production tuples. Each tuple represents
                                        one production option for that variable.
    
    Example:
        >>> grammar = Grammar()
        >>> grammar.add_rule('S', ['AB', 'a'])
        >>> grammar.add_rule('A', ['a'])
        >>> grammar.add_rule('B', ['b'])
        >>> print(grammar.rules)
        {'S': [('A', 'B'), ('a',)], 'A': [('a',)], 'B': [('b',)]}
    """
    
    def __init__(self):
        """
        Initialize an empty Grammar object.
        
        Creates a new grammar with:
        - Start variable set to 'S'
        - Empty sets for variables and terminals
        - Empty dictionary for rules
        
        Returns:
            None
        """
        self.start = 'S'  # S is always the start variable
        self.variables: Set[str] = set()  # All variables (uppercase letters)
        self.terminals: Set[str] = set()  # All terminals (lowercase, digits, $)
        self.rules: Dict[str, List[Tuple]] = {}  # Maps variable -> list of productions
    
    def add_rule(self, variable: str, productions: List[str]) -> None:
        """
        Add a production rule to the grammar.
        
        Adds one or more production options for a given variable. Each string
        in the productions list represents an alternative right-hand side.
        The productions are automatically parsed into tuples of symbols.
        
        Args:
            variable (str): The variable (non-terminal) on the left side of the rule.
                          Must be a single uppercase letter (A-Z). 'S' is typically
                          the start variable.
            productions (List[str]): List of strings, each representing one production
                                   option. Each string is parsed into symbols.
                                   Example: ['AB', 'a'] means variable -> AB | a
        
        Returns:
            None
        
        Side Effects:
            - Adds the variable to self.variables if not already present
            - Adds the rule to self.rules[variable]
            - Updates self.terminals and self.variables based on symbols found
              in the productions
        
        Example:
            >>> grammar = Grammar()
            >>> grammar.add_rule('S', ['AB', 'a'])
            >>> # This creates: S -> AB | a
            >>> grammar.add_rule('A', ['a', 'b'])
            >>> # This creates: A -> a | b
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
        Parse a production string into a tuple of individual symbols.
        
        Converts a string representation of a production into a tuple where
        each element is a single character symbol. This is an internal helper
        method used by add_rule().
        
        Args:
            production_string (str): The production as a string. Each character
                                    represents one symbol. Examples:
                                    - "AB" represents two variables
                                    - "a" represents one terminal
                                    - "$" represents epsilon
        
        Returns:
            Tuple: Tuple of symbols, where each symbol is a single character.
                  Examples:
                  - "AB" -> ('A', 'B')
                  - "a" -> ('a',)
                  - "$" -> ('$',)
                  - "1B0" -> ('1', 'B', '0')
        
        Note:
            This method does not validate CNF format. It simply converts the
            string to a tuple. CNF validation is done separately.
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
        Extract all binary production rules from the grammar.
        
        A binary rule is a production with exactly two symbols on the right-hand
        side, both of which must be variables (non-terminals). In CNF, these
        are rules of the form A -> BC where B and C are variables.
        
        Returns:
            List[Tuple[str, str, str]]: List of tuples, each representing one
                                        binary rule. Each tuple has the form:
                                        (left_variable, right_var1, right_var2)
                                        Example: [('S', 'A', 'B')] means S -> AB
        
        Example:
            >>> grammar = Grammar()
            >>> grammar.add_rule('S', ['AB'])
            >>> grammar.add_rule('A', ['CD'])
            >>> grammar.add_rule('B', ['b'])
            >>> binary_rules = grammar.get_binary_rules()
            >>> print(binary_rules)
            [('S', 'A', 'B'), ('A', 'C', 'D')]
        
        Note:
            Only returns rules with exactly 2 symbols. Rules with 1 symbol
            (terminals or epsilon) are not included.
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
        Extract all terminal production rules from the grammar.
        
        A terminal rule is a production with exactly one symbol on the right-hand
        side, and that symbol is a terminal (not epsilon). In CNF, these are rules
        of the form A -> a where 'a' is a terminal symbol.
        
        Returns:
            List[Tuple[str, str]]: List of tuples, each representing one terminal
                                  rule. Each tuple has the form:
                                  (variable, terminal)
                                  Example: [('A', 'a'), ('B', 'b')] means
                                  A -> a and B -> b
        
        Example:
            >>> grammar = Grammar()
            >>> grammar.add_rule('A', ['a'])
            >>> grammar.add_rule('B', ['b', '1'])
            >>> grammar.add_rule('S', ['$'])  # Epsilon, not included
            >>> terminal_rules = grammar.get_terminal_rules()
            >>> print(terminal_rules)
            [('A', 'a'), ('B', 'b'), ('B', '1')]
        
        Note:
            Epsilon productions (A -> $) are NOT included in the result.
            Only rules with a single terminal symbol are returned.
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
        Check if the grammar contains any epsilon production.
        
        An epsilon production is a rule where a variable can produce the empty
        string, represented as '$' in the grammar format. In CNF, only the start
        variable S is allowed to have an epsilon production.
        
        Returns:
            bool: True if at least one variable has an epsilon production
                 (like S -> $), False otherwise.
        
        Example:
            >>> grammar = Grammar()
            >>> grammar.add_rule('S', ['$'])
            >>> grammar.has_epsilon_rule()
            True
            >>> grammar2 = Grammar()
            >>> grammar2.add_rule('S', ['AB'])
            >>> grammar2.has_epsilon_rule()
            False
        """
        for variable, productions in self.rules.items():
            for production in productions:
                # Epsilon production has 1 symbol that is $
                if len(production) == 1 and production[0] == '$':
                    return True
        return False
    
    def get_epsilon_variable(self) -> str:
        """
        Find which variable has an epsilon production.
        
        Searches through all rules to find a variable that can produce epsilon
        (empty string). In CNF grammars, typically only 'S' should have epsilon.
        
        Returns:
            str or None: The variable name (like 'S') if an epsilon production
                        is found, None if no epsilon production exists.
        
        Example:
            >>> grammar = Grammar()
            >>> grammar.add_rule('S', ['AB', '$'])
            >>> grammar.get_epsilon_variable()
            'S'
            >>> grammar2 = Grammar()
            >>> grammar2.add_rule('S', ['AB'])
            >>> grammar2.get_epsilon_variable()
            None
        
        Note:
            If multiple variables have epsilon productions, returns the first
            one found. In valid CNF grammars, this should only be 'S'.
        """
        for variable, productions in self.rules.items():
            for production in productions:
                if len(production) == 1 and production[0] == '$':
                    return variable
        return None


def parse_grammar_file(filename: str) -> Grammar:
    """
    Parse a grammar file and create a Grammar object.
    
    Reads a grammar file in the specified format and converts it into a
    Grammar object that can be used for analysis. This is the main entry
    point for loading grammars from files.
    
    File Format:
        - First line: integer n (number of rules)
        - Next n lines: rules in format VAR=production1|production2|...
        - Variables: single uppercase letters (A-Z), S is start variable
        - Terminals: lowercase letters (a-z), digits (0-9), $ for epsilon
        - Right arrow: = (replaces ->)
        - Separator: | (separates alternative productions)
    
    Args:
        filename (str): Path to the grammar file. Can be relative or absolute.
                       File should be readable text file.
    
    Returns:
        Grammar: A Grammar object containing all parsed grammar information,
                including variables, terminals, and rules.
    
    Raises:
        ValueError: If the file format is incorrect. Common errors:
                   - Empty file
                   - First line is not a number
                   - Number of rules doesn't match file content
                   - Invalid rule format (missing '=')
                   - Invalid variable name (not single uppercase letter)
                   - Empty production list
    
    Example:
        Given a file "grammar.txt" containing:
            3
            S=AB|a
            A=a
            B=b
        
        >>> grammar = parse_grammar_file("grammar.txt")
        >>> print(grammar.rules)
        {'S': [('A', 'B'), ('a',)], 'A': [('a',)], 'B': [('b',)]}
        >>> print(grammar.variables)
        {'S', 'A', 'B'}
        >>> print(grammar.terminals)
        {'a', 'b'}
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


# ============================================================================
# CNF CHECKER
# ============================================================================

def is_cnf(grammar: Grammar) -> Tuple[bool, str]:
    """
    Check if a grammar is in Chomsky Normal Form.
    
    This function goes through all the rules and checks if they follow
    the CNF requirements.
    
    What is CNF?
    A grammar is in CNF if every rule follows one of these patterns:
    1. A -> BC  (two variables, like S -> AB)
    2. A -> a   (one terminal, like A -> a)
    3. S -> ε   (epsilon, only allowed for start variable S)
    
    Special Rule: If S -> ε exists, then S cannot appear on the right side
                 of any production (like in S -> AS would be invalid).
    
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
    Parse a grammar file and check if it's in Chomsky Normal Form.
    
    This is a convenience function that combines file parsing and CNF validation
    into a single operation. It's useful for command-line tools and quick checks.
    
    Args:
        filename (str): Path to the grammar file to check. File will be parsed
                       and then validated for CNF compliance.
    
    Returns:
        Tuple[bool, str]: A tuple containing:
            - bool: True if grammar is valid CNF, False otherwise
            - str: Empty string if valid, error message explaining why invalid
                  if not valid. If parsing fails, contains parsing error message.
    
    Example:
        >>> is_valid, message = check_cnf_file("grammar.txt")
        >>> if is_valid:
        ...     print("Grammar is in CNF!")
        ... else:
        ...     print(f"Not CNF: {message}")
    
    Note:
        This function catches all exceptions during parsing and returns them
        as error messages. If parsing succeeds but grammar is not CNF, returns
        False with CNF validation error message.
    """
    try:
        grammar = parse_grammar_file(filename)
        return is_cnf(grammar)
    except Exception as e:
        return False, f"Error parsing grammar: {str(e)}"


# ============================================================================
# MEMBERSHIP TESTER
# ============================================================================

class MembershipTester:
    """
    Tests whether strings can be generated by a CNF grammar.
    
    This class implements a naive brute force algorithm for membership testing
    in CNF grammars. It tries all possible derivations up to the required number
    of steps to determine if a string belongs to the language generated by
    the grammar.
    
    Algorithm:
        Uses the key property of CNF: for a string of length n ≥ 1, any
        derivation takes exactly 2n - 1 steps. The algorithm recursively
        tries all possible ways to derive the string by:
        1. Trying all binary rules (A -> BC)
        2. Trying all possible ways to split the string
        3. Recursively deriving each part
    
    Performance:
        This is a naive exponential-time algorithm. For long strings or
        grammars with many binary rules, it can be very slow. Memoization
        is used to avoid redundant calculations.
    
    Attributes:
        grammar (Grammar): The CNF grammar to test strings against.
        cache (Dict): Memoization cache storing previously computed results.
                     Key: (variable, string, steps_remaining) -> bool
    
    Example:
        >>> grammar = parse_grammar_file("grammar.txt")
        >>> tester = MembershipTester(grammar)
        >>> if tester.test_membership("ab"):
        ...     print("'ab' can be generated!")
    """
    
    def __init__(self, grammar: Grammar):
        """
        Initialize a MembershipTester for a given grammar.
        
        Creates a new tester instance that will test strings against the
        provided grammar. The grammar must be in CNF for correct results.
        
        Args:
            grammar (Grammar): The CNF grammar to test strings against.
                             Should be a valid Grammar object with CNF rules.
        
        Returns:
            None
        
        Note:
            The grammar is not validated for CNF compliance during initialization.
            It's recommended to validate the grammar separately before creating
            a MembershipTester.
        """
        self.grammar = grammar
        # Cache to avoid recalculating the same thing multiple times
        # Key: (variable, string, steps_remaining) -> True/False
        self.cache = {}
    
    def test_membership(self, string: str) -> bool:
        """
        Test if a string belongs to the language generated by the grammar.
        
        Determines whether the given string can be derived from the start
        variable S using the grammar's production rules. Uses the naive
        brute force algorithm with memoization for efficiency.
        
        Args:
            string (str): The string to test for membership. Use empty string
                         '' to test for epsilon (empty string) membership.
        
        Returns:
            bool: True if the string can be generated by the grammar starting
                 from S, False otherwise.
        
        Example:
            >>> grammar = parse_grammar_file("grammar.txt")
            >>> tester = MembershipTester(grammar)
            >>> tester.test_membership("ab")
            True
            >>> tester.test_membership("aa")
            False
            >>> tester.test_membership("")  # Test epsilon
            True
        
        Note:
            - Clears the internal cache at the start of each test
            - For empty string, checks if S can derive epsilon
            - For non-empty strings, uses the 2n-1 steps property
            - Performance degrades exponentially with string length
        """
        # Special case: empty string (epsilon)
        if string == '':
            return self._can_derive_epsilon('S')
        
        # For a string of length n, we need exactly 2n - 1 steps
        string_length = len(string)
        required_steps = 2 * string_length - 1
        
        # Clear cache for new test
        self.cache.clear()
        
        # Try to derive the string starting from S
        return self._try_to_derive('S', string, required_steps)
    
    def _can_derive_epsilon(self, variable: str) -> bool:
        """
        Check if a variable can produce epsilon (empty string).
        
        Determines whether the given variable has a production rule that
        generates epsilon, represented as '$' in the grammar format.
        
        Args:
            variable (str): The variable to check. Should be a single uppercase
                           letter (like 'S' or 'A').
        
        Returns:
            bool: True if the variable has an epsilon production (like A -> $),
                 False otherwise. Also returns False if the variable has no
                 rules defined.
        
        Example:
            >>> grammar = Grammar()
            >>> grammar.add_rule('S', ['$', 'AB'])
            >>> grammar.add_rule('A', ['a'])
            >>> tester = MembershipTester(grammar)
            >>> tester._can_derive_epsilon('S')
            True
            >>> tester._can_derive_epsilon('A')
            False
        
        Note:
            This is a helper method used internally by test_membership().
            It only checks direct epsilon productions, not indirect derivations.
        """
        if variable not in self.grammar.rules:
            return False
        
        # Look for a production that is just epsilon ($)
        for production in self.grammar.rules[variable]:
            if len(production) == 1 and production[0] == '$':
                return True
        
        return False
    
    def _try_to_derive(self, variable: str, target_string: str, steps_remaining: int) -> bool:
        """
        Recursively try to derive target_string from variable within step limit.
        
        This is the core recursive function of the membership algorithm. It
        attempts to derive the target string from the given variable using
        at most steps_remaining derivation steps. Uses memoization to avoid
        redundant calculations.
        
        Algorithm:
            1. Check cache for previously computed result
            2. Handle base cases (no steps, empty string, single character)
            3. For longer strings, try all binary rules and string splits
            4. Recursively derive left and right parts
            5. Cache and return result
        
        Args:
            variable (str): The variable to derive from (like 'S' or 'A').
                          Should be a single uppercase letter.
            target_string (str): The string we want to produce (like "ab").
                                Can be empty string for epsilon.
            steps_remaining (int): Maximum number of derivation steps allowed.
                                  For string of length n, should be 2n - 1.
        
        Returns:
            bool: True if target_string can be derived from variable using
                 at most steps_remaining steps, False otherwise.
        
        Example:
            >>> # Internal method - typically called by test_membership()
            >>> tester._try_to_derive('S', 'ab', 3)  # 2*2-1 = 3 steps
        
        Note:
            - Uses memoization to cache results: (variable, string, steps) -> bool
            - Base cases handle empty strings, single characters, and zero steps
            - For binary rules, tries all possible string splits
            - Step calculation follows CNF property: length k needs 2k-1 steps
        """
        # Check cache first - have we seen this before?
        cache_key = (variable, target_string, steps_remaining)
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Base case 1: No steps left - can only succeed if variable equals string
        if steps_remaining == 0:
            result = (variable == target_string)
            self.cache[cache_key] = result
            return result
        
        # Base case 2: Empty string - check if variable can produce epsilon
        if len(target_string) == 0:
            result = self._can_derive_epsilon(variable)
            self.cache[cache_key] = result
            return result
        
        # Base case 3: Single character - check if variable has terminal rule
        if len(target_string) == 1:
            if variable not in self.grammar.rules:
                self.cache[cache_key] = False
                return False
            
            # Look for a rule like A -> 'a' that matches our character
            for production in self.grammar.rules[variable]:
                if len(production) == 1 and production[0] == target_string:
                    # Found matching terminal rule - need exactly 1 step
                    if steps_remaining == 1:
                        self.cache[cache_key] = True
                        return True
                    # Can't use more than 1 step for a single terminal
                    continue
            
            self.cache[cache_key] = False
            return False
        
        # Recursive case: Try binary rules (like S -> AB)
        if variable not in self.grammar.rules:
            self.cache[cache_key] = False
            return False
        
        # Try each production rule for this variable
        for production in self.grammar.rules[variable]:
            # Only binary rules (2 symbols) can help us derive longer strings
            if len(production) == 2:
                left_variable = production[0]  # First variable (like A in S -> AB)
                right_variable = production[1]  # Second variable (like B in S -> AB)
                
                # Try splitting the target string in all possible ways
                # Example: "abc" can be split as "a"+"bc" or "ab"+"c"
                for split_point in range(1, len(target_string)):
                    left_part = target_string[:split_point]   # First part
                    right_part = target_string[split_point:]  # Second part
                    
                    # Calculate how many steps each part needs
                    left_steps = self._calculate_steps_needed(left_variable, left_part)
                    right_steps = self._calculate_steps_needed(right_variable, right_part)
                    
                    # If either part is impossible, skip this split
                    if left_steps < 0 or right_steps < 0:
                        continue
                    
                    # Total steps = 1 (for this binary rule) + steps for left + steps for right
                    total_steps_needed = 1 + left_steps + right_steps
                    
                    # Check if we have enough steps
                    if total_steps_needed > steps_remaining:
                        continue
                    
                    # Try to derive left part from left variable, right part from right variable
                    if (self._try_to_derive(left_variable, left_part, left_steps) and
                        self._try_to_derive(right_variable, right_part, right_steps)):
                        # Success! We found a way to derive the string
                        self.cache[cache_key] = True
                        return True
        
        # If we get here, we couldn't derive the string
        self.cache[cache_key] = False
        return False
    
    def _calculate_steps_needed(self, variable: str, string_part: str) -> int:
        """
        Calculate the exact number of steps needed to derive string_part from variable.
        
        Uses the CNF property that any derivation of a string of length k ≥ 1
        requires exactly 2k - 1 steps. For epsilon (empty string), requires
        1 step if the variable can produce epsilon directly.
        
        Args:
            variable (str): The variable to derive from (like 'S' or 'A').
            string_part (str): The string to produce. Can be empty for epsilon.
        
        Returns:
            int: Number of steps needed:
                - For empty string: 1 if variable can produce epsilon, else -1
                - For string of length k: 2k - 1
                - Returns -1 if derivation is impossible (empty string but
                  variable cannot produce epsilon)
        
        Example:
            >>> tester._calculate_steps_needed('S', 'ab')
            3  # 2*2 - 1 = 3
            >>> tester._calculate_steps_needed('A', '')
            1  # If A can produce epsilon
            >>> tester._calculate_steps_needed('B', '')
            -1  # If B cannot produce epsilon
        
        Note:
            This is a helper method used by _try_to_derive() to determine
            how to distribute steps between left and right parts of a binary
            rule application.
        """
        if len(string_part) == 0:
            # Empty string - need 1 step if variable can produce epsilon
            if self._can_derive_epsilon(variable):
                return 1
            else:
                return -1  # Impossible
        else:
            # For string of length k, need 2k - 1 steps
            return 2 * len(string_part) - 1


def test_membership(grammar: Grammar, string: str) -> bool:
    tester = MembershipTester(grammar)
    return tester.test_membership(string)


# ============================================================================
# FEASIBILITY ESTIMATOR
# ============================================================================

# Rough estimate: how many operations can we do per second?
# This is a conservative guess - actual speed depends on your computer
OPERATIONS_PER_SECOND = 1000000  # 1 million operations per second


def estimate_worst_case_operations(grammar: Grammar, string_length: int) -> int:
    """
    Estimate the worst-case number of operations for membership testing.
    
    Calculates an upper bound on the number of operations the naive membership
    algorithm might perform for a string of given length. The estimate accounts
    for the exponential nature of the brute force algorithm.
    
    Complexity:
        The algorithm has exponential worst-case complexity. For a string of
        length n with b binary rules, the estimate is roughly:
        (b * (n-1))^(2n-1) operations
    
    Args:
        grammar (Grammar): The grammar to analyze. The number of binary rules
                          affects the estimate significantly.
        string_length (int): Length of the string to test. Must be non-negative.
    
    Returns:
        int: Estimated number of operations. Returns:
            - 1 for empty string (very fast)
            - Linear for grammars with no binary rules
            - Exponential estimate for longer strings with binary rules
            - Capped at 10^18 to avoid integer overflow
    
    Example:
        >>> grammar = parse_grammar_file("grammar.txt")
        >>> estimate_worst_case_operations(grammar, 0)
        1
        >>> estimate_worst_case_operations(grammar, 5)
        3125  # Example value
        >>> estimate_worst_case_operations(grammar, 20)
        1000000000000000000  # Capped at 10^18
    
    Note:
        This is a rough upper bound estimate. Actual performance may vary
        significantly based on the specific grammar structure and string.
        The estimate assumes worst-case branching at every step.
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
    Determine if membership testing is feasible for a given string length.
    
    Evaluates whether the naive membership algorithm can complete within
    1 minute for a string of the specified length. Uses conservative
    heuristics and worst-case operation estimates.
    
    Feasibility Criteria:
        - Empty string (length 0): Always feasible
        - Single character (length 1): Always feasible
        - Length > 20: Always infeasible (threshold)
        - Many binary rules + long string: Infeasible
        - Otherwise: Based on estimated operations vs. time limit
    
    Args:
        grammar (Grammar): The grammar to test. Number of binary rules
                          significantly affects feasibility.
        string_length (int): Length of the string to test. Must be non-negative.
    
    Returns:
        Tuple[bool, str]: A tuple containing:
            - bool: True if algorithm should complete within 1 minute,
                   False if it will likely exceed 1 minute
            - str: Human-readable explanation of the decision, including
                  estimated time if calculated
    
    Example:
        >>> grammar = parse_grammar_file("grammar.txt")
        >>> feasible, reason = is_feasible(grammar, 5)
        >>> print(f"Feasible: {feasible}")
        >>> print(f"Reason: {reason}")
        Feasible: True
        Reason: Estimated worst-case time: 0.0026 seconds (within 60 seconds)
    
    Note:
        Uses OPERATIONS_PER_SECOND constant (1 million ops/sec) for time
        estimation. This is a conservative estimate and actual performance
        may vary based on hardware and grammar structure.
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


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

def cmd_check_cnf(args) -> int:
    """
    Command handler for checking if a grammar is in CNF.
    
    Parses the grammar file and validates whether it conforms to Chomsky
    Normal Form requirements. Prints YES/NO result and explanation.
    
    Args:
        args: Argument object from argparse containing:
            - grammar_file (str): Path to the grammar file to check
    
    Returns:
        int: Exit code:
            - 0 if grammar is valid CNF
            - 1 if grammar is not CNF or parsing fails
    
    Output:
        Prints to stdout:
            - "YES" if grammar is CNF, followed by confirmation message
            - "NO" if grammar is not CNF, followed by error explanation
    """
    is_cnf_result, message = check_cnf_file(args.grammar_file)
    
    if is_cnf_result:
        print("YES")
        print("The grammar is in Chomsky Normal Form.")
    else:
        print("NO")
        print(f"Reason: {message}")
    
    return 0 if is_cnf_result else 1


def cmd_test_membership(args) -> int:
    """
    Command handler for testing string membership in a grammar.
    
    Parses the grammar file, validates it's in CNF, and tests whether the
    given string can be generated by the grammar. Handles epsilon testing
    via special string values.
    
    Args:
        args: Argument object from argparse containing:
            - grammar_file (str): Path to the grammar file
            - string (str): String to test. Use "epsilon" or "ε" for empty string
    
    Returns:
        int: Exit code:
            - 0 if command executed successfully (regardless of membership result)
            - 1 if grammar parsing fails or grammar is not CNF
    
    Output:
        Prints to stdout:
            - "YES" if string belongs to grammar, followed by confirmation
            - "NO" if string does not belong, followed by rejection message
            - Error messages if grammar is invalid or not CNF
    
    Note:
        Requires the grammar to be in CNF. Will return error if grammar
        is not CNF-compliant.
    """
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


def cmd_estimate(args) -> int:
    """
    Command handler for estimating algorithm feasibility.
    
    Parses the grammar file and estimates whether the membership testing
    algorithm can complete within 1 minute for a string of the given length.
    
    Args:
        args: Argument object from argparse containing:
            - grammar_file (str): Path to the grammar file
            - string_length (str): String length to estimate for (will be
                                  converted to int)
    
    Returns:
        int: Exit code:
            - 0 if command executed successfully
            - 1 if grammar parsing fails or string_length is invalid
    
    Output:
        Prints to stdout:
            - "YES" if feasible (should complete within 1 minute)
            - "NO" if infeasible (will likely exceed 1 minute)
            - Explanation message with estimated time or reason
    
    Raises:
        ValueError: If string_length cannot be converted to integer
    """
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


def main() -> int:
    """
    Main entry point for the CNF Grammar Analyzer command-line interface.
    
    Sets up argument parsing for three commands:
    1. check_cnf: Validate if grammar is in CNF
    2. test_membership: Test if string belongs to grammar
    3. estimate: Estimate feasibility for string length
    
    Returns:
        int: Exit code:
            - 0 on success
            - 1 on error or if no command provided
    
    Example:
        Called automatically when script is run:
        $ python3 AIO.py check_cnf grammar.txt
        $ python3 AIO.py test_membership grammar.txt ab
        $ python3 AIO.py estimate grammar.txt 10
    """
    parser = argparse.ArgumentParser(
        description='CNF Grammar Analyzer - All-In-One',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 AIO.py check_cnf grammar.txt
  python3 AIO.py test_membership grammar.txt 1010
  python3 AIO.py estimate grammar.txt 10
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

