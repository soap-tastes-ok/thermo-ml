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

1. Aggregate all known physical & chemical data of atoms & compounds, so they are all accessible with once click.

2. Develop an AI that can make accurate predictions about unknown properties of elements or even completely unknown compounds, by learning the hidden relationships between the properties of compounds (e.g. enthalpy, entropy, heat capacity, etc) and the properties of its constituent atoms (e.g. ionization energy, atomic number, electronegativity, atomic radius, etc) of thousands of compounds.

    2.1 Predict enthalpy of formation of any compounds just from its chemical formula (Note: My Master's thesis ;))

    2.2 Predict electronegativity of transition metals (Note: Leland C. Allen mentioned that electronegativities are infrequently used among transition metal chemists because of the difficulty in accurately obtaining it, in his paper "Electronegativity Is the Average One-Electron Energy of the Valence-Shell Electrons in Ground-State Free Atoms" )

    2.3 Predict percentage ionic character of bonds (Note: Linus Pauling said in his book that "We cannot hope to formulate an expression for the partial ionic character of bonds that will be accurate")

    2.4. Hmm what else can I do...


Road map
========

* ``2021.03.06``

  * ✅ Started the project
  
* ``2021.03.07``
  
  * ✅ Added “parse.py” module to parse chemical formula into its constituent atoms

* ``2021.05.03``

  * ✅ Refactored “parse.py” module & added test code

  * ✅ Added "database.get_fundamental_constants" module to get major physical/chemical fundamental constants

  * ✅ Add "database.get_atoms" module to get properties of atoms (e.g. ionization energy, electronegativity, atomic radius, etc).

* ``2021.05.XX``

  * [JTBD] Add module to get thermodynamic properties of compounds (e.g. enthalpy, entropy, heat capacity, etc). 
  
    * Idea 1: Convert JANAF database to ML readable format

    * Idea 2: Convert open Thermo-Calc Database Format (TDB) to ML readable format

* ``2021.06.XX``
    
  * [JTBD] Add AI module that predicts enthalpy of formation of compounds just from its chemical formula, using properties of its constituent atoms.
  
    * Idea 1: Multilinear regression w/ constraints
    
    * Idea 2: Quadratic programming w/ constraints
    
    * Idea 3: Symbolic regression + genetic programming
    
    * Idea 4: Deep Learning

* ``2021.07.XX``

  * [JTBD] Add AI module that predicts electronegativity of all elements, including transition metals.

* ``2021.08.XX``

  * [JTBD] Add AI module that predicts percentage ionic character of bonds.

* ``2021.09.XX``

  * [JTBD] Add AI module that predicts entropy of formation of compounds just from its chemical formula, using properties of its constituent atoms.


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

1. Parsing chemical formula into atoms
--------------------------------------

To parse a chemical formula into it's constituent atoms, use the `ChemParser` module.

.. code-block:: python
    
    >>> from thermo_ml import parse
    >>> CP = parse.ChemParser()
    >>> CP.atoms("Ca2SiO3(OH)2")
    [{'Ca': 2.0, 'Si': 1.0, 'O': 5.0, 'H': 2.0}]

2. Retrieve physical & chemical properties of atoms
---------------------------------------------------

To retrieve atomic properties data, use the `database.get_atoms` module.

.. code-block:: python
    
    >>> from thermo_ml import database
    >>> df = database.get_atoms(
    >>>     atoms = ['H', 'C', 'Ca', 'Si', 'Li'],
    >>>     properties = ["Z", "Symbol", "Atomic radii (pm)", "Valence electrons"]
    >>> )

====  ===  ========  ===================  ===================
  ..    Z  Symbol      Atomic radii (pm)    Valence electrons
====  ===  ========  ===================  ===================
   0    1  H                          25                    1
   2    3  Li                        145                    1
   5    6  C                          70                    4
  13   14  Si                        110                    4
  19   20  Ca                        180                    2
====  ===  ========  ===================  ===================


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
   3  Newtonian constant of gravitation  G             6.67421e-11  m^3 kg^(-1) s^(-2)  F(r^2)/(M1 M2)                Defines the force (F) attracting two spherical bodies of mass M1 and M2, separated by a distance r.
   4  Planck constant                    h             6.62607e-34  Js                  nan                           Defines how much a photon's energy increases , when the frequency of its electromagnetic is increased by 1
   5  Reduced planck constant            ℏ             1.05457e-34  Js                  h/2π                          Defines how much a photon's energy increases , when the angular frequency (measured in radians per sec) of its electromagnetic is increased by 1
   6  Elementary charge                  e             1.60218e-19  C                   nan                           electric charge carried by a single proton or, equivalently, the magnitude of the negative electric charge carried by a single electron
   7  Magnetic flux quantum              ϕ_0           2.06783e-15  Wb                  h/2e                          Defines quantization of magnetic flux. First discovered in superconductors, where current is carried by cooper pairs of charge 2e. But the same (Aharonov-Bohm) effect has been observed in many different non-superconducting systems as well, so it's often defined as h/e instead of h/2e.
   8  Conductance quantum                G_0           7.74809e-05  S                   2e^2/h                        Quantized unit of electrical conductance
   9  Mass of electron                   m_e           9.10938e-31  kg                  nan                           Mass of a single electron
  10  Mass of proton                     m_p           1.67262e-27  kg                  nan                           Mass of a single proton
  11  Proton electron mass ratio         m_p/m_e    1836.15         nan                 nan                           Ratio of mass of proton over mass of electron
  12  Fine-structure constant            α             0.00729735   nan                 (e^2)/(4π ε_0 ħ c)            Quantifies the strength of the electromagnetic interaction between elementary charged particles.
  13  Inverse fine-structure constant    α^(-1)      137.036        nan                 nan                           nan
  14  Rydberg constant                   R_∞           1.09737e+07  m^(-1)              (α^2 m_e c)/(2 h)             The constant appearing in the Balmer formula for spectral lines of the hydrogen atom. Was first a fitting parameter, but later found by Neils Bohr as a universal constant.
  15  Avogadro constant                  N_A           6.02214e+23  mol^(-1)            nan                           A proportionality factor that relates the number of constituent particles in a sample with the amount of substance in that sample
  16  Faraday constant                   F         96485.3          C mol^(-1)          N_A e                         Magnitude of electric charge per mole of electrons
  17  Gas constant                       R             8.31447      J mol^(-1) K^(-1)   nan                           Equivalent to the Boltzmann constant, but expressed in units of energy per temperature increment per mole, i.e. the pressure–volume product, rather than energy per temperature increment per particle.
  18  Boltzmann constant                 k             1.38065e-23  J K^(-1)            R/N_A                         Relates the average relative kinetic energy of particles in a gas with the thermodynamic temperature of the gas
  19  Stefan-boltzman constant           σ             5.6704e-08   W m^(-2) K^(-4)     ((π^2 / 60) k^4) / (ℏ^3 c^2)  Constant of proportionality in Stefan-Boltzmann law of Blackbody radiation. Used to measure the amount of heat radiated from the black body, and to convert temperature (K) to units for intensity (W.m-2) which is basically Power per unit area.
  20  Electron volt                      eV            1.60218e-19  J                   e/C                           Energy gained by the charge of a single electron moved across an electric potential difference of 1 volt. Thus it is 1 volt (1 J/C) multiplied by the electron charge (1.602176565(35)×10−19 C)
  21  Unified atomic mass unit           u             1.66054e-27  kg                  (10^(-3) kg/mol ) / N_A       The dalton or unified atomic mass unit is a unit of mass widely used in physics and chemistry. It is defined as 1/12 of the mass of an unbound neutral atom of carbon-12 in its nuclear and electronic ground state and at rest
====  =================================  ========  ===============  ==================  ============================  =============================================================================================================================================================================================================================================================================================


4. ...
-----

TBD


Who’s the author?
=================

I’m currently a machine learning engineer (director of AI Dev in a
startup in Tokto) who was previously doing research in computational
thermodynamics @McGill University. (`Linkedin <https://www.linkedin.com/in/kotamatsuo2015/?locale=en_US/>`_)

I will work on this during weekends, so please wait patiently. If you are
interested to follow this project, please hit the star to let me know
you are there and I’ll try to work faster ;)


Citation
========

To cite Thermo-ML in publications, please use::

    Kota Matsuo and Contributors (2021-). Thermo-ML: Thermodynamics powered with Machine learning.
    https://github.com/soap-tastes-ok/thermo-ml.git.