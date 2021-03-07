=========
Thermo-ML
=========


:Author: Kota Matsuo ( `Linkedin <https://www.linkedin.com/in/kotamatsuo2015/?locale=en_US/>`_ )
:Version: $Revision: 0001 $

.. contents::


Thermodynamics powered by Machine Learning.

What is Thermo-ML?
------------------

Thermo-ML is a python library for scientists in the field of
thermodynamics, who want to tap into the power of machine learning to
make accurate predictions. (If you have heard of ChemSage,
FactSage, Thermochem, this project might interest you.)

This package will (soon) include:

1. Extensive thermodynamic database from JAFAF and other reliable sources

2. AI that learns from the database and make accurate predictions (my plan is to start with enthalpy of formation)

Who’s the author?
-----------------

I’m currently a machine learning engineer (director of AI Dev in a
startup in Tokto) who was previously doing research in computational
thermodynamics @McGill University. (`Linkedin <https://www.linkedin.com/in/kotamatsuo2015/?locale=en_US/>`_)

I will work on this during weekends, so please wait patiently. If you are
interested to follow this project, please hit the star to let me know
you are there and I’ll try to work faster ;)



Goal of this project
--------------------

The Goal is to make an AI that learns the relationship between
thermodynamic properties (e.g. enthalpy, entropy, heat capacity, etc)
and atomic properties (e.g. number of valence electrons,
electronegativity, atomic radius, etc) of thousands of compounds, which
then can use that learned relationships to accurately predict
thermodynamic properties of completely unknown compounds.

Road map
-------

* 2021.03.07 - [Done] added “parse.py” module to parse chemical formula into its constituent atoms 

* 2021.03.XX - [Plan] add module to calculate properties of atoms (e.g. valence electrons, electronegativity, atomic radius, etc).

* 2021.04.XX - [Plan] add module that retrieves thermodynamic properties from JANAF database (this will be used as training data for the AI) 

* 2021.04.XX - [Plan] add ML module that predicts enthalpy of formation of any chemical formula, using properties of its constituent atoms.

Installation
------------

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
-------

To parse a chemical formula into it's constituent atoms, use the `ChemParser` module.

.. code-block:: python
    
    >>> from thermo_ml import parse
    >>> CP = parse.ChemParser()
    >>> CP.atoms("Ca2SiO3(OH)2")
    [{'Ca': 2.0, 'Si': 1.0, 'O': 5.0, 'H': 2.0}]

Citation
--------

To cite Thermo-ML in publications, please use::

    Kota Matsuo and Contributors (2021-). Thermo-ML: Thermodynamics powered with Machine learning.
    https://github.com/soap-tastes-ok/thermo-ml.git.