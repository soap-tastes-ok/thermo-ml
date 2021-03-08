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

Goal of this project
--------------------

There are two goals to this project;

1. Aggregate all known physical & chemical data of atoms & molecules

2. Develop an AI that learns the hidden relationships between the properties of molecules (e.g. enthalpy, entropy, heat capacity, etc) and the properties of its constituent atoms (e.g. ionization energy, atomic number, electronegativity, atomic radius, etc) of thousands of compounds, which then can be used to make accurate predictions about properties of completely unknown compounds.

Road map
-------

* 2021.03.06 - [Done] Started the project

* 2021.03.07 - [Done] Added “parse.py” module to parse chemical formula into its constituent atoms 

* 2021.03.XX - [JTBD] Add module to get properties of atoms (e.g. ionization energy, electronegativity, atomic radius, etc).

* 2021.04.XX - [JTBD] Add module to get thermodynamic properties of molecules (e.g. enthalpy, entropy, heat capacity, etc). 

* 2021.04.XX - [JTBD] Add AI module that predicts enthalpy of formation of any chemical formula, using properties of its constituent atoms.

   - Idea 1: Multilinear regression w/ constraints

   - Idea 2: Quadratic programming w/ constraints
   
   - Idea 3: Symbolic regression + genetic programming
   
   - Idea 4: Deep Learning

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

Who’s the author?
-----------------

I’m currently a machine learning engineer (director of AI Dev in a
startup in Tokto) who was previously doing research in computational
thermodynamics @McGill University. (`Linkedin <https://www.linkedin.com/in/kotamatsuo2015/?locale=en_US/>`_)

I will work on this during weekends, so please wait patiently. If you are
interested to follow this project, please hit the star to let me know
you are there and I’ll try to work faster ;)


Citation
--------

To cite Thermo-ML in publications, please use::

    Kota Matsuo and Contributors (2021-). Thermo-ML: Thermodynamics powered with Machine learning.
    https://github.com/soap-tastes-ok/thermo-ml.git.