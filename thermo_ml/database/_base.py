#%%
from importlib import resources
import pandas as pd


DTYPES_PROPERTIES = {
    'Z': 'uint16',
    'Symbol': 'object',
    'Name': 'object',
    'Atomic weight (a.m.u.)': 'float64',
    'Density (g/cm3)': 'float64',
    'Solid-liquid-gas triple point  (MPa)': 'float64',
    'Solid-liquid-gas triple point  (C)': 'float64',
    'Melting point phase transition': 'object',
    'Melting point  (C)': 'float64',
    'Boiling point  (C)': 'float64',
    'Sublimation point (C)': 'float64',
    'Critical point  (C)': 'float64',
    'Specific heat (J/g K)': 'float64',
    'X_Allen_Pauling': 'float64',
    'Atomic radii (pm)': 'uint16',
    'Van der Waals radii (pm)': 'uint16',
    'Covalent radii (pm)': 'uint16',
    'Valence electrons': 'uint16',
    'Group': 'uint16',
    'Electron config - 1s': 'uint16',
    'Electron config - 2s': 'uint16',
    'Electron config - 2p': 'uint16',
    'Electron config - 3s': 'uint16',
    'Electron config - 3p': 'uint16',
    'Electron config - 3d': 'uint16',
    'Electron config - 4s': 'uint16',
    'Electron config - 4p': 'uint16',
    'Electron config - 4d': 'uint16',
    'Electron config - 4f': 'uint16',
    'Electron config - 5s': 'uint16',
    'Electron config - 5p': 'uint16',
    'Electron config - 5d': 'uint16',
    'Electron config - 5f': 'uint16',
    'Electron config - 6s': 'uint16',
    'Electron config - 6p': 'uint16',
    'Electron config - 6d': 'uint16',
    'Electron config - 7s': 'uint16',
    'Electron config - 7p': 'uint16',
    'Ionization energy (eV) - 1': 'float64',
    'Ionization energy (eV) - 2': 'float64',
    'Ionization energy (eV) - 3': 'float64',
    'Ionization energy (eV) - 4': 'float64',
    'Ionization energy (eV) - 5': 'float64',
    'Ionization energy (eV) - 6': 'float64',
    'Ionization energy (eV) - 7': 'float64',
    'Ionization energy (eV) - 8': 'float64',
    'Ionization energy (eV) - 9': 'float64',
    'Ionization energy (eV) - 10': 'float64',
    'Ionization energy (eV) - 11': 'float64',
    'Ionization energy (eV) - 12': 'float64',
    'Ionization energy (eV) - 13': 'float64',
    'Ionization energy (eV) - 14': 'float64',
    'Ionization energy (eV) - 15': 'float64',
    'Ionization energy (eV) - 16': 'float64',
    'Ionization energy (eV) - 17': 'float64',
    'Ionization energy (eV) - 18': 'float64',
    'Ionization energy (eV) - 19': 'float64',
    'Ionization energy (eV) - 20': 'float64',
    'Ionization energy (eV) - 21': 'float64'}

def get_fundamental_constants() -> pd.DataFrame():
    """Load fundamental constants of physics & chemistry
    
    Returns:
        pd.DataFrame: Fundamental constants
    """
    # Load file as binary data in RAM
    bytesio = resources.open_binary(
        package='thermo_ml.database.data', 
        resource='fundamental_constants.xls')
    # Convert binary data in RAM to dataframe
    df_constants = pd.read_excel(
        bytesio,
        engine=None,
        skiprows=4, 
        nrows=None,
        usecols='A:F',
        dtype=DTYPES_PROPERTIES)
    return df_constants

def get_atoms(atoms:str=None, 
              properties:str=None
              ) -> pd.DataFrame:
    """Get all atomic properties of all atoms

    Args:
        atoms (str|int|list, optional): 
            List of atomic numbers/atomic symbols
            for which to retrieve data. Use the
            "atoms" property of "Atoms" class
            to see the full list (e.g. Atoms().atoms).
            Defaults to None.
        properties (str|int|list, optional):
            List of atomic properties or its 
            integer index values to retrieve data.
            Use the "properties" property  of 
            "Atoms" class to see the full list
            (e.g. Atoms().properties).
            Defaults to None.
    Returns:
        pd.DataFrame: Atomic properties data
    """
    A = Atoms()
    return A.get_atoms(atoms, properties)

class Atoms:
    def __init__(self):
        self._df = self._load_data()
        self._df = self._rename_cols(self._df)
    
    @property
    def list_all_atoms(self) -> pd.DataFrame:
        """Table of atomic numbers and symbols
        
        Key = atomic number
        Value = atomic symbol

        Returns:
            pd.DataFrame: Atomic numbers and symbols
        """
        return self._df[['Z', 'Symbol']]
    
    @property
    def list_all_properties(self) -> pd.DataFrame:
        """Table of atomic properties and its interger indices

        Key = arbitrary integer index
        Value = atomic property

        Returns:
            pd.DataFrame: Atomic properties
        """
        cols = self._df.columns
        dict_of_atomic_properties = pd.Series(cols).to_dict()
        return pd.DataFrame(dict_of_atomic_properties.items(), 
                            columns=['Index', 'Property'])

    def get_atoms(self, 
                  atoms:str=None, 
                  properties:str=None
                  ) -> pd.DataFrame:
        """Load data of elements/atoms

        Args:
            atoms (str|int|list, optional): 
                List of atomic numbers/atomic symbols
                for which to retrieve data. Use the
                "atoms" class property to see 
                the full list (e.g. Atoms().atoms).
                Defaults to None.
            properties (str|int|list, optional):
                List of atomic properties or its 
                integer index values to retrieve data.
                Use the "properties" class property to 
                see the full list (e.g. Atoms().properties).
                Defaults to None.
        Returns:
            pd.DataFrame: Atomic properties data
        """
        # Convert to list if str or int
        atoms = _assert_list_type(atoms)
        properties = _assert_list_type(properties)
        # Check unique dtypes inside lists
        _assert_unique_dtype_in_list(atoms)
        _assert_unique_dtype_in_list(properties)
        # Check all values exist in database
        self._assert_all_values_exist(atoms, properties)
        # Prep data
        df = self._filter_data(self._df, atoms, properties)
        return df
    
    def _assert_all_values_exist(self, atoms, properties):
        """Make sure all user-specified values are valid

        Args:
            atoms (str|int|list, optional): 
                List of atomic numbers/atomic symbols
                for which to retrieve data. Use the
                "atoms" class property to see 
                the full list (e.g. Atoms().atoms).
                Defaults to None.
            properties (str|int|list, optional):
                List of atomic properties or its 
                integer index values to retrieve data.
                Use the "properties" class property to 
                see the full list (e.g. Atoms().properties).
                Defaults to None.

        Raises:
            ValueError: Specified atom doesn't exist
            ValueError: Specified property doesn't exist
        """
        ### Check atoms
        missing_atoms = []
        if atoms:
            if isinstance(atoms[0], str):
                # Take diff
                missing_atoms = self._take_diff(
                    list_all_vals=self._df["Symbol"],
                    list_vals=atoms)
            elif isinstance(atoms[0], int):
                # Take diff
                missing_atoms = self._take_diff(
                    list_all_vals=self._df["Z"],
                    list_vals=atoms)

        ### Check properties
        missing_props = []
        if properties:
            if isinstance(properties[0], str):
                # Take diff
                missing_props = self._take_diff(
                    list_all_vals=self._df.columns,
                    list_vals=properties)
            elif isinstance(properties[0], int):
                # Get integer index values of columns
                all_cols = self._df.columns
                all_cols_int = [all_cols.get_loc(c) for c in all_cols]
                # Take diff
                missing_props = self._take_diff(
                    list_all_vals=all_cols_int,
                    list_vals=properties)

        if missing_atoms:
            err_msg = f"Atom '{missing_atoms}' doesn't exist."
            raise ValueError(err_msg)
        if missing_atoms:
            err_msg = f"Property '{missing_props}' doesn't exist."
            raise ValueError(err_msg)
        return

    def _take_diff(self, list_all_vals:list, list_vals:list):
        # sourcery skip: inline-immediately-returned-variable
        """Take difference between two list-like objects

        Args:
            list_all_vals (list-like): List-like object containing all values
            list_vals (list-like): List-like object containing partial values

        Returns:
            list: List containing values that 
                didn't exist in "list_all_vals"
        """
        exist_in_both = set(list_all_vals) & set(list_vals)
        missing_vals = list(set(list_vals) - set(exist_in_both))
        return missing_vals
            
    @staticmethod
    def _load_data() -> pd.DataFrame:
        """Load atomic properties dataset

        Returns:
            pd.DataFrame: Data containing all
                atomic properties of all atoms.
        """
        binaryio = resources.open_binary(
            package='thermo_ml.database.data', 
            resource='atoms.xls')
        return pd.read_excel(
            binaryio, 
            sheet_name='Summary',
            skiprows=7,
            usecols='A:BG'
        )

    @staticmethod
    def _rename_cols(df:pd.DataFrame) -> pd.DataFrame:
        """Rename dataframe columns

        Args:
            df (pd.DataFrame): Atomic 
                properties data.

        Returns:
            pd.DataFrame: Atomic properties data
        """
        list_cols = df.columns.tolist()
        e_config_cols = list_cols[19:38]
        list_cols[19:38] = [f'Electron config - {e}' 
                            for e in e_config_cols]
        ioniz_cols = list_cols[38:59]
        list_cols[38:59] = [f'Ionization energy (eV) - {i}' 
                            for i in ioniz_cols]
        df.columns = list_cols
        return df

    @staticmethod
    def _filter_data(df:pd.DataFrame, 
                     atoms:list, 
                     properties:list
                     ) -> pd.DataFrame:
        """Filter atomic properties data

        Args:
            df (pd.DataFrame): Atomic 
                properties data.
            atoms (list): 
                List of atomic numbers/atomic symbols
                for which to retrieve data. Use the
                "atoms" class property to see 
                the full list (e.g. Atoms().atoms).
            properties (list):
                List of atomic properties or its 
                integer index values to retrieve data.
                Use the "properties" class property to 
                see the full list (e.g. Atoms().properties).

        Returns:
            pd.DataFrame: Dataset containing
                selected atomic properties 
                of selected atoms.
        """
        if atoms:
            if isinstance(atoms[0], str):
                mask_atoms = df["Symbol"].isin(atoms)
            elif isinstance(atoms[0], int):
                mask_atoms = df["Z"].isin(atoms)
            df = df.loc[mask_atoms]
        if properties:
            if isinstance(properties[0], str):
                df = df[properties]
            elif isinstance(properties[0], int):
                mask_properties = df.columns[properties]
                df = df.iloc[:, mask_properties]
        return df

def _assert_list_type(list_or_string):
    """Assert list type

    Args:
        list_or_string (any):
            If not list type,
            inserted into a list.
            E.g. "aaa" --> ["aaa"].
            If None, function also
            returns None.
    
    Returns:
        list|None: List-ified input,
            unless input is None.
    """
    list_ = list_or_string
    if isinstance(list_or_string, str):
        list_ = [list_or_string]
    return list_

def _assert_unique_dtype_in_list(list_of_something):
    """Assert unique dtype of list elements

    Args:
        list_of_something (list|None): Any list

    Raises:
        ValueError: More than one dtype in list
    """
    # Base case
    if not list_of_something:
        return
    unique_dtypes = {type(i) for i in list_of_something}
    if len(unique_dtypes) != 1:
        err_msg = (
            "Expected unique dtype inside list variable," + 
            f" instead got {unique_dtypes} in:" + 
            f"{list_of_something}.")
        raise ValueError(err_msg)
    

class Compounds:
    """To be developped"""



# #%%
# #################################################
# import sys
# # Append our package to system environmental path
# packages = ['/Users/Shared/GitHub/thermo_ml']
# for package in packages:
#     if package not in sys.path:
#         sys.path.append(package)
# #################################################



#%%
# # Key = atomic number, value = atomic symbol
# DICT_ATOMS = {
#     0: 'H',
#     1: 'He',
#     2: 'Li',
#     3: 'Be',
#     4: 'B',
#     5: 'C',
#     6: 'N',
#     7: 'O',
#     8: 'F',
#     9: 'Ne',
#     10: 'Na',
#     11: 'Mg',
#     12: 'Al',
#     13: 'Si',
#     14: 'P',
#     15: 'S',
#     16: 'Cl',
#     17: 'Ar',
#     18: 'K',
#     19: 'Ca',
#     20: 'Sc',
#     21: 'Ti',
#     22: 'V',
#     23: 'Cr',
#     24: 'Mn',
#     25: 'Fe',
#     26: 'Co',
#     27: 'Ni',
#     28: 'Cu',
#     29: 'Zn',
#     30: 'Ga',
#     31: 'Ge',
#     32: 'As',
#     33: 'Se',
#     34: 'Br',
#     35: 'Kr',
#     36: 'Rb',
#     37: 'Sr',
#     38: 'Y',
#     39: 'Zr',
#     40: 'Nb',
#     41: 'Mo',
#     42: 'Tc',
#     43: 'Ru',
#     44: 'Rh',
#     45: 'Pd',
#     46: 'Ag',
#     47: 'Cd',
#     48: 'In',
#     49: 'Sn',
#     50: 'Sb',
#     51: 'Te',
#     52: 'I',
#     53: 'Xe',
#     54: 'Cs',
#     55: 'Ba',
#     56: 'La',
#     57: 'Ce',
#     58: 'Pr',
#     59: 'Nd',
#     60: 'Pm',
#     61: 'Sm',
#     62: 'Eu',
#     63: 'Gd',
#     64: 'Tb',
#     65: 'Dy',
#     66: 'Ho',
#     67: 'Er',
#     68: 'Tm',
#     69: 'Yb',
#     70: 'Lu',
#     71: 'Hf',
#     72: 'Ta',
#     73: 'W',
#     74: 'Re',
#     75: 'Os',
#     76: 'Ir',
#     77: 'Pt',
#     78: 'Au',
#     79: 'Hg',
#     80: 'Tl',
#     81: 'Pb',
#     82: 'Bi',
#     83: 'Po',
#     84: 'At',
#     85: 'Rn',
#     86: 'Fr',
#     87: 'Ra',
#     88: 'Ac',
#     89: 'Th',
#     90: 'Pa',
#     91: 'U',
#     92: 'Np',
#     93: 'Pu',
#     94: 'Am',
#     95: 'Cm',
#     96: 'Bk',
#     97: 'Cf',
#     98: 'Es',
#     99: 'Fm',
#     100: 'Md',
#     101: 'No',
#     102: 'Lr',
#     103: 'Rf',
#     104: 'Ha',
#     105: 'Sg',
#     106: 'Ns',
#     107: 'Hs',
#     108: 'Mt',
#     109: '??',
#     110: '??',
#     111: '??'
# }

# # key = arbitrary integer, value = property name
# DICT_ATOMIC_PROPERTIES = {
#     0: 'Z',
#     1: 'Symbol',
#     2: 'Name',
#     3: 'Atomic weight (a.m.u.)',
#     4: 'Density (g/cm3)',
#     5: 'Solid-liquid-gas triple point  (MPa)',
#     6: 'Solid-liquid-gas triple point  (C)',
#     7: 'Melting point phase transition',
#     8: 'Melting point  (C)',
#     9: 'Boiling point  (C)',
#     10: 'Sublimation point (C)',
#     11: 'Critical point  (C)',
#     12: 'Specific heat (J/g K)',
#     13: 'X_Allen_Pauling',
#     14: 'Atomic radii (pm)',
#     15: 'Van der Waals radii (pm)',
#     16: 'Covalent radii (pm)',
#     17: 'Valence electrons',
#     18: 'Group',
#     19: 'Electron config - 1s',
#     20: 'Electron config - 2s',
#     21: 'Electron config - 2p',
#     22: 'Electron config - 3s',
#     23: 'Electron config - 3p',
#     24: 'Electron config - 3d',
#     25: 'Electron config - 4s',
#     26: 'Electron config - 4p',
#     27: 'Electron config - 4d',
#     28: 'Electron config - 4f',
#     29: 'Electron config - 5s',
#     30: 'Electron config - 5p',
#     31: 'Electron config - 5d',
#     32: 'Electron config - 5f',
#     33: 'Electron config - 6s',
#     34: 'Electron config - 6p',
#     35: 'Electron config - 6d',
#     36: 'Electron config - 7s',
#     37: 'Electron config - 7p',
#     38: 'Ionization energy (eV) - 1',
#     39: 'Ionization energy (eV) - 2',
#     40: 'Ionization energy (eV) - 3',
#     41: 'Ionization energy (eV) - 4',
#     42: 'Ionization energy (eV) - 5',
#     43: 'Ionization energy (eV) - 6',
#     44: 'Ionization energy (eV) - 7',
#     45: 'Ionization energy (eV) - 8',
#     46: 'Ionization energy (eV) - 9',
#     47: 'Ionization energy (eV) - 10',
#     48: 'Ionization energy (eV) - 11',
#     49: 'Ionization energy (eV) - 12',
#     50: 'Ionization energy (eV) - 13',
#     51: 'Ionization energy (eV) - 14',
#     52: 'Ionization energy (eV) - 15',
#     53: 'Ionization energy (eV) - 16',
#     54: 'Ionization energy (eV) - 17',
#     55: 'Ionization energy (eV) - 18',
#     56: 'Ionization energy (eV) - 19',
#     57: 'Ionization energy (eV) - 20',
#     58: 'Ionization energy (eV) - 21'
# }
# %%
