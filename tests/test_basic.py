import pytest

from thermocalculator import parse


def test_parser():
    """Test chemical formula parser
    """
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
        CP = parse.ChemParser()
        output = CP.atoms(formula, stack=[{}], debug=False)
        err_msg = (f'Expected\n{expected_output}\n'
                   f'as output of\n"{formula}"\n'
                   f'but instead got\n{output}')
        assert (output == expected_output), err_msg