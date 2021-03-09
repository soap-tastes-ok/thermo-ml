
"""
C*1 + O*1 + O*1 + (C*1 + (C*1 + H*3)*2)*3 + C*1 + H*3

[{'H': 22, 'C': 11, 'O': 2}]
"""

import re


class ChemParser:
    def __init__(self):
        """Parse chemical formula into atoms and corresponding stoichiometric numbers.
        """
        # Regular expressions for numbers
        regex_num = r'(\d+(?:\.\d+)?)' # optional numbers (e.g. 6.4, 6)
        #regex_num = r'(\d+\.\d+|\d+\.|\d+)' # optional numbers (e.g. 6.4, 6., 6)
        regex_num_optional = regex_num + r'?' # '?' means optional
        regex_num_at_end   = regex_num + r'$' # '$' means at end of string
        regex_num_at_start = r'^' + regex_num # '^' means at beginning of string
        # Regular expressions for atoms
        regex_atom = r'([A-Z]{1}[a-z]{0,1})' + regex_num_optional # atoms 'He', 'N2', 'H3.2', etc.
    
        # Regular expression for left delimiter, which can contain
        # brackets (e.g. '(', '['), a number (e.g. 3, 6.4) and 
        # a connecting dot (e.g. '•'). Some examples include;
        # ['•H20', '3H20', '(H2O)2', '•3H20', '•(H20)', '•3(H20)', '3(H20)']
        regex_dot = r'(\•|\∙|\·)'
        regex_left_paran = r'(\[|\()'
        _regex_dot = r'(?:\•|\∙|\·)' # '?:' means non capturing group 
        _regex_num = r'(?:\d+\.\d+|\d+\.|\d+)' # '?:' means non capturing group
        _regex_left_paran = r'(?:\[|\()' # '?:' means non capturing group
        regex_left_delimiter = r'|'.join([
            r'('+_regex_dot+_regex_num+_regex_left_paran+')', # dot number parantheses
            r'('+_regex_num+_regex_left_paran+')', # number parantheses
            r'('+_regex_dot+_regex_left_paran+')', # dot parantheses
            r'('+_regex_dot+_regex_num+')', # dot number
            regex_dot, # dot
            regex_num, # number
            regex_left_paran,  # parantheses
            ])

        # Regular expressions for right delimiter
        #regex_left_parantheses  = regex_num_optional + r'(\[|\()' # left-parantheses '('
        regex_right_delimiter = r'(\]|\))' + regex_num_optional # right-parantheses w/ optional number ')', ')3', etc
        #regex_dot_separator = r'(\•|\∙|\·){1}' + regex_num_optional # dot w/ optional number '•4', in '•4H2O'
        
        # Compile all regex into regex object to perform pattern matching
        self.re_atom = re.compile(regex_atom)
        self.re_num  = re.compile(regex_num)
        self.re_num_at_end = re.compile(regex_num_at_end)
        self.re_num_at_start = re.compile(regex_num_at_start)
        self.re_left  = re.compile(regex_left_delimiter)
        self.re_right = re.compile(regex_right_delimiter)
        self.re_left_paran = re.compile(regex_left_paran)
        #self.re_dot   = re.compile(regex_dot_separator)
        # Multiple for counts (e.g. 8 for '•8(H2O)', 2 for '2(SiO2)')
        self._multiple = 1.0
        
    def atoms(self, formula, debug=False, stack=[{}], n_open_parantheses=0):
        """Parse chemical formula into atoms and corresponding stoichiometric numbers.
        
        Based on Extended Backus-Naur Formalism (EBNF).
        https://www.garshol.priv.no/download/text/bnf.html

        Args:
            formula (str): chemical formula (e.g. 'COOH(C(CH3)2)3CH3')
            debug (bool, optional): [description]. Defaults to False.
            stack (list, optional): 
                list of dictionaries { 'atom name': int, ... }. 
                Defaults to [].
            n_open_parantheses (int, optional): [description]. Defaults to 0.
                Number of left-paranthesess that have been opened
                and not yet closed.
            atom (str, optional): string equivalent of 
                RE matching atom name including an
                optional number 'He', 'N2', 'H3', etc.
            ldel (regexp, optional): string equivalent of 
                RE matching the left-parantheses '('.
                Defaults to r'<pass>'.
            rdel (regexp, optional): string equivalent of 
                RE matching the right-parantheses 
                including an optional number ')', ')3', etc.
                Defaults to r'<pass>'.

        Returns:
            list of dicts: e.g. [{'C': 11, 'H': 22, 'O': 2}]
        """
        # Base case
        if not isinstance(formula, str):
            err_msg = ('Expected formula to be of string type,'
                    f'instead got {type(formula)}')
            raise ValueError(err_msg)
        if len(formula) == 0:
            err_msg = (f'Expected length of formula to be > 0'
                    f'instead got {len(formula)}')
            raise ValueError(err_msg)
        
        # Test match
        match_atom  = self.re_atom.match(formula)
        match_left  = self.re_left.match(formula)
        match_right = self.re_right.match(formula)

        # Atom with optional number
        if match_atom:
            # Split match with the rest
            atom, num, tail = self.extract_atoms(formula)
            # Add this atom to record (i.e. dictionary)
            if atom in stack[-1]:
                # atom already exists, so increment occurence
                stack[-1][atom] += num * self._multiple
            else:
                # new atom found, so record new occurance
                stack[-1][atom]  = num * self._multiple
            # Debug
            if debug:
                print(f'atom={atom}, num={num}, tail={tail}')
                print(f'--> stack={stack}')

        # Left-parantheses
        elif match_left:
            # Split match with the rest
            left_delim, tail, contains_left_paranthesis = self.extract_left_delimiter(formula)
            # Update count
            if contains_left_paranthesis:
                n_open_parantheses += 1
                # Add a new dictionary to stack
                stack.append({}) # will be popped from stack by next right-parantheses
            # Debug
            if debug:
                print(f'Left parantheses = "{left_delim}"')
                print(f'--> stack={stack}')

        # Right-parantheses followed by an optional number (default is 1).
        elif match_right:
            # Split match with the rest
            right_delim, num, tail = self.extract_right_delimiter(formula)
            # Base case
            if (self._multiple > 1.0) and (num > 1.0):
                Exception('Got multiples before & after paranthesis;'
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
            # Debug
            if debug:
                print(f'Right parantheses = "{right_delim}"')
                print(f'--> stack={stack}')

        # # A dot w/ optional number '•4', in '•4H2O'
        # elif match_dot:
        #     # Split match with the rest
        #     dot, num, tail = self.extract_dot(formula)
        #     # Debug
        #     if debug:
        #         print(f'Dot separator = "{dot}"')
        #         print(f'--> stack={stack}')
        
        # Wrong syntax.
        else:
            raise SyntaxError(f'The head of "{formula}" does not match any regex')
        
        # The formula has not been consumed yet. Continue recursive parsing.
        if len(tail) > 0:
            return self.atoms(tail, debug, stack, n_open_parantheses)

        # Nothing left to parse. Stop recursion.
        else:
            # Base case
            if n_open_parantheses > 0:
                raise SyntaxError(f'Unmatched left parentheses in "{formula}"')
            # Debug
            if debug:
                print(f'Stack={stack[-1]}')
                print(f'--> stack={stack}')
            return stack
        
    def extract_number(self, formula):
        """Example: 'H3' --> 'H', '3'

        Args:
            formula (str): string with 
                optional trailing number
                (e.g. 'C4', ')2', etc).

        Returns:
            [type]: [description]
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
            
    def extract_atoms(self, formula):
        """Example: 'COOH(C(CH3)2)3CH3' --> 'C', '1', 'OOH(C(CH3)2)3CH3'

        Args:
            formula (str): chemical formula
                (e.g. 'COOH(C(CH3)2)3CH3')

        Returns:
            [str, int, str]: atom, its count
                and the remaining string.
        """
        # Test match
        match_atom  = self.re_atom.match(formula)
        # Base case (formula doesn't start with atom)
        if not match_atom:
            return None, None, None
        # Split match from the rest
        atom = formula[:match_atom.end() ]
        tail = formula[ match_atom.end():]
        # Split trailing number from atom (else, num = 1)
        atom, num = self.extract_number(atom)
        return atom, num, tail
    
    # def extract_dot(self, formula):
    #     # Test match
    #     match_dot = self.re_dot.match(formula)
    #     # Split match from the rest
    #     dot = formula[:match_dot.end() ]
    #     tail = formula[ match_dot.end():]
    #     # Split dot with trailing number if any
    #     dot, num = self.extract_number(dot)
    #     # Store number following the dot
    #     self._multiple = num or 1.0
    #     return dot, num, tail
    
    def extract_left_delimiter(self, formula):
        """E.g. '(C(CH3)2)3CH3' --> '(', 'C(CH3)2)3CH3'

        Args:
            formula (str): chemical formula
                (e.g. '(C(CH3)2)3CH3')

        Returns:
            [bool, str]: whether the delimiter
                contains a left parantheses,
                and the remaining string.
        """
        # Test match
        match_left  = self.re_left.match(formula)
        # Base case (formula doesn't start with atom)
        if not match_left:
            return None, None
        # Split match from the rest
        left_delim = formula[:match_left.end() ]
        tail       = formula[ match_left.end():]
        # If parantheses in left delimiter, take note
        if self.re_left_paran.search(left_delim):
            contains_left_paranthesis = True
        else:
            contains_left_paranthesis = False
        # Get number in the left delimiter, if any
        if self.re_num.search(left_delim):
            self._multiple = float(self.re_num.search(left_delim).group())
        else:
            self._multiple = 1.0
        return left_delim, tail, contains_left_paranthesis
    
    def extract_right_delimiter(self, formula):
        """E.g. ')2)3CH3' --> ')', '2', ')3CH3'
        
        Args:
            formula ([type]): [description]

        Returns:
            [type]: [description]
        """
        # Test match
        match_right = self.re_right.match(formula)
        # Base case (formula doesn't start with atom)
        if not match_right:
            return None, None, None
        # Split match from the rest
        right_delim = formula[:match_right.end() ]
        tail        = formula[ match_right.end():]
        # Split trailing number from atom (else, num = 1)
        right_delim, num = self.extract_number(right_delim)
        return right_delim, num, tail

# %%
# formula = 'COOH[C[CH3]2]3CH3'
# formula = 'Ca7Si16O38(OH)2'
# formula = 'Ca3Si6O15·7H2O'
# formula = 'Ca9Si16O40(OH)2·14H2O'
# formula = 'Ca6.4(H0.6Si2O7)2(OH)2'
# formula = '(NH4)3PO4'
# formula = 'Ca2SiO3(OH)2'
formula = 'CaO·2(H2O)'
CP = ChemParser()
CP.atoms(formula, stack=[{}], debug=False)

# %%
def test_parser():
    # Test data
    dict_data = {
        'CaO·H2O':  [{'Ca': 1.0, 'O': 2.0, 'H': 2.0}],
        'CaO·1H2O': [{'Ca': 1.0, 'O': 2.0, 'H': 2.0}],
        'CaO·2H2O': [{'Ca': 1.0, 'O': 3.0, 'H': 4.0}],
        'CaO·2(H2O)': [{'Ca': 1.0, 'O': 3.0, 'H': 4.0}],
        '2(CaO)·2(H2O)': [{'Ca': 2.0, 'O': 4.0, 'H': 4.0}],
        '2(CaO)·2(SiO2)·2(H2O)': [{'Ca': 2.0, 'Si': 2.0, 'O': 8.0, 'H': 4.0}],
        'COOH[C[CH3]2]3CH3': [{'C': 11.0, 'O': 2.0, 'H': 22.0}],
        'Ca2SiO3(OH)2': [{'Ca': 2.0, 'Si': 1.0, 'O': 5.0, 'H': 2.0}],
        'Ca7Si16O38(OH)2': [{'Ca': 7.0, 'Si': 16.0, 'O': 40.0, 'H': 2.0}],
        'Ca6.4(H0.6Si2O7)2(OH)2': [{'Ca': 6.4, 'H': 3.2, 'Si': 4.0, 'O': 16.0}],
        'Ca9Si6O18(OH)6·8H2O': [{'Ca': 9.0, 'Si': 6.0, 'O': 32.0, 'H': 22.0}],
        'Ca9Si6O18(OH)6·8(H2O)': [{'Ca': 9.0, 'Si': 6.0, 'O': 32.0, 'H': 22.0}]
    }
    # Make sure all produce expected results
    for formula, expected_output in dict_data.items():
        CP = ChemParser()
        output = CP.atoms(formula, stack=[{}], debug=False)
        err_msg = (
            f'Expected\n{expected_output}\n'
            f'as output of\n"{formula}"\n'
            f'but instead got\n{output}'
        )
        assert (output == expected_output), err_msg

test_parser()

#%%
