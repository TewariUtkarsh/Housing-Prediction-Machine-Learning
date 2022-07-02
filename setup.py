"""
equivalent to requirements.txt so that instead using requirements.txt, we can use setup.py
"""

from setuptools import setup
from typing import List



# Declaring Variables for setup functions
PROJECT_NAME="housing-predictor"
VERSION="0.0.1"
AUTHOR="Utkarsh Tewari"
DESCRIPTION="This is my first project for current FSDS batch"
PACKAGES=["housing"]
REQUIREMENTS_FILENAME="requirements.txt"



def get_requirements_list()->List[str]:
    """
    This function is responsible for returning the list of name of all
    the dependencies required and mentioned in requirements.txt

    Returns:
    --------
    List[str]: list
        List of string specifying the packages mentioned in requirements.txt
    
    """
    
    
    with open(REQUIREMENTS_FILENAME) as requirements_file:
        return requirements_file.readlines()





setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    packages=PACKAGES,
    install_requires=get_requirements_list()

)

