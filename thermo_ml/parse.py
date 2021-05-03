import re

### Regular expressions for numbers
REGEX_NUM = r'(\d+(?:\.\d+)?)' # optional numbers (e.g. 6.4, 6)
#REGEX_NUM = r'(\d+\.\d+|\d+\.|\d+)' # optional numbers (e.g. 6.4, 6., 6)
REGEX_NUM_OPTIONAL = REGEX_NUM + r'?' # '?' means optional
REGEX_NUM_AT_END   = REGEX_NUM + r'$' # '$' means at end of string
REGEX_NUM_AT_START = r'^' + REGEX_NUM # '^' means at beginning of string

### Regular expressions for atoms
REGEX_ATOM = r'([A-Z]{1}[a-z]{0,1})' + REGEX_NUM_OPTIONAL # atoms 'He', 'N2', 'H3.2', etc.

### Regular expression for left delimiter, which can contain
#   brackets (e.g. '(', '['), a number (e.g. 3, 6.4) and 
#   a connecting dot (e.g. '•'). Some examples include;
#   ['•H20', '3H20', '(H2O)2', '•3H20', '•(H20)', '•3(H20)', '3(H20)']
REGEX_DOT = r'(\•|\∙|\·)'
REGEX_LEFT_PARAN = r'(\[|\()'
_REGEX_DOT = r'(?:\•|\∙|\·)' # '?:' means non capturing group 
_REGEX_NUM = r'(?:\d+\.\d+|\d+\.|\d+)' # '?:' means non capturing group
_REGEX_LEFT_PARAN = r'(?:\[|\()' # '?:' means non capturing group
REGEX_LEFT_DELIMITER = r'|'.join([
    r'('+_REGEX_DOT+_REGEX_NUM+_REGEX_LEFT_PARAN+')', # dot number parantheses
    r'('+_REGEX_NUM+_REGEX_LEFT_PARAN+')', # number parantheses
    r'('+_REGEX_DOT+_REGEX_LEFT_PARAN+')', # dot parantheses
    r'('+_REGEX_DOT+_REGEX_NUM+')', # dot number
    REGEX_DOT, # dot
    REGEX_NUM, # number
    REGEX_LEFT_PARAN,  # parantheses
    ])

### Regular expressions for right delimiter
#regex_left_parantheses  = REGEX_NUM_OPTIONAL + r'(\[|\()' # left-parantheses '('
REGEX_RIGHT_DELIMITER = r'(\]|\))' + REGEX_NUM_OPTIONAL # right-parantheses w/ optional number ')', ')3', etc
#regex_dot_separator = r'(\•|\∙|\·){1}' + REGEX_NUM_OPTIONAL # dot w/ optional number '•4', in '•4H2O'


def atoms(chemical_formula):
    """Parse chemical formula into atoms and corresponding stoichiometric numbers.

    Based on Extended Backus-Naur Formalism (EBNF).
    https://www.garshol.priv.no/download/text/bnf.html

    Args:
        chemical_formula (str): chemical formula (e.g. 'COOH(C(CH3)2)3CH3')
    
    Returns:
        dict: Dictionary where key=atom and value=count.
    """
    # Get atom counts
    CP = ChemParser()
    stack = CP.atoms(chemical_formula, stack=[{}])
    # Error case
    if len(stack) != 1:
        raise Exception(
            f'Parsing unsuccessful for "{chemical_formula}"'
            'Please contact bundes_liga.atok@hotmail.co.jp \n'
            'Output = {stack}')
    dict_of_atom_counts = stack[0]
    return dict_of_atom_counts


class ChemParser:
    def __init__(self):
        """Parse chemical formula into atoms and corresponding stoichiometric numbers.
        """
        # Compile all regex into regex object to perform pattern matching
        self.re_atom = re.compile(REGEX_ATOM)
        self.re_num  = re.compile(REGEX_NUM)
        self.re_num_at_end = re.compile(REGEX_NUM_AT_END)
        self.re_num_at_start = re.compile(REGEX_NUM_AT_START)
        self.re_left  = re.compile(REGEX_LEFT_DELIMITER)
        self.re_right = re.compile(REGEX_RIGHT_DELIMITER)
        self.re_left_paran = re.compile(REGEX_LEFT_PARAN)
        #self.re_dot   = re.compile(regex_dot_separator)
        # Multiple for counts (e.g. 8 for '•8(H2O)', 2 for '2(SiO2)')
        self._multiple = 1.0
        
    def atoms(self, formula, stack=[{}], n_open_parantheses=0):
        """Parse chemical formula into atoms and corresponding stoichiometric numbers.
        
        Based on Extended Backus-Naur Formalism (EBNF).
        https://www.garshol.priv.no/download/text/bnf.html

        Args:
            formula (str): chemical formula (e.g. 'COOH(C(CH3)2)3CH3')
            stack (list, optional): 
                list of dictionaries { 'atom name': int, ... }. 
                Defaults to [].
            n_open_parantheses (int, optional): [description]. Defaults to 0.
                Number of left-paranthesess that have been opened
                and not yet closed.
            atom (str, optional): string equivalent of 
                RE matching atom name including an
                optional number 'He', 'N2', 'H3', etc.
            ldel (regex, optional): string equivalent of 
                RE matching the left-parantheses '('.
                Defaults to r'<pass>'.
            rdel (regex, optional): string equivalent of 
                RE matching the right-parantheses 
                including an optional number ')', ')3', etc.
                Defaults to r'<pass>'.

        Returns:
            list of dicts: e.g. [{'C': 11, 'H': 22, 'O': 2}]
        """
        ### Assert formula argument is string and has length
        self._assert_input_format(formula)
        ### Parse head/beginning of formula using regex
        tail, stack, n_open_parantheses = self._parse_head_of_formula(
            formula, stack, n_open_parantheses)
        ### Check whether formula has been consumed yet
        if len(tail) > 0: # Continue recursive parsing.
            return self.atoms(tail, stack, n_open_parantheses)
        else: # Nothing left to parse. Stop recursion.
            # Base case
            if n_open_parantheses > 0:
                raise SyntaxError(f'Unmatched left parentheses in "{formula}"')
            return stack

    def _assert_input_format(self, formula: str):
        """Assert argument is string and has length

        Args:
            formula (str): Chemical formula

        Raises:
            ValueError: Must be string
            ValueError: Length must be > 0
        """
        if not isinstance(formula, str):
            err_msg = ('Expected formula to be of string type,'
                    f'instead got {type(formula)}')
            raise ValueError(err_msg)
        if len(formula) == 0:
            err_msg = (f'Expected length of formula to be > 0'
                    f'instead got {len(formula)}')
            raise ValueError(err_msg)

    def _parse_head_of_formula(self, formula, stack, n_open_parantheses):
        """Parse left end of formula using regex

        Args:
            formula (str): Chemical formula
                (e.g. '(C(CH3)2)3CH3')
            stack (list): List of dictionaries
                used to keep track of parsed atoms.
            n_open_parantheses (int): Number of
                open parantheses (No. of left 
                parantheses - No. of right
                parantheses).

        Raises:
            SyntaxError: Left end of formula doesn't match with any pattern

        Returns:
            str: Remains of the formula
            list: Updated "stack"
            int: Updated "n_open_parantheses"
        """
        ### Evaluate match
        match_atom  = self.re_atom.match(formula)
        match_left  = self.re_left.match(formula)
        match_right = self.re_right.match(formula)
        ### Split formula based on match
        if match_atom: # Atom with optional number
            tail, stack, = self._update_stack_with_found_atoms(formula, stack)
        elif match_left: # Left-parantheses
            tail, stack, n_open_parantheses = self._update_stack_with_left_delim(
                formula, stack, n_open_parantheses)
        elif match_right: # Right-parantheses followed by an optional number
            tail, stack, n_open_parantheses = self._update_stack_with_right_delim(
                formula, stack, n_open_parantheses)
        else: # Wrong syntax
            raise SyntaxError(f'The left end of "{formula}" does not match any regex')
        return tail, stack, n_open_parantheses

    def _update_stack_with_found_atoms(self, formula: str, stack: list):
        """Update stack when an atom is found at beginning of 'formula'

        Args:
            formula (str): Chemical formula
                (e.g. 'H3)2)3CH3').
            stack (list): List of dictionaries
                used to keep track of parsed atoms.

        Returns:
            str: Remains of the formula
            list: Updated "stack"
        """
        # Split match with the rest
        atom, num, tail = self._extract_atoms(formula)
        if atom in stack[-1]:
                # atom already exists, so increment occurence
            stack[-1][atom] += num * self._multiple
        else:
                # new atom found, so record new occurance
            stack[-1][atom]  = num * self._multiple
        return tail, stack

    def _update_stack_with_left_delim(self, formula, stack, n_open_parantheses):
        """Update stack when left delimiter is found at beginning of 'formula'

        Args:
            formula (str): Chemical formula
                (e.g. '(CH3)2)3CH3').
            stack (list): List of dictionaries
                used to keep track of parsed atoms.
            n_open_parantheses (int): Number of
                open parantheses (No. of left 
                parantheses - No. of right
                parantheses).

        Returns:
            str: Remains of the formula
            list: Updated "stack"
            int: Updated "n_open_parantheses"
        """
        # Split match with the rest
        left_delim, tail, contains_left_paranthesis = self._extract_left_delimiter(formula)
        # Update count
        if contains_left_paranthesis:
            n_open_parantheses += 1
            # Add a new dictionary to stack
            stack.append({}) # will be popped from stack by next right-parantheses
        return tail, stack, n_open_parantheses
        
    def _update_stack_with_right_delim(self, formula, stack, n_open_parantheses):
        """Update stack when right delimiter is found at beginning of 'formula'

        Args:
            formula (str): Chemical formula
                (e.g. '(C(CH3)2)3CH3').
                It can be from the middle
                (e.g. ')2)3CH3').
            stack (list): List of dictionaries
                used to keep track of parsed atoms.
            n_open_parantheses (int): Number of
                open parantheses (No. of left 
                parantheses - No. of right
                parantheses).

        Raises:
            SyntaxError: Found numbers before & after paranthesis (e.g. '2)3')
            SyntaxError: Unmatched right parentheses

        Returns:
            str: Remains of the formula
            list: Updated "stack"
            int: Updated "n_open_parantheses"
        """
        right_delim, num, tail = self._extract_right_delimiter(formula)
        # Base case
        if (self._multiple > 1.0) and (num > 1.0):
            raise SyntaxError('Found numbers before & after paranthesis;'
                          f'formula = {formula}'
                          f'before = {self._multiple}, after = {num}')
        # Update count
        n_open_parantheses -= 1
        # Base case
        if n_open_parantheses < 0:
            raise SyntaxError(f'Unmatched right parentheses in "{formula}"')
        # Take out the atom counts inside this parantheses
        dict_inside_paranthesis = stack.pop()
        # Merge the counts to the atom counts before the paratheses
        for (atom, count) in dict_inside_paranthesis.items():
            if atom in stack[-1]:
                    # increment occurence
                stack[-1][atom] += count * num
            else:
                    # record new occurance
                stack[-1][atom]  = count * num
        return tail, stack, n_open_parantheses
        
    def _extract_number(self, formula):
        """Example: 'H3' --> 'H', '3'

        Args:
            formula (str): string with 
                optional heading/trailing number
                (e.g. 'C4', ')2', '2H', etc).

        Returns:
            [str, float]: String and number if any
        """
        # See if match ends with a number
        match_num_at_start = self.re_num_at_start.search(formula)
        match_num_at_end   = self.re_num_at_end.search(formula)
        if match_num_at_start:
            # Split into number & string (e.g. '2(' --> '2', '(')
            string = formula[ match_num_at_start.end():]
            number = formula[:match_num_at_start.end() ]
        elif match_num_at_end:
            # Split into atom & number (e.g. 'H2' --> 'H', '2')
            string = formula[:match_num_at_end.start() ]
            number = formula[ match_num_at_end.start():]
        else:
            # Else num = 1 (e.g. 'C' --> 'C' & '1')
            string = formula
            number = 1.0
        return string, float(number)
            
    def _extract_atoms(self, formula):
        """Example: 'COOH(C(CH3)2)3CH3' --> 'C', '1', 'OOH(C(CH3)2)3CH3'

        Args:
            formula (str): chemical formula
                (e.g. 'COOH(C(CH3)2)3CH3')

        Returns:
            [str, int, str]: atom, its count
                and the remaining string.
        """
        # Split match on the left with the rest (i.e. tail)
        atom, tail = self.__split_by_regex_match(formula, regex=self.re_atom)
        # Base case
        if not atom:
            return None, None, tail
        # Split trailing number from atom (else, num = 1)
        atom, num = self._extract_number(atom)
        return atom, num, tail
    
    def _extract_left_delimiter(self, formula):
        """E.g. '(C(CH3)2)3CH3' --> '(', 'C(CH3)2)3CH3'
        
        Exmaples of left delimiter:
            '(', '2(', '・(', '・2(', '・2'

        Args:
            formula (str): chemical formula
                (e.g. '(C(CH3)2)3CH3')

        Returns:
            [bool, str]: whether the delimiter
                contains a left parantheses,
                and the remaining string.
        """
        # Split match on the left with the rest (i.e. tail)
        left_delim, tail = self.__split_by_regex_match(formula, regex=self.re_left)
        # Base case
        if not left_delim:
            return None, tail, False
        # If parantheses in left delimiter, take note
        contains_left_paranthesis = bool(self.re_left_paran.search(left_delim))
        # Get number in the left delimiter, if any
        self._multiple = 1.0
        if self.re_num.search(left_delim):
            self._multiple = float(self.re_num.search(left_delim).group())
        return left_delim, tail, contains_left_paranthesis
    
    def _extract_right_delimiter(self, formula):
        """E.g. ')2)3CH3' --> ')', '2', ')3CH3'
        
        Args:
            formula ([type]): [description]

        Returns:
            [type]: [description]
        """
        # Split match on the left with the rest (i.e. tail)
        right_delim, tail = self.__split_by_regex_match(formula, regex=self.re_right)
        # Base case
        if not right_delim:
            return None, None, tail
        # Split trailing number from atom (else, num = 1)
        right_delim, num = self._extract_number(right_delim)
        return right_delim, num, tail
    
    def __split_by_regex_match(self, formula, regex):
        """Split formula by regex match

        Args:
            formula (str): chemical formula
                (e.g. 'COOH(C(CH3)2)3CH3')
            regex (re.Pattern): Compiled regex 
                string for matching pattern.
        
        Returns:
            [str, str]: Matched string and the rest (i.e. tail)
        """
        # Test match
        match_regex  = regex.match(formula)
        # Base case (formula doesn't start with atom)
        if not match_regex:
            return None, formula
        # Split match from the rest
        match = formula[:match_regex.end() ]
        tail  = formula[ match_regex.end():]
        return match, tail