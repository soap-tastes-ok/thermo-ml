# Thermo-ML
Thermodynamics meets Machine Learning

What is Thermo-ML?
---------------

Thermo-ML is a python library for scientists in the field of thermodynamics, who want to tap into the power of machine learning to make highly accurate predictions.
 (If you have heard of ChemSage, FactSage, Thermochem, this project might interest you.)

This package will (soon) include:
1. Extensive thermodynamic database from JAFAF and other reliable sources
2. AI that learns from the database and make accurate predictions (my plan is to start with enthalpy of formation)

Who's the author?
---------------
I'm currently a machine learning engineer (director of AI dev in a startup)
who was previously doing research in computational thermodynamics @McGill University.

I will work on this after work, so please wait patiently.
If you are interested to follow this project, 
please hit the star to let me know you are there
and I'll try to work faster ;)

Installation
------------

1. Clone the repository using

`git clone https://github.com/soap-tastes-ok/thermo-ml.git`

2. Install all required dependencies using

`pip install -r /your/directory/thermo-ml/requirements.txt`

3. Append library path to system path

```
import sys
package = '/your/directory/thermo-ml'
if package not in sys.path:
    sys.path.append(package)
```