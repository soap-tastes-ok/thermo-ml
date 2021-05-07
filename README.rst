=========
Thermo-ML
=========

-------------------------------------------
Thermodynamics powered by Machine Learning.
-------------------------------------------

:Author: Kota Matsuo ( `Linkedin <https://www.linkedin.com/in/kotamatsuo2015/?locale=en_US/>`_ )
:Version: $Revision: 0001 $

.. contents::


What is Thermo-ML?
===================

Thermo-ML is a python library for scientists in the field of
thermodynamics, who want to tap into the power of machine learning to
make accurate predictions. (If you have heard of CALPHAD, ChemSage,
FactSage, Thermochem, this project might interest you.)

Goal of this project
====================

There are two goals to this project:

1. Make physical & chemical data of atoms & compounds accessible with once click.

2. Develop an AI that accurately predicts unknown properties of elements or even unknown compounds, by learning the hidden relationships between the properties of compounds and its constituent atoms.


Road map
========

- ``Mar 2021``
  
  - ✅  Started the project
  
  - ✅  Added “parse.py” module to parse chemical formula into its constituent atoms


- ``April 2021``
  
  - ✅  Added "database.get_fundamental_constants" module to get major physical/chemical fundamental constants

- ``May 2021``

  - ✅  Refactored “parse.py” module & added test code

  - ✅  Added "database.get_atoms" module to get properties of atoms (e.g. ionization energy, electronegativity, atomic radius, etc).

  - 🛠  Add module to get thermodynamic properties of compounds (e.g. enthalpy, entropy, heat capacity, etc). 
  
    - Idea 1: Convert JANAF database to ML readable format

    - Idea 2: Convert open Thermo-Calc Database Format (TDB) to ML readable format

- ``June 2021``
    
  - 🛠  Add AI module for predicting ``enthalpy of formation`` of oxide compounds just from its chemical formula, using properties of its constituent atoms. The reason why I focus on oxides is; (1) oxides are common, and (2) to keep the charge on cations rather constant. If the charge changes, electronegativity changes, and if electronegativity changes, so does enthalpy. For more info see `[1993, Huheey] Inorgani  Chemistry - Principles of Structure and Reactivity, 4th Edition` P.184 equation 5.62 and Fig. 5.32.
  
    - Idea 1: Multilinear regression w/ constraints
    
    - Idea 2: Quadratic programming w/ constraints
    
    - Idea 3: Symbolic regression + genetic programming
    
    - Idea 4: Deep Learning

- ``July 2021``

  - 🛠  Add AI module for predicting ``electronegativity`` of elements, including transition metals.
    
    - Note: Leland C. Allen mentioned that electronegativity of transition metals are difficult to obtain, in his paper "Electronegativity Is the Average One-Electron Energy of the Valence-Shell Electrons in Ground-State Free Atoms".

- ``Aug 2021``

  - 🛠  Add AI module for predicting ``percentage ionic character of bonds``.
    
    - Note: Linus Pauling said in his book that "We cannot hope to formulate an expression for the partial ionic character of bonds that will be accurate".

- ``Sept 2021``

  - 🛠  Add AI module for predicting ``entropy of formation`` of compounds just from its chemical formula, using properties of its constituent atoms.

- ``Oct 2021``
  
  - Hmm what else can I do...


Installation
============

1. Clone the repository using

``git clone https://github.com/soap-tastes-ok/thermo-ml.git``

2. Install all required dependencies using

``pip install -r /your/directory/thermo-ml/requirements.txt``

3. Append library path to system path

::

   import sys
   package = '/your/directory/thermo-ml'
   if package not in sys.path:
       sys.path.append(package)

Examples
========

1. Parse chemical formula into atoms
--------------------------------------

To parse a chemical formula into it's constituent atoms, use the `ChemParser` module.

.. code-block:: python
    
    >>> from thermo_ml import parse
    >>> 
    >>> CP = parse.ChemParser()
    >>> CP.atoms("Ca2SiO3(OH)2")

    [{'Ca': 2.0, 'Si': 1.0, 'O': 5.0, 'H': 2.0}]

2. Retrieve physical & chemical properties of atoms
---------------------------------------------------

To retrieve atomic properties data, use the `database.get_atoms` module.

.. code-block:: python
    
    >>> from thermo_ml import database
    >>> 
    >>> atoms = ['H', 'C', 'Ca', 'Si', 'Li']
    >>> properties = [
    >>>     "Z", "Symbol", "Group", 
    >>>     "Atomic radii (pm)", 
    >>>     "Atomic weight (a.m.u.)", 
    >>>     "Valence electrons"
    >>> ]
    >>> df = database.get_atoms(atoms, properties)

===  ========  =======  ===================  ========================  ===================
  Z  Symbol      Group    Atomic radii (pm)    Atomic weight (a.m.u.)    Valence electrons
===  ========  =======  ===================  ========================  ===================
  1  H               1                   25                   1.00794                    1
  3  Li              1                  145                   6.941                      1
  6  C              14                   70                  12.0107                     4
 14  Si             14                  110                  28.0855                     4
 20  Ca              2                  180                  40.078                      2
===  ========  =======  ===================  ========================  ===================


3. Retrieve fundamental constants of physics & chemistry
--------------------------------------------------------

To retrieve fundamental constants, use the `database.get_fundamental_constants` module.

.. code-block:: python
    
    >>> from thermo_ml import database
    >>> df = database.get_fundamental_constants()

====  =================================  ========  ===============  ==================  ============================  =============================================================================================================================================================================================================================================================================================
  ..  quantity                           symbol              value  unit                formula                       Definition
====  =================================  ========  ===============  ==================  ============================  =============================================================================================================================================================================================================================================================================================
   0  Speed of light                     c             2.99792e+08  ms^(-1)             nan                           Speed of photon in vacuum
   1  Magnetic constant                  μ_0           1.25664e-06  NA^(-2)             nan                           Magnetic permeability in vacuum
   2  Electric constant                  ε_0           8.85419e-12  Fm^(-1)             nan                           Electric field permittivity in vacuum
 ...  ...                                ...           ...          ...                 ...                           ...
  19  Stefan-boltzman constant           σ             5.6704e-08   W m^(-2) K^(-4)     ((π^2 / 60) k^4) / (ℏ^3 c^2)  Constant of proportionality in Stefan-Boltzmann law of Blackbody radiation. Used to measure the amount of heat radiated from the black body, and to convert temperature (K) to units for intensity (W.m-2) which is basically Power per unit area.
  20  Electron volt                      eV            1.60218e-19  J                   e/C                           Energy gained by the charge of a single electron moved across an electric potential difference of 1 volt. Thus it is 1 volt (1 J/C) multiplied by the electron charge (1.602176565(35)×10−19 C)
  21  Unified atomic mass unit           u             1.66054e-27  kg                  (10^(-3) kg/mol ) / N_A       The dalton or unified atomic mass unit is a unit of mass widely used in physics and chemistry. It is defined as 1/12 of the mass of an unbound neutral atom of carbon-12 in its nuclear and electronic ground state and at rest
====  =================================  ========  ===============  ==================  ============================  =============================================================================================================================================================================================================================================================================================


4. Retrieve properties of compounds
-----

TBD


Who’s the author?
=================

I’m currently a machine learning engineer in Tokyo, who was previously doing research in computational
thermodynamics & developing FactSage @McGill University. (`Linkedin <https://www.linkedin.com/in/kotamatsuo2015/?locale=en_US/>`_)

I will work on this during weekends, so please wait patiently. If you are
interested to follow this project, please hit the star to let me know
you are there and I’ll try to work faster ;)


Citation
========

To cite Thermo-ML in publications, please use::

    Kota Matsuo and Contributors (2021-). Thermo-ML: Thermodynamics powered with Machine learning.
    https://github.com/soap-tastes-ok/thermo-ml.git.