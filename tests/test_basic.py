import pytest
import pandas as pd
from thermo_ml import parse, database


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
        output = CP.atoms(formula, stack=[{}])
        err_msg = (f'Expected\n{expected_output}\n'
                   f'as output of\n"{formula}"\n'
                   f'but instead got\n{output}')
        assert (output == expected_output), err_msg
        
        
def test_atomic_data():
    """Test atomic database"""
    ### Passing test inputs
    list_of_atoms = [
        ['H', 'C', 'Ca'],
        [1, 6, 20],
        ['Si', 'Zn', 'Cl'],
    ]
    list_of_properties = [
        ["Z", "Symbol", "Density (g/cm3)"],
        ["Z", "Symbol", "Density (g/cm3)"],
        ["Z", "Symbol", "Atomic weight (a.m.u.)"]
    ]
    
    list_of_expected_outputs = [
        pd.DataFrame({'Z': {0: 1, 5: 6, 19: 20},
                      'Symbol': {0: 'H', 5: 'C', 19: 'Ca'},
                      'Density (g/cm3)': {0: 0.0708, 5: 2.267, 19: 1.54}}),
        pd.DataFrame({'Z': {0: 1, 5: 6, 19: 20},
                      'Symbol': {0: 'H', 5: 'C', 19: 'Ca'},
                      'Density (g/cm3)': {0: 0.0708, 5: 2.267, 19: 1.54}}),
        pd.DataFrame({'Z': {13: 14, 16: 17, 29: 30},
                      'Symbol': {13: 'Si', 16: 'Cl', 29: 'Zn'},
                      'Atomic weight (a.m.u.)': {13: 28.0855, 16: 35.4527, 29: 65.3900}}),
    ]
    zipped = zip(list_of_atoms, list_of_properties, list_of_expected_outputs)
    
    # Assert
    for atoms, properties, expected_output in zipped:
        df_results = database.get_atoms(atoms, properties)
        # Raise error if output not as expected
        err_msg = ('DataFrame output was not as expected for:\n' +
                   f' atoms = {atoms}\n' + 
                   f' properties = {properties}.')
        assert df_results.equals(expected_output), err_msg
    
    ### Failing test inputs
    list_of_atoms = [
        [1, 'C', 'Ca'], 
        ['1', 'C', 'Ca'],
    ]
    list_of_properties = [
        ["Z", "Symbol", "Density (g/cm3)"],
        ["Z", "Symbol", "Density (g/cm3)"],
    ]
    zipped = zip(list_of_atoms, list_of_properties)
    
    # Assert they raise ValueError
    for atoms, properties in zipped:
        with pytest.raises(ValueError):
            df_results = database.get_atoms(atoms, properties)
            
            
            
# #%%

# #################################################
# import sys
# # Append our package to system environmental path
# packages = ['/Users/Shared/GitHub/thermo_ml']
# for package in packages:
#     if package not in sys.path:
#         sys.path.append(package)
# #################################################

# import pytest
# import pandas as pd
# from thermo_ml import parse, database


# ### Passing test inputs
# atoms = ['Si', 'Zn', 'Cl']
# properties = ["Z", "Symbol", "Atomic weight (a.m.u.)"]

# # Assert
# df_results = database.get_atoms(atoms, properties)
# df_results

# #%%
# expected_output = pd.DataFrame({'Z': {13: 14, 16: 17, 29: 30},
#                     'Symbol': {13: 'Si', 16: 'Cl', 29: 'Zn'},
#                     'Atomic weight (a.m.u.)': {13: 28.0855, 16: 35.4527, 29: 65.3900}})
# expected_output

# #%%
# # Raise error if output not as expected
# err_msg = ('DataFrame output was not as expected for:\n' +
#             f' atoms = {atoms}\n' + 
#             f' properties = {properties}.')
# assert df_results.equals(expected_output), err_msg

# # %%
# df_results.dtypes
# # %%
# expected_output.dtypes
# # %%



# #%%
# database.get_atoms([],[])
# # %%

# df_results["Atomic weight (a.m.u.)"].dtype
# # %%
