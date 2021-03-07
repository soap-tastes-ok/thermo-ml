Thermo-ML
=========


:Author: Kota Matsuo
:Version: $Revision: 0001 $

.. contents::


Thermodynamics meets Machine Learning

What is Thermo-ML?
------------------

Thermo-ML is a python library for scientists in the field of
thermodynamics, who want to tap into the power of machine learning to
make highly accurate predictions. (If you have heard of ChemSage,
FactSage, Thermochem, this project might interest you.)

This package will (soon) include: 1. Extensive thermodynamic database
from JAFAF and other reliable sources 2. AI that learns from the
database and make accurate predictions (my plan is to start with
enthalpy of formation)

Who’s the author?
-----------------

I’m currently a machine learning engineer (director of AI dev in a
startup) who was previously doing research in computational
thermodynamics @McGill University.

I will work on this after work, so please wait patiently. If you are
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

Release notes & Work plan
-------------------------

* 2020.03.07 - [Done] added “parse.py” module to parse chemical formula
into its constituent atoms 

* 2020.03.XX - [Plan] add module to calculate
properties of atoms (e.g. valence electrons, electronegativity, atomic
radius, etc).

* 2020.04.XX - [Plan] add module that retrieves
thermodynamic properties from JANAF database (this will be used as
training data for the AI) 

* 2020.04.XX - [Plan] add ML module that
predicts enthalpy of formation of any chemical formula, using properties
of its constituent atoms.

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
